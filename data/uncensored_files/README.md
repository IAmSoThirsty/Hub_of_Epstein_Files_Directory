# Uncensored.ai Integration

This directory contains Epstein-related files fetched from the Uncensored.ai free database.

## Overview

The Uncensored.ai integration provides continuous data extraction and ingestion of publicly available Epstein files from the Uncensored.ai database. This includes documents, images, flight logs, financial records, and other evidence.

## Directory Structure

```
uncensored_files/
├── documents/          # Court documents, depositions, legal filings
├── images/             # Photos, scanned documents, evidence photos
├── videos/             # Video depositions, news footage, interviews
├── flight_logs/        # Aviation records and flight manifests
├── financial/          # Banking records, property records, transactions
├── metadata/           # JSON metadata for all downloaded files
├── uncensored_manifest.json  # Complete manifest of all files
├── fetch_results.json  # Latest fetch operation results
└── integration_report.md     # Integration report from last run
```

## Features

- **Automatic Deduplication**: Files are checked against existing downloads to avoid duplicates
- **Metadata Extraction**: Comprehensive metadata is extracted and stored for each file
- **Category-based Fetching**: Fetch specific categories or all at once
- **Rate Limiting**: Respects API rate limits to be a good citizen
- **Integrity Verification**: SHA-256 hashes for file integrity verification
- **Continuous Integration**: Daily automated fetches via GitHub Actions

## Usage

### Manual Fetch

Fetch all categories:
```bash
python scripts/fetch-uncensored-files.py --all
```

Fetch specific category:
```bash
python scripts/fetch-uncensored-files.py --category documents
```

Force refresh (ignore cache):
```bash
python scripts/fetch-uncensored-files.py --all --force
```

View statistics:
```bash
python scripts/fetch-uncensored-files.py --stats
```

### Automated Fetch

The GitHub Actions workflow `.github/workflows/uncensored-integration.yml` runs automatically:
- **Schedule**: Daily at 2:00 AM UTC
- **Manual Trigger**: Available via GitHub Actions UI

### Configuration

Set these environment variables in `.env`:

```bash
# Enable/disable integration
UNCENSORED_AI_ENABLED=true

# API endpoint (optional, uses default if not set)
UNCENSORED_AI_BASE_URL=https://api.uncensored.ai/v1

# API key (optional, for higher rate limits)
UNCENSORED_AI_API_KEY=your_api_key_here

# Rate limit delay in seconds between requests
UNCENSORED_AI_RATE_LIMIT=2

# Update frequency for automated fetches
UNCENSORED_AI_UPDATE_FREQUENCY=daily

# Output directory
UNCENSORED_FILES_DIR=./data/uncensored_files
```

## File Metadata

Each file has associated metadata stored in `metadata/`:

```json
{
  "id": "unique_file_id",
  "source": "Uncensored.ai",
  "url": "https://...",
  "type": "document",
  "title": "Document title",
  "description": "Document description",
  "date": "2024-01-01",
  "download_date": "2024-01-15T12:00:00Z",
  "file_path": "data/uncensored_files/documents/...",
  "file_size": 1048576,
  "sha256": "abc123...",
  "tags": ["tag1", "tag2"],
  "related_entities": ["person1", "location1"]
}
```

## Integration with Hub

The Uncensored.ai integration is fully integrated with the Hub core:

```python
from epstein_files.core.hub import Hub

# Initialize Hub
hub = Hub()

# Fetch all Uncensored.ai files
results = hub.fetch_uncensored_files()

# Fetch specific categories
results = hub.fetch_uncensored_files(categories=['documents', 'flight_logs'])

# Access the manager directly
manager = hub.uncensored_ai
stats = manager.get_statistics()
```

## Categories

### Documents
Court filings, depositions, motions, legal correspondence, and other legal documents.

### Images
Photographs, scanned documents, evidence photos, and other visual evidence.

### Videos
Video depositions, news footage, interviews, and other video content.

### Flight Logs
Aviation records, flight manifests, passenger lists, and travel documentation.

### Financial Records
Banking documents, property records, transaction records, and financial statements.

## Safety & Compliance

The integration follows these safety protocols:

1. **Source Verification**: All files are verified from Uncensored.ai API
2. **Deduplication**: Automatic checking to avoid duplicate downloads
3. **Integrity Checks**: SHA-256 hashing for file integrity
4. **Rate Limiting**: Respects API rate limits
5. **Privacy Protection**: Handles sensitive data appropriately
6. **Legal Compliance**: Only fetches publicly available data

## Troubleshooting

### Integration Disabled

If you see "Uncensored.ai integration is disabled":
1. Copy `.env.example` to `.env`
2. Set `UNCENSORED_AI_ENABLED=true`
3. Run the fetch script again

### API Errors

If you encounter API errors:
1. Check your internet connection
2. Verify `UNCENSORED_AI_BASE_URL` is correct
3. Check if API key is required and set correctly
4. Review rate limiting settings

### Large Repository Size

If the repository becomes too large:
1. Consider using Git LFS for large files
2. Exclude certain file types from repository
3. Store large files externally
4. Review and cleanup old files

## Next Steps

After fetching files:

1. **Process Documents**: Run `python scripts/process-pdfs.py` to extract text
2. **Update Search Index**: Run `python scripts/generate-search-index.py`
3. **Review Files**: Check downloaded files in each category directory
4. **Commit Changes**: If within repository limits, commit to version control

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory/issues
- Documentation: See project README.md and ARCHITECTURE.md

## License

This integration follows the same license as the main project. All data fetched is publicly available from Uncensored.ai's free database.
