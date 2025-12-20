# Azure Cost Reduction Guide

This document provides strategies to significantly reduce Azure infrastructure costs while maintaining functionality for the Epstein Files Hub.

## Cost Comparison

| Deployment Tier | Monthly Cost | Annual Cost | Capabilities |
|----------------|--------------|-------------|--------------|
| **Full Production** | $1,360 | $16,320 | All features, high performance |
| **Optimized** | $675 | $8,100 | 50% cost reduction, good performance |
| **Budget** | $200 | $2,400 | 85% cost reduction, adequate performance |
| **Minimal/Free** | $0-50 | $0-600 | 96%+ cost reduction, basic features |

---

## 🎯 Optimized Tier ($675/month - 50% reduction)

### Key Changes
1. **Downgrade service tiers** where possible
2. **Use consumption plans** instead of dedicated plans
3. **Implement aggressive caching** to reduce API calls
4. **Use GitHub Pages** for free hosting
5. **Batch process** to reduce operations

### Service Breakdown

#### 1. Azure Cognitive Search: $250 → $75 (-70%)
**Changes:**
- Downgrade from Standard S1 to Basic tier
- Use partitioning to handle 30K docs + 20K images
- Implement client-side search for simple queries
- Cache frequent search results (Redis free tier)

```bash
# Create Basic tier search service
az search service create \
  --name epstein-files-search \
  --resource-group epstein-files-rg \
  --sku basic
```

**Limitations:**
- Max 15GB storage (sufficient for metadata indexing)
- 3 replicas max
- No semantic search (use keyword search instead)

---

#### 2. Azure Computer Vision: $100 → $30 (-70%)
**Changes:**
- Use Free tier (5K images/month) for initial processing
- Batch images to reduce transaction count
- Cache analysis results in database
- Only analyze new/modified images

```python
# Batch image processing example
def batch_process_images(images, batch_size=50):
    """Process images in batches to reduce API calls"""
    results = []
    for i in range(0, len(images), batch_size):
        batch = images[i:i+batch_size]
        # Process batch once, cache results
        result = vision_client.analyze_batch(batch)
        cache_results(result)
        results.extend(result)
    return results
```

**Free Tier:**
- 5,000 transactions/month free
- Additional: $1/1,000 transactions

---

#### 3. Azure Document Intelligence: $150 → $50 (-67%)
**Changes:**
- Use Free tier (500 pages/month) for testing
- Process only new uploads, not entire archive
- Use standard OCR (Computer Vision) for simple docs
- Reserve Form Recognizer for complex legal documents

```python
# Selective document processing
def should_use_form_recognizer(doc):
    """Determine if document needs advanced processing"""
    # Use basic OCR for simple text documents
    if doc.is_text_only and not doc.has_tables:
        return False
    # Use Form Recognizer for complex legal docs
    return doc.is_legal or doc.has_complex_layout
```

**Cost:**
- Free tier: 500 pages/month
- Additional: $1/1,000 pages (process ~50K pages = $50)

---

#### 4. Azure OpenAI Service: $500 → $150 (-70%)
**Changes:**
- Use GPT-3.5-turbo instead of GPT-4 (10x cheaper)
- Aggressive prompt caching
- Pre-compute summaries, store in database
- Use OpenAI only for new content analysis

```python
# Cost-effective AI usage
class CostOptimizedAI:
    def __init__(self):
        self.cache = redis.Redis()
        
    def analyze_document(self, doc_id, text):
        # Check cache first
        cache_key = f"analysis:{doc_id}"
        if cached := self.cache.get(cache_key):
            return cached
            
        # Use cheaper model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Not gpt-4
            messages=[{"role": "user", "content": f"Analyze: {text[:2000]}"}],
            max_tokens=500  # Limit response length
        )
        
        # Cache for 30 days
        self.cache.setex(cache_key, 2592000, response)
        return response
```

**Pricing:**
- GPT-3.5-turbo: $0.0015/1K tokens (vs GPT-4: $0.03/1K tokens)
- Process 100M tokens/month = $150 (vs $3,000 with GPT-4)

---

#### 5. Azure Blob Storage: $50 → $20 (-60%)
**Changes:**
- Move old files to Cool storage ($0.01/GB vs $0.018/GB)
- Archive infrequently accessed files ($0.00099/GB)
- Enable lifecycle management policies
- Compress files before storage

```bash
# Lifecycle management policy
az storage account management-policy create \
  --account-name epsteinfilesstorage \
  --policy '{
    "rules": [{
      "name": "moveToCool",
      "type": "Lifecycle",
      "definition": {
        "actions": {
          "baseBlob": {
            "tierToCool": {"daysAfterModificationGreaterThan": 30},
            "tierToArchive": {"daysAfterModificationGreaterThan": 90}
          }
        }
      }
    }]
  }'
```

**Storage Breakdown:**
- Hot tier (50GB recent files): $0.90
- Cool tier (300GB older files): $3.00
- Archive tier (150GB rarely accessed): $0.50
- Operations: ~$15/month

---

#### 6. Azure Functions: $200 → $50 (-75%)
**Changes:**
- Switch from Premium EP1 to Consumption plan
- Only pay for execution time
- Use GitHub Actions for scheduled tasks (free)
- Optimize function execution time

```yaml
# GitHub Actions for scheduled tasks (FREE)
name: Daily Maintenance
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily
jobs:
  maintenance:
    runs-on: ubuntu-latest
    steps:
      - name: Run cleanup
        run: |
          # Index health check
          python scripts/check_index.py
          # Storage cleanup
          python scripts/cleanup_trash.py
```

**Consumption Plan Pricing:**
- First 1M executions: Free
- Additional: $0.20/million executions
- Execution time: $0.000016/GB-s

**Estimated Usage:**
- 2M executions/month: $0.20
- 50,000 GB-s: $0.80
- Total: ~$50/month

---

#### 7. App Service: $55 → $0 (FREE with GitHub Pages)
**Changes:**
- Use GitHub Pages for static hosting (FREE)
- No server costs
- Fast CDN delivery
- Automatic HTTPS

```yaml
# .github/workflows/deploy-pages.yml (already created)
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./web
```

**Cost: $0** (GitHub Pages is free for public repos)

---

#### 8. Azure DevOps: $40 → $0 (FREE)
**Changes:**
- Use GitHub Actions instead (free for public repos)
- Unlimited minutes for public repositories
- 2,000 minutes/month for private repos

**Cost: $0** (public repo)

---

#### 9. Azure Monitor: $50 → $0 (FREE tier)
**Changes:**
- Use Application Insights free tier (5GB/month)
- Reduce log retention to 30 days
- Sample telemetry data (10% sampling)

```javascript
// Application Insights with sampling
const appInsights = require('applicationinsights');
appInsights.setup(process.env.APPINSIGHTS_KEY)
  .setAutoCollectConsole(true, false)
  .setAutoCollectExceptions(true)
  .setUseDiskRetryCaching(true)
  .setSendLiveMetrics(false)  // Disable live metrics
  .setDistributedTracingMode(appInsights.DistributedTracingModes.AI_AND_W3C);

// Enable sampling
appInsights.defaultClient.config.samplingPercentage = 10;
appInsights.start();
```

**Cost: $0** (within free tier limits)

---

#### 10. Azure Key Vault: $5 → $5 (unchanged)
**Cost: $5** (minimal cost, essential for security)

---

### Optimized Total: $675/month (50% reduction)

| Service | Original | Optimized | Savings |
|---------|----------|-----------|---------|
| Cognitive Search | $250 | $75 | -$175 |
| Computer Vision | $100 | $30 | -$70 |
| Document Intelligence | $150 | $50 | -$100 |
| OpenAI Service | $500 | $150 | -$350 |
| Blob Storage | $50 | $20 | -$30 |
| Functions | $200 | $50 | -$150 |
| App Service | $55 | $0 | -$55 |
| DevOps | $40 | $0 | -$40 |
| Monitor | $50 | $0 | -$50 |
| Key Vault | $5 | $5 | $0 |
| **TOTAL** | **$1,360** | **$675** | **-$685 (50%)** |

---

## 💰 Budget Tier ($200/month - 85% reduction)

### Aggressive Cost Cutting

#### Strategy
1. **Use free tiers extensively**
2. **Client-side processing** where possible
3. **Manual uploads** instead of automated analysis
4. **Static data** with periodic updates

#### Service Configuration

| Service | Cost | Strategy |
|---------|------|----------|
| **Storage** | $20 | Archive tier for most files |
| **Search** | $0 | Client-side search (Lunr.js) |
| **AI Services** | $100 | Free tiers + minimal paid usage |
| **Hosting** | $0 | GitHub Pages |
| **Functions** | $50 | Consumption plan, minimal use |
| **Other** | $30 | Key Vault, networking |
| **TOTAL** | **$200** | **85% reduction** |

#### Implementation

**1. Client-Side Search (Free)**
```html
<!-- Use Lunr.js for client-side search -->
<script src="https://unpkg.com/lunr/lunr.js"></script>
<script>
// Build search index from static JSON
fetch('data/search-index.json')
  .then(res => res.json())
  .then(documents => {
    const idx = lunr(function() {
      this.ref('id')
      this.field('title')
      this.field('content')
      this.field('location')
      
      documents.forEach(doc => this.add(doc))
    })
    
    // Search functionality
    window.search = (query) => idx.search(query)
  })
</script>
```

**2. Pre-compute Everything**
- Run AI analysis once, store results
- Generate static search index
- Pre-render all pages
- Update weekly/monthly instead of real-time

**3. Minimal Azure Services**
- Keep only essential services
- Use free tiers for everything possible
- Batch process new uploads manually

---

## 🆓 Minimal/Free Tier ($0-50/month - 96% reduction)

### Complete Free/Low-Cost Stack

#### Architecture
1. **GitHub Pages** - Static hosting (FREE)
2. **GitHub Actions** - CI/CD (FREE for public repos)
3. **Cloudflare** - CDN, DDoS protection, SSL (FREE)
4. **Supabase** - Database (FREE tier: 500MB)
5. **Vercel** - Serverless functions (FREE tier: 100GB bandwidth)
6. **Algolia** - Search (FREE tier: 10K searches/month)

#### Service Breakdown

| Service | Provider | Cost | Limits |
|---------|----------|------|--------|
| **Hosting** | GitHub Pages | $0 | 100GB bandwidth/month |
| **Database** | Supabase | $0 | 500MB storage, 2GB bandwidth |
| **Search** | Algolia Free | $0 | 10K searches/month |
| **Functions** | Vercel/Cloudflare | $0 | 100K requests/day |
| **CDN/SSL** | Cloudflare | $0 | Unlimited bandwidth |
| **CI/CD** | GitHub Actions | $0 | Public repos |
| **Storage** | GitHub LFS | $0 | 1GB (or use external) |
| **Email** | SendGrid Free | $0 | 100 emails/day |
| **API Usage** | Various free tiers | $0-50 | Light usage |
| **TOTAL** | | **$0-50** | **96%+ reduction** |

#### Implementation Guide

**1. Static Site Generation**
```bash
# Generate static site with all data embedded
npm install -g @11ty/eleventy

# Build site with pre-computed data
eleventy --input=web --output=dist
```

**2. Deploy to GitHub Pages**
```yaml
# .github/workflows/deploy.yml
name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: npm run build
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

**3. Add Cloudflare for Performance**
- Free SSL certificate
- Global CDN
- DDoS protection
- Caching rules
- No cost

**4. Use Algolia for Search**
```javascript
// Free tier: 10K searches/month
const algoliasearch = require('algoliasearch');
const client = algoliasearch('APP_ID', 'API_KEY');
const index = client.initIndex('epstein-files');

// Upload data once
index.saveObjects([
  {
    objectID: 'doc1',
    title: 'Flight Log Entry',
    date: '1999-12-15',
    location: 'Little St. James',
    content: '...'
  }
  // ... more documents
]);

// Search
index.search('Little St. James').then(({ hits }) => {
  console.log(hits);
});
```

**5. Alternative: Client-Side Search**
```javascript
// Use Fuse.js for fuzzy search (completely free)
const fuse = new Fuse(documents, {
  keys: ['title', 'content', 'location', 'people'],
  threshold: 0.3
});

const results = fuse.search('Ghislaine Maxwell');
```

---

## 🔧 Cost Optimization Best Practices

### 1. Caching Strategy
```python
# Multi-layer caching
import redis
import functools

# Redis for distributed cache
redis_client = redis.Redis()

def cached(ttl=3600):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            
            # Check cache
            if cached := redis_client.get(key):
                return cached
                
            # Compute and cache
            result = func(*args, **kwargs)
            redis_client.setex(key, ttl, result)
            return result
        return wrapper
    return decorator

@cached(ttl=86400)  # Cache for 24 hours
def expensive_ai_call(text):
    return openai.complete(text)
```

### 2. Batch Processing
```python
# Process in batches to reduce costs
def process_documents_efficiently(docs):
    # Group by similarity to reduce redundant processing
    batches = group_similar_docs(docs, batch_size=50)
    
    for batch in batches:
        # Process batch once
        results = batch_process(batch)
        
        # Cache results
        for doc, result in zip(batch, results):
            cache.set(doc.id, result, ttl=2592000)  # 30 days
```

### 3. Resource Monitoring
```python
# Track costs in real-time
class CostMonitor:
    def __init__(self):
        self.costs = {
            'openai': 0,
            'vision': 0,
            'search': 0
        }
        
    def log_api_call(self, service, cost):
        self.costs[service] += cost
        
        # Alert if over budget
        if sum(self.costs.values()) > MONTHLY_BUDGET:
            send_alert("Cost threshold exceeded!")
            
    def get_projection(self):
        days_in_month = 30
        days_elapsed = datetime.now().day
        current_cost = sum(self.costs.values())
        
        return current_cost / days_elapsed * days_in_month
```

### 4. Smart Indexing
```python
# Only index new/changed documents
def should_reindex(doc):
    last_indexed = get_last_index_time(doc.id)
    
    if not last_indexed:
        return True
        
    if doc.modified > last_indexed:
        return True
        
    return False

# Incremental indexing
def incremental_index():
    docs_to_index = [doc for doc in all_docs if should_reindex(doc)]
    
    if docs_to_index:
        search_client.index_documents(docs_to_index)
```

---

## 📊 Cost Reduction Roadmap

### Phase 1: Immediate (Save $350/month)
- ✅ Switch to GitHub Pages hosting (-$55)
- ✅ Use GitHub Actions instead of Azure DevOps (-$40)
- ✅ Move to Consumption plan for Functions (-$150)
- ✅ Implement basic caching (-$100 in AI costs)
- **Total Savings: $350/month**

### Phase 2: Short-term (Save additional $335/month)
- ⏳ Downgrade Cognitive Search to Basic (-$175)
- ⏳ Use Computer Vision free tier + batching (-$70)
- ⏳ Switch to GPT-3.5-turbo (-$200)
- ⏳ Use Application Insights free tier (-$50)
- ⏳ Archive old files to Cool storage (-$30)
- **Additional Savings: $335/month**
- **Total: $685/month (50% reduction)**

### Phase 3: Medium-term (Save additional $475/month)
- 🔄 Implement client-side search with Lunr.js (-$75)
- 🔄 Pre-compute all AI analysis, store results (-$150)
- 🔄 Use Form Recognizer only for complex docs (-$100)
- 🔄 Minimize Computer Vision usage (-$30)
- 🔄 Reduce Functions usage with smart batching (-$50)
- **Additional Savings: $475/month**
- **Total: $1,160/month (85% reduction)**

### Phase 4: Long-term (Go nearly free)
- 🚀 Move to completely static architecture
- 🚀 Use Algolia free tier or client-side search
- 🚀 Pre-generate all data monthly
- 🚀 Use only free services
- **Final Cost: $0-50/month (96%+ reduction)**

---

## 💡 Recommendations

### For Production Launch
**Recommended: Optimized Tier ($675/month)**
- 50% cost reduction
- Maintains good performance
- All core features intact
- Scalable for growth

### For Development/Testing
**Recommended: Budget Tier ($200/month)**
- 85% cost reduction
- Adequate for testing
- Easy to scale up later

### For Personal/Community Project
**Recommended: Free Tier ($0-50/month)**
- 96%+ cost reduction
- Static site, very fast
- No recurring costs
- Perfect for public archives

---

## 🎯 Quick Start: Implement Optimized Tier

### Step 1: Update Azure Resources
```bash
# Downgrade search to Basic
az search service update \
  --name epstein-files-search \
  --resource-group epstein-files-rg \
  --sku basic

# Switch Functions to Consumption plan
az functionapp create \
  --name epstein-files-functions \
  --resource-group epstein-files-rg \
  --consumption-plan-location eastus \
  --storage-account epsteinfilesstorage

# Configure lifecycle management
az storage account management-policy create \
  --account-name epsteinfilesstorage \
  --policy @lifecycle-policy.json
```

### Step 2: Update Code for Efficiency
```python
# Use GPT-3.5 instead of GPT-4
# Add caching layer
# Batch operations
# See code examples above
```

### Step 3: Enable GitHub Pages
```bash
# Already configured in .github/workflows/deploy-pages.yml
# Just enable in repo settings
```

### Step 4: Monitor Costs
```bash
# Set up cost alerts
az monitor action-group create \
  --name cost-alerts \
  --resource-group epstein-files-rg \
  --action email admin@example.com

# Create budget alert
az consumption budget create \
  --name monthly-budget \
  --amount 700 \
  --time-grain Monthly \
  --resource-group epstein-files-rg
```

---

## 📈 Cost Tracking Dashboard

Track your actual costs vs. target:

| Month | Target | Actual | Variance | Action |
|-------|--------|--------|----------|--------|
| Jan | $675 | - | - | Monitor |
| Feb | $675 | - | - | - |
| Mar | $675 | - | - | - |

---

## 🔗 Additional Resources

- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
- [Azure Cost Management](https://portal.azure.com/#blade/Microsoft_Azure_CostManagement/Menu/overview)
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Cloudflare Free Plan](https://www.cloudflare.com/plans/free/)
- [Algolia Free Tier](https://www.algolia.com/pricing/)

---

## Summary

**You can reduce Azure costs by 50-96% depending on your needs:**

- **$1,360 → $675** (50% off) - Optimized production tier
- **$1,360 → $200** (85% off) - Budget tier  
- **$1,360 → $0-50** (96%+ off) - Free/minimal tier

**Recommended approach:** Start with Optimized tier ($675/month), monitor usage, then scale down to Budget or Free tier based on actual needs.
