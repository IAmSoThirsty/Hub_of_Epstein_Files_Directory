"""Authentication helpers for admin-only endpoints."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import secrets
import time
from typing import Optional

from fastapi import Header, HTTPException, Request, Response, status

from .config import ADMIN_API_TOKENS
from .config import ADMIN_SESSION_COOKIE_NAME
from .config import ADMIN_SESSION_COOKIE_SECURE
from .config import ADMIN_SESSION_SECRET
from .config import ADMIN_SESSION_TTL_SECONDS
from .rate_limit_store import create_rate_limit_store


AUTH_HEADER_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)

AUTH_RATE_LIMIT_ERROR = HTTPException(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    detail="Too many authentication attempts. Try again later.",
)

_RATE_LIMIT_STORE = create_rate_limit_store()


def _client_identifier(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        return forwarded_for.split(",", maxsplit=1)[0].strip()

    client = request.client.host if request.client else ""
    return client or "unknown"


def _record_failed_attempt(client_id: str) -> None:
    _RATE_LIMIT_STORE.record_failed_attempt(client_id)


def _clear_failed_attempts(client_id: str) -> None:
    _RATE_LIMIT_STORE.clear_failed_attempts(client_id)


def _is_rate_limited(client_id: str) -> bool:
    return _RATE_LIMIT_STORE.is_rate_limited(client_id)


def _extract_bearer_token(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        return None

    token = token.strip()
    return token if token else None


def _session_secret_bytes() -> bytes:
    return ADMIN_SESSION_SECRET.encode("utf-8")


def _urlsafe_b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _urlsafe_b64decode(value: str) -> Optional[bytes]:
    padding = "=" * (-len(value) % 4)
    try:
        return base64.urlsafe_b64decode(value + padding)
    except (ValueError, binascii.Error):
        return None


def validate_admin_api_token(token: str) -> bool:
    """Return True when token matches one configured admin token."""
    return any(
        secrets.compare_digest(token, admin_token)
        for admin_token in ADMIN_API_TOKENS
    )


def create_admin_session_token() -> str:
    """Create a signed, short-lived session token for admin endpoints."""
    payload = {
        "exp": int(time.time()) + ADMIN_SESSION_TTL_SECONDS,
        "nonce": secrets.token_urlsafe(16),
    }
    payload_raw = json.dumps(
        payload,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    payload_part = _urlsafe_b64encode(payload_raw)

    signature_raw = hmac.new(
        _session_secret_bytes(),
        payload_part.encode("ascii"),
        hashlib.sha256,
    ).digest()
    signature_part = _urlsafe_b64encode(signature_raw)

    return f"{payload_part}.{signature_part}"


def _session_token_is_valid(session_token: str) -> bool:
    payload_part, separator, signature_part = session_token.partition(".")
    if not separator or not payload_part or not signature_part:
        return False

    provided_signature = _urlsafe_b64decode(signature_part)
    if provided_signature is None:
        return False

    expected_signature = hmac.new(
        _session_secret_bytes(),
        payload_part.encode("ascii"),
        hashlib.sha256,
    ).digest()
    if not hmac.compare_digest(provided_signature, expected_signature):
        return False

    payload_raw = _urlsafe_b64decode(payload_part)
    if payload_raw is None:
        return False

    try:
        payload = json.loads(payload_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False

    expires_at = payload.get("exp")
    if not isinstance(expires_at, int):
        return False

    return expires_at > int(time.time())


def set_admin_session_cookie(response: Response, session_token: str) -> None:
    """Set a secure, HTTP-only cookie carrying admin session state."""
    response.set_cookie(
        key=ADMIN_SESSION_COOKIE_NAME,
        value=session_token,
        httponly=True,
        secure=ADMIN_SESSION_COOKIE_SECURE,
        samesite="lax",
        max_age=ADMIN_SESSION_TTL_SECONDS,
        path="/",
    )


def clear_admin_session_cookie(response: Response) -> None:
    """Clear the admin session cookie."""
    response.delete_cookie(
        key=ADMIN_SESSION_COOKIE_NAME,
        path="/",
        secure=ADMIN_SESSION_COOKIE_SECURE,
        samesite="lax",
    )


def establish_admin_session(request: Request, admin_token: str) -> str:
    """Validate an admin token and issue a signed cookie session token."""
    client_id = _client_identifier(request)
    if _is_rate_limited(client_id):
        raise AUTH_RATE_LIMIT_ERROR

    if not validate_admin_api_token(admin_token):
        _record_failed_attempt(client_id)
        raise AUTH_HEADER_ERROR

    _clear_failed_attempts(client_id)
    return create_admin_session_token()


def require_admin_token(
    request: Request,
    authorization: Optional[str] = Header(default=None),
    x_admin_token: Optional[str] = Header(default=None, alias="X-Admin-Token"),
) -> str:
    """Require a matching Bearer token for admin write operations."""
    client_id = _client_identifier(request)
    if _is_rate_limited(client_id):
        raise AUTH_RATE_LIMIT_ERROR

    token = _extract_bearer_token(authorization)
    if not token and x_admin_token:
        stripped = x_admin_token.strip()
        token = stripped if stripped else None

    if token:
        if validate_admin_api_token(token):
            _clear_failed_attempts(client_id)
            return token

        _record_failed_attempt(client_id)
        raise AUTH_HEADER_ERROR

    session_token = request.cookies.get(ADMIN_SESSION_COOKIE_NAME)
    if session_token and _session_token_is_valid(session_token):
        _clear_failed_attempts(client_id)
        return "session"

    _record_failed_attempt(client_id)
    raise AUTH_HEADER_ERROR
