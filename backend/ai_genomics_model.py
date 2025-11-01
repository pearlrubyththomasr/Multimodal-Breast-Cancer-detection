# ai_genomics_model.py
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
import warnings
warnings.filterwarnings('ignore')

class GenomicsAnalyzer:
    """AI-powered genomics analysis for breast cancer"""
    
    def __init__(self):
        self.biomarker_weights = {
            'ER_status': {'Positive': 0.1, 'Negative': 0.2},
            'PR_status': {'Positive': 0.1, 'Negative': 0.15},
            'HER2_status': {'Positive': 0.3, 'Negative': -0.1},
            'BRCA_status': {'Positive': 0.4, 'Negative': 0.0}
        }
        
        self.high_risk_genes = {
            'BRCA1': 0.4,
            'BRCA2': 0.35,
            'TP53': 0.3,
            'CHEK2': 0.2,
            'ATM': 0.15,
            'PALB2': 0.25,
            'CDH1': 0.2,
            'PTEN': 0.2
        }
        
        self.mutation_impact = {
            'Pathogenic': 1.0,
            'Likely_pathogenic': 0.8,
            'VUS': 0.3,  # Variant of uncertain significance
            'Likely_benign': 0.1,
            'Benign': 0.0
        }
    
    def analyze_genomic_profile(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive genomic analysis"""
        
        # Extract genomic data
        genomic_alterations = patient_data.get('genomic_alterations', [])
        biomarkers = patient_data.get('biomarkers', {})
        tumor_mutational_burden = patient_data.get('tumor_mutational_burden', 0)
        age = patient_data.get('age', 60)
        tumor_size = patient_data.get('tumor_size', 2.0)
        
        # Calculate risk scores
        genetic_risk = self._calculate_genetic_risk(genomic_alterations)
        biomarker_risk = self._calculate_biomarker_risk(biomarkers)
        clinical_risk = self._calculate_clinical_risk(age, tumor_size, tumor_mutational_burden)
        
        # Combined risk assessment
        overall_risk = self._combine_risk_scores(genetic_risk, biomarker_risk, clinical_risk)
        
        # Generate treatment recommendations
        treatment_response = self._predict_treatment_response(
            genetic_risk, biomarker_risk, biomarkers, genomic_alterations
        )
        
        return {
            'patient_id': patient_data.get('patient_id', 'unknown'),
            'analysis_type': 'genomics',
            'risk_assessment': {
                'overall_risk_score': round(overall_risk, 3),
                'genetic_risk': round(genetic_risk, 3),
                'biomarker_risk': round(biomarker_risk, 3),
                'clinical_risk': round(clinical_risk, 3),
                'risk_category': self._categorize_risk(overall_risk)
            },
            'treatment_prediction': treatment_response,
            'key_findings': self._extract_key_findings(genomic_alterations, biomarkers),
            'recommendations': self._generate_recommendations(overall_risk, biomarkers, genomic_alterations)
        }
    
    def _calculate_genetic_risk(self, genomic_alterations: List[Dict]) -> float:
        """Calculate risk based on genetic alterations"""
        if not genomic_alterations:
            return 0.1  # Baseline risk
        
        total_risk = 0.0
        
        for alteration in genomic_alterations:
            gene = alteration.get('gene', '')
            mutation = alteration.get('mutation', 'VUS')
            allele_frequency = alteration.get('allele_frequency', 0.5)
            
            # Gene-specific risk
            gene_risk = self.high_risk_genes.get(gene, 0.05)
            
            # Mutation impact
            mutation_impact = self.mutation_impact.get(mutation, 0.3)
            
            # Allele frequency impact
            frequency_impact = min(allele_frequency * 2, 1.0) if allele_frequency else 0.5
            
            # Combined alteration risk
            alteration_risk = gene_risk * mutation_impact * frequency_impact
            total_risk += alteration_risk
        
        return min(total_risk, 0.95)  # Cap at 95%
    
    def _calculate_biomarker_risk(self, biomarkers: Dict[str, str]) -> float:
        """Calculate risk based on biomarkers"""
        if not biomarkers:
            return 0.2  # Baseline risk
        
        total_risk = 0.2  # Base risk
        
        for marker, status in biomarkers.items():
            if marker in self.biomarker_weights and status in self.biomarker_weights[marker]:
                total_risk += self.biomarker_weights[marker][status]
        
        return max(0.0, min(total_risk, 0.95))
    
    def _calculate_clinical_risk(self, age: int, tumor_size: float, tmb: float) -> float:
        """Calculate risk based on clinical factors"""
        risk = 0.2  # Base risk
        
        # Age factor
        if age < 40:
            risk += 0.2
        elif age < 50:
            risk += 0.1
        elif age > 70:
            risk += 0.05
        
        # Tumor size factor
        if tumor_size > 5:
            risk += 0.3
        elif tumor_size > 2:
            risk += 0.15
        
        # Tumor mutational burden
        if tmb > 20:
            risk += 0.2
        elif tmb > 10:
            risk += 0.1
        
        return min(risk, 0.95)
    
    def _combine_risk_scores(self, genetic: float, biomarker: float, clinical: float) -> float:
        """Combine different risk scores with weights"""
        weights = {'genetic': 0.5, 'biomarker': 0.3, 'clinical': 0.2}
        
        combined = (
            genetic * weights['genetic'] +
            biomarker * weights['biomarker'] +
            clinical * weights['clinical']
        )
        
        return min(combined, 0.95)
    
    def _predict_treatment_response(self, genetic_risk: float, biomarker_risk: float, 
                                  biomarkers: Dict, alterations: List[Dict]) -> Dict[str, Any]:
        """Predict treatment response based on genomic profile"""
        
        # Base response probability
        base_response = 0.6
        
        # HER2-targeted therapy
        her2_response = 0.5
        if biomarkers.get('HER2_status') == 'Positive':
            her2_response = 0.85
        
        # Hormone therapy
        hormone_response = 0.4
        if biomarkers.get('ER_status') == 'Positive' or biomarkers.get('PR_status') == 'Positive':
            hormone_response = 0.75
        
        # PARP inhibitor (for BRCA mutations)
        parp_response = 0.3
        brca_genes = ['BRCA1', 'BRCA2']
        if any(alt.get('gene') in brca_genes for alt in alterations):
            parp_response = 0.8
        
        # Immunotherapy (based on TMB and specific markers)
        immuno_response = 0.4
        
        return {
            'chemotherapy': {
                'response_probability': round(base_response, 3),
                'confidence': 0.7
            },
            'targeted_therapy': {
                'her2_targeted': {
                    'response_probability': round(her2_response, 3),
                    'recommended': biomarkers.get('HER2_status') == 'Positive'
                },
                'hormone_therapy': {
                    'response_probability': round(hormone_response, 3),
                    'recommended': biomarkers.get('ER_status') == 'Positive' or biomarkers.get('PR_status') == 'Positive'
                },
                'parp_inhibitor': {
                    'response_probability': round(parp_response, 3),
                    'recommended': any(alt.get('gene') in brca_genes for alt in alterations)
                }
            },
            'immunotherapy': {
                'response_probability': round(immuno_response, 3),
                'confidence': 0.6
            }
        }
    
    def _extract_key_findings(self, alterations: List[Dict], biomarkers: Dict) -> List[str]:
        """Extract key genomic findings"""
        findings = []
        
        # High-risk genes
        high_risk_found = [alt['gene'] for alt in alterations if alt.get('gene') in self.high_risk_genes]
        if high_risk_found:
            findings.append(f"High-risk genes detected: {', '.join(high_risk_found)}")
        
        # Biomarker status
        positive_markers = [marker for marker, status in biomarkers.items() if status == 'Positive']
        if positive_markers:
            findings.append(f"Positive biomarkers: {', '.join(positive_markers)}")
        
        # Pathogenic mutations
        pathogenic = [alt['gene'] for alt in alterations if alt.get('mutation') == 'Pathogenic']
        if pathogenic:
            findings.append(f"Pathogenic mutations in: {', '.join(pathogenic)}")
        
        return findings if findings else ["No significant genomic alterations detected"]
    
    def _generate_recommendations(self, risk_score: float, biomarkers: Dict, alterations: List[Dict]) -> List[str]:
        """Generate clinical recommendations"""
        recommendations = []
        
        if risk_score > 0.7:
            recommendations.extend([
                "High-risk profile - urgent multidisciplinary review",
                "Consider genetic counseling",
                "Discuss prophylactic measures if appropriate"
            ])
        elif risk_score > 0.4:
            recommendations.extend([
                "Moderate risk - enhanced surveillance recommended",
                "Consider additional family history assessment"
            ])
        else:
            recommendations.append("Standard risk - routine screening appropriate")
        
        # Specific recommendations based on findings
        if biomarkers.get('HER2_status') == 'Positive':
            recommendations.append("HER2-targeted therapy should be considered")
        
        if biomarkers.get('ER_status') == 'Positive':
            recommendations.append("Hormone receptor-positive - endocrine therapy indicated")
        
        brca_genes = ['BRCA1', 'BRCA2']
        if any(alt.get('gene') in brca_genes for alt in alterations):
            recommendations.append("BRCA mutation detected - PARP inhibitor therapy may be beneficial")
        
        return recommendations
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk level"""
        if risk_score > 0.7:
            return "HIGH"
        elif risk_score > 0.4:
            return "MODERATE"
        else:
            return "LOW"

# Convenience function for external use
def analyze_patient_genomics(patient_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze patient genomics data"""
    analyzer = GenomicsAnalyzer()
    return analyzer.analyze_genomic_profile(patient_data)

# Example usage
if __name__ == "__main__":
    # Test with sample data
    sample_patient = {
        'patient_id': 'TEST_001',
        'age': 45,
        'tumor_size': 3.2,
        'tumor_mutational_burden': 15.5,
        'genomic_alterations': [
            {'gene': 'BRCA1', 'mutation': 'Pathogenic', 'allele_frequency': 0.8},
            {'gene': 'TP53', 'mutation': 'Likely_pathogenic', 'allele_frequency': 0.6}
        ],
        'biomarkers': {
            'ER_status': 'Positive',
            'PR_status': 'Positive',
            'HER2_status': 'Negative',
            'BRCA_status': 'Positive'
        }
    }
    
    result = analyze_patient_genomics(sample_patient)
    print("🧬 Genomics Analysis Result:")
    print(f"Overall Risk: {result['risk_assessment']['overall_risk_score']} ({result['risk_assessment']['risk_category']})")
    print(f"Key Findings: {result['key_findings']}")
    print(f"Recommendations: {result['recommendations']}")