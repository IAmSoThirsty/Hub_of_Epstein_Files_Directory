#!/usr/bin/env python3
"""
Example: Context Manager Usage

Demonstrates using Hub as a context manager for automatic cleanup.
"""

from epstein_files import Hub


def main():
    """Run hub with context manager."""
    print("Epstein Files Hub - Context Manager Example")
    print("=" * 50)
    
    # Use Hub as context manager (automatic cleanup on exit)
    with Hub() as hub:
        print("\n1. Hub initialized with context manager")
        
        # Fetch data
        print("\n2. Fetching public files...")
        results = hub.fetch_public_files()
        print(f"   Fetched: {results['total_files']} files")
        
        # Process documents
        print("\n3. Processing documents...")
        results = hub.process_documents()
        print(f"   Processed: {results['total_processed']} documents")
        
        # Generate index
        print("\n4. Generating search index...")
        results = hub.generate_search_index()
        print(f"   Indexed: {results.get('total_documents', 0)} documents")
        
        print("\n5. Context manager will auto-cleanup on exit")
    
    print("\n" + "=" * 50)
    print("Context manager example completed!")
    print("Cleanup was performed automatically.")


if __name__ == "__main__":
    main()
