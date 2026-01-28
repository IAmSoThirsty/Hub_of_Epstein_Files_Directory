#!/usr/bin/env python3
"""
Example: Advanced Hub Usage

Demonstrates advanced usage with full pipeline and subsystem access.
"""

from epstein_files import Hub


def main():
    """Run advanced hub operations."""
    print("Epstein Files Hub - Advanced Example")
    print("=" * 50)
    
    # Initialize with custom config
    print("\n1. Initializing Hub with configuration...")
    hub = Hub()
    hub.config.set("debug_mode", True)
    hub.config.set("max_workers", 8)
    print(f"   Debug mode: {hub.config.get('debug_mode')}")
    print(f"   Max workers: {hub.config.get('max_workers')}")
    
    # Run full pipeline
    print("\n2. Running full pipeline...")
    pipeline_results = hub.run_full_pipeline(force_refresh=False)
    print(f"   Started: {pipeline_results['started_at']}")
    print(f"   Completed: {pipeline_results['completed_at']}")
    print(f"   Steps completed: {len(pipeline_results['steps'])}")
    
    # Access subsystems directly
    print("\n3. Direct subsystem access...")
    
    # Public files
    print("\n   3a. Public Files Manager:")
    manifest = hub.public_files.get_manifest()
    print(f"       Manifest files: {len(manifest.get('files', []))}")
    
    # Wikipedia data
    print("\n   3b. Wikipedia Manager:")
    char_data = hub.wikipedia.fetch_character_data("Jeffrey Epstein")
    print(f"       Character: {char_data['name']}")
    
    # Agents
    print("\n   3c. Agent Manager:")
    agent_status = hub.agents.get_status()
    print(f"       Total agents: {agent_status['total_agents']}")
    print(f"       Active agents: {agent_status['active_agents']}")
    
    # Cache management
    print("\n4. Cache management...")
    cache_stats = hub.cache.get_stats()
    print(f"   Total entries: {cache_stats['total_entries']}")
    print(f"   Total size: {cache_stats['total_size_mb']} MB")
    
    # Data statistics
    print("\n5. Data statistics...")
    stats = hub.data.get_statistics()
    print(f"   Public files:")
    print(f"     - FBI Vault: {stats['public_files']['fbi_vault']}")
    print(f"     - DOJ: {stats['public_files']['doj']}")
    print(f"     - Total: {stats['public_files']['total']}")
    
    print("\n" + "=" * 50)
    print("Advanced example completed successfully!")


if __name__ == "__main__":
    main()
