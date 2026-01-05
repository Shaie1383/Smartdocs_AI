# PDF Processor Module Documentation

## Overview
The PDF Processor module provides robust functionality for extracting text and metadata from PDF files. It supports multiple extraction methods with fallback capabilities and comprehensive error handling.

## Features

✅ **Dual Extraction Methods**
- PyMuPDF (fitz) - Fast, reliable text extraction
- pdfplumber - Structured extraction with table support
- Automatic fallback from PyMuPDF to pdfplumber if primary fails

✅ **Metadata Extraction**
- Page count
- Document title and author
- Creator and producer information
- Creation and modification dates
- Subject and keywords
- File size information

✅ **Error Handling**
- Password-protected PDF detection
- Corrupted file recovery
- Empty document validation
- Per-page error handling with graceful degradation
- Detailed error logging

✅ **Comprehensive Output**
- Text organized by page number
- Metadata in structured format
- Extraction method tracking
- Status indicators

## Installation

### 1. Install Dependencies
```bash
pip install PyMuPDF pdfplumber python-dotenv
```

### 2. Optional: For PDF Generation (testing)
```bash
pip install reportlab
```

## Usage

### Basic Text Extraction

```python
from backend.pdf_processor import PDFProcessor

# Create processor instance
processor = PDFProcessor("path/to/document.pdf")

# Extract text using PyMuPDF
result = processor.extract_text_pymupdf()
print(f"Extracted {result['total_pages']} pages")

# Get text from specific page
page_1_text = result['text_by_page'][1]
```

### Fallback Extraction
Automatically tries PyMuPDF first, falls back to pdfplumber if needed:

```python
# Robust extraction with automatic fallback
result = processor.extract_with_fallback()
print(f"Method used: {result['extraction_method']}")
```

### Extract Everything at Once

```python
# Get text, metadata, and all information
result = processor.extract_all()

# Access text
text = result['text_by_page']

# Access metadata
metadata = result['metadata']
print(f"Title: {metadata['title']}")
print(f"Author: {metadata['author']}")
print(f"Pages: {metadata['total_pages']}")
```

### Using the Utility Function

```python
from backend.pdf_processor import process_pdf_file

# Simple one-line extraction
result = process_pdf_file("document.pdf", extract_method="fallback")

# Available methods: "pymupdf", "pdfplumber", "fallback", "all"
```

## Return Value Structure

### Text Extraction Result
```python
{
    "file_name": "document.pdf",
    "file_path": "/path/to/document.pdf",
    "total_pages": 5,
    "text_by_page": {
        1: "Page 1 text content...",
        2: "Page 2 text content...",
        # ... more pages
    },
    "extraction_method": "PyMuPDF",
    "status": "success"
}
```

### Metadata Result
```python
{
    "file_name": "document.pdf",
    "file_path": "/path/to/document.pdf",
    "file_size": 102400,  # bytes
    "total_pages": 5,
    "title": "Document Title",
    "author": "John Doe",
    "creator": "Word Processor",
    "producer": "PDF Library",
    "creation_date": "2024-01-15 10:30:00",
    "modification_date": "2024-01-20 15:45:00",
    "subject": "Document Subject",
    "keywords": "keyword1, keyword2"
}
```

### Comprehensive Result
```python
{
    # ... includes both text and metadata
    "text_by_page": { ... },
    "metadata": { ... }
}
```

## Error Handling

### Common Scenarios

#### 1. File Not Found
```python
try:
    processor = PDFProcessor("nonexistent.pdf")
except FileNotFoundError as e:
    print(f"Error: {e}")
```

#### 2. Invalid File
```python
try:
    processor = PDFProcessor("document.txt")  # Not a PDF
except ValueError as e:
    print(f"Error: {e}")
```

#### 3. Password-Protected PDF
```python
try:
    result = processor.extract_text_pymupdf()
except ValueError as e:
    if "password-protected" in str(e):
        print("PDF requires a password to open")
```

#### 4. Corrupted PDF
The processor attempts extraction with both methods:
- If PyMuPDF fails, it automatically tries pdfplumber
- If both fail, comprehensive error information is provided

## Testing

### Run the Test Suite
```bash
python test_extraction.py
```

This runs comprehensive tests on:
1. **Simple Text PDF** - Basic text document
2. **Multi-Column PDF** - Complex layout
3. **Formatted PDF** - Tables, styles, multiple pages
4. **Utility Function** - Testing the convenience function

### Generate Sample PDFs
```bash
python generate_sample_pdfs.py
```

Creates sample PDFs in the `data/` folder for testing purposes.

## Performance Notes

### PyMuPDF Advantages
- ✅ Faster extraction speed
- ✅ Better handling of complex layouts
- ✅ Lower memory usage
- ✅ Good for large documents

### pdfplumber Advantages
- ✅ Better table recognition
- ✅ Structured data extraction
- ✅ Better handling of formatted text
- ✅ Good for complex PDFs where layout matters

## Example: Full Workflow

```python
from backend.pdf_processor import PDFProcessor
from pathlib import Path

def process_document(pdf_path):
    """Complete example of PDF processing"""
    
    # Initialize processor
    processor = PDFProcessor(pdf_path)
    
    # Extract everything
    result = processor.extract_all()
    
    if result['status'] == 'success':
        # Get metadata
        metadata = result['metadata']
        print(f"Processing: {metadata['title']}")
        print(f"Pages: {metadata['total_pages']}")
        
        # Process each page
        for page_num, text in result['text_by_page'].items():
            print(f"\n--- Page {page_num} ---")
            print(text[:500])  # Print first 500 chars
            
            # Store for further processing
            # save_to_database(page_num, text)
    else:
        print(f"Error: {result['error_message']}")

# Usage
process_document("document.pdf")
```

## Logging

The module includes comprehensive logging:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

processor = PDFProcessor("document.pdf")
result = processor.extract_all()  # Detailed logs printed
```

Log levels:
- `DEBUG` - Detailed extraction information
- `INFO` - Extraction status and completion
- `WARNING` - Non-critical issues (e.g., password-protected PDFs)
- `ERROR` - Extraction failures and exceptions

## Troubleshooting

### Issue: "PyMuPDF extraction failed"
**Solution:** Module automatically falls back to pdfplumber. If both fail, the PDF might be corrupted.

### Issue: Empty pages extracted
**Solution:** Some PDFs have images instead of text. Consider using OCR (Optical Character Recognition) for scanned documents.

### Issue: Slow extraction
**Solution:** Large files may take time. Use streaming processing for very large documents.

### Issue: Special characters not extracted correctly
**Solution:** This depends on PDF encoding. Try both extraction methods and compare results.

## Advanced Usage

### Custom Processing Pipeline

```python
from backend.pdf_processor import PDFProcessor

processor = PDFProcessor("document.pdf")

# Get metadata first
metadata = processor.get_pdf_metadata()

# Try preferred method
try:
    result = processor.extract_text_pymupdf()
except Exception as e:
    print(f"PyMuPDF failed: {e}")
    result = processor.extract_text_pdfplumber()

# Process results
for page_num, text in result['text_by_page'].items():
    # Your custom processing here
    processed = text.lower().strip()
    # Save to database, file, etc.
```

### Batch Processing

```python
from pathlib import Path
from backend.pdf_processor import process_pdf_file

# Process all PDFs in a folder
pdf_folder = Path("uploads/")
results = []

for pdf_file in pdf_folder.glob("*.pdf"):
    try:
        result = process_pdf_file(str(pdf_file), extract_method="fallback")
        results.append(result)
    except Exception as e:
        print(f"Failed to process {pdf_file}: {e}")

# Analyze results
for result in results:
    print(f"{result['file_name']}: {result['total_pages']} pages")
```

## API Reference

### PDFProcessor Class

#### `__init__(file_path: str)`
Initialize processor with PDF file path.

#### `extract_text_pymupdf() -> Dict[str, Any]`
Extract text using PyMuPDF.

#### `extract_text_pdfplumber() -> Dict[str, Any]`
Extract text using pdfplumber.

#### `get_pdf_metadata() -> Dict[str, Any]`
Extract PDF metadata.

#### `extract_with_fallback() -> Dict[str, Any]`
Extract text with automatic fallback.

#### `extract_all() -> Dict[str, Any]`
Extract everything (text + metadata).

### Utility Function

#### `process_pdf_file(file_path: str, extract_method: str) -> Dict[str, Any]`
Quick extraction function with specified method.

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PyMuPDF | >=1.23.0 | Primary text extraction |
| pdfplumber | >=0.10.0 | Fallback extraction |
| python-dotenv | >=1.0.0 | Environment configuration |

## Notes

- PDFs without text (scanned images) won't be extracted. Consider implementing OCR for such documents.
- Large PDF files may consume significant memory. For production, consider streaming or chunking.
- Password-protected PDFs are detected and reported clearly.
- The module preserves page numbers for accurate reference tracking.

## Future Enhancements

- [ ] OCR support for scanned PDFs
- [ ] Table extraction and structured data
- [ ] Image extraction
- [ ] PDF form field extraction
- [ ] Async extraction for better performance
- [ ] Streaming for large documents
- [ ] Multi-language support

---

**Last Updated:** January 5, 2026
**Version:** 1.0.0
