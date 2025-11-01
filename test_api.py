#!/usr/bin/env python3
"""
Automated Test Script for Breast Cancer AI Platform
Run this to test all the test cases automatically
"""

import requests
import json
import time
from typing import Dict, Any

# Test cases
TEST_CASES = {
    "high_risk_imaging": {
        "patient_id": "TEST_001_HIGH_RISK_IMAGING",
        "age": 52,
        "ultrasound_findings": {
            "mass_present": 1,
            "mass_size": 3.2,
            "mass_shape_irregular": 1,
            "mass_margins": 1,
            "echo_pattern": 1,
            "calcifications": 1,
            "birads_score": 5
        },
        "mammography_findings": {
            "mass_present": 1,
            "calcifications": 1,
            "architectural_distortion": 1,
            "asymmetry": 1,
            "skin_thickening": 0,
            "birads_score": 5,
            "breast_density": 3
        }
    },
    
    "genomics_only": {
        "patient_id": "TEST_002_GENOMICS_ONLY",
        "age": 45,
        "genomic_alterations": [
            {
                "gene": "BRCA1",
                "mutation": "Pathogenic",
                "allele_frequency": 0.85
            },
            {
                "gene": "TP53",
                "mutation": "Likely_pathogenic",
                "allele_frequency": 0.62
            }
        ],
        "biomarkers": {
            "ER_status": "Positive",
            "PR_status": "Positive",
            "HER2_status": "Negative",
            "BRCA_status": "Positive"
        }
    },
    
    "nlp_only": {
        "patient_id": "TEST_003_NLP_ONLY",
        "age": 38,
        "clinical_notes": [
            {
                "text": "Patient presents with palpable mass in left breast, family history of breast and ovarian cancer. Mother diagnosed at age 42, maternal grandmother at 55.",
                "note_type": "clinical_note"
            }
        ]
    },
    
    "multimodal_high": {
        "patient_id": "TEST_004_MULTIMODAL_HIGH",
        "age": 48,
        "tumor_size": 4.2,
        "genomic_alterations": [
            {
                "gene": "BRCA1",
                "mutation": "Pathogenic",
                "allele_frequency": 0.92
            }
        ],
        "biomarkers": {
            "ER_status": "Negative",
            "PR_status": "Negative",
            "HER2_status": "Positive",
            "BRCA_status": "Positive"
        },
        "ultrasound_findings": {
            "mass_present": 1,
            "mass_size": 4.2,
            "mass_shape_irregular": 1,
            "mass_margins": 1,
            "echo_pattern": 1,
            "calcifications": 1,
            "birads_score": 5
        },
        "clinical_notes": [
            {
                "text": "Advanced breast cancer with multiple concerning features. Strong family history and genetic predisposition.",
                "note_type": "clinical_note"
            }
        ]
    },
    
    "low_risk": {
        "patient_id": "TEST_005_LOW_RISK",
        "age": 35,
        "ultrasound_findings": {
            "mass_present": 0,
            "mass_size": 0,
            "mass_shape_irregular": 0,
            "mass_margins": 0,
            "echo_pattern": 0,
            "calcifications": 0,
            "birads_score": 2
        },
        "biomarkers": {
            "ER_status": "Positive",
            "PR_status": "Positive",
            "HER2_status": "Negative",
            "BRCA_status": "Negative"
        }
    },
    
    "empty_data": {
        "patient_id": "TEST_006_EMPTY_DATA",
        "age": 40
    }
}

def test_api_endpoint(test_name: str, test_data: Dict[str, Any], base_url: str = "http://localhost:8000"):
    """Test a single API endpoint"""
    print(f"\n🧪 Testing: {test_name}")
    print(f"📋 Patient ID: {test_data.get('patient_id', 'Unknown')}")
    
    try:
        # Make API request
        response = requests.post(
            f"{base_url}/analyze/comprehensive",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Analyze results
            modalities_used = result.get('modalities_used', [])
            overall_risk = result.get('overall_risk_assessment', {})
            
            print(f"✅ Status: SUCCESS")
            print(f"📊 Modalities analyzed: {', '.join(modalities_used) if modalities_used else 'None'}")
            
            if overall_risk:
                risk_score = overall_risk.get('overall_risk', 0)
                risk_level = overall_risk.get('risk_category', 'Unknown')
                print(f"⚠️  Overall Risk: {risk_score:.3f} ({risk_level})")
            
            # Check modality-specific results
            modality_results = result.get('modality_results', {})
            for modality, data in modality_results.items():
                if 'risk_score' in data:
                    print(f"   {modality.title()}: {data['risk_score']:.3f}")
                elif 'malignancy_probability' in data:
                    print(f"   {modality.title()}: {data['malignancy_probability']:.3f}")
                elif 'response_probability' in data:
                    print(f"   {modality.title()}: {data['response_probability']:.3f}")
            
            return True, result
            
        else:
            print(f"❌ Status: FAILED (HTTP {response.status_code})")
            print(f"   Error: {response.text}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Status: CONNECTION FAILED")
        print(f"   Make sure the backend is running on {base_url}")
        return False, None
    except Exception as e:
        print(f"❌ Status: ERROR")
        print(f"   Exception: {str(e)}")
        return False, None

def test_health_check(base_url: str = "http://localhost:8000"):
    """Test if the API is running"""
    print("🏥 Testing API Health Check...")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy: {data.get('status', 'Unknown')}")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {str(e)}")
        return False

def run_all_tests():
    """Run all test cases"""
    print("🚀 Starting Breast Cancer AI Platform Tests")
    print("=" * 60)
    
    # Health check first
    if not test_health_check():
        print("\n❌ Cannot proceed - API is not accessible")
        return
    
    # Run all test cases
    results = {}
    total_tests = len(TEST_CASES)
    passed_tests = 0
    
    for test_name, test_data in TEST_CASES.items():
        success, result = test_api_endpoint(test_name, test_data)
        results[test_name] = {
            'success': success,
            'result': result
        }
        
        if success:
            passed_tests += 1
        
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    # Detailed results
    print("\n📋 DETAILED RESULTS:")
    for test_name, data in results.items():
        status = "✅ PASS" if data['success'] else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! The API is working correctly.")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Check the logs above.")

def test_specific_case(case_name: str):
    """Test a specific case by name"""
    if case_name not in TEST_CASES:
        print(f"❌ Test case '{case_name}' not found.")
        print(f"Available cases: {', '.join(TEST_CASES.keys())}")
        return
    
    print(f"🧪 Running specific test: {case_name}")
    success, result = test_api_endpoint(case_name, TEST_CASES[case_name])
    
    if success and result:
        print(f"\n📄 Full Result:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Test specific case
        test_specific_case(sys.argv[1])
    else:
        # Run all tests
        run_all_tests()
    
    print(f"\n💡 Usage:")
    print(f"  python test_api.py                    # Run all tests")
    print(f"  python test_api.py high_risk_imaging  # Test specific case")
    print(f"  python test_api.py genomics_only      # Test genomics only")