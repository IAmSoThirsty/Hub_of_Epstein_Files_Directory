"""Upload service for async intake and lightweight relevance scoring."""

from __future__ import annotations

import json
import re
import shutil
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi import UploadFile

from .config import ENABLE_UPLOAD_QUARANTINE
from .config import JOB_STORE_PATH
from .config import MAX_UPLOAD_MB
from .config import UPLOAD_DIR
from .config import UPLOAD_QUARANTINE_DIR
from .config import ensure_runtime_directories


class UploadService:
    """Tracks upload jobs and processes file relevance asynchronously."""

    def __init__(
        self,
        upload_dir: Optional[Path] = None,
        jobs_store_path: Optional[Path] = None,
        max_upload_mb: Optional[int] = None,
        quarantine_dir: Optional[Path] = None,
        enable_upload_quarantine: Optional[bool] = None,
    ) -> None:
        ensure_runtime_directories()
        self.upload_dir = upload_dir or UPLOAD_DIR
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        self.enable_upload_quarantine = (
            ENABLE_UPLOAD_QUARANTINE
            if enable_upload_quarantine is None
            else enable_upload_quarantine
        )
        self.quarantine_dir = quarantine_dir or UPLOAD_QUARANTINE_DIR
        if self.enable_upload_quarantine:
            self.quarantine_dir.mkdir(parents=True, exist_ok=True)

        self.jobs_store_path = jobs_store_path or JOB_STORE_PATH
        self.jobs_store_path.parent.mkdir(parents=True, exist_ok=True)

        max_upload = MAX_UPLOAD_MB if max_upload_mb is None else max_upload_mb
        self.max_upload_bytes = max_upload * 1024 * 1024
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        with self._lock:
            self._load_jobs_from_disk()

    def _safe_filename(self, filename: Optional[str], fallback: str) -> str:
        return re.sub(
            r"[^a-zA-Z0-9_.-]+",
            "_",
            filename or fallback,
        )

    def create_job(
        self,
        filename: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create and register a new upload job."""
        now = self._now()
        job_id = uuid4().hex
        with self._lock:
            self._jobs[job_id] = {
                "jobId": job_id,
                "status": "queued",
                "filename": filename,
                "source": source or "unknown",
                "metadata": metadata or {},
                "createdAt": now,
                "updatedAt": now,
                "completedAt": None,
                "result": None,
                "error": None,
            }
            self._persist_jobs_locked()
        return job_id

    def save_file(self, job_id: str, upload: UploadFile) -> Path:
        """Persist the uploaded file to storage, enforcing size limits."""
        safe_name = self._safe_filename(upload.filename, "upload.pdf")
        file_path = self.upload_dir / f"{job_id}_{safe_name}"

        total_written = 0
        with file_path.open("wb") as handle:
            while True:
                chunk = upload.file.read(1024 * 1024)
                if not chunk:
                    break
                total_written += len(chunk)
                if total_written > self.max_upload_bytes:
                    handle.close()
                    file_path.unlink(missing_ok=True)
                    raise ValueError("File exceeds maximum allowed size")
                handle.write(chunk)

        return file_path

    def save_to_quarantine(
        self,
        upload: UploadFile,
        reason: str,
        source: str = "unknown",
    ) -> Optional[Path]:
        """Persist suspicious uploads to quarantine for manual review."""
        if not self.enable_upload_quarantine:
            return None

        if upload.file is None:
            return None

        quarantine_id = uuid4().hex
        safe_name = self._safe_filename(
            upload.filename,
            "suspicious-upload.bin",
        )
        quarantine_path = self.quarantine_dir / f"{quarantine_id}_{safe_name}"

        try:
            original_position = upload.file.tell()
        except (AttributeError, OSError):
            original_position = None

        truncated = False
        total_written = 0
        try:
            if original_position is not None:
                upload.file.seek(0)

            with quarantine_path.open("wb") as handle:
                while True:
                    chunk = upload.file.read(1024 * 1024)
                    if not chunk:
                        break

                    remaining = self.max_upload_bytes - total_written
                    if remaining <= 0:
                        truncated = True
                        break

                    to_write = chunk[:remaining]
                    handle.write(to_write)
                    total_written += len(to_write)

                    if len(chunk) > remaining:
                        truncated = True
                        break

            self._write_quarantine_metadata(
                quarantine_path=quarantine_path,
                quarantine_id=quarantine_id,
                filename=upload.filename or "",
                content_type=upload.content_type or "",
                reason=reason,
                source=source,
                bytes_captured=total_written,
                truncated=truncated,
            )
            return quarantine_path
        finally:
            if original_position is not None:
                try:
                    upload.file.seek(original_position)
                except OSError:
                    pass

    def quarantine_saved_file(
        self,
        file_path: Path,
        reason: str,
        source: str = "unknown",
        move_file: bool = True,
    ) -> Optional[Path]:
        """Quarantine an already-saved file by moving or copying it."""
        if not self.enable_upload_quarantine:
            return None

        if not file_path.exists():
            return None

        quarantine_id = uuid4().hex
        safe_name = self._safe_filename(file_path.name, "quarantine-file.bin")
        quarantine_path = self.quarantine_dir / f"{quarantine_id}_{safe_name}"

        if move_file:
            file_path.replace(quarantine_path)
        else:
            shutil.copy2(file_path, quarantine_path)

        bytes_captured = quarantine_path.stat().st_size
        self._write_quarantine_metadata(
            quarantine_path=quarantine_path,
            quarantine_id=quarantine_id,
            filename=file_path.name,
            content_type="",
            reason=reason,
            source=source,
            bytes_captured=bytes_captured,
            truncated=False,
        )

        return quarantine_path

    def _write_quarantine_metadata(
        self,
        quarantine_path: Path,
        quarantine_id: str,
        filename: str,
        content_type: str,
        reason: str,
        source: str,
        bytes_captured: int,
        truncated: bool,
    ) -> None:
        metadata_path = quarantine_path.with_suffix(
            f"{quarantine_path.suffix}.json"
        )
        metadata_path.write_text(
            json.dumps(
                {
                    "quarantineId": quarantine_id,
                    "filename": filename,
                    "contentType": content_type,
                    "reason": reason,
                    "source": source,
                    "bytesCaptured": bytes_captured,
                    "truncated": truncated,
                    "createdAt": self._now(),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def process_upload(self, job_id: str, file_path: Path) -> None:
        """Process a saved upload and update job state."""
        self._update_job(job_id, status="processing")
        try:
            text = file_path.read_bytes()[:2_000_000].decode(
                "utf-8",
                errors="ignore",
            )
            score, matched_keywords = self._score_relevance(
                text,
                file_path.name,
            )

            if score >= 70:
                decision = "accepted"
                routed_to = "indexed"
            elif score >= 40:
                decision = "review"
                routed_to = "review"
            else:
                decision = "rejected"
                routed_to = "trash"

            result = {
                "relevanceScore": score,
                "decision": decision,
                "keywordsMatched": matched_keywords,
                "routedTo": routed_to,
            }
            self._update_job(
                job_id,
                status="completed",
                completedAt=self._now(),
                result=result,
            )
        except Exception as exc:  # pylint: disable=broad-except
            self._update_job(
                job_id,
                status="failed",
                completedAt=self._now(),
                error=str(exc),
            )

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get upload job details if present."""
        with self._lock:
            record = self._jobs.get(job_id)
            if not record:
                return None
            return deepcopy(record)

    def total_jobs(self) -> int:
        """Get number of tracked jobs."""
        with self._lock:
            return len(self._jobs)

    def is_upload_dir_writable(self) -> bool:
        """Check if the upload directory can be written to."""
        try:
            test_path = self.upload_dir / ".write_test"
            test_path.write_text("ok", encoding="utf-8")
            test_path.unlink(missing_ok=True)
            return True
        except OSError:
            return False

    def _update_job(self, job_id: str, **changes: Any) -> None:
        with self._lock:
            if job_id not in self._jobs:
                return
            self._jobs[job_id].update(changes)
            self._jobs[job_id]["updatedAt"] = self._now()
            self._persist_jobs_locked()

    def _load_jobs_from_disk(self) -> None:
        if not self.jobs_store_path.exists():
            return

        try:
            payload = json.loads(
                self.jobs_store_path.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError):
            return

        if not isinstance(payload, dict):
            return

        loaded_jobs: Dict[str, Dict[str, Any]] = {}
        for job_id, record in payload.items():
            if isinstance(job_id, str) and isinstance(record, dict):
                loaded_jobs[job_id] = record

        self._jobs = loaded_jobs

    def _persist_jobs_locked(self) -> None:
        temp_path = self.jobs_store_path.with_suffix(
            f"{self.jobs_store_path.suffix}.tmp"
        )

        try:
            temp_path.write_text(
                json.dumps(
                    self._jobs,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            temp_path.replace(self.jobs_store_path)
        except OSError:
            return

    def _score_relevance(
        self,
        text: str,
        filename: str,
    ) -> tuple[int, list[str]]:
        keyword_weights = {
            "epstein": 20,
            "maxwell": 15,
            "little st. james": 20,
            "flight": 10,
            "manifest": 8,
            "court": 10,
            "deposition": 10,
            "victim": 10,
            "palm beach": 10,
            "manhattan": 8,
        }

        corpus = f"{filename} {text}".lower()
        score = 5
        matched: list[str] = []

        for keyword, weight in keyword_weights.items():
            if keyword in corpus:
                score += weight
                matched.append(keyword)

        if filename.lower().endswith(".pdf"):
            score += 5

        return min(score, 100), matched

    def _now(self) -> str:
        return datetime.now(tz=timezone.utc).isoformat()


upload_service = UploadService()
