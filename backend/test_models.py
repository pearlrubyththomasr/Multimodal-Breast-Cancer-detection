# backend/test_models.py
from model_loader import ModelLoader
from config import settings

def test_model_loading():
    print("🧪 Testing model loading with adapters...")
    
    loader = ModelLoader(settings)
    
    print("\n📋 Loaded Models:")
    for model_name, model_type in loader.list_loaded_models().items():
        print(f"  {model_name}: {model_type}")
    
    print(f"\n🎯 Available Modalities: {loader.get_available_modalities()}")
    
    # Test basic functionality
    if 'genomics' in loader.get_available_modalities():
        genomics_model = loader.get_model('genomics_model')
        test_data = {
            'genomic_alterations': [{'gene': 'BRCA1', 'mutation': 'Pathogenic'}],
            'biomarkers': {'HER2_status': 'Positive'}
        }
        result = genomics_model.predict_treatment_response(test_data)
        print(f"\n🧬 Genomics Test: {result}")

if __name__ == "__main__":
    test_model_loading()