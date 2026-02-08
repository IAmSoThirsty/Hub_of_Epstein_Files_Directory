# AI Agents Directory - Complete List

This document provides a comprehensive directory of all 26+ AI agents working on the Epstein Files Hub.

## Overview

The Epstein Files Hub utilizes a sophisticated network of specialized AI agents that work together to organize, analyze, and maintain the extensive collection of documents, images, videos, and other files.

**Total Active Agents:** 26+ GitHub Copilot Agents + 11 Bot Infrastructure Agents = **37+ Total Agents**

---

## GitHub Copilot Agents (26)

These agents are configured as GitHub Copilot custom agents and can be invoked to help with specific tasks.

### Data Integration & Ingestion (5 agents)

#### 1. Uncensored.ai Integration Agent
**Purpose:** Primary data integration from Uncensored.ai free database
- Fetches documents, images, videos from external sources
- Handles format conversion and deduplication
- Ensures data quality and integrity

#### 2. API Integration Coordinator
**Purpose:** Manages all external API connections
- Handles authentication and rate limiting
- Syncs data with multiple external sources
- Monitors API performance and errors

#### 3. Document Classifier
**Purpose:** Auto-categorizes incoming documents
- Identifies document types (legal, financial, media, etc.)
- Assigns relevance scores
- Routes to appropriate processing agents

#### 4. Batch Processing Manager
**Purpose:** Manages large-scale bulk operations
- Coordinates mass file processing
- Tracks progress and handles errors
- Optimizes resource utilization

#### 5. Workflow Orchestrator
**Purpose:** Coordinates all agent activities
- Designs and manages processing workflows
- Load balances across agents
- Handles priorities and dependencies

### Media Processing (5 agents)

#### 6. Photo Collection Organizer
**Purpose:** Manages extensive photo collection
- Catalogs and organizes photos
- Extracts EXIF metadata
- Creates intelligent collections

#### 7. Video Archive Manager
**Purpose:** Manages video file library
- Indexes and catalogs videos
- Generates thumbnails and metadata
- Handles multiple video formats

#### 8. Audio File Processor
**Purpose:** Processes and transcribes audio
- Converts speech to text
- Identifies speakers
- Extracts key content

#### 9. Media Metadata Extractor
**Purpose:** Extracts comprehensive metadata from all media
- EXIF data from images
- Technical specs from videos/audio
- Forensic analysis capabilities

#### 10. Image Analysis Bot
**Purpose:** Advanced image content analysis
- Object detection and recognition
- OCR for text in images
- Quality assessment

### Flight Logs & Location (3 agents)

#### 11. Flight Log Analyzer
**Purpose:** Parses and analyzes aviation records
- Extracts passenger lists and routes
- Tracks flight patterns
- Creates flight databases

#### 12. Passenger Correlator
**Purpose:** Cross-references passengers across flights
- Identifies frequent travelers
- Maps co-traveler relationships
- Detects travel patterns

#### 13. Location Tracker
**Purpose:** Maps and tracks all locations
- Geocodes addresses
- Creates location databases
- Generates maps and visualizations

### Document Analysis (4 agents)

#### 14. Court Document Specialist
**Purpose:** Processes legal documents
- Handles court filings and depositions
- Generates legal citations
- Tracks case progression

#### 15. Financial Records Analyst
**Purpose:** Analyzes financial documents
- Tracks transactions and assets
- Maps financial networks
- Identifies suspicious patterns

#### 16. Redaction Detector
**Purpose:** Identifies redacted content
- Detects black boxes and redactions
- Analyzes redaction patterns
- Categorizes redaction types

#### 17. News & Media Monitor
**Purpose:** Tracks news coverage
- Monitors media outlets
- Verifies claims against documents
- Analyzes sentiment and coverage

### Data Quality & Integrity (5 agents)

#### 18. Quality Assessor
**Purpose:** Evaluates file quality
- Scores documents and media
- Identifies quality issues
- Recommends improvements

#### 19. Data Validator
**Purpose:** Validates data integrity
- Checks consistency across sources
- Verifies data accuracy
- Flags errors and inconsistencies

#### 20. Duplicate Detector
**Purpose:** Identifies duplicate files
- Uses hashing algorithms
- Detects near-duplicates
- Recommends deduplication actions

#### 21. Source Attributor
**Purpose:** Tracks file provenance
- Documents source information
- Maintains chain of custody
- Generates proper citations

#### 22. Privacy Protector
**Purpose:** Ensures victim privacy compliance
- Identifies sensitive information
- Manages redaction requirements
- Monitors legal compliance

### Analysis & Intelligence (4 agents)

#### 23. Relationship Mapper
**Purpose:** Builds entity relationship graphs
- Maps connections between people, places, events
- Creates network visualizations
- Identifies patterns and clusters

#### 24. DateTime Extractor
**Purpose:** Extracts temporal data
- Identifies dates and times
- Normalizes date formats
- Builds timelines

#### 25. Report Generator
**Purpose:** Creates comprehensive reports
- Generates statistical analyses
- Creates visualizations
- Produces custom reports

#### 26. The Butler (My Agent)
**Purpose:** General purpose assistant
- Coordinates with other agents
- Creates additional agents as needed
- Ensures harmonious teamwork

### System Maintenance (1 agent)

#### 27. Archive Maintainer
**Purpose:** Long-term archive health
- Monitors file integrity
- Manages backups
- Optimizes storage

---

## Bot Infrastructure Agents (11)

These are Python-based bots in the `/bots` directory that perform automated tasks.

### 1. PDF Analysis Bot
- Analyzes uploaded PDFs
- Content relevance scoring
- Automatic filing or trash routing

### 2. Search Bot
- Multi-engine search (Google, Bing, DuckDuckGo)
- Full-text search capabilities
- Advanced filtering

### 3. Summarization Bot
- Document summarization
- Key points extraction
- Multi-document synthesis

### 4. Cross-Reference Bot
- Identifies document connections
- Entity co-occurrence detection
- Citation tracking

### 5. Timeline Bot
- Creates chronological timelines
- Extracts dates from documents
- Multi-source correlation

### 6. Entity Extraction Bot
- Named entity recognition
- Character directory updates
- Relationship mapping

### 7. Fact-Checking Bot
- Source verification
- Cross-reference checking
- Credibility scoring

### 8. Indexing Bot
- Automatic categorization
- Metadata extraction
- Search index maintenance

### 9. Verification Bot
- Document authenticity checking
- Source validation
- Provenance tracking

### 10. Audit Bot
- System-wide auditing
- Health monitoring
- Issue detection

### 11. Image Analysis Bot (duplicate with Copilot agent)
- Image recognition
- Metadata extraction
- Reverse image search

---

## Agent Collaboration

### Primary Workflows

**New Document Ingestion:**
```
Document Classifier → Court/Financial Specialist → 
Entity Extraction → Relationship Mapper → 
Timeline Generator → Quality Assessor → 
Privacy Protector → Source Attributor → Indexing
```

**Media Processing:**
```
Media Type Detection → Photo/Video/Audio Processor →
Metadata Extractor → Quality Assessor →
Duplicate Detector → Archive Manager
```

**Flight Log Processing:**
```
Flight Log Analyzer → Passenger Correlator →
Location Tracker → Relationship Mapper →
Timeline Integration
```

**External Data Integration:**
```
API Integration Coordinator → Uncensored.ai Agent →
Document Classifier → Batch Processor →
Quality Pipeline → Final Integration
```

### Agent Communication

All agents are coordinated by the **Workflow Orchestrator** which:
- Routes tasks efficiently
- Manages priorities
- Handles errors and retries
- Balances workload
- Tracks progress

---

## Capacity Summary

| Category | Agents | Daily Capacity |
|----------|--------|----------------|
| Document Processing | 8 | 50,000+ documents |
| Media Processing | 5 | 30,000+ files |
| Flight Logs | 3 | 1,000+ manifests |
| Quality & Validation | 5 | Full collection scan |
| Integration & Sync | 3 | Continuous |
| Analysis & Reporting | 4 | On-demand |
| System Maintenance | 3 | Continuous |

**Total System Capacity:** 100,000+ operations per day

---

## Adding New Agents

To add a new agent:

1. Create a new `.agent.md` file in `.github/agents/`
2. Define the agent's name, description, and responsibilities
3. Integrate with the Workflow Orchestrator
4. Update this directory
5. Test the agent configuration

---

## Documentation

For detailed information about specific agents, see:
- Individual agent files in `.github/agents/`
- `/bots/README.md` for bot infrastructure
- `/bots/AGENT_INFRASTRUCTURE.md` for technical details

---

**Last Updated:** 2024-02-08
**Status:** ✅ All agents operational
**Total Agents:** 37+ (26 Copilot + 11 Bots)
