# Comprehensive Data Fetch Instructions

Generated: 2026-02-01T17:20:42.602031

## Overview

This document provides instructions for fetching ALL available files from ALL sources related to the Epstein Files.

## Statistics

- **Sources Checked**: 6
- **Files Found**: 0
- **Errors**: 0

## Sources


### FBI Vault

**Files/URLs Found**: 2

- [Document](https://vault.fbi.gov/jeffrey-epstein)
  - Visit URL and download PDF documents
- [Document](https://vault.fbi.gov/ghislaine-maxwell)
  - Visit URL and download PDF documents

### Department of Justice

**Files/URLs Found**: 2

- [search_results](https://www.justice.gov/search?keys=jeffrey+epstein)
  - Review search results and download relevant documents
- [search_results](https://www.justice.gov/search?keys=ghislaine+maxwell)
  - Review search results and download relevant documents

### Internet Archive

**Files/URLs Found**: 3

- [search_results](https://archive.org/search?query=epstein+documents)
- [search_results](https://archive.org/search?query=epstein+files)
- [search_results](https://archive.org/search?query=flight+logs)

### DocumentCloud

**Files/URLs Found**: 2

- [search_results](https://www.documentcloud.org/app?q=epstein)
- [search_results](https://www.documentcloud.org/app?q=maxwell)

### Wikimedia Commons

**Image Search URLs**: 3

- [Search: jeffrey epstein](https://commons.wikimedia.org/w/index.php?search=jeffrey+epstein&title=Special:MediaSearch&type=image)
- [Search: ghislaine maxwell](https://commons.wikimedia.org/w/index.php?search=ghislaine+maxwell&title=Special:MediaSearch&type=image)
- [Search: little st james](https://commons.wikimedia.org/w/index.php?search=little+st+james&title=Special:MediaSearch&type=image)

### Wikipedia

**Wikipedia Articles**: 4

- [Jeffrey Epstein](https://en.wikipedia.org/wiki/Jeffrey_Epstein)
- [Ghislaine Maxwell](https://en.wikipedia.org/wiki/Ghislaine_Maxwell)
- [Little Saint James, U.S. Virgin Islands](https://en.wikipedia.org/wiki/Little_Saint_James,_U.S._Virgin_Islands)
- [Epstein and Maxwell case](https://en.wikipedia.org/wiki/Epstein_and_Maxwell_case)


## Automated Fetch Process

Some sources can be fetched automatically using scripts:

```bash
# Fetch Wikipedia data
python scripts/fetch-wikipedia-data.py

# Fetch public files
python scripts/fetch-public-files.py

# Comprehensive fetch
python scripts/comprehensive-fetch.py
```

## Manual Download Process

For sources requiring manual download:

1. **FBI Vault**
   - Visit the URLs listed above
   - Click on each document PDF
   - Download to `data/public_files/fbi_vault/`
   - Organize by case/topic

2. **DOJ Documents**
   - Search the DOJ website
   - Download press releases and court documents
   - Save to `data/public_files/doj/`

3. **PACER Court Records**
   - Requires PACER account (paid)
   - Search for relevant cases
   - Download court filings
   - Save to `data/court_documents/`

4. **DocumentCloud**
   - Browse search results
   - Download relevant documents
   - Save to `data/public_files/documentcloud/`

5. **Internet Archive**
   - Search for document collections
   - Download entire collections when available
   - Save to `data/public_files/internet_archive/`

6. **Wikimedia Commons**
   - Search for images
   - Download high-resolution versions
   - Save to `data/images/wikimedia/`
   - Record source attribution

## Data Organization

Organize downloaded files in this structure:

```
data/
├── public_files/
│   ├── fbi_vault/
│   ├── doj/
│   ├── documentcloud/
│   └── internet_archive/
├── court_documents/
│   ├── sdny/  (Southern District of New York)
│   ├── sdfl/  (Southern District of Florida)
│   └── other/
├── images/
│   ├── wikimedia/
│   ├── court_exhibits/
│   └── press/
└── wikipedia/
    ├── articles/
    └── data/
```

## Processing Pipeline

After downloading files:

1. Run document processing:
   ```bash
   python scripts/process-pdfs.py
   ```

2. Generate search index:
   ```bash
   python scripts/generate-search-index.py
   ```

3. Update web interface:
   ```bash
   git add data/ web/
   git commit -m "Add new documents"
   git push
   ```

## Verification

Verify all downloads:

```bash
# Check file counts
find data/public_files -type f | wc -l

# Check total size
du -sh data/

# Verify checksums
python scripts/verify-checksums.py
```

## Legal & Ethical Considerations

- ✅ Only download PUBLIC records
- ✅ Respect copyright and licensing
- ✅ Protect victim privacy
- ✅ Cite all sources
- ✅ Follow court orders re: sealed documents
- ❌ Do NOT share private information
- ❌ Do NOT violate copyright

## Support

For questions or issues:
- GitHub Issues
- GitHub Discussions
- Documentation: docs/

---

**Last Updated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
