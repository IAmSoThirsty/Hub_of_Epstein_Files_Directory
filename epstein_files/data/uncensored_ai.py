"""
Uncensored.ai Integration Manager

Handles fetching and managing Epstein-related files from the Uncensored.ai free database.
This module provides continuous data extraction and ingestion capabilities.
"""

import requests
import hashlib
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class UncensoredAIManager:
    """Manager for Uncensored.ai data operations."""
    
    def __init__(self, config_manager, data_manager, cache_manager):
        """
        Initialize the Uncensored.ai manager.
        
        Args:
            config_manager: ConfigManager instance
            data_manager: DataManager instance
            cache_manager: CacheManager instance
        """
        self.config = config_manager
        self.data = data_manager
        self.cache = cache_manager
        
        # Get configuration
        self.enabled = self.config.get("uncensored_ai_enabled", True)
        self.base_url = self.config.get(
            "uncensored_ai_base_url", 
            "https://api.uncensored.ai/v1"
        )
        self.api_key = self.config.get("uncensored_ai_api_key", None)
        self.rate_limit_delay = self.config.get("uncensored_ai_rate_limit", 2)
        
        # Setup output directory
        self.output_dir = Path(self.config.get(
            "uncensored_files_dir",
            "./data/uncensored_files"
        ))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / 'documents').mkdir(exist_ok=True)
        (self.output_dir / 'images').mkdir(exist_ok=True)
        (self.output_dir / 'videos').mkdir(exist_ok=True)
        (self.output_dir / 'flight_logs').mkdir(exist_ok=True)
        (self.output_dir / 'financial').mkdir(exist_ok=True)
        (self.output_dir / 'metadata').mkdir(exist_ok=True)
        
        # Setup HTTP session
        self.session = requests.Session()
        
        # Get user agent from config or use default
        user_agent = self.config.get(
            "user_agent",
            "Mozilla/5.0 (compatible; EpsteinFilesBot/1.0)"
        )
        
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'application/json',
        })
        
        if self.api_key:
            self.session.headers['Authorization'] = f'Bearer {self.api_key}'
    
    def fetch_documents(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetch court documents and legal filings.
        
        Args:
            limit: Optional limit on number of documents to fetch
            
        Returns:
            Dictionary with fetch results
        """
        if not self.enabled:
            return {"status": "disabled", "files_fetched": 0}
        
        # Check cache first
        cache_key = "uncensored_documents"
        cached = self.cache.get(cache_key, "uncensored_ai")
        if cached is not None:
            return cached
        
        results = {
            "source": "Uncensored.ai - Documents",
            "files_fetched": 0,
            "files_skipped": 0,
            "errors": [],
            "files": []
        }
        
        try:
            # Query documents endpoint
            endpoint = f"{self.base_url}/epstein/documents"
            params = {"limit": limit or 100}
            
            response = self.session.get(endpoint, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                documents = data.get('documents', [])
                
                for doc in documents:
                    doc_id = doc.get('id')
                    doc_type = doc.get('type', 'document')
                    
                    # Check for duplicates
                    if self._is_duplicate(doc):
                        results["files_skipped"] += 1
                        continue
                    
                    # Download document
                    file_path = self._download_file(
                        doc.get('url'),
                        self.output_dir / 'documents',
                        f"{doc_type}_{doc_id}"
                    )
                    
                    if file_path:
                        # Extract and save metadata
                        metadata = self._extract_metadata(doc, file_path)
                        self._save_metadata(doc_id, metadata, 'documents')
                        
                        results["files_fetched"] += 1
                        results["files"].append({
                            "id": doc_id,
                            "type": doc_type,
                            "path": str(file_path)
                        })
                        
                        # Respect rate limits
                        time.sleep(self.rate_limit_delay)
                    else:
                        results["errors"].append(f"Failed to download: {doc_id}")
            
            else:
                results["errors"].append(f"API error: {response.status_code}")
        
        except Exception as e:
            results["errors"].append(f"Exception: {str(e)}")
        
        # Cache results
        self.cache.set(cache_key, results, "uncensored_ai")
        
        return results
    
    def fetch_images(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetch photos and scanned documents.
        
        Args:
            limit: Optional limit on number of images to fetch
            
        Returns:
            Dictionary with fetch results
        """
        if not self.enabled:
            return {"status": "disabled", "files_fetched": 0}
        
        results = {
            "source": "Uncensored.ai - Images",
            "files_fetched": 0,
            "files_skipped": 0,
            "errors": [],
            "files": []
        }
        
        try:
            endpoint = f"{self.base_url}/epstein/images"
            params = {"limit": limit or 100}
            
            response = self.session.get(endpoint, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                images = data.get('images', [])
                
                for img in images:
                    img_id = img.get('id')
                    
                    # Check for duplicates
                    if self._is_duplicate(img):
                        results["files_skipped"] += 1
                        continue
                    
                    # Download image
                    file_path = self._download_file(
                        img.get('url'),
                        self.output_dir / 'images',
                        f"image_{img_id}"
                    )
                    
                    if file_path:
                        metadata = self._extract_metadata(img, file_path)
                        self._save_metadata(img_id, metadata, 'images')
                        
                        results["files_fetched"] += 1
                        results["files"].append({
                            "id": img_id,
                            "path": str(file_path)
                        })
                        
                        time.sleep(self.rate_limit_delay)
                    else:
                        results["errors"].append(f"Failed to download: {img_id}")
            
            else:
                results["errors"].append(f"API error: {response.status_code}")
        
        except Exception as e:
            results["errors"].append(f"Exception: {str(e)}")
        
        return results
    
    def fetch_flight_logs(self) -> Dict[str, Any]:
        """
        Fetch aviation records and flight manifests.
        
        Returns:
            Dictionary with fetch results
        """
        if not self.enabled:
            return {"status": "disabled", "files_fetched": 0}
        
        results = {
            "source": "Uncensored.ai - Flight Logs",
            "files_fetched": 0,
            "files_skipped": 0,
            "errors": [],
            "files": []
        }
        
        try:
            endpoint = f"{self.base_url}/epstein/flight-logs"
            
            response = self.session.get(endpoint, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                logs = data.get('logs', [])
                
                for log in logs:
                    log_id = log.get('id')
                    
                    # Check for duplicates
                    if self._is_duplicate(log):
                        results["files_skipped"] += 1
                        continue
                    
                    # Download flight log
                    file_path = self._download_file(
                        log.get('url'),
                        self.output_dir / 'flight_logs',
                        f"flight_log_{log_id}"
                    )
                    
                    if file_path:
                        metadata = self._extract_metadata(log, file_path)
                        self._save_metadata(log_id, metadata, 'flight_logs')
                        
                        results["files_fetched"] += 1
                        results["files"].append({
                            "id": log_id,
                            "path": str(file_path)
                        })
                        
                        time.sleep(self.rate_limit_delay)
                    else:
                        results["errors"].append(f"Failed to download: {log_id}")
            
            else:
                results["errors"].append(f"API error: {response.status_code}")
        
        except Exception as e:
            results["errors"].append(f"Exception: {str(e)}")
        
        return results
    
    def fetch_financial_records(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetch financial documents and transaction records.
        
        Args:
            limit: Optional limit on number of records to fetch
            
        Returns:
            Dictionary with fetch results
        """
        if not self.enabled:
            return {"status": "disabled", "files_fetched": 0}
        
        results = {
            "source": "Uncensored.ai - Financial Records",
            "files_fetched": 0,
            "files_skipped": 0,
            "errors": [],
            "files": []
        }
        
        try:
            endpoint = f"{self.base_url}/epstein/financial"
            params = {"limit": limit or 50}
            
            response = self.session.get(endpoint, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                records = data.get('records', [])
                
                for record in records:
                    record_id = record.get('id')
                    
                    # Check for duplicates
                    if self._is_duplicate(record):
                        results["files_skipped"] += 1
                        continue
                    
                    # Download financial record
                    file_path = self._download_file(
                        record.get('url'),
                        self.output_dir / 'financial',
                        f"financial_{record_id}"
                    )
                    
                    if file_path:
                        metadata = self._extract_metadata(record, file_path)
                        self._save_metadata(record_id, metadata, 'financial')
                        
                        results["files_fetched"] += 1
                        results["files"].append({
                            "id": record_id,
                            "path": str(file_path)
                        })
                        
                        time.sleep(self.rate_limit_delay)
                    else:
                        results["errors"].append(f"Failed to download: {record_id}")
            
            else:
                results["errors"].append(f"API error: {response.status_code}")
        
        except Exception as e:
            results["errors"].append(f"Exception: {str(e)}")
        
        return results
    
    def fetch_all(self, categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Fetch all Epstein files from Uncensored.ai.
        
        Args:
            categories: Optional list of categories to fetch
            
        Returns:
            Dictionary with fetch results
        """
        if not self.enabled:
            return {
                "status": "disabled",
                "message": "Uncensored.ai integration is disabled in configuration"
            }
        
        all_categories = categories or [
            "documents", "images", "flight_logs", "financial"
        ]
        
        results = {
            "total_files": 0,
            "total_skipped": 0,
            "categories": {},
            "started_at": datetime.utcnow().isoformat(),
        }
        
        if "documents" in all_categories:
            doc_results = self.fetch_documents()
            results["categories"]["documents"] = doc_results
            results["total_files"] += doc_results.get("files_fetched", 0)
            results["total_skipped"] += doc_results.get("files_skipped", 0)
        
        if "images" in all_categories:
            img_results = self.fetch_images()
            results["categories"]["images"] = img_results
            results["total_files"] += img_results.get("files_fetched", 0)
            results["total_skipped"] += img_results.get("files_skipped", 0)
        
        if "flight_logs" in all_categories:
            log_results = self.fetch_flight_logs()
            results["categories"]["flight_logs"] = log_results
            results["total_files"] += log_results.get("files_fetched", 0)
            results["total_skipped"] += log_results.get("files_skipped", 0)
        
        if "financial" in all_categories:
            fin_results = self.fetch_financial_records()
            results["categories"]["financial"] = fin_results
            results["total_files"] += fin_results.get("files_fetched", 0)
            results["total_skipped"] += fin_results.get("files_skipped", 0)
        
        results["completed_at"] = datetime.utcnow().isoformat()
        
        # Save complete manifest
        self._save_complete_manifest(results)
        
        return results
    
    def _download_file(self, url: str, output_dir: Path, 
                      filename_prefix: str) -> Optional[Path]:
        """
        Download a file from URL.
        
        Args:
            url: File URL
            output_dir: Output directory
            filename_prefix: Prefix for output filename
            
        Returns:
            Path to downloaded file or None if failed
        """
        if not url:
            return None
        
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=60, stream=True)
                response.raise_for_status()
                
                # Determine file extension from content type or URL
                content_type = response.headers.get('content-type', '')
                extension = self._get_extension(content_type, url)
                
                output_path = output_dir / f"{filename_prefix}{extension}"
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                return output_path
            
            except Exception as e:
                if attempt < max_retries - 1:
                    # Log retry attempt
                    import logging
                    logger = logging.getLogger("EpsteinHub.UncensoredAI")
                    logger.warning(f"Download attempt {attempt + 1} failed for {url}: {e}")
                    time.sleep(retry_delay)
                else:
                    # Log final failure
                    import logging
                    logger = logging.getLogger("EpsteinHub.UncensoredAI")
                    logger.error(f"Download failed after {max_retries} attempts for {url}: {e}")
                    return None
        
        return None
    
    def _get_extension(self, content_type: str, url: str) -> str:
        """Determine file extension from content type or URL."""
        # Map common content types
        type_map = {
            'application/pdf': '.pdf',
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'video/mp4': '.mp4',
            'text/plain': '.txt',
            'application/json': '.json',
        }
        
        extension = type_map.get(content_type.split(';')[0].strip(), '')
        
        if not extension and url:
            # Try to get from URL
            path = Path(url)
            extension = path.suffix
        
        return extension or '.dat'
    
    def _is_duplicate(self, item: Dict[str, Any]) -> bool:
        """
        Check if item is a duplicate.
        
        Args:
            item: Item dictionary with id/hash
            
        Returns:
            True if duplicate exists
        """
        item_id = item.get('id')
        item_hash = item.get('hash') or item.get('sha256')
        
        # Check by ID
        if item_id:
            metadata_file = self.output_dir / 'metadata' / f"{item_id}.json"
            if metadata_file.exists():
                return True
        
        # Check by hash if available
        if item_hash:
            # Search through existing metadata
            metadata_dir = self.output_dir / 'metadata'
            for meta_file in metadata_dir.glob('*.json'):
                try:
                    with open(meta_file, 'r') as f:
                        meta = json.load(f)
                        if meta.get('hash') == item_hash or meta.get('sha256') == item_hash:
                            return True
                except (json.JSONDecodeError, IOError, OSError):
                    # Skip corrupted or unreadable metadata files
                    pass
        
        return False
    
    def _extract_metadata(self, item: Dict[str, Any], 
                         file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from item and file.
        
        Args:
            item: Item dictionary from API
            file_path: Path to downloaded file
            
        Returns:
            Metadata dictionary
        """
        # Calculate file hash
        file_hash = self._calculate_hash(file_path)
        
        metadata = {
            "id": item.get('id'),
            "source": "Uncensored.ai",
            "url": item.get('url'),
            "type": item.get('type'),
            "title": item.get('title'),
            "description": item.get('description'),
            "date": item.get('date'),
            "download_date": datetime.utcnow().isoformat(),
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "sha256": file_hash,
            "tags": item.get('tags', []),
            "related_entities": item.get('related_entities', []),
        }
        
        return metadata
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _save_metadata(self, item_id: str, metadata: Dict[str, Any], 
                      category: str) -> None:
        """Save metadata to JSON file."""
        metadata_file = self.output_dir / 'metadata' / f"{category}_{item_id}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _save_complete_manifest(self, results: Dict[str, Any]) -> None:
        """Save complete manifest of all fetched files."""
        manifest_file = self.output_dir / 'uncensored_manifest.json'
        with open(manifest_file, 'w') as f:
            json.dump(results, f, indent=2)
    
    def verify_file(self, filepath: Path, expected_hash: Optional[str] = None) -> bool:
        """
        Verify a file's integrity.
        
        Args:
            filepath: Path to file
            expected_hash: Expected SHA-256 hash
            
        Returns:
            True if file is valid
        """
        if not filepath.exists():
            return False
        
        if expected_hash:
            file_hash = self._calculate_hash(filepath)
            return file_hash == expected_hash
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about fetched files.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_files": 0,
            "by_category": {},
            "total_size_bytes": 0,
        }
        
        for category in ['documents', 'images', 'videos', 'flight_logs', 'financial']:
            category_dir = self.output_dir / category
            if category_dir.exists():
                files = list(category_dir.iterdir())
                stats["by_category"][category] = len(files)
                stats["total_files"] += len(files)
                
                for file in files:
                    if file.is_file():
                        stats["total_size_bytes"] += file.stat().st_size
        
        stats["total_size_mb"] = round(stats["total_size_bytes"] / (1024 * 1024), 2)
        
        return stats
    
    def __repr__(self) -> str:
        stats = self.get_statistics()
        return f"UncensoredAIManager(files={stats['total_files']}, enabled={self.enabled})"
