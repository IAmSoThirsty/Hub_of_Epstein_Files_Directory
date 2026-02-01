#!/usr/bin/env python3
"""
Location Pages Generator
Creates comprehensive pages for all key locations
"""

import json
from pathlib import Path
from typing import Dict, List

LOCATIONS_DATABASE = {
    "little_st_james": {
        "name": "Little St. James Island",
        "type": "Private Island",
        "location": "U.S. Virgin Islands",
        "coordinates": "18.300°N 64.825°W",
        "size": "70-78 acres",
        "nickname": "Pedophile Island",
        "acquired": "1998",
        "sold": "2023",
        "description": "Private island owned by Jeffrey Epstein from 1998 until his death. The island featured a main compound, guest houses, and became central to trafficking allegations.",
        "key_features": [
            "Main residence compound",
            "Guest villas",
            "Temple-like structure",
            "Helipad",
            "Private beaches",
            "Dock facilities"
        ],
        "significance": "Central location in trafficking allegations. Multiple victims reported being taken to the island.",
        "timeline": [
            {"date": "1998", "event": "Purchased by Epstein for $7.95 million"},
            {"date": "2019", "event": "FBI raid following Epstein's arrest"},
            {"date": "2023", "event": "Sold by estate"}
        ],
        "related_characters": ["jeffrey_epstein", "ghislaine_maxwell"],
        "images": ["little_st_james_aerial.jpg", "temple_structure.jpg"]
    },
    "great_st_james": {
        "name": "Great St. James Island",
        "type": "Private Island",
        "location": "U.S. Virgin Islands",
        "acquired": "2016",
        "size": "165 acres",
        "description": "Larger island adjacent to Little St. James, purchased by Epstein in 2016.",
        "timeline": [
            {"date": "2016", "event": "Purchased by Epstein"},
            {"date": "2023", "event": "Sold by estate"}
        ],
        "related_characters": ["jeffrey_epstein"]
    },
    "palm_beach": {
        "name": "Palm Beach Residence",
        "type": "Private Residence",
        "location": "358 El Brillo Way, Palm Beach, Florida",
        "acquired": "1990",
        "description": "Epstein's Florida mansion where many of the initial allegations originated. This was a key location in the 2005 police investigation.",
        "key_features": [
            "Large mansion",
            "Multiple bedrooms",
            "Pool area",
            "Security systems"
        ],
        "significance": "Site of initial 2005 investigation. Multiple victims recruited from the area.",
        "timeline": [
            {"date": "1990", "event": "Purchased by Epstein"},
            {"date": "2005", "event": "Police investigation begins"},
            {"date": "2019", "event": "Property inventoried after arrest"}
        ],
        "related_characters": ["jeffrey_epstein", "ghislaine_maxwell", "virginia_giuffre"],
        "images": ["palm_beach_exterior.jpg"]
    },
    "new_york": {
        "name": "Manhattan Townhouse",
        "type": "Private Residence",
        "location": "9 East 71st Street, Manhattan, New York",
        "acquired": "1996",
        "size": "21,000 square feet",
        "description": "Epstein's massive Manhattan townhouse, one of the largest private residences in New York City. Originally owned by Leslie Wexner.",
        "key_features": [
            "7 floors",
            "40 rooms",
            "Elevator",
            "Extensive art collection",
            "Security systems"
        ],
        "significance": "Major location for meetings with high-profile individuals. Site of alleged abuse.",
        "timeline": [
            {"date": "1989", "event": "Purchased by Leslie Wexner"},
            {"date": "1996", "event": "Transferred to Epstein"},
            {"date": "2019", "event": "FBI search after arrest"}
        ],
        "related_characters": ["jeffrey_epstein", "leslie_wexner", "ghislaine_maxwell"],
        "images": ["nyc_townhouse.jpg"]
    },
    "paris": {
        "name": "Paris Apartment",
        "type": "Private Residence",
        "location": "Avenue Foch, Paris, France",
        "description": "Luxury apartment in one of Paris's most exclusive neighborhoods.",
        "related_characters": ["jeffrey_epstein", "jean_luc_brunel"],
    },
    "new_mexico": {
        "name": "Zorro Ranch",
        "type": "Ranch",
        "location": "Stanley, New Mexico",
        "size": "7,500 acres",
        "acquired": "1993",
        "description": "Sprawling ranch in New Mexico where Epstein allegedly planned to seed the human race with his DNA.",
        "key_features": [
            "Main residence",
            "Airstrip",
            "Equestrian facilities",
            "Guest houses"
        ],
        "significance": "Location of alleged abuse. Epstein spoke of creating a 'baby ranch' here.",
        "timeline": [
            {"date": "1993", "event": "Purchased by Epstein"}
        ],
        "related_characters": ["jeffrey_epstein"],
    },
    "mar_a_lago": {
        "name": "Mar-a-Lago Club",
        "type": "Private Club/Resort",
        "location": "Palm Beach, Florida",
        "description": "Exclusive resort where Virginia Giuffre was recruited while working as a spa attendant.",
        "significance": "Location where Ghislaine Maxwell recruited Virginia Giuffre in 1998.",
        "timeline": [
            {"date": "1998", "event": "Virginia Giuffre recruited here"}
        ],
        "related_characters": ["virginia_giuffre", "ghislaine_maxwell", "donald_trump"]
    },
    "manhattan_jail": {
        "name": "Metropolitan Correctional Center",
        "type": "Federal Prison",
        "location": "Manhattan, New York",
        "description": "Federal detention facility where Epstein was held and died in 2019.",
        "significance": "Site of Epstein's death on August 10, 2019.",
        "timeline": [
            {"date": "2019-07-06", "event": "Epstein detained here"},
            {"date": "2019-07-23", "event": "Found injured in cell"},
            {"date": "2019-08-10", "event": "Found dead in cell"}
        ],
        "related_characters": ["jeffrey_epstein"]
    }
}

class LocationPageGenerator:
    """Generates location profile pages"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.web_dir = self.project_root / 'web'
        self.locations_dir = self.web_dir / 'locations'
        self.locations_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_location_html(self, loc_id: str, loc_data: Dict) -> str:
        """Generate HTML for a single location"""
        name = loc_data.get('name', loc_id.replace('_', ' ').title())
        loc_type = loc_data.get('type', 'Location')
        location = loc_data.get('location', 'Unknown')
        description = loc_data.get('description', 'No description available')
        
        # Build features HTML
        features_html = ""
        if 'key_features' in loc_data:
            features_html = '<div class="features"><h3>Key Features</h3><ul>\n'
            for feature in loc_data['key_features']:
                features_html += f'<li>{feature}</li>\n'
            features_html += '</ul></div>\n'
        
        # Build timeline HTML
        timeline_html = ""
        if 'timeline' in loc_data:
            timeline_html = '<div class="timeline"><h3>Timeline</h3><ul>\n'
            for event in loc_data['timeline']:
                date = event.get('date', 'Unknown')
                evt = event.get('event', '')
                timeline_html += f'<li><strong>{date}:</strong> {evt}</li>\n'
            timeline_html += '</ul></div>\n'
        
        # Build related characters HTML
        chars_html = ""
        if 'related_characters' in loc_data:
            chars_html = '<div class="related-characters"><h3>Related Individuals</h3><ul>\n'
            for char_id in loc_data['related_characters']:
                chars_html += f'<li><a href="../profiles/{char_id}.html">{char_id.replace("_", " ").title()}</a></li>\n'
            chars_html += '</ul></div>\n'
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Epstein Files Location</title>
    <link rel="stylesheet" href="../css/styles.css">
    <style>
        .location-profile {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .location-header {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .location-header h1 {{
            margin: 0 0 10px 0;
            font-size: 2.5em;
        }}
        .location-header .type {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .location-content {{
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
        .timeline ul, .features ul, .related-characters ul {{
            list-style: none;
            padding: 0;
        }}
        .timeline li {{
            padding: 10px;
            border-left: 3px solid #f5576c;
            margin: 10px 0;
            padding-left: 15px;
        }}
        .back-link {{
            display: inline-block;
            margin: 20px 0;
            padding: 10px 20px;
            background: #f5576c;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
        @media (max-width: 768px) {{
            .location-content {{
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

    <div class="location-profile">
        <a href="../locations.html" class="back-link">← Back to Locations</a>
        
        <div class="location-header">
            <h1>{name}</h1>
            <div class="type">{loc_type} • {location}</div>
        </div>

        <div class="location-content">
            <div class="main-info">
                <h2>Overview</h2>
                <p>{description}</p>
                
                {features_html}
                {timeline_html}
            </div>
            
            <div class="sidebar-info">
                {chars_html}
            </div>
        </div>
    </div>

    <script src="../js/main.js"></script>
</body>
</html>'''
        
        return html
    
    def generate_all_locations(self):
        """Generate HTML pages for all locations"""
        print(f"Generating location pages for {len(LOCATIONS_DATABASE)} locations...")
        
        for loc_id, loc_data in LOCATIONS_DATABASE.items():
            html = self.generate_location_html(loc_id, loc_data)
            
            output_path = self.locations_dir / f"{loc_id}.html"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
        
        print(f"✓ Generated {len(LOCATIONS_DATABASE)} location pages")
        
        # Save JSON database
        json_path = self.project_root / 'data' / 'locations' / 'locations_database.json'
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(LOCATIONS_DATABASE, f, indent=2)
        print(f"✓ Saved locations database")

if __name__ == '__main__':
    generator = LocationPageGenerator()
    generator.generate_all_locations()
    print("\n✓ Location page generation complete!")
