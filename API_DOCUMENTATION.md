<!-- markdownlint-disable MD022 MD024 MD031 MD032 MD060 -->

# API Documentation

## Overview

The Epstein Files Hub provides a comprehensive API for accessing documents, searching content, and managing data. This API follows REST principles with a focus on simplicity, consistency, and security.

## Base URL

```text
Static Site (GitHub Pages): https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/
Backend API (self-hosted): https://<your-api-host>/
Local Development API: http://localhost:8000/
```

### FastAPI Docs Endpoints

When running the backend locally or in a hosted environment:

```text
OpenAPI JSON: /api/openapi.json
Swagger UI: /api/docs
ReDoc: /api/redoc
```

## API Version

Current Version: **v1.0.0**

## Authentication

Authentication is required for write/admin routes.

### Public Endpoints (No Auth Required)

- `GET /api/health`
- `POST /api/v1/search`

### Admin Endpoints (Auth Required)

- `POST /api/v1/upload`
- `GET /api/v1/upload/{job_id}`

### Session Bootstrap Endpoints

- `POST /api/v1/auth/session` (accepts admin token in request body and
  issues secure HTTP-only cookie)
- `DELETE /api/v1/auth/session` (clears session cookie)

### Accepted Auth Headers

- `Authorization: Bearer <token>`
- `X-Admin-Token: <token>`

### Accepted Admin Session Cookie

- `epstein_admin_session` (name is configurable via
  `ADMIN_SESSION_COOKIE_NAME`)

Tokens are loaded from runtime configuration:

- `ADMIN_API_TOKENS` (comma-separated list)
- `ADMIN_API_TOKEN` (single token, also accepted)

## Rate Limiting

Authentication failures are rate-limited per client identifier (prefers
`X-Forwarded-For`, falls back to client host):

- `AUTH_RATE_LIMIT_MAX_ATTEMPTS` (default: `10`)
- `AUTH_RATE_LIMIT_WINDOW_SECONDS` (default: `60`)
- `AUTH_RATE_LIMIT_BACKEND` (`memory` or `redis`)
- `AUTH_RATE_LIMIT_REDIS_URL` (required when backend is `redis`)
- `AUTH_RATE_LIMIT_REDIS_PREFIX` (redis key namespace)

After threshold is exceeded, auth-protected endpoints return `429 Too Many Requests`.

## Backend Runtime Runbook (FastAPI)

### Environment Variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `ENVIRONMENT` | `development` | Runtime mode; production/staging rejects default dev token |
| `ADMIN_API_TOKEN` | `change-me-dev-token` | Single admin token |
| `ADMIN_API_TOKENS` | `""` | Comma-separated admin token list |
| `ADMIN_SESSION_SECRET` | `change-me-dev-session-secret` | Signing key for session cookie tokens |
| `ADMIN_SESSION_TTL_SECONDS` | `3600` | Session cookie TTL in seconds |
| `ADMIN_SESSION_COOKIE_NAME` | `epstein_admin_session` | Session cookie key |
| `ADMIN_SESSION_COOKIE_SECURE` | `false` (dev) | Set `true` on HTTPS deployments |
| `AUTH_RATE_LIMIT_MAX_ATTEMPTS` | `10` | Max failed auth attempts per window |
| `AUTH_RATE_LIMIT_WINDOW_SECONDS` | `60` | Rate-limit rolling window in seconds |
| `AUTH_RATE_LIMIT_BACKEND` | `memory` | Auth throttling store backend (`memory`/`redis`) |
| `AUTH_RATE_LIMIT_REDIS_URL` | `""` | Redis connection URL for distributed throttling |
| `AUTH_RATE_LIMIT_REDIS_PREFIX` | `epstein_auth_rl` | Redis key prefix for auth throttling entries |
| `DATA_DIR` | `./data` | Root runtime data directory |
| `UPLOAD_DIR` | `./data/uploads` | Upload destination directory |
| `ENABLE_UPLOAD_QUARANTINE` | `true` | Save suspicious uploads for manual review |
| `UPLOAD_QUARANTINE_DIR` | `./data/uploads/quarantine` | Quarantine storage path |
| `ENABLE_MALWARE_SCAN` | `false` | Enable scanner command execution on saved uploads |
| `MALWARE_SCAN_COMMAND` | `""` | Scanner command template (supports `{file}` placeholder) |
| `MALWARE_SCAN_TIMEOUT_SECONDS` | `30` | Malware scanner command timeout |
| `MALWARE_SCAN_FAIL_CLOSED` | `false` | Reject uploads when scanner errors/timeouts |
| `MALWARE_SCAN_INFECTED_EXIT_CODES` | `1` | Comma-separated exit codes treated as detected malware |
| `JOB_STORE_PATH` | `./data/uploads/jobs.json` | Persistent upload-job state store |
| `CORS_ALLOW_ORIGINS` | `*` | Comma-separated CORS allowlist |

### Start Commands

```bash
# Local API server
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Targeted endpoint tests
python -m pytest tests/unit/test_api_endpoints.py tests/integration/test_api_routes.py -v
```

### Operational Notes

- `X-Request-ID` is accepted from clients and always returned in response headers.
- Validation errors are normalized to include `requestId` and `errors` details.
- Upload jobs persist to disk and survive backend restarts via `JOB_STORE_PATH`.
- Upload intake validates extension + MIME + PDF signature + parser structure.
- Suspicious upload attempts can be quarantined for review when enabled.
- Optional malware scanning runs after upload save and before job queueing.
- Detected malware is quarantined and rejected; scanner errors can be fail-open
  or fail-closed via `MALWARE_SCAN_FAIL_CLOSED`.

## Response Format

All API responses follow this structure:

```json
{
  "status": "success" | "error",
  "data": { ... },
  "meta": {
    "timestamp": "2026-02-01T17:00:00Z",
    "version": "1.0.0",
    "pagination": {
      "page": 1,
      "perPage": 50,
      "total": 1000,
      "totalPages": 20
    }
  },
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { ... }
  }
}
```

## Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Temporary service issue |

## Python Library API

### Installation

```bash
pip install -e .
```

### Core Hub API

#### Initialize Hub

```python
from epstein_files import Hub

# Basic initialization
hub = Hub()

# With custom configuration
hub = Hub(config={
    'data_dir': '/path/to/data',
    'cache_enabled': True,
    'log_level': 'INFO'
})

# Using context manager (recommended)
with Hub() as hub:
    # Automatic cleanup on exit
    hub.run_full_pipeline()
```

#### Hub Methods

##### `get_status()`
Get current system status.

```python
status = hub.get_status()
print(status)
# {
#     'documents': 30000,
#     'images': 20000,
#     'agents': 27,
#     'health': 'operational'
# }
```

##### `fetch_public_files(source=None, force=False)`
Fetch public files from configured sources.

```python
# Fetch from all sources
hub.fetch_public_files()

# Fetch from specific source
hub.fetch_public_files(source='fbi_vault')

# Force re-fetch (ignore cache)
hub.fetch_public_files(force=True)
```

**Parameters:**
- `source` (str, optional): Specific source to fetch from
- `force` (bool): Force re-fetch ignoring cache

**Returns:** Dict with fetch results

##### `process_documents(path=None, parallel=True)`
Process documents (PDF extraction, OCR, metadata).

```python
# Process all documents
hub.process_documents()

# Process specific path
hub.process_documents(path='/path/to/docs')

# Disable parallel processing
hub.process_documents(parallel=False)
```

**Parameters:**
- `path` (str, optional): Path to documents
- `parallel` (bool): Enable parallel processing

**Returns:** Dict with processing results

##### `generate_search_index(incremental=True)`
Generate or update search index.

```python
# Incremental update
hub.generate_search_index()

# Full rebuild
hub.generate_search_index(incremental=False)
```

**Parameters:**
- `incremental` (bool): Update only changed documents

**Returns:** Dict with index statistics

##### `run_full_pipeline()`
Execute complete data pipeline.

```python
results = hub.run_full_pipeline()
print(f"Processed {results['documents_processed']} documents")
```

**Returns:** Dict with pipeline results

##### `search(query, filters=None, limit=50)`
Search documents.

```python
# Basic search
results = hub.search("flight logs")

# With filters
results = hub.search(
    query="epstein",
    filters={
        'date_range': ('2000-01-01', '2020-12-31'),
        'location': 'New York',
        'document_type': 'court_filing'
    },
    limit=100
)
```

**Parameters:**
- `query` (str): Search query
- `filters` (dict, optional): Search filters
- `limit` (int): Maximum results

**Returns:** List of search results

##### `get_document(doc_id)`
Get specific document by ID.

```python
doc = hub.get_document('doc_12345')
print(doc['title'])
print(doc['content'])
```

**Parameters:**
- `doc_id` (str): Document identifier

**Returns:** Document dict or None

##### `get_character(name)`
Get character profile.

```python
character = hub.get_character('Jeffrey Epstein')
print(character['biography'])
print(character['connections'])
```

**Parameters:**
- `name` (str): Character name

**Returns:** Character dict or None

##### `get_timeline(start_date=None, end_date=None)`
Get timeline events.

```python
# All events
timeline = hub.get_timeline()

# Date range
timeline = hub.get_timeline(
    start_date='2000-01-01',
    end_date='2020-12-31'
)
```

**Parameters:**
- `start_date` (str, optional): Start date (ISO format)
- `end_date` (str, optional): End date (ISO format)

**Returns:** List of timeline events

### Data Management API

```python
from epstein_files.data import PublicFilesManager, WikipediaIntegration

# Public files
public_files = PublicFilesManager()
files = public_files.fetch_fbi_vault()
files = public_files.fetch_doj_releases()

# Wikipedia integration
wiki = WikipediaIntegration()
data = wiki.fetch_character_data('Ghislaine Maxwell')
timeline = wiki.fetch_timeline_events()
```

### Processing API

```python
from epstein_files.processing import PDFProcessor

processor = PDFProcessor()

# Extract text
text = processor.extract_text('document.pdf')

# With OCR
text = processor.extract_text('scanned.pdf', ocr=True)

# Extract metadata
metadata = processor.extract_metadata('document.pdf')

# Extract images
images = processor.extract_images('document.pdf')
```

### Search API

```python
from epstein_files.search import SearchIndexer

indexer = SearchIndexer()

# Build index
indexer.build_index(documents)

# Search
results = indexer.search(
    query='flight logs',
    filters={'year': 2005},
    limit=50
)

# Get index stats
stats = indexer.get_stats()
```

### Agent API

```python
from epstein_files.agents import AgentManager

manager = AgentManager()

# Get agent status
status = manager.get_agent_status('document-processor')

# Run specific agent
result = manager.run_agent('pdf-analyzer', document_id='doc_123')

# Get all agents
agents = manager.list_agents()
```

## CLI API

### Installation

```bash
pip install -e .
```

### Commands

#### `epstein-hub status`
Get system status.

```bash
$ epstein-hub status

Epstein Files Hub - System Status
==================================
Documents: 30,000
Images: 20,000
Search Index: 50 MB
Agents: 27 (all operational)
Health: OPERATIONAL
```

#### `epstein-hub fetch`
Fetch public files.

```bash
# Fetch all sources
$ epstein-hub fetch

# Specific source
$ epstein-hub fetch --source fbi_vault

# Force refresh
$ epstein-hub fetch --force
```

**Options:**
- `--source TEXT`: Specific source to fetch
- `--force`: Force re-fetch
- `--verbose`: Verbose output

#### `epstein-hub process`
Process documents.

```bash
# Process all
$ epstein-hub process

# Specific path
$ epstein-hub process --path /data/documents

# Single-threaded
$ epstein-hub process --no-parallel
```

**Options:**
- `--path TEXT`: Path to documents
- `--no-parallel`: Disable parallel processing
- `--verbose`: Verbose output

#### `epstein-hub index`
Generate search index.

```bash
# Incremental update
$ epstein-hub index

# Full rebuild
$ epstein-hub index --full

# With statistics
$ epstein-hub index --stats
```

**Options:**
- `--full`: Full rebuild
- `--stats`: Show statistics
- `--verbose`: Verbose output

#### `epstein-hub search`
Search documents.

```bash
# Basic search
$ epstein-hub search "flight logs"

# With filters
$ epstein-hub search "epstein" \
    --date-start 2000-01-01 \
    --date-end 2020-12-31 \
    --limit 100

# JSON output
$ epstein-hub search "island" --json
```

**Options:**
- `--date-start DATE`: Start date filter
- `--date-end DATE`: End date filter
- `--location TEXT`: Location filter
- `--type TEXT`: Document type filter
- `--limit INT`: Result limit
- `--json`: JSON output
- `--verbose`: Verbose output

#### `epstein-hub pipeline`
Run full pipeline.

```bash
# Full pipeline
$ epstein-hub pipeline

# Skip certain steps
$ epstein-hub pipeline --skip-fetch --skip-process

# Dry run
$ epstein-hub pipeline --dry-run
```

**Options:**
- `--skip-fetch`: Skip fetching
- `--skip-process`: Skip processing
- `--skip-index`: Skip indexing
- `--dry-run`: Preview without execution
- `--verbose`: Verbose output

## REST API (Future)

### Documents

#### List Documents
```http
GET /api/v1/documents?page=1&limit=50&sort=date
```

**Query Parameters:**
- `page` (int): Page number
- `limit` (int): Results per page (max 100)
- `sort` (string): Sort field
- `order` (string): asc or desc
- `date_start` (string): Filter by date
- `date_end` (string): Filter by date
- `type` (string): Document type

**Response:**
```json
{
  "status": "success",
  "data": {
    "documents": [
      {
        "id": "doc_12345",
        "title": "Flight Logs 2005",
        "date": "2005-03-15",
        "type": "flight_log",
        "source": "fbi_vault",
        "url": "/documents/doc_12345",
        "snippet": "Flight from...",
        "metadata": { ... }
      }
    ]
  },
  "meta": {
    "pagination": {
      "page": 1,
      "perPage": 50,
      "total": 30000,
      "totalPages": 600
    }
  }
}
```

#### Get Document
```http
GET /api/v1/documents/:id
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "document": {
      "id": "doc_12345",
      "title": "Flight Logs 2005",
      "date": "2005-03-15",
      "type": "flight_log",
      "source": "fbi_vault",
      "content": "Full text content...",
      "metadata": {
        "pages": 25,
        "size": 1024000,
        "checksum": "sha256:abc123...",
        "extracted_date": "2026-01-15"
      },
      "related": ["doc_123", "doc_456"]
    }
  }
}
```

### Search

#### Search Documents
```http
GET /api/v1/search?q=flight+logs&limit=50
POST /api/v1/search
```

**Query Parameters (GET):**
- `q` (string): Search query
- `limit` (int): Result limit
- `page` (int): Page number
- `filters` (object): JSON-encoded filters

**Request Body (POST):**
```json
{
  "query": "flight logs",
  "filters": {
    "date_range": ["2000-01-01", "2020-12-31"],
    "location": "New York",
    "document_type": "court_filing"
  },
  "limit": 50,
  "offset": 0,
  "sort": "relevance"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "id": "doc_12345",
        "title": "Flight Logs 2005",
        "snippet": "...highlighted text...",
        "score": 0.95,
        "url": "/documents/doc_12345"
      }
    ],
    "facets": {
      "years": {"2005": 150, "2006": 200},
      "types": {"flight_log": 100, "court_filing": 50},
      "locations": {"New York": 80, "Palm Beach": 70}
    }
  },
  "meta": {
    "query": "flight logs",
    "total": 350,
    "took_ms": 45
  }
}
```

### Characters

#### List Characters
```http
GET /api/v1/characters?limit=100&sort=name
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "characters": [
      {
        "id": "char_001",
        "name": "Jeffrey Epstein",
        "role": "Primary Subject",
        "connections": 250,
        "documents": 5000,
        "url": "/characters/char_001"
      }
    ]
  }
}
```

#### Get Character
```http
GET /api/v1/characters/:id
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "character": {
      "id": "char_001",
      "name": "Jeffrey Epstein",
      "biography": "...",
      "birth_date": "1953-01-20",
      "death_date": "2019-08-10",
      "roles": ["Financier", "Convicted Sex Offender"],
      "connections": [
        {
          "id": "char_002",
          "name": "Ghislaine Maxwell",
          "relationship": "Associate",
          "strength": 0.95
        }
      ],
      "timeline": [...],
      "documents": [...]
    }
  }
}
```

### Timeline

#### Get Timeline
```http
GET /api/v1/timeline?start=2000-01-01&end=2020-12-31
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "events": [
      {
        "id": "event_001",
        "date": "2005-03-15",
        "title": "Flight to Little St. James",
        "description": "...",
        "participants": ["char_001", "char_002"],
        "location": "loc_001",
        "sources": ["doc_123", "doc_456"],
        "significance": "high"
      }
    ]
  }
}
```

### Locations

#### List Locations
```http
GET /api/v1/locations
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "locations": [
      {
        "id": "loc_001",
        "name": "Little St. James Island",
        "type": "Private Island",
        "coordinates": [18.3000, -64.8250],
        "address": "U.S. Virgin Islands",
        "significance": "Primary residence",
        "events": 150,
        "documents": 500
      }
    ]
  }
}
```

## Error Handling

### Error Response Format

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid search query",
    "details": {
      "field": "query",
      "reason": "Query too short (minimum 3 characters)"
    }
  },
  "meta": {
    "timestamp": "2026-02-01T17:00:00Z"
  }
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| `INVALID_REQUEST` | Malformed request |
| `INVALID_PARAMETER` | Invalid parameter value |
| `RESOURCE_NOT_FOUND` | Resource doesn't exist |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `INTERNAL_ERROR` | Server error |
| `SERVICE_UNAVAILABLE` | Temporary unavailability |

## Examples

### Python Examples

#### Example 1: Basic Search
```python
from epstein_files import Hub

with Hub() as hub:
    results = hub.search("flight logs", limit=10)
    for doc in results:
        print(f"{doc['title']}: {doc['snippet']}")
```

#### Example 2: Full Pipeline
```python
from epstein_files import Hub

hub = Hub()

# Run full pipeline
results = hub.run_full_pipeline()

print(f"Fetched: {results['files_fetched']}")
print(f"Processed: {results['documents_processed']}")
print(f"Indexed: {results['documents_indexed']}")
```

#### Example 3: Character Analysis
```python
from epstein_files import Hub

hub = Hub()

# Get character
character = hub.get_character("Jeffrey Epstein")

# Analyze connections
connections = character['connections']
print(f"Total connections: {len(connections)}")

for conn in connections[:10]:
    print(f"  {conn['name']}: {conn['relationship']}")
```

### CLI Examples

#### Example 1: Quick Status Check
```bash
#!/bin/bash
epstein-hub status | grep "Health"
```

#### Example 2: Daily Update Script
```bash
#!/bin/bash

echo "Starting daily update..."

# Fetch new files
epstein-hub fetch --verbose

# Process documents
epstein-hub process --verbose

# Update search index
epstein-hub index --verbose

echo "Daily update complete!"
```

#### Example 3: Search and Export
```bash
#!/bin/bash

# Search and save results
epstein-hub search "court filings" \
    --date-start 2019-01-01 \
    --limit 1000 \
    --json > results.json

# Process results
jq '.data.results[] | .title' results.json
```

## SDK Support

### Official SDKs
- **Python**: Built-in (epstein_files package)
- **JavaScript**: Planned (Q2 2026)
- **Go**: Planned (Q3 2026)

### Community SDKs
Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## Webhooks (Future)

Subscribe to events:
- `document.created`
- `document.updated`
- `search.indexed`
- `agent.completed`

Configuration:
```json
{
  "url": "https://your-server.com/webhook",
  "events": ["document.created"],
  "secret": "your_webhook_secret"
}
```

## GraphQL API (Future)

Example query:
```graphql
query {
  documents(limit: 10, filters: {dateRange: ["2000-01-01", "2020-12-31"]}) {
    id
    title
    date
    characters {
      name
      role
    }
  }
}
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for API version history.

## Support

- **Documentation**: This file
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: Via GitHub profile

---

**API Version**: 1.0.0  
**Last Updated**: February 1, 2026  
**Status**: Production Ready
