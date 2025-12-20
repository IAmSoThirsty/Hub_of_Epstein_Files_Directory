#!/usr/bin/env python3
"""
PDF Processing Tool
Extracts text from PDFs, performs OCR on scanned documents, and indexes content
Works with FBI Vault PDFs and other public documents
"""

import os
import json
from pathlib import Path
from datetime import datetime
import re

try:
    import PyPDF2
    HAS_PYPDF = True
except ImportError:
    print("⚠️ PyPDF2 not installed. Install with: pip install PyPDF2")
    HAS_PYPDF = False

try:
    import pytesseract
    from PIL import Image
    import pdf2image
    HAS_OCR = True
except ImportError:
    print("⚠️ OCR libraries not installed. Install with:")
    print("   pip install pytesseract pillow pdf2image")
    print("   Also install tesseract: apt-get install tesseract-ocr (Linux)")
    HAS_OCR = False


class PDFProcessor:
    def __init__(self, input_dir='data/public_files', output_dir='data/processed'):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / 'text').mkdir(exist_ok=True)
        (self.output_dir / 'metadata').mkdir(exist_ok=True)
        (self.output_dir / 'indexed').mkdir(exist_ok=True)
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using PyPDF2"""
        if not HAS_PYPDF:
            return None
        
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)
                
                for page_num in range(page_count):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n\n"
            
            return text, page_count
        except Exception as e:
            print(f"  ⚠️ Error extracting text: {str(e)}")
            return None, 0
    
    def ocr_pdf(self, pdf_path):
        """Perform OCR on scanned PDF"""
        if not HAS_OCR:
            return None
        
        try:
            # Convert PDF to images
            images = pdf2image.convert_from_path(pdf_path)
            
            text = ""
            for i, image in enumerate(images):
                print(f"    OCR page {i+1}/{len(images)}...")
                page_text = pytesseract.image_to_string(image)
                text += page_text + "\n\n"
            
            return text, len(images)
        except Exception as e:
            print(f"  ⚠️ Error performing OCR: {str(e)}")
            return None, 0
    
    def extract_metadata(self, text, pdf_path):
        """Extract metadata from document text"""
        metadata = {
            'file_name': pdf_path.name,
            'processed_date': datetime.now().isoformat(),
            'word_count': len(text.split()),
            'char_count': len(text)
        }
        
        # Try to extract dates (YYYY-MM-DD or MM/DD/YYYY format)
        date_pattern = r'\b(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})\b'
        dates = re.findall(date_pattern, text)
        if dates:
            metadata['dates_found'] = list(set(dates))[:10]  # First 10 unique dates
        
        # Try to extract case numbers (common formats)
        case_pattern = r'\b(CV|CR|INV)-?\d{4}-?\d{3,6}\b'
        cases = re.findall(case_pattern, text, re.IGNORECASE)
        if cases:
            metadata['case_numbers'] = list(set(cases))
        
        # Try to extract locations (common cities/islands)
        locations = [
            'Little St. James', 'St. Thomas', 'Manhattan', 'New York',
            'Palm Beach', 'Florida', 'Paris', 'London', 'New Mexico'
        ]
        found_locations = [loc for loc in locations if loc.lower() in text.lower()]
        if found_locations:
            metadata['locations'] = found_locations
        
        return metadata
    
    def process_pdf(self, pdf_path):
        """Process a single PDF file"""
        print(f"\n📄 Processing: {pdf_path.name}")
        
        # Try text extraction first
        result = self.extract_text_from_pdf(pdf_path)
        if result:
            text, page_count = result
            method = "text_extraction"
        else:
            # Fall back to OCR if text extraction failed
            print("  ℹ️ Text extraction failed, trying OCR...")
            result = self.ocr_pdf(pdf_path)
            if result:
                text, page_count = result
                method = "ocr"
            else:
                print("  ❌ Could not process PDF")
                return None
        
        print(f"  ✅ Extracted text: {len(text)} characters, {page_count} pages")
        print(f"  Method: {method}")
        
        # Save extracted text
        text_file = self.output_dir / 'text' / f"{pdf_path.stem}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Extract and save metadata
        metadata = self.extract_metadata(text, pdf_path)
        metadata['page_count'] = page_count
        metadata['extraction_method'] = method
        
        meta_file = self.output_dir / 'metadata' / f"{pdf_path.stem}.json"
        with open(meta_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Create indexed version for search
        indexed = {
            'id': pdf_path.stem,
            'title': pdf_path.stem.replace('-', ' ').title(),
            'content': text[:1000],  # First 1000 chars for search preview
            'full_text_path': str(text_file),
            'metadata': metadata
        }
        
        index_file = self.output_dir / 'indexed' / f"{pdf_path.stem}.json"
        with open(index_file, 'w') as f:
            json.dump(indexed, f, indent=2)
        
        return indexed
    
    def process_all_pdfs(self):
        """Process all PDFs in input directory"""
        pdf_files = list(self.input_dir.rglob('*.pdf'))
        
        if not pdf_files:
            print("⚠️ No PDF files found in input directory")
            return []
        
        print(f"\n📚 Found {len(pdf_files)} PDF files to process")
        
        results = []
        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"\n[{i}/{len(pdf_files)}]")
            result = self.process_pdf(pdf_path)
            if result:
                results.append(result)
        
        # Save processing summary
        summary = {
            'processed_date': datetime.now().isoformat(),
            'total_files': len(pdf_files),
            'successful': len(results),
            'failed': len(pdf_files) - len(results),
            'files': results
        }
        
        summary_file = self.output_dir / 'processing_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return results


def main():
    print("=" * 60)
    print("  PDF Processing Tool")
    print("  Epstein Files Hub")
    print("=" * 60)
    print()
    
    if not HAS_PYPDF:
        print("⚠️ Missing required libraries!")
        print("Install with: pip install PyPDF2 pytesseract pillow pdf2image")
        return
    
    processor = PDFProcessor()
    
    print("Processing PDFs...")
    print(f"Input: {processor.input_dir}")
    print(f"Output: {processor.output_dir}")
    print()
    
    results = processor.process_all_pdfs()
    
    print("\n" + "=" * 60)
    print("✅ Processing complete!")
    print("=" * 60)
    print(f"\nProcessed: {len(results)} files")
    print(f"Output directory: {processor.output_dir}")
    print("\nNext steps:")
    print("1. Review extracted text in data/processed/text/")
    print("2. Check metadata in data/processed/metadata/")
    print("3. Update search index: python scripts/generate-search-index.py")


if __name__ == '__main__':
    main()
