# Search Bot Infrastructure (AI Agents Only)

This search infrastructure is designed for AI agent use only. It provides backend search capabilities across multiple search engines to help agents locate and retrieve information from the 30,000+ documents and 20,000+ images.

## Overview

The search bots operate independently in the background, accessible only to other AI agents for information retrieval, fact-checking, and cross-referencing tasks. Users do not have direct access to search functionality; instead, they browse the AI-curated codex.

## Search Agent Architecture

### 1. Multi-Engine Search Coordinator Agent

**Purpose:** Coordinates searches across multiple search engines simultaneously

**Capabilities:**
- Query distribution to multiple engines
- Result aggregation and deduplication
- Relevance ranking
- Response caching
- Load balancing

**Search Engines Integrated:**
- Internal Elasticsearch cluster
- Azure Cognitive Search
- Google Custom Search API
- Bing Search API
- DuckDuckGo API

**Configuration:**
```yaml
coordinator:
  max_concurrent_searches: 10
  timeout_seconds: 30
  cache_ttl: 3600
  deduplication: true
  relevance_threshold: 0.7
```

### 2. Internal Document Search Agent

**Purpose:** Fast full-text search across indexed documents

**Technology:**
- **Elasticsearch** - Primary search engine
- **Azure Cognitive Search** - Semantic search
- **PostgreSQL Full-Text Search** - Backup

**Features:**
- Full-text search with stemming
- Fuzzy matching for misspellings
- Phrase matching
- Boolean operators
- Field-specific search
- Faceted search by category, date, source
- Proximity search

**Index Structure:**
```json
{
  "document_id": "unique-id",
  "title": "document title",
  "content": "full text content",
  "summary": "AI-generated summary",
  "date": "2024-01-01",
  "category": "legal",
  "source": "SDNY",
  "verification_level": 1,
  "entities": ["person1", "location1"],
  "tags": ["keyword1", "keyword2"]
}
```

### 3. Image Search Agent

**Purpose:** Search and retrieve images from the 20,000+ image database

**Capabilities:**
- Reverse image search
- Visual similarity matching
- OCR text search within images
- Metadata search (EXIF, tags, captions)
- Facial recognition (when legally appropriate)
- Location-based search

**Technology:**
- **Azure Computer Vision** - Image analysis
- **Azure Face API** - Facial recognition
- **TinEye API** - Reverse image search
- **Google Vision AI** - Image understanding
- **Custom image hash database** - Similarity matching

**Search Methods:**
1. Content-based (visual similarity)
2. Text-based (OCR content)
3. Metadata-based (tags, locations, dates)
4. Hash-based (exact and near duplicates)

### 4. Semantic Search Agent

**Purpose:** Natural language understanding and semantic search

**Technology:**
- **Azure OpenAI Service** - Embeddings and semantic understanding
- **Vector database** - Semantic similarity search
- **BERT models** - Context understanding

**Capabilities:**
- Natural language query interpretation
- Conceptual search (not just keywords)
- Context-aware results
- Query expansion
- Intent recognition
- Relationship discovery

**Example Queries:**
- "Documents about property transactions in Virgin Islands"
- "Communications between individuals during 2005"
- "Evidence related to specific locations"

### 5. Entity Search Agent

**Purpose:** Search by people, places, organizations

**Capabilities:**
- Entity-based filtering
- Relationship traversal
- Co-occurrence analysis
- Network queries
- Timeline queries

**Entity Types:**
- **People** - Indexed from Character Directory
- **Locations** - Geographic entities
- **Organizations** - Companies, foundations, agencies
- **Dates** - Temporal entities
- **Events** - Significant occurrences

### 6. Cross-Reference Search Agent

**Purpose:** Find relationships and connections between documents

**Capabilities:**
- Citation tracking
- Document similarity
- Network analysis
- Pattern detection
- Connection discovery

**Algorithms:**
- Graph traversal
- Link analysis
- Clustering
- Association rule mining

### 7. Fact-Checking Search Agent

**Purpose:** Verify claims and find supporting evidence

**Capabilities:**
- Multi-source verification
- Contradiction detection
- Evidence gathering
- Source credibility assessment
- Timeline verification

**Process:**
1. Parse claim to verify
2. Search across all sources
3. Find supporting/contradicting evidence
4. Assess source credibility
5. Generate verification report

### 8. Source Verification Search Agent

**Purpose:** Validate document sources and authenticity

**Capabilities:**
- Source origin tracking
- Cross-reference with official records
- Document authenticity checks
- Chain of custody verification
- Provenance tracking

**Verification Levels:**
- Level 1: Official court documents (PACER verified)
- Level 2: Government records (FOIA verified)
- Level 3: Verified media sources
- Level 4: Secondary sources
- Level 5: Unverified/pending

## Search APIs (AI Agents Only)

### REST API Endpoints

**Base URL:** `http://internal-api.epstein-codex.local/api/v1/`

**Authentication:** Internal service token (not exposed to public)

#### Document Search
```
POST /search/documents
{
  "query": "search terms",
  "filters": {
    "category": ["legal", "financial"],
    "date_range": {"start": "2005-01-01", "end": "2008-12-31"},
    "source": ["SDNY"],
    "verification_level": [1, 2]
  },
  "limit": 100,
  "offset": 0
}
```

#### Image Search
```
POST /search/images
{
  "query": "search terms",
  "search_type": "text|visual|metadata",
  "filters": {
    "category": ["evidence", "location"],
    "date_range": {},
    "location": "Little St. James"
  }
}
```

#### Semantic Search
```
POST /search/semantic
{
  "query": "natural language query",
  "context": "additional context",
  "max_results": 50
}
```

#### Entity Search
```
POST /search/entities
{
  "entity_type": "person|location|organization",
  "entity_name": "name",
  "relationship_type": "connected_to|mentioned_with",
  "depth": 2
}
```

#### Cross-Reference
```
POST /search/cross-reference
{
  "document_id": "doc-123",
  "relationship_types": ["cites", "cited_by", "related", "similar"],
  "max_depth": 3
}
```

#### Fact Check
```
POST /search/fact-check
{
  "claim": "statement to verify",
  "context": "additional context",
  "source_types": ["court", "government", "media"]
}
```

## Search Engine Configuration

### Google Custom Search
```yaml
google_search:
  api_key: ${GOOGLE_SEARCH_API_KEY}
  cx: ${GOOGLE_CUSTOM_SEARCH_CX}
  safe_search: off
  num_results: 10
  rate_limit: 100/day
```

### Bing Search API
```yaml
bing_search:
  api_key: ${BING_SEARCH_API_KEY}
  endpoint: https://api.bing.microsoft.com/v7.0/search
  num_results: 10
  rate_limit: 1000/month
```

### DuckDuckGo
```yaml
duckduckgo:
  no_api_key_required: true
  rate_limit: respectful
  safe_search: off
```

### Azure Cognitive Search
```yaml
azure_search:
  api_key: ${AZURE_SEARCH_KEY}
  endpoint: ${AZURE_SEARCH_ENDPOINT}
  index_name: epstein-documents
  scoring_profile: relevance-boost
```

### Internal Elasticsearch
```yaml
elasticsearch:
  hosts: [internal-es-cluster:9200]
  index: epstein-codex
  shards: 5
  replicas: 2
  max_results: 10000
```

## Agent Communication Protocol

### Inter-Agent Search Requests

Agents communicate via internal message queue (RabbitMQ):

```json
{
  "request_id": "uuid",
  "requesting_agent": "document-analysis-agent",
  "search_type": "semantic",
  "query": {
    "text": "search query",
    "filters": {},
    "options": {}
  },
  "priority": "normal|high|urgent",
  "timeout": 30
}
```

### Response Format

```json
{
  "request_id": "uuid",
  "status": "success|partial|failed",
  "results": [
    {
      "document_id": "doc-123",
      "title": "Document Title",
      "relevance_score": 0.95,
      "summary": "...",
      "url": "internal://...",
      "metadata": {}
    }
  ],
  "total_found": 150,
  "search_time_ms": 245,
  "sources_searched": ["elasticsearch", "azure", "google"]
}
```

## Performance Metrics

### Target Performance
- **Search latency:** < 500ms (internal)
- **External API latency:** < 2 seconds
- **Cache hit rate:** > 60%
- **Throughput:** 1000 searches/minute
- **Availability:** 99.9%

### Monitoring
- Query response times
- Cache effectiveness
- API quota usage
- Error rates
- Result quality scores

## Rate Limiting & Quotas

### External APIs
- **Google:** 100 queries/day (free tier)
- **Bing:** 1000 queries/month (free tier)
- **Azure:** Based on subscription
- **Internal:** No limit

### Agent Quotas
- Each agent has search quota based on role
- Critical agents get higher quotas
- Quota resets daily
- Caching reduces quota usage

## Security & Privacy

### Access Control
- Only authenticated AI agents can access search APIs
- Service-to-service authentication
- No public endpoints
- Audit logging of all searches

### Data Protection
- Search queries logged but anonymized
- Results cached with encryption
- No sensitive data in logs
- Compliance with privacy regulations

### Redaction
- Automatic PII redaction in results
- Victim identity protection
- Compliance with court sealing orders

## Caching Strategy

### Multi-Level Cache
1. **L1 Cache:** In-memory (Redis) - 15 minutes TTL
2. **L2 Cache:** Disk cache - 24 hours TTL
3. **L3 Cache:** Result database - 7 days TTL

### Cache Invalidation
- Time-based expiration
- Event-based (new document added)
- Manual invalidation
- LRU eviction

## Search Quality Assurance

### Quality Metrics
- Relevance scoring
- Precision and recall
- User feedback (from agent reports)
- A/B testing of algorithms

### Continuous Improvement
- ML model retraining
- Algorithm optimization
- Index tuning
- Query expansion refinement

## Integration Examples

### Document Analysis Agent Using Search

```python
from search_api import SearchClient

search = SearchClient(service_token=SERVICE_TOKEN)

# Search for related documents
results = search.documents(
    query="Jeffrey Epstein Palm Beach",
    filters={
        "date_range": {"start": "2005-01-01", "end": "2008-12-31"},
        "category": ["legal", "investigation"]
    },
    limit=50
)

for doc in results:
    # Process each document
    analyze_document(doc)
```

### Entity Extraction Agent Using Search

```python
# Find all documents mentioning an entity
entity_docs = search.entities(
    entity_name="Little St. James",
    entity_type="location",
    include_related=True
)

# Build entity profile
profile = build_entity_profile(entity_docs)
```

### Cross-Reference Agent Using Search

```python
# Find all documents connected to a source document
related = search.cross_reference(
    document_id="doc-123",
    relationship_types=["cites", "cited_by", "mentions"],
    max_depth=2
)

# Build citation network
network = build_citation_network(related)
```

## Maintenance

### Daily Tasks
- Index updates
- Cache cleanup
- Performance monitoring
- Error log review

### Weekly Tasks
- Index optimization
- Cache analysis
- Query pattern analysis
- Algorithm tuning

### Monthly Tasks
- Full reindex
- Model retraining
- Capacity planning
- Performance benchmarking

---

**This search infrastructure operates entirely in the background, accessible only to AI agents for maintaining and organizing the Epstein Files Codex.**

*Last Updated: December 2024*
