#!/usr/bin/env python3
"""Generate integration report for Uncensored.ai workflow"""

import json
import sys
from pathlib import Path

def main():
    """Generate report from fetch results"""
    results_file = Path("data/uncensored_files/fetch_results.json")
    report_file = Path("data/uncensored_files/integration_report.md")
    
    if not results_file.exists():
        print("No fetch results found")
        return 1
    
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        # Append to report
        with open(report_file, 'a') as report:
            report.write('### Fetch Results\n')
            report.write(f"- Total files fetched: {data.get('total_files', 0)}\n")
            report.write(f"- Total files skipped: {data.get('total_skipped', 0)}\n")
            
            if 'categories' in data:
                report.write('\n### By Category\n')
                for cat, results in data['categories'].items():
                    fetched = results.get('files_fetched', 0)
                    skipped = results.get('files_skipped', 0)
                    report.write(f"- **{cat.capitalize()}**: {fetched} fetched, {skipped} skipped\n")
        
        print("Report generated successfully")
        return 0
    
    except Exception as e:
        print(f"Error generating report: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
