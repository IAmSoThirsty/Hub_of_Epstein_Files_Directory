"""Admin session authentication routes."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter
from fastapi import Request
from fastapi import Response
from pydantic import BaseModel, Field

from ..auth import clear_admin_session_cookie
from ..auth import establish_admin_session
from ..auth import set_admin_session_cookie
from ..config import ADMIN_SESSION_TTL_SECONDS

router = APIRouter(prefix="/api/v1", tags=["auth"])


class SessionCreateRequest(BaseModel):
    """Payload for creating an authenticated admin session."""

    adminToken: str = Field(min_length=1, max_length=512)


class SessionCreateResponse(BaseModel):
    """Response for a successful admin session bootstrap."""

    status: Literal["authenticated"]
    expiresInSeconds: int
    requestId: str


class SessionDeleteResponse(BaseModel):
    """Response for clearing an admin session cookie."""

    status: Literal["logged_out"]
    requestId: str


@router.post("/auth/session", response_model=SessionCreateResponse)
def create_admin_session(
    payload: SessionCreateRequest,
    request: Request,
    response: Response,
) -> SessionCreateResponse:
    """Validate an admin token and issue a secure session cookie."""
    session_token = establish_admin_session(
        request,
        payload.adminToken.strip(),
    )
    set_admin_session_cookie(response, session_token)

    request_id = getattr(request.state, "request_id", "unknown")
    return SessionCreateResponse(
        status="authenticated",
        expiresInSeconds=ADMIN_SESSION_TTL_SECONDS,
        requestId=request_id,
    )


@router.delete("/auth/session", response_model=SessionDeleteResponse)
def clear_admin_session(
    request: Request,
    response: Response,
) -> SessionDeleteResponse:
    """Clear any existing admin session cookie."""
    clear_admin_session_cookie(response)

    request_id = getattr(request.state, "request_id", "unknown")
    return SessionDeleteResponse(status="logged_out", requestId=request_id)
