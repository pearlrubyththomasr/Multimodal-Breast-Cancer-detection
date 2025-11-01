# schemas.py
from typing import Optional, List, Dict, Any

# Simple data classes without Pydantic for compatibility
class GenomicAlteration:
    def __init__(self, gene: str, mutation: str, allele_frequency: Optional[float] = None):
        self.gene = gene
        self.mutation = mutation
        self.allele_frequency = allele_frequency

class Biomarkers:
    def __init__(self, ER_status: Optional[str] = None, PR_status: Optional[str] = None, 
                 HER2_status: Optional[str] = None, BRCA_status: Optional[str] = None):
        self.ER_status = ER_status
        self.PR_status = PR_status
        self.HER2_status = HER2_status
        self.BRCA_status = BRCA_status

class UltrasoundFindings:
    def __init__(self, mass_present: int = 0, mass_size: float = 0.0, 
                 mass_shape_irregular: int = 0, mass_margins: int = 0,
                 echo_pattern: int = 0, calcifications: int = 0, birads_score: int = 2):
        self.mass_present = max(0, min(1, mass_present))
        self.mass_size = max(0.0, mass_size)
        self.mass_shape_irregular = max(0, min(1, mass_shape_irregular))
        self.mass_margins = max(0, min(1, mass_margins))
        self.echo_pattern = max(0, min(1, echo_pattern))
        self.calcifications = max(0, min(1, calcifications))
        self.birads_score = max(1, min(5, birads_score))

class MammographyFindings:
    def __init__(self, mass_present: int = 0, calcifications: int = 0,
                 architectural_distortion: int = 0, asymmetry: int = 0,
                 skin_thickening: int = 0, birads_score: int = 2, breast_density: int = 2):
        self.mass_present = max(0, min(1, mass_present))
        self.calcifications = max(0, min(1, calcifications))
        self.architectural_distortion = max(0, min(1, architectural_distortion))
        self.asymmetry = max(0, min(1, asymmetry))
        self.skin_thickening = max(0, min(1, skin_thickening))
        self.birads_score = max(1, min(5, birads_score))
        self.breast_density = max(1, min(4, breast_density))

class XRayFindings:
    def __init__(self, lung_metastasis: int = 0, pleural_effusion: int = 0,
                 lymphadenopathy: int = 0, bone_metastasis: int = 0, cancer_stage: int = 1):
        self.lung_metastasis = max(0, min(1, lung_metastasis))
        self.pleural_effusion = max(0, min(1, pleural_effusion))
        self.lymphadenopathy = max(0, min(1, lymphadenopathy))
        self.bone_metastasis = max(0, min(1, bone_metastasis))
        self.cancer_stage = max(1, min(4, cancer_stage))

class ClinicalText:
    def __init__(self, text: str, note_type: str = "clinical_note"):
        self.text = text
        self.note_type = note_type

class PatientData:
    def __init__(self, patient_id: str, age: Optional[int] = None, 
                 tumor_size: Optional[float] = None, tumor_mutational_burden: Optional[float] = None,
                 genomic_alterations: Optional[List[Dict]] = None, biomarkers: Optional[Dict] = None,
                 ultrasound_findings: Optional[Dict] = None, mammography_findings: Optional[Dict] = None,
                 xray_findings: Optional[Dict] = None, clinical_notes: Optional[List[Dict]] = None):
        self.patient_id = patient_id
        self.age = age
        self.tumor_size = tumor_size
        self.tumor_mutational_burden = tumor_mutational_burden
        self.genomic_alterations = genomic_alterations or []
        self.biomarkers = biomarkers or {}
        self.ultrasound_findings = ultrasound_findings
        self.mammography_findings = mammography_findings
        self.xray_findings = xray_findings
        self.clinical_notes = clinical_notes or []
    
    def dict(self):
        """Convert to dictionary for compatibility"""
        return {
            'patient_id': self.patient_id,
            'age': self.age,
            'tumor_size': self.tumor_size,
            'tumor_mutational_burden': self.tumor_mutational_burden,
            'genomic_alterations': self.genomic_alterations,
            'biomarkers': self.biomarkers,
            'ultrasound_findings': self.ultrasound_findings,
            'mammography_findings': self.mammography_findings,
            'xray_findings': self.xray_findings,
            'clinical_notes': self.clinical_notes
        }

class AnalysisResponse:
    def __init__(self, patient_id: str, analysis_timestamp: str,
                 overall_risk_assessment: Dict[str, Any], modality_results: Dict[str, Any],
                 treatment_recommendations: List[str], clinical_guidance: List[str]):
        self.patient_id = patient_id
        self.analysis_timestamp = analysis_timestamp
        self.overall_risk_assessment = overall_risk_assessment
        self.modality_results = modality_results
        self.treatment_recommendations = treatment_recommendations
        self.clinical_guidance = clinical_guidance

# For FastAPI compatibility, create simple Pydantic models when needed
try:
    from pydantic import BaseModel
    
    class PatientDataAPI(BaseModel):
        patient_id: str
        age: Optional[int] = None
        tumor_size: Optional[float] = None
        tumor_mutational_burden: Optional[float] = None
        genomic_alterations: Optional[List[Dict[str, Any]]] = []
        biomarkers: Optional[Dict[str, str]] = {}
        ultrasound_findings: Optional[Dict[str, Any]] = None
        mammography_findings: Optional[Dict[str, Any]] = None
        xray_findings: Optional[Dict[str, Any]] = None
        clinical_notes: Optional[List[Dict[str, str]]] = []
    
    class AnalysisResponseAPI(BaseModel):
        patient_id: str
        analysis_timestamp: str
        overall_risk_assessment: Dict[str, Any]
        modality_results: Dict[str, Any]
        treatment_recommendations: List[str]
        clinical_guidance: List[str]
    
    # Use Pydantic models for API
    PatientData = PatientDataAPI
    AnalysisResponse = AnalysisResponseAPI
    
except ImportError:
    # Fallback to simple classes if Pydantic not available
    pass