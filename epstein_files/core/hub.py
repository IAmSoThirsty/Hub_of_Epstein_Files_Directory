"""
Hub - Central Control System for Epstein Files Hub

The sovereign monolithic interface that orchestrates all operations.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

from .config_manager import ConfigManager
from .data_manager import DataManager
from .cache_manager import CacheManager


class Hub:
    """
    Central Hub for all operations.
    
    This is the monolithic sovereign interface that provides:
    - Unified API for all operations
    - Centralized state management
    - Integrated workflows
    - System-wide coordination
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the Hub.
        
        Args:
            config_path: Optional path to configuration file
        """
        # Initialize core managers
        self.config = ConfigManager(config_path)
        self.data = DataManager(self.config)
        self.cache = CacheManager(self.config)
        
        # Ensure all directories exist
        self.config.ensure_directories()
        
        # Setup logging
        self._setup_logging()
        
        # Initialize subsystems (lazy loading)
        self._public_files = None
        self._wikipedia = None
        self._uncensored_ai = None
        self._pdf_processor = None
        self._search_indexer = None
        self._agents = None
        
        self.logger.info("Hub initialized successfully")
    
    def _setup_logging(self) -> None:
        """Setup logging system."""
        log_dir = self.config.get_paths()["logs"]
        log_file = log_dir / "hub.log"
        
        logging.basicConfig(
            level=logging.DEBUG if self.config.get("debug_mode") else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("EpsteinHub")
    
    @property
    def public_files(self):
        """Lazy load public files module."""
        if self._public_files is None:
            from ..data.public_files import PublicFilesManager
            self._public_files = PublicFilesManager(self.config, self.data, self.cache)
        return self._public_files
    
    @property
    def wikipedia(self):
        """Lazy load Wikipedia module."""
        if self._wikipedia is None:
            from ..data.wikipedia import WikipediaManager
            self._wikipedia = WikipediaManager(self.config, self.data, self.cache)
        return self._wikipedia
    
    @property
    def uncensored_ai(self):
        """Lazy load Uncensored.ai module."""
        if self._uncensored_ai is None:
            from ..data.uncensored_ai import UncensoredAIManager
            self._uncensored_ai = UncensoredAIManager(self.config, self.data, self.cache)
        return self._uncensored_ai
    
    @property
    def pdf_processor(self):
        """Lazy load PDF processor."""
        if self._pdf_processor is None:
            from ..processing.pdf_processor import PDFProcessor
            self._pdf_processor = PDFProcessor(self.config, self.data, self.cache)
        return self._pdf_processor
    
    @property
    def search_indexer(self):
        """Lazy load search indexer."""
        if self._search_indexer is None:
            from ..search.indexer import SearchIndexer
            self._search_indexer = SearchIndexer(self.config, self.data, self.cache)
        return self._search_indexer
    
    @property
    def agents(self):
        """Lazy load agents system."""
        if self._agents is None:
            from ..agents.agent_manager import AgentManager
            self._agents = AgentManager(self.config, self.data, self.cache)
        return self._agents
    
    # High-level operations
    
    def fetch_public_files(self, sources: Optional[List[str]] = None, 
                          force_refresh: bool = False) -> Dict[str, Any]:
        """
        Fetch public files from various sources.
        
        Args:
            sources: Optional list of sources to fetch from
            force_refresh: Force refresh even if cached
            
        Returns:
            Dictionary with fetch results
        """
        self.logger.info("Fetching public files...")
        
        if force_refresh:
            self.cache.clear("public_files")
        
        results = self.public_files.fetch_all(sources)
        
        self.logger.info(f"Fetched {results.get('total_files', 0)} files")
        return results
    
    def fetch_wikipedia_data(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Fetch Wikipedia data.
        
        Args:
            force_refresh: Force refresh even if cached
            
        Returns:
            Dictionary with fetch results
        """
        self.logger.info("Fetching Wikipedia data...")
        
        if force_refresh:
            self.cache.clear("wikipedia")
        
        results = self.wikipedia.fetch_all()
        
        self.logger.info(f"Fetched data for {results.get('total_entries', 0)} entries")
        return results
    
    def fetch_uncensored_files(self, categories: Optional[List[str]] = None,
                               force_refresh: bool = False) -> Dict[str, Any]:
        """
        Fetch Epstein files from Uncensored.ai.
        
        Args:
            categories: Optional list of categories to fetch
            force_refresh: Force refresh even if cached
            
        Returns:
            Dictionary with fetch results
        """
        self.logger.info("Fetching Uncensored.ai files...")
        
        if force_refresh:
            self.cache.clear("uncensored_ai")
        
        results = self.uncensored_ai.fetch_all(categories)
        
        self.logger.info(f"Fetched {results.get('total_files', 0)} files from Uncensored.ai")
        return results
    
    def process_documents(self, input_dir: Optional[Path] = None,
                         enable_ocr: Optional[bool] = None) -> Dict[str, Any]:
        """
        Process PDF documents.
        
        Args:
            input_dir: Optional input directory (uses public_files if None)
            enable_ocr: Optional OCR setting (uses config if None)
            
        Returns:
            Dictionary with processing results
        """
        self.logger.info("Processing documents...")
        
        if enable_ocr is None:
            enable_ocr = self.config.get("enable_ocr")
        
        results = self.pdf_processor.process_all(input_dir, enable_ocr)
        
        self.logger.info(f"Processed {results.get('total_processed', 0)} documents")
        return results
    
    def generate_search_index(self, force_rebuild: bool = False) -> Dict[str, Any]:
        """
        Generate search index.
        
        Args:
            force_rebuild: Force rebuild even if index exists
            
        Returns:
            Dictionary with indexing results
        """
        self.logger.info("Generating search index...")
        
        if force_rebuild:
            self.cache.clear("search_index")
        
        results = self.search_indexer.build_index()
        
        self.logger.info(f"Indexed {results.get('total_documents', 0)} documents")
        return results
    
    def run_full_pipeline(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Run the complete data pipeline.
        
        Args:
            force_refresh: Force refresh all data
            
        Returns:
            Dictionary with pipeline results
        """
        self.logger.info("Starting full pipeline...")
        
        pipeline_results = {
            "started_at": None,
            "completed_at": None,
            "steps": {},
        }
        
        from datetime import datetime
        pipeline_results["started_at"] = datetime.utcnow().isoformat()
        
        # Step 1: Fetch public files
        pipeline_results["steps"]["fetch_public_files"] = self.fetch_public_files(
            force_refresh=force_refresh
        )
        
        # Step 2: Fetch Wikipedia data
        pipeline_results["steps"]["fetch_wikipedia"] = self.fetch_wikipedia_data(
            force_refresh=force_refresh
        )
        
        # Step 3: Fetch Uncensored.ai files
        pipeline_results["steps"]["fetch_uncensored"] = self.fetch_uncensored_files(
            force_refresh=force_refresh
        )
        
        # Step 4: Process documents
        pipeline_results["steps"]["process_documents"] = self.process_documents()
        
        # Step 5: Generate search index
        pipeline_results["steps"]["generate_index"] = self.generate_search_index(
            force_rebuild=force_refresh
        )
        
        pipeline_results["completed_at"] = datetime.utcnow().isoformat()
        
        self.logger.info("Full pipeline completed successfully")
        return pipeline_results
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status.
        
        Returns:
            Dictionary with system status
        """
        return {
            "config": {
                "valid": self.config.validate(),
                "debug_mode": self.config.get("debug_mode"),
                "paths": {k: str(v) for k, v in self.config.get_paths().items()},
            },
            "data": self.data.get_statistics(),
            "cache": self.cache.get_stats(),
            "agents": self.agents.get_status() if self._agents else {"loaded": False},
        }
    
    def cleanup(self) -> Dict[str, int]:
        """
        Clean up temporary files and expired cache.
        
        Returns:
            Dictionary with cleanup results
        """
        self.logger.info("Running cleanup...")
        
        results = {
            "temp_files_deleted": self.data.cleanup_temp_files(),
            "cache_entries_cleaned": self.cache.cleanup_expired(),
        }
        
        self.logger.info(f"Cleanup completed: {results}")
        return results
    
    def __repr__(self) -> str:
        status = self.get_status()
        return f"Hub(files={status['data']['public_files']['total']}, cache={status['cache']['total_entries']})"
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
