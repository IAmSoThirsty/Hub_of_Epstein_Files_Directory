# Fact-Checking Bot

## Purpose
Verifies claims and sources information.

## Features
- Source verification
- Cross-reference checking
- Credibility scoring
- Citation validation

## Configuration

### Bot Settings
```yaml
bot_name: fact-checking-bot
capacity: 3000  # claims per day
priority: high
```

## Usage

### Basic Usage
```bash
# Check facts in a document
python fact-checking-bot/verify.py --file path/to/document.pdf

# Verify a specific claim
python fact-checking-bot/verify.py --claim "Specific claim to verify"

# Generate verification report
python fact-checking-bot/verify.py --file document.pdf --output report.json
```

### API Usage
```python
from bots.fact_checking_bot import FactCheckingBot

bot = FactCheckingBot()
result = bot.verify_claim("Specific claim to verify")
print(result)
```

## Output Format

### Verification Result
```json
{
  "claim": "Specific claim to verify",
  "verdict": "verified|disputed|unverifiable",
  "confidence": 0.85,
  "sources": [
    {
      "title": "Court Records",
      "url": "https://example.com/doc",
      "date": "2020-01-15",
      "relevance": 0.92,
      "credibility": "high"
    }
  ],
  "inconsistencies": [
    {
      "type": "date_mismatch",
      "description": "Date conflicts with other source",
      "severity": "medium"
    }
  ],
  "fact_check_summary": "Summary of findings"
}
```

## Verification Process

1. **Extract Claims** - Identify factual statements
2. **Search Sources** - Query authoritative databases
   - Court records
   - Government databases
   - Verified news sources
   - Academic publications
3. **Compare** - Cross-reference information
4. **Score** - Assign credibility rating
5. **Flag** - Mark inconsistencies

## Dependencies
- Python 3.9+
- Azure Cognitive Search
- BeautifulSoup4
- requests

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
