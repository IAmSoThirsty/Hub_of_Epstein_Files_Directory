"""
Configuration Manager for Epstein Files Hub

Handles all configuration loading, validation, and management
across the entire system.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """
    Central configuration management for the entire hub.
    
    This is the sovereign authority for all configuration across the system.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config_path = config_path or self._get_default_config_path()
        self._config: Dict[str, Any] = {}
        self._load_config()
        
    def _get_default_config_path(self) -> Path:
        """Get the default configuration path."""
        return Path(__file__).parent.parent.parent / ".env"
    
    def _load_config(self) -> None:
        """Load configuration from environment and config files."""
        # Load from environment variables
        self._config = {
            "data_dir": os.getenv("DATA_DIR", "data"),
            "cache_dir": os.getenv("CACHE_DIR", "cache"),
            "logs_dir": os.getenv("LOGS_DIR", "logs"),
            "web_dir": os.getenv("WEB_DIR", "web"),
            "scripts_dir": os.getenv("SCRIPTS_DIR", "scripts"),
            "bots_dir": os.getenv("BOTS_DIR", "bots"),
            "docs_dir": os.getenv("DOCS_DIR", "docs"),
            "tmp_dir": os.getenv("TMP_DIR", "tmp"),
            
            # Data source URLs
            "fbi_vault_url": "https://vault.fbi.gov/jeffrey-epstein",
            "internet_archive_url": "https://archive.org/search.php?query=epstein",
            "document_cloud_url": "https://www.documentcloud.org/search/epstein",
            
            # Processing settings
            "enable_ocr": os.getenv("ENABLE_OCR", "true").lower() == "true",
            "max_file_size": int(os.getenv("MAX_FILE_SIZE", "104857600")),  # 100MB
            "parallel_processing": os.getenv("PARALLEL_PROCESSING", "true").lower() == "true",
            "max_workers": int(os.getenv("MAX_WORKERS", "4")),
            
            # Search settings
            "search_index_path": "web/js/search-index.js",
            "search_stats_path": "web/js/search-stats.json",
            "max_search_results": int(os.getenv("MAX_SEARCH_RESULTS", "1000")),
            
            # Agent settings
            "agent_monitoring_enabled": os.getenv("AGENT_MONITORING", "true").lower() == "true",
            "agent_count": 26,
            
            # System settings
            "debug_mode": os.getenv("DEBUG", "false").lower() == "true",
            "verbose_logging": os.getenv("VERBOSE", "false").lower() == "true",
        }
        
        # Load from .env file if it exists
        if self.config_path.exists():
            self._load_env_file()
    
    def _load_env_file(self) -> None:
        """Load configuration from .env file."""
        try:
            with open(self.config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        
                        # Convert to appropriate type
                        if value.lower() in ('true', 'false'):
                            value = value.lower() == 'true'
                        elif value.isdigit():
                            value = int(value)
                        
                        # Update config with snake_case key
                        config_key = key.lower()
                        self._config[config_key] = value
        except Exception as e:
            # Config file errors are non-fatal
            pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return self._config.copy()
    
    def get_paths(self) -> Dict[str, Path]:
        """
        Get all directory paths as Path objects.
        
        Returns:
            Dictionary of path names to Path objects
        """
        base_dir = Path(__file__).parent.parent.parent
        return {
            "base": base_dir,
            "data": base_dir / self._config["data_dir"],
            "cache": base_dir / self._config["cache_dir"],
            "logs": base_dir / self._config["logs_dir"],
            "web": base_dir / self._config["web_dir"],
            "scripts": base_dir / self._config["scripts_dir"],
            "bots": base_dir / self._config["bots_dir"],
            "docs": base_dir / self._config["docs_dir"],
            "tmp": base_dir / self._config["tmp_dir"],
        }
    
    def ensure_directories(self) -> None:
        """Create all required directories if they don't exist."""
        paths = self.get_paths()
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True)
    
    def validate(self) -> bool:
        """
        Validate configuration.
        
        Returns:
            True if configuration is valid
        """
        required_keys = ["data_dir", "cache_dir", "logs_dir"]
        return all(key in self._config for key in required_keys)
    
    def to_json(self) -> str:
        """Export configuration as JSON."""
        return json.dumps(self._config, indent=2)
    
    def __repr__(self) -> str:
        return f"ConfigManager(config_path={self.config_path})"
