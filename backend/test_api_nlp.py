#!/usr/bin/env python3
"""
Test the API endpoint directly with clinical notes
"""

import requests
import json

def test_api_with_clinical_notes():
    """Test the comprehensive analysis API with clinical notes"""
    
    # Test data that matches the frontend format
    test_data = {
        "patient_id": "TEST_API_NLP_001",
        "age": 45,
        "tumor_size": 2.5,
        "clinical_notes": [
            {
                "text": "Patient presents with a palpable mass in the left breast. Mammography shows suspicious calcifications. BI-RADS 4 lesion requiring biopsy.",
                "note_type": "radiology"
            },
            {
                "text": "Physical examination reveals irregular mass with skin dimpling. Patient reports breast pain and nipple discharge over the past month.",
                "note_type": "clinical"
            }
        ],
        "biomarkers": {
            "ER_status": "Positive",
            "PR_status": "Positive", 
            "HER2_status": "Negative",
            "BRCA_status": "Unknown"
        },
        "genomic_alterations": [
            {
                "gene": "BRCA1",
                "mutation": "Pathogenic",
                "allele_frequency": 0.5
            }
        ],
        "ultrasound_findings": {
            "mass_present": 1,
            "mass_size": 2.5,
            "birads_score": 4,
            "mass_shape_irregular": 1,
            "calcifications": 1
        }
    }
    
    print("🧪 Testing API with Clinical Notes")
    print("=" * 50)
    print(f"Sending data: {json.dumps(test_data, indent=2)}")
    
    try:
        # Test the comprehensive analysis endpoint
        url = "http://localhost:8000/analyze/comprehensive"
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis successful!")
            print(f"Patient ID: {result.get('patient_id')}")
            print(f"Modalities used: {result.get('modalities_used', [])}")
            
            # Check if NLP was included
            modality_results = result.get('modality_results', {})
            if 'nlp' in modality_results:
                nlp_result = modality_results['nlp']
                print(f"\n🔬 NLP Analysis Results:")
                print(f"   Status: {nlp_result.get('status')}")
                print(f"   Risk Score: {nlp_result.get('risk_score')}")
                print(f"   Risk Category: {nlp_result.get('risk_category')}")
                print(f"   AI Confidence: {nlp_result.get('ai_confidence')}")
                print(f"   Notes Processed: {nlp_result.get('notes_processed')}")
                
                if 'key_findings' in nlp_result:
                    print(f"   Key Findings: {nlp_result['key_findings']}")
            else:
                print(f"\n❌ NLP not included in results")
                print(f"Available modalities: {list(modality_results.keys())}")
            
            # Check overall risk assessment
            overall_risk = result.get('overall_risk_assessment', {})
            print(f"\n📊 Overall Assessment:")
            print(f"   Risk Category: {overall_risk.get('risk_category')}")
            print(f"   Risk Score: {overall_risk.get('overall_risk')}")
            print(f"   Confidence: {overall_risk.get('confidence')}")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the backend is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api_with_clinical_notes()