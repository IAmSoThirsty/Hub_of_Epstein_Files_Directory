"""Runtime configuration for the API service."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final, List


def _env_flag(name: str, default: bool) -> bool:
    """Parse a boolean flag from environment variables."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int_values(name: str, default: str) -> tuple[int, ...]:
    """Parse comma-separated integer values from environment."""
    raw = os.getenv(name, default)
    values: list[int] = []
    for item in raw.split(","):
        stripped = item.strip()
        if not stripped:
            continue
        try:
            values.append(int(stripped))
        except ValueError:
            return tuple()
    return tuple(dict.fromkeys(values))


ROOT_DIR: Final[Path] = Path(__file__).resolve().parents[1]
DATA_DIR: Final[Path] = Path(os.getenv("DATA_DIR", str(ROOT_DIR / "data")))

UPLOAD_DIR: Final[Path] = Path(
    os.getenv("UPLOAD_DIR", str(DATA_DIR / "uploads"))
)
UPLOAD_QUARANTINE_DIR: Final[Path] = Path(
    os.getenv("UPLOAD_QUARANTINE_DIR", str(UPLOAD_DIR / "quarantine"))
)
ENABLE_UPLOAD_QUARANTINE: Final[bool] = _env_flag(
    "ENABLE_UPLOAD_QUARANTINE",
    True,
)
ENABLE_MALWARE_SCAN: Final[bool] = _env_flag(
    "ENABLE_MALWARE_SCAN",
    False,
)
MALWARE_SCAN_COMMAND: Final[str] = os.getenv(
    "MALWARE_SCAN_COMMAND",
    "",
).strip()
MALWARE_SCAN_TIMEOUT_SECONDS: Final[int] = int(
    os.getenv("MALWARE_SCAN_TIMEOUT_SECONDS", "30")
)
MALWARE_SCAN_FAIL_CLOSED: Final[bool] = _env_flag(
    "MALWARE_SCAN_FAIL_CLOSED",
    False,
)
MALWARE_SCAN_INFECTED_EXIT_CODES: Final[tuple[int, ...]] = _env_int_values(
    "MALWARE_SCAN_INFECTED_EXIT_CODES",
    "1",
)
JOB_STORE_PATH: Final[Path] = Path(
    os.getenv("JOB_STORE_PATH", str(UPLOAD_DIR / "jobs.json"))
)
SEARCH_INDEX_JS_PATH: Final[Path] = Path(
    os.getenv(
        "SEARCH_INDEX_JS_PATH",
        str(ROOT_DIR / "web" / "js" / "search-index.js"),
    )
)
SEARCH_INDEX_JSON_PATH: Final[Path] = Path(
    os.getenv(
        "SEARCH_INDEX_JSON_PATH",
        str(ROOT_DIR / "web" / "data" / "search-index.json"),
    )
)

MAX_UPLOAD_MB: Final[int] = int(os.getenv("MAX_UPLOAD_MB", "100"))
ENVIRONMENT: Final[str] = (
    os.getenv("ENVIRONMENT", "development").strip().lower()
)
DEFAULT_DEV_ADMIN_TOKEN: Final[str] = "change-me-dev-token"
ADMIN_API_TOKEN: Final[str] = os.getenv(
    "ADMIN_API_TOKEN",
    DEFAULT_DEV_ADMIN_TOKEN,
)
DEFAULT_DEV_ADMIN_SESSION_SECRET: Final[str] = (
    "change-me-dev-session-secret"
)
ADMIN_SESSION_SECRET: Final[str] = os.getenv(
    "ADMIN_SESSION_SECRET",
    DEFAULT_DEV_ADMIN_SESSION_SECRET,
).strip()
ADMIN_SESSION_TTL_SECONDS: Final[int] = int(
    os.getenv("ADMIN_SESSION_TTL_SECONDS", "3600")
)
ADMIN_SESSION_COOKIE_NAME: Final[str] = (
    os.getenv("ADMIN_SESSION_COOKIE_NAME", "epstein_admin_session").strip()
    or "epstein_admin_session"
)
ADMIN_SESSION_COOKIE_SECURE: Final[bool] = _env_flag(
    "ADMIN_SESSION_COOKIE_SECURE",
    ENVIRONMENT in {"production", "staging"},
)

_admin_tokens_from_env = [
    token.strip()
    for token in os.getenv("ADMIN_API_TOKENS", "").split(",")
    if token.strip()
]
if ADMIN_API_TOKEN.strip():
    _admin_tokens_from_env.append(ADMIN_API_TOKEN.strip())

ADMIN_API_TOKENS: Final[tuple[str, ...]] = tuple(
    dict.fromkeys(_admin_tokens_from_env)
)

AUTH_RATE_LIMIT_MAX_ATTEMPTS: Final[int] = int(
    os.getenv("AUTH_RATE_LIMIT_MAX_ATTEMPTS", "10")
)
AUTH_RATE_LIMIT_WINDOW_SECONDS: Final[int] = int(
    os.getenv("AUTH_RATE_LIMIT_WINDOW_SECONDS", "60")
)
AUTH_RATE_LIMIT_BACKEND: Final[str] = (
    os.getenv("AUTH_RATE_LIMIT_BACKEND", "memory").strip().lower()
)
AUTH_RATE_LIMIT_REDIS_URL: Final[str] = os.getenv(
    "AUTH_RATE_LIMIT_REDIS_URL",
    "",
).strip()
AUTH_RATE_LIMIT_REDIS_PREFIX: Final[str] = (
    os.getenv("AUTH_RATE_LIMIT_REDIS_PREFIX", "epstein_auth_rl").strip()
    or "epstein_auth_rl"
)

ALLOWED_ORIGINS: Final[List[str]] = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
    if origin.strip()
]

API_NAME: Final[str] = "Epstein Files Hub API"
API_VERSION: Final[str] = "1.0.0"


def ensure_runtime_directories() -> None:
    """Ensure directories required by runtime services exist."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    if ENABLE_UPLOAD_QUARANTINE:
        UPLOAD_QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    JOB_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)


def validate_security_configuration() -> None:
    """Validate security-sensitive runtime settings."""
    if not ADMIN_API_TOKENS:
        raise RuntimeError("At least one ADMIN_API_TOKEN must be configured")

    if AUTH_RATE_LIMIT_MAX_ATTEMPTS < 1:
        raise RuntimeError("AUTH_RATE_LIMIT_MAX_ATTEMPTS must be >= 1")

    if AUTH_RATE_LIMIT_WINDOW_SECONDS < 1:
        raise RuntimeError("AUTH_RATE_LIMIT_WINDOW_SECONDS must be >= 1")

    if AUTH_RATE_LIMIT_BACKEND not in {"memory", "redis"}:
        raise RuntimeError(
            "AUTH_RATE_LIMIT_BACKEND must be 'memory' or 'redis'"
        )

    if AUTH_RATE_LIMIT_BACKEND == "redis" and not AUTH_RATE_LIMIT_REDIS_URL:
        raise RuntimeError(
            "AUTH_RATE_LIMIT_REDIS_URL must be configured when "
            "AUTH_RATE_LIMIT_BACKEND=redis"
        )

    if ADMIN_SESSION_TTL_SECONDS < 60:
        raise RuntimeError("ADMIN_SESSION_TTL_SECONDS must be >= 60")

    if not ADMIN_SESSION_COOKIE_NAME:
        raise RuntimeError("ADMIN_SESSION_COOKIE_NAME must not be empty")

    if ENABLE_UPLOAD_QUARANTINE and not str(UPLOAD_QUARANTINE_DIR).strip():
        raise RuntimeError("UPLOAD_QUARANTINE_DIR must not be empty")

    if MALWARE_SCAN_TIMEOUT_SECONDS < 1:
        raise RuntimeError("MALWARE_SCAN_TIMEOUT_SECONDS must be >= 1")

    if not MALWARE_SCAN_INFECTED_EXIT_CODES:
        raise RuntimeError(
            "MALWARE_SCAN_INFECTED_EXIT_CODES must include "
            "at least one integer"
        )

    if ENABLE_MALWARE_SCAN and not MALWARE_SCAN_COMMAND:
        raise RuntimeError(
            "MALWARE_SCAN_COMMAND must be configured when "
            "ENABLE_MALWARE_SCAN=true"
        )

    if ENVIRONMENT in {"production", "staging"}:
        if DEFAULT_DEV_ADMIN_TOKEN in ADMIN_API_TOKENS:
            raise RuntimeError(
                "Refusing to start with default admin token "
                "outside development"
            )

        if ADMIN_SESSION_SECRET == DEFAULT_DEV_ADMIN_SESSION_SECRET:
            raise RuntimeError(
                "Refusing default admin session secret "
                "outside development"
            )

        if len(ADMIN_SESSION_SECRET) < 32:
            raise RuntimeError(
                "ADMIN_SESSION_SECRET must be at least 32 characters "
                "outside development"
            )

        if "*" in ALLOWED_ORIGINS:
            raise RuntimeError(
                "Refusing wildcard CORS origins in production/staging"
            )
