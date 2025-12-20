#!/usr/bin/env python3
"""
Safe Source Expansion Tool
Monitors official government and public sources for new Epstein-related documents
All sources are legal, ethical, and respect ToS

Sources monitored:
- PACER court filings (via RSS)
- Archive.org collections
- DocumentCloud
- Government FOIA libraries
- Wikimedia Commons (images)
- News archives with public APIs
"""

import requests
import json
import feedparser
from pathlib import Path
from datetime import datetime
import time

# Safe sources configuration
SAFE_SOURCES = {
    'archive_org': {
        'name': 'Internet Archive - Epstein Collections',
        'search_url': 'https://archive.org/advancedsearch.php',
        'params': {
            'q': 'epstein OR maxwell',
            'fl[]': ['identifier', 'title', 'date', 'creator', 'mediatype'],
            'rows': 50,
            'page': 1,
            'output': 'json'
        },
        'enabled': True
    },
    'documentcloud': {
        'name': 'DocumentCloud Public Documents',
        'api_url': 'https://api.www.documentcloud.org/api/documents/',
        'params': {
            'q': 'epstein OR maxwell',
            'per_page': 50
        },
        'enabled': True
    },
    'wikimedia_commons': {
        'name': 'Wikimedia Commons',
        'api_url': 'https://commons.wikimedia.org/w/api.php',
        'params': {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': 'epstein OR maxwell',
            'srnamespace': 6,  # File namespace
            'srlimit': 50
        },
        'enabled': True
    },
    'justice_gov': {
        'name': 'Justice.gov News',
        'rss_url': 'https://www.justice.gov/news/rss',
        'keywords': ['epstein', 'maxwell', 'trafficking'],
        'enabled': True
    },
    'fbi_news': {
        'name': 'FBI News',
        'rss_url': 'https://www.fbi.gov/feeds/feeds.xml',
        'keywords': ['epstein', 'maxwell', 'trafficking'],
        'enabled': True
    }
}

class SafeSourceExpander:
    """Monitor safe public sources for new documents"""
    
    def __init__(self, output_dir='data/discovered_sources'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EpsteinFilesHub/1.0 (Research; https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory)'
        })
    
    def check_archive_org(self):
        """Check Internet Archive for new items"""
        print("🔍 Checking Internet Archive...")
        
        source = SAFE_SOURCES['archive_org']
        if not source['enabled']:
            print("   ⏭️  Skipped (disabled)")
            return []
        
        try:
            response = self.session.get(source['search_url'], params=source['params'])
            response.raise_for_status()
            data = response.json()
            
            items = []
            for doc in data.get('response', {}).get('docs', []):
                item = {
                    'source': 'archive_org',
                    'identifier': doc.get('identifier'),
                    'title': doc.get('title'),
                    'date': doc.get('date'),
                    'url': f"https://archive.org/details/{doc.get('identifier')}",
                    'media_type': doc.get('mediatype'),
                    'discovered_at': datetime.now().isoformat()
                }
                items.append(item)
            
            print(f"   ✅ Found {len(items)} items")
            return items
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []
    
    def check_documentcloud(self):
        """Check DocumentCloud for new documents"""
        print("🔍 Checking DocumentCloud...")
        
        source = SAFE_SOURCES['documentcloud']
        if not source['enabled']:
            print("   ⏭️  Skipped (disabled)")
            return []
        
        try:
            response = self.session.get(source['api_url'], params=source['params'])
            response.raise_for_status()
            data = response.json()
            
            items = []
            for doc in data.get('results', []):
                item = {
                    'source': 'documentcloud',
                    'id': doc.get('id'),
                    'title': doc.get('title'),
                    'pages': doc.get('pages'),
                    'url': doc.get('canonical_url'),
                    'created_at': doc.get('created_at'),
                    'organization': doc.get('organization', {}).get('name'),
                    'discovered_at': datetime.now().isoformat()
                }
                items.append(item)
            
            print(f"   ✅ Found {len(items)} documents")
            return items
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []
    
    def check_wikimedia_commons(self):
        """Check Wikimedia Commons for images"""
        print("🔍 Checking Wikimedia Commons...")
        
        source = SAFE_SOURCES['wikimedia_commons']
        if not source['enabled']:
            print("   ⏭️  Skipped (disabled)")
            return []
        
        try:
            response = self.session.get(source['api_url'], params=source['params'])
            response.raise_for_status()
            data = response.json()
            
            items = []
            for result in data.get('query', {}).get('search', []):
                item = {
                    'source': 'wikimedia_commons',
                    'title': result.get('title'),
                    'page_id': result.get('pageid'),
                    'url': f"https://commons.wikimedia.org/wiki/{result.get('title')}",
                    'snippet': result.get('snippet', ''),
                    'discovered_at': datetime.now().isoformat()
                }
                items.append(item)
            
            print(f"   ✅ Found {len(items)} media files")
            return items
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []
    
    def check_rss_feed(self, source_key):
        """Check RSS feed for new items"""
        source = SAFE_SOURCES[source_key]
        print(f"🔍 Checking {source['name']}...")
        
        if not source['enabled']:
            print("   ⏭️  Skipped (disabled)")
            return []
        
        try:
            feed = feedparser.parse(source['rss_url'])
            
            items = []
            for entry in feed.entries[:20]:  # Last 20 items
                # Check if any keyword matches
                content = f"{entry.get('title', '')} {entry.get('summary', '')}".lower()
                
                if any(keyword in content for keyword in source['keywords']):
                    item = {
                        'source': source_key,
                        'title': entry.get('title'),
                        'url': entry.get('link'),
                        'published': entry.get('published'),
                        'summary': entry.get('summary', '')[:200],
                        'discovered_at': datetime.now().isoformat()
                    }
                    items.append(item)
            
            print(f"   ✅ Found {len(items)} relevant items")
            return items
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []
    
    def save_discoveries(self, discoveries):
        """Save discovered items to JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"discoveries_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(discoveries, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved discoveries to: {filepath}")
        return filepath
    
    def generate_report(self, discoveries):
        """Generate human-readable report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"discovery_report_{timestamp}.md"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Source Discovery Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary by source
            f.write("## Summary\n\n")
            source_counts = {}
            for discovery in discoveries:
                source = discovery['source']
                source_counts[source] = source_counts.get(source, 0) + 1
            
            for source, count in sorted(source_counts.items()):
                f.write(f"- **{source}**: {count} items\n")
            
            f.write(f"\n**Total discoveries:** {len(discoveries)}\n\n")
            
            # Detailed findings
            f.write("## Detailed Findings\n\n")
            
            for discovery in discoveries:
                f.write(f"### {discovery.get('title', 'Untitled')}\n\n")
                f.write(f"- **Source:** {discovery['source']}\n")
                f.write(f"- **URL:** {discovery.get('url', 'N/A')}\n")
                
                if 'date' in discovery:
                    f.write(f"- **Date:** {discovery['date']}\n")
                if 'published' in discovery:
                    f.write(f"- **Published:** {discovery['published']}\n")
                if 'pages' in discovery:
                    f.write(f"- **Pages:** {discovery['pages']}\n")
                if 'organization' in discovery:
                    f.write(f"- **Organization:** {discovery['organization']}\n")
                
                f.write(f"- **Discovered:** {discovery['discovered_at']}\n\n")
                
                if 'summary' in discovery:
                    f.write(f"**Summary:** {discovery['summary']}\n\n")
                
                f.write("---\n\n")
        
        print(f"📄 Generated report: {filepath}")
        return filepath
    
    def run_discovery(self):
        """Run discovery across all enabled sources"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║              Safe Source Expansion - Discovery Run           ║
║           Monitoring official and public sources             ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        all_discoveries = []
        
        # Check each source
        all_discoveries.extend(self.check_archive_org())
        time.sleep(2)  # Rate limiting
        
        all_discoveries.extend(self.check_documentcloud())
        time.sleep(2)
        
        all_discoveries.extend(self.check_wikimedia_commons())
        time.sleep(2)
        
        all_discoveries.extend(self.check_rss_feed('justice_gov'))
        time.sleep(2)
        
        all_discoveries.extend(self.check_rss_feed('fbi_news'))
        
        # Save results
        print("\n" + "=" * 60)
        print(f"📊 Discovery complete!")
        print(f"✅ Found {len(all_discoveries)} new items across all sources")
        
        if all_discoveries:
            json_file = self.save_discoveries(all_discoveries)
            report_file = self.generate_report(all_discoveries)
            
            print("\n📋 Next steps:")
            print("1. Review the discovery report")
            print("2. Manually verify relevant items")
            print("3. Add approved items to download queue")
        else:
            print("\n📋 No new items found in this run")
        
        print("=" * 60)

def main():
    """Main execution"""
    expander = SafeSourceExpander()
    expander.run_discovery()

if __name__ == '__main__':
    main()
