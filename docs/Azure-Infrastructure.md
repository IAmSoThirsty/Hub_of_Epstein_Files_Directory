# Azure Infrastructure Setup

This document outlines the Azure services and configuration required for the Epstein Files Codex infrastructure.

## Azure Services Required

### 1. Azure Cognitive Search
**Purpose:** Primary search engine for documents and images (backend AI agents only)

**Configuration:**
- Service Tier: Standard S1 or higher
- Indexes:
  - `documents-index` (30,000+ documents)
  - `images-index` (20,000+ images)
  - `entities-index` (people, locations, organizations)
- Features to Enable:
  - Semantic Search
  - AI Enrichment
  - Custom Skills
  - Synonym Maps

**Estimated Cost:** ~$250/month (S1 tier)

### 2. Azure Computer Vision
**Purpose:** Image analysis, OCR, and facial recognition

**Configuration:**
- Service: Computer Vision API
- Features Used:
  - OCR (Optical Character Recognition)
  - Image Analysis
  - Face Detection (with privacy compliance)
  - Object Detection
  - Image Categorization

**Estimated Cost:** ~$100/month (20K images/month)

### 3. Azure Document Intelligence (Form Recognizer)
**Purpose:** PDF analysis and document understanding

**Configuration:**
- Service: Form Recognizer / Document Intelligence
- Models:
  - Prebuilt Document Model
  - Custom Model (trained on legal documents)
- Features:
  - Layout Analysis
  - Key-Value Pair Extraction
  - Table Extraction
  - Redaction Detection

**Estimated Cost:** ~$150/month (30K documents/month)

### 4. Azure OpenAI Service
**Purpose:** Advanced AI analysis, summarization, and relevance scoring

**Configuration:**
- Model Deployments:
  - GPT-4 (for complex analysis)
  - GPT-3.5-turbo (for summarization)
  - text-embedding-ada-002 (for semantic search)
- Rate Limits:
  - GPT-4: 100K tokens/minute
  - GPT-3.5: 240K tokens/minute

**Estimated Cost:** ~$500/month (high volume)

### 5. Azure Blob Storage
**Purpose:** Document and image storage

**Configuration:**
- Storage Type: Hot tier (LRS)
- Containers:
  - `documents` (30K+ PDFs)
  - `images` (20K+ photos)
  - `trash` (rejected uploads)
  - `indexed` (accepted uploads)
- Features:
  - Lifecycle Management
  - Soft Delete (30 days)
  - Versioning Enabled

**Estimated Cost:** ~$50/month (500 GB storage + operations)

### 6. Azure Functions
**Purpose:** Serverless compute for bot operations

**Configuration:**
- Plan: Premium EP1
- Functions:
  - PDF Analysis Bot
  - Image Analysis Bot
  - Document Indexing Bot
  - Fact-Checking Bot
  - Source Verification Bot
- Runtime: Python 3.11

**Estimated Cost:** ~$200/month (EP1 plan)

### 7. Azure App Service
**Purpose:** Host web application

**Configuration:**
- Service Plan: B2 (Basic)
- Runtime: Static HTML/CSS/JS
- Features:
  - Custom Domain Support
  - SSL Certificate (Let's Encrypt)
  - GitHub Actions Deployment

**Estimated Cost:** ~$55/month (B2 tier)

Alternatively, use **GitHub Pages** (Free) for static hosting.

### 8. Azure DevOps
**Purpose:** CI/CD pipelines and self-hosted runners

**Configuration:**
- Self-hosted agents: 2-3 agents
- Pipelines:
  - PDF Processing Pipeline
  - Image Processing Pipeline
  - Website Deployment Pipeline
  - Agent Health Monitoring

**Estimated Cost:** Free for public projects, ~$40/month for additional pipeline minutes

### 9. Azure Monitor & Application Insights
**Purpose:** Monitoring, logging, and alerting

**Configuration:**
- Application Insights for:
  - Bot performance monitoring
  - Error tracking
  - Usage analytics
- Log Analytics Workspace
- Alerts:
  - Bot failures
  - High error rates
  - Storage capacity warnings

**Estimated Cost:** ~$50/month

### 10. Azure Key Vault
**Purpose:** Secure storage of API keys, connection strings, and secrets

**Configuration:**
- Standard tier
- Secrets:
  - Storage connection strings
  - API keys (OpenAI, Computer Vision, etc.)
  - Search service keys
  - Third-party API keys (Google, Bing)

**Estimated Cost:** ~$5/month

## Total Estimated Cost

**Monthly Azure Infrastructure Cost: ~$1,360**

Breakdown:
- Cognitive Search: $250
- Computer Vision: $100
- Document Intelligence: $150
- OpenAI Service: $500
- Blob Storage: $50
- Functions: $200
- App Service: $55 (or $0 with GitHub Pages)
- DevOps: $40
- Monitor: $50
- Key Vault: $5

**Annual Cost: ~$16,320**

## Cost Optimization Options

1. **Use GitHub Pages** instead of App Service (saves $55/month)
2. **Reduce OpenAI usage** with caching and batch processing (save ~$200/month)
3. **Use consumption plan** for Functions instead of Premium (save ~$150/month)
4. **Archive old documents** to Cool/Archive storage (save ~$30/month)

**Optimized Monthly Cost: ~$1,100**

## Deployment Steps

### Step 1: Create Azure Resources

```bash
# Login to Azure
az login

# Create resource group
az group create --name epstein-files-rg --location eastus

# Create Storage Account
az storage account create \
  --name epsteinfilesstorage \
  --resource-group epstein-files-rg \
  --location eastus \
  --sku Standard_LRS

# Create Cognitive Search
az search service create \
  --name epstein-files-search \
  --resource-group epstein-files-rg \
  --location eastus \
  --sku standard

# Create Computer Vision
az cognitiveservices account create \
  --name epstein-files-vision \
  --resource-group epstein-files-rg \
  --kind ComputerVision \
  --sku S1 \
  --location eastus

# Create Form Recognizer
az cognitiveservices account create \
  --name epstein-files-forms \
  --resource-group epstein-files-rg \
  --kind FormRecognizer \
  --sku S0 \
  --location eastus

# Create OpenAI Service (requires special access)
az cognitiveservices account create \
  --name epstein-files-openai \
  --resource-group epstein-files-rg \
  --kind OpenAI \
  --sku S0 \
  --location eastus

# Create Key Vault
az keyvault create \
  --name epstein-files-kv \
  --resource-group epstein-files-rg \
  --location eastus
```

### Step 2: Configure Services

See individual configuration files in:
- `.azure/cognitive-search-config.json`
- `.azure/function-app-config.json`
- `.azure/storage-config.json`

### Step 3: Deploy Functions

```bash
# Deploy Azure Functions
cd bots
func azure functionapp publish epstein-files-functions
```

### Step 4: Configure GitHub Actions

Update secrets in GitHub repository:
- `AZURE_CREDENTIALS`
- `AZURE_STORAGE_CONNECTION_STRING`
- `AZURE_SEARCH_ENDPOINT`
- `AZURE_SEARCH_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_VISION_ENDPOINT`
- `AZURE_VISION_API_KEY`

### Step 5: Deploy Website

**Option A: Azure App Service**
```bash
az webapp up --name epstein-files-hub --resource-group epstein-files-rg
```

**Option B: GitHub Pages** (Recommended for cost savings)
- Enable GitHub Pages in repository settings
- Set source to `gh-pages` branch or `docs/` folder
- Configure custom domain (optional)

## Monitoring & Maintenance

### Health Checks
- Monitor Application Insights dashboard
- Set up alerts for:
  - Function failures
  - High latency
  - Storage capacity > 80%
  - Search index size

### Automated Tasks
- Daily: Index health check
- Weekly: Storage cleanup (trash container)
- Monthly: Cost analysis and optimization review

### Security
- Rotate API keys every 90 days
- Review access logs monthly
- Enable Azure AD authentication for admin access
- Use managed identities where possible

## Alternative Free/Low-Cost Setup

For development or low-budget deployments:

1. **GitHub Pages** - Free static hosting
2. **Vercel/Netlify** - Free serverless functions (limited)
3. **Cloudflare Workers** - Free tier for light processing
4. **Local Search** - Use client-side search (Lunr.js, Fuse.js)
5. **GitHub Actions** - Free CI/CD for public repos

**Estimated Cost: $0-50/month** (API usage only)

## Next Steps

1. [ ] Create Azure subscription (if not exists)
2. [ ] Run deployment scripts
3. [ ] Configure services
4. [ ] Test bot functionality
5. [ ] Deploy website
6. [ ] Configure monitoring
7. [ ] Set up alerts
8. [ ] Document operational procedures
