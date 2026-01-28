"""
Cache Manager for Epstein Files Hub

Efficient caching system for reducing redundant operations.
"""

import json
import hashlib
import pickle
from pathlib import Path
from typing import Any, Optional, Callable
from datetime import datetime, timedelta
from functools import wraps


class CacheManager:
    """
    Central caching system for the entire hub.
    
    Provides intelligent caching to reduce redundant operations.
    """
    
    def __init__(self, config_manager):
        """
        Initialize the cache manager.
        
        Args:
            config_manager: ConfigManager instance
        """
        self.config = config_manager
        self.cache_dir = config_manager.get_paths()["cache"]
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache expiration times (in hours)
        self.expiration_times = {
            "public_files": 24,  # 1 day
            "wikipedia": 168,    # 1 week
            "search_index": 24,  # 1 day
            "processing": 1,     # 1 hour
            "default": 24,       # 1 day
        }
    
    def _get_cache_key(self, key: str, namespace: str = "default") -> str:
        """
        Generate a cache key.
        
        Args:
            key: Base key
            namespace: Cache namespace
            
        Returns:
            Hashed cache key
        """
        full_key = f"{namespace}:{key}"
        return hashlib.md5(full_key.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str, namespace: str = "default") -> Path:
        """
        Get the path for a cache file.
        
        Args:
            cache_key: Cache key
            namespace: Cache namespace
            
        Returns:
            Path to cache file
        """
        namespace_dir = self.cache_dir / namespace
        namespace_dir.mkdir(parents=True, exist_ok=True)
        return namespace_dir / f"{cache_key}.cache"
    
    def _is_expired(self, cache_path: Path, namespace: str = "default") -> bool:
        """
        Check if a cache file is expired.
        
        Args:
            cache_path: Path to cache file
            namespace: Cache namespace
            
        Returns:
            True if cache is expired
        """
        if not cache_path.exists():
            return True
        
        # Get modification time
        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
        
        # Get expiration time for namespace
        expiration_hours = self.expiration_times.get(namespace, self.expiration_times["default"])
        expiration_time = timedelta(hours=expiration_hours)
        
        # Check if expired
        return datetime.now() - mtime > expiration_time
    
    def get(self, key: str, namespace: str = "default", 
            default: Any = None) -> Any:
        """
        Get a value from cache.
        
        Args:
            key: Cache key
            namespace: Cache namespace
            default: Default value if not found or expired
            
        Returns:
            Cached value or default
        """
        cache_key = self._get_cache_key(key, namespace)
        cache_path = self._get_cache_path(cache_key, namespace)
        
        # Check if cache exists and is not expired
        if self._is_expired(cache_path, namespace):
            return default
        
        # Load cache
        try:
            with open(cache_path, 'rb') as f:
                cache_data = pickle.load(f)
                return cache_data.get("value", default)
        except Exception:
            return default
    
    def set(self, key: str, value: Any, namespace: str = "default",
            ttl: Optional[int] = None) -> None:
        """
        Set a value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            namespace: Cache namespace
            ttl: Time to live in hours (optional)
        """
        cache_key = self._get_cache_key(key, namespace)
        cache_path = self._get_cache_path(cache_key, namespace)
        
        # Store cache data
        cache_data = {
            "value": value,
            "cached_at": datetime.now().isoformat(),
            "namespace": namespace,
            "ttl": ttl or self.expiration_times.get(namespace, self.expiration_times["default"]),
        }
        
        # Save cache
        with open(cache_path, 'wb') as f:
            pickle.dump(cache_data, f)
    
    def delete(self, key: str, namespace: str = "default") -> bool:
        """
        Delete a cache entry.
        
        Args:
            key: Cache key
            namespace: Cache namespace
            
        Returns:
            True if deleted
        """
        cache_key = self._get_cache_key(key, namespace)
        cache_path = self._get_cache_path(cache_key, namespace)
        
        if cache_path.exists():
            cache_path.unlink()
            return True
        return False
    
    def clear(self, namespace: Optional[str] = None) -> int:
        """
        Clear cache entries.
        
        Args:
            namespace: Optional namespace to clear (clears all if None)
            
        Returns:
            Number of entries cleared
        """
        count = 0
        
        if namespace:
            namespace_dir = self.cache_dir / namespace
            if namespace_dir.exists():
                for cache_file in namespace_dir.glob("*.cache"):
                    cache_file.unlink()
                    count += 1
        else:
            for cache_file in self.cache_dir.rglob("*.cache"):
                cache_file.unlink()
                count += 1
        
        return count
    
    def cleanup_expired(self) -> int:
        """
        Clean up expired cache entries.
        
        Returns:
            Number of entries cleaned up
        """
        count = 0
        
        for cache_file in self.cache_dir.rglob("*.cache"):
            # Extract namespace from path
            namespace = cache_file.parent.name
            
            if self._is_expired(cache_file, namespace):
                cache_file.unlink()
                count += 1
        
        return count
    
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        stats = {
            "total_entries": 0,
            "total_size_bytes": 0,
            "namespaces": {},
        }
        
        for cache_file in self.cache_dir.rglob("*.cache"):
            namespace = cache_file.parent.name
            size = cache_file.stat().st_size
            
            stats["total_entries"] += 1
            stats["total_size_bytes"] += size
            
            if namespace not in stats["namespaces"]:
                stats["namespaces"][namespace] = {
                    "entries": 0,
                    "size_bytes": 0,
                }
            
            stats["namespaces"][namespace]["entries"] += 1
            stats["namespaces"][namespace]["size_bytes"] += size
        
        # Convert to human-readable sizes
        stats["total_size_mb"] = round(stats["total_size_bytes"] / (1024 * 1024), 2)
        
        for namespace in stats["namespaces"]:
            size_bytes = stats["namespaces"][namespace]["size_bytes"]
            stats["namespaces"][namespace]["size_mb"] = round(size_bytes / (1024 * 1024), 2)
        
        return stats
    
    def cached(self, namespace: str = "default", ttl: Optional[int] = None):
        """
        Decorator for caching function results.
        
        Args:
            namespace: Cache namespace
            ttl: Time to live in hours (optional)
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key from function name and arguments
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                
                # Try to get from cache
                cached_value = self.get(cache_key, namespace)
                if cached_value is not None:
                    return cached_value
                
                # Call function and cache result
                result = func(*args, **kwargs)
                self.set(cache_key, result, namespace, ttl)
                
                return result
            
            return wrapper
        return decorator
    
    def __repr__(self) -> str:
        stats = self.get_stats()
        return f"CacheManager(entries={stats['total_entries']}, size={stats['total_size_mb']}MB)"
