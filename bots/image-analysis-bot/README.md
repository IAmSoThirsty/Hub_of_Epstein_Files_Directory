# Image Analysis Bot

## Purpose
Analyzes and catalogs images and photographs.

## Features
- Image recognition
- Reverse image search
- Metadata extraction
- Face detection (when legally appropriate)
- Location identification

## Configuration

### Bot Settings
```yaml
bot_name: image-analysis-bot
capacity: 5000  # images per day
priority: normal
```

## Usage

### Basic Usage
```bash
# Analyze a single image
python image-analysis-bot/analyze.py --file path/to/image.jpg

# Analyze directory of images
python image-analysis-bot/analyze.py --directory path/to/images/

# Extract metadata only
python image-analysis-bot/analyze.py --file image.jpg --metadata-only
```

### API Usage
```python
from bots.image_analysis_bot import ImageAnalysisBot

bot = ImageAnalysisBot()
analysis = bot.analyze_image("path/to/image.jpg")
print(analysis)
```

## Output Format

### Analysis Result
```json
{
  "image_id": "img_123",
  "filename": "photo.jpg",
  "metadata": {
    "date_taken": "2015-03-15",
    "location": {
      "latitude": 40.7128,
      "longitude": -74.0060,
      "name": "New York"
    },
    "camera": "Canon EOS 5D",
    "dimensions": "3000x2000"
  },
  "content_analysis": {
    "description": "Aerial view of an island",
    "objects": ["building", "trees", "water"],
    "text_detected": ["Sign text"],
    "confidence": 0.87
  },
  "reverse_search_results": [
    {
      "source": "public database",
      "url": "https://example.com/image",
      "similarity": 0.95
    }
  ],
  "privacy_flags": [
    {
      "type": "identifiable_person",
      "action": "redaction_required"
    }
  ]
}
```

## Privacy & Legal Compliance

### Automatic Redaction
- Identifies faces in images
- Applies privacy-compliant blurring
- Logs all redactions
- Complies with court orders

### Content Filtering
- Detects inappropriate content
- Flags for manual review
- Maintains audit trail

## Dependencies
- Python 3.9+
- Azure Computer Vision
- Pillow
- ExifRead

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
