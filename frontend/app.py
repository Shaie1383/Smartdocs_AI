import streamlit as st
import sys
from pathlib import Path
import os
import json
from datetime import datetime
import difflib

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

try:
    from pdf_processor import PDFProcessor
    from text_cleaner import TextCleaner
    BACKEND_AVAILABLE = True
except ImportError as e:
    BACKEND_AVAILABLE = False
    BACKEND_ERROR = str(e)

# Initialize session state for guidelines
if 'show_guidelines' not in st.session_state:
    st.session_state.show_guidelines = False

# Configure Streamlit page
st.set_page_config(
    page_title="SmartDocs AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIMPLIFIED CSS WITH DARK THEME - IMPROVED TEXT VISIBILITY
# ============================================================================

st.markdown("""
    <style>
    /* Global Dark Theme Background - Enhanced Multi-Color */
    .stApp {
        background: linear-gradient(135deg, 
            #0f0c29 0%, 
            #302b63 25%, 
            #24243e 50%, 
            #302b63 75%, 
            #0f0c29 100%);
        background-attachment: fixed;
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header:hover {
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
        transform: translateY(-3px);
    }
    
    .main-title {
        font-size: 2.8em;
        font-weight: bold;
        margin: 0;
        color: white !important;
        letter-spacing: 2px;
    }
    
    .main-subtitle {
        font-size: 1.1em;
        margin-top: 10px;
        color: white !important;
        opacity: 0.95;
        letter-spacing: 1px;
    }
    
    /* Sidebar Header */
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar-header:hover {
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    .sidebar-title {
        font-size: 1.8em;
        font-weight: bold;
        margin: 0;
        color: white !important;
        letter-spacing: 1px;
    }
    
    .sidebar-subtitle {
        font-size: 0.85em;
        margin-top: 8px;
        color: white !important;
        opacity: 0.95;
        letter-spacing: 0.5px;
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
        color: #0a3622 !important;
        padding: 15px;
        border-radius: 10px;
        margin: 12px 0;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.15);
    }
    
    .success-box:hover {
        box-shadow: 0 6px 18px rgba(40, 167, 69, 0.25);
        transform: translateX(3px);
    }
    
    /* Make ALL text in success box highly visible */
    .success-box *, 
    .success-box b, 
    .success-box strong,
    .success-box span,
    .success-box p {
        color: #0a3622 !important;
        font-weight: 700 !important;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #cfe2ff 0%, #b6d4fe 100%);
        border: 2px solid #0d6efd;
        color: #084298 !important;
        padding: 15px;
        border-radius: 10px;
        margin: 12px 0;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(13, 110, 253, 0.15);
    }
    
    .info-box:hover {
        box-shadow: 0 6px 18px rgba(13, 110, 253, 0.25);
        transform: translateX(3px);
    }
    
    /* Make ALL text in info box highly visible */
    .info-box *, 
    .info-box b, 
    .info-box strong,
    .info-box span,
    .info-box p {
        color: #052c65 !important;
        font-weight: 700 !important;
    }
    
    /* Error Box */
    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 2px solid #dc3545;
        color: #842029 !important;
        padding: 15px;
        border-radius: 10px;
        margin: 12px 0;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(220, 53, 69, 0.15);
    }
    
    .error-box:hover {
        box-shadow: 0 6px 18px rgba(220, 53, 69, 0.25);
        transform: translateX(3px);
    }
    .error-box * {
    color: #842029 !important;
    font-weight: 700 !important;
    }        
    
    /* Warning Box */
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
        border: 2px solid #ffc107;
        color: #664d03 !important;
        padding: 15px;
        border-radius: 10px;
        margin: 12px 0;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255, 193, 7, 0.15);
    }
    
    .warning-box:hover {
        box-shadow: 0 6px 18px rgba(255, 193, 7, 0.25);
        transform: translateX(3px);
    }
    
    /* Make ALL text in warning box highly visible */
    .warning-box *, 
    .warning-box b, 
    .warning-box strong,
    .warning-box span,
    .warning-box p {
        color: #523c02 !important;
        font-weight: 700 !important;
    }
    
    /* Task Headers */
    .task-header {
        color: #8899ff !important;
        font-size: 1.6em;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 15px;
        border-left: 5px solid #667eea;
        padding-left: 15px;
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }
    
    .task-header:hover {
        border-left-color: #764ba2;
        color: #aa99ff !important;
    }
    
    /* Metrics Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .metric-label {
        font-size: 0.95em;
        color: white !important;
        opacity: 0.95;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 2.2em;
        font-weight: bold;
        color: white !important;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #aaa !important;
        font-size: 0.95em;
        margin-top: 40px;
        padding: 30px 20px;
        border-top: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 10px;
    }
    
    .footer p {
        margin: 8px 0;
        color: #aaa !important;
        letter-spacing: 0.5px;
    }
    
    /* Guide Cards */
    .guide-card {
        transition: all 0.3s ease;
        border-radius: 15px;
    }
    
    .guide-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Text Area Styling */
    .stTextArea > textarea {
        border-radius: 12px !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        transition: all 0.3s ease !important;
        background-color: rgba(255, 255, 255, 0.98) !important;
        color: #333 !important;
    }
    
    .stTextArea > textarea:hover {
        border-color: #667eea !important;
        box-shadow: 0 2px 12px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stTextArea > textarea:focus {
        border-color: #764ba2 !important;
        box-shadow: 0 4px 18px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3) !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4) !important;
    }
    
    .stDownloadButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 10px rgba(79, 172, 254, 0.3) !important;
    }
    
    /* Text Color for Dark Theme - HIGH VISIBILITY */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f9fafb !important;
    }
    
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #e5e5e5 !important;
    }
    
    .stMarkdown p, .stMarkdown span, .stMarkdown div, .stMarkdown li {
        color: #e5e7eb !important;
    }
    /* ================= STREAMLIT OVERRIDE FIX ================= */

/* Force readable text inside ALL status boxes */
.stMarkdown .success-box,
.stMarkdown .success-box * {
    color: #0a3622 !important;
    opacity: 1 !important;
}

.stMarkdown .info-box,
.stMarkdown .info-box * {
    color: #052c65 !important;
    opacity: 1 !important;
}

.stMarkdown .warning-box,
.stMarkdown .warning-box * {
    color: #523c02 !important;
    opacity: 1 !important;
}

.stMarkdown .error-box,
.stMarkdown .error-box * {
    color: #842029 !important;
    opacity: 1 !important;
}

/* Kill Streamlit's opacity rule */
.stMarkdown * {
    opacity: 1 !important;
}

    
    
    /* Sidebar styling */
    .stSidebar {
        background-color: rgba(15, 15, 30, 0.95) !important;
    }
    
    .stSidebar * {
        color: #e8e8e8 !important;
    }
    
    /* Labels and small text */
    label, .stMarkdown small {
        color: #cccccc !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

# Sidebar Header
st.sidebar.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-title">🤖 SmartDocs AI</div>
        <div class="sidebar-subtitle">PDF Intelligence Platform</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'file_details' not in st.session_state:
    st.session_state.file_details = []
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'file_path' not in st.session_state:
    st.session_state.file_path = None
if 'extraction_result' not in st.session_state:
    st.session_state.extraction_result = None
if 'cleaned_text' not in st.session_state:
    st.session_state.cleaned_text = None
if 'task_completed' not in st.session_state:
    st.session_state.task_completed = {}
if 'process_triggered' not in st.session_state:
    st.session_state.process_triggered = False

# ============================================================================
# FILE UPLOAD WITH VALIDATION
# ============================================================================

st.sidebar.markdown("### 📁 Upload PDF Documents")

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

uploaded_files = st.sidebar.file_uploader(
    "Choose PDF file(s) to process",
    type=["pdf"],
    accept_multiple_files=True,
    help=f"Upload one or more PDF files (max {MAX_FILE_SIZE_MB}MB per file). Only .pdf files are accepted."
)

validated_files = []
upload_messages = []

if uploaded_files:
    uploads_dir = Path(__file__).parent.parent / "uploads"
    uploads_dir.mkdir(exist_ok=True)
    
    for uploaded_file in uploaded_files:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        if uploaded_file.size > MAX_FILE_SIZE_BYTES:
            upload_messages.append({
                "type": "error",
                "message": f"❌ **{uploaded_file.name}** - File size ({file_size_mb:.2f}MB) exceeds {MAX_FILE_SIZE_MB}MB limit"
            })
        elif not uploaded_file.name.lower().endswith('.pdf'):
            upload_messages.append({
                "type": "error",
                "message": f"❌ **{uploaded_file.name}** - Invalid file type. Only PDF files are allowed"
            })
        else:
            try:
                temp_path = uploads_dir / uploaded_file.name
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                validated_files.append({
                    "name": uploaded_file.name,
                    "size": file_size_mb,
                    "path": str(temp_path),
                    "size_bytes": uploaded_file.size,
                    "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                upload_messages.append({
                    "type": "success",
                    "message": f"✅ **{uploaded_file.name}** - Validated ({file_size_mb:.2f}MB)"
                })
            except Exception as e:
                upload_messages.append({
                    "type": "error",
                    "message": f"❌ **{uploaded_file.name}** - Error saving file: {str(e)}"
                })
    
    st.session_state.uploaded_files = validated_files
    
    st.sidebar.markdown("#### Validation Results:")
    for msg in upload_messages:
        if msg["type"] == "success":
            st.sidebar.markdown(f'<div class="success-box">{msg["message"]}</div>', unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f'<div class="error-box">{msg["message"]}</div>', unsafe_allow_html=True)

if st.session_state.uploaded_files:
    file_count = len(st.session_state.uploaded_files)
    total_size = sum(f["size"] for f in st.session_state.uploaded_files)
    
    st.sidebar.markdown(f"""
        <div style="background: #667eea; color: white; padding: 12px; border-radius: 6px; text-align: center;">
        <b style="font-size: 1.2em;">📊 Files Uploaded: <span style="font-size: 1.4em;">{file_count}</span></b><br>
        <small>Total Size: {total_size:.2f} MB</small>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("### ⚙️ Process Documents")

if st.session_state.uploaded_files:
    if st.sidebar.button("🚀 Process Documents", key="process_btn", use_container_width=True):
        st.session_state.process_triggered = True
else:
    st.sidebar.button("🚀 Process Documents", key="process_btn", use_container_width=True, disabled=True)

st.sidebar.markdown("---")

# Guidelines Collapsible Button
if st.sidebar.button("📋 Guidelines", use_container_width=True, key="guidelines_btn"):
    st.session_state.show_guidelines = not st.session_state.show_guidelines

if st.session_state.show_guidelines:
    st.sidebar.markdown("""
**File Requirements:**
- 📄 Format: PDF only
- 📏 Size: Max 10MB per file
- 🔢 Multiple: Yes, batch upload

**Tips:**
- ✓ Use high-quality PDFs
- ✓ Check file integrity
- ✓ Ensure readable content
- ✓ Organize by category
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; color: #666; font-size: 0.85em;">
<b>SmartDocs AI v1.0.0</b><br>
Infosys Springboard<br>
© 2026 All Rights Reserved
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

st.markdown("""
    <div class="main-header">
        <div class="main-title">🤖 SmartDocs AI</div>
        <div class="main-subtitle">Intelligent PDF Processing & Analysis Platform</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
Advanced document intelligence system for PDF processing, text extraction, automatic cleaning, 
and comprehensive document comparison with detailed analytics.
""")

st.markdown("---")

# ============================================================================
# SECTION 1: UPLOADED FILES MANAGEMENT
# ============================================================================

st.markdown("""
<div class="task-header">
    📂 Upload & Validate Documents
</div>
""", unsafe_allow_html=True)

if st.session_state.uploaded_files:
    st.markdown(f"""
        <div class="success-box">
        ✅ <b>{len(st.session_state.uploaded_files)} document(s) validated and ready for processing</b>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### File Information")
    
    table_data = []
    for idx, file_info in enumerate(st.session_state.uploaded_files, 1):
        table_data.append({
            "No.": idx,
            "Document Name": file_info["name"],
            "Size (MB)": f"{file_info['size']:.2f}",
            "Uploaded": file_info["upload_time"],
            "Status": "✅ Ready"
        })
    
    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "No.": st.column_config.NumberColumn("No."),
            "Document Name": st.column_config.TextColumn("Document Name"),
            "Size (MB)": st.column_config.TextColumn("Size (MB)"),
            "Uploaded": st.column_config.TextColumn("Uploaded"),
            "Status": st.column_config.TextColumn("Status")
        }
    )
    
    st.markdown("#### 📊 Processing Statistics")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Documents</div>
                <div class="metric-value">{len(st.session_state.uploaded_files)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        total_size = sum(f["size"] for f in st.session_state.uploaded_files)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Size</div>
                <div class="metric-value">{total_size:.2f} MB</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        session_status = "🟢 Active" if st.session_state.uploaded_files else "🟡 Waiting"
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Session Status</div>
                <div class="metric-value" style="font-size: 1.3em;">{session_status}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Add Chunking Summary (Task 6)
    st.markdown("#### 📊 Chunking Summary")
    
    col_chunk1, col_chunk2, col_chunk3 = st.columns(3)
    
    with col_chunk1:
        # Calculate total pages from uploaded files (placeholder - will be accurate after processing)
        total_pages = 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Pages Processed</div>
                <div class="metric-value">{total_pages}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_chunk2:
        # Total chunks created (placeholder - will be calculated during processing)
        total_chunks = 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Chunks Created</div>
                <div class="metric-value">{total_chunks}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_chunk3:
        # Chunk size information
        chunk_size_info = "Text-based"
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Chunk Size Info</div>
                <div class="metric-value" style="font-size: 1.3em;">{chunk_size_info}</div>
            </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div class="info-box">
        ℹ️ <b>Ready to Process Documents</b><br>
        Upload PDF files using the sidebar file uploader to begin. You can upload multiple files for batch processing.
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SECTION 2: PROCESSING STEPS
# ============================================================================

st.markdown("""
<div class="task-header">
    ⚙️ Process Documents
</div>
""", unsafe_allow_html=True)

if st.session_state.uploaded_files:
    col_process1, col_process2 = st.columns([3, 1])
    
    with col_process1:
        st.markdown("""
        **Processing Pipeline:**
        1. **Extract** - Advanced text extraction using PyMuPDF and pdfplumber
        2. **Clean** - Automatic text cleaning, normalization, and formatting
        3. **Compare** - Side-by-side comparison of raw vs. processed text
        4. **Download** - Export results in multiple formats
        """)
    
    with col_process2:
        if not BACKEND_AVAILABLE:
            st.warning("⚠️ Install dependencies")
        else:
            if st.button("🚀 Process All Documents", key="process_btn_main", use_container_width=True, type="primary"):
                st.session_state.process_triggered = True
                st.success("✅ Processing started! Scroll down to see results.")
    
    st.markdown("---")
    
    if st.session_state.process_triggered:
        if not BACKEND_AVAILABLE:
            st.error(f"❌ Backend Error: {BACKEND_ERROR}")
            st.info("Please install PyMuPDF: `pip install PyMuPDF`")
        else:
            st.markdown("""
            <div class="task-header">
                📄 Processing Results - Page by Page Comparison
            </div>
            """, unsafe_allow_html=True)
            
            for idx, file_info in enumerate(st.session_state.uploaded_files, 1):
                st.markdown(f"### 📋 {file_info['name']}")
                
                try:
                    processor = PDFProcessor(file_info["path"])
                    extraction_result = processor.extract_all()
                    cleaner = TextCleaner()
                    
                    content = extraction_result.get("content", {})
                    
                    if content:
                        for page_num in sorted(content.keys()):
                            raw_page_text = content[page_num]
                            cleaned_page_text = cleaner.clean_text(raw_page_text)
                            
                            with st.expander(f"📄 Page {page_num}", expanded=(page_num == 1)):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("**Raw Text**")
                                    st.text_area(
                                        "Raw Content",
                                        value=raw_page_text,
                                        height=400,
                                        disabled=True,
                                        key=f"raw_{idx}_{page_num}",
                                        label_visibility="collapsed"
                                    )
                                
                                with col2:
                                    st.markdown("**Cleaned Text**")
                                    st.text_area(
                                        "Cleaned Content",
                                        value=cleaned_page_text,
                                        height=400,
                                        disabled=True,
                                        key=f"clean_{idx}_{page_num}",
                                        label_visibility="collapsed"
                                    )
                        
                        full_raw_text = "\n\n".join([f"=== PAGE {p} ===\n{content[p]}" for p in sorted(content.keys())])
                        full_cleaned_text = "\n\n".join([f"=== PAGE {p} ===\n{cleaner.clean_text(content[p])}" for p in sorted(content.keys())])
                        
                        st.session_state.cleaned_text = {
                            "raw": full_raw_text,
                            "cleaned": full_cleaned_text,
                            "file_name": file_info["name"]
                        }
                        
                        st.markdown("---")
                        st.markdown("#### 📥 Download Results")
                        col_down1, col_down2, col_down3 = st.columns(3)
                        
                        with col_down1:
                            st.download_button(
                                label="📄 Download Raw Text",
                                data=full_raw_text,
                                file_name=f"raw_{file_info['name']}.txt",
                                mime="text/plain",
                                use_container_width=True,
                                key=f"download_raw_{idx}"
                            )
                        
                        with col_down2:
                            st.download_button(
                                label="✨ Download Cleaned Text",
                                data=full_cleaned_text,
                                file_name=f"cleaned_{file_info['name']}.txt",
                                mime="text/plain",
                                use_container_width=True,
                                key=f"download_clean_{idx}"
                            )
                        
                        with col_down3:
                            json_data = {
                                "file_name": file_info["name"],
                                "raw_text": full_raw_text,
                                "cleaned_text": full_cleaned_text,
                                "total_pages": len(content),
                                "timestamp": datetime.now().isoformat()
                            }
                            st.download_button(
                                label="📊 Download as JSON",
                                data=json.dumps(json_data, indent=2),
                                file_name=f"results_{file_info['name']}.json",
                                mime="application/json",
                                use_container_width=True,
                                key=f"download_json_{idx}"
                            )
                    else:
                        st.error("❌ No text content could be extracted from this PDF.")
                    
                    st.markdown("---")
                
                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")
                    st.markdown("---")

else:
    st.markdown("""
    <div class="warning-box">
    ⚠️ <b>No Documents Uploaded</b><br>
    Please upload PDF files using the sidebar to begin processing.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# USER GUIDE
# ============================================================================

st.markdown("""
<div class="task-header">
    📚 How to Use SmartDocs AI
</div>
""", unsafe_allow_html=True)

col_guide1, col_guide2, col_guide3 = st.columns(3)

with col_guide1:
    st.markdown("""
    <div class="guide-card" style="padding: 25px; border-radius: 10px; border: 2px solid #667eea; text-align: center; min-height: 280px; background: rgba(102, 126, 234, 0.05);">
        <h2 style="color: #8899ff; margin-top: 0;">📤 Upload</h2>
        <div style="font-size: 1.1em; line-height: 1.8; color: #d8d8d8;">
        <p style="color: #d8d8d8;">✓ Click file uploader in sidebar</p>
        <p style="color: #d8d8d8;">✓ Select PDF documents</p>
        <p style="color: #d8d8d8;">✓ Multiple files supported</p>
        <p style="color: #d8d8d8;">✓ Automatic validation</p>
        <p style="margin-bottom: 0; color: #d8d8d8;"><b>Max: 10MB per file</b></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_guide2:
    st.markdown("""
    <div class="guide-card" style="padding: 25px; border-radius: 10px; border: 2px solid #f093fb; text-align: center; min-height: 280px; background: rgba(240, 147, 251, 0.05);">
        <h2 style="color: #ff99dd; margin-top: 0;">⚙️ Process</h2>
        <div style="font-size: 1.1em; line-height: 1.8; color: #d8d8d8;">
        <p style="color: #d8d8d8;">✓ Click "Process Documents"</p>
        <p style="color: #d8d8d8;">✓ AI extracts all text</p>
        <p style="color: #d8d8d8;">✓ Auto-cleaning applied</p>
        <p style="color: #d8d8d8;">✓ Page-by-page comparison</p>
        <p style="margin-bottom: 0; color: #d8d8d8;"><b>Real-time results</b></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_guide3:
    st.markdown("""
    <div class="guide-card" style="padding: 25px; border-radius: 10px; border: 2px solid #4facfe; text-align: center; min-height: 280px; background: rgba(79, 172, 254, 0.05);">
        <h2 style="color: #66ccff; margin-top: 0;">💾 Download</h2>
        <div style="font-size: 1.1em; line-height: 1.8; color: #d8d8d8;">
        <p style="color: #d8d8d8;">✓ Raw text format (TXT)</p>
        <p style="color: #d8d8d8;">✓ Cleaned text format (TXT)</p>
        <p style="color: #d8d8d8;">✓ Complete data (JSON)</p>
        <p style="color: #d8d8d8;">✓ Ready to use anywhere</p>
        <p style="margin-bottom: 0; color: #d8d8d8;"><b>Instant downloads</b></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div class="footer">
<p><b>SmartDocs AI v1.0.0</b> - Intelligent PDF Processing Platform</p>
<p>Infosys Springboard | © 2026 All Rights Reserved</p>
<p style="color: #999; font-size: 0.85em;">
Advanced document intelligence system for automated PDF processing, text extraction, and analysis
</p>
</div>
""", unsafe_allow_html=True)
