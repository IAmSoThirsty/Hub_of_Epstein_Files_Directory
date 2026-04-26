"""Unit tests for auth rate-limit store backends."""

from __future__ import annotations

from api import rate_limit_store


def test_in_memory_store_enforces_threshold() -> None:
    store = rate_limit_store.InMemoryRateLimitStore(
        max_attempts=3,
        window_seconds=60,
    )

    assert not store.is_rate_limited("client-a")

    store.record_failed_attempt("client-a")
    store.record_failed_attempt("client-a")
    assert not store.is_rate_limited("client-a")

    store.record_failed_attempt("client-a")
    assert store.is_rate_limited("client-a")


def test_in_memory_store_clear_resets_client() -> None:
    store = rate_limit_store.InMemoryRateLimitStore(
        max_attempts=2,
        window_seconds=60,
    )

    store.record_failed_attempt("client-b")
    store.record_failed_attempt("client-b")
    assert store.is_rate_limited("client-b")

    store.clear_failed_attempts("client-b")
    assert not store.is_rate_limited("client-b")


def test_create_rate_limit_store_falls_back_when_redis_init_fails(
    monkeypatch,
) -> None:
    class BrokenRedisStore:
        def __init__(self, *args, **kwargs) -> None:
            raise RuntimeError("redis unavailable")

    monkeypatch.setattr(rate_limit_store, "AUTH_RATE_LIMIT_BACKEND", "redis")
    monkeypatch.setattr(
        rate_limit_store,
        "AUTH_RATE_LIMIT_REDIS_URL",
        "redis://localhost:6379/0",
    )
    monkeypatch.setattr(
        rate_limit_store,
        "RedisRateLimitStore",
        BrokenRedisStore,
    )

    store = rate_limit_store.create_rate_limit_store()

    assert isinstance(store, rate_limit_store.InMemoryRateLimitStore)
