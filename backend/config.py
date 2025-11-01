# config.py
import os
from typing import Dict, Any

class Settings:
    """Application settings - UPDATED to match your model_loader keys"""
    
    # API Settings
    API_TITLE = "Multi-Modal Breast Cancer AI API"
    API_VERSION = "2.0.0"
    API_DESCRIPTION = "Comprehensive breast cancer analysis using genomics, imaging, and clinical data"
    
    # Model Paths - CORRECTED to match your model_loader.py keys
    MODEL_PATHS = {
        'genomics_model': 'models/genomics_model.joblib',
        'clinical_model': 'models/clinical_model.joblib', 
        'clinical_scaler': 'models/clinical_scaler.joblib',
        'complete_breast_cancer_model': 'models/complete_breast_cancer_model.joblib',
        'imaging_api_model': 'models/imaging_api_model.pkl',
        'imaging_model': 'models/imaging_model.h5',
        'lightweight_breast_cancer_model': 'models/lightweight_breast_cancer_model.joblib',
        'medical_bert_improved': 'models/medical_bert_improved.pth'
    }
    
    # API Settings
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    
    # CORS Settings
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]

settings = Settings()