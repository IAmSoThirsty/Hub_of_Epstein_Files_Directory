"""
Data Manager for Epstein Files Hub

Central authority for all data operations, storage, and retrieval.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime


class DataManager:
    """
    Central data management for the entire hub.
    
    This is the sovereign authority for all data operations.
    """
    
    def __init__(self, config_manager):
        """
        Initialize the data manager.
        
        Args:
            config_manager: ConfigManager instance
        """
        self.config = config_manager
        self.paths = config_manager.get_paths()
        self._ensure_data_structure()
    
    def _ensure_data_structure(self) -> None:
        """Create the full data directory structure."""
        data_dirs = [
            self.paths["data"] / "public_files",
            self.paths["data"] / "public_files" / "fbi_vault",
            self.paths["data"] / "public_files" / "doj",
            self.paths["data"] / "public_files" / "metadata",
            self.paths["data"] / "processed",
            self.paths["data"] / "processed" / "text",
            self.paths["data"] / "processed" / "metadata",
            self.paths["data"] / "processed" / "indexed",
            self.paths["data"] / "wikipedia",
            self.paths["data"] / "wikipedia" / "characters",
            self.paths["data"] / "wikipedia" / "locations",
            self.paths["data"] / "wikipedia" / "events",
            self.paths["data"] / "search_index",
            self.paths["data"] / "agents",
        ]
        
        for directory in data_dirs:
            directory.mkdir(parents=True, exist_ok=True)
    
    def save_file(self, content: Union[str, bytes], filepath: Path, 
                  metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Save a file with metadata.
        
        Args:
            content: File content (string or bytes)
            filepath: Path to save file
            metadata: Optional metadata dictionary
            
        Returns:
            Dictionary with save information
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Save content
        mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(filepath, mode) as f:
            f.write(content)
        
        # Calculate hash
        if isinstance(content, str):
            content = content.encode('utf-8')
        file_hash = hashlib.sha256(content).hexdigest()
        
        # Create file info
        file_info = {
            "filepath": str(filepath),
            "size": len(content),
            "hash": file_hash,
            "saved_at": datetime.utcnow().isoformat(),
        }
        
        # Add metadata if provided
        if metadata:
            file_info["metadata"] = metadata
        
        # Save metadata file
        metadata_path = filepath.parent / f"{filepath.stem}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(file_info, f, indent=2)
        
        return file_info
    
    def load_file(self, filepath: Path, binary: bool = False) -> Union[str, bytes]:
        """
        Load a file.
        
        Args:
            filepath: Path to file
            binary: Whether to load as binary
            
        Returns:
            File content
        """
        filepath = Path(filepath)
        mode = 'rb' if binary else 'r'
        with open(filepath, mode) as f:
            return f.read()
    
    def get_file_metadata(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a file.
        
        Args:
            filepath: Path to file
            
        Returns:
            Metadata dictionary or None
        """
        filepath = Path(filepath)
        metadata_path = filepath.parent / f"{filepath.stem}_metadata.json"
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                return json.load(f)
        return None
    
    def list_files(self, directory: Path, pattern: str = "*",
                   recursive: bool = True) -> List[Path]:
        """
        List files in a directory.
        
        Args:
            directory: Directory to search
            pattern: File pattern (e.g., "*.pdf")
            recursive: Whether to search recursively
            
        Returns:
            List of file paths
        """
        directory = Path(directory)
        if recursive:
            return list(directory.rglob(pattern))
        else:
            return list(directory.glob(pattern))
    
    def get_public_files(self, source: Optional[str] = None) -> List[Path]:
        """
        Get all public files, optionally filtered by source.
        
        Args:
            source: Optional source filter (e.g., "fbi_vault", "doj")
            
        Returns:
            List of file paths
        """
        base_path = self.paths["data"] / "public_files"
        
        if source:
            return self.list_files(base_path / source, "*.pdf")
        else:
            return self.list_files(base_path, "*.pdf")
    
    def get_processed_files(self, file_type: str = "text") -> List[Path]:
        """
        Get all processed files of a specific type.
        
        Args:
            file_type: Type of processed files ("text", "metadata", "indexed")
            
        Returns:
            List of file paths
        """
        base_path = self.paths["data"] / "processed" / file_type
        return self.list_files(base_path, "*.*")
    
    def save_json(self, data: Any, filepath: Path) -> None:
        """
        Save data as JSON.
        
        Args:
            data: Data to save
            filepath: Path to save file
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_json(self, filepath: Path) -> Any:
        """
        Load JSON data.
        
        Args:
            filepath: Path to file
            
        Returns:
            Loaded data
        """
        filepath = Path(filepath)
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def get_manifest(self, manifest_name: str = "download_manifest.json") -> Dict[str, Any]:
        """
        Get a manifest file.
        
        Args:
            manifest_name: Name of manifest file
            
        Returns:
            Manifest dictionary
        """
        manifest_path = self.paths["data"] / "public_files" / manifest_name
        
        if manifest_path.exists():
            return self.load_json(manifest_path)
        return {"files": [], "last_updated": None}
    
    def update_manifest(self, manifest_data: Dict[str, Any],
                       manifest_name: str = "download_manifest.json") -> None:
        """
        Update a manifest file.
        
        Args:
            manifest_data: Manifest data
            manifest_name: Name of manifest file
        """
        manifest_path = self.paths["data"] / "public_files" / manifest_name
        manifest_data["last_updated"] = datetime.utcnow().isoformat()
        self.save_json(manifest_data, manifest_path)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the data.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            "public_files": {
                "fbi_vault": len(self.get_public_files("fbi_vault")),
                "doj": len(self.get_public_files("doj")),
                "total": len(self.get_public_files()),
            },
            "processed": {
                "text": len(self.get_processed_files("text")),
                "metadata": len(self.get_processed_files("metadata")),
                "indexed": len(self.get_processed_files("indexed")),
            },
            "wikipedia": {
                "characters": len(self.list_files(self.paths["data"] / "wikipedia" / "characters")),
                "locations": len(self.list_files(self.paths["data"] / "wikipedia" / "locations")),
                "events": len(self.list_files(self.paths["data"] / "wikipedia" / "events")),
            }
        }
        
        return stats
    
    def cleanup_temp_files(self) -> int:
        """
        Clean up temporary files.
        
        Returns:
            Number of files deleted
        """
        temp_dir = self.paths["tmp"]
        if not temp_dir.exists():
            return 0
        
        count = 0
        for file in temp_dir.rglob("*"):
            if file.is_file():
                file.unlink()
                count += 1
        
        return count
    
    def __repr__(self) -> str:
        stats = self.get_statistics()
        return f"DataManager(public_files={stats['public_files']['total']}, processed={stats['processed']['text']})"
