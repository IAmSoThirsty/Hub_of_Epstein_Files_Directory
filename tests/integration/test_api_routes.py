"""Integration tests for API route behavior and auth controls."""

from __future__ import annotations

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from api.config import ADMIN_API_TOKEN, AUTH_RATE_LIMIT_MAX_ATTEMPTS
from api.main import app


client = TestClient(app)


@pytest.mark.integration
def test_request_id_header_is_propagated() -> None:
    request_id = f"integration-{uuid4().hex}"

    response = client.get(
        "/api/health",
        headers={"X-Request-ID": request_id},
    )

    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == request_id


@pytest.mark.integration
def test_search_validation_error_shape_includes_request_id() -> None:
    response = client.post(
        "/api/v1/search",
        json={"sortBy": "not-a-valid-sort-order"},
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["detail"] == "Validation error"
    assert payload["requestId"]
    assert isinstance(payload["errors"], list)
    assert payload["errors"]


@pytest.mark.integration
def test_upload_status_accepts_x_admin_token_header() -> None:
    response = client.get(
        "/api/v1/upload/non-existent-job",
        headers={
            "X-Admin-Token": ADMIN_API_TOKEN,
            "X-Forwarded-For": f"xff-{uuid4().hex}",
        },
    )

    # Auth succeeded; endpoint reached and missing job was returned.
    assert response.status_code == 404


@pytest.mark.integration
def test_upload_rejects_invalid_metadata_json() -> None:
    response = client.post(
        "/api/v1/upload",
        headers={
            "Authorization": f"Bearer {ADMIN_API_TOKEN}",
            "X-Forwarded-For": f"xff-{uuid4().hex}",
        },
        files={"file": ("doc.pdf", b"epstein", "application/pdf")},
        data={"metadata": "not-json"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "metadata must be valid JSON"


@pytest.mark.integration
def test_auth_session_cookie_allows_admin_route_access() -> None:
    scoped_client = TestClient(app)
    forwarded_for = f"session-auth-{uuid4().hex}"

    login_response = scoped_client.post(
        "/api/v1/auth/session",
        json={"adminToken": ADMIN_API_TOKEN},
        headers={"X-Forwarded-For": forwarded_for},
    )

    assert login_response.status_code == 200
    assert "set-cookie" in login_response.headers

    authorized_status = scoped_client.get(
        "/api/v1/upload/non-existent-job",
        headers={"X-Forwarded-For": forwarded_for},
    )

    # Cookie-based admin session is accepted.
    assert authorized_status.status_code == 404


@pytest.mark.integration
def test_auth_session_rejects_invalid_bootstrap_token() -> None:
    scoped_client = TestClient(app)

    login_response = scoped_client.post(
        "/api/v1/auth/session",
        json={"adminToken": "invalid-token"},
        headers={"X-Forwarded-For": f"session-auth-{uuid4().hex}"},
    )

    assert login_response.status_code == 401


@pytest.mark.integration
def test_auth_session_logout_clears_cookie_access() -> None:
    scoped_client = TestClient(app)
    forwarded_for = f"session-logout-{uuid4().hex}"

    login_response = scoped_client.post(
        "/api/v1/auth/session",
        json={"adminToken": ADMIN_API_TOKEN},
        headers={"X-Forwarded-For": forwarded_for},
    )
    assert login_response.status_code == 200

    logout_response = scoped_client.delete(
        "/api/v1/auth/session",
        headers={"X-Forwarded-For": forwarded_for},
    )
    assert logout_response.status_code == 200

    unauthorized_status = scoped_client.get(
        "/api/v1/upload/non-existent-job",
        headers={"X-Forwarded-For": forwarded_for},
    )
    assert unauthorized_status.status_code == 401


@pytest.mark.integration
def test_successful_session_bootstrap_clears_failed_attempts() -> None:
    scoped_client = TestClient(app)
    forwarded_for = f"session-reset-{uuid4().hex}"

    for _ in range(AUTH_RATE_LIMIT_MAX_ATTEMPTS - 1):
        invalid_response = scoped_client.post(
            "/api/v1/auth/session",
            json={"adminToken": "invalid-token"},
            headers={"X-Forwarded-For": forwarded_for},
        )
        assert invalid_response.status_code == 401

    first_success = scoped_client.post(
        "/api/v1/auth/session",
        json={"adminToken": ADMIN_API_TOKEN},
        headers={"X-Forwarded-For": forwarded_for},
    )
    assert first_success.status_code == 200

    for _ in range(AUTH_RATE_LIMIT_MAX_ATTEMPTS - 1):
        invalid_response = scoped_client.post(
            "/api/v1/auth/session",
            json={"adminToken": "invalid-token"},
            headers={"X-Forwarded-For": forwarded_for},
        )
        assert invalid_response.status_code == 401

    second_success = scoped_client.post(
        "/api/v1/auth/session",
        json={"adminToken": ADMIN_API_TOKEN},
        headers={"X-Forwarded-For": forwarded_for},
    )
    assert second_success.status_code == 200


@pytest.mark.integration
def test_auth_rate_limit_is_scoped_by_client_identifier() -> None:
    client_a = f"rate-limit-a-{uuid4().hex}"
    client_b = f"rate-limit-b-{uuid4().hex}"

    for _ in range(AUTH_RATE_LIMIT_MAX_ATTEMPTS):
        response = client.get(
            "/api/v1/upload/non-existent-job",
            headers={
                "Authorization": "Bearer invalid-token",
                "X-Forwarded-For": client_a,
            },
        )
        assert response.status_code == 401

    blocked_response = client.get(
        "/api/v1/upload/non-existent-job",
        headers={
            "Authorization": "Bearer invalid-token",
            "X-Forwarded-For": client_a,
        },
    )
    assert blocked_response.status_code == 429

    other_client_response = client.get(
        "/api/v1/upload/non-existent-job",
        headers={
            "Authorization": "Bearer invalid-token",
            "X-Forwarded-For": client_b,
        },
    )
    assert other_client_response.status_code == 401
