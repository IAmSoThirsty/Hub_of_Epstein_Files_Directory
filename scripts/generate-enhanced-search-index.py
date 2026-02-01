#!/usr/bin/env python3
"""
Enhanced Search Index Generator
Creates comprehensive search index from ALL documents and data
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class SearchIndexGenerator:
    """Generates comprehensive search index for all content"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.data_dir = self.project_root / 'data'
        self.web_dir = self.project_root / 'web'
        
        self.search_index = {
            'documents': [],
            'characters': [],
            'locations': [],
            'events': [],
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_items': 0,
                'version': '2.0'
            }
        }
    
    def index_documents(self):
        """Index all documents from public_files"""
        print("Indexing documents...")
        
        public_files_dir = self.data_dir / 'public_files'
        if not public_files_dir.exists():
            print("No public files directory found")
            return
        
        for file_path in public_files_dir.rglob('*'):
            if file_path.is_file():
                doc_entry = {
                    'id': str(file_path.relative_to(public_files_dir)),
                    'name': file_path.name,
                    'path': str(file_path.relative_to(self.project_root)),
                    'type': file_path.suffix,
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'category': self._categorize_document(file_path)
                }
                self.search_index['documents'].append(doc_entry)
        
        print(f"✓ Indexed {len(self.search_index['documents'])} documents")
    
    def index_characters(self):
        """Index all characters"""
        print("Indexing characters...")
        
        char_db_path = self.data_dir / 'characters' / 'characters_database.json'
        if char_db_path.exists():
            with open(char_db_path, 'r') as f:
                characters = json.load(f)
            
            for char_id, char_data in characters.items():
                char_entry = {
                    'id': char_id,
                    'name': char_data.get('name', ''),
                    'role': char_data.get('role', ''),
                    'summary': char_data.get('summary', ''),
                    'url': f'profiles/{char_id}.html',
                    'connections': char_data.get('connections', []),
                    'searchable_text': self._create_searchable_text(char_data)
                }
                self.search_index['characters'].append(char_entry)
        
        print(f"✓ Indexed {len(self.search_index['characters'])} characters")
    
    def index_locations(self):
        """Index all locations"""
        print("Indexing locations...")
        
        locations = [
            {'id': 'little_st_james', 'name': 'Little St. James Island', 'type': 'Private Island', 'country': 'US Virgin Islands'},
            {'id': 'great_st_james', 'name': 'Great St. James Island', 'type': 'Private Island', 'country': 'US Virgin Islands'},
            {'id': 'palm_beach', 'name': 'Palm Beach Residence', 'type': 'Residence', 'country': 'USA'},
            {'id': 'new_york', 'name': 'New York Mansion', 'type': 'Residence', 'country': 'USA'},
            {'id': 'paris', 'name': 'Paris Apartment', 'type': 'Residence', 'country': 'France'},
            {'id': 'new_mexico', 'name': 'Zorro Ranch', 'type': 'Ranch', 'country': 'USA'},
            {'id': 'mar_a_lago', 'name': 'Mar-a-Lago', 'type': 'Resort', 'country': 'USA'},
            {'id': 'manhattan_jail', 'name': 'Metropolitan Correctional Center', 'type': 'Facility', 'country': 'USA'},
        ]
        
        for loc in locations:
            loc['url'] = f'locations/{loc["id"]}.html'
            self.search_index['locations'].append(loc)
        
        print(f"✓ Indexed {len(self.search_index['locations'])} locations")
    
    def index_events(self):
        """Index major timeline events"""
        print("Indexing events...")
        
        events = [
            {'date': '2008-06-30', 'title': 'Epstein Plea Deal', 'description': 'Pleaded guilty to state prostitution charges'},
            {'date': '2019-07-06', 'title': 'Epstein Arrested', 'description': 'Arrested on federal sex trafficking charges'},
            {'date': '2019-08-10', 'title': 'Epstein Death', 'description': 'Found dead in Manhattan jail'},
            {'date': '2020-07-02', 'title': 'Maxwell Arrested', 'description': 'Ghislaine Maxwell arrested in New Hampshire'},
            {'date': '2021-12-29', 'title': 'Maxwell Convicted', 'description': 'Convicted on 5 of 6 counts'},
            {'date': '2022-06-28', 'title': 'Maxwell Sentenced', 'description': 'Sentenced to 20 years in prison'},
        ]
        
        self.search_index['events'] = events
        print(f"✓ Indexed {len(self.search_index['events'])} events")
    
    def _categorize_document(self, file_path: Path) -> str:
        """Categorize document based on path"""
        path_str = str(file_path).lower()
        if 'fbi' in path_str:
            return 'FBI Document'
        elif 'doj' in path_str:
            return 'DOJ Document'
        elif 'court' in path_str:
            return 'Court Filing'
        elif 'flight' in path_str:
            return 'Flight Log'
        else:
            return 'General Document'
    
    def _create_searchable_text(self, data: Dict) -> str:
        """Create searchable text from character data"""
        parts = [
            data.get('name', ''),
            data.get('role', ''),
            data.get('summary', ''),
            ' '.join(data.get('key_locations', [])),
            ' '.join(data.get('aliases', [])),
        ]
        return ' '.join(filter(None, parts))
    
    def generate_search_index_js(self):
        """Generate JavaScript search index file"""
        print("Generating search index JavaScript...")
        
        # Update metadata
        self.search_index['metadata']['total_items'] = (
            len(self.search_index['documents']) +
            len(self.search_index['characters']) +
            len(self.search_index['locations']) +
            len(self.search_index['events'])
        )
        
        # Generate JavaScript file
        js_content = f'''// Search Index - Generated {datetime.now().isoformat()}
// Total items: {self.search_index['metadata']['total_items']}

const SEARCH_INDEX = {json.dumps(self.search_index, indent=2)};

// Make available globally
if (typeof window !== 'undefined') {{
    window.SEARCH_INDEX = SEARCH_INDEX;
}}

// Export for modules
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = SEARCH_INDEX;
}}
'''
        
        output_path = self.web_dir / 'js' / 'search-index.js'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"✓ Generated search index: {output_path}")
        
        # Also save as JSON
        json_path = self.web_dir / 'data' / 'search-index.json'
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.search_index, f, indent=2)
        
        print(f"✓ Saved JSON index: {json_path}")
    
    def generate(self):
        """Generate complete search index"""
        print("\n" + "="*60)
        print("SEARCH INDEX GENERATOR")
        print("="*60 + "\n")
        
        self.index_documents()
        self.index_characters()
        self.index_locations()
        self.index_events()
        self.generate_search_index_js()
        
        print("\n" + "="*60)
        print(f"✓ Search index complete!")
        print(f"  Documents: {len(self.search_index['documents'])}")
        print(f"  Characters: {len(self.search_index['characters'])}")
        print(f"  Locations: {len(self.search_index['locations'])}")
        print(f"  Events: {len(self.search_index['events'])}")
        print(f"  Total: {self.search_index['metadata']['total_items']}")
        print("="*60 + "\n")

if __name__ == '__main__':
    generator = SearchIndexGenerator()
    generator.generate()
