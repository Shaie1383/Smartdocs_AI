# SmartDocs AI: Intelligent File Understanding & Query Platform

## Project Overview

SmartDocs AI is an intelligent Streamlit-based web application that enables users to upload, process, and interact with multiple PDF documents using AI-powered natural language processing (NLP) and Large Language Models (LLMs). By leveraging advanced text extraction, preprocessing, and vector-based search techniques, users can ask questions and receive instant, context-aware responses from their documents.

### Key Features
- **PDF Text Extraction**: Support for multiple extraction methods (PyMuPDF, pdfplumber)
- **Intelligent Text Processing**: Automatic cleaning, normalization, and preprocessing
- **Vector Embeddings**: Convert text into embeddings for semantic search
- **AI-Powered Search**: Query documents using natural language
- **Multi-Model Support**: Integration with Google Gemini Pro and Langchain
- **Streamlit UI**: User-friendly interface for document interaction
- **Vector Database**: Support for ChromaDB, Qdrant, and Pinecone

---

## Project Structure

```
smartdocs_ai/
│
├── backend/                    # Core processing modules
│   ├── __init__.py
│   ├── pdf_processor.py       # PDF text extraction
│   ├── text_cleaner.py        # Text preprocessing and cleaning
│   └── vectorizer.py          # Text to embedding conversion (future)
│
├── frontend/                   # Streamlit web application
│   └── app.py                 # Main Streamlit interface
│
├── tests/                      # Test modules
│   ├── test_extraction.py     # PDF extraction tests
│   └── test_cleaning.py       # Text cleaning tests
│
├── config/                     # Configuration files
│   ├── __init__.py
│   └── settings.py            # Application settings
│
├── data/                       # Data storage
│   └── [sample PDFs will be stored here]
│
├── uploads/                    # User uploaded files
│   └── [temporary storage for user uploads]
│
├── utils/                      # Utility functions
│   └── [helper modules]
│
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── generate_sample_pdfs.py    # Script to generate test PDFs
└── .gitignore                 # Git ignore rules
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step 1: Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Generate Sample PDFs (Optional but Recommended)
```bash
python generate_sample_pdfs.py
```

This creates 3 sample PDFs in the `data/` directory:
- `sample_simple_text.pdf` - Basic text document
- `sample_multicolumn.pdf` - Multi-column layout
- `sample_complex_formatting.pdf` - Complex formatting with tables

---

## Usage

### Running Tests

#### Test 1: PDF Extraction Module
```bash
python tests/test_extraction.py
```

**What it tests:**
- PDF text extraction using PyMuPDF
- PDF text extraction using pdfplumber
- Fallback extraction mechanism
- PDF metadata extraction
- Error handling for corrupted/protected PDFs

#### Test 2: Text Cleaning Module
```bash
python tests/test_cleaning.py
```

**What it tests:**
- Extra whitespace removal
- Special character removal
- Header/footer elimination
- Text normalization
- Complete cleaning pipeline
- Edge cases (empty text, unicode, very long text)

#### Run All Tests
```bash
pytest tests/ -v
```

### Using the Modules Directly

#### PDF Extraction
```python
from backend.pdf_processor import PDFProcessor

processor = PDFProcessor("path/to/document.pdf")
result = processor.extract_all()
print(result['text_by_page'])
```

#### Text Cleaning
```python
from backend.text_cleaner import TextCleaner

cleaner = TextCleaner()
cleaned_text = cleaner.clean_text("Your messy text here...")
```

### Running Streamlit App (Future)
```bash
streamlit run frontend/app.py
```

---

## Module Documentation

### Backend Modules

#### 1. `pdf_processor.py`

**Class: PDFProcessor**

Methods:
- `extract_text_pymupdf()` - Extract text using PyMuPDF (fast, reliable)
- `extract_text_pdfplumber()` - Extract text using pdfplumber (better for tables)
- `get_pdf_metadata()` - Extract PDF metadata
- `extract_with_fallback()` - Try PyMuPDF first, fallback to pdfplumber
- `extract_all()` - Complete extraction with text and metadata

#### 2. `text_cleaner.py`

**Class: TextCleaner**

Methods:
- `remove_extra_whitespace(text)` - Normalize spaces and line breaks
- `remove_special_characters(text)` - Remove unwanted symbols
- `remove_headers_footers(text)` - Eliminate page numbers and headers
- `normalize_text(text)` - Lowercase and Unicode normalization
- `clean_text(text)` - Master method applying all cleaning steps

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Web UI framework |
| PyMuPDF | 1.23.8 | PDF text extraction |
| pdfplumber | 0.10.3 | PDF processing (fallback) |
| openai | 1.3.9 | OpenAI API integration |
| python-dotenv | 1.0.0 | Environment variable management |
| chromadb | 0.4.14 | Vector database |
| langchain | 0.1.1 | LLM framework |
| reportlab | 4.0.7 | PDF generation (testing) |
| sentence-transformers | 2.2.2 | Embeddings generation |
| faiss-cpu | 1.7.4 | Vector similarity search |
| pytest | 7.4.3 | Testing framework |

---

## Task Completion Status

### Task 1: Environment Setup & Project Initialization ✅
- [x] Complete folder structure created
- [x] Virtual environment setup documented
- [x] requirements.txt with all dependencies
- [x] Git repository initialized with .gitignore
- [x] README.md with comprehensive instructions

### Task 2: Basic PDF Text Extraction ✅
- [x] PDFProcessor class implemented
- [x] PyMuPDF and pdfplumber extraction
- [x] Metadata extraction
- [x] Error handling for corrupted/protected PDFs
- [x] Comprehensive test suite

### Task 3: Text Preprocessing & Cleaning ✅
- [x] TextCleaner class with all functions
- [x] Edge case handling
- [x] Comprehensive test suite

---

## Quick Start

```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Generate sample PDFs
python generate_sample_pdfs.py

# 3. Run extraction tests
python tests/test_extraction.py

# 4. Run text cleaning tests
python tests/test_cleaning.py
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
DEBUG=False
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fitz'"
```bash
pip install PyMuPDF==1.23.8
```

### Issue: "reportlab not found"
```bash
pip install reportlab==4.0.7
```

### Issue: Tests fail with path errors
Run from project root directory.

---

## Technologies Used
- **Streamlit**: Web application framework
- **PyMuPDF (fitz)**: PDF extraction and manipulation
- **pdfplumber**: PDF data extraction
- **OpenAI API**: Large language model for AI features
- **ChromaDB**: Vector database for embeddings
- **LangChain**: Framework for building AI applications
- **Python-dotenv**: Environment variable management

---

**Last Updated**: January 7, 2026
**Status**: Tasks 1-3 Complete ✅
**Version**: 1.0.0
