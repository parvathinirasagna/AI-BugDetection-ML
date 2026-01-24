# 🚀 How to Run Frontend & Backend Together

## Quick Summary

You need to run **TWO terminals** at the same time:
1. **Terminal 1**: Backend (Python/FastAPI) on port 8000
2. **Terminal 2**: Frontend (React) on port 3000

---

## Step-by-Step Setup & Run

### Prerequisites
- ✅ Python 3.8+ installed
- ✅ Node.js & npm installed
- ✅ Code cloned: `git clone https://github.com/parvathinirasagna/AI-BugDetection-ML.git`

---

## Method 1: Using Two Terminal Windows (Recommended)

### Terminal 1: Start Backend Server

```bash
# Navigate to backend directory
cd AI-BugDetection-ML/backend

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies (if not done)
pip install -r requirements.txt

# Run backend server
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ Backend is now running at `http://localhost:8000`

---

### Terminal 2: Start Frontend Server

**Open a NEW terminal window** and run:

```bash
# Navigate to frontend directory
cd AI-BugDetection-ML/frontend

# Install dependencies (first time only)
npm install

# Start React development server
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view ai-bugdetection-ml in the browser.
  http://localhost:3000/

Note that the development build is not optimized.
```

✅ Frontend is now running at `http://localhost:3000`

---

## Method 2: Using a Single Terminal (Advanced)

If you want to run both from one terminal, use `&` (background process):

### Windows:
```cmd
cd AI-BugDetection-ML/backend
venv\Scripts\activate
start "Backend" cmd /k "python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000"

cd ../frontend
start "Frontend" cmd /k "npm start"
```

### Mac/Linux:
```bash
cd AI-BugDetection-ML/backend
source venv/bin/activate
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000 &

cd ../frontend
npm start
```

---

## Method 3: Using Docker (Optional)

If you have Docker installed:

```bash
cd AI-BugDetection-ML

# Build and run both services
docker-compose up
```

---

## Complete Setup Checklist

### Backend Setup:
- [ ] Navigate to `backend` directory: `cd AI-BugDetection-ML/backend`
- [ ] Create virtual env: `python -m venv venv`
- [ ] Activate venv:
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run server: `python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000`
- [ ] Verify at http://localhost:8000/docs ✓

### Frontend Setup:
- [ ] Navigate to `frontend` directory: `cd AI-BugDetection-ML/frontend`
- [ ] Install dependencies: `npm install`
- [ ] Run React: `npm start`
- [ ] Browser opens at http://localhost:3000 ✓

---

## Test Both Are Running

### Check Backend:
```bash
curl http://localhost:8000/docs
```
Should show Swagger UI documentation

### Check Frontend:
```bash
curl http://localhost:3000
```
Should show React app HTML

---

## Frontend & Backend Communication

The frontend makes API calls to the backend:

```javascript
// Example in React component
const analyzeBugs = async (codeSnippet) => {
  const response = await fetch('http://localhost:8000/analyze-multilang', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ code_snippet: codeSnippet })
  });
  const data = await response.json();
  return data;
};
```

---

## Directory Structure

```
AI-BugDetection-ML/
├── backend/                    ← Terminal 1 runs here
│   ├── venv/                   ← Virtual environment
│   ├── app.py                  ← FastAPI server
│   ├── multi_language_detector.py
│   ├── feature_extractor.py
│   ├── requirements.txt
│   └── ... other files
│
├── frontend/                   ← Terminal 2 runs here
│   ├── src/
│   │   ├── App.jsx             ← Main React component
│   │   ├── index.js
│   │   └── ... other components
│   ├── package.json
│   └── public/
│
└── README.md
```

---

## Accessing the Application

### Frontend UI:
- **URL**: http://localhost:3000
- **Purpose**: User interface for code analysis
- **Features**: Code editor, language selector, bug display

### Backend API:
- **URL**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs (interactive API docs)
- **Endpoints**:
  - `POST /analyze-multilang` - Analyze code
  - `GET /` - Health check

---

## Ports Explanation

| Service | Port | URL | Purpose |
|---------|------|-----|----------|
| Backend (FastAPI) | 8000 | http://localhost:8000 | API server |
| Backend Docs | 8000 | http://localhost:8000/docs | Interactive API explorer |
| Frontend (React) | 3000 | http://localhost:3000 | Web UI |

---

## Troubleshooting

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Change backend port
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8001

# Change frontend port (in package.json or):
PORT=3001 npm start
```

### Frontend Can't Connect to Backend

**Error**: Network error when submitting code

**Solution**: Update API URL in frontend if ports changed:
```javascript
// In frontend/src/App.jsx or config
const API_URL = 'http://localhost:8000'; // Update if port is different
```

### Module Not Found

**Backend**: `pip install -r requirements.txt`

**Frontend**: `npm install`

### Virtual Environment Issues

```bash
# Recreate virtual environment
cd backend
rmdir /s venv  # Windows
rm -rf venv    # Mac/Linux
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## Development Workflow

### When You Make Changes:

**Backend Changes** (Python files):
- Code automatically reloads (due to `--reload` flag)
- Check terminal for errors
- Test with http://localhost:8000/docs

**Frontend Changes** (JavaScript/React files):
- Code automatically reloads in browser
- Check browser console for errors
- Check terminal for build warnings

---

## Production Deployment

For production, you would:

1. **Build Frontend**:
   ```bash
   cd frontend
   npm run build  # Creates optimized build
   ```

2. **Deploy Backend** (with Docker/Heroku/AWS)

3. **Serve Frontend** from production server

---

## Quick Command Reference

```bash
# Backend Commands
cd backend
python -m venv venv                    # Create venv
venv\Scripts\activate                  # Activate (Windows)
source venv/bin/activate               # Activate (Mac/Linux)
pip install -r requirements.txt        # Install deps
python -m uvicorn app:app --reload     # Run server

# Frontend Commands  
cd frontend
npm install                            # Install deps
npm start                              # Run dev server
npm run build                          # Build for production
npm test                               # Run tests
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│         Browser (Port 3000)             │
│  ┌─────────────────────────────────┐   │
│  │   React Frontend Application    │   │
│  │  - Code Editor                  │   │
│  │  - Language Selection           │   │
│  │  - Results Display              │   │
│  └─────────────────────────────────┘   │
│              │                         │
│              │ HTTP Requests           │
│              │ (localhost:8000/api)    │
│              ▼                         │
└─────────────────────────────────────────┘
                 │
                 │
┌────────────────▼────────────────────────┐
│    Backend API Server (Port 8000)       │
│  ┌─────────────────────────────────┐   │
│  │    FastAPI Application          │   │
│  │  - analyze-multilang endpoint   │   │
│  │  - analyze endpoint             │   │
│  │  - Multi-language detection     │   │
│  │  - Bug detection engine         │   │
│  │  - ML models                    │   │
│  └─────────────────────────────────┘   │
│              │                         │
│              ▼                         │
│  ┌─────────────────────────────────┐   │
│  │   Machine Learning Models       │   │
│  │  - Baseline Model               │   │
│  │  - Improved Model (CodeBERT)    │   │
│  │  - Feature Extractors           │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

---

## Next Steps

1. ✅ Start Backend Server (Terminal 1)
2. ✅ Start Frontend Server (Terminal 2)
3. ✅ Open http://localhost:3000 in browser
4. ✅ Submit code for analysis
5. ✅ View results from ML models

---

**Last Updated**: January 24, 2026
**Status**: Ready for development 🎉
