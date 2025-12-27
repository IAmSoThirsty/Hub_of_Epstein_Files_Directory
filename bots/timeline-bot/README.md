# Timeline Generator Bot

## Purpose
Creates chronological timelines from documents.

## Features
- Date extraction
- Event sequencing
- Timeline visualization
- Multi-source correlation

## Configuration

### Bot Settings
```yaml
bot_name: timeline-bot
capacity: 5000  # documents per day
priority: normal
```

## Usage

### Basic Usage
```bash
# Generate timeline from documents
python timeline-bot/generate.py --source docs/ --output timeline.html

# Generate timeline for specific person
python timeline-bot/generate.py --entity "Person Name" --output timeline.json

# Generate timeline for date range
python timeline-bot/generate.py --start 2000-01-01 --end 2020-12-31
```

### API Usage
```python
from bots.timeline_bot import TimelineBot

bot = TimelineBot()
timeline = bot.generate_timeline("Person Name")
print(timeline)
```

## Output Format

### Timeline Structure
```json
{
  "entity": "Person Name",
  "events": [
    {
      "date": "2015-06-15",
      "description": "Event description",
      "source_document": "doc_id_123",
      "location": "New York",
      "confidence": 0.95
    }
  ],
  "date_range": {
    "start": "2000-01-01",
    "end": "2020-12-31"
  }
}
```

### HTML Output
Generates an interactive HTML timeline with:
- Zoomable date range
- Clickable events
- Source links
- Visual markers

## Dependencies
- Python 3.9+
- Azure Form Recognizer
- Plotly (for visualization)

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
