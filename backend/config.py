import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8000))
    DEBUG = os.getenv('DEBUG', False)
    
    # Model paths
    BASELINE_MODEL_PATH = os.getenv('BASELINE_MODEL_PATH', 'models/baseline_model.pkl')
    IMPROVED_MODEL_PATH = os.getenv('IMPROVED_MODEL_PATH', 'models/improved_model.pkl')
    BASELINE_SCALER_PATH = os.getenv('BASELINE_SCALER_PATH', 'models/baseline_scaler.pkl')
    IMPROVED_SCALER_PATH = os.getenv('IMPROVED_SCALER_PATH', 'models/improved_scaler.pkl')
    
    # Feature extraction settings
    BASELINE_FEATURE_DIM = 10
    IMPROVED_FEATURE_DIM = 15
    CODEBERT_EMBEDDING_DIM = 768
    
    # Model training settings
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    BASELINE_N_ESTIMATORS = 100
    IMPROVED_N_ESTIMATORS = 150
    IMPROVED_MAX_DEPTH = 15
    
    # Prediction confidence thresholds
    MIN_CONFIDENCE = 0.5
    HIGH_CONFIDENCE = 0.8
    
    # Data paths
    DATASET_PATH = os.getenv('DATASET_PATH', 'data/dataset.csv')
    TRAIN_DATA_PATH = os.getenv('TRAIN_DATA_PATH', 'data/train.csv')
    TEST_DATA_PATH = os.getenv('TEST_DATA_PATH', 'data/test.csv')
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # CORS settings
    CORS_ORIGINS = ['*']
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ['*']
    CORS_ALLOW_HEADERS = ['*']

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATASET_PATH = 'data/test_dataset.csv'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

# Select configuration based on environment
environment = os.getenv('ENVIRONMENT', 'development')

if environment == 'production':
    config = ProductionConfig()
elif environment == 'testing':
    config = TestingConfig()
else:
    config = DevelopmentConfig()
