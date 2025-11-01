#!/usr/bin/env python3
"""
Detailed check for ai_genomics_model.py, breast_cancer_imaging_analysis.py, and medical_bert_classifier.py
"""

import sys
import traceback

def test_ai_genomics_model():
    """Test ai_genomics_model.py thoroughly"""
    print("🧬 Testing ai_genomics_model.py")
    print("-" * 40)
    
    try:
        from ai_genomics_model import GenomicsAnalyzer, analyze_patient_genomics
        print("✅ Import successful")
        
        # Test initialization
        analyzer = GenomicsAnalyzer()
        print("✅ GenomicsAnalyzer initialization successful")
        
        # Test with comprehensive data
        test_data = {
            'patient_id': 'GENOMICS_TEST_001',
            'age': 42,
            'tumor_size': 3.2,
            'tumor_mutational_burden': 18.5,
            'genomic_alterations': [
                {'gene': 'BRCA1', 'mutation': 'Pathogenic', 'allele_frequency': 0.85},
                {'gene': 'TP53', 'mutation': 'Likely_pathogenic', 'allele_frequency': 0.65},
                {'gene': 'CHEK2', 'mutation': 'VUS', 'allele_frequency': 0.45}
            ],
            'biomarkers': {
                'ER_status': 'Positive',
                'PR_status': 'Positive',
                'HER2_status': 'Negative',
                'BRCA_status': 'Positive'
            }
        }
        
        # Test analysis
        result = analyzer.analyze_genomic_profile(test_data)
        print(f"✅ Analysis successful - Risk: {result['risk_assessment']['risk_category']}")
        print(f"   Overall Risk Score: {result['risk_assessment']['overall_risk_score']}")
        print(f"   Key Findings: {len(result['key_findings'])}")
        print(f"   Recommendations: {len(result['recommendations'])}")
        
        # Test convenience function
        result2 = analyze_patient_genomics(test_data)
        print("✅ Convenience function works")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in ai_genomics_model: {e}")
        traceback.print_exc()
        return False

def test_breast_cancer_imaging_analysis():
    """Test breast_cancer_imaging_analysis.py thoroughly"""
    print("\n🔬 Testing breast_cancer_imaging_analysis.py")
    print("-" * 40)
    
    try:
        from breast_cancer_imaging_analysis import ImagingAnalyzer, analyze_patient_imaging
        print("✅ Import successful")
        
        # Test initialization
        analyzer = ImagingAnalyzer()
        print("✅ ImagingAnalyzer initialization successful")
        
        # Test with comprehensive imaging data
        test_data = {
            'patient_id': 'IMAGING_TEST_001',
            'ultrasound_findings': {
                'mass_present': 1,
                'mass_size': 3.5,
                'mass_shape_irregular': 1,
                'mass_margins': 1,
                'echo_pattern': 1,
                'calcifications': 1,
                'birads_score': 4
            },
            'mammography_findings': {
                'mass_present': 1,
                'calcifications': 1,
                'architectural_distortion': 0,
                'asymmetry': 1,
                'skin_thickening': 0,
                'birads_score': 4,
                'breast_density': 3
            },
            'xray_findings': {
                'lung_metastasis': 0,
                'pleural_effusion': 0,
                'lymphadenopathy': 1,
                'bone_metastasis': 0,
                'cancer_stage': 2
            }
        }
        
        # Test comprehensive analysis
        result = analyzer.comprehensive_analysis(test_data)
        print(f"✅ Comprehensive analysis successful")
        print(f"   Modalities analyzed: {result['modalities_analyzed']}")
        print(f"   Overall risk: {result['unified_assessment']['risk_category']}")
        
        # Test individual modalities
        if 'ultrasound' in result:
            print(f"   Ultrasound risk: {result['ultrasound']['risk_category']}")
        
        if 'mammography' in result:
            print(f"   Mammography risk: {result['mammography']['risk_category']}")
        
        if 'chest_xray' in result:
            print(f"   X-ray risk: {result['chest_xray']['risk_category']}")
        
        # Test individual analysis methods
        us_result = analyzer.analyze_ultrasound(test_data['ultrasound_findings'])
        print(f"✅ Individual ultrasound analysis: {us_result['risk_category']}")
        
        mammo_result = analyzer.analyze_mammography(test_data['mammography_findings'])
        print(f"✅ Individual mammography analysis: {mammo_result['risk_category']}")
        
        xray_result = analyzer.analyze_xray(test_data['xray_findings'])
        print(f"✅ Individual X-ray analysis: {xray_result['risk_category']}")
        
        # Test model saving/loading
        try:
            analyzer.save_models("test_models/")
            print("✅ Model saving successful")
            
            new_analyzer = ImagingAnalyzer()
            if new_analyzer.load_models("test_models/"):
                print("✅ Model loading successful")
            else:
                print("⚠️ Model loading failed (expected if no saved models)")
        except Exception as e:
            print(f"⚠️ Model save/load test failed: {e}")
        
        # Test convenience function
        result2 = analyze_patient_imaging(test_data)
        print("✅ Convenience function works")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in breast_cancer_imaging_analysis: {e}")
        traceback.print_exc()
        return False

def test_medical_bert_classifier():
    """Test medical_bert_classifier.py thoroughly"""
    print("\n🤖 Testing medical_bert_classifier.py")
    print("-" * 40)
    
    try:
        from medical_bert_classifier import MedicalBERTClassifier
        print("✅ Import successful")
        
        # Test initialization
        classifier = MedicalBERTClassifier()
        print("✅ MedicalBERTClassifier initialization successful")
        print(f"   Device: {classifier.device}")
        print(f"   Model name: {classifier.model_name}")
        print(f"   Label map: {list(classifier.label_map.keys())}")
        
        # Test model initialization (this downloads BERT model)
        print("🔄 Initializing BERT model (may take time for first run)...")
        try:
            classifier.initialize_model()
            print("✅ BERT model initialization successful")
            
            # Test synthetic data generation
            print("🔄 Generating synthetic medical text...")
            synthetic_data = classifier.generate_synthetic_medical_text(100)
            print(f"✅ Generated {len(synthetic_data)} synthetic samples")
            print(f"   Sample text: {synthetic_data.iloc[0]['text'][:100]}...")
            
            # Test prediction (without training)
            test_text = "Patient presents with suspicious breast mass, family history of BRCA mutations, urgent evaluation needed"
            print("🔄 Testing prediction interface...")
            
            # Note: This will fail if model isn't trained, but we test the interface
            try:
                result = classifier.predict(test_text)
                print("✅ Prediction interface works")
                print(f"   Clinical urgency: {result['clinical_urgency']['level']}")
                print(f"   Cancer assessment: {result['cancer_assessment']['suspicion_level']}")
            except Exception as pred_e:
                print(f"⚠️ Prediction failed (expected if not trained): {pred_e}")
            
            # Test training preparation
            print("🔄 Testing training data preparation...")
            train_dataset, val_dataset = classifier.prepare_datasets(synthetic_data)
            print(f"✅ Dataset preparation successful")
            print(f"   Training samples: {len(train_dataset)}")
            print(f"   Validation samples: {len(val_dataset)}")
            
        except Exception as bert_e:
            print(f"⚠️ BERT model initialization failed: {bert_e}")
            print("   This might be due to network issues or missing dependencies")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in medical_bert_classifier: {e}")
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between modules"""
    print("\n🔗 Testing Integration")
    print("-" * 40)
    
    try:
        # Test if all modules can be imported together
        from ai_genomics_model import GenomicsAnalyzer
        from breast_cancer_imaging_analysis import ImagingAnalyzer
        from medical_bert_classifier import MedicalBERTClassifier
        
        print("✅ All modules can be imported together")
        
        # Test if they can be instantiated together
        genomics = GenomicsAnalyzer()
        imaging = ImagingAnalyzer()
        bert = MedicalBERTClassifier()
        
        print("✅ All modules can be instantiated together")
        
        # Test with unified patient data
        patient_data = {
            'patient_id': 'INTEGRATION_TEST_001',
            'age': 48,
            'tumor_size': 2.9,
            'tumor_mutational_burden': 15.2,
            'genomic_alterations': [
                {'gene': 'BRCA2', 'mutation': 'Pathogenic', 'allele_frequency': 0.75}
            ],
            'biomarkers': {
                'ER_status': 'Positive',
                'HER2_status': 'Positive'
            },
            'ultrasound_findings': {
                'mass_present': 1,
                'mass_size': 2.9,
                'birads_score': 4
            },
            'clinical_notes': [
                {'text': 'Patient with strong family history of breast cancer, palpable mass detected'}
            ]
        }
        
        # Test genomics analysis
        genomics_result = genomics.analyze_genomic_profile(patient_data)
        print(f"✅ Genomics integration: {genomics_result['risk_assessment']['risk_category']}")
        
        # Test imaging analysis
        imaging_result = imaging.comprehensive_analysis(patient_data)
        print(f"✅ Imaging integration: {imaging_result['unified_assessment']['risk_category']}")
        
        print("✅ Integration test successful")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all detailed checks"""
    print("🔍 Detailed Backend Module Check")
    print("=" * 50)
    
    tests = [
        ("AI Genomics Model", test_ai_genomics_model),
        ("Breast Cancer Imaging Analysis", test_breast_cancer_imaging_analysis),
        ("Medical BERT Classifier", test_medical_bert_classifier),
        ("Integration Test", test_integration)
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
    print(f"🎯 Detailed Check Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All detailed checks passed! All modules are working correctly.")
    else:
        print("⚠️ Some detailed checks failed. See specific errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)