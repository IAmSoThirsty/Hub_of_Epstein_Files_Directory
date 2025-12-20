#!/usr/bin/env python3
"""
Generate static search index from documents for client-side search
This enables the free tier by pre-computing search data
"""

import json
import os
from pathlib import Path
from datetime import datetime

def generate_search_index():
    """Generate static search index from documents"""
    
    print("🔍 Generating search index for free tier...")
    
    # Sample documents for demonstration
    # In production, these would be loaded from actual document files
    documents = [
        {
            'id': 'DOC-2019-001',
            'title': 'Flight Log Entry - December 1999',
            'content': 'Flight manifest showing passengers traveling to Little St. James island. Multiple redacted names present in passenger list. This document was obtained through FOIA requests and contains critical travel information.',
            'date': '1999-12-15',
            'location': 'Little St. James Island',
            'person': 'Jeffrey Epstein',
            'redaction_status': 'Partially Redacted',
            'case_number': 'CV-2019-001',
            'type': 'Flight Log',
            'relevance': 95,
            'tags': ['Travel', 'Island', 'FOIA', 'Flight Records']
        },
        {
            'id': 'IMG-2008-032',
            'title': 'Photographic Evidence - Island Facility',
            'content': 'Aerial and ground-level photographs of structures and facilities on Little St. James island. Shows property layout, buildings, and infrastructure. High-resolution images available.',
            'date': '2008-07-14',
            'location': 'Little St. James Island',
            'person': 'Jeffrey Epstein',
            'redaction_status': 'Unredacted',
            'case_number': 'INV-2019-9878',
            'type': 'Photograph',
            'relevance': 85,
            'tags': ['Photos', 'Evidence', 'Property', 'Island']
        },
        {
            'id': 'DOC-2006-145',
            'title': 'Financial Transaction Records',
            'content': 'Bank statements and wire transfer records showing financial transactions related to property acquisitions and operational expenses. Documents span multiple years and jurisdictions.',
            'date': '2006-03-22',
            'location': 'Manhattan',
            'person': 'Jeffrey Epstein',
            'redaction_status': 'Partially Redacted',
            'case_number': 'CV-2019-001',
            'type': 'Financial Record',
            'relevance': 78,
            'tags': ['Financial', 'Transactions', 'Property']
        },
        {
            'id': 'DOC-2015-089',
            'title': 'Deposition Transcript - Civil Case',
            'content': 'Sealed deposition testimony from civil proceedings. Contains witness statements and cross-examination records. Multiple parties involved.',
            'date': '2015-11-03',
            'location': 'Florida',
            'person': 'Multiple Witnesses',
            'redaction_status': 'Sealed',
            'case_number': 'CV-2015-3456',
            'type': 'Court Document',
            'relevance': 92,
            'tags': ['Deposition', 'Legal', 'Testimony']
        },
        {
            'id': 'DOC-2019-234',
            'title': 'Property Deed - Palm Beach Residence',
            'content': 'Official property records for Palm Beach residence including deed transfers, property boundaries, and historical ownership records.',
            'date': '2019-08-12',
            'location': 'Palm Beach',
            'person': 'Jeffrey Epstein',
            'redaction_status': 'Unredacted',
            'case_number': 'N/A',
            'type': 'Property Record',
            'relevance': 70,
            'tags': ['Property', 'Real Estate', 'Palm Beach']
        },
        {
            'id': 'DOC-2020-056',
            'title': 'Victim Impact Statement',
            'content': 'Statement from victim detailing experiences and impact. Contains sensitive information protected by court order. Full statement available under restricted access.',
            'date': '2020-01-15',
            'location': 'New York',
            'person': 'Victim',
            'redaction_status': 'Heavily Redacted',
            'case_number': 'CR-2019-7654',
            'type': 'Legal Document',
            'relevance': 88,
            'tags': ['Victim', 'Legal', 'Statement']
        },
        {
            'id': 'DOC-2016-178',
            'title': 'Flight Logs - International Travel',
            'content': 'Comprehensive flight logs showing international travel patterns, passenger manifests, and destination records across multiple years.',
            'date': '2016-05-20',
            'location': 'Paris',
            'person': 'Multiple Passengers',
            'redaction_status': 'Partially Redacted',
            'case_number': 'INV-2019-001',
            'type': 'Flight Log',
            'relevance': 82,
            'tags': ['Travel', 'International', 'Flight Records']
        },
        {
            'id': 'DOC-2019-445',
            'title': 'Address Book - Contact Information',
            'content': 'Personal address book containing contact information for numerous individuals. Contains names, phone numbers, and addresses.',
            'date': '2019-07-08',
            'location': 'Manhattan',
            'person': 'Jeffrey Epstein',
            'redaction_status': 'Unredacted',
            'case_number': 'N/A',
            'type': 'Personal Document',
            'relevance': 75,
            'tags': ['Contacts', 'Address Book', 'Associates']
        }
    ]
    
    # Ensure output directory exists
    output_dir = Path('web/js')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate JavaScript file with search data
    output_path = output_dir / 'search-index.js'
    
    with open(output_path, 'w') as f:
        f.write('// Auto-generated search index for client-side search\n')
        f.write(f'// Generated: {datetime.now().isoformat()}\n')
        f.write(f'// Total documents: {len(documents)}\n\n')
        f.write('const SEARCH_DATA = ')
        f.write(json.dumps(documents, indent=2))
        f.write(';\n\n')
        f.write('// Export for use in search.js\n')
        f.write('if (typeof module !== "undefined" && module.exports) {\n')
        f.write('  module.exports = SEARCH_DATA;\n')
        f.write('}\n')
    
    print(f"✅ Generated search index with {len(documents)} documents")
    print(f"📄 Output: {output_path}")
    print(f"📊 Total size: {output_path.stat().st_size / 1024:.2f} KB")
    
    # Generate statistics
    stats = {
        'total_documents': len(documents),
        'by_type': {},
        'by_location': {},
        'by_redaction_status': {},
        'date_range': {
            'earliest': min(doc['date'] for doc in documents),
            'latest': max(doc['date'] for doc in documents)
        }
    }
    
    for doc in documents:
        # Count by type
        doc_type = doc['type']
        stats['by_type'][doc_type] = stats['by_type'].get(doc_type, 0) + 1
        
        # Count by location
        location = doc['location']
        stats['by_location'][location] = stats['by_location'].get(location, 0) + 1
        
        # Count by redaction status
        status = doc['redaction_status']
        stats['by_redaction_status'][status] = stats['by_redaction_status'].get(status, 0) + 1
    
    # Save statistics
    stats_path = output_dir / 'search-stats.json'
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n📈 Statistics:")
    print(f"   Document types: {len(stats['by_type'])}")
    print(f"   Locations: {len(stats['by_location'])}")
    print(f"   Date range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
    
    return documents, stats


def generate_metadata():
    """Generate metadata file for the index"""
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'version': '1.0.0',
        'index_type': 'client-side',
        'search_library': 'lunr.js',
        'features': [
            'full-text search',
            'filter by date',
            'filter by location',
            'filter by redaction status',
            'filter by document type',
            'relevance scoring'
        ],
        'performance': {
            'estimated_load_time': '< 500ms',
            'search_time': '< 100ms',
            'supports_offline': True
        }
    }
    
    output_path = Path('web/js/search-metadata.json')
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n📋 Generated metadata: {output_path}")


if __name__ == '__main__':
    print("=" * 60)
    print("  Free Tier Search Index Generator")
    print("  Epstein Files Hub")
    print("=" * 60)
    print()
    
    documents, stats = generate_search_index()
    generate_metadata()
    
    print("\n" + "=" * 60)
    print("✅ Index generation complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review generated files in web/js/")
    print("2. Test search functionality locally")
    print("3. Commit and push to GitHub")
    print("4. GitHub Pages will auto-deploy")
    print("\n💡 This enables FREE tier with $0/month costs!")
