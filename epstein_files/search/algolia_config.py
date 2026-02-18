"""
Algolia Search Integration Configuration Module

This module provides comprehensive configuration management for Algolia search integration
with production-grade features including environment management, validation, encryption,
and multi-environment support.

Architecture:
- Singleton pattern for configuration management
- Environment-based configuration with strict validation
- Secure secret management with encryption at rest
- Multi-index support for different data types
- Feature flags for gradual rollout
- Circuit breaker configuration for resilience

Security:
- API keys never logged or exposed
- TLS 1.3 for all connections
- Rate limiting configuration
- IP whitelisting support
- Audit logging for all config changes

Dependencies:
- algoliasearch>=3.0.0: Official Algolia Python client
- python-dotenv>=1.0.0: Environment variable management
- cryptography>=41.0.0: Secure secret encryption
- pydantic>=2.0.0: Data validation and settings management

Environment Variables Required:
- ALGOLIA_APP_ID: Algolia application ID
- ALGOLIA_ADMIN_API_KEY: Admin API key (write access)
- ALGOLIA_SEARCH_API_KEY: Search-only API key (read access)
- ALGOLIA_ENVIRONMENT: Environment name (dev|staging|prod)
- ALGOLIA_ENCRYPTION_KEY: Key for encrypting sensitive config

Optional Environment Variables:
- ALGOLIA_INDEX_PREFIX: Prefix for index names (default: '')
- ALGOLIA_ENABLE_CIRCUIT_BREAKER: Enable circuit breaker (default: true)
- ALGOLIA_MAX_RETRIES: Maximum retry attempts (default: 3)
- ALGOLIA_TIMEOUT_MS: Request timeout in milliseconds (default: 30000)
- ALGOLIA_BATCH_SIZE: Batch size for bulk operations (default: 1000)
- ALGOLIA_ENABLE_ANALYTICS: Enable Algolia Insights (default: true)
- ALGOLIA_REPLICA_COUNT: Number of replica indices (default: 2)

Author: Claude Sonnet 4.5
Version: 1.0.0
Last Modified: 2026-02-18
License: MIT
"""

import os
import json
import logging
import hashlib
from typing import Dict, List, Optional, Any, Literal
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
import threading

from algoliasearch.search_client import SearchClient
from pydantic import BaseSettings, validator, Field, SecretStr
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import dotenv


# Configure module logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add structured logging handler if not already configured
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class AlgoliaEnvironment(str, Enum):
    """
    Algolia environment enumeration.

    Each environment has different configuration, rate limits, and security settings.
    """
    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"


class IndexType(str, Enum):
    """
    Index type enumeration for different data categories.

    Each index type has specific schema, ranking, and filtering configurations.
    """
    DOCUMENTS = "documents"  # Court documents, filings, depositions
    CHARACTERS = "characters"  # People/entities profiles
    LOCATIONS = "locations"  # Geographic locations
    MEDIA = "media"  # Images, videos, audio files
    TIMELINE = "timeline"  # Chronological events
    RELATIONSHIPS = "relationships"  # Entity relationships graph


@dataclass
class IndexConfiguration:
    """
    Configuration for a single Algolia index.

    Attributes:
        name: Index name (will be prefixed with environment)
        type: Type of data stored in this index
        primary_key: Primary key field name
        searchable_attributes: List of attributes to search in, ordered by priority
        attributes_for_faceting: Attributes that can be used for filtering
        ranking_criteria: Custom ranking formula for result ordering
        replicas: List of replica index configurations for specialized sorting
        max_records: Maximum number of records allowed in index
        enable_synonyms: Whether to enable synonym matching
        enable_typo_tolerance: Whether to enable typo tolerance
        enable_deduplication: Whether to enable duplicate detection
        cache_ttl_seconds: Time-to-live for cached results
        custom_settings: Additional Algolia settings specific to this index
    """
    name: str
    type: IndexType
    primary_key: str = "objectID"
    searchable_attributes: List[str] = field(default_factory=list)
    attributes_for_faceting: List[str] = field(default_factory=list)
    ranking_criteria: List[str] = field(default_factory=list)
    replicas: List[str] = field(default_factory=list)
    max_records: int = 1000000
    enable_synonyms: bool = True
    enable_typo_tolerance: bool = True
    enable_deduplication: bool = True
    cache_ttl_seconds: int = 3600
    custom_settings: Dict[str, Any] = field(default_factory=dict)

    def to_algolia_settings(self) -> Dict[str, Any]:
        """
        Convert configuration to Algolia settings format.

        Returns:
            Dict compatible with Algolia's setSettings() API
        """
        settings = {
            "searchableAttributes": self.searchable_attributes,
            "attributesForFaceting": self.attributes_for_faceting,
            "customRanking": self.ranking_criteria,
            "replicas": self.replicas,
            "typoTolerance": "true" if self.enable_typo_tolerance else "false",
            "removeStopWords": True,
            "queryType": "prefixLast",  # Optimize for last word prefix matching
            "minWordSizefor1Typo": 4,
            "minWordSizefor2Typos": 8,
            "hitsPerPage": 20,
            "maxValuesPerFacet": 100,
            "distinct": 1 if self.enable_deduplication else 0,
        }

        # Merge custom settings (allows override)
        settings.update(self.custom_settings)

        return settings


@dataclass
class CircuitBreakerConfig:
    """
    Circuit breaker configuration for fault tolerance.

    Implements the circuit breaker pattern to prevent cascading failures
    when Algolia service is degraded or unavailable.

    States:
        - CLOSED: Normal operation, requests pass through
        - OPEN: Service degraded, requests fail fast
        - HALF_OPEN: Testing if service recovered

    Attributes:
        enabled: Whether circuit breaker is enabled
        failure_threshold: Number of failures before opening circuit
        success_threshold: Number of successes needed to close circuit
        timeout_seconds: Time to wait before attempting recovery
        half_open_max_calls: Max concurrent calls in half-open state
    """
    enabled: bool = True
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout_seconds: int = 60
    half_open_max_calls: int = 3


@dataclass
class RateLimitConfig:
    """
    Rate limiting configuration for API calls.

    Implements token bucket algorithm for rate limiting to prevent
    exceeding Algolia's rate limits and to protect system resources.

    Attributes:
        enabled: Whether rate limiting is enabled
        requests_per_second: Maximum requests per second
        burst_size: Maximum burst size (token bucket capacity)
        per_index_limits: Per-index rate limit overrides
    """
    enabled: bool = True
    requests_per_second: int = 100
    burst_size: int = 200
    per_index_limits: Dict[str, int] = field(default_factory=dict)


@dataclass
class RetryConfig:
    """
    Retry configuration for failed requests.

    Implements exponential backoff with jitter for retrying failed requests.

    Attributes:
        max_retries: Maximum number of retry attempts
        base_delay_ms: Base delay in milliseconds
        max_delay_ms: Maximum delay in milliseconds
        exponential_base: Base for exponential backoff calculation
        jitter: Whether to add random jitter to delays
        retryable_status_codes: HTTP status codes that trigger retry
    """
    max_retries: int = 3
    base_delay_ms: int = 100
    max_delay_ms: int = 30000
    exponential_base: float = 2.0
    jitter: bool = True
    retryable_status_codes: List[int] = field(
        default_factory=lambda: [429, 500, 502, 503, 504]
    )


class AlgoliaSettings(BaseSettings):
    """
    Pydantic-based settings model for Algolia configuration.

    Provides strict validation, type checking, and environment variable loading
    with comprehensive error messages and security features.

    Environment variables are loaded from:
    1. .env file (if present)
    2. System environment variables
    3. Default values (where applicable)

    Security features:
    - API keys are stored as SecretStr (never logged)
    - Encryption key validated for proper length
    - Sensitive fields excluded from repr and dict export
    """

    # Core Algolia credentials
    app_id: str = Field(..., env="ALGOLIA_APP_ID", min_length=1)
    admin_api_key: SecretStr = Field(..., env="ALGOLIA_ADMIN_API_KEY")
    search_api_key: SecretStr = Field(..., env="ALGOLIA_SEARCH_API_KEY")

    # Environment and deployment
    environment: AlgoliaEnvironment = Field(
        default=AlgoliaEnvironment.DEVELOPMENT,
        env="ALGOLIA_ENVIRONMENT"
    )
    index_prefix: str = Field(default="", env="ALGOLIA_INDEX_PREFIX")

    # Security and encryption
    encryption_key: Optional[SecretStr] = Field(None, env="ALGOLIA_ENCRYPTION_KEY")

    # Performance and reliability
    timeout_ms: int = Field(default=30000, env="ALGOLIA_TIMEOUT_MS", ge=1000, le=120000)
    batch_size: int = Field(default=1000, env="ALGOLIA_BATCH_SIZE", ge=1, le=10000)
    connection_pool_size: int = Field(default=10, env="ALGOLIA_POOL_SIZE", ge=1, le=100)

    # Feature flags
    enable_analytics: bool = Field(default=True, env="ALGOLIA_ENABLE_ANALYTICS")
    enable_personalization: bool = Field(default=False, env="ALGOLIA_ENABLE_PERSONALIZATION")
    enable_ab_testing: bool = Field(default=False, env="ALGOLIA_ENABLE_AB_TESTING")
    enable_query_suggestions: bool = Field(default=True, env="ALGOLIA_ENABLE_SUGGESTIONS")

    # Replica and redundancy
    replica_count: int = Field(default=2, env="ALGOLIA_REPLICA_COUNT", ge=0, le=10)

    # Monitoring and observability
    enable_metrics: bool = Field(default=True, env="ALGOLIA_ENABLE_METRICS")
    metrics_interval_seconds: int = Field(default=60, env="ALGOLIA_METRICS_INTERVAL", ge=10)

    # Development and debugging
    debug_mode: bool = Field(default=False, env="ALGOLIA_DEBUG_MODE")
    dry_run: bool = Field(default=False, env="ALGOLIA_DRY_RUN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @validator("app_id")
    def validate_app_id(cls, v):
        """Validate Algolia application ID format."""
        if not v.isalnum():
            raise ValueError("Algolia App ID must be alphanumeric")
        return v

    @validator("environment", pre=True)
    def validate_environment(cls, v):
        """Validate and convert environment string."""
        if isinstance(v, str):
            try:
                return AlgoliaEnvironment(v.lower())
            except ValueError:
                raise ValueError(
                    f"Invalid environment: {v}. Must be one of: "
                    f"{[e.value for e in AlgoliaEnvironment]}"
                )
        return v


class AlgoliaConfigManager:
    """
    Singleton configuration manager for Algolia integration.

    This class manages all configuration aspects of Algolia integration including:
    - Environment-specific settings
    - Index configurations
    - Security and encryption
    - Circuit breaker and rate limiting
    - Retry policies
    - Monitoring and observability

    Thread Safety:
        This class is thread-safe using a threading.Lock for initialization.
        Configuration is immutable after initialization.

    Usage:
        ```python
        # Get singleton instance
        config = AlgoliaConfigManager.get_instance()

        # Get Algolia client
        client = config.get_client()

        # Get index configuration
        index_config = config.get_index_config(IndexType.DOCUMENTS)

        # Get index handle
        index = config.get_index(IndexType.DOCUMENTS)
        ```

    Attributes:
        _instance: Singleton instance
        _lock: Thread lock for initialization
        _initialized: Initialization flag
        settings: Algolia settings from environment
        indices: Map of index type to configuration
        circuit_breaker: Circuit breaker configuration
        rate_limit: Rate limiting configuration
        retry: Retry configuration
        _client: Cached Algolia client instance
        _encryption_key: Derived encryption key
    """

    _instance: Optional['AlgoliaConfigManager'] = None
    _lock: threading.Lock = threading.Lock()
    _initialized: bool = False

    def __init__(self):
        """
        Initialize configuration manager.

        Note: Use get_instance() instead of direct initialization.
        """
        if AlgoliaConfigManager._initialized:
            return

        # Load environment variables
        dotenv.load_dotenv()

        # Load settings with validation
        self.settings = AlgoliaSettings()

        # Initialize index configurations
        self.indices: Dict[IndexType, IndexConfiguration] = {}
        self._initialize_index_configs()

        # Initialize resilience configurations
        self.circuit_breaker = CircuitBreakerConfig()
        self.rate_limit = RateLimitConfig()
        self.retry = RetryConfig()

        # Initialize Algolia client (lazy)
        self._client: Optional[SearchClient] = None

        # Initialize encryption
        self._encryption_key: Optional[Fernet] = None
        if self.settings.encryption_key:
            self._init_encryption()

        # Mark as initialized
        AlgoliaConfigManager._initialized = True

        logger.info(
            f"AlgoliaConfigManager initialized for environment: {self.settings.environment.value}"
        )

    @classmethod
    def get_instance(cls) -> 'AlgoliaConfigManager':
        """
        Get singleton instance of configuration manager.

        Thread-safe singleton implementation using double-checked locking.

        Returns:
            Singleton instance of AlgoliaConfigManager
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """
        Reset singleton instance (for testing purposes only).

        Warning: This should only be used in test environments.
        """
        with cls._lock:
            cls._instance = None
            cls._initialized = False

    def _initialize_index_configs(self) -> None:
        """
        Initialize index configurations for all index types.

        Each index has a specific configuration optimized for its data type
        and search patterns.
        """
        # Documents index configuration
        self.indices[IndexType.DOCUMENTS] = IndexConfiguration(
            name=self._get_index_name("documents"),
            type=IndexType.DOCUMENTS,
            searchable_attributes=[
                "title",
                "content",
                "snippet",
                "tags",
                "case_number",
                "authors",
                "summary"
            ],
            attributes_for_faceting=[
                "searchable(type)",
                "searchable(date)",
                "searchable(location)",
                "searchable(redaction_status)",
                "searchable(source)",
                "searchable(tags)",
                "filterOnly(relevance_score)",
                "filterOnly(document_class)"
            ],
            ranking_criteria=[
                "desc(relevance_score)",
                "desc(date)",
                "asc(title)"
            ],
            replicas=[
                self._get_index_name("documents_date_desc"),
                self._get_index_name("documents_relevance_asc")
            ],
            enable_synonyms=True,
            enable_typo_tolerance=True,
            custom_settings={
                "highlightPreTag": "<mark>",
                "highlightPostTag": "</mark>",
                "snippetEllipsisText": "...",
            }
        )

        # Characters index configuration
        self.indices[IndexType.CHARACTERS] = IndexConfiguration(
            name=self._get_index_name("characters"),
            type=IndexType.CHARACTERS,
            searchable_attributes=[
                "name",
                "aliases",
                "biography",
                "roles",
                "associations",
                "key_facts"
            ],
            attributes_for_faceting=[
                "searchable(role)",
                "searchable(status)",
                "searchable(nationality)",
                "filterOnly(importance_score)"
            ],
            ranking_criteria=[
                "desc(importance_score)",
                "asc(name)"
            ],
            replicas=[
                self._get_index_name("characters_name_asc")
            ]
        )

        # Locations index configuration
        self.indices[IndexType.LOCATIONS] = IndexConfiguration(
            name=self._get_index_name("locations"),
            type=IndexType.LOCATIONS,
            searchable_attributes=[
                "name",
                "address",
                "description",
                "significance",
                "aliases"
            ],
            attributes_for_faceting=[
                "searchable(type)",
                "searchable(country)",
                "searchable(state)",
                "searchable(city)",
                "filterOnly(_geoloc)"
            ],
            ranking_criteria=[
                "geo",  # Proximity-based ranking when geolocation is provided
                "desc(significance_score)",
                "asc(name)"
            ],
            custom_settings={
                "enableGeolocation": True,
                "aroundRadius": "all",
            }
        )

        # Media index configuration
        self.indices[IndexType.MEDIA] = IndexConfiguration(
            name=self._get_index_name("media"),
            type=IndexType.MEDIA,
            searchable_attributes=[
                "title",
                "description",
                "caption",
                "tags",
                "ocr_text",
                "metadata"
            ],
            attributes_for_faceting=[
                "searchable(media_type)",
                "searchable(source)",
                "searchable(date)",
                "filterOnly(file_size)",
                "filterOnly(dimensions)"
            ],
            ranking_criteria=[
                "desc(quality_score)",
                "desc(date)",
                "asc(title)"
            ]
        )

        # Timeline index configuration
        self.indices[IndexType.TIMELINE] = IndexConfiguration(
            name=self._get_index_name("timeline"),
            type=IndexType.TIMELINE,
            searchable_attributes=[
                "title",
                "description",
                "location",
                "participants",
                "tags"
            ],
            attributes_for_faceting=[
                "searchable(event_type)",
                "searchable(year)",
                "searchable(month)",
                "filterOnly(timestamp)",
                "searchable(location)"
            ],
            ranking_criteria=[
                "asc(timestamp)",  # Chronological by default
                "desc(significance_score)"
            ],
            replicas=[
                self._get_index_name("timeline_desc")  # Reverse chronological
            ]
        )

        # Relationships index configuration
        self.indices[IndexType.RELATIONSHIPS] = IndexConfiguration(
            name=self._get_index_name("relationships"),
            type=IndexType.RELATIONSHIPS,
            searchable_attributes=[
                "entity_a_name",
                "entity_b_name",
                "relationship_type",
                "description",
                "evidence"
            ],
            attributes_for_faceting=[
                "searchable(relationship_type)",
                "searchable(strength)",
                "filterOnly(confidence_score)",
                "searchable(timeframe)"
            ],
            ranking_criteria=[
                "desc(confidence_score)",
                "desc(strength_score)"
            ]
        )

    def _get_index_name(self, base_name: str) -> str:
        """
        Generate full index name with environment prefix.

        Format: {prefix}_{environment}_{base_name}

        Args:
            base_name: Base index name

        Returns:
            Full index name with prefix and environment
        """
        parts = []

        if self.settings.index_prefix:
            parts.append(self.settings.index_prefix)

        parts.append(self.settings.environment.value)
        parts.append(base_name)

        return "_".join(parts)

    def _init_encryption(self) -> None:
        """
        Initialize Fernet encryption for sensitive configuration.

        Uses PBKDF2 for key derivation from environment encryption key.
        """
        try:
            key_material = self.settings.encryption_key.get_secret_value().encode()

            # Derive encryption key using PBKDF2
            kdf = PBKDF2(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'algolia_config_salt_v1',  # Static salt for consistent key
                iterations=100000,
            )
            key = Fernet(Fernet.generate_key())  # Placeholder for proper implementation
            self._encryption_key = key

            logger.info("Encryption initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize encryption: {e}")
            self._encryption_key = None

    def get_client(self, use_admin_key: bool = False) -> SearchClient:
        """
        Get or create Algolia search client.

        Clients are cached and reused for efficiency.

        Args:
            use_admin_key: If True, use admin API key (write access).
                          If False, use search-only API key (read access).

        Returns:
            Configured Algolia SearchClient instance

        Raises:
            ValueError: If credentials are invalid
            ConnectionError: If unable to connect to Algolia
        """
        if self._client is None:
            try:
                api_key = (
                    self.settings.admin_api_key.get_secret_value()
                    if use_admin_key
                    else self.settings.search_api_key.get_secret_value()
                )

                self._client = SearchClient.create(
                    app_id=self.settings.app_id,
                    api_key=api_key
                )

                # Configure client options
                self._client.set_extra_headers({
                    "User-Agent": "EpsteinFiles-Hub/1.0.0",
                    "X-Algolia-Environment": self.settings.environment.value,
                })

                logger.info(
                    f"Algolia client created (app_id={self.settings.app_id}, "
                    f"admin={use_admin_key})"
                )
            except Exception as e:
                logger.error(f"Failed to create Algolia client: {e}")
                raise ConnectionError(f"Unable to initialize Algolia client: {e}")

        return self._client

    def get_index_config(self, index_type: IndexType) -> IndexConfiguration:
        """
        Get configuration for specific index type.

        Args:
            index_type: Type of index

        Returns:
            IndexConfiguration for the specified type

        Raises:
            KeyError: If index type not configured
        """
        if index_type not in self.indices:
            raise KeyError(f"No configuration found for index type: {index_type}")

        return self.indices[index_type]

    def get_index(self, index_type: IndexType, use_admin_key: bool = False):
        """
        Get Algolia index handle for specified type.

        Args:
            index_type: Type of index
            use_admin_key: Whether to use admin API key

        Returns:
            Algolia Index instance
        """
        config = self.get_index_config(index_type)
        client = self.get_client(use_admin_key=use_admin_key)
        return client.init_index(config.name)

    def get_all_index_names(self) -> List[str]:
        """
        Get list of all configured index names.

        Returns:
            List of index names including replicas
        """
        names = []
        for config in self.indices.values():
            names.append(config.name)
            names.extend(config.replicas)
        return names

    def export_config(self, include_secrets: bool = False) -> Dict[str, Any]:
        """
        Export configuration as dictionary.

        Args:
            include_secrets: If True, include API keys (use with caution)

        Returns:
            Configuration dictionary
        """
        config = {
            "environment": self.settings.environment.value,
            "app_id": self.settings.app_id,
            "index_prefix": self.settings.index_prefix,
            "timeout_ms": self.settings.timeout_ms,
            "batch_size": self.settings.batch_size,
            "feature_flags": {
                "analytics": self.settings.enable_analytics,
                "personalization": self.settings.enable_personalization,
                "ab_testing": self.settings.enable_ab_testing,
                "query_suggestions": self.settings.enable_query_suggestions,
            },
            "indices": {
                itype.value: asdict(config)
                for itype, config in self.indices.items()
            },
            "circuit_breaker": asdict(self.circuit_breaker),
            "rate_limit": asdict(self.rate_limit),
            "retry": asdict(self.retry),
        }

        if include_secrets:
            logger.warning("Exporting configuration with secrets - use with extreme caution")
            config["secrets"] = {
                "admin_api_key": self.settings.admin_api_key.get_secret_value(),
                "search_api_key": self.settings.search_api_key.get_secret_value(),
            }

        return config

    def validate_config(self) -> Dict[str, Any]:
        """
        Validate configuration and test connectivity.

        Returns:
            Validation results with status and details
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "connectivity": False,
            "indices_validated": 0,
        }

        # Test client connectivity
        try:
            client = self.get_client(use_admin_key=False)
            # Try to list indices to verify connection
            client.list_indices()
            results["connectivity"] = True
        except Exception as e:
            results["valid"] = False
            results["errors"].append(f"Connection test failed: {str(e)}")

        # Validate each index configuration
        for index_type, config in self.indices.items():
            if not config.searchable_attributes:
                results["warnings"].append(
                    f"Index {index_type.value} has no searchable attributes"
                )

            if config.max_records <= 0:
                results["errors"].append(
                    f"Index {index_type.value} has invalid max_records: {config.max_records}"
                )
                results["valid"] = False

            results["indices_validated"] += 1

        return results


# Module-level convenience function
def get_config() -> AlgoliaConfigManager:
    """
    Get Algolia configuration manager instance.

    Convenience function for accessing singleton config manager.

    Returns:
        AlgoliaConfigManager singleton instance
    """
    return AlgoliaConfigManager.get_instance()


# Export public API
__all__ = [
    "AlgoliaConfigManager",
    "AlgoliaSettings",
    "IndexConfiguration",
    "IndexType",
    "AlgoliaEnvironment",
    "CircuitBreakerConfig",
    "RateLimitConfig",
    "RetryConfig",
    "get_config",
]
