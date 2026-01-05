import streamlit as st

# Page configuration
st.set_page_config(
    page_title="SmartDocs AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and heading
st.title("SmartDocs AI")
st.subheader("Intelligent Document Processing System")

# Welcome message
st.write("Hello World!")

# Basic description
st.markdown("""
Welcome to SmartDocs AI - Your intelligent document processing assistant.

This application is designed to:
- Extract and analyze documents
- Process PDF files efficiently
- Provide intelligent insights using AI
- Store and manage document data

🚀 **Getting Started**: Navigate through the sidebar to explore different features.
""")

# Sidebar info
with st.sidebar:
    st.header("About")
    st.info("SmartDocs AI v1.0 - Internship Project")
    st.markdown("---")
    st.subheader("Quick Links")
    st.write("- Documentation: Coming soon")
    st.write("- GitHub: Coming soon")
