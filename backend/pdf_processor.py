try:
    import fitz  # PyMuPDF
except ImportError:
    try:
        import pymupdf as fitz  # type: ignore
    except ImportError:
        fitz = None  # type: ignore

import pdfplumber
from typing import Dict, Any
from pathlib import Path
import os


class PDFProcessor:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def extract_text_pymupdf(self) -> Dict[str, Any]:
        if fitz is None:
            raise Exception("PyMuPDF (fitz) is not installed. Install with: pip install PyMuPDF")
        try:
            doc = fitz.open(self.file_path)  # type: ignore
            if doc.needs_pass:
                raise Exception("PDF is password protected")

            content = {}
            for i in range(len(doc)):
                content[i + 1] = doc.load_page(i).get_text()

            if not any(content.values()):
                raise Exception("Empty PDF")

            return {
                "file_name": self.file_path,
                "total_pages": len(doc),
                "content": content
            }

        except Exception as e:
            raise Exception(f"PyMuPDF Error: {e}")

    def extract_text_pdfplumber(self) -> Dict[str, Any]:
        try:
            content: Dict[int, str] = {}
            with pdfplumber.open(self.file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    content[i + 1] = page.extract_text()

            return {
                "file_name": self.file_path,
                "total_pages": len(content),
                "content": content
            }

        except Exception as e:
            raise Exception(f"pdfplumber Error: {e}")

    def get_pdf_metadata(self) -> Dict[str, Any]:
        """Extract metadata from PDF file"""
        if fitz is None:
            return {"file_name": Path(self.file_path).name, "error": "PyMuPDF not installed"}
        doc = fitz.open(self.file_path)  # type: ignore
        meta = doc.metadata if doc.metadata else {}
        file_size = os.path.getsize(self.file_path)
        return {
            "file_name": Path(self.file_path).name,
            "total_pages": doc.page_count,
            "title": meta.get("title"),
            "author": meta.get("author"),
            "creator": meta.get("creator"),
            "producer": meta.get("producer"),
            "subject": meta.get("subject"),
            "keywords": meta.get("keywords"),
            "file_size": file_size
        }
    
    def extract_all(self) -> Dict[str, Any]:
        """Comprehensive extraction with metadata and fallback mechanism"""
        try:
            result = self.extract_text_pymupdf()
            result["extraction_method"] = "PyMuPDF"
        except Exception:
            result = self.extract_text_pdfplumber()
            result["extraction_method"] = "pdfplumber (fallback)"
        
        try:
            result["metadata"] = self.get_pdf_metadata()
        except Exception:
            result["metadata"] = {}
        
        result["status"] = "success"
        return result
