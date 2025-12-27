# Entity Extraction Bot

## Purpose
Identifies and catalogs people, places, and organizations.

## Features
- Named entity recognition
- Relationship mapping
- Character directory updates
- Location tracking

## Configuration

### Bot Settings
```yaml
bot_name: entity-extraction-bot
capacity: 8000  # documents per day
priority: high
```

## Usage

### Basic Usage
```bash
# Extract entities from a document
python entity-extraction-bot/extract.py --file path/to/document.pdf

# Extract entities from directory
python entity-extraction-bot/extract.py --directory path/to/documents/

# Update character directory
python entity-extraction-bot/extract.py --update-directory
```

### API Usage
```python
from bots.entity_extraction_bot import EntityExtractionBot

bot = EntityExtractionBot()
entities = bot.extract_entities("path/to/document.pdf")
print(entities)
```

## Output Format

### Entity Structure
```json
{
  "document_id": "abc123",
  "entities": {
    "people": [
      {
        "name": "John Doe",
        "mentions": 15,
        "contexts": ["witness", "associate"],
        "confidence": 0.98
      }
    ],
    "organizations": [
      {
        "name": "ABC Corporation",
        "mentions": 8,
        "type": "company",
        "confidence": 0.92
      }
    ],
    "locations": [
      {
        "name": "New York",
        "mentions": 23,
        "type": "city",
        "coordinates": [40.7128, -74.0060],
        "confidence": 0.99
      }
    ]
  },
  "relationships": [
    {
      "entity1": "John Doe",
      "entity2": "ABC Corporation",
      "type": "employed_by"
    }
  ]
}
```

## Dependencies
- Python 3.9+
- Azure Text Analytics
- spaCy

## Installation
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

## Status
⚠️ **In Development** - This bot is currently being developed. Full implementation coming soon.

## Contributing
See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## Support
- GitHub Issues for bugs
- GitHub Discussions for questions
