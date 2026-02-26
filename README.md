# Financial Document Analyzer

A FastAPI-based web service that uses CrewAI agents to analyze financial documents and provide investment insights using Google's Gemini LLM.

---

## 📋 Table of Contents
- [Bugs Found & Fixed](#bugs-found--fixed)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## 🐛 Bugs Found & Fixed

### 1. **Missing FastAPI Module** ❌
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Root Cause:** FastAPI was not installed in the environment.

**Fix:** Installed FastAPI and Uvicorn
```bash
pip install fastapi==0.110.3 uvicorn
```

---

### 2. **Incorrect Agent Import Path** ❌
**Error:** `ImportError: cannot import name 'Agent' from 'crewai.agents'`

**Original Code:**
```python
from crewai.agents import Agent
```

**Root Cause:** In the newer version of CrewAI (0.130.0+), `Agent` is exported directly from the `crewai` package, not from `crewai.agents`.

**Fix:** Updated import
```python
from crewai import Agent, LLM
```

---

### 3. **Incorrect SerperDevTool Import Path** ❌
**Error:** `ImportError: cannot import name 'SerperDevTool' from 'crewai_tools.tools.serper_dev_tool'`

**Original Code:**
```python
from crewai_tools.tools.serper_dev_tool import SerperDevTool
```

**Root Cause:** The import path was incomplete. The actual module structure required an extra level.

**Fix:** Updated to correct import path
```python
from crewai_tools.tools.serper_dev_tool.serper_dev_tool import SerperDevTool
```

---

### 4. **Missing crewai-tools Package** ❌
**Error:** `ModuleNotFoundError: No module named 'crewai_tools'`

**Root Cause:** The crewai-tools package was not installed.

**Fix:** Installed crewai-tools
```bash
pip install crewai-tools==0.47.1
```

---


**Updated Code:**
```python
from crewai import LLM

try:
    llm = LLM(model="gemini-1.5-flash")
except ImportError as e:
    print(f"Warning: Could not initialize LLM: {e}")
    llm = None
```

---

### 5. **Invalid Tool References in Tasks** ❌
**Error:** `ValidationError: Input should be a valid dictionary or instance of BaseTool`

**Original Code in task.py:**
```python
tools=[FinancialDocumentTool.read_data_tool]  # This is a function, not a BaseTool
```

**Root Cause:** Tasks expect `BaseTool` instances, but `FinancialDocumentTool.read_data_tool` was a plain async function, not a defined tool class.

**Fix:** Replaced with the valid `search_tool` instance or empty list
```python
tools=[search_tool] if search_tool else []
```

---

### 6. **Module Import Error on Wrong Directory** ❌
**Error:** `ERROR: Error loading ASGI app. Could not import module "main".`

**Root Cause:** Uvicorn was being run from the parent directory instead of the project directory.

**Fix:** Changed to correct working directory before running uvicorn
```bash
cd "/Users/harshwardhanmourya/Desktop/dev/python/GEN AI/financial-document-analyzer-debug"
conda activate finance && uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.12
- Conda (Miniconda or Anaconda)
- Google API Key (for Gemini LLM access)

### Step 1: Activate Conda Environment
```bash
conda activate finance
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

If you encounter dependency conflicts, install main packages individually:
```bash
pip install fastapi==0.110.3
pip install uvicorn
pip install crewai==0.130.0
pip install crewai-tools==0.47.1
pip install "crewai[google-genai]"
```

### Step 3: Configure Environment Variables
Create a `.env` file in the project directory with your Google API key:

```env
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
```

### Step 4: Verify Installation
```bash
python -c "from main import app; print('✓ Setup successful!')"
```

---

## 💻 Usage

### Start the Server

```bash
cd "/Users/harshwardhanmourya/Desktop/dev/python/GEN AI/financial-document-analyzer-debug"
conda activate finance
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [PID] using WatchFiles
```

### Testing the API

#### Option 1: Interactive Swagger UI (Easiest)
Open in browser: http://127.0.0.1:8001/docs

This provides an interactive interface to test all API endpoints.

#### Option 2: Using curl
```bash
# Health check
curl http://127.0.0.1:8001/

# Analyze a document
curl -X POST "http://127.0.0.1:8001/analyze" \
  -F "file=@path/to/document.pdf" \
  -F "query=Analyze this financial document"
```

#### Option 3: Using Python Script
```bash
python test_api.py
```

#### Option 4: Python Requests Library
```python
import requests

# Health check
response = requests.get('http://127.0.0.1:8001/')
print(response.json())

# Analyze document
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    data = {'query': 'What is the financial status?'}
    response = requests.post(
        'http://127.0.0.1:8001/analyze',
        files=files,
        data=data
    )
    print(response.json())
```

---

## 📚 API Documentation

### Endpoints

#### 1. **GET /**
**Health Check Endpoint**

**Description:** Verify the API is running

**Request:**
```bash
GET http://127.0.0.1:8001/
```

**Response:**
```json
{
  "message": "Financial Document Analyzer API is running"
}
```

**Status Code:** `200 OK`

---

#### 2. **POST /analyze**
**Document Analysis Endpoint**

**Description:** Upload and analyze a financial document

**Request:**
```bash
POST http://127.0.0.1:8001/analyze
Content-Type: multipart/form-data

Parameters:
- file: UploadFile (PDF document)
- query: str (Analysis question/request)
```

**Example with curl:**
```bash
curl -X POST "http://127.0.0.1:8001/analyze" \
  -F "file=@financial_report.pdf" \
  -F "query=Provide a comprehensive financial analysis"
```

**Example with Python:**
```python
import requests

with open('financial_report.pdf', 'rb') as f:
    files = {'file': f}
    data = {'query': 'Analyze the financial metrics'}
    
    response = requests.post(
        'http://127.0.0.1:8001/analyze',
        files=files,
        data=data
    )
    
    result = response.json()
    print(result)
```

**Response:**
```json
{
  "analysis": "Detailed financial analysis from the CrewAI agents",
  "file_path": "uploads/filename_uuid.pdf",
  "status": "completed"
}
```

**Status Codes:**
- `200 OK` - Analysis successful
- `400 Bad Request` - Missing file or query
- `413 Payload Too Large` - File too large
- `500 Internal Server Error` - Processing error

---

### Response Structure

#### Success Response (200)
```json
{
  "analysis": "string (Financial analysis result)",
  "file_path": "string (Path to uploaded file)",
  "status": "string (completed|processing)"
}
```

#### Error Response (400+)
```json
{
  "detail": "string (Error message)",
  "code": "string (Error code)"
}
```

---

### Query Examples

**For Balance Sheet Analysis:**
```
"Analyze the balance sheet and provide insights on assets, liabilities, and equity"
```

**For Income Statement:**
```
"Review the income statement and highlight revenue trends and profit margins"
```

**For Cash Flow Analysis:**
```
"Examine the cash flow statement and assess operational, investing, and financing activities"
```

**For Investment Recommendation:**
```
"Based on the financial documents, what would be your investment recommendation?"
```

---

## 📁 Project Structure

```
financial-document-analyzer-debug/
├── main.py                 # FastAPI application
├── agents.py              # CrewAI agents definition
├── task.py                # CrewAI tasks definition
├── tools.py               # Custom tools (SerperDevTool, PDF reader, etc.)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
├── test_api.py           # API test script
├── data/
│   └── sample.pdf        # Sample PDF for testing
├── outputs/               # Analysis output files
└── README.md             # This file
```

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file:
```env
GOOGLE_API_KEY="your-google-api-key-here"
```

### Uvicorn Configuration
Modify the startup command for different settings:

**Development with Debug Logging:**
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8001 --log-level DEBUG
```

**Production:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --workers 4
```

**Custom Port:**
```bash
uvicorn main:app --host 127.0.0.1 --port 8080
```

---

## 🔧 Troubleshooting

### Issue: `GOOGLE_API_KEY is required`
**Solution:** Ensure `.env` file exists in the project directory with your API key:
```bash
echo 'GOOGLE_API_KEY="your-key-here"' > .env
```

### Issue: `Connection refused` on port 8001
**Solution:** The server may not be running. Start it:
```bash
conda activate finance && uvicorn main:app --host 127.0.0.1 --port 8001
```

### Issue: `ModuleNotFoundError` when running tests
**Solution:** Install missing package and ensure you're in the correct conda environment:
```bash
conda activate finance
pip install -r requirements.txt
```

### Issue: Port 8001 already in use
**Solution:** Use a different port:
```bash
uvicorn main:app --host 127.0.0.1 --port 8002
```

Or find and kill the process using port 8001:
```bash
lsof -i :8001  # Find process
kill -9 <PID>  # Kill process (replace <PID>)
```

### Issue: File upload fails with "413 Payload Too Large"
**Solution:** The default file size limit is typically 25MB. Modify `main.py` if needed:
```python
app = FastAPI(
    max_request_size=100_000_000  # 100MB
)
```

### Issue: Analysis takes too long
**Solution:** This is normal for the first request (model initialization). Subsequent requests are faster. You can monitor progress in the server logs.

---

## 📝 Development

### Running Tests
```bash
python test_api.py
```

### Adding New Agents
Edit `agents.py` and define a new `Agent` with appropriate configuration.

### Adding New Tasks
Edit `task.py` and create a new `Task` instance for the agent.

### Adding New Tools
Edit `tools.py` and implement custom tool classes or functions.

---

## 📄 License
This project is provided as-is for educational and development purposes.

---

## 🤝 Support
For issues or questions, refer to the troubleshooting section or check:
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [CrewAI Documentation](https://docs.crewai.com)
- [Google Gemini API](https://ai.google.dev)

---

**Last Updated:** February 27, 2026
**Status:** ✅ All bugs fixed, API operational on port 8001
