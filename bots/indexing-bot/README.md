# Document Indexing Bot

## Purpose
Automatically indexes new documents for searchability and organization.

## Features
- Automatic categorization
- Metadata extraction
- Index updates
- Cross-referencing

## Configuration

### Bot Settings
```yaml
bot_name: indexing-bot
capacity: 6000  # documents per day
priority: high
```

## Usage

### Basic Usage
```bash
# Index a single document
python indexing-bot/index.py --file path/to/document.pdf

# Index directory of documents
python indexing-bot/index.py --directory path/to/documents/

# Re-index all documents
python indexing-bot/index.py --reindex-all
```

### API Usage
```python
from bots.indexing_bot import IndexingBot

bot = IndexingBot()
result = bot.index_document("path/to/document.pdf")
print(result)
```

## Output Format

### Index Entry
```json
{
  "document_id": "doc_123",
  "title": "Document Title",
  "category": "court_filing",
  "subcategory": "deposition",
  "date": "2020-01-15",
  "metadata": {
    "case_number": "20-CV-1234",
    "filing_date": "2020-01-15",
    "court": "Southern District of New York",
    "pages": 45,
    "redaction_status": "partial"
  },
  "entities": {
    "people": ["Person A", "Person B"],
    "organizations": ["Org A"],
    "locations": ["New York", "Florida"]
  },
  "keywords": ["keyword1", "keyword2"],
  "full_text_path": "data/processed/text/doc_123.txt",
  "indexed_at": "2024-12-22T10:30:00Z"
}
```

## Indexing Process

1. **Document Analysis**
   - Extract text content
   - Identify document type
   - Extract metadata

2. **Categorization**
   - Assign primary category
   - Assign subcategory
   - Tag with keywords

3. **Entity Extraction**
   - Identify people
   - Identify organizations
   - Identify locations
   - Identify dates

4. **Cross-Reference**
   - Link to related documents
   - Update entity profiles
   - Build relationship graph

5. **Search Index Update**
   - Add to search engine
   - Update facets
   - Refresh statistics

## Search Integration

### Lunr.js Index Format
```javascript
{
  "id": "doc_123",
  "title": "Document Title",
  "body": "Full text content...",
  "category": "court_filing",
  "date": "2020-01-15",
  "people": "Person A, Person B"
}
```

## Dependencies
- Python 3.9+
- PyPDF2
- Azure Cognitive Search
- Lunr.js (for client-side search)

## Installation
```bash
pip install -r requirements.txt
```

## Status
⚠️ **In Development** - This bot is currently being developed. Full implementation coming soon.

## Contributing
See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## Support
- GitHub Issues for bugs
- GitHub Discussions for questions
