# Summarization Bot

## Purpose
Generates summaries of documents and collections.

## Features
- Document summarization
- Key points extraction
- Executive summaries
- Multi-document synthesis

## Configuration

### Bot Settings
```yaml
bot_name: summarization-bot
capacity: 10000  # documents per day
priority: normal
```

## Usage

### Basic Usage
```bash
# Summarize a single document
python summarization-bot/summarize.py --file path/to/document.pdf

# Summarize multiple documents
python summarization-bot/summarize.py --directory path/to/documents/

# Generate executive summary
python summarization-bot/summarize.py --file document.pdf --format executive
```

### API Usage
```python
from bots.summarization_bot import SummarizationBot

bot = SummarizationBot()
summary = bot.summarize_document("path/to/document.pdf")
print(summary)
```

## Output Format

### Summary Structure
```json
{
  "document_id": "abc123",
  "brief_summary": "50-100 word summary",
  "key_points": [
    "Point 1",
    "Point 2",
    "Point 3"
  ],
  "important_dates": ["2024-01-01"],
  "key_names": ["Person A", "Person B"],
  "relevance_score": 0.85
}
```

## Dependencies
- Python 3.9+
- Azure OpenAI Service
- PyPDF2

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
