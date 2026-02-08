#!/usr/bin/env python3
"""
Uncensored.ai Integration Tool
Fetches and processes Epstein-related files from the Uncensored.ai free database

Features:
- Continuous data extraction
- Automatic deduplication
- Category-based filtering
- Metadata extraction
- Rate limiting
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from epstein_files.core.hub import Hub


class UncensoredAIIntegrator:
    """Integrator for Uncensored.ai files."""
    
    def __init__(self, config_path=None):
        """
        Initialize the integrator.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.hub = Hub(config_path)
        self.output_dir = Path('data/uncensored_files')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch_all_categories(self, force_refresh=False):
        """
        Fetch all categories of Epstein files.
        
        Args:
            force_refresh: Force refresh even if cached
            
        Returns:
            Dictionary with fetch results
        """
        print("\n" + "=" * 60)
        print("  Uncensored.ai Integration - Fetch All")
        print("=" * 60)
        print()
        
        results = self.hub.fetch_uncensored_files(force_refresh=force_refresh)
        
        return results
    
    def fetch_category(self, category, force_refresh=False):
        """
        Fetch specific category of files.
        
        Args:
            category: Category to fetch
            force_refresh: Force refresh even if cached
            
        Returns:
            Dictionary with fetch results
        """
        print(f"\n📁 Fetching {category} from Uncensored.ai...")
        print("=" * 60)
        
        results = self.hub.fetch_uncensored_files(
            categories=[category],
            force_refresh=force_refresh
        )
        
        return results
    
    def display_results(self, results):
        """
        Display fetch results in a readable format.
        
        Args:
            results: Results dictionary
        """
        print("\n" + "=" * 60)
        print("  FETCH RESULTS")
        print("=" * 60)
        
        if results.get('status') == 'disabled':
            print("\n⚠️ Uncensored.ai integration is disabled")
            print("Enable it by setting UNCENSORED_AI_ENABLED=true in .env")
            return
        
        print(f"\n✅ Total files fetched: {results.get('total_files', 0)}")
        print(f"⏭️ Total files skipped (duplicates): {results.get('total_skipped', 0)}")
        
        if results.get('categories'):
            print("\n📊 Results by Category:")
            for category, cat_results in results['categories'].items():
                files_fetched = cat_results.get('files_fetched', 0)
                files_skipped = cat_results.get('files_skipped', 0)
                errors = len(cat_results.get('errors', []))
                
                print(f"  • {category.capitalize()}:")
                print(f"    - Fetched: {files_fetched}")
                print(f"    - Skipped: {files_skipped}")
                if errors > 0:
                    print(f"    - Errors: {errors}")
        
        # Save results to file
        results_file = self.output_dir / 'fetch_results.json'
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: {results_file}")
        print(f"📁 Files saved to: {self.output_dir}")
    
    def get_statistics(self):
        """Get and display statistics about fetched files."""
        stats = self.hub.uncensored_ai.get_statistics()
        
        print("\n" + "=" * 60)
        print("  UNCENSORED.AI STATISTICS")
        print("=" * 60)
        print(f"\n📊 Total files: {stats['total_files']}")
        print(f"💾 Total size: {stats['total_size_mb']} MB")
        
        if stats['by_category']:
            print("\n📁 Files by Category:")
            for category, count in stats['by_category'].items():
                print(f"  • {category.capitalize()}: {count} files")
        
        return stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch Epstein files from Uncensored.ai free database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch all categories
  python scripts/fetch-uncensored-files.py --all
  
  # Fetch specific category
  python scripts/fetch-uncensored-files.py --category documents
  
  # Force refresh (ignore cache)
  python scripts/fetch-uncensored-files.py --all --force
  
  # View statistics
  python scripts/fetch-uncensored-files.py --stats
  
  # Non-interactive mode (for automation)
  python scripts/fetch-uncensored-files.py --all --non-interactive
        """
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Fetch all categories'
    )
    
    parser.add_argument(
        '--category',
        choices=['documents', 'images', 'videos', 'flight_logs', 'financial'],
        help='Fetch specific category'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force refresh (ignore cache)'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Display statistics only'
    )
    
    parser.add_argument(
        '--non-interactive',
        action='store_true',
        help='Run in non-interactive mode (for automation)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    
    # Print header
    print("=" * 60)
    print("  Uncensored.ai Integration Tool")
    print("  Epstein Files Hub")
    print("=" * 60)
    print()
    print("Fetching Epstein-related files from Uncensored.ai free database")
    print()
    
    # Initialize integrator
    try:
        integrator = UncensoredAIIntegrator(args.config)
    except Exception as e:
        print(f"❌ Error initializing: {e}")
        return 1
    
    # Display statistics
    if args.stats:
        integrator.get_statistics()
        return 0
    
    # Check if enabled
    if not integrator.hub.uncensored_ai.enabled:
        print("⚠️ Uncensored.ai integration is disabled")
        print("\nTo enable:")
        print("1. Copy .env.example to .env")
        print("2. Set UNCENSORED_AI_ENABLED=true")
        print("3. Optionally set UNCENSORED_AI_API_KEY if you have one")
        return 1
    
    # Determine what to fetch
    if not args.all and not args.category and not args.non_interactive:
        # Interactive mode
        print("What would you like to fetch?")
        print("1. All categories (documents, images, videos, flight logs, financial)")
        print("2. Documents only")
        print("3. Images only")
        print("4. Videos only")
        print("5. Flight logs only")
        print("6. Financial records only")
        print("7. View statistics")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == '0':
            print("Exiting...")
            return 0
        elif choice == '1':
            args.all = True
        elif choice == '2':
            args.category = 'documents'
        elif choice == '3':
            args.category = 'images'
        elif choice == '4':
            args.category = 'videos'
        elif choice == '5':
            args.category = 'flight_logs'
        elif choice == '6':
            args.category = 'financial'
        elif choice == '7':
            integrator.get_statistics()
            return 0
        else:
            print("Invalid choice")
            return 1
    
    # Fetch files
    if args.all:
        print("\n🚀 Fetching all categories...")
        results = integrator.fetch_all_categories(force_refresh=args.force)
        integrator.display_results(results)
    
    elif args.category:
        print(f"\n🚀 Fetching {args.category}...")
        results = integrator.fetch_category(args.category, force_refresh=args.force)
        integrator.display_results(results)
    
    else:
        print("No action specified. Use --all or --category")
        return 1
    
    # Next steps
    print("\n" + "=" * 60)
    print("✅ Integration complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review downloaded files in data/uncensored_files/")
    print("2. Run processing: python scripts/process-pdfs.py")
    print("3. Update search index: python scripts/generate-search-index.py")
    print("4. Commit changes (if within repository limits)")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
