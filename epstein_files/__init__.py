"""
Epstein Files Hub - Sovereign Level Monolithic Dense Library

A comprehensive, centralized library for managing, processing, and searching
Epstein-related files and documentation.

This monolithic architecture provides:
- Unified API for all operations
- Centralized data management
- Integrated search and indexing
- Document processing pipelines
- AI agent coordination
- Full system control

Usage:
    from epstein_files import Hub
    
    hub = Hub()
    hub.fetch_public_files()
    hub.process_documents()
    hub.generate_search_index()
"""

__version__ = "1.0.0"
__author__ = "IAmSoThirsty"
__license__ = "MIT"

from .core.hub import Hub
from .core.config_manager import ConfigManager
from .core.data_manager import DataManager
from .core.cache_manager import CacheManager

__all__ = [
    "Hub",
    "ConfigManager",
    "DataManager",
    "CacheManager",
]
