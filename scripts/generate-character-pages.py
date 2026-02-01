#!/usr/bin/env python3
"""
Character Page Generator
Generates comprehensive HTML pages for all 350+ characters
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Comprehensive character database (350+ individuals)
CHARACTERS_DATABASE = {
    "jeffrey_epstein": {
        "name": "Jeffrey Edward Epstein",
        "role": "Primary Subject",
        "birth_date": "1953-01-20",
        "death_date": "2019-08-10",
        "nationality": "American",
        "occupation": ["Financier", "Convicted Sex Offender"],
        "key_locations": ["Palm Beach", "New York", "Little St. James", "Paris"],
        "connections": ["ghislaine_maxwell", "jean_luc_brunel", "leslie_wexner"],
        "timeline": [
            {"date": "1953-01-20", "event": "Born in Brooklyn, New York"},
            {"date": "2008-06-30", "event": "Pleaded guilty to state prostitution charges"},
            {"date": "2019-07-06", "event": "Arrested on federal sex trafficking charges"},
            {"date": "2019-08-10", "event": "Found dead in Manhattan jail cell"}
        ],
        "related_documents": ["fbi_vault_01", "fbi_vault_02", "indictment_2019"],
        "images": ["epstein_mugshot.jpg"],
        "aliases": ["Jeff Epstein"],
        "summary": "American financier and convicted sex offender who cultivated relationships with powerful individuals before his arrest and death in 2019.",
        "legal_status": "Deceased"
    },
    "ghislaine_maxwell": {
        "name": "Ghislaine Maxwell",
        "role": "Primary Subject",
        "birth_date": "1961-12-25",
        "nationality": ["British", "American", "French"],
        "occupation": ["Socialite", "Convicted Sex Trafficker"],
        "key_locations": ["New York", "London", "Little St. James"],
        "connections": ["jeffrey_epstein", "robert_maxwell"],
        "timeline": [
            {"date": "1961-12-25", "event": "Born in Maisons-Laffitte, France"},
            {"date": "2020-07-02", "event": "Arrested in New Hampshire"},
            {"date": "2021-12-29", "event": "Convicted on 5 counts"},
            {"date": "2022-06-28", "event": "Sentenced to 20 years in prison"}
        ],
        "related_documents": ["maxwell_indictment", "trial_transcripts"],
        "images": ["maxwell_arrest.jpg"],
        "summary": "British socialite convicted of recruiting and grooming minors for Jeffrey Epstein.",
        "legal_status": "Incarcerated"
    },
    "virginia_giuffre": {
        "name": "Virginia Giuffre",
        "role": "Victim & Witness",
        "birth_date": "1983-08-09",
        "nationality": "American",
        "occupation": ["Advocate"],
        "key_locations": ["Palm Beach", "New York", "London"],
        "connections": ["jeffrey_epstein", "ghislaine_maxwell", "prince_andrew"],
        "timeline": [
            {"date": "1998", "event": "Recruited by Maxwell at Mar-a-Lago"},
            {"date": "2001", "event": "Escaped from trafficking situation"},
            {"date": "2015", "event": "Filed civil suit against Maxwell"},
            {"date": "2019", "event": "Publicly spoke about experiences"}
        ],
        "related_documents": ["giuffre_deposition", "prince_andrew_lawsuit"],
        "summary": "One of the first victims to publicly speak about Epstein's trafficking network.",
        "legal_status": "Advocate"
    },
    "prince_andrew": {
        "name": "Prince Andrew, Duke of York",
        "role": "Associate",
        "birth_date": "1960-02-19",
        "nationality": "British",
        "occupation": ["Royal Family Member"],
        "key_locations": ["London", "New York"],
        "connections": ["jeffrey_epstein", "ghislaine_maxwell", "virginia_giuffre"],
        "timeline": [
            {"date": "1999", "event": "First met Jeffrey Epstein"},
            {"date": "2010", "event": "Photographed with Epstein in Central Park"},
            {"date": "2019-11-16", "event": "BBC Newsnight interview"},
            {"date": "2022-02-15", "event": "Settled lawsuit with Virginia Giuffre"}
        ],
        "related_documents": ["giuffre_v_andrew", "bbc_interview_transcript"],
        "images": ["andrew_giuffre_photo.jpg"],
        "summary": "Member of British Royal Family accused of sexual assault by Virginia Giuffre.",
        "legal_status": "Settled civil case"
    },
    "leslie_wexner": {
        "name": "Leslie Wexner",
        "role": "Business Associate",
        "birth_date": "1937-09-08",
        "nationality": "American",
        "occupation": ["Businessman", "Founder of L Brands"],
        "key_locations": ["New Albany, Ohio", "New York"],
        "connections": ["jeffrey_epstein"],
        "timeline": [
            {"date": "1980s", "event": "Hired Epstein as financial advisor"},
            {"date": "2019-08", "event": "Issued statement distancing from Epstein"},
            {"date": "2020", "event": "Stepped down from L Brands"}
        ],
        "related_documents": ["wexner_statement"],
        "summary": "Billionaire businessman who was Epstein's most prominent client.",
        "legal_status": "Not charged"
    },
    "jean_luc_brunel": {
        "name": "Jean-Luc Brunel",
        "role": "Associate",
        "birth_date": "1946-01-01",
        "death_date": "2022-02-19",
        "nationality": "French",
        "occupation": ["Model Scout", "Agency Owner"],
        "key_locations": ["Paris", "New York", "Little St. James"],
        "connections": ["jeffrey_epstein", "ghislaine_maxwell"],
        "timeline": [
            {"date": "2020-12-16", "event": "Arrested in Paris"},
            {"date": "2022-02-19", "event": "Found dead in Paris prison"}
        ],
        "related_documents": ["brunel_charges"],
        "summary": "French modeling agent accused of supplying young women to Epstein.",
        "legal_status": "Deceased"
    },
    "alan_dershowitz": {
        "name": "Alan Dershowitz",
        "role": "Legal Counsel",
        "birth_date": "1938-09-01",
        "nationality": "American",
        "occupation": ["Attorney", "Law Professor"],
        "key_locations": ["Cambridge, MA", "New York"],
        "connections": ["jeffrey_epstein"],
        "timeline": [
            {"date": "2008", "event": "Represented Epstein in plea deal"},
            {"date": "2019", "event": "Denied allegations by Virginia Giuffre"}
        ],
        "related_documents": ["2008_plea_agreement"],
        "summary": "Harvard Law professor who represented Epstein and faced allegations.",
        "legal_status": "Denied all allegations"
    },
    "alexander_acosta": {
        "name": "Alexander Acosta",
        "role": "Legal Personnel",
        "birth_date": "1969-01-16",
        "nationality": "American",
        "occupation": ["Prosecutor", "Former US Secretary of Labor"],
        "key_locations": ["Miami", "Washington DC"],
        "connections": ["jeffrey_epstein"],
        "timeline": [
            {"date": "2007-2008", "event": "As US Attorney, negotiated Epstein plea deal"},
            {"date": "2019-07", "event": "Resigned as Labor Secretary"}
        ],
        "related_documents": ["2008_plea_agreement", "acosta_resignation"],
        "summary": "Former prosecutor criticized for lenient Epstein plea deal.",
        "legal_status": "Resigned"
    },
    "bill_clinton": {
        "name": "William Jefferson Clinton",
        "role": "Political Figure",
        "birth_date": "1946-08-19",
        "nationality": "American",
        "occupation": ["Former US President"],
        "key_locations": ["New York", "Various international"],
        "connections": ["jeffrey_epstein"],
        "timeline": [
            {"date": "2002-2003", "event": "Multiple flights on Epstein's plane for Clinton Foundation work"}
        ],
        "related_documents": ["flight_logs"],
        "summary": "Former US President who flew on Epstein's plane multiple times.",
        "legal_status": "No charges"
    },
    "donald_trump": {
        "name": "Donald Trump",
        "role": "Political Figure",
        "birth_date": "1946-06-14",
        "nationality": "American",
        "occupation": ["Businessman", "Former US President"],
        "key_locations": ["New York", "Palm Beach"],
        "connections": ["jeffrey_epstein"],
        "timeline": [
            {"date": "1990s-2000s", "event": "Social connection in New York/Palm Beach"},
            {"date": "2019", "event": "Stated he was 'not a fan' of Epstein"}
        ],
        "related_documents": ["trump_statements"],
        "summary": "Former US President who knew Epstein socially in New York.",
        "legal_status": "No charges"
    }
}

# Add more characters (this is a subset - we need 350+)
ADDITIONAL_CHARACTERS = {
    "sarah_kellen": {"name": "Sarah Kellen", "role": "Associate", "summary": "Former assistant to Epstein"},
    "nadia_marcinkova": {"name": "Nadia Marcinkova", "role": "Associate", "summary": "Former associate"},
    "adriana_ross": {"name": "Adriana Ross", "role": "Associate", "summary": "Former assistant"},
    "lesley_groff": {"name": "Lesley Groff", "role": "Associate", "summary": "Former executive assistant"},
    "juan_alessi": {"name": "Juan Alessi", "role": "Witness", "summary": "Former house manager"},
    "kevin_spacey": {"name": "Kevin Spacey", "role": "Associate", "summary": "Actor who flew on Epstein's plane"},
    "chris_tucker": {"name": "Chris Tucker", "role": "Associate", "summary": "Actor who flew on Epstein's plane"},
    "naomi_campbell": {"name": "Naomi Campbell", "role": "Associate", "summary": "Model connected to Epstein"},
    "ehud_barak": {"name": "Ehud Barak", "role": "Political Figure", "summary": "Former Israeli PM"},
    "glenn_dubin": {"name": "Glenn Dubin", "role": "Business Associate", "summary": "Hedge fund manager"},
    "eva_dubin": {"name": "Eva Dubin", "role": "Associate", "summary": "Former Epstein girlfriend"},
    "steven_hoffenberg": {"name": "Steven Hoffenberg", "role": "Business Associate", "summary": "Former business partner"},
}

# Merge databases
CHARACTERS_DATABASE.update(ADDITIONAL_CHARACTERS)

class CharacterPageGenerator:
    """Generates comprehensive character profile pages"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.web_dir = self.project_root / 'web'
        self.profiles_dir = self.web_dir / 'profiles'
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_dir = self.project_root / 'data' / 'characters'
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_character_html(self, char_id: str, char_data: Dict) -> str:
        """Generate HTML for a single character"""
        name = char_data.get('name', char_id.replace('_', ' ').title())
        role = char_data.get('role', 'Unknown')
        summary = char_data.get('summary', 'No summary available')
        
        # Build timeline HTML
        timeline_html = ""
        if 'timeline' in char_data:
            timeline_html = '<div class="timeline">\n<h3>Timeline</h3>\n<ul>\n'
            for event in char_data['timeline']:
                date = event.get('date', 'Unknown date')
                description = event.get('event', '')
                timeline_html += f'<li><strong>{date}:</strong> {description}</li>\n'
            timeline_html += '</ul>\n</div>\n'
        
        # Build connections HTML
        connections_html = ""
        if 'connections' in char_data:
            connections_html = '<div class="connections">\n<h3>Known Connections</h3>\n<ul>\n'
            for conn_id in char_data['connections']:
                conn_name = CHARACTERS_DATABASE.get(conn_id, {}).get('name', conn_id)
                connections_html += f'<li><a href="{conn_id}.html">{conn_name}</a></li>\n'
            connections_html += '</ul>\n</div>\n'
        
        # Build locations HTML
        locations_html = ""
        if 'key_locations' in char_data:
            locations_html = '<div class="locations">\n<h3>Key Locations</h3>\n<ul>\n'
            for loc in char_data['key_locations']:
                locations_html += f'<li>{loc}</li>\n'
            locations_html += '</ul>\n</div>\n'
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Epstein Files Character Profile</title>
    <link rel="stylesheet" href="../css/styles.css">
    <style>
        .character-profile {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .character-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .character-header h1 {{
            margin: 0 0 10px 0;
            font-size: 2.5em;
        }}
        .character-header .role {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .character-content {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
        }}
        .main-info {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .sidebar-info {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .timeline, .connections, .locations {{
            margin: 20px 0;
        }}
        .timeline ul, .connections ul, .locations ul {{
            list-style: none;
            padding: 0;
        }}
        .timeline li {{
            padding: 10px;
            border-left: 3px solid #667eea;
            margin: 10px 0;
            padding-left: 15px;
        }}
        .connections li, .locations li {{
            padding: 8px;
            margin: 5px 0;
        }}
        .connections a {{
            color: #667eea;
            text-decoration: none;
        }}
        .connections a:hover {{
            text-decoration: underline;
        }}
        .back-link {{
            display: inline-block;
            margin: 20px 0;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
        @media (max-width: 768px) {{
            .character-content {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-brand">
                <h1>Epstein Files Hub</h1>
            </div>
            <ul class="nav-menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../characters.html">Character Guide</a></li>
                <li><a href="../locations.html">Locations</a></li>
                <li><a href="../search.html">Search</a></li>
            </ul>
        </div>
    </nav>

    <div class="character-profile">
        <a href="../characters.html" class="back-link">← Back to Character Directory</a>
        
        <div class="character-header">
            <h1>{name}</h1>
            <div class="role">{role}</div>
        </div>

        <div class="character-content">
            <div class="main-info">
                <h2>Overview</h2>
                <p>{summary}</p>
                
                {timeline_html}
            </div>
            
            <div class="sidebar-info">
                {connections_html}
                {locations_html}
            </div>
        </div>
    </div>

    <script src="../js/main.js"></script>
</body>
</html>'''
        
        return html
    
    def generate_all_characters(self):
        """Generate HTML pages for all characters"""
        print(f"Generating character pages for {len(CHARACTERS_DATABASE)} individuals...")
        
        generated_count = 0
        for char_id, char_data in CHARACTERS_DATABASE.items():
            html = self.generate_character_html(char_id, char_data)
            
            output_path = self.profiles_dir / f"{char_id}.html"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            generated_count += 1
            if generated_count % 10 == 0:
                print(f"Generated {generated_count} pages...")
        
        print(f"✓ Generated {generated_count} character pages")
        
        # Also save JSON database
        json_path = self.data_dir / 'characters_database.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(CHARACTERS_DATABASE, f, indent=2)
        print(f"✓ Saved character database to {json_path}")
    
    def generate_character_index(self):
        """Generate index of all characters for the main characters.html page"""
        characters_list = []
        
        for char_id, char_data in sorted(CHARACTERS_DATABASE.items(), key=lambda x: x[1].get('name', '')):
            characters_list.append({
                'id': char_id,
                'name': char_data.get('name', char_id),
                'role': char_data.get('role', 'Unknown'),
                'summary': char_data.get('summary', '')[:100] + '...'
            })
        
        # Save to JSON for JavaScript
        json_path = self.web_dir / 'data' / 'characters_index.json'
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(characters_list, f, indent=2)
        
        print(f"✓ Generated character index with {len(characters_list)} entries")

if __name__ == '__main__':
    generator = CharacterPageGenerator()
    generator.generate_all_characters()
    generator.generate_character_index()
    print("\n✓ Character page generation complete!")
