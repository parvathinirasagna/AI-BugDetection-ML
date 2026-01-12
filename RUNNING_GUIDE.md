# 🚀 AI-Powered Bug Detection ML - Running Guide

## Quick Start (2 Steps)

### Step 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/parvathinirasagna/AI-BugDetection-ML.git
cd AI-BugDetection-ML

# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
# From the backend directory
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

## Testing the API

### 1. Access Swagger UI
- **URL**: http://localhost:8000/docs
- This gives you an interactive API explorer

### 2. Test Endpoints

#### Test Python Code Analysis
```bash
curl -X POST "http://localhost:8000/analyze-multilang" \
  -H "Content-Type: application/json" \
  -d '{
    "code_snippet": "try:\n    x = 1\nexcept:\n    pass"
  }'
```

**Expected Response:**
```json
{
  "language": "python",
  "bugs_found": [
    "Bare except clause detected - specify exception type"
  ],
  "bug_count": 1,
  "severity": "medium",
  "feature_count": 5,
  "supported_languages": ["python", "java", "cpp"]
}
```

#### Test Java Code Analysis
```bash
curl -X POST "http://localhost:8000/analyze-multilang" \
  -H "Content-Type: application/json" \
  -d '{
    "code_snippet": "FileInputStream fis = new FileInputStream(file);"
  }'
```

#### Test C++ Code Analysis
```bash
curl -X POST "http://localhost:8000/analyze-multilang" \
  -H "Content-Type: application/json" \
  -d '{
    "code_snippet": "int* ptr = new int(10);"
  }'
```

## Frontend Setup (Optional)

### If you want to use the React frontend:

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start React development server
npm start
```

**Frontend will run on**: http://localhost:3000

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'multi_language_detector'"
**Solution**: Make sure you're in the `backend` directory when running the app

### Problem: "Port 8000 is already in use"
**Solution**: Use a different port:
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

### Problem: "requirements.txt not found"
**Solution**: Make sure you're in the correct directory:
```bash
cd backend
pip install -r requirements.txt
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|----------|
| `/analyze-multilang` | POST | Analyze code in Python, Java, or C++ |
| `/analyze` | POST | Original baseline model analysis |
| `/docs` | GET | Interactive API documentation |
| `/` | GET | API status |

## Supported Languages & Bugs Detected

### Python
- Mutable default arguments
- Bare except clauses
- Missing return statements
- Infinite loops

### Java
- Null pointer exceptions
- Unclosed resources
- Infinite loops
- Unhandled exceptions
- Missing break statements

### C++
- Memory leaks (new without delete)
- Null pointer dereferences
- Buffer overflow risks
- Uninitialized variables
- Array bounds checking

## Testing Different Code Samples

### Python - Valid Code (No Bugs)
```python
def calculate_sum(numbers):
    try:
        result = sum(numbers)
        return result
    except ValueError as e:
        print(f"Error: {e}")
```

### Java - With Bugs
```java
int[] arr = new int[5];
System.out.println(arr[i]);  // Potential array out of bounds
```

### C++ - With Bugs
```cpp
int* ptr = new int(10);
ptr = nullptr;
delete ptr;  // May cause issues
```

## File Structure

```
AI-BugDetection-ML/
├── backend/
│   ├── app.py                      # FastAPI application
│   ├── bug_detector.py             # Bug detection engine
│   ├── multi_language_detector.py  # Multi-language support
│   ├── feature_extractor.py        # Feature extraction
│   ├── requirements.txt            # Python dependencies
│   └── models/                     # Trained ML models
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── RUNNING_GUIDE.md
├── README.md
└── SETUP.md
```

## Next Steps

1. ✅ Run the backend server
2. ✅ Test with sample code snippets
3. ✅ Explore the Swagger UI at http://localhost:8000/docs
4. ✅ Train models with your own dataset (optional)
5. ✅ Deploy to production (AWS, Heroku, etc.)

## Support

For issues or questions, please create an issue on GitHub or contact the development team.

---
**Happy Bug Hunting! 🐛🔍**
