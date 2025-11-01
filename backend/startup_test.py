#!/usr/bin/env python3
"""
Startup test for the breast cancer AI backend
Tests all components without starting the full server
"""

import sys
import os
import traceback

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except Exception as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except Exception as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import sklearn
        print("✅ Scikit-learn imported successfully")
    except Exception as e:
        print(f"❌ Scikit-learn import failed: {e}")
        return False
    
    try:
        from config import settings
        print("✅ Config imported successfully")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from schemas import PatientData, AnalysisResponse
        print("✅ Schemas imported successfully")
    except Exception as e:
        print(f"❌ Schemas import failed: {e}")
        return False
    
    try:
        from model_loader import ModelLoader
        print("✅ ModelLoader imported successfully")
    except Exception as e:
        print(f"❌ ModelLoader import failed: {e}")
        return False
    
    try:
        from unified_analyzer import UnifiedAnalyzer
        print("✅ UnifiedAnalyzer imported successfully")
    except Exception as e:
        print(f"❌ UnifiedAnalyzer import failed: {e}")
        return False
    
    return True

def test_model_loading():
    """Test model loading functionality"""
    print("\n🔧 Testing model loading...")
    
    try:
        from config import settings
        from model_loader import ModelLoader
        
        loader = ModelLoader(settings)
        available_modalities = loader.get_available_modalities()
        loaded_models = loader.list_loaded_models()
        
        print(f"✅ Available modalities: {available_modalities}")
        print(f"✅ Loaded models: {list(loaded_models.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        traceback.print_exc()
        return False

def test_analyzer():
    """Test unified analyzer functionality"""
    print("\n🧠 Testing unified analyzer...")
    
    try:
        from config import settings
        from model_loader import ModelLoader
        from unified_analyzer import UnifiedAnalyzer
        
        loader = ModelLoader(settings)
        analyzer = UnifiedAnalyzer(loader)
        
        # Test with sample data
        sample_data = {
            'patient_id': 'TEST_001',
            'age': 45,
            'tumor_size': 2.5,
            'genomic_alterations': [
                {'gene': 'BRCA1', 'mutation': 'Pathogenic', 'allele_frequency': 0.8}
            ],
            'biomarkers': {
                'ER_status': 'Positive',
                'HER2_status': 'Negative'
            }
        }
        
        # Test genomics analysis
        genomics_result = analyzer.genomics_analysis(sample_data)
        print(f"✅ Genomics analysis: {genomics_result.get('status', 'completed')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analyzer test failed: {e}")
        traceback.print_exc()
        return False

def test_fastapi_compatibility():
    """Test FastAPI compatibility without starting server"""
    print("\n🚀 Testing FastAPI compatibility...")
    
    try:
        # Test if we can import FastAPI components
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        print("✅ FastAPI imports successful")
        
        # Test if we can create app instance
        app = FastAPI(title="Test App")
        print("✅ FastAPI app creation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ FastAPI compatibility test failed: {e}")
        return False

def test_individual_models():
    """Test individual model components"""
    print("\n🔬 Testing individual models...")
    
    try:
        # Test genomics model
        from ai_genomics_model import GenomicsAnalyzer
        genomics = GenomicsAnalyzer()
        print("✅ Genomics model initialized")
        
        # Test imaging model
        from breast_cancer_imaging_analysis import ImagingAnalyzer
        imaging = ImagingAnalyzer()
        print("✅ Imaging model initialized")
        
        # Test BERT model
        from medical_bert_classifier import MedicalBERTClassifier
        bert = MedicalBERTClassifier()
        print("✅ BERT model initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Individual model test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all startup tests"""
    print("🎯 Breast Cancer AI Backend Startup Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Model Loading Test", test_model_loading),
        ("Analyzer Test", test_analyzer),
        ("FastAPI Compatibility Test", test_fastapi_compatibility),
        ("Individual Models Test", test_individual_models)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*50}")
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to start.")
        return True
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)