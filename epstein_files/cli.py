"""
Command-line interface for Epstein Files Hub.
"""

import argparse
import sys
from pathlib import Path

from .core.hub import Hub


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Epstein Files Hub - Sovereign Level Monolithic Dense Library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  epstein-hub status                    # Get system status
  epstein-hub fetch                     # Fetch public files
  epstein-hub process                   # Process documents
  epstein-hub index                     # Generate search index
  epstein-hub pipeline                  # Run full pipeline
  epstein-hub cleanup                   # Clean up temp files
        """
    )
    
    parser.add_argument(
        'command',
        choices=['status', 'fetch', 'process', 'index', 'pipeline', 'cleanup'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force refresh/rebuild'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    # Initialize hub
    print(f"Epstein Files Hub - {args.command.upper()}")
    print("=" * 60)
    
    hub = Hub()
    
    if args.debug:
        hub.config.set("debug_mode", True)
    
    # Execute command
    try:
        if args.command == 'status':
            status = hub.get_status()
            print(f"\nConfiguration:")
            print(f"  Valid: {status['config']['valid']}")
            print(f"  Debug Mode: {status['config']['debug_mode']}")
            print(f"\nData:")
            print(f"  Public Files: {status['data']['public_files']['total']}")
            print(f"  FBI Vault: {status['data']['public_files']['fbi_vault']}")
            print(f"  DOJ: {status['data']['public_files']['doj']}")
            print(f"  Processed Text: {status['data']['processed']['text']}")
            print(f"\nCache:")
            print(f"  Entries: {status['cache']['total_entries']}")
            print(f"  Size: {status['cache']['total_size_mb']} MB")
            
        elif args.command == 'fetch':
            print("\nFetching public files...")
            results = hub.fetch_public_files(force_refresh=args.force)
            print(f"Fetched: {results['total_files']} files")
            
        elif args.command == 'process':
            print("\nProcessing documents...")
            results = hub.process_documents()
            print(f"Processed: {results['total_processed']} documents")
            print(f"Failed: {results['total_failed']} documents")
            
        elif args.command == 'index':
            print("\nGenerating search index...")
            results = hub.generate_search_index(force_rebuild=args.force)
            print(f"Indexed: {results.get('total_documents', 0)} documents")
            
        elif args.command == 'pipeline':
            print("\nRunning full pipeline...")
            results = hub.run_full_pipeline(force_refresh=args.force)
            print(f"Started: {results['started_at']}")
            print(f"Completed: {results['completed_at']}")
            print(f"Steps: {len(results['steps'])}")
            
        elif args.command == 'cleanup':
            print("\nCleaning up...")
            results = hub.cleanup()
            print(f"Temp files deleted: {results['temp_files_deleted']}")
            print(f"Cache entries cleaned: {results['cache_entries_cleaned']}")
        
        print("\n" + "=" * 60)
        print("Command completed successfully!")
        
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
