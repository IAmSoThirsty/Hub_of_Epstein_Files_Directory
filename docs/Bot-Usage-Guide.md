# Epstein Files Hub - Bot Usage Guide

This guide explains how the AI agents work and how to interact with them effectively.

## Overview

The Epstein Files Hub uses **37+ specialized AI agents** (26 GitHub Copilot agents + 11 Python bots) that work 24/7 to maintain and organize over 30,000 documents and 20,000 images.

### Recent Additions (February 2024)
20 new specialized agents have been added to enhance data integration from Uncensored.ai and other sources:
- Flight log analysis and passenger tracking
- Video and audio file processing
- Financial records analysis
- Court document specialization
- News and media monitoring
- Enhanced privacy protection
- Advanced relationship mapping
- And more...

**See the complete agent directory:** `.github/agents/AGENTS_DIRECTORY.md`

## Agent Categories

### 1. Document Management Agents (7 agents)

#### Document Indexing Agent
- **Purpose:** Indexes all incoming documents
- **Capacity:** 6,000 documents/day
- **Features:**
  - Full-text extraction
  - Metadata generation
  - Tag assignment
  - Cross-referencing

#### OCR Processing Agent
- **Purpose:** Converts scanned documents to searchable text
- **Capacity:** 5,000 pages/day
- **Technology:** Azure Document Intelligence
- **Output:** Searchable PDFs with extracted text

#### Document Analysis Agent
- **Purpose:** Deep content analysis
- **Capacity:** 3,000 documents/day
- **Analysis:**
  - Entity extraction (people, places, organizations)
  - Date/timeline extraction
  - Relationship mapping
  - Redaction detection

#### Document Verification Agent
- **Purpose:** Verifies document authenticity
- **Capacity:** 2,000 documents/day
- **Checks:**
  - Source verification
  - Duplicate detection
  - Format validation
  - Metadata consistency

#### Document Summarization Agent
- **Purpose:** Creates document summaries
- **Capacity:** 10,000 documents/day
- **Output:**
  - Brief summary (50-100 words)
  - Key points extraction
  - Important dates and names
  - Relevance scoring

#### Cross-Reference Agent
- **Purpose:** Links related documents
- **Capacity:** 15,000 documents/day
- **Connections:**
  - Same people mentioned
  - Same locations
  - Same time periods
  - Related cases

#### Document Classification Agent
- **Purpose:** Categorizes documents
- **Capacity:** 10,000 documents/day
- **Categories:**
  - Flight logs
  - Court filings
  - Depositions
  - Financial records
  - Property documents
  - Communications

**Total Document Processing Capacity:** 42,000+ operations/day

---

### 2. Image Management Agents (5 agents)

#### Image Indexing Agent
- **Purpose:** Catalogs all images
- **Capacity:** 10,000 images/day
- **Features:**
  - Metadata extraction
  - Tag assignment
  - Location data
  - Timestamp extraction

#### Image Analysis Agent
- **Purpose:** Visual content analysis
- **Capacity:** 5,000 images/day
- **Technology:** Azure Computer Vision
- **Detection:**
  - Objects and scenes
  - Structures and buildings
  - Documents in photos
  - Text in images (OCR)

#### Image Verification Agent
- **Purpose:** Verifies image authenticity
- **Capacity:** 3,000 images/day
- **Checks:**
  - Duplicate detection
  - Manipulation detection
  - Source verification
  - Quality assessment

#### Image Organization Agent
- **Purpose:** Organizes image library
- **Capacity:** 15,000 images/day
- **Actions:**
  - Folder structure maintenance
  - Collection creation
  - Related image grouping
  - Timeline arrangement

#### Image Maintenance Agent
- **Purpose:** Library upkeep
- **Capacity:** 5,000 images/day
- **Tasks:**
  - Broken link checking
  - Format optimization
  - Backup verification
  - Storage management

**Total Image Processing Capacity:** 26,000+ operations/day

---

### 3. Search & Retrieval Agents (3 agents - Backend Only)

#### Web Search Agent
- **Purpose:** Searches external sources for verification
- **Engines:** Google, Bing, DuckDuckGo, Azure Search
- **Usage:** Backend only (AI agents only)
- **Functions:**
  - Fact verification
  - Source discovery
  - News monitoring
  - Related content finding

#### Image Search Agent
- **Purpose:** Finds related images
- **Engines:** Google Images, Bing Images, TinEye
- **Usage:** Backend only (AI agents only)
- **Functions:**
  - Reverse image search
  - Similar image finding
  - Source tracing
  - Duplicate detection

#### Internal Search Agent
- **Purpose:** Searches internal database
- **Technology:** Azure Cognitive Search
- **Features:**
  - Full-text search
  - Semantic search
  - Faceted search
  - Relevance ranking

**Note:** External search engines are NOT exposed to users. Users only access the Internal Search Agent through the web UI.

---

### 4. Quality Control Agents (3 agents)

#### Fact-Checking Agent
- **Purpose:** Verifies facts and claims
- **Process:**
  1. Extract factual claims
  2. Search authoritative sources
  3. Compare and verify
  4. Flag inconsistencies
- **Sources:**
  - Court records
  - Government databases
  - Verified news sources
  - Academic publications

#### Source Verification Agent
- **Purpose:** Validates document sources
- **Checks:**
  - Source authenticity
  - Publication verification
  - Chain of custody
  - Legal compliance
- **Actions:**
  - Assign verification level (1-5)
  - Flag suspicious sources
  - Recommend additional verification

#### Content Moderation Agent
- **Purpose:** Ensures content quality
- **Monitors:**
  - Inappropriate content
  - Unverified claims
  - Duplicate submissions
  - Privacy violations
- **Actions:**
  - Flag for review
  - Auto-reject if clearly inappropriate
  - Notify moderators
  - Log incidents

---

### 5. Organization Agents (4 agents)

#### Collection Management Agent
- **Purpose:** Maintains document collections
- **Functions:**
  - Create thematic collections
  - Update collection metadata
  - Remove outdated items
  - Generate collection summaries

#### Timeline Generation Agent
- **Purpose:** Creates chronological timelines
- **Features:**
  - Extract dates from documents
  - Build event sequences
  - Link related events
  - Generate visual timelines

#### Relationship Mapping Agent
- **Purpose:** Maps connections between entities
- **Outputs:**
  - Person-to-person connections
  - Person-to-location links
  - Organization relationships
  - Timeline of interactions

#### Auto-Tagging Agent
- **Purpose:** Automatically tags content
- **Tags:**
  - People mentioned
  - Locations
  - Organizations
  - Topics
  - Date ranges
  - Document types

---

### 6. Monitoring Agents (2 agents)

#### System Health Agent
- **Purpose:** Monitors system health
- **Checks:**
  - Bot performance
  - Error rates
  - Processing queues
  - Storage capacity
  - API rate limits
- **Alerts:**
  - Critical errors
  - Performance degradation
  - Capacity warnings
  - Service outages

#### Performance Optimization Agent
- **Purpose:** Optimizes system performance
- **Actions:**
  - Identify bottlenecks
  - Adjust processing priorities
  - Optimize database queries
  - Manage caching
  - Balance load

---

### 7. User Support Agents (2 agents)

#### Search Assistant Agent
- **Purpose:** Helps users find information
- **Features:**
  - Query interpretation
  - Search suggestions
  - Related content recommendations
  - Result explanation

#### Help & Documentation Agent
- **Purpose:** Provides user assistance
- **Functions:**
  - Answer common questions
  - Generate help content
  - Provide usage tips
  - Troubleshoot issues

---

## How to Use the Bots

### For End Users

#### Using the Search Feature
1. Go to [Search Page](https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/search.html)
2. Enter your search criteria
3. Internal Search Agent processes your query
4. Results display with relevance scores
5. Click to view full documents

**Search Tips:**
- Use specific keywords for better results
- Filter by date range for focused searches
- Use location filters to narrow results
- Check redaction status filters
- Try advanced filters for precision

#### Uploading Documents
1. Visit [Upload Page](https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/upload.html)
2. Select PDF file(s)
3. **PDF Analysis Agent** automatically analyzes
4. **Document Routing Agent** decides:
   - ≥70% relevance → Accepted & indexed
   - <70% relevance → Rejected & trashed
5. Receive notification of results

**Upload Guidelines:**
- PDFs only
- Maximum 50MB per file
- Must be Epstein-related
- No copyrighted material
- Verifiable sources preferred

### For Contributors

#### Submitting via GitHub
```bash
# 1. Fork repository
git clone https://github.com/YOUR_USERNAME/Hub_of_Epstein_Files_Directory.git

# 2. Add document
cp document.pdf data/uploads/

# 3. Create metadata
cat > data/uploads/document.json << EOF
{
  "title": "Document Title",
  "date": "2024-01-01",
  "source": "Court Records",
  "relevance": "High"
}
EOF

# 4. Commit and push
git add data/uploads/
git commit -m "Add new court filing"
git push origin main

# 5. Create pull request
```

**Automated Processing:**
- GitHub Actions workflow triggers
- PDF Analysis Bot processes document
- If relevant (≥70%), automatically merged
- If uncertain (40-69%), flagged for manual review
- If irrelevant (<40%), rejected with explanation

### For Developers

#### Adding New Bots

```python
# bots/your-new-bot/bot.py

from typing import Dict, Any
from azure.ai import DocumentAnalysisClient

class YourNewBot:
    """
    Description of what this bot does.
    
    Capacity: X operations/day
    Dependencies: Azure service, etc.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # Initialize services
        
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Main processing function.
        
        Args:
            input_data: Input to process
            
        Returns:
            Processing results
        """
        # Implementation
        pass
```

**Steps:**
1. Create bot directory in `bots/`
2. Implement bot class
3. Create README documenting bot
4. Add to `bots/AGENT_INFRASTRUCTURE.md`
5. Create GitHub Actions workflow
6. Write tests
7. Submit PR

#### Monitoring Bot Performance

Check Application Insights:
```bash
# Azure CLI
az monitor metrics list \
  --resource /subscriptions/SUB_ID/resourceGroups/RG/providers/Microsoft.Insights/components/APP_INSIGHTS \
  --metric-names requests/count \
  --aggregation Average
```

Dashboard available at: [Monitor Dashboard](https://portal.azure.com)

---

## Bot Coordination

Agents work together in workflows:

### Document Upload Workflow
1. **Upload** → PDF Analysis Bot
2. **Analysis** → Document Routing Bot
3. If accepted:
   - **OCR** → OCR Processing Agent
   - **Index** → Document Indexing Agent
   - **Analyze** → Document Analysis Agent
   - **Verify** → Document Verification Agent
   - **Summarize** → Summarization Agent
   - **Link** → Cross-Reference Agent
   - **Classify** → Classification Agent
4. **Complete** → Notification

### Image Upload Workflow
1. **Upload** → Image Analysis Bot
2. **Analysis** → Image Routing Bot
3. If accepted:
   - **Index** → Image Indexing Agent
   - **Analyze** → Image Analysis Agent
   - **Verify** → Image Verification Agent
   - **Organize** → Organization Agent
4. **Complete** → Notification

### Search Query Workflow
1. **Query** → Search Assistant Agent
2. **Process** → Internal Search Agent
3. **Rank** → Relevance Scoring
4. **Results** → User Interface

---

## Troubleshooting

### Bot Not Processing

**Check:**
1. GitHub Actions status
2. Azure service health
3. Processing queue length
4. Error logs in App Insights

**Solution:**
- Restart workflow
- Check API limits
- Review error messages
- Contact maintainers

### Slow Processing

**Causes:**
- High queue length
- API rate limits
- Service degradation
- Large file size

**Solution:**
- Wait for queue to clear
- Upload smaller batches
- Try during off-peak hours

### Document Rejected

**Reasons:**
- Relevance score < 70%
- Duplicate detected
- Invalid format
- Copyright issue

**Solution:**
- Check relevance criteria
- Verify it's unique content
- Ensure proper PDF format
- Confirm source rights

---

## API Documentation

For developers integrating with the system:

### Search API
```http
GET /api/search?q=query&type=document&from=0&size=20
```

### Upload API
```http
POST /api/upload
Content-Type: multipart/form-data

file: <binary data>
metadata: <json>
```

### Status API
```http
GET /api/status/{upload_id}
```

Full API docs: [API Documentation](docs/API.md)

---

## Best Practices

1. **Upload Guidelines:**
   - Verify documents before uploading
   - Include source information
   - Use descriptive filenames
   - Check for duplicates first

2. **Search Tips:**
   - Start broad, then refine
   - Use filters effectively
   - Check related documents
   - Review source verification levels

3. **Contributing:**
   - Follow contribution guidelines
   - Test before submitting
   - Document your changes
   - Be patient with review process

---

## Support

- **Documentation:** Check this guide and other docs
- **Issues:** Open GitHub issue
- **Questions:** Use GitHub Discussions
- **Urgent:** Email maintainers (see README)

---

**Last Updated:** December 2024
