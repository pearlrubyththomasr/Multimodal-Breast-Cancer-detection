# breast_cancer_imaging_analysis.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

class ImagingAnalyzer:
    """Lightweight imaging analysis for breast cancer"""
    
    def __init__(self):
        self.ultrasound_model = None
        self.mammography_model = None
        self.xray_model = None
        self.scalers = {}
        self.is_trained = False
        
        # Feature definitions
        self.ultrasound_features = [
            'mass_present', 'mass_size', 'mass_shape_irregular',
            'mass_margins', 'echo_pattern', 'calcifications', 'birads_score'
        ]
        
        self.mammography_features = [
            'mass_present', 'calcifications', 'architectural_distortion',
            'asymmetry', 'skin_thickening', 'birads_score', 'breast_density'
        ]
        
        self.xray_features = [
            'lung_metastasis', 'pleural_effusion', 'lymphadenopathy',
            'bone_metastasis', 'cancer_stage'
        ]
    
    def generate_synthetic_data(self, n_samples=500):
        """Generate synthetic imaging data for training"""
        np.random.seed(42)
        
        # Ultrasound data
        ultrasound_data = []
        for i in range(n_samples):
            has_mass = np.random.choice([0, 1], p=[0.4, 0.6])
            mass_size = np.random.uniform(0.3, 4.5) if has_mass else 0.0
            birads = np.random.choice([2, 3, 4, 5], p=[0.3, 0.4, 0.2, 0.1])
            
            # Calculate malignancy probability
            malignancy_prob = (
                has_mass * 0.25 +
                (mass_size > 2) * 0.15 +
                np.random.choice([0, 1], p=[0.7, 0.3]) * 0.20 +  # irregular shape
                np.random.choice([0, 1], p=[0.6, 0.4]) * 0.15 +  # margins
                np.random.choice([0, 1], p=[0.5, 0.5]) * 0.10 +  # echo pattern
                np.random.choice([0, 1], p=[0.8, 0.2]) * 0.10 +  # calcifications
                (birads >= 4) * 0.25 +
                np.random.normal(0, 0.05)
            )
            
            ultrasound_data.append({
                'mass_present': has_mass,
                'mass_size': mass_size,
                'mass_shape_irregular': np.random.choice([0, 1], p=[0.7, 0.3]) if has_mass else 0,
                'mass_margins': np.random.choice([0, 1], p=[0.6, 0.4]) if has_mass else 0,
                'echo_pattern': np.random.choice([0, 1], p=[0.5, 0.5]),
                'calcifications': np.random.choice([0, 1], p=[0.8, 0.2]),
                'birads_score': birads,
                'malignant': 1 if malignancy_prob > 0.5 else 0
            })
        
        # Mammography data
        mammography_data = []
        for i in range(n_samples):
            birads = np.random.choice([1, 2, 3, 4, 5], p=[0.2, 0.3, 0.3, 0.15, 0.05])
            
            malignancy_prob = (
                np.random.choice([0, 1], p=[0.5, 0.5]) * 0.20 +  # mass
                np.random.choice([0, 1], p=[0.6, 0.4]) * 0.25 +  # calcifications
                np.random.choice([0, 1], p=[0.85, 0.15]) * 0.30 +  # distortion
                np.random.choice([0, 1], p=[0.7, 0.3]) * 0.10 +  # asymmetry
                np.random.choice([0, 1], p=[0.9, 0.1]) * 0.25 +  # skin thickening
                (birads >= 4) * 0.25 +
                np.random.normal(0, 0.05)
            )
            
            mammography_data.append({
                'mass_present': np.random.choice([0, 1], p=[0.5, 0.5]),
                'calcifications': np.random.choice([0, 1], p=[0.6, 0.4]),
                'architectural_distortion': np.random.choice([0, 1], p=[0.85, 0.15]),
                'asymmetry': np.random.choice([0, 1], p=[0.7, 0.3]),
                'skin_thickening': np.random.choice([0, 1], p=[0.9, 0.1]),
                'birads_score': birads,
                'breast_density': np.random.choice([1, 2, 3, 4], p=[0.1, 0.4, 0.3, 0.2]),
                'malignant': 1 if malignancy_prob > 0.5 else 0
            })
        
        # X-ray data
        xray_data = []
        for i in range(n_samples):
            cancer_stage = np.random.choice([1, 2, 3, 4], p=[0.4, 0.3, 0.2, 0.1])
            base_met_prob = (cancer_stage - 1) * 0.2
            
            lung_met = 1 if np.random.random() < base_met_prob + 0.05 else 0
            pleural_eff = 1 if np.random.random() < base_met_prob + 0.03 else 0
            lymph = 1 if np.random.random() < base_met_prob + 0.08 else 0
            bone_met = 1 if np.random.random() < base_met_prob + 0.10 else 0
            
            xray_data.append({
                'lung_metastasis': lung_met,
                'pleural_effusion': pleural_eff,
                'lymphadenopathy': lymph,
                'bone_metastasis': bone_met,
                'cancer_stage': cancer_stage,
                'any_metastasis': 1 if any([lung_met, pleural_eff, lymph, bone_met]) else 0
            })
        
        return (pd.DataFrame(ultrasound_data), 
                pd.DataFrame(mammography_data), 
                pd.DataFrame(xray_data))
    
    def train_models(self):
        """Train all imaging models"""
        print("🔬 Training imaging analysis models...")
        
        # Generate synthetic data
        us_data, mammo_data, xray_data = self.generate_synthetic_data()
        
        # Train ultrasound model
        X_us = us_data[self.ultrasound_features]
        y_us = us_data['malignant']
        
        self.ultrasound_model = RandomForestClassifier(
            n_estimators=50, max_depth=8, random_state=42, class_weight='balanced'
        )
        self.ultrasound_model.fit(X_us, y_us)
        
        # Train mammography model
        X_mammo = mammo_data[self.mammography_features]
        y_mammo = mammo_data['malignant']
        
        self.mammography_model = RandomForestClassifier(
            n_estimators=50, max_depth=8, random_state=42, class_weight='balanced'
        )
        self.mammography_model.fit(X_mammo, y_mammo)
        
        # Train X-ray model
        X_xray = xray_data[self.xray_features]
        y_xray = xray_data['any_metastasis']
        
        self.xray_model = RandomForestClassifier(
            n_estimators=50, max_depth=6, random_state=42, class_weight='balanced'
        )
        self.xray_model.fit(X_xray, y_xray)
        
        self.is_trained = True
        
        # Print training accuracies
        print(f"✅ Ultrasound model accuracy: {self.ultrasound_model.score(X_us, y_us):.3f}")
        print(f"✅ Mammography model accuracy: {self.mammography_model.score(X_mammo, y_mammo):.3f}")
        print(f"✅ X-ray model accuracy: {self.xray_model.score(X_xray, y_xray):.3f}")
    
    def analyze_ultrasound(self, findings):
        """Analyze ultrasound findings"""
        if not self.is_trained:
            self.train_models()
        
        # Prepare features
        features = []
        for feature in self.ultrasound_features:
            features.append(findings.get(feature, 0))
        
        features_array = np.array(features).reshape(1, -1)
        probability = self.ultrasound_model.predict_proba(features_array)[0][1]
        
        return {
            'modality': 'ultrasound',
            'malignancy_probability': round(probability, 3),
            'risk_category': self._categorize_risk(probability),
            'confidence': min(probability, 1-probability) * 2,
            'key_findings': self._extract_ultrasound_findings(findings),
            'recommendations': self._generate_ultrasound_recommendations(probability, findings)
        }
    
    def analyze_mammography(self, findings):
        """Analyze mammography findings"""
        if not self.is_trained:
            self.train_models()
        
        features = []
        for feature in self.mammography_features:
            features.append(findings.get(feature, 0))
        
        features_array = np.array(features).reshape(1, -1)
        probability = self.mammography_model.predict_proba(features_array)[0][1]
        
        density_map = {1: 'Fatty', 2: 'Scattered', 3: 'Heterogeneous', 4: 'Extremely Dense'}
        
        return {
            'modality': 'mammography',
            'malignancy_probability': round(probability, 3),
            'risk_category': self._categorize_risk(probability),
            'birads_category': f"BI-RADS {findings.get('birads_score', 2)}",
            'breast_density': density_map.get(findings.get('breast_density', 2), 'Unknown'),
            'key_findings': self._extract_mammography_findings(findings),
            'recommendations': self._generate_mammography_recommendations(probability)
        }
    
    def analyze_xray(self, findings):
        """Analyze chest X-ray findings"""
        if not self.is_trained:
            self.train_models()
        
        features = []
        for feature in self.xray_features:
            features.append(findings.get(feature, 0))
        
        features_array = np.array(features).reshape(1, -1)
        probability = self.xray_model.predict_proba(features_array)[0][1]
        
        metastasis_sites = []
        if findings.get('lung_metastasis'): metastasis_sites.append('Lung')
        if findings.get('pleural_effusion'): metastasis_sites.append('Pleura')
        if findings.get('lymphadenopathy'): metastasis_sites.append('Lymph nodes')
        if findings.get('bone_metastasis'): metastasis_sites.append('Bone')
        
        return {
            'modality': 'chest_xray',
            'metastasis_probability': round(probability, 3),
            'risk_category': self._categorize_risk(probability),
            'sites_detected': metastasis_sites,
            'stage': f"Stage {findings.get('cancer_stage', 1)}",
            'recommendations': self._generate_xray_recommendations(probability, metastasis_sites)
        }
    
    def comprehensive_analysis(self, patient_data):
        """Perform comprehensive imaging analysis"""
        if not self.is_trained:
            self.train_models()
        
        results = {
            'patient_id': patient_data.get('patient_id', 'unknown'),
            'analysis_timestamp': pd.Timestamp.now().isoformat(),
            'modalities_analyzed': []
        }
        
        # Analyze each available modality
        if 'ultrasound_findings' in patient_data and patient_data['ultrasound_findings']:
            results['ultrasound'] = self.analyze_ultrasound(patient_data['ultrasound_findings'])
            results['modalities_analyzed'].append('ultrasound')
        
        if 'mammography_findings' in patient_data and patient_data['mammography_findings']:
            results['mammography'] = self.analyze_mammography(patient_data['mammography_findings'])
            results['modalities_analyzed'].append('mammography')
        
        if 'xray_findings' in patient_data and patient_data['xray_findings']:
            results['chest_xray'] = self.analyze_xray(patient_data['xray_findings'])
            results['modalities_analyzed'].append('chest_xray')
        
        # Generate unified assessment
        results['unified_assessment'] = self._generate_unified_assessment(results)
        
        return results
    
    def _categorize_risk(self, probability):
        """Categorize risk level"""
        if probability > 0.7:
            return "HIGH"
        elif probability > 0.4:
            return "MODERATE"
        else:
            return "LOW"
    
    def _extract_ultrasound_findings(self, findings):
        """Extract key ultrasound findings"""
        findings_list = []
        if findings.get('mass_present'): 
            findings_list.append(f"Mass present ({findings.get('mass_size', 0):.1f}cm)")
        if findings.get('mass_shape_irregular'): 
            findings_list.append('Irregular shape')
        if findings.get('calcifications'): 
            findings_list.append('Calcifications')
        if findings.get('birads_score', 0) >= 4:
            findings_list.append(f"BI-RADS {findings['birads_score']}")
        
        return findings_list if findings_list else ['No significant findings']
    
    def _extract_mammography_findings(self, findings):
        """Extract key mammography findings"""
        findings_list = []
        if findings.get('mass_present'): findings_list.append('Mass')
        if findings.get('calcifications'): findings_list.append('Calcifications')
        if findings.get('architectural_distortion'): findings_list.append('Architectural distortion')
        if findings.get('asymmetry'): findings_list.append('Asymmetry')
        if findings.get('skin_thickening'): findings_list.append('Skin thickening')
        
        return findings_list if findings_list else ['No significant findings']
    
    def _generate_ultrasound_recommendations(self, probability, findings):
        """Generate ultrasound-specific recommendations"""
        if probability > 0.7:
            return ["Urgent biopsy recommended", "Surgical consultation", "Multidisciplinary review"]
        elif probability > 0.4:
            return ["Short-term follow-up (3-6 months)", "Consider additional imaging", "Correlate with clinical findings"]
        else:
            return ["Routine screening", "Annual follow-up", "Continue surveillance"]
    
    def _generate_mammography_recommendations(self, probability):
        """Generate mammography-specific recommendations"""
        if probability > 0.6:
            return ["Diagnostic workup", "Ultrasound correlation", "Consider biopsy"]
        elif probability > 0.3:
            return ["6-month follow-up", "Additional views if needed", "Clinical correlation"]
        else:
            return ["Routine annual screening", "Continue standard surveillance"]
    
    def _generate_xray_recommendations(self, probability, sites):
        """Generate X-ray specific recommendations"""
        if probability > 0.6:
            recs = ["PET-CT for full staging", "Oncology consultation", "Systemic therapy evaluation"]
            if 'Bone' in sites:
                recs.append("Bone scan recommended")
            return recs
        elif probability > 0.3:
            return ["CT scan for confirmation", "3-month follow-up", "Monitor for progression"]
        else:
            return ["Routine surveillance", "Standard follow-up imaging"]
    
    def _generate_unified_assessment(self, results):
        """Generate unified risk assessment from all imaging modalities"""
        risk_scores = []
        
        # Collect risk scores from all modalities
        for modality in ['ultrasound', 'mammography']:
            if modality in results:
                risk_scores.append(results[modality]['malignancy_probability'])
        
        if 'chest_xray' in results:
            risk_scores.append(results['chest_xray']['metastasis_probability'])
        
        if risk_scores:
            overall_risk = np.mean(risk_scores)
        else:
            overall_risk = 0.1
        
        # Risk categorization
        if overall_risk > 0.7:
            category = "HIGH RISK"
            actions = ["Urgent multidisciplinary review", "Immediate biopsy consideration", "Oncology referral"]
        elif overall_risk > 0.4:
            category = "MODERATE RISK"
            actions = ["Close monitoring", "Additional imaging if needed", "Clinical correlation"]
        else:
            category = "LOW RISK"
            actions = ["Routine surveillance", "Continue screening schedule"]
        
        return {
            'overall_risk_score': round(overall_risk, 3),
            'risk_category': category,
            'recommended_actions': actions,
            'modalities_count': len(risk_scores),
            'confidence': round(np.std(risk_scores) if len(risk_scores) > 1 else 0.7, 3)
        }
    
    def save_models(self, base_path="models/"):
        """Save trained models"""
        if not self.is_trained:
            self.train_models()
        
        import os
        os.makedirs(base_path, exist_ok=True)
        
        # Save individual models
        joblib.dump(self.ultrasound_model, f"{base_path}ultrasound_model.joblib")
        joblib.dump(self.mammography_model, f"{base_path}mammography_model.joblib")
        joblib.dump(self.xray_model, f"{base_path}xray_model.joblib")
        
        # Save complete analyzer
        analyzer_data = {
            'ultrasound_model': self.ultrasound_model,
            'mammography_model': self.mammography_model,
            'xray_model': self.xray_model,
            'ultrasound_features': self.ultrasound_features,
            'mammography_features': self.mammography_features,
            'xray_features': self.xray_features,
            'is_trained': self.is_trained,
            'version': '1.0.0'
        }
        
        joblib.dump(analyzer_data, f"{base_path}imaging_analyzer.joblib")
        print(f"✅ Imaging models saved to {base_path}")
    
    def load_models(self, base_path="models/"):
        """Load trained models"""
        try:
            analyzer_data = joblib.load(f"{base_path}imaging_analyzer.joblib")
            
            self.ultrasound_model = analyzer_data['ultrasound_model']
            self.mammography_model = analyzer_data['mammography_model']
            self.xray_model = analyzer_data['xray_model']
            self.ultrasound_features = analyzer_data['ultrasound_features']
            self.mammography_features = analyzer_data['mammography_features']
            self.xray_features = analyzer_data['xray_features']
            self.is_trained = analyzer_data['is_trained']
            
            print(f"✅ Imaging models loaded from {base_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return False

# Convenience function for external use
def analyze_patient_imaging(patient_data):
    """Analyze patient imaging data"""
    analyzer = ImagingAnalyzer()
    return analyzer.comprehensive_analysis(patient_data)

# Example usage and testing
if __name__ == "__main__":
    print("🔬 Testing Breast Cancer Imaging Analysis")
    
    # Initialize analyzer
    analyzer = ImagingAnalyzer()
    
    # Test with sample data
    sample_patient = {
        'patient_id': 'IMG_TEST_001',
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
    
    # Perform analysis
    results = analyzer.comprehensive_analysis(sample_patient)
    
    print(f"\n📊 Analysis Results for {results['patient_id']}:")
    print(f"📈 Overall Risk: {results['unified_assessment']['overall_risk_score']} ({results['unified_assessment']['risk_category']})")
    print(f"🔬 Modalities: {', '.join(results['modalities_analyzed'])}")
    
    # Save models for future use
    analyzer.save_models()
    
    print("\n✅ Imaging analysis system ready!")