# PDF Analysis Bot

This bot analyzes uploaded PDF files to determine if they contain Epstein-related content. Files with relevant content are processed and indexed; irrelevant files are moved to trash.

## Features

### Content Analysis
- **Keyword Detection:** Scans for relevant names, places, and terms
- **Entity Recognition:** Identifies people, organizations, and locations
- **Context Analysis:** Uses AI to understand document context
- **Relevance Scoring:** Assigns confidence score (0-100%)

### Automated Routing
- **Relevant Content (>70%):** → Indexing pipeline
- **Possibly Relevant (40-70%):** → Manual review queue
- **Not Relevant (<40%):** → Trash

### Metadata Extraction
- Document title
- Creation date
- Author (if available)
- Page count
- Text content
- Embedded images

## How It Works

### 1. Upload Detection
When a PDF is uploaded to `/data/uploads/`:
- GitHub Actions workflow triggers
- File is queued for analysis

### 2. Analysis Pipeline
```
Upload → Extract Text → Analyze Content → Score Relevance → Route Document
```

### 3. Processing Steps

#### Text Extraction
- OCR for scanned documents
- Text parsing for digital PDFs
- Image extraction
- Metadata reading

#### Content Analysis
- Keyword matching against relevance dictionary
- Named entity recognition
- Context analysis using Azure OpenAI
- Pattern matching (dates, locations, names)

#### Relevance Scoring
```python
relevance_score = (
    keyword_matches * 0.3 +
    entity_matches * 0.3 +
    context_score * 0.4
)
```

### 4. Results
- Analysis report generated
- File routed based on score
- Metadata saved to index
- Notifications sent (if configured)

## Configuration

### Keywords Dictionary
Located in `config/keywords.yml`:

```yaml
high_priority:
  - "Jeffrey Epstein"
  - "Ghislaine Maxwell"
  - "Little St. James"
  - "flight logs"
  - # ... more terms

medium_priority:
  - "Virgin Islands"
  - "Palm Beach"
  - # ... more terms

entities:
  people:
    - # Names from Character Directory
  places:
    - # Locations from Glossary
  organizations:
    - # Organizations
```

### Scoring Thresholds
Located in `config/pdf-analysis.yml`:

```yaml
thresholds:
  accept: 70  # Auto-index if score >= 70
  review: 40  # Manual review if 40 <= score < 70
  reject: 40  # Auto-trash if score < 40

processing:
  ocr_enabled: true
  max_file_size: 100MB
  timeout: 300  # seconds

ai_services:
  azure_openai_endpoint: ${AZURE_OPENAI_ENDPOINT}
  azure_document_intelligence: ${AZURE_DOC_INTEL_ENDPOINT}
```

## Usage

### Via GitHub Actions (Recommended)

1. **Upload File:** Add PDF to `/data/uploads/` folder
2. **Commit & Push:** Changes trigger analysis workflow
3. **Wait for Analysis:** Bot processes automatically
4. **Check Results:** View analysis report in PR comments

### Via CLI

```bash
# Analyze single file
python bots/pdf-analysis-bot/analyze.py --file path/to/document.pdf

# Analyze directory
python bots/pdf-analysis-bot/analyze.py --dir path/to/pdfs/

# With custom threshold
python bots/pdf-analysis-bot/analyze.py --file doc.pdf --threshold 60
```

### Via Web Interface

1. Navigate to web interface
2. Click "Upload PDF"
3. Select file(s)
4. Click "Analyze"
5. View results

## Analysis Report Format

```json
{
  "file": "document.pdf",
  "timestamp": "2024-12-20T12:00:00Z",
  "analysis": {
    "relevance_score": 85,
    "confidence": 0.92,
    "decision": "ACCEPT",
    "routing": "index"
  },
  "content": {
    "page_count": 45,
    "text_extracted": true,
    "language": "en",
    "has_images": true
  },
  "matches": {
    "keywords": ["Jeffrey Epstein", "flight logs", "Little St. James"],
    "entities": {
      "people": ["Jane Doe", "John Smith"],
      "places": ["Virgin Islands", "Palm Beach"],
      "dates": ["2005-03-15", "2019-07-06"]
    }
  },
  "metadata": {
    "title": "Flight Manifests 2005",
    "author": "Unknown",
    "created": "2005-03-20",
    "modified": "2005-03-20"
  }
}
```

## GitHub Actions Workflow

File: `.github/workflows/pdf-analysis.yml`

```yaml
name: PDF Analysis
on:
  push:
    paths:
      - 'data/uploads/**.pdf'
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r bots/pdf-analysis-bot/requirements.txt
      
      - name: Analyze PDFs
        env:
          AZURE_OPENAI_KEY: ${{ secrets.AZURE_OPENAI_KEY }}
          AZURE_DOC_INTEL_KEY: ${{ secrets.AZURE_DOC_INTEL_KEY }}
        run: |
          python bots/pdf-analysis-bot/analyze.py --dir data/uploads/
      
      - name: Process Results
        run: |
          python bots/pdf-analysis-bot/route.py
      
      - name: Commit Changes
        run: |
          git config user.name "PDF Analysis Bot"
          git config user.email "bot@github.com"
          git add .
          git commit -m "Process uploaded PDFs" || exit 0
          git push
```

## Dependencies

### Python Requirements
```txt
azure-ai-documentintelligence>=1.0.0
azure-ai-textanalytics>=5.3.0
openai>=1.0.0
pypdf>=3.9.0
pdf2image>=1.16.0
pytesseract>=0.3.10
pillow>=10.0.0
pyyaml>=6.0
python-magic>=0.4.27
```

### System Requirements
- Python 3.9+
- Tesseract OCR
- Poppler (for pdf2image)
- Azure subscription (for AI services)

## Security & Privacy

### Data Protection
- Files encrypted at rest
- Secure deletion for trash items
- Access logging
- No external data transmission (except to Azure)

### Privacy Compliance
- Automatic PII redaction
- Victim identity protection
- Compliance with court sealing orders
- GDPR/privacy law adherence

### Content Filtering
- Inappropriate content detection
- Automatic flagging system
- Admin review for flagged content

## Monitoring

### Logs
- Processing logs: `logs/pdf-analysis/`
- Error logs: `logs/errors/`
- Access logs: `logs/access/`

### Metrics
- Files processed
- Average processing time
- Success/failure rate
- Relevance score distribution

### Alerts
- Processing failures
- High volume uploads
- Suspicious patterns
- API quota warnings

## Troubleshooting

### Common Issues

**OCR Fails:**
- Check Tesseract installation
- Verify image quality
- Increase timeout

**Low Relevance Scores:**
- Update keywords dictionary
- Adjust scoring weights
- Check AI model performance

**Upload Errors:**
- Check file size limits
- Verify file format
- Check permissions

## Development

### Testing
```bash
# Unit tests
pytest bots/pdf-analysis-bot/tests/

# Integration tests
pytest bots/pdf-analysis-bot/tests/integration/

# Test with sample file
python bots/pdf-analysis-bot/analyze.py --file tests/fixtures/sample.pdf --debug
```

### Contributing
See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## API Reference

### analyze_pdf()
```python
def analyze_pdf(file_path: str, threshold: int = 70) -> AnalysisResult:
    """
    Analyze PDF for Epstein-related content.
    
    Args:
        file_path: Path to PDF file
        threshold: Minimum relevance score (0-100)
    
    Returns:
        AnalysisResult object with scores and routing decision
    """
```

### route_document()
```python
def route_document(analysis: AnalysisResult) -> str:
    """
    Route document based on analysis.
    
    Args:
        analysis: AnalysisResult object
    
    Returns:
        Destination path (index, review, or trash)
    """
```

## Examples

### Example 1: High Relevance Document
```
File: flight_log_2005.pdf
Score: 95
Decision: ACCEPT → Indexed
Reason: Contains multiple high-priority keywords and entities
```

### Example 2: Low Relevance Document
```
File: random_recipe.pdf
Score: 5
Decision: REJECT → Trash
Reason: No relevant keywords or entities found
```

### Example 3: Manual Review Needed
```
File: business_document.pdf
Score: 55
Decision: REVIEW → Manual Review Queue
Reason: Some matches but context unclear
```

---

*This bot is continuously improved based on feedback and performance metrics.*

*Last Updated: December 2024*
