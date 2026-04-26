"""Upload intake and job status routes."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import UploadFile, status
from pypdf import PdfReader

from ..auth import require_admin_token
from ..config import MALWARE_SCAN_FAIL_CLOSED
from ..malware_scan import scan_file_for_malware
from ..models import UploadAcceptedResponse, UploadJobStatusResponse
from ..upload_service import upload_service

router = APIRouter(prefix="/api/v1", tags=["uploads"])

PDF_SIGNATURE = b"%PDF-"
ALLOWED_PDF_MIME_TYPES = {
    "application/pdf",
    "application/x-pdf",
    "application/acrobat",
    "applications/vnd.pdf",
    "text/pdf",
}


def _mime_type_is_pdf(upload: UploadFile) -> bool:
    """Return True when content type is empty or a known PDF MIME type."""
    content_type = (upload.content_type or "").split(";", maxsplit=1)[0]
    content_type = content_type.strip().lower()

    if not content_type:
        return True
    return content_type in ALLOWED_PDF_MIME_TYPES


def _has_pdf_signature(upload: UploadFile) -> bool:
    """Return True when the upload stream begins with PDF magic bytes."""
    if upload.file is None:
        return False

    try:
        original_position = upload.file.tell()
    except (AttributeError, OSError):
        original_position = None

    reset_failed = False
    try:
        header = upload.file.read(len(PDF_SIGNATURE))
    except OSError:
        return False
    finally:
        if original_position is not None:
            try:
                upload.file.seek(original_position)
            except OSError:
                reset_failed = True

    if reset_failed:
        return False

    if not isinstance(header, (bytes, bytearray)):
        return False
    return bytes(header).startswith(PDF_SIGNATURE)


def _has_valid_pdf_structure(upload: UploadFile) -> bool:
    """Return True when pypdf can parse at least one page from the upload."""
    if upload.file is None:
        return False

    try:
        original_position = upload.file.tell()
    except (AttributeError, OSError):
        original_position = None

    reset_failed = False
    is_valid = False
    try:
        upload.file.seek(0)
        reader = PdfReader(upload.file, strict=False)
        is_valid = len(reader.pages) >= 1
    except Exception:  # pylint: disable=broad-except
        is_valid = False
    finally:
        if original_position is not None:
            try:
                upload.file.seek(original_position)
            except OSError:
                reset_failed = True

    return is_valid and not reset_failed


def _quarantine_if_suspicious(
    file: UploadFile,
    source: str,
    reason: str,
) -> None:
    """Best-effort quarantine hook for suspicious uploads."""
    try:
        upload_service.save_to_quarantine(file, reason=reason, source=source)
    except Exception:  # pylint: disable=broad-except
        # Quarantine must never block API response flow.
        return


def _quarantine_saved_if_suspicious(
    source: str,
    reason: str,
    file_path,
    move_file: bool,
) -> None:
    """Best-effort quarantine hook for already saved files."""
    try:
        upload_service.quarantine_saved_file(
            file_path,
            reason=reason,
            source=source,
            move_file=move_file,
        )
    except Exception:  # pylint: disable=broad-except
        return


@router.post(
    "/upload",
    response_model=UploadAcceptedResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def upload_document(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    source: str = Form("manual"),
    metadata: Optional[str] = Form(None),
    _token: str = Depends(require_admin_token),
) -> UploadAcceptedResponse:
    """Accept a PDF upload and queue it for asynchronous processing."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    parsed_metadata: Dict[str, Any] = {}
    if metadata:
        try:
            parsed_metadata = json.loads(metadata)
        except json.JSONDecodeError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="metadata must be valid JSON",
            ) from exc

    if not _mime_type_is_pdf(file):
        _quarantine_if_suspicious(
            file=file,
            source=source,
            reason="mime-type-not-pdf",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid PDF",
        )

    if not _has_pdf_signature(file):
        _quarantine_if_suspicious(
            file=file,
            source=source,
            reason="missing-pdf-signature",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid PDF",
        )

    if not _has_valid_pdf_structure(file):
        _quarantine_if_suspicious(
            file=file,
            source=source,
            reason="pdf-structure-parse-failed",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid PDF",
        )

    job_id = upload_service.create_job(
        filename=file.filename,
        source=source,
        metadata=parsed_metadata,
    )

    try:
        file_path = upload_service.save_file(job_id=job_id, upload=file)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(exc),
        ) from exc

    scan_result = scan_file_for_malware(file_path)
    if scan_result.status == "infected":
        _quarantine_saved_if_suspicious(
            source=source,
            reason=f"malware-detected:{scan_result.details}",
            file_path=file_path,
            move_file=True,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file failed malware scan",
        )

    if scan_result.status == "error":
        _quarantine_saved_if_suspicious(
            source=source,
            reason=f"malware-scan-error:{scan_result.details}",
            file_path=file_path,
            move_file=MALWARE_SCAN_FAIL_CLOSED,
        )
        if MALWARE_SCAN_FAIL_CLOSED:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Malware scanner unavailable",
            )

    background_tasks.add_task(upload_service.process_upload, job_id, file_path)

    request_id = getattr(request.state, "request_id", "unknown")
    return UploadAcceptedResponse(
        jobId=job_id,
        status="queued",
        statusUrl=f"/api/v1/upload/{job_id}",
        requestId=request_id,
    )


@router.get("/upload/{job_id}", response_model=UploadJobStatusResponse)
def get_upload_status(
    job_id: str,
    _token: str = Depends(require_admin_token),
) -> UploadJobStatusResponse:
    """Return status and analysis details for an upload job."""
    job = upload_service.get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload job not found",
        )

    return UploadJobStatusResponse(**job)
