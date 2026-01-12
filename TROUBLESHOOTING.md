# 🐛 Troubleshooting Guide - AI-Powered Bug Detection ML

## Common Errors & Solutions

### 1. **ImportError: cannot import name 'LanguageSpecificExtractor'**

**Error Message:**
```
ImportError: cannot import name 'LanguageSpecificExtractor' from 'multi_language_detector'
```

**Root Cause:**
The import statement in `app.py` was incorrect. `LanguageSpecificExtractor` is defined in `feature_extractor.py`, not `multi_language_detector.py`.

**Solution:**
Update the import statements in `app.py`:

```python
# ❌ WRONG:
from multi_language_detector import MultiLanguageDetector, LanguageSpecificExtractor

# ✅ CORRECT:
from multi_language_detector import MultiLanguageDetector
from feature_extractor import LanguageSpecificExtractor
```

**What to Do:**
1. Pull the latest changes from GitHub:
   ```bash
   git pull origin main
   ```
2. The issue has been fixed in the latest commit
3. Run the server again:
   ```bash
   python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

---

### 2. **ModuleNotFoundError: No module named 'multi_language_detector'**

**Error Message:**
```
ModuleNotFoundError: No module named 'multi_language_detector'
```

**Root Cause:**
You're running the app from the wrong directory. The module must be found relative to the backend directory.

**Solution:**
```bash
# ❌ WRONG - from parent directory:
cd AI-BugDetection-ML
python -m uvicorn backend.app:app

# ✅ CORRECT - from backend directory:
cd AI-BugDetection-ML/backend
python -m uvicorn app:app --reload
```

---

### 3. **ModuleNotFoundError: No module named 'venv'**

**Error Message:**
```
ModuleNotFoundError: No module named 'venv'
```

**Root Cause:**
Virtual environment was not created or activated properly.

**Solution:**
```bash
# Create a new virtual environment
cd AI-BugDetection-ML/backend
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 4. **Port 8000 is already in use**

**Error Message:**
```
OSError: [Errno 48] Address already in use
```

**Root Cause:**
Port 8000 is already being used by another application.

**Solution:**

**Option A: Use a different port**
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

**Option B: Kill the process using port 8000**

*Windows:*
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

*Mac/Linux:*
```bash
lsof -i :8000
kill -9 <PID>
```

---

### 5. **Requirements.txt not found**

**Error Message:**
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

**Root Cause:**
You're not in the `backend` directory.

**Solution:**
```bash
# Navigate to backend directory
cd backend

# Then install requirements
pip install -r requirements.txt
```

---

### 6. **fastapi not found after pip install**

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Root Cause:**
Dependencies were installed in the wrong Python environment.

**Solution:**
```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Check Python path
python --version
which python  # On Mac/Linux
where python  # On Windows

# Reinstall
pip install -r requirements.txt
```

---

## Quick Checklist Before Running

- [ ] Clone the repository: `git clone https://github.com/parvathinirasagna/AI-BugDetection-ML.git`
- [ ] Navigate to backend: `cd AI-BugDetection-ML/backend`
- [ ] Create virtual env: `python -m venv venv`
- [ ] Activate venv: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run server: `python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000`
- [ ] Check: http://localhost:8000/docs should load

---

## If Issues Persist

### Reset Everything

```bash
# Remove virtual environment
rmdir /s venv  # Windows
rm -rf venv    # Mac/Linux

# Create fresh virtual environment
python -m venv venv

# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install fresh
pip install --upgrade pip
pip install -r requirements.txt

# Run
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Check File Structure

Ensure you have these files in the `backend/` directory:
```
backend/
├── app.py                      ✓
├── bug_detector.py             ✓
├── multi_language_detector.py  ✓
├── feature_extractor.py        ✓
├── config.py
├── train_model.py
├── utils.py
├── requirements.txt            ✓
└── venv/                       ✓ (created by you)
```

### Verify Latest Code

```bash
# Pull latest changes
git pull origin main

# Check app.py imports (lines 7-8)
cat app.py | head -20
```

Should show:
```python
from multi_language_detector import MultiLanguageDetector
from feature_extractor import LanguageSpecificExtractor
```

---

## Testing the Fix

After fixing the import issue, test with:

```bash
# In a new terminal
curl -X POST "http://localhost:8000/analyze-multilang" \
  -H "Content-Type: application/json" \
  -d '{"code_snippet": "try:\n    x = 1\nexcept:\n    pass"}'
```

**Expected Response:**
```json
{
  "language": "python",
  "bugs_found": ["Bare except clause detected - specify exception type"],
  "bug_count": 1,
  "severity": "medium",
  "feature_count": 5,
  "supported_languages": ["python", "java", "cpp"]
}
```

---

## Still Having Issues?

1. **Check GitHub Issues**: https://github.com/parvathinirasagna/AI-BugDetection-ML/issues
2. **Verify Python Version**: `python --version` (Should be 3.8+)
3. **Reinstall Python**: If all else fails, reinstall Python and repeat setup
4. **Check Firewall**: Port 8000 might be blocked by firewall

---

**Last Updated**: January 12, 2026
**Fixed Issues**: Import error with LanguageSpecificExtractor resolved 🌟
