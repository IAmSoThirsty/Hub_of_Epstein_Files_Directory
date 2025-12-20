#!/usr/bin/env python3
"""
Public Files Integration Tool
Fetches and processes publicly available Epstein-related files from official sources

Sources:
- DOJ flight logs (text files)
- FBI vault PDFs (21-22 files)
- Other publicly available government documents
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
import hashlib
import time

# Known public sources
PUBLIC_SOURCES = {
    'fbi_vault': {
        'name': 'FBI Vault - Jeffrey Epstein',
        'base_url': 'https://vault.fbi.gov/jeffrey-epstein',
        'files': [
            'jeffrey-epstein-part-01-of-22/view',
            'jeffrey-epstein-part-02-of-22/view',
            'jeffrey-epstein-part-03-of-22/view',
            'jeffrey-epstein-part-04-of-22/view',
            'jeffrey-epstein-part-05-of-22/view',
            'jeffrey-epstein-part-06-of-22/view',
            'jeffrey-epstein-part-07-of-22/view',
            'jeffrey-epstein-part-08-of-22/view',
            'jeffrey-epstein-part-09-of-22/view',
            'jeffrey-epstein-part-10-of-22/view',
            'jeffrey-epstein-part-11-of-22/view',
            'jeffrey-epstein-part-12-of-22/view',
            'jeffrey-epstein-part-13-of-22/view',
            'jeffrey-epstein-part-14-of-22/view',
            'jeffrey-epstein-part-15-of-22/view',
            'jeffrey-epstein-part-16-of-22/view',
            'jeffrey-epstein-part-17-of-22/view',
            'jeffrey-epstein-part-18-of-22/view',
            'jeffrey-epstein-part-19-of-22/view',
            'jeffrey-epstein-part-20-of-22/view',
            'jeffrey-epstein-part-21-of-22/view',
            'jeffrey-epstein-part-22-of-22/view',
        ]
    },
    'doj_flight_logs': {
        'name': 'DOJ Flight Logs',
        'base_url': 'https://www.documentcloud.org/documents',
        'files': [
            # Flight logs are often hosted on DocumentCloud or similar services
            # These would need to be updated with actual URLs when available
        ]
    }
}

class PublicFilesIntegrator:
    def __init__(self, output_dir='data/public_files'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / 'fbi_vault').mkdir(exist_ok=True)
        (self.output_dir / 'doj_flight_logs').mkdir(exist_ok=True)
        (self.output_dir / 'metadata').mkdir(exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; EpsteinFilesBot/1.0; +https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory)'
        })
    
    def download_file(self, url, output_path, source_name):
        """Download a file with retry logic"""
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                print(f"  Downloading: {url}")
                response = self.session.get(url, timeout=30, stream=True)
                response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                file_size = output_path.stat().st_size
                print(f"  ✅ Downloaded: {file_size / 1024:.2f} KB")
                
                # Generate metadata
                file_hash = self.calculate_hash(output_path)
                metadata = {
                    'source': source_name,
                    'url': url,
                    'download_date': datetime.now().isoformat(),
                    'file_size': file_size,
                    'sha256': file_hash,
                    'file_path': str(output_path)
                }
                
                return metadata
                
            except Exception as e:
                print(f"  ⚠️ Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"  Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"  ❌ Failed after {max_retries} attempts")
                    return None
    
    def calculate_hash(self, file_path):
        """Calculate SHA-256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def fetch_fbi_vault_files(self):
        """Fetch all FBI Vault PDF files"""
        print("\n📁 Fetching FBI Vault Files...")
        print("=" * 60)
        
        source = PUBLIC_SOURCES['fbi_vault']
        metadata_list = []
        
        for i, file_path in enumerate(source['files'], 1):
            print(f"\n[{i}/{len(source['files'])}] FBI Vault Part {i:02d}")
            
            # Construct download URL
            # Note: FBI Vault URLs may need adjustment based on actual structure
            file_url = f"{source['base_url']}/{file_path}"
            output_path = self.output_dir / 'fbi_vault' / f'epstein-part-{i:02d}.pdf'
            
            if output_path.exists():
                print(f"  ℹ️ Already downloaded: {output_path}")
                # Load existing metadata
                meta_file = self.output_dir / 'metadata' / f'fbi-vault-{i:02d}.json'
                if meta_file.exists():
                    with open(meta_file, 'r') as f:
                        metadata_list.append(json.load(f))
                continue
            
            metadata = self.download_file(file_url, output_path, 'FBI Vault')
            
            if metadata:
                # Save individual metadata
                meta_file = self.output_dir / 'metadata' / f'fbi-vault-{i:02d}.json'
                with open(meta_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                metadata_list.append(metadata)
                
                # Be respectful - rate limit
                time.sleep(2)
        
        # Save combined metadata
        combined_meta = self.output_dir / 'metadata' / 'fbi_vault_complete.json'
        with open(combined_meta, 'w') as f:
            json.dump({
                'source': 'FBI Vault',
                'total_files': len(metadata_list),
                'download_date': datetime.now().isoformat(),
                'files': metadata_list
            }, f, indent=2)
        
        print(f"\n✅ FBI Vault: {len(metadata_list)} files processed")
        return metadata_list
    
    def fetch_doj_flight_logs(self):
        """Fetch DOJ flight log text files"""
        print("\n✈️ Fetching DOJ Flight Logs...")
        print("=" * 60)
        
        # Note: Actual DOJ flight log URLs would need to be provided
        # This is a placeholder structure
        
        print("ℹ️ DOJ flight logs require manual URL configuration")
        print("Please update PUBLIC_SOURCES['doj_flight_logs']['files'] with actual URLs")
        
        # Example structure for when URLs are available:
        """
        source = PUBLIC_SOURCES['doj_flight_logs']
        metadata_list = []
        
        for i, file_url in enumerate(source['files'], 1):
            output_path = self.output_dir / 'doj_flight_logs' / f'flight-log-{i:02d}.txt'
            metadata = self.download_file(file_url, output_path, 'DOJ Flight Logs')
            if metadata:
                metadata_list.append(metadata)
        
        return metadata_list
        """
        
        return []
    
    def generate_download_manifest(self):
        """Generate a manifest of all available public files"""
        manifest = {
            'generated_at': datetime.now().isoformat(),
            'sources': {},
            'total_files': 0,
            'instructions': 'Use this manifest to track publicly available files'
        }
        
        for source_key, source_info in PUBLIC_SOURCES.items():
            manifest['sources'][source_key] = {
                'name': source_info['name'],
                'base_url': source_info['base_url'],
                'file_count': len(source_info['files']),
                'files': source_info['files']
            }
            manifest['total_files'] += len(source_info['files'])
        
        manifest_path = self.output_dir / 'download_manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"\n📋 Manifest saved: {manifest_path}")
        return manifest


def main():
    print("=" * 60)
    print("  Public Files Integration Tool")
    print("  Epstein Files Hub")
    print("=" * 60)
    print()
    print("This tool fetches publicly available files from:")
    print("  • FBI Vault (22 PDF files)")
    print("  • DOJ Flight Logs (text files)")
    print("  • Other official government sources")
    print()
    print("⚠️ Note: Large downloads may take time. Be patient!")
    print()
    
    integrator = PublicFilesIntegrator()
    
    # Generate manifest
    print("📋 Generating download manifest...")
    manifest = integrator.generate_download_manifest()
    
    # Fetch files
    choice = input("\nFetch FBI Vault files now? (y/n): ").lower()
    if choice == 'y':
        fbi_files = integrator.fetch_fbi_vault_files()
        print(f"\n✅ Downloaded {len(fbi_files)} FBI Vault files")
    else:
        print("\nℹ️ Skipping FBI Vault downloads")
    
    choice = input("\nFetch DOJ Flight Logs now? (y/n): ").lower()
    if choice == 'y':
        doj_files = integrator.fetch_doj_flight_logs()
        print(f"\n✅ Downloaded {len(doj_files)} DOJ files")
    else:
        print("\nℹ️ Skipping DOJ downloads")
    
    print("\n" + "=" * 60)
    print("✅ Integration complete!")
    print("=" * 60)
    print(f"\nFiles saved to: {integrator.output_dir}")
    print("\nNext steps:")
    print("1. Review downloaded files in data/public_files/")
    print("2. Run OCR processing: python scripts/process-pdfs.py")
    print("3. Generate search index: python scripts/generate-search-index.py")
    print("4. Commit to repository (if within size limits)")


if __name__ == '__main__':
    main()
