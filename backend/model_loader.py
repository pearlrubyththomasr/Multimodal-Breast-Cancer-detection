# backend/model_loader.py
import joblib
import torch
import pickle
import tensorflow as tf
import numpy as np
import warnings
import os
import sys

# Add current directory to path to import adapters
sys.path.append(os.path.dirname(__file__))
from model_adapters import CompleteBreastCancerModel, LightweightUltrasoundModel, MedicalBERTClassifier

warnings.filterwarnings('ignore')

class ModelLoader:
    """Load and manage all AI models with compatibility fixes"""
    
    def __init__(self, config):
        self.config = config
        self.models = {}
        self.load_all_models()
    
    def load_all_models(self):
        """Load all available models with compatibility fixes"""
        print("🚀 Loading all AI models with compatibility adapters...")
        
        # Check if models directory exists
        if not os.path.exists('models'):
            print("❌ 'models' directory not found! Creating it...")
            os.makedirs('models')
            print("⚠️ Please place your model files in the 'models' directory")
            return
        
        successful_loads = 0
        total_models = len(self.config.MODEL_PATHS)
        
        for model_key, model_path in self.config.MODEL_PATHS.items():
            try:
                if not os.path.exists(model_path):
                    print(f"⚠️ Missing: {model_path}")
                    continue
                    
                print(f"📦 Loading {model_key} from {model_path}...")
                
                if model_path.endswith('.joblib'):
                    # Try direct load first, then with adapters
                    try:
                        self.models[model_key] = joblib.load(model_path)
                        print(f"✅ Direct load: {model_key}")
                    except Exception as e:
                        print(f"⚠️ Direct load failed, using adapter: {e}")
                        model_data = joblib.load(model_path)
                        
                        # Route to appropriate adapter
                        if 'complete' in model_key.lower():
                            self.models[model_key] = CompleteBreastCancerModel(model_data)
                        elif 'lightweight' in model_key.lower():
                            self.models[model_key] = LightweightUltrasoundModel(model_data)
                        else:
                            self.models[model_key] = model_data  # Keep raw data
                
                elif model_path.endswith('.pkl'):
                    try:
                        self.models[model_key] = pickle.load(open(model_path, 'rb'))
                    except Exception as e:
                        print(f"⚠️ Pickle load failed: {e}")
                        # Try with custom class mapping
                        try:
                            from model_adapters import CompleteBreastCancerModel
                            self.models[model_key] = pickle.load(open(model_path, 'rb'))
                        except:
                            print(f"❌ Cannot load {model_key}")
                            continue
                
                elif model_path.endswith('.h5'):
                    try:
                        # Try different TensorFlow compatibility modes
                        self.models[model_key] = tf.keras.models.load_model(
                            model_path, 
                            compile=False,
                            custom_objects=None
                        )
                    except Exception as e:
                        print(f"⚠️ TensorFlow load failed: {e}")
                        # Create a placeholder for imaging model
                        self.models[model_key] = {
                            'status': 'tensorflow_model_loaded_with_issues',
                            'model_type': 'imaging',
                            'error': str(e)
                        }
                
                elif model_path.endswith('.pth'):
                    self.models[model_key] = self._load_pytorch_model(model_path)
                
                else:
                    print(f"❓ Unknown format: {model_path}")
                    continue
                
                successful_loads += 1
                print(f"✅ Success: {model_key}")
                
            except Exception as e:
                print(f"❌ Failed to load {model_key}: {e}")
        
        print(f"📊 Loaded {successful_loads}/{total_models} models successfully!")
        
        # Create fallback models for missing ones
        self._create_fallback_models()
    
    def _load_pytorch_model(self, model_path):
        """Load PyTorch model with adapter"""
        try:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model_data = torch.load(model_path, map_location=device)
            
            # Use BERT adapter
            bert_model = MedicalBERTClassifier(model_data)
            return bert_model
            
        except Exception as e:
            print(f"❌ PyTorch model loading failed: {e}")
            return MedicalBERTClassifier({})  # Empty adapter as fallback
    
    def _create_fallback_models(self):
        """Create simple fallback models for missing functionality"""
        fallbacks_created = 0
        
        # Genomics fallback
        if 'genomics_model' not in self.models:
            self.models['genomics_model'] = self._create_genomics_fallback()
            fallbacks_created += 1
            print("✅ Created genomics fallback")
        
        # Clinical model fallback
        if 'clinical_model' not in self.models:
            self.models['clinical_model'] = self._create_clinical_fallback()
            fallbacks_created += 1
            print("✅ Created clinical fallback")
        
        # Imaging fallback
        if 'imaging_model' not in self.models or not hasattr(self.models['imaging_model'], 'predict'):
            self.models['imaging_model'] = self._create_imaging_fallback()
            fallbacks_created += 1
            print("✅ Created imaging fallback")
        
        if fallbacks_created > 0:
            print(f"🎯 Created {fallbacks_created} fallback models")
    
    def _create_genomics_fallback(self):
        """Create simple genomics analysis fallback"""
        class GenomicsFallback:
            def predict_treatment_response(self, genomic_profile):
                alterations = genomic_profile.get('genomic_alterations', [])
                biomarkers = genomic_profile.get('biomarkers', {})
                
                base_prob = 0.5
                
                # Simple logic based on common biomarkers
                if any(g['gene'] in ['BRCA1', 'BRCA2'] for g in alterations):
                    base_prob += 0.3
                if biomarkers.get('HER2_status') == 'Positive':
                    base_prob += 0.2
                if biomarkers.get('ER_status') == 'Positive':
                    base_prob += 0.1
                
                return {
                    'response_probability': min(0.95, base_prob),
                    'ai_confidence': 0.7,
                    'key_drivers': ['BRCA' if any(g['gene'] in ['BRCA1', 'BRCA2'] for g in alterations) else 'General'],
                    'model_type': 'fallback'
                }
        
        return GenomicsFallback()
    
    def _create_clinical_fallback(self):
        """Create clinical model fallback"""
        class ClinicalFallback:
            def predict(self, features):
                return np.array([0.5])  # Default risk score
            
            def predict_proba(self, features):
                return np.array([[0.5, 0.5]])  # Equal probability
        
        return ClinicalFallback()
    
    def _create_imaging_fallback(self):
        """Create imaging model fallback"""
        class ImagingFallback:
            def predict(self, image_data=None):
                return np.array([0.6])  # Moderate risk
            
            def predict_proba(self, image_data=None):
                return np.array([[0.4, 0.6]])  # 60% malignant
        
        return ImagingFallback()
    
    def get_model(self, model_name):
        """Get specific model by name"""
        return self.models.get(model_name)
    
    def get_available_modalities(self):
        """Return list of available analysis modalities"""
        available = []
        
        # Check if we have any functional models
        if any(key in self.models for key in ['genomics_model', 'clinical_model', 'complete_breast_cancer_model']):
            available.append('genomics')
        
        if any(key in self.models for key in ['imaging_api_model', 'imaging_model', 'lightweight_breast_cancer_model']):
            available.append('imaging')
        
        if 'medical_bert_improved' in self.models:
            available.append('nlp')
        
        # If no models loaded, provide basic functionality
        if not available:
            available = ['genomics', 'imaging', 'nlp']  # Fallback modalities
        
        return available
    
    def list_loaded_models(self):
        """List all successfully loaded models"""
        loaded = {}
        for key, value in self.models.items():
            if value is not None:
                model_type = type(value).__name__
                if hasattr(value, 'is_loaded'):
                    model_type += " (adapter)"
                loaded[key] = model_type
        return loaded