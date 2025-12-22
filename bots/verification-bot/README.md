# Source Verification Bot

## Purpose
Validates document authenticity and sources.

## Features
- Source checking
- Authenticity verification
- Provenance tracking
- Quality scoring

## Configuration

### Bot Settings
```yaml
bot_name: verification-bot
capacity: 2000  # documents per day
priority: critical
```

## Usage

### Basic Usage
```bash
# Verify a document source
python verification-bot/verify.py --file path/to/document.pdf

# Verify multiple documents
python verification-bot/verify.py --directory path/to/documents/

# Generate verification report
python verification-bot/verify.py --file document.pdf --report detailed
```

### API Usage
```python
from bots.verification_bot import VerificationBot

bot = VerificationBot()
result = bot.verify_source("document_id_123")
print(result)
```

## Output Format

### Verification Result
```json
{
  "document_id": "doc_123",
  "verification_level": 4,
  "verification_date": "2024-12-22",
  "source_authenticity": {
    "status": "verified",
    "confidence": 0.95,
    "method": "digital_signature_check"
  },
  "provenance": {
    "original_source": "Federal Court",
    "source_type": "official_document",
    "acquisition_method": "public_records_request",
    "chain_of_custody": [
      {
        "date": "2020-01-15",
        "event": "Filed in court",
        "location": "SDNY Clerk's Office"
      },
      {
        "date": "2020-02-01",
        "event": "Made public",
        "location": "PACER"
      }
    ]
  },
  "quality_checks": {
    "format_valid": true,
    "metadata_complete": true,
    "no_tampering_detected": true,
    "watermark_verified": true
  },
  "flags": [],
  "recommendations": ["Safe to publish"]
}
```

## Verification Levels

| Level | Description | Requirements |
|-------|-------------|--------------|
| 5 | **Verified Official** | Court-stamped, digitally signed, official source |
| 4 | **Verified Public** | Public records, PACER, official government sites |
| 3 | **Credible Source** | Reputable journalism, verified leaks |
| 2 | **Unverified** | Source unclear, needs additional verification |
| 1 | **Suspicious** | Potential manipulation, unverifiable source |

## Verification Process

1. **Source Identification**
   - Identify originating source
   - Check source credibility
   - Verify official markings

2. **Authenticity Checks**
   - Digital signature verification
   - Watermark analysis
   - Format validation
   - Metadata consistency

3. **Provenance Tracking**
   - Document chain of custody
   - Verify acquisition method
   - Check publication history

4. **Quality Assessment**
   - Check completeness
   - Detect tampering
   - Assess reliability

5. **Scoring**
   - Assign verification level (1-5)
   - Flag suspicious elements
   - Recommend actions

## Dependencies
- Python 3.9+
- cryptography
- PyPDF2
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
