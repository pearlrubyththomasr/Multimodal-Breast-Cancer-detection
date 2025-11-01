# unified_analyzer.py
import pandas as pd
import numpy as np
from typing import Dict, Any, List

class UnifiedAnalyzer:
    """Orchestrates analysis across all modalities"""
    
    def __init__(self, model_loader):
        self.model_loader = model_loader
        self.available_modalities = model_loader.get_available_modalities()
        print(f"🎯 Available modalities: {self.available_modalities}")
    
    def comprehensive_analysis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive multi-modal analysis"""
        print(f"🔍 Comprehensive analysis for {patient_data.get('patient_id')}")
        
        results = {
            'patient_id': patient_data.get('patient_id'),
            'analysis_timestamp': pd.Timestamp.now().isoformat(),
            'modalities_used': [],
            'overall_risk_assessment': {},
            'modality_results': {},
            'treatment_recommendations': [],
            'clinical_guidance': []
        }
        
        # Run available analyses
        if 'genomics' in self.available_modalities and self._has_genomic_data(patient_data):
            results['modality_results']['genomics'] = self.genomics_analysis(patient_data)
            results['modalities_used'].append('genomics')
        
        if 'imaging' in self.available_modalities and self._has_imaging_data(patient_data):
            results['modality_results']['imaging'] = self.imaging_analysis(patient_data)
            results['modalities_used'].append('imaging')
        
        if 'nlp' in self.available_modalities and self._has_clinical_text(patient_data):
            print("🔬 Running NLP analysis...")
            results['modality_results']['nlp'] = self.nlp_analysis(patient_data)
            results['modalities_used'].append('nlp')
            print(f"✅ NLP analysis complete: {results['modality_results']['nlp'].get('status')}")
        else:
            print(f"❌ NLP analysis skipped - Available: {'nlp' in self.available_modalities}, Has text: {self._has_clinical_text(patient_data)}")
        
        # Generate unified assessment
        results['overall_risk_assessment'] = self._generate_unified_risk(results)
        results['treatment_recommendations'] = self._generate_treatment_recommendations(results)
        results['clinical_guidance'] = self._generate_clinical_guidance(results)
        
        return results
    
    def genomics_analysis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform genomics analysis"""
        try:
            # Try to use the complete model first
            complete_model = self.model_loader.get_model('complete_breast_cancer_model')
            if complete_model and hasattr(complete_model, 'predict'):
                # Adapt to your complete model interface
                clinical_data = self._prepare_clinical_data(patient_data)
                prediction = complete_model.predict(clinical_data)
                return {
                    'status': 'complete_model_analysis',
                    'risk_score': float(prediction[0]) if hasattr(prediction, '__iter__') else float(prediction),
                    'model_used': 'complete_breast_cancer_model'
                }
            
            # Fallback to individual genomics model
            genomics_model = self.model_loader.get_model('genomics_model')
            if genomics_model and hasattr(genomics_model, 'predict_treatment_response'):
                genomic_profile = {
                    'genomic_alterations': patient_data.get('genomic_alterations', []),
                    'biomarkers': patient_data.get('biomarkers', {}),
                    'tumor_mutational_burden': patient_data.get('tumor_mutational_burden'),
                    'age': patient_data.get('age'),
                    'tumor_size': patient_data.get('tumor_size')
                }
                results = genomics_model.predict_treatment_response(genomic_profile)
                return {
                    'status': 'genomics_analysis_complete',
                    'response_probability': results.get('response_probability', 0.5),
                    'ai_confidence': results.get('ai_confidence', 0.5),
                    'key_drivers': results.get('key_drivers', [])
                }
            
            return {"status": "genomics_models_available_but_interface_unknown"}
            
        except Exception as e:
            return {"error": f"Genomics analysis failed: {str(e)}", "status": "error"}
    
    def imaging_analysis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform multi-modal imaging analysis"""
        try:
            # Try lightweight model first
            lightweight_model = self.model_loader.get_model('lightweight_breast_cancer_model')
            if lightweight_model and hasattr(lightweight_model, 'comprehensive_analysis'):
                return lightweight_model.comprehensive_analysis(patient_data)
            
            # Fallback to individual imaging models
            return self._legacy_imaging_analysis(patient_data)
            
        except Exception as e:
            return {"error": f"Imaging analysis failed: {str(e)}", "status": "error"}
    
    def nlp_analysis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform clinical text analysis"""
        try:
            bert_model = self.model_loader.get_model('medical_bert_improved')
            clinical_notes = patient_data.get('clinical_notes', [])
            
            if not bert_model:
                return {"status": "nlp_model_not_available", "error": "BERT model not loaded"}
            
            if not clinical_notes:
                return {"status": "no_clinical_text_provided", "error": "No clinical notes provided"}
            
            # Process clinical notes
            all_text = ""
            processed_notes = []
            
            for note in clinical_notes:
                if isinstance(note, dict):
                    text = note.get('text', '')
                    note_type = note.get('type', 'general')
                elif isinstance(note, str):
                    text = note
                    note_type = 'general'
                else:
                    continue
                
                if text.strip():
                    all_text += text + " "
                    processed_notes.append({
                        'text': text,
                        'type': note_type,
                        'length': len(text)
                    })
            
            if not all_text.strip():
                return {"status": "empty_clinical_text", "error": "Clinical notes contain no text"}
            
            # Analyze with BERT model
            bert_results = bert_model.predict(all_text.strip())
            
            # Calculate risk score based on NLP analysis
            risk_score = self._calculate_nlp_risk_score(bert_results, all_text)
            
            # Extract key clinical indicators
            clinical_indicators = self._extract_clinical_indicators(all_text)
            
            return {
                'status': 'nlp_analysis_complete',
                'risk_score': risk_score,
                'ai_confidence': bert_results.get('cancer_assessment', {}).get('confidence', 0.7),
                'risk_category': self._categorize_nlp_risk(risk_score),
                'clinical_indicators': clinical_indicators,
                'bert_analysis': bert_results,
                'notes_processed': len(processed_notes),
                'total_text_length': len(all_text),
                'key_findings': self._extract_key_findings(all_text, bert_results)
            }
                
        except Exception as e:
            return {"error": f"NLP analysis failed: {str(e)}", "status": "error"}
    
    def _calculate_nlp_risk_score(self, bert_results: Dict[str, Any], text: str) -> float:
        """Calculate risk score from NLP analysis"""
        base_risk = 0.3
        
        # Analyze BERT results
        cancer_assessment = bert_results.get('cancer_assessment', {})
        suspicion_level = cancer_assessment.get('suspicion_level', 'low')
        
        if suspicion_level == 'high':
            base_risk += 0.4
        elif suspicion_level == 'moderate':
            base_risk += 0.2
        
        # Analyze symptom severity
        symptom_analysis = bert_results.get('symptom_analysis', {})
        severity = symptom_analysis.get('severity', 'mild')
        
        if severity == 'severe':
            base_risk += 0.3
        elif severity == 'moderate':
            base_risk += 0.15
        
        # Check for high-risk keywords in text
        high_risk_terms = [
            'malignant', 'carcinoma', 'metastasis', 'invasive', 'aggressive',
            'stage iii', 'stage iv', 'lymph node', 'spread', 'recurrence'
        ]
        
        moderate_risk_terms = [
            'suspicious', 'atypical', 'irregular', 'mass', 'lesion',
            'calcifications', 'birads 4', 'birads 5', 'biopsy recommended'
        ]
        
        text_lower = text.lower()
        
        for term in high_risk_terms:
            if term in text_lower:
                base_risk += 0.1
        
        for term in moderate_risk_terms:
            if term in text_lower:
                base_risk += 0.05
        
        return min(0.95, max(0.05, base_risk))
    
    def _categorize_nlp_risk(self, risk_score: float) -> str:
        """Categorize NLP risk score"""
        if risk_score >= 0.7:
            return "HIGH RISK"
        elif risk_score >= 0.4:
            return "MODERATE RISK"
        else:
            return "LOW RISK"
    
    def _extract_clinical_indicators(self, text: str) -> Dict[str, Any]:
        """Extract clinical indicators from text"""
        text_lower = text.lower()
        
        indicators = {
            'symptoms': [],
            'findings': [],
            'risk_factors': [],
            'family_history': False,
            'previous_cancer': False
        }
        
        # Symptom keywords
        symptom_keywords = {
            'breast_lump': ['lump', 'mass', 'nodule'],
            'breast_pain': ['pain', 'tenderness', 'discomfort'],
            'nipple_discharge': ['discharge', 'secretion'],
            'skin_changes': ['dimpling', 'puckering', 'rash', 'redness'],
            'breast_swelling': ['swelling', 'enlargement']
        }
        
        for symptom, keywords in symptom_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                indicators['symptoms'].append(symptom)
        
        # Clinical findings
        finding_keywords = {
            'calcifications': ['calcification', 'microcalcification'],
            'architectural_distortion': ['architectural distortion', 'distortion'],
            'lymphadenopathy': ['lymph node', 'lymphadenopathy', 'adenopathy'],
            'skin_thickening': ['skin thickening', 'thickening']
        }
        
        for finding, keywords in finding_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                indicators['findings'].append(finding)
        
        # Risk factors
        risk_keywords = ['family history', 'brca', 'genetic', 'hereditary']
        if any(keyword in text_lower for keyword in risk_keywords):
            indicators['family_history'] = True
        
        cancer_history_keywords = ['previous cancer', 'history of cancer', 'prior malignancy']
        if any(keyword in text_lower for keyword in cancer_history_keywords):
            indicators['previous_cancer'] = True
        
        return indicators
    
    def _extract_key_findings(self, text: str, bert_results: Dict[str, Any]) -> List[str]:
        """Extract key findings from text and BERT analysis"""
        findings = []
        
        # Add BERT-based findings
        cancer_assessment = bert_results.get('cancer_assessment', {})
        if cancer_assessment.get('suspicion_level') == 'high':
            findings.append("High cancer suspicion detected in clinical notes")
        
        symptom_analysis = bert_results.get('symptom_analysis', {})
        if symptom_analysis.get('severity') == 'severe':
            findings.append("Severe symptoms documented")
        
        urgency = bert_results.get('clinical_urgency', {})
        if urgency.get('level') == 'urgent':
            findings.append("Urgent clinical attention recommended")
        
        # Add text-based findings
        text_lower = text.lower()
        
        if 'birads 4' in text_lower or 'birads 5' in text_lower:
            findings.append("High BI-RADS score documented")
        
        if 'biopsy' in text_lower:
            findings.append("Biopsy mentioned in clinical notes")
        
        if 'metastasis' in text_lower or 'spread' in text_lower:
            findings.append("Possible metastatic disease mentioned")
        
        return findings if findings else ["Standard clinical documentation reviewed"]
    
    def _has_genomic_data(self, patient_data: Dict[str, Any]) -> bool:
        # Check for meaningful genomic data
        genomic_alterations = patient_data.get('genomic_alterations', [])
        biomarkers = patient_data.get('biomarkers', {})
        
        # Only return True if there's actual data, not empty structures
        has_alterations = genomic_alterations and len(genomic_alterations) > 0
        has_biomarkers = biomarkers and any(v for v in biomarkers.values() if v)
        
        return has_alterations or has_biomarkers
    
    def _has_imaging_data(self, patient_data: Dict[str, Any]) -> bool:
        # Check for meaningful imaging data
        ultrasound = patient_data.get('ultrasound_findings', {})
        mammography = patient_data.get('mammography_findings', {})
        xray = patient_data.get('xray_findings', {})
        
        # Only return True if there's actual data, not empty objects
        has_ultrasound = ultrasound and any(v for v in ultrasound.values() if v)
        has_mammography = mammography and any(v for v in mammography.values() if v)
        has_xray = xray and any(v for v in xray.values() if v)
        
        return has_ultrasound or has_mammography or has_xray
    
    def _has_clinical_text(self, patient_data: Dict[str, Any]) -> bool:
        # Check for meaningful clinical text data
        clinical_notes = patient_data.get('clinical_notes', [])
        
        print(f"🔍 Checking clinical text: {clinical_notes}")
        
        # Only return True if there are actual notes with text content
        if not clinical_notes or len(clinical_notes) == 0:
            print("   ❌ No clinical notes provided")
            return False
        
        # Check if any note has actual text content
        has_text = any(note.get('text', '').strip() for note in clinical_notes if isinstance(note, dict))
        print(f"   {'✅' if has_text else '❌'} Has meaningful text: {has_text}")
        return has_text
    
    def _prepare_clinical_data(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare clinical data for model consumption"""
        return {
            'age': patient_data.get('age', 60),
            'tumor_size': patient_data.get('tumor_size', 2.0),
            'genomic_alterations': patient_data.get('genomic_alterations', []),
            'biomarkers': patient_data.get('biomarkers', {})
        }
    
    def _generate_unified_risk(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate unified risk assessment from all modalities"""
        risk_scores = []
        
        # Extract risk scores from each modality
        for modality, analysis in results['modality_results'].items():
            if 'risk_score' in analysis:
                risk_scores.append(analysis['risk_score'])
            elif 'response_probability' in analysis:
                risk_scores.append(analysis['response_probability'])
            elif 'malignancy_probability' in analysis:
                risk_scores.append(analysis['malignancy_probability'])
        
        if risk_scores:
            overall_risk = np.mean(risk_scores)
            confidence = min(risk_scores)  # Use minimum as confidence measure
        else:
            overall_risk = 0.1  # Baseline risk
            confidence = 0.5
        
        # Categorize risk
        if overall_risk > 0.7:
            category = "HIGH RISK"
        elif overall_risk > 0.4:
            category = "MEDIUM RISK"
        else:
            category = "LOW RISK"
        
        return {
            'overall_risk': round(overall_risk, 3),
            'risk_category': category,
            'confidence': round(confidence, 3),
            'modalities_considered': len(risk_scores)
        }
    
    def _generate_treatment_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate treatment recommendations based on risk"""
        risk_category = results['overall_risk_assessment']['risk_category']
        
        if risk_category == "HIGH RISK":
            return [
                "Urgent multidisciplinary review required",
                "Consider immediate biopsy",
                "Genetic counseling recommended",
                "Surgical oncology consultation"
            ]
        elif risk_category == "MEDIUM RISK":
            return [
                "Close clinical monitoring",
                "Consider additional diagnostic imaging",
                "3-6 month follow-up recommended"
            ]
        else:
            return [
                "Continue routine screening",
                "Annual follow-up as per guidelines"
            ]
    
    def _generate_clinical_guidance(self, results: Dict[str, Any]) -> List[str]:
        """Generate clinical guidance"""
        guidance = []
        
        if results['overall_risk_assessment']['risk_category'] == "HIGH RISK":
            guidance.append("Patient should be seen within 1-2 weeks")
        
        if len(results['modalities_used']) >= 2:
            guidance.append("Multi-modal consensus achieved")
        else:
            guidance.append("Limited modality analysis - consider additional tests")
        
        return guidance
    
    def _legacy_imaging_analysis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback imaging analysis with comprehensive scoring"""
        risk_scores = []
        modalities_analyzed = []
        detailed_results = {}
        
        # Analyze ultrasound findings
        if 'ultrasound_findings' in patient_data and patient_data['ultrasound_findings']:
            us_findings = patient_data['ultrasound_findings']
            us_risk = 0.0
            
            # Mass characteristics
            if us_findings.get('mass_present', 0):
                us_risk += 0.3
                mass_size = us_findings.get('mass_size', 0)
                if mass_size > 2.0:
                    us_risk += 0.2
                if us_findings.get('mass_shape_irregular', 0):
                    us_risk += 0.15
                if us_findings.get('mass_margins', 0):
                    us_risk += 0.15
            
            # Other features
            if us_findings.get('calcifications', 0):
                us_risk += 0.1
            if us_findings.get('echo_pattern', 0):
                us_risk += 0.1
            
            # BI-RADS score
            birads = us_findings.get('birads_score', 2)
            if birads >= 4:
                us_risk += 0.3
            elif birads == 3:
                us_risk += 0.1
            
            us_risk = min(us_risk, 1.0)  # Cap at 1.0
            risk_scores.append(us_risk)
            modalities_analyzed.append('ultrasound')
            detailed_results['ultrasound'] = {
                'risk_score': us_risk,
                'birads_score': birads,
                'mass_present': bool(us_findings.get('mass_present', 0)),
                'mass_size': us_findings.get('mass_size', 0)
            }
        
        # Analyze mammography findings
        if 'mammography_findings' in patient_data and patient_data['mammography_findings']:
            mammo_findings = patient_data['mammography_findings']
            mammo_risk = 0.0
            
            if mammo_findings.get('mass_present', 0):
                mammo_risk += 0.25
            if mammo_findings.get('calcifications', 0):
                mammo_risk += 0.2
            if mammo_findings.get('architectural_distortion', 0):
                mammo_risk += 0.3
            if mammo_findings.get('asymmetry', 0):
                mammo_risk += 0.15
            if mammo_findings.get('skin_thickening', 0):
                mammo_risk += 0.2
            
            # BI-RADS score
            birads = mammo_findings.get('birads_score', 2)
            if birads >= 4:
                mammo_risk += 0.3
            elif birads == 3:
                mammo_risk += 0.1
            
            mammo_risk = min(mammo_risk, 1.0)
            risk_scores.append(mammo_risk)
            modalities_analyzed.append('mammography')
            detailed_results['mammography'] = {
                'risk_score': mammo_risk,
                'birads_score': birads,
                'findings_count': sum([
                    mammo_findings.get('mass_present', 0),
                    mammo_findings.get('calcifications', 0),
                    mammo_findings.get('architectural_distortion', 0),
                    mammo_findings.get('asymmetry', 0),
                    mammo_findings.get('skin_thickening', 0)
                ])
            }
        
        # Analyze X-ray findings
        if 'xray_findings' in patient_data and patient_data['xray_findings']:
            xray_findings = patient_data['xray_findings']
            xray_risk = 0.0
            
            if xray_findings.get('lung_metastasis', 0):
                xray_risk += 0.4
            if xray_findings.get('pleural_effusion', 0):
                xray_risk += 0.3
            if xray_findings.get('lymphadenopathy', 0):
                xray_risk += 0.25
            if xray_findings.get('bone_metastasis', 0):
                xray_risk += 0.35
            
            # Cancer stage
            stage = xray_findings.get('cancer_stage', 1)
            if stage >= 3:
                xray_risk += 0.3
            elif stage == 2:
                xray_risk += 0.15
            
            xray_risk = min(xray_risk, 1.0)
            risk_scores.append(xray_risk)
            modalities_analyzed.append('xray')
            detailed_results['xray'] = {
                'risk_score': xray_risk,
                'stage': stage,
                'metastasis_indicators': sum([
                    xray_findings.get('lung_metastasis', 0),
                    xray_findings.get('pleural_effusion', 0),
                    xray_findings.get('lymphadenopathy', 0),
                    xray_findings.get('bone_metastasis', 0)
                ])
            }
        
        # Calculate overall risk
        if risk_scores:
            overall_risk = sum(risk_scores) / len(risk_scores)
        else:
            overall_risk = 0.0
        
        return {
            'status': 'basic_imaging_analysis',
            'risk_score': round(overall_risk, 3),
            'malignancy_probability': round(overall_risk, 3),
            'modalities_analyzed': modalities_analyzed,
            'detailed_results': detailed_results,
            'modalities_count': len(modalities_analyzed),
            'confidence': 0.75 if len(modalities_analyzed) > 1 else 0.6
        }