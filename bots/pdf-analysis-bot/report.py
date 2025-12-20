#!/usr/bin/env python3
"""
PDF Analysis Report Generator

Generates markdown reports from analysis results.
"""

import json
import argparse
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_report(results_file: str, output_file: str):
    """Generate markdown report from results."""
    
    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load results: {e}")
        return
    
    # Calculate statistics
    total = len(results)
    accepted = sum(1 for r in results if r['analysis']['decision'] == 'ACCEPT')
    review = sum(1 for r in results if r['analysis']['decision'] == 'REVIEW')
    rejected = sum(1 for r in results if r['analysis']['decision'] == 'REJECT')
    errors = sum(1 for r in results if r['analysis']['decision'] == 'ERROR')
    
    # Generate report
    report = f"""# PDF Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Summary

- **Total Files Analyzed:** {total}
- **✅ Accepted (Indexed):** {accepted}
- **⚠️ Review Needed:** {review}
- **❌ Rejected (Trash):** {rejected}
- **🔴 Errors:** {errors}

## Results by File

"""
    
    # Sort by score (descending)
    sorted_results = sorted(results, 
                          key=lambda x: x['analysis'].get('relevance_score', 0),
                          reverse=True)
    
    for result in sorted_results:
        filename = result['file']
        score = result['analysis'].get('relevance_score', 0)
        decision = result['analysis']['decision']
        
        decision_emoji = {
            'ACCEPT': '✅',
            'REVIEW': '⚠️',
            'REJECT': '❌',
            'ERROR': '🔴'
        }.get(decision, '❓')
        
        report += f"\n### {decision_emoji} {filename}\n\n"
        report += f"- **Score:** {score}/100\n"
        report += f"- **Decision:** {decision}\n"
        
        if 'matches' in result and result['matches'].get('keywords'):
            keywords = result['matches']['keywords'][:5]
            report += f"- **Matched Keywords:** {', '.join(keywords)}\n"
        
        if 'metadata' in result:
            meta = result['metadata']
            if 'page_count' in meta:
                report += f"- **Pages:** {meta['page_count']}\n"
        
        report += "\n"
    
    # Save report
    with open(output_file, 'w') as f:
        f.write(report)
    
    logger.info(f"Report saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Generate PDF analysis report')
    parser.add_argument('--input', default='logs/pdf-analysis/results.json',
                       help='Input results file')
    parser.add_argument('--output', default='logs/pdf-analysis/report.md',
                       help='Output report file')
    
    args = parser.parse_args()
    generate_report(args.input, args.output)


if __name__ == '__main__':
    main()
