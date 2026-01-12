import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.pdf_processor import PDFProcessor


def test_pdf_extraction():
    pdf_files = [
        "uploads/SmartDocs AI.pdf"
    ]

    for pdf in pdf_files:
        print(f"\nProcessing: {pdf}")

        try:
            processor = PDFProcessor(pdf)

            try:
                result = processor.extract_text_pymupdf()
            except:
                result = processor.extract_text_pdfplumber()

            metadata = processor.get_pdf_metadata()

            print("Metadata:", metadata)
            print("Total Pages:", result["total_pages"])

            first_page = next(iter(result["content"].values()))
            print("Sample Text:", first_page[:300])

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    test_pdf_extraction()
