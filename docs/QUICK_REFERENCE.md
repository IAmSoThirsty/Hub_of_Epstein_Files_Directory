# Quick Reference: Epstein Files Hub Library

## Installation

```bash
pip install -e .
```

## Basic Usage

```python
from epstein_files import Hub

# Initialize
hub = Hub()

# Fetch data
hub.fetch_public_files()
hub.fetch_wikipedia_data()

# Process
hub.process_documents()

# Index
hub.generate_search_index()

# Full pipeline
hub.run_full_pipeline()

# Status
status = hub.get_status()
```

## CLI Commands

```bash
epstein-hub status      # System status
epstein-hub fetch       # Fetch public files
epstein-hub process     # Process documents
epstein-hub index       # Generate index
epstein-hub pipeline    # Run full pipeline
epstein-hub cleanup     # Cleanup temp files

# Options
--force                 # Force refresh/rebuild
--debug                 # Enable debug mode
```

## FastAPI Backend Quick Ops

```bash
# Run API locally
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# API docs
# http://localhost:8000/api/docs

# Targeted API tests
python -m pytest tests/unit/test_api_endpoints.py tests/integration/test_api_routes.py -v
```

### Key Environment Variables

- `ADMIN_API_TOKEN` / `ADMIN_API_TOKENS`: admin auth tokens for upload endpoints
- `AUTH_RATE_LIMIT_MAX_ATTEMPTS`: failed-auth limit per client window
- `AUTH_RATE_LIMIT_WINDOW_SECONDS`: failed-auth rolling window in seconds
- `UPLOAD_DIR`: location for uploaded PDFs
- `JOB_STORE_PATH`: persistent upload-job state file (survives restarts)
- `CORS_ALLOW_ORIGINS`: comma-separated allowed origins

## Context Manager

```python
with Hub() as hub:
    hub.fetch_public_files()
    hub.process_documents()
# Automatic cleanup
```

## Configuration

```python
hub.config.get("data_dir")
hub.config.set("debug_mode", True)
hub.config.get_paths()
```

## Data Operations

```python
# Save/load files
hub.data.save_file(content, path)
hub.data.load_file(path)

# JSON operations
hub.data.save_json(data, path)
hub.data.load_json(path)

# List files
hub.data.list_files(dir, "*.pdf")

# Statistics
stats = hub.data.get_statistics()
```

## Cache Operations

```python
# Basic cache
hub.cache.set("key", value, "namespace")
value = hub.cache.get("key", "namespace")

# Decorator
@hub.cache.cached(namespace="data", ttl=24)
def expensive_function():
    return result

# Stats
stats = hub.cache.get_stats()
```

## Subsystem Access

```python
# Public files
hub.public_files.fetch_fbi_vault()

# Wikipedia
hub.wikipedia.fetch_character_data("Name")

# PDF processing
hub.pdf_processor.process_file("file.pdf")

# Search
hub.search_indexer.build_index()

# Agents
hub.agents.run_agent("agent_name", task)
hub.agents.get_status()
```

## Examples

See `examples/` directory:
- `basic_usage.py` - Basic operations
- `advanced_usage.py` - Advanced features
- `context_manager.py` - Context manager usage

## Documentation

- [Library Documentation](docs/LIBRARY_DOCUMENTATION.md)
- [Migration Guide](docs/MIGRATION_GUIDE.md)
- [Main README](README.md)

## Testing

```bash
pytest tests/test_library.py -v
```

## Common Patterns

### Fetch and Process

```python
hub = Hub()
hub.fetch_public_files()
hub.process_documents()
```

### Full Pipeline

```python
hub = Hub()
results = hub.run_full_pipeline(force_refresh=True)
```

### Custom Configuration

```python
hub = Hub()
hub.config.set("max_workers", 8)
hub.config.set("enable_ocr", True)
```

### Statistics

```python
hub = Hub()
status = hub.get_status()
data_stats = hub.data.get_statistics()
cache_stats = hub.cache.get_stats()
```
