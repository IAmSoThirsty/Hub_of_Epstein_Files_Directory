# Migration Guide: From Scripts to Library

This guide helps you migrate from using standalone scripts to the new sovereign level monolithic dense library.

## Overview

The new library consolidates all functionality into a unified, object-oriented interface while maintaining backward compatibility with existing scripts.

## Key Changes

### Before (Scripts)
```bash
# Old approach - separate scripts
python scripts/fetch-public-files.py
python scripts/process-pdfs.py
python scripts/generate-search-index.py
```

### After (Library)
```python
# New approach - unified library
from epstein_files import Hub

hub = Hub()
hub.fetch_public_files()
hub.process_documents()
hub.generate_search_index()
```

## Migration Steps

### 1. Install the Library

```bash
# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### 2. Update Your Code

#### Fetching Public Files

**Before:**
```python
# scripts/fetch-public-files.py
import requests
# ... manual implementation
```

**After:**
```python
from epstein_files import Hub

hub = Hub()
results = hub.fetch_public_files(sources=["fbi_vault", "doj"])
print(f"Fetched {results['total_files']} files")
```

#### Processing Documents

**Before:**
```python
# scripts/process-pdfs.py
import pypdf
# ... manual implementation
```

**After:**
```python
from epstein_files import Hub

hub = Hub()
results = hub.process_documents(enable_ocr=True)
print(f"Processed {results['total_processed']} documents")
```

#### Generating Search Index

**Before:**
```python
# scripts/generate-search-index.py
import json
# ... manual implementation
```

**After:**
```python
from epstein_files import Hub

hub = Hub()
results = hub.generate_search_index()
print(f"Indexed {results['total_documents']} documents")
```

### 3. Configuration Management

#### Before (Environment Variables)
```bash
export DATA_DIR=data
export ENABLE_OCR=true
```

#### After (Unified Config)
```python
from epstein_files import Hub

hub = Hub()

# Access configuration
data_dir = hub.config.get("data_dir")

# Modify configuration
hub.config.set("enable_ocr", True)
hub.config.set("max_workers", 8)

# Get all paths
paths = hub.config.get_paths()
```

### 4. Data Management

#### Before (Manual File Handling)
```python
import json
with open("data/file.json", "r") as f:
    data = json.load(f)
```

#### After (DataManager)
```python
from epstein_files import Hub

hub = Hub()

# Load data
data = hub.data.load_json("data/file.json")

# Save data
hub.data.save_json(data, "data/output.json")

# List files
files = hub.data.list_files("data/public_files", "*.pdf")

# Get statistics
stats = hub.data.get_statistics()
```

### 5. Caching

#### Before (No Built-in Caching)
```python
# Manual cache implementation required
```

#### After (CacheManager)
```python
from epstein_files import Hub

hub = Hub()

# Cache data
hub.cache.set("key", value, namespace="processing")

# Retrieve cached data
value = hub.cache.get("key", namespace="processing")

# Cache decorator
@hub.cache.cached(namespace="wikipedia", ttl=168)
def expensive_operation():
    return result

# Get cache statistics
stats = hub.cache.get_stats()
```

### 6. Running Full Pipeline

#### Before (Multiple Scripts)
```bash
#!/bin/bash
python scripts/fetch-public-files.py
python scripts/fetch-wikipedia-data.py
python scripts/process-pdfs.py
python scripts/generate-search-index.py
```

#### After (Single Command)
```python
from epstein_files import Hub

hub = Hub()

# Run entire pipeline
results = hub.run_full_pipeline(force_refresh=False)

# Or use CLI
# epstein-hub pipeline
```

## CLI Usage

The library provides a command-line interface:

```bash
# Get system status
epstein-hub status

# Fetch public files
epstein-hub fetch

# Process documents
epstein-hub process

# Generate search index
epstein-hub index

# Run full pipeline
epstein-hub pipeline

# Cleanup
epstein-hub cleanup

# Use debug mode
epstein-hub status --debug

# Force refresh
epstein-hub fetch --force
```

## Backward Compatibility

### Scripts Still Work

All original scripts continue to work:
```bash
python scripts/fetch-public-files.py
python scripts/process-pdfs.py
python scripts/generate-search-index.py
```

### Gradual Migration

You can migrate gradually:
1. Keep using scripts for some operations
2. Use library for new functionality
3. Migrate scripts one at a time
4. Eventually deprecate old scripts

## Advanced Usage

### Direct Subsystem Access

```python
from epstein_files import Hub

hub = Hub()

# Access subsystems directly
hub.public_files.fetch_fbi_vault()
hub.wikipedia.fetch_character_data("Name")
hub.pdf_processor.process_file("doc.pdf")
hub.search_indexer.build_index()
hub.agents.run_agent("pdf_analysis", task)
```

### Context Manager

```python
from epstein_files import Hub

# Automatic cleanup
with Hub() as hub:
    hub.fetch_public_files()
    hub.process_documents()
    hub.generate_search_index()
# Cleanup happens automatically
```

### Custom Configuration

```python
from epstein_files import Hub
from pathlib import Path

# Custom config path
hub = Hub(config_path=Path(".env.custom"))

# Or modify after initialization
hub.config.set("data_dir", "custom_data")
hub.config.set("max_workers", 16)
hub.config.ensure_directories()
```

## Benefits of Migration

### 1. Unified Interface
- Single import for all functionality
- Consistent API across all operations
- Reduced code duplication

### 2. Better Performance
- Intelligent caching reduces redundant operations
- Lazy loading of subsystems
- Parallel processing support

### 3. Improved Maintainability
- Centralized configuration
- Better error handling
- Comprehensive logging

### 4. Enhanced Features
- Context manager support
- CLI interface
- Statistics and monitoring
- Automatic cleanup

### 5. Type Safety
- Type hints throughout
- Better IDE support
- Fewer runtime errors

## Common Migration Patterns

### Pattern 1: Simple Script to Library

**Before:**
```python
# my_script.py
import scripts.fetch_public_files as fetch
fetch.main()
```

**After:**
```python
# my_script.py
from epstein_files import Hub

hub = Hub()
hub.fetch_public_files()
```

### Pattern 2: Configuration

**Before:**
```python
import os
data_dir = os.getenv("DATA_DIR", "data")
```

**After:**
```python
from epstein_files import Hub

hub = Hub()
data_dir = hub.config.get("data_dir")
```

### Pattern 3: Data Operations

**Before:**
```python
import json
from pathlib import Path

data_path = Path("data/file.json")
with open(data_path, "r") as f:
    data = json.load(f)
```

**After:**
```python
from epstein_files import Hub

hub = Hub()
data = hub.data.load_json("data/file.json")
```

## Testing After Migration

```python
# test_migration.py
from epstein_files import Hub

def test_basic_operations():
    hub = Hub()
    
    # Test status
    status = hub.get_status()
    assert status['config']['valid']
    
    # Test operations
    results = hub.fetch_public_files()
    assert 'total_files' in results
    
    results = hub.process_documents()
    assert 'total_processed' in results
    
    results = hub.generate_search_index()
    assert 'total_documents' in results
```

## Troubleshooting

### Issue: Module not found

```bash
# Solution: Install the library
pip install -e .
```

### Issue: Configuration not loading

```python
# Solution: Ensure .env file exists or create config
from epstein_files import Hub

hub = Hub()
hub.config.ensure_directories()
```

### Issue: Import errors

```python
# Solution: Check PYTHONPATH
import sys
sys.path.insert(0, '/path/to/Hub_of_Epstein_Files_Directory')

from epstein_files import Hub
```

## Support

For help with migration:
- See `docs/LIBRARY_DOCUMENTATION.md` for full API reference
- Check `examples/` directory for usage examples
- Open an issue on GitHub for migration questions

## Timeline

- **Phase 1 (Current)**: Library released, scripts still supported
- **Phase 2 (Next)**: Deprecation warnings added to scripts
- **Phase 3 (Future)**: Scripts marked deprecated
- **Phase 4 (Later)**: Scripts removed (with sufficient notice)

## Summary

The new library provides:
- ✅ Unified interface for all operations
- ✅ Backward compatibility with existing scripts
- ✅ Better performance through caching
- ✅ Enhanced features (CLI, context manager, etc.)
- ✅ Comprehensive documentation and examples
- ✅ Full test coverage

Start migrating today to take advantage of these benefits!
