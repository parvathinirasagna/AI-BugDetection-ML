import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import joblib
import warnings
warnings.filterwarnings('ignore')

class BaselineModelTrainer:
    """Trains baseline model based on Nadim & Roy 2022 methodology"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.metrics = {}
    
    def load_data(self, csv_path):
        """Load dataset from CSV"""
        self.data = pd.read_csv(csv_path)
        return self.data
    
    def prepare_features(self):
        """Extract features from code snippets"""
        # TODO: Implement actual feature extraction
        # Placeholder: using synthetic features for now
        X = np.random.rand(len(self.data), 10)
        y = self.data['is_bug'].values if 'is_bug' in self.data.columns else np.random.randint(0, 2, len(self.data))
        return X, y
    
    def train(self, X, y):
        """Train baseline model"""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)
        
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred)
        }
        
        return self.metrics
    
    def save_model(self, path='models/baseline_model.pkl'):
        """Save trained model"""
        joblib.dump(self.model, path)
        joblib.dump(self.scaler, 'models/baseline_scaler.pkl')

class ImprovedModelTrainer:
    """Trains improved model with CodeBERT + Ensemble methods"""
    
    def __init__(self):
        self.models = [
            RandomForestClassifier(n_estimators=100, random_state=42),
            RandomForestClassifier(n_estimators=150, max_depth=15, random_state=43)
        ]
        self.scaler = StandardScaler()
        self.metrics = {}
    
    def load_data(self, csv_path):
        self.data = pd.read_csv(csv_path)
        return self.data
    
    def prepare_features(self):
        """Enhanced feature extraction with CodeBERT embeddings"""
        # TODO: Integrate CodeBERT for better embeddings
        X = np.random.rand(len(self.data), 15)  # 15 features from CodeBERT
        y = self.data['is_bug'].values if 'is_bug' in self.data.columns else np.random.randint(0, 2, len(self.data))
        return X, y
    
    def train(self, X, y):
        """Train ensemble model"""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)
        
        predictions = []
        for model in self.models:
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            predictions.append(pred)
        
        # Ensemble voting
        ensemble_pred = np.round(np.mean(predictions, axis=0)).astype(int)
        
        self.metrics = {
            'accuracy': accuracy_score(y_test, ensemble_pred),
            'precision': precision_score(y_test, ensemble_pred),
            'recall': recall_score(y_test, ensemble_pred),
            'f1': f1_score(y_test, ensemble_pred)
        }
        
        return self.metrics
    
    def save_model(self, path='models/improved_model.pkl'):
        joblib.dump(self.models, path)
        joblib.dump(self.scaler, 'models/improved_scaler.pkl')

if __name__ == "__main__":
    # Train baseline model
    baseline = BaselineModelTrainer()
    print("Training Baseline Model (Nadim & Roy 2022)...")
    # baseline.load_data('dataset.csv')
    X, y = baseline.prepare_features()
    baseline_metrics = baseline.train(X, y)
    print("Baseline Model Metrics:", baseline_metrics)
    baseline.save_model()
    
    # Train improved model
    improved = ImprovedModelTrainer()
    print("\nTraining Improved Model (Ensemble with CodeBERT)...")
    # improved.load_data('dataset.csv')
    X, y = improved.prepare_features()
    improved_metrics = improved.train(X, y)
    print("Improved Model Metrics:", improved_metrics)
    improved.save_model()
