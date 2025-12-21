#!/usr/bin/env python3
"""
PDF Analysis Bot - Main Analysis Script

Analyzes PDF files for Epstein-related content and generates relevance scores.
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any
import yaml
import re
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFAnalyzer:
    """Analyzes PDF files for relevance to Epstein case."""
    
    def __init__(self, config_path: str = "bots/config/pdf-analysis.yml"):
        """Initialize analyzer with configuration."""
        self.config = self._load_config(config_path)
        self.keywords = self._load_keywords("bots/config/keywords.yml")
        
    def _load_config(self, path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return self._default_config()
    
    def _load_keywords(self, path: str) -> Dict:
        """Load keywords from YAML file."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load keywords: {e}")
            return {}
    
    def _default_config(self) -> Dict:
        """Return default configuration."""
        return {
            'thresholds': {'accept': 70, 'review': 40, 'reject': 40},
            'scoring': {
                'weights': {
                    'keyword_match': 0.30,
                    'entity_match': 0.30,
                    'context_analysis': 0.40
                }
            }
        }
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Analysis results dictionary
        """
        logger.info(f"Analyzing file: {file_path}")
        
        try:
            # Extract text from PDF
            text = self._extract_text(file_path)
            
            # Analyze content
            keyword_score = self._analyze_keywords(text)
            entity_score = self._analyze_entities(text)
            context_score = self._analyze_context(text)
            
            # Calculate final score
            weights = self.config['scoring']['weights']
            final_score = (
                keyword_score * weights['keyword_match'] +
                entity_score * weights['entity_match'] +
                context_score * weights['context_analysis']
            )
            
            # Determine routing decision
            decision = self._make_decision(final_score)
            
            # Extract metadata
            metadata = self._extract_metadata(file_path)
            
            # Build result
            result = {
                'file': os.path.basename(file_path),
                'path': file_path,
                'timestamp': datetime.now().isoformat(),
                'analysis': {
                    'relevance_score': round(final_score, 2),
                    'keyword_score': round(keyword_score, 2),
                    'entity_score': round(entity_score, 2),
                    'context_score': round(context_score, 2),
                    'decision': decision,
                    'routing': self._get_routing(decision)
                },
                'metadata': metadata,
                'matches': {
                    'keywords': self._get_matched_keywords(text),
                    'entities': self._extract_entities(text)
                }
            }
            
            logger.info(f"Analysis complete: {result['analysis']['decision']} "
                       f"(score: {final_score:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return self._error_result(file_path, str(e))
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            import pypdf as PyPDF2
            
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                
                if not text.strip():
                    logger.warning(f"No text extracted from {file_path}, may need OCR")
                    return ""
                
                return text
                
        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            return ""
    
    def _analyze_keywords(self, text: str) -> float:
        """Analyze keyword matches in text."""
        text_lower = text.lower()
        score = 0
        max_score = 100
        
        # High priority keywords
        for keyword in self.keywords.get('high_priority', []):
            if keyword.lower() in text_lower:
                score += 10
        
        # Medium priority keywords
        for keyword in self.keywords.get('medium_priority', []):
            if keyword.lower() in text_lower:
                score += 5
        
        # Low priority keywords
        for keyword in self.keywords.get('low_priority', []):
            if keyword.lower() in text_lower:
                score += 2
        
        return min(score, max_score)
    
    def _analyze_entities(self, text: str) -> float:
        """Analyze named entities in text."""
        score = 0
        max_score = 100
        
        # Simple entity detection (would use NER in production)
        entities = self.keywords.get('entities', {})
        
        # Check for person indicators
        for indicator in entities.get('person_indicators', []):
            if indicator in text:
                score += 8
        
        # Check for location indicators
        for indicator in entities.get('location_indicators', []):
            if indicator in text:
                score += 6
        
        # Check for organization indicators
        for indicator in entities.get('organization_indicators', []):
            if indicator in text:
                score += 6
        
        return min(score, max_score)
    
    def _analyze_context(self, text: str) -> float:
        """Analyze contextual relevance of text."""
        score = 0
        max_score = 100
        text_lower = text.lower()
        
        # Check for legal document indicators
        legal_indicators = self.keywords.get('legal_document_indicators', [])
        legal_matches = sum(1 for ind in legal_indicators if ind.lower() in text_lower)
        if legal_matches > 3:
            score += 30
        
        # Check for context phrases
        context_phrases = self.keywords.get('context_phrases', {})
        for phrase_list in context_phrases.get('high_context', []):
            if all(phrase.lower() in text_lower for phrase in phrase_list):
                score += 20
        
        for phrase_list in context_phrases.get('medium_context', []):
            if all(phrase.lower() in text_lower for phrase in phrase_list):
                score += 10
        
        # Check for negative indicators (reduce score)
        negative_indicators = self.keywords.get('negative_indicators', [])
        for indicator in negative_indicators:
            if indicator.lower() in text_lower:
                score -= 20
        
        return max(0, min(score, max_score))
    
    def _make_decision(self, score: float) -> str:
        """Make routing decision based on score."""
        thresholds = self.config['thresholds']
        
        if score >= thresholds['accept']:
            return 'ACCEPT'
        elif score >= thresholds['review']:
            return 'REVIEW'
        else:
            return 'REJECT'
    
    def _get_routing(self, decision: str) -> str:
        """Get routing destination for decision."""
        routing_map = {
            'ACCEPT': 'data/indexed',
            'REVIEW': 'data/review',
            'REJECT': 'data/trash'
        }
        return routing_map.get(decision, 'data/trash')
    
    def _extract_metadata(self, file_path: str) -> Dict:
        """Extract metadata from PDF file."""
        try:
            import pypdf as PyPDF2
            
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                info = reader.metadata or {}
                
                return {
                    'title': info.get('/Title', 'Unknown'),
                    'author': info.get('/Author', 'Unknown'),
                    'created': info.get('/CreationDate', 'Unknown'),
                    'modified': info.get('/ModDate', 'Unknown'),
                    'page_count': len(reader.pages),
                    'file_size': os.path.getsize(file_path)
                }
        except Exception as e:
            logger.error(f"Metadata extraction failed: {e}")
            return {'error': str(e)}
    
    def _get_matched_keywords(self, text: str) -> List[str]:
        """Get list of matched keywords."""
        text_lower = text.lower()
        matches = []
        
        for priority in ['high_priority', 'medium_priority', 'low_priority']:
            for keyword in self.keywords.get(priority, []):
                if keyword.lower() in text_lower and keyword not in matches:
                    matches.append(keyword)
        
        return matches[:10]  # Return top 10 matches
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text (simplified)."""
        # This is a simplified version. Production would use NER models
        return {
            'people': [],
            'places': [],
            'dates': [],
            'organizations': []
        }
    
    def _error_result(self, file_path: str, error: str) -> Dict:
        """Generate error result."""
        return {
            'file': os.path.basename(file_path),
            'path': file_path,
            'timestamp': datetime.now().isoformat(),
            'error': error,
            'analysis': {
                'relevance_score': 0,
                'decision': 'ERROR',
                'routing': 'data/errors'
            }
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Analyze PDFs for Epstein-related content')
    parser.add_argument('--file', help='Single PDF file to analyze')
    parser.add_argument('--dir', help='Directory of PDFs to analyze')
    parser.add_argument('--output', default='logs/pdf-analysis/results.json',
                       help='Output file for results')
    parser.add_argument('--threshold', type=int, help='Custom acceptance threshold')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize analyzer
    analyzer = PDFAnalyzer()
    
    if args.threshold:
        analyzer.config['thresholds']['accept'] = args.threshold
    
    # Collect files to analyze
    files_to_analyze = []
    
    if args.file:
        if os.path.exists(args.file):
            files_to_analyze.append(args.file)
        else:
            logger.error(f"File not found: {args.file}")
            sys.exit(1)
    
    if args.dir:
        if os.path.exists(args.dir):
            for root, dirs, files in os.walk(args.dir):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        files_to_analyze.append(os.path.join(root, file))
        else:
            logger.error(f"Directory not found: {args.dir}")
            sys.exit(1)
    
    if not files_to_analyze:
        logger.info("No PDF files to analyze")
        sys.exit(0)
    
    # Analyze files
    results = []
    for file_path in files_to_analyze:
        result = analyzer.analyze_file(file_path)
        results.append(result)
    
    # Save results
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Analysis complete. Results saved to {args.output}")
    
    # Print summary
    accepted = sum(1 for r in results if r['analysis']['decision'] == 'ACCEPT')
    review = sum(1 for r in results if r['analysis']['decision'] == 'REVIEW')
    rejected = sum(1 for r in results if r['analysis']['decision'] == 'REJECT')
    errors = sum(1 for r in results if r['analysis']['decision'] == 'ERROR')
    
    print(f"\n=== Analysis Summary ===")
    print(f"Total files: {len(results)}")
    print(f"Accepted: {accepted}")
    print(f"Review needed: {review}")
    print(f"Rejected: {rejected}")
    print(f"Errors: {errors}")


if __name__ == '__main__':
    main()
