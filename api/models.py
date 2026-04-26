"""Pydantic models for API requests and responses."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class SearchRequest(BaseModel):
    """Search request payload."""

    keyword: str = ""
    documentType: str = ""
    dateFrom: str = ""
    dateTo: str = ""
    location: str = ""
    locationKeyword: str = ""
    redactionStatus: List[str] = Field(default_factory=list)
    person: str = ""
    caseNumber: str = ""
    fileSource: str = ""
    relevanceScore: int = 0
    contentFlags: List[str] = Field(default_factory=list)
    sortBy: Literal[
        "relevance",
        "date-desc",
        "date-asc",
        "type",
        "location",
    ] = "relevance"
    limit: int = Field(default=100, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


class SearchResult(BaseModel):
    """Single search result record."""

    model_config = ConfigDict(extra="ignore")

    id: str
    title: str
    type: str
    date: str = ""
    location: str = "Unknown"
    redaction: str = "Unknown"
    snippet: str = ""
    tags: List[str] = Field(default_factory=list)
    relevance: int = 0
    source: str = "Public Records"
    caseNumber: Optional[str] = None


class SearchResponse(BaseModel):
    """Search response payload."""

    total: int
    results: List[SearchResult]
    requestId: str


class UploadAnalysisResult(BaseModel):
    """Result metadata for analyzed uploads."""

    relevanceScore: int
    decision: Literal["accepted", "review", "rejected"]
    keywordsMatched: List[str] = Field(default_factory=list)
    routedTo: str


class UploadAcceptedResponse(BaseModel):
    """Upload accepted response."""

    jobId: str
    status: Literal["queued"]
    statusUrl: str
    requestId: str


class UploadJobStatusResponse(BaseModel):
    """Current status for an upload job."""

    jobId: str
    status: Literal["queued", "processing", "completed", "failed"]
    filename: str
    source: str
    createdAt: str
    updatedAt: str
    completedAt: Optional[str] = None
    result: Optional[UploadAnalysisResult] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health endpoint response."""

    status: Literal["ok"]
    service: str
    version: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Consistent API error shape."""

    detail: str
    requestId: str
    errors: Optional[List[Dict[str, Any]]] = None
