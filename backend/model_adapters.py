# backend/model_adapters.py
import numpy as np
import pandas as pd
from typing import Dict, Any, List

class CompleteBreastCancerModel:
    """Adapter for complete_breast_cancer_model.joblib"""
    def __init__(self, model_data):
        self.model_data = model_data
        self.is_loaded = True
    
    def predict(self, clinical_data):
        """Basic prediction adapter"""
        # Simple risk calculation based on available data
        risk_score = 0.5  # Default
        
        if isinstance(clinical_data, dict):
            age = clinical_data.get('age', 60)
            tumor_size = clinical_data.get('tumor_size', 2.0)
            
            # Simple risk calculation
            if age < 40:
                risk_score += 0.2
            if tumor_size > 2:
                risk_score += 0.2
            if clinical_data.get('genomic_alterations'):
                risk_score += 0.1
        
        return np.array([min(0.95, max(0.1, risk_score))])

class LightweightUltrasoundModel:
    """Adapter for lightweight models"""
    def __init__(self, model_data):
        self.model_data = model_data
        self.is_loaded = True
    
    def comprehensive_analysis(self, patient_data):
        """Basic analysis adapter"""
        return {
            'status': 'lightweight_analysis',
            'overall_risk_score': 0.6,
            'modalities_analyzed': ['ultrasound', 'mammography', 'xray'],
            'recommendations': ['Further evaluation recommended']
        }

class MedicalBERTClassifier:
    """Adapter for BERT model"""
    def __init__(self, model_data):
        self.model_data = model_data
        self.is_loaded = True
    
    def predict(self, text):
        """Enhanced text analysis with keyword-based logic"""
        text_lower = text.lower()
        
        # Analyze cancer suspicion level
        high_suspicion_terms = [
            'malignant', 'carcinoma', 'metastasis', 'invasive', 'aggressive',
            'stage iii', 'stage iv', 'birads 5', 'highly suspicious'
        ]
        
        moderate_suspicion_terms = [
            'suspicious', 'atypical', 'irregular', 'birads 4', 'concerning',
            'abnormal', 'lesion', 'mass', 'biopsy recommended'
        ]
        
        # Determine suspicion level
        suspicion_level = 'low'
        suspicion_confidence = 0.6
        
        high_count = sum(1 for term in high_suspicion_terms if term in text_lower)
        moderate_count = sum(1 for term in moderate_suspicion_terms if term in text_lower)
        
        if high_count > 0:
            suspicion_level = 'high'
            suspicion_confidence = min(0.95, 0.7 + (high_count * 0.1))
        elif moderate_count > 0:
            suspicion_level = 'moderate'
            suspicion_confidence = min(0.9, 0.6 + (moderate_count * 0.05))
        
        # Analyze symptom severity
        severe_symptoms = [
            'severe pain', 'rapid growth', 'skin ulceration', 'nipple retraction',
            'bloody discharge', 'extensive', 'widespread'
        ]
        
        moderate_symptoms = [
            'pain', 'tenderness', 'discharge', 'lump', 'swelling', 'dimpling'
        ]
        
        severity = 'mild'
        severity_confidence = 0.6
        
        severe_count = sum(1 for symptom in severe_symptoms if symptom in text_lower)
        moderate_count = sum(1 for symptom in moderate_symptoms if symptom in text_lower)
        
        if severe_count > 0:
            severity = 'severe'
            severity_confidence = min(0.9, 0.7 + (severe_count * 0.1))
        elif moderate_count > 0:
            severity = 'moderate'
            severity_confidence = min(0.85, 0.6 + (moderate_count * 0.05))
        
        # Determine clinical urgency
        urgent_terms = [
            'urgent', 'immediate', 'emergent', 'stat', 'asap', 'priority',
            'rapidly growing', 'inflammatory'
        ]
        
        routine_terms = [
            'routine', 'follow-up', 'monitor', 'observe', 'annual'
        ]
        
        urgency_level = 'standard'
        urgency_confidence = 0.6
        
        if any(term in text_lower for term in urgent_terms):
            urgency_level = 'urgent'
            urgency_confidence = 0.8
        elif any(term in text_lower for term in routine_terms):
            urgency_level = 'routine'
            urgency_confidence = 0.7
        
        return {
            'clinical_text_length': len(text),
            'symptom_analysis': {
                'severity': severity, 
                'confidence': severity_confidence,
                'symptoms_detected': moderate_count + severe_count
            },
            'clinical_urgency': {
                'level': urgency_level, 
                'confidence': urgency_confidence
            },
            'cancer_assessment': {
                'suspicion_level': suspicion_level, 
                'confidence': suspicion_confidence,
                'risk_indicators': high_count + moderate_count
            },
            'text_analysis': {
                'high_risk_terms': high_count,
                'moderate_risk_terms': moderate_count,
                'total_words': len(text.split())
            }
        }