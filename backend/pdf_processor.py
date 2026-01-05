"""
PDF Processor Module for SmartDocs AI
Handles PDF text extraction and metadata extraction using PyMuPDF and pdfplumber
"""

import fitz  # PyMuPDF
import pdfplumber
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFProcessor:
    """
    A class to process PDF files and extract text and metadata.
    Supports both PyMuPDF and pdfplumber for text extraction.
    """

    def __init__(self, file_path: str):
        """
        Initialize PDFProcessor with a PDF file path.
        
        Args:
            file_path (str): Path to the PDF file
            
        Raises:
            FileNotFoundError: If the PDF file does not exist
            ValueError: If the file is not a PDF
        """
        self.file_path = Path(file_path)
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {self.file_path}")
        
        if self.file_path.suffix.lower() != ".pdf":
            raise ValueError(f"File must be a PDF: {self.file_path}")
        
        self.file_name = self.file_path.name
        self.logger = logger

    def extract_text_pymupdf(self) -> Dict[str, Any]:
        """
        Extract text from PDF using PyMuPDF (fitz).
        Provides fast and reliable extraction with good handling of complex layouts.
        
        Returns:
            Dict: Contains filename, total_pages, text_by_page, and extraction method
            
        Raises:
            Exception: If PDF is corrupted or cannot be read
        """
        try:
            self.logger.info(f"Starting PyMuPDF extraction for {self.file_name}")
            
            doc = fitz.open(self.file_path)
            text_by_page = {}
            
            # Check if document is encrypted (password-protected)
            if doc.is_pdf and doc.is_encrypted:
                self.logger.warning(f"PDF is password-protected: {self.file_name}")
                raise ValueError("PDF is password-protected. Please provide the password.")
            
            total_pages = len(doc)
            
            if total_pages == 0:
                self.logger.warning(f"PDF has no pages: {self.file_name}")
                raise ValueError("PDF document contains no pages")
            
            # Extract text page by page
            for page_num in range(total_pages):
                try:
                    page = doc[page_num]
                    text = page.get_text()
                    
                    # Store with 1-based page numbering for user-friendly output
                    text_by_page[page_num + 1] = text
                    self.logger.debug(f"Extracted page {page_num + 1} from {self.file_name}")
                
                except Exception as e:
                    self.logger.error(f"Error extracting page {page_num + 1}: {str(e)}")
                    text_by_page[page_num + 1] = f"[Error extracting page: {str(e)}]"
            
            doc.close()
            
            self.logger.info(f"PyMuPDF extraction completed for {self.file_name}")
            
            return {
                "file_name": self.file_name,
                "file_path": str(self.file_path),
                "total_pages": total_pages,
                "text_by_page": text_by_page,
                "extraction_method": "PyMuPDF",
                "status": "success"
            }
        
        except Exception as e:
            self.logger.error(f"PyMuPDF extraction failed: {str(e)}")
            raise

    def extract_text_pdfplumber(self) -> Dict[str, Any]:
        """
        Extract text from PDF using pdfplumber.
        Provides structured extraction with better handling of tables and formatted text.
        
        Returns:
            Dict: Contains filename, total_pages, text_by_page, and extraction method
            
        Raises:
            Exception: If PDF is corrupted or cannot be read
        """
        try:
            self.logger.info(f"Starting pdfplumber extraction for {self.file_name}")
            
            with pdfplumber.open(self.file_path) as pdf:
                text_by_page = {}
                total_pages = len(pdf.pages)
                
                if total_pages == 0:
                    self.logger.warning(f"PDF has no pages: {self.file_name}")
                    raise ValueError("PDF document contains no pages")
                
                # Extract text page by page
                for page_num, page in enumerate(pdf.pages):
                    try:
                        text = page.extract_text()
                        # Store with 1-based page numbering
                        text_by_page[page_num + 1] = text if text else "[No text found on this page]"
                        self.logger.debug(f"Extracted page {page_num + 1} from {self.file_name}")
                    
                    except Exception as e:
                        self.logger.error(f"Error extracting page {page_num + 1}: {str(e)}")
                        text_by_page[page_num + 1] = f"[Error extracting page: {str(e)}]"
            
            self.logger.info(f"pdfplumber extraction completed for {self.file_name}")
            
            return {
                "file_name": self.file_name,
                "file_path": str(self.file_path),
                "total_pages": total_pages,
                "text_by_page": text_by_page,
                "extraction_method": "pdfplumber",
                "status": "success"
            }
        
        except Exception as e:
            self.logger.error(f"pdfplumber extraction failed: {str(e)}")
            raise

    def get_pdf_metadata(self) -> Dict[str, Any]:
        """
        Extract metadata from PDF including page count, title, author, and other properties.
        
        Returns:
            Dict: Contains metadata like title, author, creator, producer, creation_date, etc.
            
        Raises:
            Exception: If PDF cannot be read
        """
        try:
            self.logger.info(f"Extracting metadata for {self.file_name}")
            
            doc = fitz.open(self.file_path)
            
            # Get metadata
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            
            metadata_info = {
                "file_name": self.file_name,
                "file_path": str(self.file_path),
                "file_size": self.file_path.stat().st_size,  # in bytes
                "total_pages": len(doc),
                "title": metadata.get("title", "N/A") if metadata else "N/A",
                "author": metadata.get("author", "N/A") if metadata else "N/A",
                "creator": metadata.get("creator", "N/A") if metadata else "N/A",
                "producer": metadata.get("producer", "N/A") if metadata else "N/A",
                "creation_date": metadata.get("creationDate", "N/A") if metadata else "N/A",
                "modification_date": metadata.get("modDate", "N/A") if metadata else "N/A",
                "subject": metadata.get("subject", "N/A") if metadata else "N/A",
                "keywords": metadata.get("keywords", "N/A") if metadata else "N/A",
            }
            
            doc.close()
            
            self.logger.info(f"Metadata extraction completed for {self.file_name}")
            
            return metadata_info
        
        except Exception as e:
            self.logger.error(f"Metadata extraction failed: {str(e)}")
            raise

    def extract_with_fallback(self) -> Dict[str, Any]:
        """
        Attempt extraction with PyMuPDF first, fall back to pdfplumber if it fails.
        
        Returns:
            Dict: Extraction result with text and metadata
        """
        try:
            self.logger.info(f"Starting extraction with fallback for {self.file_name}")
            result = self.extract_text_pymupdf()
            self.logger.info("Using PyMuPDF extraction")
            return result
        
        except Exception as e:
            self.logger.warning(f"PyMuPDF failed, trying pdfplumber: {str(e)}")
            try:
                result = self.extract_text_pdfplumber()
                self.logger.info("Using pdfplumber extraction as fallback")
                return result
            except Exception as e2:
                self.logger.error(f"Both extraction methods failed: {str(e2)}")
                raise RuntimeError(
                    f"Could not extract text using either PyMuPDF or pdfplumber. "
                    f"PyMuPDF error: {str(e)} | pdfplumber error: {str(e2)}"
                )

    def extract_all(self) -> Dict[str, Any]:
        """
        Extract text and metadata from PDF in one call.
        Uses fallback extraction method and includes metadata.
        
        Returns:
            Dict: Comprehensive extraction result with text, metadata, and status
        """
        try:
            self.logger.info(f"Starting comprehensive extraction for {self.file_name}")
            
            # Extract text with fallback
            extraction_result = self.extract_with_fallback()
            
            # Extract metadata
            metadata = self.get_pdf_metadata()
            
            # Combine results
            combined_result = {
                **extraction_result,
                "metadata": metadata
            }
            
            self.logger.info(f"Comprehensive extraction completed for {self.file_name}")
            return combined_result
        
        except Exception as e:
            self.logger.error(f"Comprehensive extraction failed: {str(e)}")
            return {
                "file_name": self.file_name,
                "file_path": str(self.file_path),
                "status": "error",
                "error_message": str(e)
            }


def process_pdf_file(file_path: str, extract_method: str = "fallback") -> Dict[str, Any]:
    """
    Utility function to process a PDF file with specified extraction method.
    
    Args:
        file_path (str): Path to the PDF file
        extract_method (str): "pymupdf", "pdfplumber", "fallback", or "all"
        
    Returns:
        Dict: Extraction result
        
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        ValueError: If file is not a PDF or extract_method is invalid
    """
    if extract_method not in ["pymupdf", "pdfplumber", "fallback", "all"]:
        raise ValueError(f"Invalid extract_method: {extract_method}")
    
    processor = PDFProcessor(file_path)
    
    if extract_method == "pymupdf":
        return processor.extract_text_pymupdf()
    elif extract_method == "pdfplumber":
        return processor.extract_text_pdfplumber()
    elif extract_method == "fallback":
        return processor.extract_with_fallback()
    else:  # "all"
        return processor.extract_all()
