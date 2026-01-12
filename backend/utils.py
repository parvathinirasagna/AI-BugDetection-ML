import logging
import json
from datetime import datetime
from typing import Dict, Any
import os

class Logger:
    """Custom logging utility"""
    
    def __init__(self, name: str, log_file: str = None):
        self.logger = logging.getLogger(name)
        
        if log_file is None:
            log_file = f'logs/{name}.log'
        
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def debug(self, message: str):
        self.logger.debug(message)

class MetricsTracker:
    """Track model performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'baseline_accuracy': 0.0,
            'baseline_precision': 0.0,
            'baseline_recall': 0.0,
            'baseline_f1': 0.0,
            'improved_accuracy': 0.0,
            'improved_precision': 0.0,
            'improved_recall': 0.0,
            'improved_f1': 0.0,
            'total_predictions': 0,
            'correct_predictions': 0
        }
    
    def update_metrics(self, metrics: Dict[str, float]):
        self.metrics.update(metrics)
    
    def get_metrics(self) -> Dict[str, float]:
        return self.metrics
    
    def reset_metrics(self):
        for key in self.metrics:
            self.metrics[key] = 0.0

class DataValidator:
    """Validate input data"""
    
    @staticmethod
    def validate_code_snippet(code: str) -> bool:
        """Validate code snippet input"""
        if not isinstance(code, str):
            return False
        if len(code) < 10 or len(code) > 10000:
            return False
        return True
    
    @staticmethod
    def validate_request(request_data: Dict[str, Any]) -> bool:
        """Validate API request"""
        if 'code_snippet' not in request_data:
            return False
        return DataValidator.validate_code_snippet(request_data['code_snippet'])

class ResponseFormatter:
    """Format API responses"""
    
    @staticmethod
    def success_response(data: Dict[str, Any], message: str = "Success") -> Dict:
        return {
            'status': 'success',
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def error_response(error: str, code: int = 400) -> Dict:
        return {
            'status': 'error',
            'error': error,
            'code': code,
            'timestamp': datetime.now().isoformat()
        }

def get_timestamp() -> str:
    """Get current timestamp"""
    return datetime.now().isoformat()

def calculate_accuracy_improvement(baseline_acc: float, improved_acc: float) -> float:
    """Calculate accuracy improvement percentage"""
    if baseline_acc == 0:
        return 0.0
    return ((improved_acc - baseline_acc) / baseline_acc) * 100

def format_prediction_result(result: Dict) -> Dict:
    """Format prediction result for API response"""
    return {
        'code_snippet': result.get('code_snippet', ''),
        'is_bug': result.get('consensus', False),
        'baseline_model': {
            'prediction': result.get('baseline_detection', False),
            'confidence': round(result.get('confidence_baseline', 0.0), 4)
        },
        'improved_model': {
            'prediction': result.get('improved_detection', False),
            'confidence': round(result.get('confidence_improved', 0.0), 4)
        },
        'recommendations': result.get('recommendations', [])
    }
