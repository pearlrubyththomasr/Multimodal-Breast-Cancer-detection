#!/usr/bin/env python3
"""
Complete NLP test to verify the full pipeline is working
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from config import settings
from model_loader import ModelLoader
from unified_analyzer import UnifiedAnalyzer

def test_nlp_pipeline():
    """Test the complete NLP analysis pipeline"""
    
    print("🧪 Testing Complete NLP Pipeline")
    print("=" * 50)
    
    # Initialize components
    print("1. Loading models...")
    loader = ModelLoader(settings)
    analyzer = UnifiedAnalyzer(loader)
    
    print(f"   Available modalities: {analyzer.available_modalities}")
    
    # Test data with various clinical scenarios
    test_cases = [
        {
            'name': 'High Risk Case',
            'data': {
                'patient_id': 'TEST_HIGH_RISK',
                'clinical_notes': [
                    {
                        'text': 'Patient presents with a highly suspicious mass in the left breast. Mammography shows irregular calcifications with architectural distortion. BI-RADS 5 lesion identified. Urgent biopsy recommended. Family history of BRCA1 mutation.',
                        'note_type': 'radiology'
                    },
                    {
                        'text': 'Physical examination reveals a hard, irregular mass with skin dimpling. Patient reports rapid growth over 2 months. Nipple retraction noted. Lymphadenopathy present.',
                        'note_type': 'clinical'
                    }
                ]
            }
        },
        {
            'name': 'Moderate Risk Case',
            'data': {
                'patient_id': 'TEST_MODERATE_RISK',
                'clinical_notes': [
                    {
                        'text': 'Suspicious lesion detected on routine screening. BI-RADS 4 classification. Biopsy recommended for further evaluation. No family history of breast cancer.',
                        'note_type': 'radiology'
                    }
                ]
            }
        },
        {
            'name': 'Low Risk Case',
            'data': {
                'patient_id': 'TEST_LOW_RISK',
                'clinical_notes': [
                    {
                        'text': 'Routine annual screening mammography. No significant abnormalities detected. BI-RADS 2 - benign findings. Continue routine screening.',
                        'note_type': 'radiology'
                    }
                ]
            }
        }
    ]
    
    # Test each case
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test_case['name']}")
        print("-" * 30)
        
        # Run NLP analysis
        result = analyzer.nlp_analysis(test_case['data'])
        
        print(f"   Status: {result.get('status')}")
        print(f"   Risk Score: {result.get('risk_score', 'N/A')}")
        print(f"   Risk Category: {result.get('risk_category', 'N/A')}")
        print(f"   AI Confidence: {result.get('ai_confidence', 'N/A')}")
        print(f"   Notes Processed: {result.get('notes_processed', 'N/A')}")
        
        if 'clinical_indicators' in result:
            indicators = result['clinical_indicators']
            print(f"   Symptoms: {indicators.get('symptoms', [])}")
            print(f"   Findings: {indicators.get('findings', [])}")
        
        if 'key_findings' in result:
            print(f"   Key Findings: {result['key_findings']}")
        
        # Test comprehensive analysis
        print(f"\n   Running comprehensive analysis...")
        comp_result = analyzer.comprehensive_analysis(test_case['data'])
        
        if 'nlp' in comp_result.get('modality_results', {}):
            nlp_result = comp_result['modality_results']['nlp']
            print(f"   Comprehensive NLP Status: {nlp_result.get('status')}")
            print(f"   Comprehensive Risk Score: {nlp_result.get('risk_score')}")
        else:
            print("   ❌ NLP not included in comprehensive analysis")
    
    print("\n" + "=" * 50)
    print("✅ NLP Pipeline Test Complete!")

if __name__ == "__main__":
    test_nlp_pipeline()