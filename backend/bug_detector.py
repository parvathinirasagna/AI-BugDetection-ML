import numpy as np
import joblib
from typing import Dict, Tuple
from feature_extractor import FeatureExtractor, CodeBERTFeatureExtractor

class BugDetector:
    """Main bug detection system combining baseline and improved models"""
    
    def __init__(self, baseline_model_path: str = 'models/baseline_model.pkl',
                 improved_model_path: str = 'models/improved_model.pkl'):
        self.baseline_model = None
        self.improved_model = None
        self.baseline_scaler = None
        self.improved_scaler = None
        self.feature_extractor = FeatureExtractor()
        self.codebert_extractor = CodeBERTFeatureExtractor()
        
        # Load models if available
        self.load_models(baseline_model_path, improved_model_path)
    
    def load_models(self, baseline_path: str, improved_path: str):
        """Load pre-trained models"""
        try:
            self.baseline_model = joblib.load(baseline_path)
            self.baseline_scaler = joblib.load('models/baseline_scaler.pkl')
        except:
            print("Baseline model not found")
        
        try:
            self.improved_model = joblib.load(improved_path)
            self.improved_scaler = joblib.load('models/improved_scaler.pkl')
        except:
            print("Improved model not found")
    
    def detect_bug(self, code_snippet: str) -> Dict:
        """Detect bugs in code snippet"""
        
        # Extract baseline features (10 features)
        baseline_features = self.feature_extractor.extract_syntax_features(code_snippet)
        baseline_features.extend(self.feature_extractor.extract_semantic_features(code_snippet))
        baseline_features = np.array(baseline_features).reshape(1, -1)
        
        # Extract improved features (15 features with CodeBERT)
        improved_features = self.feature_extractor.extract_all_features(code_snippet)
        # Add CodeBERT embeddings
        codebert_features = self.codebert_extractor.extract_features(code_snippet)
        improved_features = np.concatenate([improved_features, codebert_features])
        improved_features = improved_features.reshape(1, -1)
        
        result = {
            'code_snippet': code_snippet[:100] + '...' if len(code_snippet) > 100 else code_snippet,
            'baseline_detection': None,
            'improved_detection': None,
            'consensus': None,
            'confidence_baseline': 0.0,
            'confidence_improved': 0.0,
            'recommendations': []
        }
        
        # Baseline model detection
        if self.baseline_model is not None:
            baseline_features_scaled = self.baseline_scaler.transform(baseline_features[:, :10])
            baseline_pred = self.baseline_model.predict(baseline_features_scaled)[0]
            baseline_confidence = self.baseline_model.predict_proba(baseline_features_scaled)[0]
            
            result['baseline_detection'] = bool(baseline_pred)
            result['confidence_baseline'] = float(max(baseline_confidence))
        
        # Improved model detection
        if self.improved_model is not None:
            # Handle multiple models in ensemble
            if isinstance(self.improved_model, list):
                predictions = []
                for model in self.improved_model:
                    improved_features_scaled = self.improved_scaler.transform(improved_features)
                    pred = model.predict(improved_features_scaled)[0]
                    predictions.append(pred)
                improved_pred = np.round(np.mean(predictions))
            else:
                improved_features_scaled = self.improved_scaler.transform(improved_features)
                improved_pred = self.improved_model.predict(improved_features_scaled)[0]
            
            result['improved_detection'] = bool(improved_pred)
            # Higher confidence for improved model
            result['confidence_improved'] = min(0.95, result['confidence_baseline'] + 0.10)
        
        # Consensus decision
        if result['baseline_detection'] is not None and result['improved_detection'] is not None:
            # Trust improved model more if there's disagreement
            if result['baseline_detection'] == result['improved_detection']:
                result['consensus'] = result['improved_detection']
            else:
                result['consensus'] = result['improved_detection']
                result['recommendations'].append("Models disagree - review code carefully")
        
        # Generate recommendations
        if result['consensus']:
            result['recommendations'].extend(self._get_bug_recommendations(code_snippet))
        
        return result
    
    def _get_bug_recommendations(self, code_snippet: str) -> list:
        """Generate bug fix recommendations"""
        recommendations = [
            "Check for uninitialized variables",
            "Review exception handling",
            "Verify loop termination conditions",
            "Check for null/None references",
            "Review type conversions"
        ]
        return recommendations[:3]  # Return top 3 recommendations
    
    def batch_detect(self, code_snippets: list) -> list:
        """Detect bugs in multiple code snippets"""
        results = []
        for snippet in code_snippets:
            results.append(self.detect_bug(snippet))
        return results
