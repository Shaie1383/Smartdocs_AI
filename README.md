# SmartDocs AI - Intelligent Document Processing System

## Project Overview
SmartDocs AI is an intelligent document processing application that leverages AI and machine learning to extract, analyze, and manage documents efficiently. This is an internship project for learning and developing production-ready Python applications.

## Features
- 📄 PDF document processing and extraction
- 🤖 AI-powered document analysis using OpenAI
- 💾 Vector database integration with ChromaDB
- 🔍 Semantic search capabilities using LangChain
- 🎨 Interactive web interface with Streamlit

## Project Structure
```
Smartdocs_AI/
├── backend/              # Backend logic and APIs
├── frontend/             # Streamlit web application
│   └── app.py           # Main application entry point
├── uploads/             # User uploaded files
├── data/                # Data storage and databases
├── utils/               # Utility functions and helpers
├── config/              # Configuration files
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation & Setup

### Step 1: Clone or Initialize Repository
```bash
cd Smartdocs_AI
git init
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application

### Start the Streamlit App
```bash
streamlit run frontend/app.py
```

The application will open in your default browser at `http://localhost:8501`

## Development Guide

### Project Structure Details
- **backend/**: Contains core business logic, API routes, and database operations
- **frontend/**: Streamlit UI components and page definitions
- **uploads/**: Temporary storage for user-uploaded documents (gitignored)
- **data/**: Vector database and persistent data storage
- **utils/**: Helper functions for PDF processing, text extraction, etc.
- **config/**: Configuration variables and settings

### Adding Dependencies
When adding new packages:
1. Install the package: `pip install package_name`
2. Update requirements.txt: `pip freeze > requirements.txt`
3. Commit changes to git

### Common Commands
```bash
# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# Deactivate virtual environment
deactivate

# Run tests
pytest

# Format code
black .

# Lint code
flake8 .
```

## Technologies Used
- **Streamlit**: Web application framework
- **PyMuPDF (fitz)**: PDF extraction and manipulation
- **pdfplumber**: PDF data extraction
- **OpenAI API**: Large language model for AI features
- **ChromaDB**: Vector database for embeddings
- **LangChain**: Framework for building AI applications
- **Python-dotenv**: Environment variable management

## API Keys & Configuration
To use the full functionality:
1. Get OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
2. Create `.env` file with your API key
3. Never commit `.env` file (it's in .gitignore)

## Git Workflow
```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Descriptive commit message"

# Push to remote (when applicable)
git push origin main
```

## Troubleshooting

### Virtual Environment Issues
- Ensure Python 3.8+ is installed: `python --version`
- Try creating venv with full path: `python -m venv c:\path\to\Smartdocs_AI\venv`

### Streamlit Issues
- Clear Streamlit cache: `streamlit cache clear`
- Restart the app if changes aren't reflected

### Dependency Issues
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## Next Steps
1. Implement backend PDF processing functions
2. Add OpenAI integration for document analysis
3. Set up ChromaDB for vector storage
4. Build additional Streamlit pages
5. Implement authentication (if needed)

## Contributing
Follow these guidelines when contributing:
- Create feature branches for new features
- Write clear commit messages
- Update documentation as needed
- Test code before committing

## License
This project is created for educational purposes during internship.

## Support
For issues or questions, please refer to the documentation or contact the project maintainer.

---

**Last Updated**: January 5, 2026
**Version**: 1.0.0
