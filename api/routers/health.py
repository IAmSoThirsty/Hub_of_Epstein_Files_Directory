"""Health, readiness, and metrics endpoints."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from ..config import API_NAME, API_VERSION
from ..models import HealthResponse
from ..search_service import search_service
from ..upload_service import upload_service

router = APIRouter(tags=["health"])


@router.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness probe endpoint."""
    return HealthResponse(
        status="ok",
        service=API_NAME,
        version=API_VERSION,
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
    )


@router.get("/api/ready")
def ready() -> dict:
    """Readiness probe endpoint."""
    checks = {
        "search_index_loaded": search_service.get_index_count() > 0,
        "upload_dir_writable": upload_service.is_upload_dir_writable(),
    }
    overall_status = "ready" if all(checks.values()) else "degraded"
    return {
        "status": overall_status,
        "checks": checks,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }


@router.get("/api/metrics", response_class=PlainTextResponse)
def metrics() -> str:
    """Minimal Prometheus-compatible metrics endpoint."""
    lines = [
        "# HELP epstein_api_up API health indicator",
        "# TYPE epstein_api_up gauge",
        "epstein_api_up 1",
        "# HELP epstein_search_index_documents Loaded search records",
        "# TYPE epstein_search_index_documents gauge",
        f"epstein_search_index_documents {search_service.get_index_count()}",
        "# HELP epstein_upload_jobs_total Upload jobs tracked in-memory",
        "# TYPE epstein_upload_jobs_total gauge",
        f"epstein_upload_jobs_total {upload_service.total_jobs()}",
    ]
    return "\n".join(lines) + "\n"
