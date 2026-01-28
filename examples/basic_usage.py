#!/usr/bin/env python3
"""
Example: Basic Hub Usage

Demonstrates basic usage of the Epstein Files Hub library.
"""

from epstein_files import Hub


def main():
    """Run basic hub operations."""
    print("Epstein Files Hub - Basic Example")
    print("=" * 50)
    
    # Initialize the hub
    print("\n1. Initializing Hub...")
    hub = Hub()
    print(f"   Hub initialized: {hub}")
    
    # Get system status
    print("\n2. Getting system status...")
    status = hub.get_status()
    print(f"   Configuration valid: {status['config']['valid']}")
    print(f"   Total public files: {status['data']['public_files']['total']}")
    print(f"   Cache entries: {status['cache']['total_entries']}")
    
    # Fetch public files
    print("\n3. Fetching public files...")
    results = hub.fetch_public_files(sources=["fbi_vault"])
    print(f"   Files fetched: {results['total_files']}")
    
    # Process documents
    print("\n4. Processing documents...")
    results = hub.process_documents()
    print(f"   Documents processed: {results['total_processed']}")
    print(f"   Documents failed: {results['total_failed']}")
    
    # Generate search index
    print("\n5. Generating search index...")
    results = hub.generate_search_index()
    print(f"   Documents indexed: {results.get('total_documents', 0)}")
    
    # Get final statistics
    print("\n6. Final statistics...")
    stats = hub.data.get_statistics()
    print(f"   FBI Vault files: {stats['public_files']['fbi_vault']}")
    print(f"   Processed text files: {stats['processed']['text']}")
    
    # Cleanup
    print("\n7. Cleanup...")
    cleanup_results = hub.cleanup()
    print(f"   Temp files deleted: {cleanup_results['temp_files_deleted']}")
    print(f"   Cache entries cleaned: {cleanup_results['cache_entries_cleaned']}")
    
    print("\n" + "=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()
