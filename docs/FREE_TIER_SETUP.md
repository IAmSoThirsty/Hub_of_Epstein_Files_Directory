# Free Tier Setup Guide ($0-50/month)

## Overview

This guide implements the **FREE tier** infrastructure for the Epstein Files Hub, reducing costs from $1,360/month to **$0-50/month** (96%+ savings).

**Annual Savings: $15,720 - $16,320**

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│           GitHub Pages (FREE)                        │
│  Static site hosting with HTML/CSS/JS                │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│         Cloudflare CDN (FREE)                        │
│  Global CDN, SSL, DDoS protection                    │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│    Client-Side Search (FREE)                         │
│  Lunr.js or Fuse.js for full-text search            │
│  Pre-computed search index (static JSON)             │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│    Static Data Files (FREE)                          │
│  JSON files with pre-processed content               │
│  Hosted on GitHub/Cloudflare                         │
└─────────────────────────────────────────────────────┘
```

---

## Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| **GitHub Pages** | FREE | Unlimited public repos |
| **Cloudflare CDN** | FREE | 100GB bandwidth/month |
| **Client Search (Lunr.js)** | FREE | Open source library |
| **GitHub Actions** | FREE | 2,000 minutes/month |
| **Storage** | FREE | Included in GitHub |
| **Domain (optional)** | $0-15/year | Use .github.io or custom |
| **Total** | **$0-2/month** | Or $0 with .github.io domain |

---

## Setup Instructions

### Step 1: Enable GitHub Pages

1. Go to repository **Settings** → **Pages**
2. Source: Deploy from a branch
3. Branch: `main` or `copilot/create-self-organizing-workflow`
4. Folder: `/web` (or root if web files are moved)
5. Click **Save**

Your site will be available at:
```
https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/
```

### Step 2: Set Up Cloudflare (Optional but Recommended)

1. Sign up at [cloudflare.com](https://cloudflare.com) (FREE plan)
2. Add your custom domain (if you have one)
3. Update DNS to point to GitHub Pages:
   ```
   CNAME: yourdomain.com → iamsothirsty.github.io
   ```
4. Enable SSL/TLS (Full)
5. Enable caching for static assets

**Benefits:**
- Global CDN (faster loading)
- DDoS protection
- SSL certificate
- Better analytics

### Step 3: Implement Client-Side Search

#### Option A: Lunr.js (Recommended)
```html
<!-- Add to web/search.html -->
<script src="https://unpkg.com/lunr/lunr.js"></script>
<script src="js/search-index.js"></script>
<script>
// Initialize search index
const documents = SEARCH_DATA; // From search-index.js

const idx = lunr(function () {
  this.ref('id')
  this.field('title')
  this.field('content')
  this.field('location')
  this.field('date')
  this.field('person')
  
  documents.forEach(function (doc) {
    this.add(doc)
  }, this)
})

// Search function
function performSearch(query) {
  const results = idx.search(query)
  displayResults(results)
}
</script>
```

#### Option B: Fuse.js (Better for fuzzy search)
```html
<script src="https://cdn.jsdelivr.net/npm/fuse.js@6.6.2"></script>
<script>
const options = {
  includeScore: true,
  keys: ['title', 'content', 'location', 'person'],
  threshold: 0.3
}

const fuse = new Fuse(SEARCH_DATA, options)

function performSearch(query) {
  const results = fuse.search(query)
  displayResults(results)
}
</script>
```

### Step 4: Generate Search Index

Create a script to pre-process documents into a search index:

```python
# scripts/generate-search-index.py
import json
import os
from pathlib import Path

def generate_search_index():
    """Generate static search index from documents"""
    documents = []
    
    # Load all documents
    doc_dir = Path('data/documents')
    for doc_file in doc_dir.glob('**/*.json'):
        with open(doc_file, 'r') as f:
            doc = json.load(f)
            documents.append({
                'id': doc['id'],
                'title': doc['title'],
                'content': doc['content'][:500],  # First 500 chars
                'date': doc['date'],
                'location': doc['location'],
                'person': doc.get('person', ''),
                'redaction_status': doc['redaction_status'],
                'case_number': doc.get('case_number', ''),
                'relevance': doc.get('relevance', 0),
                'tags': doc.get('tags', [])
            })
    
    # Save as JavaScript file
    output = f"const SEARCH_DATA = {json.dumps(documents, indent=2)};"
    
    with open('web/js/search-index.js', 'w') as f:
        f.write(output)
    
    print(f"Generated search index with {len(documents)} documents")

if __name__ == '__main__':
    generate_search_index()
```

Run this script whenever documents are updated:
```bash
python scripts/generate-search-index.py
```

### Step 5: Update Search UI

Modify `web/js/search.js` to use client-side search:

```javascript
// web/js/search.js - Updated for client-side search

let searchIndex;
let allDocuments = [];

// Load search index on page load
async function initSearch() {
    try {
        // Load pre-computed search data
        const response = await fetch('js/search-index.js');
        const scriptText = await response.text();
        
        // Execute script to load SEARCH_DATA
        eval(scriptText);
        allDocuments = SEARCH_DATA;
        
        // Initialize Lunr.js index
        searchIndex = lunr(function () {
            this.ref('id')
            this.field('title', { boost: 10 })
            this.field('content', { boost: 5 })
            this.field('location')
            this.field('person')
            this.field('case_number')
            
            allDocuments.forEach(doc => this.add(doc))
        });
        
        console.log('Search index loaded:', allDocuments.length, 'documents');
    } catch (error) {
        console.error('Error loading search index:', error);
    }
}

// Perform search with filters
function performSearch() {
    const query = document.getElementById('keyword-search').value;
    const docType = document.getElementById('doc-type').value;
    const location = document.getElementById('location').value;
    const redactionStatus = getSelectedRedactionStatus();
    const dateFrom = document.getElementById('date-from').value;
    const dateTo = document.getElementById('date-to').value;
    
    // Search using Lunr.js
    let results = searchIndex.search(query);
    
    // Map results back to full documents
    let documents = results.map(result => {
        return allDocuments.find(doc => doc.id === result.ref);
    });
    
    // Apply filters
    if (docType && docType !== 'all') {
        documents = documents.filter(doc => doc.type === docType);
    }
    
    if (location && location !== 'all') {
        documents = documents.filter(doc => doc.location === location);
    }
    
    if (redactionStatus.length > 0) {
        documents = documents.filter(doc => 
            redactionStatus.includes(doc.redaction_status)
        );
    }
    
    if (dateFrom) {
        documents = documents.filter(doc => doc.date >= dateFrom);
    }
    
    if (dateTo) {
        documents = documents.filter(doc => doc.date <= dateTo);
    }
    
    displayResults(documents);
}

// Display search results
function displayResults(documents) {
    const container = document.getElementById('search-results');
    container.innerHTML = '';
    
    if (documents.length === 0) {
        container.innerHTML = '<p>No results found.</p>';
        return;
    }
    
    const resultsCount = document.createElement('p');
    resultsCount.textContent = `${documents.length} Results Found`;
    container.appendChild(resultsCount);
    
    documents.forEach(doc => {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'search-result';
        resultDiv.innerHTML = `
            <h3>${doc.title}</h3>
            <p><strong>Date:</strong> ${doc.date}</p>
            <p><strong>Location:</strong> ${doc.location}</p>
            <p><strong>Status:</strong> ${doc.redaction_status}</p>
            <p>${doc.content}</p>
            <button onclick="viewDocument('${doc.id}')">View Document</button>
        `;
        container.appendChild(resultDiv);
    });
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', initSearch);
```

### Step 6: Set Up Automated Updates

Create a GitHub Action to regenerate search index on updates:

```yaml
# .github/workflows/update-search-index.yml
name: Update Search Index

on:
  push:
    paths:
      - 'data/documents/**'
      - 'data/images/**'
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:

jobs:
  update-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Generate search index
        run: |
          python scripts/generate-search-index.py
      
      - name: Commit and push if changed
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add web/js/search-index.js
          git diff --quiet && git diff --staged --quiet || git commit -m "Update search index"
          git push
```

### Step 7: Optimize for Performance

#### Compress Data Files
```bash
# Install compression
npm install -g terser uglify-js

# Minify JavaScript
terser web/js/search.js -o web/js/search.min.js
uglifyjs web/js/main.js -o web/js/main.min.js

# Update HTML to use minified versions
```

#### Enable Caching
Add to `web/.htaccess` (if using custom domain):
```apache
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 1 day"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType image/* "access plus 1 year"
</IfModule>
```

Or configure in Cloudflare:
- Cache Level: Standard
- Browser Cache TTL: 1 year for static assets

---

## Advanced Features (Still Free)

### 1. Algolia Search (Free Tier)
**10,000 searches/month free**

```javascript
// web/js/algolia-search.js
const client = algoliasearch('YOUR_APP_ID', 'YOUR_SEARCH_KEY');
const index = client.initIndex('epstein_files');

async function searchAlgolia(query) {
  const { hits } = await index.search(query, {
    filters: 'status:unredacted',
    attributesToRetrieve: ['title', 'date', 'location'],
    hitsPerPage: 20
  });
  
  displayResults(hits);
}
```

### 2. GitHub LFS for Large Files
**Free: 1GB storage + 1GB bandwidth/month**

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.pdf"
git lfs track "*.jpg"
git lfs track "*.png"

git add .gitattributes
git commit -m "Configure Git LFS"
```

### 3. Vercel Hosting (Alternative to GitHub Pages)
**Free tier: 100GB bandwidth/month**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd web
vercel --prod
```

---

## Limitations of Free Tier

| Feature | Limitation | Workaround |
|---------|-----------|------------|
| **Search Complexity** | No semantic search | Use Lunr.js with good tokenization |
| **Real-time Updates** | Manual index regeneration | GitHub Actions automate this |
| **Storage** | 1GB GitHub repo limit | Use Git LFS for large files |
| **Bandwidth** | Cloudflare: 100GB/month | Usually sufficient for this use case |
| **AI Analysis** | No OpenAI integration | Pre-compute analysis offline |
| **OCR** | No automated OCR | Use Tesseract locally, upload results |

---

## Migration Path (Free → Paid if Needed)

If you outgrow the free tier:

1. **First upgrade**: Algolia Standard ($99/month)
   - Better search performance
   - 100K searches/month
   
2. **Second upgrade**: Azure Basic tier ($200/month)
   - Add real-time OCR
   - Better document analysis
   
3. **Full production**: Azure Optimized ($675/month)
   - All enterprise features
   - OpenAI integration

---

## Testing the Setup

1. **Test search locally:**
   ```bash
   cd web
   python -m http.server 8000
   # Visit http://localhost:8000
   ```

2. **Test search index:**
   ```bash
   python scripts/generate-search-index.py
   # Check web/js/search-index.js exists
   ```

3. **Test GitHub Pages:**
   - Push changes to GitHub
   - Wait 1-2 minutes for deployment
   - Visit your GitHub Pages URL

---

## Maintenance

### Weekly Tasks (5 minutes)
- Review GitHub Actions logs
- Check search index updates
- Monitor bandwidth usage

### Monthly Tasks (30 minutes)
- Review analytics (Cloudflare/GitHub)
- Update documentation if needed
- Check for broken links

### Quarterly Tasks (2 hours)
- Review and optimize search performance
- Update client-side libraries
- Clean up unused files

---

## Support & Resources

**Documentation:**
- [GitHub Pages Docs](https://docs.github.com/pages)
- [Cloudflare Docs](https://developers.cloudflare.com/)
- [Lunr.js Guide](https://lunrjs.com/guides/)
- [Fuse.js Docs](https://fusejs.io/)

**Troubleshooting:**
- GitHub Pages not updating? Check Actions tab
- Search not working? Check browser console
- Slow loading? Enable Cloudflare caching

---

## Summary

✅ **Total Cost: $0-50/month** (vs $1,360)
✅ **Savings: $15,720-16,320/year**
✅ **Setup Time: 2-4 hours**
✅ **Maintenance: 30-60 min/month**
✅ **Scalability: Handles 10K+ visitors/month**

This free tier setup provides:
- Full search functionality
- Fast performance
- No infrastructure costs
- Easy maintenance
- Room to scale

**Next Steps:**
1. Enable GitHub Pages (5 minutes)
2. Generate search index (10 minutes)
3. Test search functionality (15 minutes)
4. Optional: Set up Cloudflare (30 minutes)

Your site will be live and fully functional with zero monthly costs!
