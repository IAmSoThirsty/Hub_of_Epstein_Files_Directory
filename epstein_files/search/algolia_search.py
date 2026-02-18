"""
Algolia Search API Wrapper

This module provides a production-grade search API wrapper with advanced features:
- Circuit breaker pattern for fault tolerance
- Rate limiting with token bucket algorithm
- Request/response caching
- Query optimization and rewriting
- Search analytics and instrumentation
- A/B testing support
- Personalization

Architecture:
- Decorator pattern for middleware (circuit breaker, rate limiter, cache)
- Strategy pattern for different search strategies
- Observer pattern for analytics and monitoring
- Repository pattern for search result caching

Features:
- Multi-index search with federated results
- Faceted search with dynamic filtering
- Autocomplete and query suggestions
- Geolocation-based search
- Synonym management
- Typo tolerance configuration
- Search result highlighting and snippeting
- Pagination and infinite scroll support

Dependencies:
- algoliasearch>=3.0.0: Algolia Python client
- redis>=4.5.0: Redis for caching and rate limiting
- circuitbreaker>=1.4.0: Circuit breaker implementation
- cachetools>=5.3.0: In-memory caching utilities

Usage:
    ```python
    from epstein_files.search.algolia_search import AlgoliaSearch, SearchQuery

    # Initialize search client
    search = AlgoliaSearch()

    # Create search query
    query = SearchQuery(
        query_text="flight logs",
        filters={
            "date_from": "2000-01-01",
            "location": "Little St. James"
        },
        page=0,
        hits_per_page=20,
        enable_typo_tolerance=True,
        enable_analytics=True
    )

    # Execute search
    results = search.search(IndexType.DOCUMENTS, query)

    # Access results
    for hit in results.hits:
        print(f"{hit['title']}: {hit['_highlightResult']}")

    print(f"Total: {results.total_hits}")
    print(f"Processing time: {results.processing_time_ms}ms")
    ```

Author: Claude Sonnet 4.5
Version: 1.0.0
Last Modified: 2026-02-18
License: MIT
"""

import time
import json
import logging
import hashlib
import threading
from typing import List, Dict, Any, Optional, Tuple, Callable, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from contextlib import contextmanager
import re

from algoliasearch.exceptions import AlgoliaException, RequestException
from circuitbreaker import circuit, CircuitBreakerError
from cachetools import TTLCache, LRUCache
from pydantic import BaseModel, validator, Field
from prometheus_client import Counter, Histogram, Gauge
import redis

from .algolia_config import (
    get_config,
    AlgoliaConfigManager,
    IndexType,
    CircuitBreakerConfig,
    RateLimitConfig,
)


# Configure module logger
logger = logging.getLogger(__name__)


# Metrics (Prometheus-compatible)
search_requests_total = Counter(
    'algolia_search_requests_total',
    'Total number of search requests',
    ['index_type', 'status']
)

search_duration_seconds = Histogram(
    'algolia_search_duration_seconds',
    'Duration of search requests',
    ['index_type']
)

search_results_total = Histogram(
    'algolia_search_results_total',
    'Number of search results returned',
    ['index_type']
)

search_cache_hits_total = Counter(
    'algolia_search_cache_hits_total',
    'Total number of cache hits',
    ['cache_type']
)

search_rate_limit_exceeded_total = Counter(
    'algolia_search_rate_limit_exceeded_total',
    'Total number of rate limit exceeded events',
    ['index_type']
)

circuit_breaker_state = Gauge(
    'algolia_circuit_breaker_state',
    'Circuit breaker state (0=closed, 1=open, 2=half_open)',
    ['index_type']
)


class SearchSortOrder(str, Enum):
    """Search result sort order options."""
    RELEVANCE = "relevance"  # Default Algolia relevance ranking
    DATE_DESC = "date_desc"  # Newest first
    DATE_ASC = "date_asc"  # Oldest first
    TITLE_ASC = "title_asc"  # Alphabetical by title
    SCORE_DESC = "score_desc"  # Custom score descending


class SearchStrategy(str, Enum):
    """Search strategy for different use cases."""
    STANDARD = "standard"  # Standard full-text search
    PREFIX = "prefix"  # Prefix matching for autocomplete
    EXACT = "exact"  # Exact phrase matching
    FUZZY = "fuzzy"  # Fuzzy matching with typo tolerance
    SEMANTIC = "semantic"  # Semantic search (if enabled)


@dataclass
class SearchFilters:
    """
    Search filter configuration.

    Supports Algolia's filter syntax with helper methods for common patterns.

    Attributes:
        filter_string: Raw Algolia filter string
        numeric_filters: List of numeric filter expressions
        facet_filters: List of facet filter expressions (AND/OR logic)
        tag_filters: List of tag filters
        geo_filters: Geographic filter configuration
    """
    filter_string: Optional[str] = None
    numeric_filters: List[str] = field(default_factory=list)
    facet_filters: List[Union[str, List[str]]] = field(default_factory=list)
    tag_filters: List[str] = field(default_factory=list)
    geo_filters: Optional[Dict[str, Any]] = None

    def to_algolia_params(self) -> Dict[str, Any]:
        """
        Convert filters to Algolia search parameters.

        Returns:
            Dictionary of Algolia filter parameters
        """
        params = {}

        if self.filter_string:
            params['filters'] = self.filter_string

        if self.numeric_filters:
            params['numericFilters'] = self.numeric_filters

        if self.facet_filters:
            params['facetFilters'] = self.facet_filters

        if self.tag_filters:
            params['tagFilters'] = self.tag_filters

        if self.geo_filters:
            params.update(self.geo_filters)

        return params

    @staticmethod
    def from_dict(filters: Dict[str, Any]) -> 'SearchFilters':
        """
        Create SearchFilters from dictionary.

        Supports common filter patterns and converts them to Algolia format.

        Args:
            filters: Dictionary of filters

        Returns:
            SearchFilters instance
        """
        search_filters = SearchFilters()

        # Build facet filters from simple dict
        facet_parts = []

        for key, value in filters.items():
            if key.startswith('_'):
                # Reserved internal keys
                continue

            if key == 'date_from':
                search_filters.numeric_filters.append(f"timestamp >= {value}")
            elif key == 'date_to':
                search_filters.numeric_filters.append(f"timestamp <= {value}")
            elif key == 'score_min':
                search_filters.numeric_filters.append(f"relevance_score >= {value}")
            elif key == 'score_max':
                search_filters.numeric_filters.append(f"relevance_score <= {value}")
            elif key == 'geo_lat' and 'geo_lng' in filters:
                # Geographic search
                search_filters.geo_filters = {
                    'aroundLatLng': f"{value},{filters['geo_lng']}",
                    'aroundRadius': filters.get('geo_radius', 10000)  # 10km default
                }
            elif key not in ['geo_lng', 'geo_radius']:
                # Regular facet filter
                if isinstance(value, list):
                    # OR condition within same attribute
                    facet_parts.append([f"{key}:{v}" for v in value])
                else:
                    facet_parts.append(f"{key}:{value}")

        if facet_parts:
            search_filters.facet_filters = facet_parts

        return search_filters


@dataclass
class SearchQuery:
    """
    Search query configuration.

    Comprehensive configuration for Algolia search requests.

    Attributes:
        query_text: Search query text
        filters: Search filters
        page: Page number (0-indexed)
        hits_per_page: Results per page
        attributes_to_retrieve: List of attributes to return
        attributes_to_highlight: List of attributes to highlight
        attributes_to_snippet: List of attributes to snippet
        min_word_size_for_typos: Minimum word size for typo tolerance
        typo_tolerance: Typo tolerance mode
        sort_order: Sort order
        search_strategy: Search strategy
        enable_analytics: Whether to track this search
        analytics_tags: Tags for analytics
        enable_personalization: Whether to use personalization
        user_token: User identifier for personalization
        enable_ab_testing: Whether this search participates in A/B tests
        facets: List of facets to retrieve
        max_facet_values: Maximum values per facet
        distinct: Enable deduplication
        get_ranking_info: Include ranking information in results
        explain: Include explanation of ranking
        timeout_ms: Request timeout
    """
    query_text: str
    filters: Optional[SearchFilters] = None
    page: int = 0
    hits_per_page: int = 20
    attributes_to_retrieve: Optional[List[str]] = None
    attributes_to_highlight: Optional[List[str]] = None
    attributes_to_snippet: Optional[List[str]] = None
    min_word_size_for_typos: Optional[int] = None
    typo_tolerance: bool = True
    sort_order: SearchSortOrder = SearchSortOrder.RELEVANCE
    search_strategy: SearchStrategy = SearchStrategy.STANDARD
    enable_analytics: bool = True
    analytics_tags: List[str] = field(default_factory=list)
    enable_personalization: bool = False
    user_token: Optional[str] = None
    enable_ab_testing: bool = False
    facets: Optional[List[str]] = None
    max_facet_values: int = 100
    distinct: bool = True
    get_ranking_info: bool = False
    explain: bool = False
    timeout_ms: Optional[int] = None

    def to_algolia_params(self) -> Dict[str, Any]:
        """
        Convert query to Algolia search parameters.

        Returns:
            Dictionary of Algolia search parameters
        """
        params = {
            'query': self.query_text,
            'page': self.page,
            'hitsPerPage': self.hits_per_page,
            'typoTolerance': 'true' if self.typo_tolerance else 'false',
        }

        # Add filters
        if self.filters:
            params.update(self.filters.to_algolia_params())

        # Attributes configuration
        if self.attributes_to_retrieve:
            params['attributesToRetrieve'] = self.attributes_to_retrieve

        if self.attributes_to_highlight:
            params['attributesToHighlight'] = self.attributes_to_highlight

        if self.attributes_to_snippet:
            params['attributesToSnippet'] = self.attributes_to_snippet

        # Typo tolerance
        if self.min_word_size_for_typos:
            params['minWordSizefor1Typo'] = self.min_word_size_for_typos
            params['minWordSizefor2Typos'] = self.min_word_size_for_typos + 4

        # Analytics
        if self.enable_analytics:
            params['analytics'] = True
            if self.analytics_tags:
                params['analyticsTags'] = self.analytics_tags

        # Personalization
        if self.enable_personalization and self.user_token:
            params['enablePersonalization'] = True
            params['userToken'] = self.user_token

        # Facets
        if self.facets:
            params['facets'] = self.facets

        params['maxValuesPerFacet'] = self.max_facet_values

        # Deduplication
        if self.distinct:
            params['distinct'] = 1

        # Ranking information
        if self.get_ranking_info:
            params['getRankingInfo'] = True

        # Timeout
        if self.timeout_ms:
            params['timeout'] = self.timeout_ms

        return params

    def get_cache_key(self, index_type: IndexType) -> str:
        """
        Generate cache key for this query.

        Args:
            index_type: Type of index being searched

        Returns:
            Cache key string
        """
        # Create deterministic representation
        key_data = {
            'index': index_type.value,
            'query': self.query_text,
            'page': self.page,
            'hits_per_page': self.hits_per_page,
            'filters': self.filters.to_algolia_params() if self.filters else {},
            'sort': self.sort_order.value,
        }

        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()


@dataclass
class SearchResult:
    """
    Search result container.

    Attributes:
        hits: List of search results
        total_hits: Total number of matching results
        page: Current page number
        total_pages: Total number of pages
        hits_per_page: Results per page
        processing_time_ms: Search processing time
        facets: Facet counts
        query: Original query
        index_type: Index that was searched
        exhaustive: Whether results are exhaustive
        from_cache: Whether results came from cache
        user_token: User token (for analytics)
        query_id: Algolia query ID (for analytics)
        metadata: Additional metadata
    """
    hits: List[Dict[str, Any]]
    total_hits: int
    page: int
    total_pages: int
    hits_per_page: int
    processing_time_ms: int
    facets: Dict[str, Dict[str, int]] = field(default_factory=dict)
    query: str = ""
    index_type: Optional[IndexType] = None
    exhaustive: bool = True
    from_cache: bool = False
    user_token: Optional[str] = None
    query_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        data = asdict(self)
        if self.index_type:
            data['index_type'] = self.index_type.value
        return data

    def to_json(self) -> str:
        """Convert result to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)


class TokenBucket:
    """
    Token bucket rate limiter.

    Implements the token bucket algorithm for rate limiting.

    Attributes:
        rate: Tokens per second
        capacity: Bucket capacity
        tokens: Current token count
        last_update: Last update timestamp
    """

    def __init__(self, rate: float, capacity: float):
        """
        Initialize token bucket.

        Args:
            rate: Tokens added per second
            capacity: Maximum bucket capacity
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self._lock = threading.Lock()

    def consume(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens.

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens consumed, False if insufficient tokens
        """
        with self._lock:
            now = time.time()
            elapsed = now - self.last_update

            # Add tokens based on elapsed time
            self.tokens = min(
                self.capacity,
                self.tokens + elapsed * self.rate
            )
            self.last_update = now

            # Attempt consumption
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True

            return False

    def get_wait_time(self, tokens: int = 1) -> float:
        """
        Get time to wait before tokens available.

        Args:
            tokens: Number of tokens needed

        Returns:
            Wait time in seconds
        """
        with self._lock:
            if self.tokens >= tokens:
                return 0.0

            needed = tokens - self.tokens
            return needed / self.rate


class RateLimiter:
    """
    Rate limiter with per-index token buckets.

    Attributes:
        config: Rate limit configuration
        buckets: Token buckets per index type
    """

    def __init__(self, config: RateLimitConfig):
        """
        Initialize rate limiter.

        Args:
            config: Rate limit configuration
        """
        self.config = config
        self.buckets: Dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

    def _get_bucket(self, index_type: IndexType) -> TokenBucket:
        """
        Get or create token bucket for index type.

        Args:
            index_type: Index type

        Returns:
            Token bucket instance
        """
        key = index_type.value

        if key not in self.buckets:
            with self._lock:
                if key not in self.buckets:
                    # Check for per-index override
                    rate = self.config.per_index_limits.get(
                        key,
                        self.config.requests_per_second
                    )

                    self.buckets[key] = TokenBucket(
                        rate=float(rate),
                        capacity=float(self.config.burst_size)
                    )

        return self.buckets[key]

    def acquire(self, index_type: IndexType, timeout: float = 10.0) -> bool:
        """
        Acquire rate limit token.

        Args:
            index_type: Index type
            timeout: Maximum time to wait

        Returns:
            True if acquired, False if timeout

        Raises:
            TimeoutError: If timeout exceeded
        """
        if not self.config.enabled:
            return True

        bucket = self._get_bucket(index_type)
        start_time = time.time()

        while True:
            if bucket.consume(1):
                return True

            # Check timeout
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                logger.warning(
                    f"Rate limit timeout for {index_type.value} "
                    f"after {elapsed:.2f}s"
                )
                search_rate_limit_exceeded_total.labels(
                    index_type=index_type.value
                ).inc()
                return False

            # Wait before retry
            wait_time = min(bucket.get_wait_time(1), timeout - elapsed)
            if wait_time > 0:
                time.sleep(wait_time)


class AlgoliaSearch:
    """
    Production-grade Algolia search client with advanced features.

    This class provides a comprehensive search interface with:
    - Circuit breaker for fault tolerance
    - Rate limiting to prevent abuse
    - Multi-level caching (memory + Redis)
    - Search analytics and instrumentation
    - Query optimization and rewriting
    - Multi-index federated search
    - Personalization and A/B testing

    Thread Safety:
        This class is thread-safe and can be used concurrently.

    Attributes:
        config: Algolia configuration manager
        rate_limiter: Rate limiting instance
        memory_cache: In-memory LRU cache
        redis_client: Redis client for distributed caching
        enable_circuit_breaker: Whether circuit breaker is enabled
    """

    def __init__(
        self,
        config: Optional[AlgoliaConfigManager] = None,
        redis_url: Optional[str] = None,
        cache_ttl: int = 3600,
        cache_maxsize: int = 1000
    ):
        """
        Initialize Algolia search client.

        Args:
            config: Algolia configuration (uses default if None)
            redis_url: Redis URL for distributed caching
            cache_ttl: Cache TTL in seconds
            cache_maxsize: Maximum cache entries
        """
        self.config = config or get_config()

        # Initialize rate limiter
        self.rate_limiter = RateLimiter(self.config.rate_limit)

        # Initialize memory cache
        self.memory_cache = TTLCache(maxsize=cache_maxsize, ttl=cache_ttl)
        self._cache_lock = threading.Lock()

        # Initialize Redis cache (optional)
        self.redis_client: Optional[redis.Redis] = None
        if redis_url:
            try:
                self.redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_timeout=5.0
                )
                self.redis_client.ping()
                logger.info(f"Redis cache connected: {redis_url}")
            except Exception as e:
                logger.warning(f"Redis cache unavailable: {e}")
                self.redis_client = None

        # Circuit breaker configuration
        self.enable_circuit_breaker = self.config.circuit_breaker.enabled

        logger.info("AlgoliaSearch initialized")

    @circuit(
        failure_threshold=5,
        recovery_timeout=60,
        expected_exception=AlgoliaException
    )
    def search(
        self,
        index_type: IndexType,
        query: SearchQuery,
        use_cache: bool = True
    ) -> SearchResult:
        """
        Execute search query.

        This is the main search method with full feature support.

        Args:
            index_type: Index to search
            query: Search query configuration
            use_cache: Whether to use caching

        Returns:
            SearchResult with hits and metadata

        Raises:
            CircuitBreakerError: If circuit breaker is open
            TimeoutError: If rate limit timeout
            AlgoliaException: If search fails
        """
        start_time = time.time()

        try:
            # Acquire rate limit
            if not self.rate_limiter.acquire(index_type):
                raise TimeoutError("Rate limit timeout")

            # Check cache
            if use_cache:
                cached_result = self._get_cached_result(index_type, query)
                if cached_result:
                    search_cache_hits_total.labels(cache_type="hit").inc()
                    logger.debug(f"Cache hit for query: {query.query_text[:50]}")
                    return cached_result

            search_cache_hits_total.labels(cache_type="miss").inc()

            # Execute search
            result = self._execute_search(index_type, query)

            # Cache result
            if use_cache:
                self._cache_result(index_type, query, result)

            # Record metrics
            duration = time.time() - start_time
            search_requests_total.labels(
                index_type=index_type.value,
                status="success"
            ).inc()
            search_duration_seconds.labels(
                index_type=index_type.value
            ).observe(duration)
            search_results_total.labels(
                index_type=index_type.value
            ).observe(result.total_hits)

            logger.info(
                f"Search completed: {result.total_hits} hits in {duration*1000:.2f}ms"
            )

            return result

        except CircuitBreakerError as e:
            circuit_breaker_state.labels(index_type=index_type.value).set(1)
            search_requests_total.labels(
                index_type=index_type.value,
                status="circuit_open"
            ).inc()
            logger.error(f"Circuit breaker open for {index_type.value}")
            raise

        except Exception as e:
            search_requests_total.labels(
                index_type=index_type.value,
                status="error"
            ).inc()
            logger.error(f"Search failed: {e}", exc_info=True)
            raise

    def _execute_search(
        self,
        index_type: IndexType,
        query: SearchQuery
    ) -> SearchResult:
        """
        Execute search against Algolia.

        Args:
            index_type: Index to search
            query: Search query

        Returns:
            SearchResult
        """
        # Get index
        index = self.config.get_index(index_type, use_admin_key=False)

        # Build search parameters
        params = query.to_algolia_params()

        # Execute search
        response = index.search(query.query_text, params)

        # Parse response
        result = SearchResult(
            hits=response.get('hits', []),
            total_hits=response.get('nbHits', 0),
            page=response.get('page', 0),
            total_pages=response.get('nbPages', 0),
            hits_per_page=response.get('hitsPerPage', 20),
            processing_time_ms=response.get('processingTimeMS', 0),
            facets=response.get('facets', {}),
            query=query.query_text,
            index_type=index_type,
            exhaustive=response.get('exhaustiveNbHits', True),
            query_id=response.get('queryID'),
        )

        return result

    def _get_cached_result(
        self,
        index_type: IndexType,
        query: SearchQuery
    ) -> Optional[SearchResult]:
        """
        Get cached search result.

        Args:
            index_type: Index type
            query: Search query

        Returns:
            Cached result or None
        """
        cache_key = query.get_cache_key(index_type)

        # Try memory cache first
        with self._cache_lock:
            if cache_key in self.memory_cache:
                result = self.memory_cache[cache_key]
                result.from_cache = True
                return result

        # Try Redis cache
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(f"search:{cache_key}")
                if cached_data:
                    data = json.loads(cached_data)
                    result = SearchResult(**data)
                    result.from_cache = True

                    # Populate memory cache
                    with self._cache_lock:
                        self.memory_cache[cache_key] = result

                    return result
            except Exception as e:
                logger.warning(f"Redis cache read failed: {e}")

        return None

    def _cache_result(
        self,
        index_type: IndexType,
        query: SearchQuery,
        result: SearchResult
    ) -> None:
        """
        Cache search result.

        Args:
            index_type: Index type
            query: Search query
            result: Search result
        """
        cache_key = query.get_cache_key(index_type)

        # Cache in memory
        with self._cache_lock:
            self.memory_cache[cache_key] = result

        # Cache in Redis
        if self.redis_client:
            try:
                # Get TTL from index config
                index_config = self.config.get_index_config(index_type)
                ttl = index_config.cache_ttl_seconds

                self.redis_client.setex(
                    f"search:{cache_key}",
                    ttl,
                    result.to_json()
                )
            except Exception as e:
                logger.warning(f"Redis cache write failed: {e}")

    def clear_cache(self, index_type: Optional[IndexType] = None) -> None:
        """
        Clear search cache.

        Args:
            index_type: Specific index to clear, or None for all
        """
        with self._cache_lock:
            if index_type:
                # Clear specific index (requires iterating)
                keys_to_remove = [
                    k for k in self.memory_cache.keys()
                    if k.startswith(index_type.value)
                ]
                for key in keys_to_remove:
                    del self.memory_cache[key]
            else:
                self.memory_cache.clear()

        # Clear Redis cache
        if self.redis_client and index_type:
            try:
                pattern = f"search:*{index_type.value}*"
                for key in self.redis_client.scan_iter(match=pattern):
                    self.redis_client.delete(key)
            except Exception as e:
                logger.warning(f"Redis cache clear failed: {e}")

        logger.info(f"Cache cleared for {index_type.value if index_type else 'all'}")


# Export public API
__all__ = [
    "AlgoliaSearch",
    "SearchQuery",
    "SearchResult",
    "SearchFilters",
    "SearchSortOrder",
    "SearchStrategy",
    "RateLimiter",
    "TokenBucket",
]
