#!/usr/bin/env python3
"""
PDF Routing Script

Routes analyzed PDFs to appropriate directories based on analysis results.
"""

import os
import sys
import json
import shutil
import argparse
import logging
from pathlib import Path
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def route_documents(results_file: str):
    """Route documents based on analysis results."""
    
    # Load results
    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load results: {e}")
        return
    
    # Ensure destination directories exist
    os.makedirs('data/indexed', exist_ok=True)
    os.makedirs('data/review', exist_ok=True)
    os.makedirs('data/trash', exist_ok=True)
    os.makedirs('data/errors', exist_ok=True)
    
    # Route each file
    for result in results:
        file_path = result.get('path')
        decision = result['analysis']['decision']
        routing = result['analysis']['routing']
        
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            continue
        
        # Determine destination
        filename = os.path.basename(file_path)
        dest_path = os.path.join(routing, filename)
        
        # Move file
        try:
            shutil.move(file_path, dest_path)
            logger.info(f"Routed {filename} to {routing} ({decision})")
            
            # Save analysis report alongside file
            report_path = dest_path.replace('.pdf', '_analysis.json')
            with open(report_path, 'w') as f:
                json.dump(result, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to route {filename}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Route analyzed PDFs')
    parser.add_argument('--input', default='logs/pdf-analysis/results.json',
                       help='Input results file')
    
    args = parser.parse_args()
    route_documents(args.input)


if __name__ == '__main__':
    main()
