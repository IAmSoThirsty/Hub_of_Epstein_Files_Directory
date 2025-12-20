#!/usr/bin/env python3
"""
Wikipedia Data Integration Tool
Fetches comprehensive information on dates, times, locations, characters from Wikipedia
Uses official Wikipedia API - fully legal and compliant with ToS

Data collected:
- Character/person information (dates of birth, roles, relationships)
- Location details (addresses, coordinates, significance)
- Timeline events (dates, descriptions, sources)
- Travel records (dates, locations, companions)
"""

import requests
import json
import time
from pathlib import Path
from datetime import datetime
import re

# Wikipedia API endpoint
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

# Target articles to fetch
WIKIPEDIA_ARTICLES = {
    'main': [
        'Jeffrey_Epstein',
        'Ghislaine_Maxwell',
        'Little_Saint_James,_U.S._Virgin_Islands',
        'Great_Saint_James,_U.S._Virgin_Islands',
        'Jeffrey_Epstein_VI_Foundation',
    ],
    'locations': [
        'Palm_Beach,_Florida',
        'Manhattan',
        'New_Mexico',
        'Paris',
        'London',
        'Zorro_Ranch',
    ],
    'related_persons': [
        'Virginia_Giuffre',
        'Alan_Dershowitz',
        'Leslie_Wexner',
        'Prince_Andrew,_Duke_of_York',
    ],
    'investigations': [
        'United_States_v._Ghislaine_Maxwell',
        'Southern_District_of_New_York',
    ]
}

class WikipediaFetcher:
    """Fetch and process Wikipedia data"""
    
    def __init__(self, output_dir='data/wikipedia'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EpsteinFilesHub/1.0 (Educational/Research; https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory)'
        })
        
    def fetch_article(self, title):
        """Fetch Wikipedia article content"""
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts|info|categories|links|images|revisions',
            'exintro': False,
            'explaintext': True,
            'inprop': 'url',
            'redirects': 1,
            'rvprop': 'timestamp',
            'rvlimit': 1
        }
        
        try:
            response = self.session.get(WIKIPEDIA_API, params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            page_id = list(pages.keys())[0]
            
            if page_id == '-1':
                print(f"⚠️  Article not found: {title}")
                return None
                
            return pages[page_id]
            
        except Exception as e:
            print(f"❌ Error fetching {title}: {e}")
            return None
    
    def extract_dates(self, text):
        """Extract dates from Wikipedia text"""
        date_patterns = [
            r'\b(\d{4})\b',  # Years
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month Day, Year
            r'\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',  # Day Month Year
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return list(set(dates))
    
    def extract_locations(self, text):
        """Extract location mentions from text"""
        # Common locations in Epstein case
        known_locations = [
            'Little Saint James', 'Little St. James', 'Great Saint James',
            'Palm Beach', 'Manhattan', 'New York', 'Florida', 'Virgin Islands',
            'Paris', 'London', 'New Mexico', 'Zorro Ranch', 'Santa Fe',
            'East 71st Street', 'Madison Avenue'
        ]
        
        found_locations = []
        for location in known_locations:
            if location.lower() in text.lower():
                found_locations.append(location)
        
        return list(set(found_locations))
    
    def extract_persons(self, text):
        """Extract person mentions from text"""
        # Key persons in case
        known_persons = [
            'Jeffrey Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre',
            'Alan Dershowitz', 'Leslie Wexner', 'Prince Andrew',
            'Bill Clinton', 'Donald Trump', 'Jean-Luc Brunel',
            'Sarah Kellen', 'Nadia Marcinkova'
        ]
        
        found_persons = []
        for person in known_persons:
            if person.lower() in text.lower():
                found_persons.append(person)
        
        return list(set(found_persons))
    
    def process_article(self, title):
        """Fetch and process a Wikipedia article"""
        print(f"📥 Fetching: {title}")
        
        article = self.fetch_article(title)
        if not article:
            return None
        
        extract = article.get('extract', '')
        
        # Extract structured data
        data = {
            'title': article.get('title', title),
            'url': article.get('fullurl', ''),
            'last_modified': article.get('revisions', [{}])[0].get('timestamp', ''),
            'content': extract,
            'dates': self.extract_dates(extract),
            'locations': self.extract_locations(extract),
            'persons': self.extract_persons(extract),
            'word_count': len(extract.split()),
            'fetched_at': datetime.now().isoformat(),
        }
        
        # Save individual article
        filename = f"{title.replace('/', '_').replace(',', '')}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved: {filename}")
        print(f"   📊 {data['word_count']} words, {len(data['dates'])} dates, {len(data['locations'])} locations, {len(data['persons'])} persons")
        
        return data
    
    def generate_character_profiles(self, articles_data):
        """Generate character profiles from Wikipedia data"""
        profiles = {}
        
        for data in articles_data:
            if not data:
                continue
                
            title = data['title']
            
            # Create character profile
            profile = {
                'name': title,
                'source': 'Wikipedia',
                'url': data['url'],
                'summary': data['content'][:500] + '...' if len(data['content']) > 500 else data['content'],
                'associated_dates': data['dates'][:10],  # Top 10 dates
                'associated_locations': data['locations'],
                'associated_persons': data['persons'],
                'last_updated': data['fetched_at']
            }
            
            profiles[title] = profile
        
        # Save profiles
        profiles_file = self.output_dir / 'character_profiles.json'
        with open(profiles_file, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Generated {len(profiles)} character profiles")
        return profiles
    
    def generate_timeline(self, articles_data):
        """Generate timeline from all dates found"""
        timeline = []
        
        for data in articles_data:
            if not data:
                continue
            
            for date in data['dates']:
                event = {
                    'date': date,
                    'source': data['title'],
                    'url': data['url'],
                    'context': 'Mentioned in Wikipedia article'
                }
                timeline.append(event)
        
        # Sort by date (simple year-based sort)
        timeline.sort(key=lambda x: x['date'])
        
        # Save timeline
        timeline_file = self.output_dir / 'timeline.json'
        with open(timeline_file, 'w', encoding='utf-8') as f:
            json.dump(timeline, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated timeline with {len(timeline)} events")
        return timeline
    
    def generate_location_guide(self, articles_data):
        """Generate location guide from Wikipedia data"""
        locations = {}
        
        for data in articles_data:
            if not data:
                continue
            
            for location in data['locations']:
                if location not in locations:
                    locations[location] = {
                        'name': location,
                        'mentions': 0,
                        'sources': [],
                        'associated_persons': [],
                        'dates': []
                    }
                
                locations[location]['mentions'] += 1
                locations[location]['sources'].append({
                    'title': data['title'],
                    'url': data['url']
                })
                locations[location]['associated_persons'].extend(data['persons'])
                locations[location]['dates'].extend(data['dates'])
        
        # Clean up duplicates
        for loc in locations.values():
            loc['associated_persons'] = list(set(loc['associated_persons']))
            loc['dates'] = list(set(loc['dates']))
        
        # Save location guide
        locations_file = self.output_dir / 'locations_guide.json'
        with open(locations_file, 'w', encoding='utf-8') as f:
            json.dump(locations, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated location guide with {len(locations)} locations")
        return locations
    
    def fetch_all(self):
        """Fetch all configured Wikipedia articles"""
        print("🌐 Starting Wikipedia data integration...")
        print(f"📁 Output directory: {self.output_dir}")
        print()
        
        all_articles = []
        
        # Fetch all categories
        for category, articles in WIKIPEDIA_ARTICLES.items():
            print(f"\n📚 Category: {category.upper()}")
            print("=" * 60)
            
            for article_title in articles:
                data = self.process_article(article_title)
                if data:
                    all_articles.append(data)
                
                # Rate limiting - be respectful to Wikipedia
                time.sleep(1)
        
        print("\n" + "=" * 60)
        print("📊 Generating aggregated data...")
        print()
        
        # Generate aggregated outputs
        profiles = self.generate_character_profiles(all_articles)
        timeline = self.generate_timeline(all_articles)
        locations = self.generate_location_guide(all_articles)
        
        # Generate summary
        summary = {
            'generated_at': datetime.now().isoformat(),
            'total_articles': len(all_articles),
            'total_profiles': len(profiles),
            'total_timeline_events': len(timeline),
            'total_locations': len(locations),
            'sources': {
                'wikipedia_api': WIKIPEDIA_API,
                'articles_fetched': [a['title'] for a in all_articles if a]
            }
        }
        
        summary_file = self.output_dir / 'summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("✅ Wikipedia integration complete!")
        print(f"📊 Total articles fetched: {len(all_articles)}")
        print(f"👥 Character profiles: {len(profiles)}")
        print(f"📅 Timeline events: {len(timeline)}")
        print(f"📍 Locations documented: {len(locations)}")
        print(f"📁 All data saved to: {self.output_dir}")
        print("=" * 60)

def main():
    """Main execution"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║        Wikipedia Data Integration for Epstein Files Hub     ║
║        Fetching dates, times, locations, characters          ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    fetcher = WikipediaFetcher()
    fetcher.fetch_all()
    
    print("\n✅ Integration complete! Data ready for indexing.")
    print("📝 Next step: Run 'python scripts/generate-search-index.py' to update search")

if __name__ == '__main__':
    main()
