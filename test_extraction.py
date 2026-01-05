"""
Test Script for PDF Extraction Module
Tests the PDFProcessor class with different PDF types and extraction methods
"""

import sys
from pathlib import Path
import json
import logging
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from pdf_processor import PDFProcessor, process_pdf_file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_separator(title: str = ""):
    """Print a formatted separator line"""
    sep = "=" * 80
    if title:
        print(f"\n{sep}")
        print(f"  {title}")
        print(f"{sep}\n")
    else:
        print(f"{sep}\n")


def test_pdf_extraction(pdf_path: str, test_name: str):
    """
    Test PDF extraction with detailed output
    
    Args:
        pdf_path (str): Path to the PDF file
        test_name (str): Name of the test
    """
    print_separator(f"Test: {test_name}")
    
    try:
        # Initialize processor
        processor = PDFProcessor(pdf_path)
        print(f"✓ PDF file loaded: {pdf_path}")
        print(f"  File size: {Path(pdf_path).stat().st_size / 1024:.2f} KB")
        
        # Test metadata extraction
        print("\n[1] METADATA EXTRACTION")
        print("-" * 80)
        metadata = processor.get_pdf_metadata()
        
        print(f"File Name: {metadata.get('file_name')}")
        print(f"Total Pages: {metadata.get('total_pages')}")
        print(f"Title: {metadata.get('title')}")
        print(f"Author: {metadata.get('author')}")
        print(f"Creator: {metadata.get('creator')}")
        print(f"Producer: {metadata.get('producer')}")
        print(f"File Size: {metadata.get('file_size')} bytes")
        
        # Test PyMuPDF extraction
        print("\n[2] PYMUPDF EXTRACTION")
        print("-" * 80)
        try:
            pymupdf_result = processor.extract_text_pymupdf()
            print(f"✓ Status: {pymupdf_result.get('status')}")
            print(f"✓ Total Pages: {pymupdf_result.get('total_pages')}")
            print(f"✓ Extraction Method: {pymupdf_result.get('extraction_method')}")
            
            # Print first 200 characters from each page
            text_by_page = pymupdf_result.get('text_by_page', {})
            for page_num in sorted(text_by_page.keys())[:3]:  # Show first 3 pages
                text = text_by_page[page_num]
                preview = text[:200].replace('\n', ' ') + "..." if len(text) > 200 else text
                print(f"\n  Page {page_num} Preview: {preview}")
        
        except Exception as e:
            print(f"✗ PyMuPDF extraction failed: {str(e)}")
        
        # Test pdfplumber extraction
        print("\n[3] PDFPLUMBER EXTRACTION")
        print("-" * 80)
        try:
            pdfplumber_result = processor.extract_text_pdfplumber()
            print(f"✓ Status: {pdfplumber_result.get('status')}")
            print(f"✓ Total Pages: {pdfplumber_result.get('total_pages')}")
            print(f"✓ Extraction Method: {pdfplumber_result.get('extraction_method')}")
            
            # Print first 200 characters from each page
            text_by_page = pdfplumber_result.get('text_by_page', {})
            for page_num in sorted(text_by_page.keys())[:3]:  # Show first 3 pages
                text = text_by_page[page_num]
                preview = text[:200].replace('\n', ' ') + "..." if len(text) > 200 else text
                print(f"\n  Page {page_num} Preview: {preview}")
        
        except Exception as e:
            print(f"✗ pdfplumber extraction failed: {str(e)}")
        
        # Test comprehensive extraction
        print("\n[4] COMPREHENSIVE EXTRACTION (WITH FALLBACK)")
        print("-" * 80)
        try:
            full_result = processor.extract_all()
            print(f"✓ Status: {full_result.get('status')}")
            print(f"✓ Extraction Method Used: {full_result.get('extraction_method')}")
            print(f"✓ Total Pages Extracted: {full_result.get('total_pages')}")
            
            if 'metadata' in full_result:
                print(f"✓ Metadata included: Yes")
            
            # Show extraction summary
            text_by_page = full_result.get('text_by_page', {})
            if text_by_page:
                total_chars = sum(len(text) for text in text_by_page.values())
                print(f"✓ Total characters extracted: {total_chars}")
                avg_chars_per_page = total_chars / len(text_by_page)
                print(f"✓ Average characters per page: {avg_chars_per_page:.0f}")
        
        except Exception as e:
            print(f"✗ Comprehensive extraction failed: {str(e)}")
        
        print("\n✓ Test completed successfully!")
        return True
    
    except FileNotFoundError as e:
        print(f"✗ File not found: {e}")
        return False
    except ValueError as e:
        print(f"✗ Invalid file: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        logger.exception("Detailed error:")
        return False


def test_process_pdf_utility():
    """Test the utility function for PDF processing"""
    print_separator("Test: Utility Function - process_pdf_file()")
    
    # Get sample PDF paths
    data_dir = Path(__file__).parent / "data"
    pdf_files = list(data_dir.glob("sample_*.pdf"))
    
    if not pdf_files:
        print("✗ No sample PDFs found. Generate them first using generate_sample_pdfs.py")
        return False
    
    try:
        pdf_path = str(pdf_files[0])
        
        # Test different extraction methods
        methods = ["pymupdf", "pdfplumber", "fallback", "all"]
        
        for method in methods:
            print(f"\nTesting with method: {method}")
            result = process_pdf_file(pdf_path, method)
            print(f"✓ Status: {result.get('status')}")
            print(f"✓ Method used: {result.get('extraction_method', 'N/A')}")
        
        return True
    
    except Exception as e:
        print(f"✗ Error testing utility function: {str(e)}")
        logger.exception("Detailed error:")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  SmartDocs AI - PDF Extraction Module Test Suite".center(78) + "║")
    print("║" + f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Check if sample PDFs exist
    data_dir = Path(__file__).parent / "data"
    pdf_files = sorted(data_dir.glob("sample_*.pdf"))
    
    if not pdf_files:
        print("\n⚠ Sample PDFs not found. Generating them now...")
        try:
            from generate_sample_pdfs import generate_sample_pdfs
            if generate_sample_pdfs():
                pdf_files = sorted(data_dir.glob("sample_*.pdf"))
                print("✓ Sample PDFs generated successfully!\n")
            else:
                print("✗ Failed to generate sample PDFs")
                print("Please install reportlab: pip install reportlab")
                return False
        except ImportError:
            print("✗ reportlab library not found")
            print("Please install it: pip install reportlab")
            return False
    
    # Run tests for each PDF
    test_results = []
    
    for pdf_file in pdf_files:
        test_name = pdf_file.stem.replace("sample_", "").replace("_", " ").title()
        result = test_pdf_extraction(str(pdf_file), test_name)
        test_results.append((test_name, result))
    
    # Test utility function
    test_results.append(("Utility Function", test_process_pdf_utility()))
    
    # Print summary
    print_separator("TEST SUMMARY")
    print(f"Total Tests: {len(test_results)}")
    passed = sum(1 for _, result in test_results if result)
    failed = len(test_results) - passed
    
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()
    
    for test_name, result in test_results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {test_name}: {status}")
    
    print_separator()
    
    if failed == 0:
        print("🎉 All tests passed successfully!")
        return True
    else:
        print(f"⚠ {failed} test(s) failed. Please review the output above.")
        return False


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✗ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {str(e)}")
        logger.exception("Detailed error:")
        sys.exit(1)
