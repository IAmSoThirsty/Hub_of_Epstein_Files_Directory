"""Search API routes."""

from __future__ import annotations

from fastapi import APIRouter, Request

from ..models import SearchRequest, SearchResponse
from ..search_service import search_service

router = APIRouter(prefix="/api/v1", tags=["search"])


@router.post("/search", response_model=SearchResponse)
def search(payload: SearchRequest, request: Request) -> SearchResponse:
    """Execute search query and return matching records."""
    total, results = search_service.search(payload)
    request_id = getattr(request.state, "request_id", "unknown")
    return SearchResponse(total=total, results=results, requestId=request_id)
