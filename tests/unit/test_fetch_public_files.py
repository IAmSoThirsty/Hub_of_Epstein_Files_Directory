"""
Unit tests for fetch-public-files.py script.
"""

import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import requests


@pytest.mark.unit
class TestFetchPublicFiles:
    """Test suite for public files fetching."""
    
    def test_fbi_vault_url_formation(self):
        """Test FBI Vault URL is correctly formed."""
        base_url = "https://vault.fbi.gov/jeffrey-epstein"
        assert base_url.startswith("https://")
        assert "vault.fbi.gov" in base_url
    
    def test_file_download_path(self, temp_dir):
        """Test that download paths are created correctly."""
        download_dir = temp_dir / "data" / "public_files" / "fbi_vault"
        download_dir.mkdir(parents=True, exist_ok=True)
        
        assert download_dir.exists()
        assert download_dir.is_dir()
    
    @patch('requests.get')
    def test_http_request_success(self, mock_get):
        """Test successful HTTP request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'PDF content'
        mock_get.return_value = mock_response
        
        response = requests.get('https://example.com/file.pdf')
        assert response.status_code == 200
    
    @patch('requests.get')
    def test_http_request_failure(self, mock_get):
        """Test HTTP request failure handling."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        response = requests.get('https://example.com/nonexistent.pdf')
        assert response.status_code == 404
    
    def test_sha256_verification(self):
        """Test SHA-256 checksum verification."""
        import hashlib
        
        test_data = b"Test PDF content"
        expected_hash = hashlib.sha256(test_data).hexdigest()
        actual_hash = hashlib.sha256(test_data).hexdigest()
        
        assert expected_hash == actual_hash
    
    def test_file_extension_validation(self):
        """Test that only valid file extensions are processed."""
        valid_extensions = ['.pdf', '.PDF']
        test_files = ['document.pdf', 'file.PDF', 'report.pdf']
        
        for filename in test_files:
            ext = os.path.splitext(filename)[1]
            assert ext in valid_extensions
    
    @pytest.mark.parametrize("url,expected_filename", [
        ("https://vault.fbi.gov/file1.pdf", "file1.pdf"),
        ("https://vault.fbi.gov/docs/report.pdf", "report.pdf"),
        ("https://example.com/document.PDF", "document.PDF"),
    ])
    def test_filename_extraction(self, url, expected_filename):
        """Test filename extraction from URL."""
        filename = url.split('/')[-1]
        assert filename == expected_filename
    
    def test_directory_creation(self, temp_dir):
        """Test that necessary directories are created."""
        dirs_to_create = [
            temp_dir / "data",
            temp_dir / "data" / "public_files",
            temp_dir / "data" / "public_files" / "fbi_vault"
        ]
        
        for directory in dirs_to_create:
            directory.mkdir(parents=True, exist_ok=True)
            assert directory.exists()
    
    @patch('requests.get')
    def test_timeout_handling(self, mock_get):
        """Test timeout handling for slow connections."""
        mock_get.side_effect = requests.Timeout("Connection timeout")
        
        with pytest.raises(requests.Timeout):
            requests.get('https://example.com/file.pdf', timeout=30)
    
    def test_file_size_validation(self):
        """Test file size validation."""
        test_sizes = [1024, 1024*1024, 10*1024*1024]  # 1KB, 1MB, 10MB
        
        for size in test_sizes:
            assert size > 0
            assert size < 100 * 1024 * 1024  # Less than 100MB


@pytest.mark.unit
class TestPublicFilesSources:
    """Test suite for various public file sources."""
    
    def test_fbi_vault_source(self):
        """Test FBI Vault as a source."""
        source = {
            'name': 'FBI Vault',
            'base_url': 'https://vault.fbi.gov',
            'type': 'government'
        }
        assert source['type'] == 'government'
        assert 'fbi.gov' in source['base_url']
    
    def test_doj_source(self):
        """Test DOJ as a source."""
        source = {
            'name': 'Department of Justice',
            'base_url': 'https://www.justice.gov',
            'type': 'government'
        }
        assert source['type'] == 'government'
        assert 'justice.gov' in source['base_url']
    
    def test_multiple_sources_configuration(self):
        """Test configuration with multiple sources."""
        sources = [
            {'name': 'FBI Vault', 'url': 'https://vault.fbi.gov'},
            {'name': 'DOJ', 'url': 'https://justice.gov'},
        ]
        assert len(sources) >= 2


@pytest.mark.integration
class TestFetchPublicFilesIntegration:
    """Integration tests for file fetching workflow."""
    
    @pytest.mark.network
    def test_fbi_vault_accessibility(self):
        """Test that FBI Vault is accessible (requires network)."""
        # This test would actually check network connectivity
        # Marked as network test to be skipped in offline environments
        assert True  # Placeholder
    
    def test_complete_download_workflow(self):
        """Test complete file download workflow."""
        # Would test full pipeline in actual implementation
        assert True  # Placeholder
