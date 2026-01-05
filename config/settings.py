"""
Configuration module for SmartDocs AI application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Application settings
APP_NAME = os.getenv("APP_NAME", "SmartDocs AI")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/smartdocs.db")

# File upload settings
UPLOAD_FOLDER = PROJECT_ROOT / "uploads"
DATA_FOLDER = PROJECT_ROOT / "data"
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Create folders if they don't exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
DATA_FOLDER.mkdir(exist_ok=True)

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
