# 🚀 Complete Setup & Installation Guide

## Quick Start (5 Minutes)

### Windows Users

```bash
# 1. Clone repository
git clone https://github.com/parvathinirasagna/AI-BugDetection-ML.git
cd AI-BugDetection-ML

# 2. Setup backend
cd backend
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt

# 3. Setup frontend (Open new terminal)
cd ..\\frontend
npm install

# 4. Run backend (Terminal 1)
cd ..\\backend
python -m app.main

# 5. Run frontend (Terminal 2)  
cd frontend
npm start

# 6. Open browser
# http://localhost:3000
```

### Linux/macOS Users

```bash
# 1. Clone
git clone https://github.com/parvathinirasagna/AI-BugDetection-ML.git
cd AI-BugDetection-ML

# 2. Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Setup frontend (New terminal)
cd ../frontend
npm install

# 4. Run backend (Terminal 1)
cd ../backend
python -m app.main

# 5. Run frontend (Terminal 2)
cd ../frontend
npm start

# Open: http://localhost:3000
```

---

## System Requirements

- Python 3.9 or higher
- Node.js 16 or higher  
- Git
- 4GB RAM minimum
- Windows/macOS/Linux

---

## File Structure Setup

The project will auto-create these directories:

```
AI-BugDetection-ML/
├── backend/
│   ├── app/              (FastAPI app)
│   ├── ml_models/        (ML models)
│   ├── saved_models/     (Auto-created)
│   ├── data/
│   ├── venv/             (Created by pip)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   ├── node_modules/     (Created by npm)
│   └── package.json
└── README.md
```

---

## Troubleshooting

### "pip: command not found"
- Use `pip3` or `python -m pip`

### Port 8000 already in use
- Change in backend/app/main.py: `uvicorn.run(..., port=8001)`

### Port 3000 already in use
- Set environment: `PORT=3001 npm start`

### Module not found errors
- Ensure venv is activated
- Run: `pip install -r requirements.txt` again

### npm errors
- Delete node_modules: `rm -rf node_modules`
- Run: `npm install` again

---

## API Testing

```bash
# After backend is running

# Baseline prediction
curl -X POST http://localhost:8000/api/predict/baseline \
  -H "Content-Type: application/json" \
  -d '{"code_content": "def test(): return 1+1"}'

# Get metrics
curl http://localhost:8000/api/metrics
```

---

## Next Steps

1. See README.md for detailed documentation
2. Check API docs at http://localhost:8000/api/docs
3. Review model comparison in frontend dashboard
