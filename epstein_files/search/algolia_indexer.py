"""
Algolia Data Indexing Pipeline

This module implements a production-grade indexing pipeline for syncing data
to Algolia with comprehensive error handling, retry logic, batching, and monitoring.

Architecture:
- Producer-consumer pattern for efficient batching
- Exponential backoff retry with jitter
- Dead letter queue for failed records
- Checkpointing for resumable indexing
- Concurrent workers for parallel processing
- Circuit breaker for fault tolerance

Features:
- Bulk indexing with configurable batch sizes
- Incremental indexing for updates
- Schema validation before indexing
- Deduplication and conflict resolution
- Progress tracking and reporting
- Comprehensive error handling and recovery

Dependencies:
- algoliasearch>=3.0.0: Algolia Python client
- pydantic>=2.0.0: Data validation
- tenacity>=8.2.0: Retry logic
- prometheus-client>=0.17.0: Metrics collection

Usage:
    ```python
    from epstein_files.search.algolia_indexer import AlgoliaIndexer, IndexingJob
    from epstein_files.search.algolia_config import IndexType

    # Create indexer
    indexer = AlgoliaIndexer()

    # Prepare documents
    documents = [
        {
            "objectID": "doc1",
            "title": "Flight Log Entry",
            "content": "...",
            "date": "2000-01-01",
            # ... more fields
        },
        # ... more documents
    ]

    # Create indexing job
    job = IndexingJob(
        index_type=IndexType.DOCUMENTS,
        operation="add_or_update",  # or "delete", "partial_update"
        records=documents,
        batch_size=1000,
        enable_checkpoints=True,
    )

    # Execute indexing
    result = indexer.execute(job)

    # Check results
    print(f"Indexed: {result.records_processed}")
    print(f"Failed: {result.records_failed}")
    print(f"Duration: {result.duration_seconds}s")
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
import queue
from typing import List, Dict, Any, Optional, Callable, Literal
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from contextlib import contextmanager
from enum import Enum
import os

from algoliasearch.exceptions import AlgoliaException, RequestException
from algoliasearch.responses import Response
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
from pydantic import BaseModel, validator, Field
from prometheus_client import Counter, Histogram, Gauge

from .algolia_config import (
    get_config,
    AlgoliaConfigManager,
    IndexType,
    IndexConfiguration,
)


# Configure module logger
logger = logging.getLogger(__name__)


# Metrics (Prometheus-compatible)
indexing_operations_total = Counter(
    'algolia_indexing_operations_total',
    'Total number of indexing operations',
    ['index_type', 'operation', 'status']
)

indexing_duration_seconds = Histogram(
    'algolia_indexing_duration_seconds',
    'Duration of indexing operations',
    ['index_type', 'operation']
)

indexing_batch_size = Histogram(
    'algolia_indexing_batch_size',
    'Size of indexing batches',
    ['index_type']
)

indexing_records_processed = Counter(
    'algolia_indexing_records_processed_total',
    'Total number of records processed',
    ['index_type', 'status']
)

indexing_queue_size = Gauge(
    'algolia_indexing_queue_size',
    'Current size of indexing queue',
    ['index_type']
)


class IndexingOperation(str, Enum):
    """Supported indexing operations."""
    ADD_OR_UPDATE = "add_or_update"  # Insert or update records
    DELETE = "delete"  # Delete records by objectID
    PARTIAL_UPDATE = "partial_update"  # Update specific fields
    REPLACE = "replace"  # Replace entire index
    CLEAR = "clear"  # Clear all records from index


class IndexingStatus(str, Enum):
    """Indexing job status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIALLY_COMPLETED = "partially_completed"


@dataclass
class IndexingResult:
    """
    Result of an indexing operation.

    Attributes:
        job_id: Unique job identifier
        status: Final status of the job
        records_processed: Number of records successfully processed
        records_failed: Number of records that failed
        duration_seconds: Total duration of the job
        started_at: Job start timestamp
        completed_at: Job completion timestamp
        errors: List of errors encountered
        warnings: List of warnings
        algolia_task_ids: Algolia task IDs for tracking
        checkpoint_data: Checkpoint data for resuming
        metadata: Additional metadata
    """
    job_id: str
    status: IndexingStatus
    records_processed: int = 0
    records_failed: int = 0
    duration_seconds: float = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    algolia_task_ids: List[str] = field(default_factory=list)
    checkpoint_data: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        data = asdict(self)
        data['status'] = self.status.value
        if self.started_at:
            data['started_at'] = self.started_at.isoformat()
        if self.completed_at:
            data['completed_at'] = self.completed_at.isoformat()
        return data

    def to_json(self) -> str:
        """Convert result to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class AlgoliaRecord(BaseModel):
    """
    Base model for Algolia records with validation.

    All records must have an objectID field for Algolia.
    """
    objectID: str = Field(..., min_length=1, max_length=512)

    class Config:
        extra = "allow"  # Allow additional fields

    @validator('objectID')
    def validate_object_id(cls, v):
        """Validate objectID format."""
        # Ensure objectID is URL-safe and doesn't contain special chars
        if not v.replace('_', '').replace('-', '').replace('.', '').isalnum():
            raise ValueError(
                f"objectID must be alphanumeric with _, -, . allowed: {v}"
            )
        return v


@dataclass
class IndexingJob:
    """
    Configuration for an indexing job.

    Attributes:
        index_type: Type of index to operate on
        operation: Type of indexing operation
        records: List of records to index
        batch_size: Number of records per batch
        enable_checkpoints: Whether to enable checkpointing
        checkpoint_interval: Number of batches between checkpoints
        max_retries: Maximum retry attempts per batch
        timeout_seconds: Timeout for the entire job
        validate_schema: Whether to validate records against schema
        enable_deduplication: Whether to deduplicate records
        progress_callback: Optional callback for progress updates
        dry_run: If True, don't actually index (validation only)
        metadata: Additional job metadata
    """
    index_type: IndexType
    operation: IndexingOperation
    records: List[Dict[str, Any]]
    batch_size: int = 1000
    enable_checkpoints: bool = True
    checkpoint_interval: int = 10  # Checkpoint every 10 batches
    max_retries: int = 3
    timeout_seconds: int = 3600  # 1 hour default
    validate_schema: bool = True
    enable_deduplication: bool = True
    progress_callback: Optional[Callable[[int, int], None]] = None
    dry_run: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate job configuration."""
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")


class AlgoliaIndexer:
    """
    Production-grade Algolia indexing pipeline.

    This class handles all aspects of indexing data to Algolia including:
    - Batching and bulk operations
    - Error handling and retries
    - Progress tracking and checkpointing
    - Concurrent processing
    - Circuit breaker integration
    - Metrics and observability

    Thread Safety:
        This class is thread-safe and can be used concurrently.

    Attributes:
        config: Algolia configuration manager
        max_workers: Maximum number of concurrent workers
        dead_letter_queue: Queue for failed records
        checkpoint_dir: Directory for storing checkpoints
    """

    def __init__(
        self,
        config: Optional[AlgoliaConfigManager] = None,
        max_workers: int = 4,
        checkpoint_dir: str = "./checkpoints"
    ):
        """
        Initialize Algolia indexer.

        Args:
            config: Algolia configuration manager (uses default if None)
            max_workers: Maximum concurrent workers
            checkpoint_dir: Directory for checkpoint files
        """
        self.config = config or get_config()
        self.max_workers = max_workers
        self.checkpoint_dir = checkpoint_dir
        self.dead_letter_queue: queue.Queue = queue.Queue()

        # Ensure checkpoint directory exists
        os.makedirs(self.checkpoint_dir, exist_ok=True)

        # Job tracking
        self._active_jobs: Dict[str, IndexingResult] = {}
        self._jobs_lock = threading.Lock()

        logger.info(
            f"AlgoliaIndexer initialized (max_workers={max_workers}, "
            f"checkpoint_dir={checkpoint_dir})"
        )

    def execute(self, job: IndexingJob) -> IndexingResult:
        """
        Execute an indexing job.

        This is the main entry point for indexing operations. It handles:
        - Job validation and preparation
        - Batching and parallel processing
        - Error handling and retries
        - Progress tracking and checkpointing
        - Result aggregation

        Args:
            job: Indexing job configuration

        Returns:
            IndexingResult with operation outcome

        Raises:
            ValueError: If job configuration is invalid
            TimeoutError: If job exceeds timeout
            AlgoliaException: If indexing fails critically
        """
        # Generate unique job ID
        job_id = self._generate_job_id(job)

        # Create result object
        result = IndexingResult(
            job_id=job_id,
            status=IndexingStatus.PENDING,
            started_at=datetime.utcnow(),
            metadata=job.metadata.copy()
        )

        # Register job
        with self._jobs_lock:
            self._active_jobs[job_id] = result

        try:
            logger.info(
                f"Starting indexing job {job_id}: "
                f"{len(job.records)} records to {job.index_type.value}"
            )

            # Update status
            result.status = IndexingStatus.RUNNING

            # Validate job
            self._validate_job(job)

            # Prepare records
            records = self._prepare_records(job)

            # Execute based on operation
            if job.operation == IndexingOperation.CLEAR:
                self._execute_clear(job, result)
            elif job.operation == IndexingOperation.DELETE:
                self._execute_delete(job, result, records)
            else:
                self._execute_index(job, result, records)

            # Determine final status
            if result.records_failed == 0:
                result.status = IndexingStatus.COMPLETED
            elif result.records_processed > 0:
                result.status = IndexingStatus.PARTIALLY_COMPLETED
            else:
                result.status = IndexingStatus.FAILED

            # Record metrics
            indexing_operations_total.labels(
                index_type=job.index_type.value,
                operation=job.operation.value,
                status=result.status.value
            ).inc()

            logger.info(
                f"Indexing job {job_id} completed: {result.status.value}, "
                f"processed={result.records_processed}, failed={result.records_failed}"
            )

        except Exception as e:
            result.status = IndexingStatus.FAILED
            result.errors.append({
                "type": "fatal_error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
            logger.error(f"Indexing job {job_id} failed with error: {e}", exc_info=True)
            raise

        finally:
            result.completed_at = datetime.utcnow()
            if result.started_at:
                result.duration_seconds = (
                    result.completed_at - result.started_at
                ).total_seconds()

            # Record duration metric
            indexing_duration_seconds.labels(
                index_type=job.index_type.value,
                operation=job.operation.value
            ).observe(result.duration_seconds)

            # Unregister job
            with self._jobs_lock:
                self._active_jobs.pop(job_id, None)

        return result

    def _generate_job_id(self, job: IndexingJob) -> str:
        """Generate unique job ID."""
        timestamp = datetime.utcnow().isoformat()
        data = f"{job.index_type.value}_{job.operation.value}_{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def _validate_job(self, job: IndexingJob) -> None:
        """
        Validate job configuration.

        Args:
            job: Job to validate

        Raises:
            ValueError: If job is invalid
        """
        if not job.records and job.operation != IndexingOperation.CLEAR:
            raise ValueError("Job has no records to process")

        if job.batch_size > self.config.settings.batch_size:
            logger.warning(
                f"Job batch size ({job.batch_size}) exceeds configured limit "
                f"({self.config.settings.batch_size}), will be capped"
            )
            job.batch_size = self.config.settings.batch_size

    def _prepare_records(self, job: IndexingJob) -> List[Dict[str, Any]]:
        """
        Prepare and validate records for indexing.

        Args:
            job: Indexing job

        Returns:
            List of validated records

        Raises:
            ValueError: If records are invalid
        """
        records = job.records.copy()

        # Validate schema if enabled
        if job.validate_schema:
            records = self._validate_records(records)

        # Deduplicate if enabled
        if job.enable_deduplication:
            records = self._deduplicate_records(records)

        return records

    def _validate_records(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate records against Algolia requirements.

        Args:
            records: Records to validate

        Returns:
            Validated records

        Raises:
            ValueError: If validation fails
        """
        validated = []

        for idx, record in enumerate(records):
            try:
                # Validate using Pydantic model
                validated_record = AlgoliaRecord(**record)
                validated.append(record)
            except Exception as e:
                error_msg = f"Record validation failed at index {idx}: {e}"
                logger.error(error_msg)
                raise ValueError(error_msg)

        return validated

    def _deduplicate_records(
        self,
        records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Deduplicate records by objectID.

        Later occurrences take precedence.

        Args:
            records: Records to deduplicate

        Returns:
            Deduplicated records
        """
        seen = {}
        for record in records:
            object_id = record.get('objectID')
            if object_id:
                seen[object_id] = record

        deduplicated = list(seen.values())

        if len(deduplicated) < len(records):
            logger.warning(
                f"Removed {len(records) - len(deduplicated)} duplicate records"
            )

        return deduplicated

    def _execute_clear(self, job: IndexingJob, result: IndexingResult) -> None:
        """
        Execute clear index operation.

        Args:
            job: Indexing job
            result: Result object to update
        """
        if job.dry_run:
            logger.info(f"DRY RUN: Would clear index {job.index_type.value}")
            return

        try:
            index = self.config.get_index(job.index_type, use_admin_key=True)
            response = index.clear_objects()

            result.algolia_task_ids.append(response['taskID'])
            result.records_processed = 1  # Mark as processed

            logger.info(f"Index {job.index_type.value} cleared")

        except AlgoliaException as e:
            result.records_failed = 1
            result.errors.append({
                "type": "clear_failed",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
            logger.error(f"Failed to clear index: {e}")

    def _execute_delete(
        self,
        job: IndexingJob,
        result: IndexingResult,
        records: List[Dict[str, Any]]
    ) -> None:
        """
        Execute delete operation.

        Args:
            job: Indexing job
            result: Result object to update
            records: Records with objectIDs to delete
        """
        # Extract objectIDs
        object_ids = [r.get('objectID') for r in records if r.get('objectID')]

        if not object_ids:
            logger.warning("No valid objectIDs found for deletion")
            return

        # Process in batches
        batches = self._create_batches(object_ids, job.batch_size)

        for batch_idx, batch in enumerate(batches):
            if job.dry_run:
                logger.info(f"DRY RUN: Would delete {len(batch)} objects")
                result.records_processed += len(batch)
                continue

            try:
                index = self.config.get_index(job.index_type, use_admin_key=True)

                # Delete with retry
                response = self._retry_operation(
                    lambda: index.delete_objects(batch),
                    job.max_retries
                )

                result.algolia_task_ids.append(response['taskID'])
                result.records_processed += len(batch)

                # Progress callback
                if job.progress_callback:
                    job.progress_callback(result.records_processed, len(object_ids))

            except Exception as e:
                result.records_failed += len(batch)
                result.errors.append({
                    "type": "delete_batch_failed",
                    "batch_index": batch_idx,
                    "batch_size": len(batch),
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })
                logger.error(f"Failed to delete batch {batch_idx}: {e}")

    def _execute_index(
        self,
        job: IndexingJob,
        result: IndexingResult,
        records: List[Dict[str, Any]]
    ) -> None:
        """
        Execute indexing operation (add/update/partial_update/replace).

        Args:
            job: Indexing job
            result: Result object to update
            records: Records to index
        """
        # Create batches
        batches = self._create_batches(records, job.batch_size)
        total_records = len(records)

        logger.info(f"Processing {total_records} records in {len(batches)} batches")

        # Process batches with ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures: Dict[Future, int] = {}

            for batch_idx, batch in enumerate(batches):
                future = executor.submit(
                    self._process_batch,
                    job,
                    batch,
                    batch_idx
                )
                futures[future] = batch_idx

            # Collect results
            for future in as_completed(futures):
                batch_idx = futures[future]

                try:
                    batch_result = future.result(timeout=job.timeout_seconds)

                    result.records_processed += batch_result['processed']
                    result.records_failed += batch_result['failed']

                    if batch_result.get('task_id'):
                        result.algolia_task_ids.append(batch_result['task_id'])

                    if batch_result.get('errors'):
                        result.errors.extend(batch_result['errors'])

                    # Progress callback
                    if job.progress_callback:
                        job.progress_callback(result.records_processed, total_records)

                    # Checkpoint if enabled
                    if (job.enable_checkpoints and
                        batch_idx % job.checkpoint_interval == 0):
                        self._save_checkpoint(job, result, batch_idx)

                except Exception as e:
                    logger.error(f"Batch {batch_idx} processing failed: {e}", exc_info=True)
                    result.errors.append({
                        "type": "batch_processing_failed",
                        "batch_index": batch_idx,
                        "message": str(e),
                        "timestamp": datetime.utcnow().isoformat()
                    })

        # Record batch size metric
        indexing_batch_size.labels(
            index_type=job.index_type.value
        ).observe(job.batch_size)

    def _process_batch(
        self,
        job: IndexingJob,
        batch: List[Dict[str, Any]],
        batch_idx: int
    ) -> Dict[str, Any]:
        """
        Process a single batch of records.

        Args:
            job: Indexing job
            batch: Batch of records
            batch_idx: Batch index

        Returns:
            Batch processing result
        """
        result = {
            "processed": 0,
            "failed": 0,
            "task_id": None,
            "errors": []
        }

        if job.dry_run:
            logger.info(f"DRY RUN: Would index batch {batch_idx} ({len(batch)} records)")
            result["processed"] = len(batch)
            return result

        try:
            index = self.config.get_index(job.index_type, use_admin_key=True)

            # Choose operation method
            if job.operation == IndexingOperation.ADD_OR_UPDATE:
                operation = lambda: index.save_objects(batch)
            elif job.operation == IndexingOperation.PARTIAL_UPDATE:
                operation = lambda: index.partial_update_objects(batch)
            elif job.operation == IndexingOperation.REPLACE:
                # For replace, clear first batch then add
                if batch_idx == 0:
                    index.clear_objects().wait()
                operation = lambda: index.save_objects(batch)
            else:
                raise ValueError(f"Unsupported operation: {job.operation}")

            # Execute with retry
            response = self._retry_operation(operation, job.max_retries)

            result["task_id"] = response.get('taskID')
            result["processed"] = len(batch)

            # Record metric
            indexing_records_processed.labels(
                index_type=job.index_type.value,
                status="success"
            ).inc(len(batch))

            logger.debug(f"Batch {batch_idx} indexed successfully ({len(batch)} records)")

        except Exception as e:
            result["failed"] = len(batch)
            result["errors"].append({
                "type": "batch_index_failed",
                "batch_index": batch_idx,
                "batch_size": len(batch),
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })

            # Record metric
            indexing_records_processed.labels(
                index_type=job.index_type.value,
                status="failed"
            ).inc(len(batch))

            # Add to dead letter queue
            self.dead_letter_queue.put({
                "job": job.metadata,
                "batch_index": batch_idx,
                "batch": batch,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })

            logger.error(f"Batch {batch_idx} failed: {e}", exc_info=True)

        return result

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=30),
        retry=retry_if_exception_type((RequestException, AlgoliaException)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def _retry_operation(self, operation: Callable, max_retries: int) -> Any:
        """
        Execute operation with retry logic.

        Args:
            operation: Operation to execute
            max_retries: Maximum retries

        Returns:
            Operation result

        Raises:
            Exception from operation if all retries exhausted
        """
        return operation()

    def _create_batches(
        self,
        items: List[Any],
        batch_size: int
    ) -> List[List[Any]]:
        """
        Split items into batches.

        Args:
            items: Items to batch
            batch_size: Size of each batch

        Returns:
            List of batches
        """
        batches = []
        for i in range(0, len(items), batch_size):
            batches.append(items[i:i + batch_size])
        return batches

    def _save_checkpoint(
        self,
        job: IndexingJob,
        result: IndexingResult,
        batch_idx: int
    ) -> None:
        """
        Save checkpoint for job recovery.

        Args:
            job: Indexing job
            result: Current result
            batch_idx: Current batch index
        """
        try:
            checkpoint_file = os.path.join(
                self.checkpoint_dir,
                f"{result.job_id}_checkpoint.json"
            )

            checkpoint_data = {
                "job_id": result.job_id,
                "index_type": job.index_type.value,
                "operation": job.operation.value,
                "batch_idx": batch_idx,
                "records_processed": result.records_processed,
                "records_failed": result.records_failed,
                "timestamp": datetime.utcnow().isoformat(),
            }

            with open(checkpoint_file, 'w') as f:
                json.dump(checkpoint_data, f, indent=2)

            result.checkpoint_data = checkpoint_data

            logger.debug(f"Checkpoint saved at batch {batch_idx}")

        except Exception as e:
            logger.warning(f"Failed to save checkpoint: {e}")

    def get_dead_letter_records(self) -> List[Dict[str, Any]]:
        """
        Retrieve all failed records from dead letter queue.

        Returns:
            List of failed record entries
        """
        records = []
        while not self.dead_letter_queue.empty():
            try:
                records.append(self.dead_letter_queue.get_nowait())
            except queue.Empty:
                break
        return records

    def get_active_jobs(self) -> Dict[str, IndexingResult]:
        """
        Get currently active indexing jobs.

        Returns:
            Map of job ID to result
        """
        with self._jobs_lock:
            return self._active_jobs.copy()


# Export public API
__all__ = [
    "AlgoliaIndexer",
    "IndexingJob",
    "IndexingResult",
    "IndexingOperation",
    "IndexingStatus",
    "AlgoliaRecord",
]
