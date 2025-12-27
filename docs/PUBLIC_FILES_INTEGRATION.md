# Public Files Integration Guide

## Overview

This guide explains how to integrate publicly available Epstein-related files from official government sources into the Hub.

## Available Sources

### 1. FBI Vault (22 PDF Files)
**URL:** https://vault.fbi.gov/jeffrey-epstein

**Files:**
- 22 PDF parts totaling ~1,500 pages
- Investigation records
- Interview transcripts
- Evidence documentation

**Access:** Publicly available, no authentication required

### 2. DOJ Flight Logs (Text Files)
**URL:** Various DOJ and court document repositories

**Content:**
- Flight manifest records
- Passenger lists
- Travel dates and locations
- Aircraft tail numbers

**Access:** Available through FOIA releases and court filings

### 3. Court Filings
**Sources:**
- PACER (Public Access to Court Electronic Records)
- CourtListener
- DocumentCloud

**Content:**
- Case documents
- Depositions
- Exhibits
- Motions and filings

---

## Integration Tools

### Tool 1: Fetch Public Files
**Script:** `scripts/fetch-public-files.py`

**Features:**
- Automated downloading from FBI Vault
- Checksum verification (SHA-256)
- Duplicate detection
- Metadata generation
- Progress tracking

**Usage:**
```bash
# Interactive mode
python scripts/fetch-public-files.py

# Non-interactive (for automation)
python scripts/fetch-public-files.py --non-interactive --source fbi_vault
```

### Tool 2: Process PDFs
**Script:** `scripts/process-pdfs.py`

**Features:**
- Text extraction from PDFs
- OCR for scanned documents
- Metadata extraction (dates, locations, case numbers)
- Full-text indexing
- Search-ready output

**Usage:**
```bash
# Process all PDFs in data/public_files
python scripts/process-pdfs.py

# Process specific directory
python scripts/process-pdfs.py --input data/public_files/fbi_vault
```

### Tool 3: Update Search Index
**Script:** `scripts/generate-search-index.py`

**Features:**
- Incorporates processed documents
- Updates client-side search
- Generates statistics
- Creates search-ready JSON

**Usage:**
```bash
# Update search index with new documents
python scripts/generate-search-index.py --include-processed
```

---

## Step-by-Step Integration

### Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install requests pypdf pytesseract pillow pdf2image

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils

# For macOS
brew install tesseract poppler
```

### Step 2: Fetch FBI Vault Files

```bash
# Run the fetch script
python scripts/fetch-public-files.py

# Follow prompts:
# - Select "FBI Vault" source
# - Confirm download (y/n)
# - Wait for download to complete

# Files will be saved to:
# data/public_files/fbi_vault/
```

**Expected output:**
```
📁 Fetching FBI Vault Files...
[1/22] FBI Vault Part 01
  Downloading: https://vault.fbi.gov/...
  ✅ Downloaded: 1,234.56 KB

[2/22] FBI Vault Part 02
  ...

✅ FBI Vault: 22 files processed
```

### Step 3: Process PDFs

```bash
# Extract text and metadata
python scripts/process-pdfs.py

# This will:
# - Extract text from each PDF
# - Perform OCR if needed
# - Extract dates, locations, case numbers
# - Generate metadata files
# - Create search-ready index
```

**Output structure:**
```
data/processed/
├── text/
│   ├── epstein-part-01.txt
│   ├── epstein-part-02.txt
│   └── ...
├── metadata/
│   ├── epstein-part-01.json
│   ├── epstein-part-02.json
│   └── ...
├── indexed/
│   ├── epstein-part-01.json
│   └── ...
└── processing_summary.json
```

### Step 4: Update Search Index

```bash
# Regenerate search index with new documents
python scripts/generate-search-index.py

# This updates:
# web/js/search-index.js
# web/js/search-stats.json
# web/js/search-metadata.json
```

### Step 5: Commit Changes

```bash
# Add processed files
git add data/processed/
git add web/js/search-index.js

# Commit
git commit -m "Add FBI Vault documents (22 files processed)"

# Push to GitHub
git push
```

---

## Automated Integration

### GitHub Actions Workflow

The repository includes an automated workflow that can fetch and process files monthly.

**Workflow:** `.github/workflows/fetch-public-files.yml`

**Features:**
- Monthly automatic updates
- Manual trigger available
- Automatic PDF processing
- Search index updates
- Git commits if changes detected

**Manual trigger:**
1. Go to **Actions** tab in GitHub
2. Select **Fetch and Process Public Files**
3. Click **Run workflow**
4. Choose options:
   - ☑️ Fetch FBI Vault files
   - ☑️ Fetch DOJ flight logs
5. Click **Run workflow**

---

## File Size Considerations

### GitHub Repository Limits
- Maximum file size: 100 MB
- Maximum repository size: 100 GB (soft limit)
- Recommended: Keep under 5 GB

### FBI Vault Files
- Total size: ~200-300 MB (all 22 files)
- Individual files: 5-20 MB each
- ✅ **Within GitHub limits**

### Solutions for Large Files

#### Option 1: Git LFS (Free Tier)
```bash
# Install Git LFS
git lfs install

# Track PDF files
git lfs track "*.pdf"
git lfs track "data/public_files/**"

# Add and commit
git add .gitattributes
git commit -m "Configure Git LFS for PDFs"
```

**Free tier limits:**
- Storage: 1 GB
- Bandwidth: 1 GB/month

#### Option 2: External Storage
Store raw PDFs externally, keep only processed text:

```bash
# Don't commit raw PDFs
echo "data/public_files/*.pdf" >> .gitignore

# Only commit processed text
git add data/processed/text/
git add data/processed/metadata/
```

#### Option 3: Release Assets
Upload large files as GitHub Release assets:

```bash
# Create release
gh release create v1.0 \
  --title "Public Files Archive" \
  --notes "FBI Vault documents"

# Upload files
gh release upload v1.0 data/public_files/fbi_vault/*.pdf
```

---

## Data Structure

### Metadata Format

Each processed document includes:

```json
{
  "file_name": "epstein-part-01.pdf",
  "processed_date": "2024-12-20T08:00:00Z",
  "word_count": 15234,
  "char_count": 89456,
  "page_count": 75,
  "extraction_method": "text_extraction",
  "dates_found": [
    "1999-12-15",
    "2006-03-22",
    "2008-07-14"
  ],
  "case_numbers": [
    "CV-2019-001",
    "INV-2019-9878"
  ],
  "locations": [
    "Little St. James",
    "Palm Beach",
    "Manhattan"
  ]
}
```

### Search Index Format

```javascript
{
  "id": "fbi-vault-01",
  "title": "FBI Vault Part 01",
  "content": "First 1000 characters of text...",
  "full_text_path": "data/processed/text/epstein-part-01.txt",
  "date": "2019-08-10",
  "source": "FBI Vault",
  "type": "Investigation Record",
  "relevance": 95,
  "metadata": { /* ... */ }
}
```

---

## Adding New Sources

### Example: Adding Court Documents

1. **Update `fetch-public-files.py`:**

```python
PUBLIC_SOURCES['court_docs'] = {
    'name': 'Court Filings - SDNY',
    'base_url': 'https://example.com/docs',
    'files': [
        'case-123-exhibit-a.pdf',
        'case-123-exhibit-b.pdf'
    ]
}
```

2. **Add fetch method:**

```python
def fetch_court_documents(self):
    """Fetch court documents"""
    source = PUBLIC_SOURCES['court_docs']
    # Implementation similar to FBI Vault
```

3. **Update workflow:**

```yaml
- name: Fetch court documents
  run: |
    python scripts/fetch-public-files.py --source court_docs
```

---

## Best Practices

### 1. Rate Limiting
- Don't hammer servers with rapid requests
- Add delays between downloads (2-5 seconds)
- Respect robots.txt

### 2. Verification
- Always verify file integrity (checksums)
- Check file sizes match expected
- Review extracted text for accuracy

### 3. Documentation
- Document source URLs
- Track download dates
- Note any processing issues

### 4. Updates
- Check sources monthly for new files
- Version control metadata
- Keep download logs

### 5. Privacy
- Respect victim privacy redactions
- Don't attempt to de-redact documents
- Follow court orders on sealed materials

---

## Troubleshooting

### Issue: Download Fails

**Solution:**
- Check internet connection
- Verify source URL is still valid
- Try manual download to test
- Check if source requires authentication

### Issue: OCR Not Working

**Solution:**
```bash
# Install Tesseract
sudo apt-get install tesseract-ocr

# Verify installation
tesseract --version

# Test OCR
python -c "import pytesseract; print('OCR ready')"
```

### Issue: Out of Memory

**Solution:**
- Process files one at a time
- Reduce image resolution for OCR
- Use streaming for large files

### Issue: Files Too Large for GitHub

**Solution:**
- Use Git LFS
- Store externally, commit only text
- Split into smaller batches

---

## Maintenance

### Monthly Tasks
- [ ] Check for new FBI Vault updates
- [ ] Review DOJ document releases
- [ ] Update search index
- [ ] Verify all links still work

### Quarterly Tasks
- [ ] Full re-index of all documents
- [ ] Update metadata standards
- [ ] Clean up duplicate files
- [ ] Archive old versions

---

## Resources

**Official Sources:**
- FBI Vault: https://vault.fbi.gov/
- PACER: https://pacer.uscourts.gov/
- CourtListener: https://www.courtlistener.com/

**Tools:**
- pypdf: https://pypdf.readthedocs.io/
- Tesseract: https://github.com/tesseract-ocr/tesseract
- PDF.js: https://mozilla.github.io/pdf.js/

**Documentation:**
- Git LFS: https://git-lfs.github.com/
- GitHub Actions: https://docs.github.com/en/actions

---

## Summary

✅ **Tools provided:**
- Automated file fetching
- PDF processing and OCR
- Search index generation
- GitHub Actions workflow

✅ **Sources supported:**
- FBI Vault (22 files)
- DOJ flight logs
- Court documents
- Easy to add more

✅ **Features:**
- Free tier compatible
- Automated updates
- Full-text search
- Metadata extraction

**Next steps:**
1. Install dependencies
2. Run `python scripts/fetch-public-files.py`
3. Process with `python scripts/process-pdfs.py`
4. Update search index
5. Deploy to GitHub Pages

**Cost: $0** - All tools use free tier services!
