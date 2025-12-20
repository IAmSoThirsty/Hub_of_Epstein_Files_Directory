# Scripts Directory

This directory contains tools for managing the Epstein Files Hub.

## Available Scripts

### 1. generate-search-index.py
**Purpose:** Generate client-side search index for free tier

**Usage:**
```bash
python scripts/generate-search-index.py
```

**Output:**
- `web/js/search-index.js` - Search data
- `web/js/search-stats.json` - Statistics
- `web/js/search-metadata.json` - Metadata

**When to run:**
- After adding new documents
- Weekly via GitHub Actions
- After processing PDFs

---

### 2. fetch-public-files.py
**Purpose:** Download publicly available FBI Vault and DOJ files

**Usage:**
```bash
# Interactive mode
python scripts/fetch-public-files.py

# Non-interactive
python scripts/fetch-public-files.py --non-interactive
```

**Features:**
- Downloads FBI Vault PDFs (22 files)
- Downloads DOJ flight logs
- Verifies checksums (SHA-256)
- Prevents duplicates
- Generates metadata

**Output:**
- `data/public_files/fbi_vault/` - FBI PDFs
- `data/public_files/doj_flight_logs/` - Flight logs
- `data/public_files/metadata/` - File metadata
- `data/public_files/download_manifest.json` - Manifest

**Requirements:**
```bash
pip install requests
```

---

### 3. process-pdfs.py
**Purpose:** Extract text from PDFs and perform OCR

**Usage:**
```bash
# Process all PDFs
python scripts/process-pdfs.py

# Process specific directory
python scripts/process-pdfs.py --input data/public_files/fbi_vault
```

**Features:**
- Text extraction (PyPDF2)
- OCR for scanned docs (Tesseract)
- Metadata extraction (dates, locations, case numbers)
- Search-ready JSON output

**Output:**
- `data/processed/text/` - Extracted text
- `data/processed/metadata/` - Document metadata
- `data/processed/indexed/` - Search-ready JSON
- `data/processed/processing_summary.json` - Summary

**Requirements:**
```bash
pip install PyPDF2 pytesseract pillow pdf2image

# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils

# macOS
brew install tesseract poppler
```

---

## Typical Workflow

### Initial Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Fetch public files
python scripts/fetch-public-files.py

# 3. Process PDFs
python scripts/process-pdfs.py

# 4. Generate search index
python scripts/generate-search-index.py

# 5. Commit and deploy
git add data/ web/js/
git commit -m "Add processed public files"
git push
```

### Weekly Updates
```bash
# Check for new files
python scripts/fetch-public-files.py

# Process any new PDFs
python scripts/process-pdfs.py

# Update search
python scripts/generate-search-index.py
```

---

## Automated Execution

All scripts can run automatically via GitHub Actions:

### Workflows
1. **update-search-index.yml** - Weekly search index updates
2. **fetch-public-files.yml** - Monthly file fetching
3. **agent-monitoring.yml** - Daily health checks

### Manual Triggers
1. Go to **Actions** tab
2. Select workflow
3. Click **Run workflow**
4. Choose options

---

## Dependencies

### Python Packages
```
requests>=2.28.0
PyPDF2>=3.0.0
pytesseract>=0.3.10
Pillow>=9.0.0
pdf2image>=1.16.0
```

Install all:
```bash
pip install -r requirements.txt
```

### System Requirements

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils python3-pip
```

**macOS:**
```bash
brew install tesseract poppler python
```

**Windows:**
- Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Add to PATH
- Install poppler from: https://github.com/oschwartz10612/poppler-windows

---

## File Size Management

### Git LFS (Recommended)
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.pdf"
git lfs track "data/public_files/**"

# Commit
git add .gitattributes
git commit -m "Configure Git LFS"
```

### Alternative: Exclude Raw Files
```bash
# Add to .gitignore
echo "data/public_files/*.pdf" >> .gitignore

# Only commit processed text
git add data/processed/
```

---

## Troubleshooting

### Issue: Module not found
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: Tesseract not found
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Verify
tesseract --version
```

### Issue: poppler not found
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler

# Verify
pdftoppm -v
```

### Issue: Out of memory
```bash
# Process files one at a time
for pdf in data/public_files/*.pdf; do
    python scripts/process-pdfs.py --input "$pdf"
done
```

---

## Best Practices

### 1. Backup Before Processing
```bash
# Backup original files
cp -r data/public_files data/public_files.backup
```

### 2. Verify Downloads
```bash
# Check checksums after download
sha256sum data/public_files/fbi_vault/*.pdf
```

### 3. Test First
```bash
# Process one file first
python scripts/process-pdfs.py --input data/public_files/fbi_vault/epstein-part-01.pdf
```

### 4. Monitor Progress
```bash
# Watch processing
tail -f processing.log
```

### 5. Clean Up
```bash
# Remove temporary files
rm -rf data/processed/temp/
```

---

## Cost: $0

All scripts use free tier services:
- ✅ Python (FREE)
- ✅ GitHub Actions (2,000 min/month FREE)
- ✅ Storage on GitHub (within limits)
- ✅ No API costs

---

## Support

**Documentation:**
- [PUBLIC_FILES_INTEGRATION.md](../docs/PUBLIC_FILES_INTEGRATION.md)
- [FREE_TIER_SETUP.md](../docs/FREE_TIER_SETUP.md)
- [Bot-Usage-Guide.md](../docs/Bot-Usage-Guide.md)

**Issues:**
- GitHub Issues for bugs
- GitHub Discussions for questions

**Contributing:**
- See [CONTRIBUTING.md](../CONTRIBUTING.md)
