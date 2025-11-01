# main_simple.py - Simplified version without FastAPI dependency issues
import json
import sys
import os
from typing import Dict, Any

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from config import settings
from model_loader import ModelLoader
from unified_analyzer import UnifiedAnalyzer

class SimpleBreastCancerAPI:
    """Simple API without FastAPI dependencies"""
    
    def __init__(self):
        self.model_loader = None
        self.analyzer = None
        self.initialize()
    
    def initialize(self):
        """Initialize models"""
        try:
            print("🚀 Initializing Breast Cancer AI System...")
            self.model_loader = ModelLoader(settings)
            self.analyzer = UnifiedAnalyzer(self.model_loader)
            print("✅ System initialized successfully!")
        except Exception as e:
            print(f"❌ Initialization error: {e}")
    
    def health_check(self) -> Dict[str, Any]:
        """Health check endpoint"""
        if not self.model_loader:
            return {"status": "unhealthy", "error": "Models not loaded"}
        
        available_modalities = self.model_loader.get_available_modalities()
        loaded_models = self.model_loader.list_loaded_models()
        
        return {
            "status": "healthy",
            "available_modalities": available_modalities,
            "loaded_models": list(loaded_models.keys()),
            "total_models_loaded": len(loaded_models)
        }
    
    def comprehensive_analysis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive analysis endpoint"""
        if not self.analyzer:
            return {"error": "Analyzer not ready"}
        
        try:
            results = self.analyzer.comprehensive_analysis(patient_data)
            return results
        except Exception as e:
            return {"error": f"Analysis error: {str(e)}"}
    
    def genomics_analysis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Genomics-only analysis"""
        if not self.analyzer:
            return {"error": "Analyzer not ready"}
        
        try:
            results = self.analyzer.genomics_analysis(patient_data)
            return {"modality": "genomics", "results": results}
        except Exception as e:
            return {"error": f"Genomics analysis error: {str(e)}"}
    
    def imaging_analysis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Imaging-only analysis"""
        if not self.analyzer:
            return {"error": "Analyzer not ready"}
        
        try:
            results = self.analyzer.imaging_analysis(patient_data)
            return {"modality": "imaging", "results": results}
        except Exception as e:
            return {"error": f"Imaging analysis error: {str(e)}"}
    
    def nlp_analysis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clinical text NLP analysis"""
        if not self.analyzer:
            return {"error": "Analyzer not ready"}
        
        try:
            results = self.analyzer.nlp_analysis(patient_data)
            return {"modality": "clinical_nlp", "results": results}
        except Exception as e:
            return {"error": f"NLP analysis error: {str(e)}"}

def test_api():
    """Test the simple API"""
    print("🧪 Testing Simple Breast Cancer API")
    print("=" * 40)
    
    # Initialize API
    api = SimpleBreastCancerAPI()
    
    # Test health check
    health = api.health_check()
    print(f"🏥 Health Check: {health['status']}")
    print(f"📊 Available Modalities: {health.get('available_modalities', [])}")
    
    # Test with sample patient data
    sample_patient = {
        'patient_id': 'SIMPLE_TEST_001',
        'age': 45,
        'tumor_size': 2.8,
        'tumor_mutational_burden': 12.5,
        'genomic_alterations': [
            {'gene': 'BRCA1', 'mutation': 'Pathogenic', 'allele_frequency': 0.8},
            {'gene': 'TP53', 'mutation': 'Likely_pathogenic', 'allele_frequency': 0.6}
        ],
        'biomarkers': {
            'ER_status': 'Positive',
            'PR_status': 'Positive',
            'HER2_status': 'Negative',
            'BRCA_status': 'Positive'
        },
        'ultrasound_findings': {
            'mass_present': 1,
            'mass_size': 2.8,
            'mass_shape_irregular': 1,
            'mass_margins': 1,
            'echo_pattern': 1,
            'calcifications': 0,
            'birads_score': 4
        },
        'clinical_notes': [
            {'text': 'Patient presents with palpable breast mass, family history of breast cancer', 'note_type': 'clinical_note'}
        ]
    }
    
    print(f"\n🔍 Testing Comprehensive Analysis...")
    comprehensive_result = api.comprehensive_analysis(sample_patient)
    
    if 'error' not in comprehensive_result:
        print(f"✅ Patient ID: {comprehensive_result.get('patient_id')}")
        print(f"📈 Overall Risk: {comprehensive_result.get('overall_risk_assessment', {}).get('overall_risk', 'N/A')}")
        print(f"🎯 Modalities Used: {comprehensive_result.get('modalities_used', [])}")
        print(f"💊 Treatment Recommendations: {len(comprehensive_result.get('treatment_recommendations', []))}")
    else:
        print(f"❌ Error: {comprehensive_result['error']}")
    
    # Test individual analyses
    print(f"\n🧬 Testing Genomics Analysis...")
    genomics_result = api.genomics_analysis(sample_patient)
    if 'error' not in genomics_result:
        print(f"✅ Genomics Status: {genomics_result['results'].get('status', 'completed')}")
    else:
        print(f"❌ Genomics Error: {genomics_result['error']}")
    
    print(f"\n🔬 Testing Imaging Analysis...")
    imaging_result = api.imaging_analysis(sample_patient)
    if 'error' not in imaging_result:
        print(f"✅ Imaging Status: {imaging_result['results'].get('status', 'completed')}")
    else:
        print(f"❌ Imaging Error: {imaging_result['error']}")
    
    print(f"\n📝 Testing NLP Analysis...")
    nlp_result = api.nlp_analysis(sample_patient)
    if 'error' not in nlp_result:
        print(f"✅ NLP Status: {nlp_result['results'].get('status', 'completed')}")
    else:
        print(f"❌ NLP Error: {nlp_result['error']}")
    
    print(f"\n🎉 Simple API Test Complete!")
    return api

if __name__ == "__main__":
    api = test_api()
    
    print(f"\n{'='*50}")
    print("🚀 Simple Breast Cancer AI API Ready!")
    print("📋 Available Methods:")
    print("  - api.health_check()")
    print("  - api.comprehensive_analysis(patient_data)")
    print("  - api.genomics_analysis(patient_data)")
    print("  - api.imaging_analysis(patient_data)")
    print("  - api.nlp_analysis(patient_data)")
    print("="*50)