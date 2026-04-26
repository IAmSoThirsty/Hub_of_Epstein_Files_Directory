"""Rate-limit stores for authentication throttling."""

from __future__ import annotations

import hashlib
import threading
import time
from collections import defaultdict
from collections import deque
from typing import Deque, Dict, Protocol
from uuid import uuid4

from .config import AUTH_RATE_LIMIT_BACKEND
from .config import AUTH_RATE_LIMIT_MAX_ATTEMPTS
from .config import AUTH_RATE_LIMIT_REDIS_PREFIX
from .config import AUTH_RATE_LIMIT_REDIS_URL
from .config import AUTH_RATE_LIMIT_WINDOW_SECONDS


class RateLimitStore(Protocol):
    """Interface for storing and evaluating auth attempt counts."""

    def is_rate_limited(self, client_id: str) -> bool:
        """Return True when client has exceeded threshold."""

    def record_failed_attempt(self, client_id: str) -> None:
        """Record one failed authentication attempt for a client."""

    def clear_failed_attempts(self, client_id: str) -> None:
        """Clear all tracked failed attempts for a client."""


class InMemoryRateLimitStore:
    """Process-local auth rate-limit store using deques."""

    def __init__(self, max_attempts: int, window_seconds: int) -> None:
        self._max_attempts = max_attempts
        self._window_seconds = window_seconds
        self._attempts: Dict[str, Deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def _cleanup_attempts(self, client_id: str, now: float) -> Deque[float]:
        attempts = self._attempts[client_id]
        cutoff = now - self._window_seconds
        while attempts and attempts[0] < cutoff:
            attempts.popleft()
        return attempts

    def is_rate_limited(self, client_id: str) -> bool:
        now = time.monotonic()
        with self._lock:
            attempts = self._cleanup_attempts(client_id, now)
            if not attempts:
                self._attempts.pop(client_id, None)
                return False
            return len(attempts) >= self._max_attempts

    def record_failed_attempt(self, client_id: str) -> None:
        now = time.monotonic()
        with self._lock:
            attempts = self._cleanup_attempts(client_id, now)
            attempts.append(now)

    def clear_failed_attempts(self, client_id: str) -> None:
        with self._lock:
            self._attempts.pop(client_id, None)


class RedisRateLimitStore:
    """Redis-backed auth rate-limit store for multi-worker consistency."""

    def __init__(
        self,
        redis_url: str,
        redis_prefix: str,
        max_attempts: int,
        window_seconds: int,
    ) -> None:
        try:
            import redis
        except ImportError as exc:
            raise RuntimeError(
                "redis package is required for redis backend"
            ) from exc

        self._client = redis.Redis.from_url(redis_url)
        self._prefix = redis_prefix
        self._max_attempts = max_attempts
        self._window_seconds = window_seconds
        self._window_ms = window_seconds * 1000

        # Validate connectivity eagerly to avoid silent broken config.
        self._client.ping()

    def _key(self, client_id: str) -> str:
        digest = hashlib.sha256(client_id.encode("utf-8")).hexdigest()
        return f"{self._prefix}:{digest}"

    def _now_ms(self) -> int:
        return int(time.time() * 1000)

    def _trim_and_count(self, key: str) -> int:
        now_ms = self._now_ms()
        oldest_allowed = now_ms - self._window_ms

        with self._client.pipeline() as pipe:
            pipe.zremrangebyscore(key, "-inf", oldest_allowed)
            pipe.zcard(key)
            pipe.expire(key, self._window_seconds + 5)
            _, count, _ = pipe.execute()

        return int(count)

    def is_rate_limited(self, client_id: str) -> bool:
        count = self._trim_and_count(self._key(client_id))
        return count >= self._max_attempts

    def record_failed_attempt(self, client_id: str) -> None:
        key = self._key(client_id)
        now_ms = self._now_ms()
        oldest_allowed = now_ms - self._window_ms
        member = f"{now_ms}-{uuid4().hex}"

        with self._client.pipeline() as pipe:
            pipe.zadd(key, {member: now_ms})
            pipe.zremrangebyscore(key, "-inf", oldest_allowed)
            pipe.expire(key, self._window_seconds + 5)
            pipe.execute()

    def clear_failed_attempts(self, client_id: str) -> None:
        self._client.delete(self._key(client_id))


class ResilientRateLimitStore:
    """Primary/fallback store wrapper for robust runtime behavior."""

    def __init__(
        self,
        primary: RateLimitStore,
        fallback: RateLimitStore,
    ) -> None:
        self._primary = primary
        self._fallback = fallback

    def is_rate_limited(self, client_id: str) -> bool:
        try:
            return self._primary.is_rate_limited(client_id)
        except Exception:  # pylint: disable=broad-except
            return self._fallback.is_rate_limited(client_id)

    def record_failed_attempt(self, client_id: str) -> None:
        try:
            self._primary.record_failed_attempt(client_id)
        except Exception:  # pylint: disable=broad-except
            self._fallback.record_failed_attempt(client_id)

    def clear_failed_attempts(self, client_id: str) -> None:
        try:
            self._primary.clear_failed_attempts(client_id)
        except Exception:  # pylint: disable=broad-except
            self._fallback.clear_failed_attempts(client_id)


def create_rate_limit_store() -> RateLimitStore:
    """Build the configured auth rate-limit store backend."""
    memory_store: RateLimitStore = InMemoryRateLimitStore(
        max_attempts=AUTH_RATE_LIMIT_MAX_ATTEMPTS,
        window_seconds=AUTH_RATE_LIMIT_WINDOW_SECONDS,
    )

    if AUTH_RATE_LIMIT_BACKEND != "redis":
        return memory_store

    try:
        redis_store = RedisRateLimitStore(
            redis_url=AUTH_RATE_LIMIT_REDIS_URL,
            redis_prefix=AUTH_RATE_LIMIT_REDIS_PREFIX,
            max_attempts=AUTH_RATE_LIMIT_MAX_ATTEMPTS,
            window_seconds=AUTH_RATE_LIMIT_WINDOW_SECONDS,
        )
    except Exception:  # pylint: disable=broad-except
        return memory_store

    return ResilientRateLimitStore(redis_store, memory_store)
