# Bot Infrastructure

This directory contains configuration and documentation for automated bots that help organize, analyze, and search the Epstein files directory.

## Available Bots

### 1. PDF Analysis Bot
**Purpose:** Analyzes uploaded PDF files to determine if they contain Epstein-related content.

**Features:**
- Automatic content analysis
- Keyword and entity detection
- Relevance scoring
- Auto-filing or trash routing
- Metadata extraction

**Usage:** See [pdf-analysis-bot/README.md](pdf-analysis-bot/README.md)

### 2. Document Search Bot
**Purpose:** Provides intelligent search across all documents.

**Features:**
- Multi-engine search (Google, Bing, DuckDuckGo)
- Full-text search
- Entity-based search
- Image search capabilities
- Advanced filtering

**Usage:** See [search-bot/README.md](search-bot/README.md)

### 3. Summarization Bot
**Purpose:** Generates summaries of documents and collections.

**Features:**
- Document summarization
- Key points extraction
- Executive summaries
- Multi-document synthesis

**Usage:** See [summarization-bot/README.md](summarization-bot/README.md)

### 4. Cross-Reference Bot
**Purpose:** Identifies connections between documents and entities.

**Features:**
- Entity co-occurrence detection
- Document relationship mapping
- Citation tracking
- Network analysis

**Usage:** See [cross-reference-bot/README.md](cross-reference-bot/README.md)

### 5. Timeline Generator Bot
**Purpose:** Creates chronological timelines from documents.

**Features:**
- Date extraction
- Event sequencing
- Timeline visualization
- Multi-source correlation

**Usage:** See [timeline-bot/README.md](timeline-bot/README.md)

### 6. Entity Extraction Bot
**Purpose:** Identifies and catalogs people, places, and organizations.

**Features:**
- Named entity recognition
- Relationship mapping
- Character directory updates
- Location tracking

**Usage:** See [entity-extraction-bot/README.md](entity-extraction-bot/README.md)

### 7. Fact-Checking Bot
**Purpose:** Verifies claims and sources information.

**Features:**
- Source verification
- Cross-reference checking
- Credibility scoring
- Citation validation

**Usage:** See [fact-checking-bot/README.md](fact-checking-bot/README.md)

### 8. Image Analysis Bot
**Purpose:** Analyzes and catalogs images and photographs.

**Features:**
- Image recognition
- Reverse image search
- Metadata extraction
- Face detection (when legally appropriate)
- Location identification

**Usage:** See [image-analysis-bot/README.md](image-analysis-bot/README.md)

### 9. Document Indexing Bot
**Purpose:** Automatically indexes new documents.

**Features:**
- Automatic categorization
- Metadata extraction
- Index updates
- Cross-referencing

**Usage:** See [indexing-bot/README.md](indexing-bot/README.md)

### 10. Source Verification Bot
**Purpose:** Validates document authenticity and sources.

**Features:**
- Source checking
- Authenticity verification
- Provenance tracking
- Quality scoring

**Usage:** See [verification-bot/README.md](verification-bot/README.md)

## Bot Orchestration

### Workflow Integration
Bots work together in automated workflows:

1. **Document Upload** → PDF Analysis Bot
2. **If Relevant** → Indexing Bot → Entity Extraction Bot
3. **If Not Relevant** → Moved to trash
4. **After Indexing** → Cross-Reference Bot + Timeline Bot
5. **On Request** → Search Bot, Summarization Bot, Fact-Checking Bot

### Configuration
See [config/orchestration.yml](config/orchestration.yml) for workflow configuration.

## Technical Architecture

### Backend
- Python-based bot framework
- Azure AI Services integration
- GitHub Actions for automation
- Azure Cognitive Search

### APIs Used
- Azure Document Intelligence
- Azure Cognitive Search
- Azure OpenAI Service
- Google Search API
- Bing Search API
- DuckDuckGo API

### Data Storage
- Azure Blob Storage for documents
- GitHub repository for metadata
- Azure SQL for indexing
- Redis for caching

## Security & Privacy

### Data Protection
- Encrypted storage
- Secure API access
- Privacy-compliant processing
- Access logging

### Content Filtering
- Automatic redaction of sensitive info
- Privacy law compliance
- Victim identity protection

## Getting Started

### Prerequisites
- Azure subscription (for AI services)
- GitHub account
- API keys for search engines
- Python 3.9+

### Setup
1. Clone the repository
2. Configure Azure services
3. Set up API keys
4. Install dependencies
5. Run configuration script

See [SETUP.md](SETUP.md) for detailed instructions.

## Bot Development

### Creating a New Bot
1. Follow bot template structure
2. Implement required interfaces
3. Add configuration
4. Write tests
5. Document usage

See [DEVELOPMENT.md](DEVELOPMENT.md) for guidelines.

### Testing Bots
```bash
# Test individual bot
python -m pytest bots/bot-name/tests/

# Test all bots
python -m pytest bots/

# Integration tests
python -m pytest tests/integration/
```

## Configuration Files

### Bot Configs
- `config/pdf-analysis.yml` - PDF analysis settings
- `config/search.yml` - Search engine configuration
- `config/ai-services.yml` - Azure AI settings
- `config/orchestration.yml` - Workflow configuration

### Secrets Management
- Use GitHub Secrets for sensitive data
- Azure Key Vault for API keys
- Environment variables for configuration

## Monitoring & Logs

### Bot Activity
- Activity logs in `logs/`
- Error reporting
- Performance metrics
- Usage statistics

### Dashboards
- Bot performance dashboard
- Processing queue status
- Error rate monitoring
- Resource utilization

## Usage Examples

### Analyzing a PDF
```bash
# Upload via web interface
# Or trigger via GitHub Actions
# Or use CLI
python bots/pdf-analysis-bot/analyze.py --file path/to/document.pdf
```

### Searching Documents
```bash
# Web interface search
# Or API call
curl -X POST https://api.example.com/search -d '{"query": "flight logs"}'
```

### Generating Timeline
```bash
# Automatic generation
python bots/timeline-bot/generate.py --source docs/ --output timeline.html
```

## Support

### Documentation
- Individual bot READMEs
- API documentation
- Configuration guides
- Troubleshooting guides

### Issues
Report bot issues on GitHub Issues with:
- Bot name
- Error messages
- Steps to reproduce
- Expected vs actual behavior

## Future Enhancements

- Machine learning model improvements
- Additional language support
- Enhanced OCR capabilities
- Real-time processing
- Collaborative features
- Mobile app integration

---

*This bot infrastructure is continuously improved based on usage and feedback.*

*Last Updated: December 2024*
