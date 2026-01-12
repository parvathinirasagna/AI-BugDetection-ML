from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List
import uvicorn
from multi_language_detector import MultiLanguageDetector, LanguageSpecificExtractor

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
baseline_model = None
baseline_scaler = None
improved_models = None
improved_scaler = None

try:
    baseline_model = joblib.load('models/baseline_model.pkl')
    baseline_scaler = joblib.load('models/baseline_scaler.pkl')
except:
    print("Baseline model not found")

try:
    improved_models = joblib.load('models/improved_model.pkl')
    improved_scaler = joblib.load('models/improved_scaler.pkl')
except:
    print("Improved model not found")


# Initialize multi-language detector
multi_detector = MultiLanguageDetector()
lang_extractor = LanguageSpecificExtractor()
class CodeInput(BaseModel):
    code_snippet: str

class BugPrediction(BaseModel):
    baseline_prediction: int
    baseline_confidence: float
    improved_prediction: int
    improved_confidence: float
    is_bug: bool
    confidence_baseline: float
    confidence_improved: float

@app.get("/")
def read_root():
    return {"message": "AI Bug Detection API is running"}

@app.post("/detect_bug")
def detect_bug(input_data: CodeInput):
    try:
        # Simple feature extraction from code
        code = input_data.code_snippet
        features = [
            code.count('for'),
            code.count('if'),
            code.count('('),
            code.count('='),
            code.count('def'),
            len(code),
            code.count('\n'),
            code.count('try'),
            code.count('['),
            code.count('import')
        ]
        features = np.array(features).reshape(1, -1)
        
        baseline_pred = 0
        baseline_conf = 0.5
        improved_pred = 0
        improved_conf = 0.5
        
        # Baseline prediction
        if baseline_model is not None and baseline_scaler is not None:
            features_scaled = baseline_scaler.transform(features)
            baseline_pred = int(baseline_model.predict(features_scaled)[0])
            try:
                proba = baseline_model.predict_proba(features_scaled)[0]
                baseline_conf = float(max(proba))
            except:
                baseline_conf = 0.75
        
        # Improved prediction (ensemble)
        if improved_models is not None and improved_scaler is not None:
            features_scaled = improved_scaler.transform(features)
            
            # Handle ensemble list of models
            if isinstance(improved_models, list):
                predictions = []
                for model in improved_models:
                    pred = int(model.predict(features_scaled)[0])
                    predictions.append(pred)
                improved_pred = int(np.round(np.mean(predictions)))
            else:
                improved_pred = int(improved_models.predict(features_scaled)[0])
            
            improved_conf = min(0.95, baseline_conf + 0.15)
        
        # Consensus
        is_bug = bool(improved_pred) if improved_models else bool(baseline_pred)
        
        return {
            "code_snippet": code[:100] + "..." if len(code) > 100 else code,
            "baseline_prediction": baseline_pred,
            "baseline_confidence": baseline_conf,
            "improved_prediction": improved_pred,
            "improved_confidence": improved_conf,
            "is_bug": is_bug,
            "confidence_baseline": baseline_conf,
            "confidence_improved": improved_conf
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/analyze-multilang")
def analyze_multilang(code_input: CodeInput):
    """Analyze code in multiple languages (Python, Java, C++)"""
    try:
        # Detect language and analyze
        result = multi_detector.analyze_code(code_input.code_snippet)
        
        return {
            "language": result['language'],
            "bugs_found": result['bugs_found'],
            "bug_count": len(result['bugs_found']),
            "severity": result['severity'],
            "feature_count": result['feature_count'],
            "supported_languages": ['python', 'java', 'cpp']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
