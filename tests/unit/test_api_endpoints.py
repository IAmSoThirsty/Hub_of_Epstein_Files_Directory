"""Unit tests for API wave-1 endpoints."""

from io import BytesIO

from fastapi.testclient import TestClient
from pypdf import PdfWriter
from starlette.datastructures import UploadFile

from api.malware_scan import MalwareScanResult
from api.routers import uploads as upload_routes
from api.main import app
from api.upload_service import UploadService


client = TestClient(app)


def _build_valid_pdf_bytes() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    stream = BytesIO()
    writer.write(stream)
    return stream.getvalue()


def test_health_endpoint_is_ok() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "version" in payload


def test_search_endpoint_returns_records() -> None:
    response = client.post(
        "/api/v1/search",
        json={
            "keyword": "flight",
            "sortBy": "relevance",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] >= 1
    assert len(payload["results"]) >= 1
    assert "requestId" in payload


def test_search_document_type_filter() -> None:
    response = client.post(
        "/api/v1/search",
        json={
            "documentType": "flight-log",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] >= 1
    assert all("flight" in item["type"].lower() for item in payload["results"])


def test_upload_requires_auth() -> None:
    response = client.post(
        "/api/v1/upload",
        files={"file": ("doc.pdf", b"epstein", "application/pdf")},
    )

    assert response.status_code == 401


def test_upload_rejects_invalid_token() -> None:
    response = client.post(
        "/api/v1/upload",
        headers={"Authorization": "Bearer invalid-token"},
        files={"file": ("doc.pdf", b"epstein", "application/pdf")},
    )

    assert response.status_code == 401


def test_upload_accepts_pdf_and_tracks_job() -> None:
    headers = {"Authorization": "Bearer change-me-dev-token"}
    pdf_bytes = _build_valid_pdf_bytes()
    response = client.post(
        "/api/v1/upload",
        headers=headers,
        files={
            "file": (
                "flight_evidence.pdf",
                pdf_bytes,
                "application/pdf",
            ),
        },
        data={"source": "unit-test"},
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["status"] == "queued"

    unauthorized_status = client.get(f"/api/v1/upload/{payload['jobId']}")
    assert unauthorized_status.status_code == 401

    status_response = client.get(
        f"/api/v1/upload/{payload['jobId']}",
        headers=headers,
    )
    assert status_response.status_code == 200
    status_payload = status_response.json()
    assert status_payload["status"] in {
        "queued",
        "processing",
        "completed",
        "failed",
    }


def test_upload_rejects_non_pdf_content_with_pdf_extension() -> None:
    headers = {"Authorization": "Bearer change-me-dev-token"}
    response = client.post(
        "/api/v1/upload",
        headers=headers,
        files={
            "file": (
                "masquerading.pdf",
                b"This is plain text, not a PDF signature",
                "application/pdf",
            ),
        },
        data={"source": "unit-test"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is not a valid PDF"


def test_upload_rejects_non_pdf_mime_type() -> None:
    headers = {"Authorization": "Bearer change-me-dev-token"}
    response = client.post(
        "/api/v1/upload",
        headers=headers,
        files={
            "file": (
                "valid-looking.pdf",
                (
                    b"%PDF-1.4\n"
                    b"1 0 obj\n<< /Type /Catalog >>\nendobj\n"
                    b"trailer\n<< /Root 1 0 R >>\n%%EOF"
                ),
                "text/plain",
            ),
        },
        data={"source": "unit-test"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is not a valid PDF"


def test_upload_rejects_malformed_pdf_structure() -> None:
    headers = {"Authorization": "Bearer change-me-dev-token"}
    response = client.post(
        "/api/v1/upload",
        headers=headers,
        files={
            "file": (
                "broken.pdf",
                b"%PDF-1.7\nthis is not a valid PDF structure",
                "application/pdf",
            ),
        },
        data={"source": "unit-test"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is not a valid PDF"


def test_upload_rejects_malware_detected(monkeypatch) -> None:
    headers = {"Authorization": "Bearer change-me-dev-token"}
    pdf_bytes = _build_valid_pdf_bytes()

    monkeypatch.setattr(
        upload_routes,
        "scan_file_for_malware",
        lambda _file_path: MalwareScanResult(
            status="infected",
            details="eicar-signature",
        ),
    )

    response = client.post(
        "/api/v1/upload",
        headers=headers,
        files={
            "file": (
                "infected.pdf",
                pdf_bytes,
                "application/pdf",
            ),
        },
        data={"source": "unit-test"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file failed malware scan"


def test_upload_fail_closed_on_scanner_error(monkeypatch) -> None:
    headers = {"Authorization": "Bearer change-me-dev-token"}
    pdf_bytes = _build_valid_pdf_bytes()

    monkeypatch.setattr(upload_routes, "MALWARE_SCAN_FAIL_CLOSED", True)
    monkeypatch.setattr(
        upload_routes,
        "scan_file_for_malware",
        lambda _file_path: MalwareScanResult(
            status="error",
            details="scanner-timeout",
        ),
    )

    response = client.post(
        "/api/v1/upload",
        headers=headers,
        files={
            "file": (
                "timeout.pdf",
                pdf_bytes,
                "application/pdf",
            ),
        },
        data={"source": "unit-test"},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "Malware scanner unavailable"


def test_upload_fail_open_on_scanner_error(monkeypatch) -> None:
    headers = {"Authorization": "Bearer change-me-dev-token"}
    pdf_bytes = _build_valid_pdf_bytes()

    monkeypatch.setattr(upload_routes, "MALWARE_SCAN_FAIL_CLOSED", False)
    monkeypatch.setattr(
        upload_routes,
        "scan_file_for_malware",
        lambda _file_path: MalwareScanResult(
            status="error",
            details="scanner-timeout",
        ),
    )

    response = client.post(
        "/api/v1/upload",
        headers=headers,
        files={
            "file": (
                "timeout-open.pdf",
                pdf_bytes,
                "application/pdf",
            ),
        },
        data={"source": "unit-test"},
    )

    assert response.status_code == 202


def test_upload_service_persists_jobs(tmp_path) -> None:
    upload_dir = tmp_path / "uploads"
    jobs_store = upload_dir / "jobs.json"

    service = UploadService(
        upload_dir=upload_dir,
        jobs_store_path=jobs_store,
        max_upload_mb=1,
    )
    job_id = service.create_job(
        filename="persisted.pdf",
        source="unit-test",
        metadata={"origin": "pytest"},
    )

    reloaded_service = UploadService(
        upload_dir=upload_dir,
        jobs_store_path=jobs_store,
        max_upload_mb=1,
    )
    restored_job = reloaded_service.get_job(job_id)

    assert restored_job is not None
    assert restored_job["filename"] == "persisted.pdf"
    assert restored_job["source"] == "unit-test"


def test_upload_service_quarantine_saves_file_and_metadata(tmp_path) -> None:
    upload_dir = tmp_path / "uploads"
    quarantine_dir = tmp_path / "quarantine"
    jobs_store = upload_dir / "jobs.json"

    service = UploadService(
        upload_dir=upload_dir,
        jobs_store_path=jobs_store,
        quarantine_dir=quarantine_dir,
        enable_upload_quarantine=True,
        max_upload_mb=1,
    )

    upload = UploadFile(
        file=BytesIO(b"suspicious content"),
        filename="suspicious.pdf",
    )

    quarantined_path = service.save_to_quarantine(
        upload,
        reason="unit-test-suspicious",
        source="unit-test",
    )

    assert quarantined_path is not None
    assert quarantined_path.exists()

    metadata_path = quarantined_path.with_suffix(
        f"{quarantined_path.suffix}.json"
    )
    assert metadata_path.exists()


def test_upload_service_quarantine_saved_file_move(tmp_path) -> None:
    upload_dir = tmp_path / "uploads"
    quarantine_dir = tmp_path / "quarantine"
    jobs_store = upload_dir / "jobs.json"

    service = UploadService(
        upload_dir=upload_dir,
        jobs_store_path=jobs_store,
        quarantine_dir=quarantine_dir,
        enable_upload_quarantine=True,
        max_upload_mb=1,
    )

    file_path = upload_dir / "to-move.pdf"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(b"dummy")

    quarantined_path = service.quarantine_saved_file(
        file_path,
        reason="move-test",
        source="unit-test",
        move_file=True,
    )

    assert quarantined_path is not None
    assert quarantined_path.exists()
    assert not file_path.exists()


def test_upload_service_quarantine_saved_file_copy(tmp_path) -> None:
    upload_dir = tmp_path / "uploads"
    quarantine_dir = tmp_path / "quarantine"
    jobs_store = upload_dir / "jobs.json"

    service = UploadService(
        upload_dir=upload_dir,
        jobs_store_path=jobs_store,
        quarantine_dir=quarantine_dir,
        enable_upload_quarantine=True,
        max_upload_mb=1,
    )

    file_path = upload_dir / "to-copy.pdf"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(b"dummy")

    quarantined_path = service.quarantine_saved_file(
        file_path,
        reason="copy-test",
        source="unit-test",
        move_file=False,
    )

    assert quarantined_path is not None
    assert quarantined_path.exists()
    assert file_path.exists()
