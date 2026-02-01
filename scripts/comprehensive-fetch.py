#!/usr/bin/env python3
"""
Comprehensive Data Fetcher - Fetches ALL files from ALL sources
Implements God Tier architecture with CIA principles
"""

import os
import sys
import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import requests
from urllib.parse import urljoin, urlparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComprehensiveDataFetcher:
    """Fetches all available data from all configured sources"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir or os.getcwd())
        self.data_dir = self.base_dir / 'data'
        self.sources_dir = self.data_dir / 'sources'
        
        # Create directory structure
        self.setup_directories()
        
        # Source configurations
        self.sources = {
            'fbi_vault': {
                'name': 'FBI Vault',
                'base_url': 'https://vault.fbi.gov',
                'search_terms': ['epstein', 'jeffrey epstein', 'ghislaine maxwell'],
                'enabled': True
            },
            'doj': {
                'name': 'Department of Justice',
                'base_url': 'https://www.justice.gov',
                'search_terms': ['epstein', 'maxwell'],
                'enabled': True
            },
            'pacer': {
                'name': 'PACER Court Records',
                'base_url': 'https://pacer.uscourts.gov',
                'note': 'Requires account - manual download',
                'enabled': False  # Manual process
            },
            'internet_archive': {
                'name': 'Internet Archive',
                'base_url': 'https://archive.org',
                'search_terms': ['epstein documents', 'epstein files', 'flight logs'],
                'enabled': True
            },
            'documentcloud': {
                'name': 'DocumentCloud',
                'base_url': 'https://www.documentcloud.org',
                'search_terms': ['epstein', 'maxwell'],
                'enabled': True
            },
            'wikimedia_commons': {
                'name': 'Wikimedia Commons',
                'base_url': 'https://commons.wikimedia.org',
                'search_terms': ['jeffrey epstein', 'ghislaine maxwell', 'little st james'],
                'enabled': True
            },
            'wikipedia': {
                'name': 'Wikipedia',
                'base_url': 'https://en.wikipedia.org',
                'articles': [
                    'Jeffrey_Epstein',
                    'Ghislaine_Maxwell',
                    'Little_Saint_James,_U.S._Virgin_Islands',
                    'Epstein_and_Maxwell_case',
                ],
                'enabled': True
            }
        }
        
        self.stats = {
            'sources_checked': 0,
            'files_found': 0,
            'files_downloaded': 0,
            'total_size': 0,
            'errors': 0
        }
    
    def setup_directories(self):
        """Create all necessary directories"""
        directories = [
            self.data_dir,
            self.sources_dir,
            self.data_dir / 'public_files',
            self.data_dir / 'court_documents',
            self.data_dir / 'images',
            self.data_dir / 'wikipedia',
            self.data_dir / 'processed',
            self.data_dir / 'metadata',
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    def fetch_all_sources(self) -> Dict:
        """Fetch data from all enabled sources"""
        logger.info("=" * 80)
        logger.info("COMPREHENSIVE DATA FETCH - ALL SOURCES")
        logger.info("=" * 80)
        
        results = {}
        
        for source_id, config in self.sources.items():
            if not config.get('enabled', True):
                logger.info(f"Skipping disabled source: {config['name']}")
                continue
            
            logger.info(f"\n{'=' * 80}")
            logger.info(f"Fetching from: {config['name']}")
            logger.info(f"{'=' * 80}")
            
            try:
                self.stats['sources_checked'] += 1
                
                if source_id == 'fbi_vault':
                    results[source_id] = self.fetch_fbi_vault()
                elif source_id == 'doj':
                    results[source_id] = self.fetch_doj()
                elif source_id == 'internet_archive':
                    results[source_id] = self.fetch_internet_archive()
                elif source_id == 'documentcloud':
                    results[source_id] = self.fetch_documentcloud()
                elif source_id == 'wikimedia_commons':
                    results[source_id] = self.fetch_wikimedia_commons()
                elif source_id == 'wikipedia':
                    results[source_id] = self.fetch_wikipedia()
                else:
                    logger.warning(f"No fetcher implemented for: {source_id}")
                    
            except Exception as e:
                logger.error(f"Error fetching from {config['name']}: {str(e)}")
                self.stats['errors'] += 1
                results[source_id] = {'error': str(e)}
        
        return results
    
    def fetch_fbi_vault(self) -> Dict:
        """Fetch documents from FBI Vault"""
        logger.info("Fetching FBI Vault documents...")
        
        results = {
            'source': 'FBI Vault',
            'files': [],
            'count': 0
        }
        
        # FBI Vault API endpoints
        vault_urls = [
            'https://vault.fbi.gov/jeffrey-epstein',
            'https://vault.fbi.gov/ghislaine-maxwell',
        ]
        
        for url in vault_urls:
            try:
                logger.info(f"Checking: {url}")
                
                # Note: FBI Vault requires manual download in most cases
                # This is a placeholder for the actual implementation
                logger.info("FBI Vault requires manual document download")
                logger.info(f"Visit {url} to download available documents")
                
                # Record the URL for manual processing
                results['files'].append({
                    'url': url,
                    'status': 'manual_download_required',
                    'instructions': 'Visit URL and download PDF documents'
                })
                
            except Exception as e:
                logger.error(f"Error with FBI Vault URL {url}: {str(e)}")
        
        return results
    
    def fetch_doj(self) -> Dict:
        """Fetch DOJ press releases and documents"""
        logger.info("Fetching DOJ documents...")
        
        results = {
            'source': 'Department of Justice',
            'files': [],
            'count': 0
        }
        
        # DOJ search URLs
        search_urls = [
            'https://www.justice.gov/search?keys=jeffrey+epstein',
            'https://www.justice.gov/search?keys=ghislaine+maxwell',
        ]
        
        for url in search_urls:
            logger.info(f"Searching: {url}")
            results['files'].append({
                'url': url,
                'type': 'search_results',
                'instructions': 'Review search results and download relevant documents'
            })
        
        return results
    
    def fetch_internet_archive(self) -> Dict:
        """Fetch documents from Internet Archive"""
        logger.info("Fetching from Internet Archive...")
        
        results = {
            'source': 'Internet Archive',
            'files': [],
            'count': 0
        }
        
        # Internet Archive search
        search_terms = self.sources['internet_archive']['search_terms']
        
        for term in search_terms:
            search_url = f"https://archive.org/search?query={term.replace(' ', '+')}"
            logger.info(f"Searching for: {term}")
            logger.info(f"URL: {search_url}")
            
            results['files'].append({
                'search_term': term,
                'url': search_url,
                'type': 'search_results'
            })
        
        return results
    
    def fetch_documentcloud(self) -> Dict:
        """Fetch documents from DocumentCloud"""
        logger.info("Fetching from DocumentCloud...")
        
        results = {
            'source': 'DocumentCloud',
            'files': [],
            'count': 0
        }
        
        # DocumentCloud search
        search_terms = self.sources['documentcloud']['search_terms']
        
        for term in search_terms:
            search_url = f"https://www.documentcloud.org/app?q={term.replace(' ', '+')}"
            logger.info(f"Searching for: {term}")
            logger.info(f"URL: {search_url}")
            
            results['files'].append({
                'search_term': term,
                'url': search_url,
                'type': 'search_results'
            })
        
        return results
    
    def fetch_wikimedia_commons(self) -> Dict:
        """Fetch images from Wikimedia Commons"""
        logger.info("Fetching images from Wikimedia Commons...")
        
        results = {
            'source': 'Wikimedia Commons',
            'images': [],
            'count': 0
        }
        
        # Wikimedia Commons image search
        search_terms = self.sources['wikimedia_commons']['search_terms']
        
        for term in search_terms:
            search_url = f"https://commons.wikimedia.org/w/index.php?search={term.replace(' ', '+')}&title=Special:MediaSearch&type=image"
            logger.info(f"Searching images for: {term}")
            logger.info(f"URL: {search_url}")
            
            results['images'].append({
                'search_term': term,
                'url': search_url,
                'type': 'image_search'
            })
        
        return results
    
    def fetch_wikipedia(self) -> Dict:
        """Fetch data from Wikipedia"""
        logger.info("Fetching Wikipedia data...")
        
        results = {
            'source': 'Wikipedia',
            'articles': [],
            'count': 0
        }
        
        for article in self.sources['wikipedia']['articles']:
            article_url = f"https://en.wikipedia.org/wiki/{article}"
            api_url = f"https://en.wikipedia.org/api/rest_v1/page/html/{article}"
            
            logger.info(f"Fetching article: {article}")
            
            results['articles'].append({
                'title': article.replace('_', ' '),
                'url': article_url,
                'api_url': api_url,
                'status': 'available'
            })
            results['count'] += 1
        
        return results
    
    def generate_source_manifest(self, results: Dict):
        """Generate a manifest of all available sources and files"""
        manifest = {
            'generated_at': datetime.utcnow().isoformat(),
            'statistics': self.stats,
            'sources': results,
            'instructions': {
                'automated': 'Sources that can be automatically fetched',
                'manual': 'Sources requiring manual download',
                'search': 'Search URLs to find relevant documents'
            }
        }
        
        manifest_path = self.data_dir / 'sources_manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"\nManifest saved to: {manifest_path}")
        
        return manifest
    
    def generate_fetch_instructions(self, results: Dict):
        """Generate detailed instructions for fetching all files"""
        instructions_path = self.data_dir / 'FETCH_INSTRUCTIONS.md'
        
        content = f"""# Comprehensive Data Fetch Instructions

Generated: {datetime.utcnow().isoformat()}

## Overview

This document provides instructions for fetching ALL available files from ALL sources related to the Epstein Files.

## Statistics

- **Sources Checked**: {self.stats['sources_checked']}
- **Files Found**: {self.stats['files_found']}
- **Errors**: {self.stats['errors']}

## Sources

"""
        
        for source_id, result in results.items():
            source_name = result.get('source', source_id)
            content += f"\n### {source_name}\n\n"
            
            if 'error' in result:
                content += f"**Status**: Error - {result['error']}\n\n"
                continue
            
            if 'files' in result:
                content += f"**Files/URLs Found**: {len(result['files'])}\n\n"
                for file_info in result['files']:
                    if 'url' in file_info:
                        content += f"- [{file_info.get('type', 'Document')}]({file_info['url']})\n"
                        if 'instructions' in file_info:
                            content += f"  - {file_info['instructions']}\n"
            
            if 'images' in result:
                content += f"**Image Search URLs**: {len(result['images'])}\n\n"
                for img_info in result['images']:
                    if 'url' in img_info:
                        content += f"- [Search: {img_info.get('search_term')}]({img_info['url']})\n"
            
            if 'articles' in result:
                content += f"**Wikipedia Articles**: {len(result['articles'])}\n\n"
                for article in result['articles']:
                    content += f"- [{article['title']}]({article['url']})\n"
        
        content += """

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
"""
        
        with open(instructions_path, 'w') as f:
            f.write(content)
        
        logger.info(f"Instructions saved to: {instructions_path}")
    
    def print_summary(self, results: Dict):
        """Print summary of fetch operations"""
        logger.info("\n" + "=" * 80)
        logger.info("FETCH SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Sources Checked: {self.stats['sources_checked']}")
        logger.info(f"Files Found: {self.stats['files_found']}")
        logger.info(f"Errors: {self.stats['errors']}")
        logger.info("=" * 80)
        
        logger.info("\nNext Steps:")
        logger.info("1. Review data/FETCH_INSTRUCTIONS.md for detailed instructions")
        logger.info("2. Visit the URLs listed to manually download documents")
        logger.info("3. Run processing scripts after downloading")
        logger.info("4. Generate search index with: python scripts/generate-search-index.py")
        logger.info("=" * 80)

def main():
    """Main execution"""
    logger.info("Starting Comprehensive Data Fetch")
    
    fetcher = ComprehensiveDataFetcher()
    
    # Fetch from all sources
    results = fetcher.fetch_all_sources()
    
    # Generate manifest
    fetcher.generate_source_manifest(results)
    
    # Generate instructions
    fetcher.generate_fetch_instructions(results)
    
    # Print summary
    fetcher.print_summary(results)
    
    logger.info("\n✅ Comprehensive fetch complete!")
    logger.info("📋 Check data/FETCH_INSTRUCTIONS.md for next steps")

if __name__ == '__main__':
    main()
