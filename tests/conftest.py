"""
Pytest configuration and shared fixtures for all tests.
"""

import os
import tempfile
from pathlib import Path
from collections.abc import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_data_dir(temp_dir: Path) -> Path:
    """Create a mock data directory structure."""
    data_dir = temp_dir / "data"
    data_dir.mkdir()
    
    # Create subdirectories
    (data_dir / "public_files").mkdir()
    (data_dir / "processed").mkdir()
    (data_dir / "wikipedia").mkdir()
    
    return data_dir


@pytest.fixture
def mock_env_vars(monkeypatch) -> dict:
    """Set up mock environment variables for testing."""
    env_vars = {
        "DATA_DIR": "/tmp/test_data",
        "LOG_LEVEL": "INFO",
        "CACHE_DIR": "/tmp/test_cache",
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    return env_vars


@pytest.fixture
def sample_pdf_path(temp_dir: Path) -> Path:
    """Create a sample PDF file path (without actual PDF content)."""
    pdf_path = temp_dir / "sample.pdf"
    pdf_path.touch()
    return pdf_path


@pytest.fixture
def sample_json_data() -> dict:
    """Provide sample JSON data for testing."""
    return {
        "documents": [
            {
                "id": "doc1",
                "title": "Test Document 1",
                "date": "2020-01-01",
                "type": "legal_document"
            },
            {
                "id": "doc2",
                "title": "Test Document 2",
                "date": "2020-01-02",
                "type": "court_filing"
            }
        ]
    }
