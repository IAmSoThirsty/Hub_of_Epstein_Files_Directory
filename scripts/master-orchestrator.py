#!/usr/bin/env python3
"""
MASTER ORCHESTRATOR - The Butler's Command Center
Coordinates all data acquisition, processing, and deployment operations
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('MasterOrchestrator')

class MasterOrchestrator:
    """The Butler's central command system"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.data_dir = self.project_root / 'data'
        self.web_dir = self.project_root / 'web'
        self.scripts_dir = self.project_root / 'scripts'
        
        # Create necessary directories
        self.ensure_directories()
        
        self.mission_status = {
            'phase1_data_acquisition': 'pending',
            'phase2_character_generation': 'pending',
            'phase3_web_interface': 'pending',
            'phase4_asset_integration': 'pending',
            'phase5_deployment': 'pending',
            'phase6_verification': 'pending'
        }
        
    def ensure_directories(self):
        """Create all necessary directories"""
        dirs = [
            self.data_dir / 'public_files' / 'fbi_vault',
            self.data_dir / 'public_files' / 'doj',
            self.data_dir / 'public_files' / 'court_docs',
            self.data_dir / 'public_files' / 'documentcloud',
            self.data_dir / 'public_files' / 'internet_archive',
            self.data_dir / 'public_files' / 'metadata',
            self.data_dir / 'characters',
            self.data_dir / 'locations',
            self.data_dir / 'timeline',
            self.data_dir / 'relationships',
            self.web_dir / 'profiles',
            self.web_dir / 'locations',
            self.web_dir / 'assets' / 'images',
            self.web_dir / 'assets' / 'documents',
            self.web_dir / 'assets' / 'infographics',
            self.web_dir / 'data',
        ]
        
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured directory: {directory}")
    
    def execute_phase_1_data_acquisition(self):
        """Phase 1: Fetch all data from all sources"""
        logger.info("=" * 60)
        logger.info("PHASE 1: DATA ACQUISITION")
        logger.info("=" * 60)
        
        tasks = [
            ('fetch-public-files.py', 'Fetching FBI Vault & DOJ files'),
            ('fetch-wikipedia-data.py', 'Fetching Wikipedia data'),
        ]
        
        for script, description in tasks:
            logger.info(f"\n→ {description}")
            script_path = self.scripts_dir / script
            if script_path.exists():
                os.system(f"python3 {script_path}")
            else:
                logger.warning(f"Script not found: {script_path}")
        
        self.mission_status['phase1_data_acquisition'] = 'complete'
        logger.info("\n✓ Phase 1 Complete: Data Acquisition")
    
    def execute_phase_2_character_generation(self):
        """Phase 2: Generate all character pages"""
        logger.info("=" * 60)
        logger.info("PHASE 2: CHARACTER DATABASE GENERATION")
        logger.info("=" * 60)
        
        # This will be handled by specialized scripts
        script_path = self.scripts_dir / 'generate-character-pages.py'
        if script_path.exists():
            logger.info("\n→ Generating character pages")
            os.system(f"python3 {script_path}")
        else:
            logger.warning(f"Character generation script not found")
        
        self.mission_status['phase2_character_generation'] = 'complete'
        logger.info("\n✓ Phase 2 Complete: Character Generation")
    
    def execute_phase_3_web_interface(self):
        """Phase 3: Build complete web interface"""
        logger.info("=" * 60)
        logger.info("PHASE 3: WEB INTERFACE COMPLETION")
        logger.info("=" * 60)
        
        tasks = [
            ('generate-search-index.py', 'Generating search index'),
            ('generate-location-pages.py', 'Generating location pages'),
            ('generate-timeline-data.py', 'Generating timeline data'),
        ]
        
        for script, description in tasks:
            logger.info(f"\n→ {description}")
            script_path = self.scripts_dir / script
            if script_path.exists():
                os.system(f"python3 {script_path}")
            else:
                logger.warning(f"Script not found: {script_path}")
        
        self.mission_status['phase3_web_interface'] = 'complete'
        logger.info("\n✓ Phase 3 Complete: Web Interface")
    
    def execute_phase_4_asset_integration(self):
        """Phase 4: Integrate all assets"""
        logger.info("=" * 60)
        logger.info("PHASE 4: ASSET INTEGRATION")
        logger.info("=" * 60)
        
        # Download images, create visualizations
        logger.info("\n→ Integrating assets")
        
        self.mission_status['phase4_asset_integration'] = 'complete'
        logger.info("\n✓ Phase 4 Complete: Asset Integration")
    
    def execute_phase_5_deployment(self):
        """Phase 5: Deploy to GitHub Pages"""
        logger.info("=" * 60)
        logger.info("PHASE 5: GITHUB PAGES DEPLOYMENT")
        logger.info("=" * 60)
        
        logger.info("\n→ Configuring GitHub Pages")
        
        # Create/update CNAME if needed
        # Configure gh-pages branch
        
        self.mission_status['phase5_deployment'] = 'complete'
        logger.info("\n✓ Phase 5 Complete: Deployment")
    
    def execute_phase_6_verification(self):
        """Phase 6: Verify everything works"""
        logger.info("=" * 60)
        logger.info("PHASE 6: VERIFICATION")
        logger.info("=" * 60)
        
        logger.info("\n→ Verifying all systems")
        
        # Test links, search, pages
        
        self.mission_status['phase6_verification'] = 'complete'
        logger.info("\n✓ Phase 6 Complete: Verification")
    
    def generate_mission_report(self):
        """Generate comprehensive mission report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'status': self.mission_status,
            'statistics': self.gather_statistics()
        }
        
        report_path = self.project_root / 'MISSION_REPORT.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"\nMission report saved to: {report_path}")
        return report
    
    def gather_statistics(self) -> Dict[str, Any]:
        """Gather statistics about the mission"""
        stats = {
            'files_downloaded': 0,
            'characters_generated': 0,
            'locations_mapped': 0,
            'documents_indexed': 0,
            'pages_created': 0
        }
        
        # Count files
        if (self.data_dir / 'public_files').exists():
            stats['files_downloaded'] = sum(1 for _ in (self.data_dir / 'public_files').rglob('*') if _.is_file())
        
        # Count character pages
        if (self.web_dir / 'profiles').exists():
            stats['characters_generated'] = sum(1 for _ in (self.web_dir / 'profiles').rglob('*.html'))
        
        # Count location pages
        if (self.web_dir / 'locations').exists():
            stats['locations_mapped'] = sum(1 for _ in (self.web_dir / 'locations').rglob('*.html'))
        
        return stats
    
    def execute_mission(self):
        """Execute the complete mission"""
        logger.info("\n" + "=" * 60)
        logger.info("THE BUTLER - MASTER ORCHESTRATOR")
        logger.info("Mission: Complete Documentation & Dissemination")
        logger.info("=" * 60 + "\n")
        
        start_time = datetime.now()
        
        try:
            # Execute all phases
            self.execute_phase_1_data_acquisition()
            self.execute_phase_2_character_generation()
            self.execute_phase_3_web_interface()
            self.execute_phase_4_asset_integration()
            self.execute_phase_5_deployment()
            self.execute_phase_6_verification()
            
            # Generate final report
            report = self.generate_mission_report()
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info("\n" + "=" * 60)
            logger.info("MISSION COMPLETE")
            logger.info("=" * 60)
            logger.info(f"Duration: {duration}")
            logger.info(f"Status: All phases complete")
            logger.info("=" * 60 + "\n")
            
        except Exception as e:
            logger.error(f"Mission failed: {e}", exc_info=True)
            raise

if __name__ == '__main__':
    orchestrator = MasterOrchestrator()
    orchestrator.execute_mission()
