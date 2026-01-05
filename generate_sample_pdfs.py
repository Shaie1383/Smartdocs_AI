"""
Sample PDF Generator for Testing
Creates 3 different types of PDFs for testing the PDF processor
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.units import inch
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_simple_text_pdf():
    """Create a simple text document PDF"""
    output_path = Path(__file__).parent / "data" / "sample_simple_text.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Add content
    title_style = styles['Title']
    story.append(Paragraph("Sample PDF 1: Simple Text Document", title_style))
    story.append(Spacer(1, 0.3 * inch))
    
    body_style = styles['BodyText']
    content = """
    <b>Introduction</b><br/>
    This is a simple text PDF document used for testing the PDF processor module.
    It contains basic text content without complex formatting or multiple columns.
    <br/><br/>
    
    <b>Content Section</b><br/>
    The PDF processor should be able to extract all the text from this document
    without any issues. The extraction should preserve the general structure and
    formatting of the content.
    <br/><br/>
    
    <b>Features Tested</b><br/>
    - Basic text extraction<br/>
    - Paragraph handling<br/>
    - Bold and italic text preservation<br/>
    - Line breaks and spacing<br/>
    <br/><br/>
    
    <b>Conclusion</b><br/>
    This simple document serves as the baseline for testing PDF text extraction
    functionality. It should produce clean, readable output with proper formatting.
    """
    story.append(Paragraph(content, body_style))
    story.append(Spacer(1, 0.5 * inch))
    
    # Build PDF
    doc.build(story)
    logger.info(f"Created simple text PDF: {output_path}")
    return output_path


def create_multicolumn_pdf():
    """Create a multi-column layout PDF"""
    output_path = Path(__file__).parent / "data" / "sample_multicolumn.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = styles['Title']
    story.append(Paragraph("Sample PDF 2: Multi-Column Layout", title_style))
    story.append(Spacer(1, 0.3 * inch))
    
    # Create a table for multi-column effect
    col1_text = """
    <b>Column 1</b><br/><br/>
    This is the first column of content. The PDF processor needs to handle
    multi-column layouts properly. Text extraction should combine content
    from multiple columns in a logical order.<br/><br/>
    
    <b>Key Points:</b><br/>
    • Point 1: Text extraction<br/>
    • Point 2: Column handling<br/>
    • Point 3: Layout preservation<br/><br/>
    
    The challenge here is to maintain readability when combining columns.
    """
    
    col2_text = """
    <b>Column 2</b><br/><br/>
    This is the second column of content. Multi-column documents are common
    in newspapers, magazines, and professional reports. Proper handling is
    crucial for accurate text extraction.<br/><br/>
    
    <b>Considerations:</b><br/>
    • Column width variation<br/>
    • Text flow direction<br/>
    • Merged cells<br/><br/>
    
    The processor should intelligently combine columns in reading order.
    """
    
    col_style = styles['BodyText']
    
    # Create two-column table
    col_data = [
        [Paragraph(col1_text, col_style), Paragraph(col2_text, col_style)]
    ]
    
    col_table = Table(col_data, colWidths=[3.25 * inch, 3.25 * inch])
    col_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    story.append(col_table)
    
    # Build PDF
    doc.build(story)
    logger.info(f"Created multi-column PDF: {output_path}")
    return output_path


def create_complex_formatting_pdf():
    """Create a PDF with complex formatting"""
    output_path = Path(__file__).parent / "data" / "sample_complex_formatting.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = styles['Title']
    story.append(Paragraph("Sample PDF 3: Complex Formatting", title_style))
    story.append(Spacer(1, 0.3 * inch))
    
    # Add complex content with tables
    body_style = styles['BodyText']
    story.append(Paragraph("<b>Section 1: Data Table</b>", body_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Create a data table
    table_data = [
        ['Product', 'Q1', 'Q2', 'Q3', 'Q4', 'Total'],
        ['Widget A', '$1,200', '$1,500', '$1,800', '$2,100', '$6,600'],
        ['Widget B', '$900', '$1,100', '$1,300', '$1,600', '$4,900'],
        ['Widget C', '$2,000', '$2,200', '$2,400', '$2,800', '$9,400'],
        ['Service X', '$3,500', '$3,800', '$4,000', '$4,200', '$15,500'],
    ]
    
    table = Table(table_data, colWidths=[1.5 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1.25 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.3 * inch))
    
    # Add more content
    story.append(Paragraph("<b>Section 2: Mixed Content</b>", body_style))
    story.append(Spacer(1, 0.2 * inch))
    
    mixed_content = """
    This section demonstrates <b>bold text</b>, <i>italic text</i>, and 
    <u>underlined text</u>. The processor should handle these formatting
    elements properly.<br/><br/>
    
    We also have <font color="red">colored text</font> and 
    <font size=12>different font sizes</font>.<br/><br/>
    
    Special characters and symbols: © ® ™ € £ ¥<br/>
    Mathematical symbols: ∑ ∫ √ ∞ ≈ ≠<br/>
    """
    
    story.append(Paragraph(mixed_content, body_style))
    story.append(PageBreak())
    
    # Add second page
    story.append(Paragraph("Page 2: Continuation", title_style))
    story.append(Spacer(1, 0.3 * inch))
    
    page2_content = """
    <b>Additional Information</b><br/><br/>
    This is the second page of the complex formatting PDF. It tests the
    processor's ability to handle multiple pages and extract content from
    each page separately.<br/><br/>
    
    The extraction should preserve:<br/>
    1. Page breaks and pagination<br/>
    2. Text order and logical flow<br/>
    3. Table structures and data<br/>
    4. Special characters and symbols<br/>
    5. Different formatting styles<br/>
    """
    
    story.append(Paragraph(page2_content, body_style))
    
    # Build PDF
    doc.build(story)
    logger.info(f"Created complex formatting PDF: {output_path}")
    return output_path


def generate_sample_pdfs():
    """Generate all sample PDFs for testing"""
    logger.info("Starting sample PDF generation...")
    
    try:
        create_simple_text_pdf()
        create_multicolumn_pdf()
        create_complex_formatting_pdf()
        logger.info("All sample PDFs created successfully!")
        return True
    except Exception as e:
        logger.error(f"Error generating sample PDFs: {str(e)}")
        return False


if __name__ == "__main__":
    generate_sample_pdfs()
