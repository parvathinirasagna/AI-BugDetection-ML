from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List
import uvicorn

app = FastAPI(title="AI Bug Detection API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained models
try:
    baseline_model = joblib.load('models/baseline_model.pkl')
    improved_model = joblib.load('models/improved_model.pkl')
except:
    baseline_model = None
    improved_model = None

class CodeInput(BaseModel):
    code_snippet: str

class BugPrediction(BaseModel):
    baseline_prediction: int
    baseline_confidence: float
    improved_prediction: int
    improved_confidence: float
    is_bug: bool

@app.get("/")
def read_root():
    return {"message": "AI Bug Detection API is running"}

@app.post("/detect_bug", response_model=BugPrediction)
def detect_bug(input_data: CodeInput):
    if baseline_model is None or improved_model is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    # TODO: Implement feature extraction
    # For now, using placeholder prediction
    baseline_pred = baseline_model.predict([np.zeros(10)])[0]
    improved_pred = improved_model.predict([np.zeros(10)])[0]
    
    return BugPrediction(
        baseline_prediction=int(baseline_pred),
        baseline_confidence=0.85,
        improved_prediction=int(improved_pred),
        improved_confidence=0.92,
        is_bug=bool(improved_pred)
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
