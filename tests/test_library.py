"""
Tests for the Epstein Files Hub Library.
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from epstein_files import Hub, ConfigManager, DataManager, CacheManager


class TestConfigManager:
    """Test ConfigManager functionality."""
    
    def test_initialization(self):
        """Test ConfigManager initialization."""
        config = ConfigManager()
        assert config is not None
        assert isinstance(config.get_all(), dict)
    
    def test_get_set(self):
        """Test get/set operations."""
        config = ConfigManager()
        config.set("test_key", "test_value")
        assert config.get("test_key") == "test_value"
    
    def test_get_paths(self):
        """Test path retrieval."""
        config = ConfigManager()
        paths = config.get_paths()
        assert "base" in paths
        assert "data" in paths
        assert "cache" in paths
        assert isinstance(paths["base"], Path)
    
    def test_validate(self):
        """Test configuration validation."""
        config = ConfigManager()
        assert config.validate() is True


class TestDataManager:
    """Test DataManager functionality."""
    
    def test_initialization(self):
        """Test DataManager initialization."""
        config = ConfigManager()
        data = DataManager(config)
        assert data is not None
    
    def test_get_statistics(self):
        """Test statistics retrieval."""
        config = ConfigManager()
        data = DataManager(config)
        stats = data.get_statistics()
        assert "public_files" in stats
        assert "processed" in stats
        assert "wikipedia" in stats


class TestCacheManager:
    """Test CacheManager functionality."""
    
    def test_initialization(self):
        """Test CacheManager initialization."""
        config = ConfigManager()
        cache = CacheManager(config)
        assert cache is not None
    
    def test_cache_operations(self):
        """Test cache get/set operations."""
        config = ConfigManager()
        cache = CacheManager(config)
        
        # Set and get
        cache.set("test_key", "test_value", "test")
        value = cache.get("test_key", "test")
        assert value == "test_value"
        
        # Delete
        deleted = cache.delete("test_key", "test")
        assert deleted is True
        
        # Get after delete
        value = cache.get("test_key", "test")
        assert value is None
    
    def test_cache_stats(self):
        """Test cache statistics."""
        config = ConfigManager()
        cache = CacheManager(config)
        
        cache.set("test1", "value1", "test")
        cache.set("test2", "value2", "test")
        
        stats = cache.get_stats()
        assert "total_entries" in stats
        assert stats["total_entries"] >= 2


class TestHub:
    """Test Hub functionality."""
    
    def test_initialization(self):
        """Test Hub initialization."""
        hub = Hub()
        assert hub is not None
        assert hub.config is not None
        assert hub.data is not None
        assert hub.cache is not None
    
    def test_get_status(self):
        """Test status retrieval."""
        hub = Hub()
        status = hub.get_status()
        assert "config" in status
        assert "data" in status
        assert "cache" in status
    
    def test_context_manager(self):
        """Test Hub as context manager."""
        with Hub() as hub:
            assert hub is not None
            status = hub.get_status()
            assert status is not None
    
    def test_lazy_loading(self):
        """Test lazy loading of subsystems."""
        hub = Hub()
        
        # Access subsystems
        assert hub.public_files is not None
        assert hub.wikipedia is not None
        assert hub.pdf_processor is not None
        assert hub.search_indexer is not None
        assert hub.agents is not None
    
    def test_fetch_public_files(self):
        """Test public files fetching."""
        hub = Hub()
        results = hub.fetch_public_files(sources=["fbi_vault"])
        assert "total_files" in results
        assert "sources" in results
    
    def test_process_documents(self):
        """Test document processing."""
        hub = Hub()
        results = hub.process_documents()
        assert "total_processed" in results
        assert "total_failed" in results
    
    def test_generate_search_index(self):
        """Test search index generation."""
        hub = Hub()
        results = hub.generate_search_index()
        assert "total_documents" in results
    
    def test_cleanup(self):
        """Test cleanup operations."""
        hub = Hub()
        results = hub.cleanup()
        assert "temp_files_deleted" in results
        assert "cache_entries_cleaned" in results


class TestIntegration:
    """Integration tests."""
    
    def test_full_pipeline(self):
        """Test full pipeline execution."""
        hub = Hub()
        results = hub.run_full_pipeline(force_refresh=False)
        assert "started_at" in results
        assert "completed_at" in results
        assert "steps" in results
        assert len(results["steps"]) > 0
    
    def test_subsystem_coordination(self):
        """Test coordination between subsystems."""
        hub = Hub()
        
        # Test config -> data coordination
        paths = hub.config.get_paths()
        stats = hub.data.get_statistics()
        assert paths is not None
        assert stats is not None
        
        # Test cache coordination
        cache_stats = hub.cache.get_stats()
        assert cache_stats is not None


def test_library_imports():
    """Test that all library components can be imported."""
    from epstein_files import Hub
    from epstein_files import ConfigManager
    from epstein_files import DataManager
    from epstein_files import CacheManager
    
    assert Hub is not None
    assert ConfigManager is not None
    assert DataManager is not None
    assert CacheManager is not None


def test_version():
    """Test version information."""
    import epstein_files
    assert hasattr(epstein_files, '__version__')
    assert epstein_files.__version__ == "1.0.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
