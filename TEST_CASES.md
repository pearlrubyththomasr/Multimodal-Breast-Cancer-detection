# Breast Cancer AI Platform - Test Cases

## Test Case 1: High-Risk Imaging Only
**Scenario**: Patient with suspicious ultrasound and mammography findings
**Expected**: Only imaging analysis should run, showing high risk

### Input Data:
```json
{
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
}
```

**Expected Results**:
- Imaging analysis: HIGH risk (>0.7)
- Genomics: Not analyzed
- NLP: Not analyzed

---

## Test Case 2: Moderate Risk Genomics Only
**Scenario**: Patient with BRCA mutations and biomarkers
**Expected**: Only genomics analysis should run

### Input Data:
```json
{
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
}
```

**Expected Results**:
- Genomics analysis: MODERATE-HIGH risk
- Imaging: Not analyzed
- NLP: Not analyzed

---

## Test Case 3: Clinical Text Only
**Scenario**: Patient with detailed clinical notes
**Expected**: Only NLP analysis should run

### Input Data:
```json
{
  "patient_id": "TEST_003_NLP_ONLY",
  "age": 38,
  "clinical_notes": [
    {
      "text": "Patient presents with palpable mass in left breast, family history of breast and ovarian cancer. Mother diagnosed at age 42, maternal grandmother at 55. Patient reports breast tenderness and recent changes in breast texture.",
      "note_type": "clinical_note"
    },
    {
      "text": "Physical examination reveals 2.5cm firm, irregular mass in upper outer quadrant of left breast. No skin changes or nipple discharge observed. Lymph nodes palpable in left axilla.",
      "note_type": "physical_exam"
    }
  ]
}
```

**Expected Results**:
- NLP analysis: Results based on clinical text
- Genomics: Not analyzed
- Imaging: Not analyzed

---

## Test Case 4: Multi-Modal High Risk
**Scenario**: Patient with data across all modalities - high risk case
**Expected**: All three analyses should run, showing high overall risk

### Input Data:
```json
{
  "patient_id": "TEST_004_MULTIMODAL_HIGH",
  "age": 48,
  "tumor_size": 4.2,
  "genomic_alterations": [
    {
      "gene": "BRCA1",
      "mutation": "Pathogenic",
      "allele_frequency": 0.92
    },
    {
      "gene": "BRCA2",
      "mutation": "Pathogenic",
      "allele_frequency": 0.78
    },
    {
      "gene": "TP53",
      "mutation": "Pathogenic",
      "allele_frequency": 0.85
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
  "mammography_findings": {
    "mass_present": 1,
    "calcifications": 1,
    "architectural_distortion": 1,
    "asymmetry": 1,
    "skin_thickening": 1,
    "birads_score": 5,
    "breast_density": 4
  },
  "xray_findings": {
    "lung_metastasis": 1,
    "pleural_effusion": 1,
    "lymphadenopathy": 1,
    "bone_metastasis": 0,
    "cancer_stage": 3
  },
  "clinical_notes": [
    {
      "text": "Advanced breast cancer with multiple concerning features. Patient has strong family history and genetic predisposition. Imaging shows large irregular mass with suspicious characteristics. Metastatic disease suspected based on chest imaging.",
      "note_type": "clinical_note"
    }
  ]
}
```

**Expected Results**:
- All modalities analyzed
- Overall risk: HIGH (>0.8)
- Treatment recommendations: Urgent intervention

---

## Test Case 5: Low Risk Multi-Modal
**Scenario**: Patient with data across modalities but low risk findings
**Expected**: All analyses run, showing low overall risk

### Input Data:
```json
{
  "patient_id": "TEST_005_MULTIMODAL_LOW",
  "age": 35,
  "tumor_size": 0.8,
  "genomic_alterations": [],
  "biomarkers": {
    "ER_status": "Positive",
    "PR_status": "Positive",
    "HER2_status": "Negative",
    "BRCA_status": "Negative"
  },
  "ultrasound_findings": {
    "mass_present": 0,
    "mass_size": 0,
    "mass_shape_irregular": 0,
    "mass_margins": 0,
    "echo_pattern": 0,
    "calcifications": 0,
    "birads_score": 2
  },
  "mammography_findings": {
    "mass_present": 0,
    "calcifications": 0,
    "architectural_distortion": 0,
    "asymmetry": 0,
    "skin_thickening": 0,
    "birads_score": 1,
    "breast_density": 2
  },
  "clinical_notes": [
    {
      "text": "Routine screening mammography. No family history of breast or ovarian cancer. Patient reports no symptoms or concerns. Physical examination normal.",
      "note_type": "screening_note"
    }
  ]
}
```

**Expected Results**:
- All modalities analyzed
- Overall risk: LOW (<0.3)
- Treatment recommendations: Routine screening

---

## Test Case 6: Empty Data
**Scenario**: Patient with minimal/empty data
**Expected**: No analyses should run or minimal analysis with default values

### Input Data:
```json
{
  "patient_id": "TEST_006_EMPTY_DATA",
  "age": 40
}
```

**Expected Results**:
- No modality analyses run
- Minimal risk assessment based on age only

---

## Test Case 7: Imaging with Metastasis
**Scenario**: Patient with metastatic disease on imaging
**Expected**: High risk imaging analysis with metastasis indicators

### Input Data:
```json
{
  "patient_id": "TEST_007_METASTATIC",
  "age": 55,
  "ultrasound_findings": {
    "mass_present": 1,
    "mass_size": 5.1,
    "mass_shape_irregular": 1,
    "mass_margins": 1,
    "echo_pattern": 1,
    "calcifications": 1,
    "birads_score": 5
  },
  "xray_findings": {
    "lung_metastasis": 1,
    "pleural_effusion": 1,
    "lymphadenopathy": 1,
    "bone_metastasis": 1,
    "cancer_stage": 4
  }
}
```

**Expected Results**:
- Imaging analysis: VERY HIGH risk
- Metastasis indicators present
- Stage 4 disease

---

## Test Case 8: BRCA Positive with Family History
**Scenario**: Strong genetic predisposition
**Expected**: High genomics risk score

### Input Data:
```json
{
  "patient_id": "TEST_008_BRCA_POSITIVE",
  "age": 42,
  "genomic_alterations": [
    {
      "gene": "BRCA1",
      "mutation": "Pathogenic",
      "allele_frequency": 0.95
    }
  ],
  "biomarkers": {
    "ER_status": "Negative",
    "PR_status": "Negative",
    "HER2_status": "Negative",
    "BRCA_status": "Positive"
  },
  "clinical_notes": [
    {
      "text": "Strong family history: mother, sister, and maternal grandmother all diagnosed with breast cancer before age 50. Patient is BRCA1 positive. Considering prophylactic measures.",
      "note_type": "genetic_counseling"
    }
  ]
}
```

**Expected Results**:
- Genomics: HIGH risk
- NLP: Family history indicators
- Recommendations: Genetic counseling, enhanced screening

---

## Test Case 9: Borderline BI-RADS 3
**Scenario**: Probably benign findings requiring follow-up
**Expected**: Moderate risk with follow-up recommendations

### Input Data:
```json
{
  "patient_id": "TEST_009_BIRADS_3",
  "age": 44,
  "ultrasound_findings": {
    "mass_present": 1,
    "mass_size": 1.2,
    "mass_shape_irregular": 0,
    "mass_margins": 0,
    "echo_pattern": 0,
    "calcifications": 0,
    "birads_score": 3
  },
  "mammography_findings": {
    "mass_present": 1,
    "calcifications": 0,
    "architectural_distortion": 0,
    "asymmetry": 1,
    "skin_thickening": 0,
    "birads_score": 3,
    "breast_density": 2
  }
}
```

**Expected Results**:
- Imaging: MODERATE risk
- BI-RADS 3 findings
- Recommendations: 6-month follow-up

---

## Test Case 10: Triple Negative Breast Cancer
**Scenario**: Aggressive subtype with poor prognosis markers
**Expected**: High risk across genomics and clinical factors

### Input Data:
```json
{
  "patient_id": "TEST_010_TRIPLE_NEGATIVE",
  "age": 39,
  "tumor_size": 3.8,
  "genomic_alterations": [
    {
      "gene": "TP53",
      "mutation": "Pathogenic",
      "allele_frequency": 0.88
    },
    {
      "gene": "PIK3CA",
      "mutation": "Likely_pathogenic",
      "allele_frequency": 0.72
    }
  ],
  "biomarkers": {
    "ER_status": "Negative",
    "PR_status": "Negative",
    "HER2_status": "Negative",
    "BRCA_status": "Negative"
  },
  "ultrasound_findings": {
    "mass_present": 1,
    "mass_size": 3.8,
    "mass_shape_irregular": 1,
    "mass_margins": 1,
    "echo_pattern": 1,
    "calcifications": 0,
    "birads_score": 4
  },
  "clinical_notes": [
    {
      "text": "Triple negative breast cancer diagnosed on core biopsy. Rapidly growing mass over 3 months. Patient is young with aggressive tumor characteristics. Neoadjuvant chemotherapy planned.",
      "note_type": "oncology_note"
    }
  ]
}
```

**Expected Results**:
- All modalities: HIGH risk
- Triple negative subtype identified
- Recommendations: Aggressive treatment protocol

---

## How to Test

### Using the Web Interface:
1. Go to "New Patient Analysis" 
2. Copy and paste the JSON data into the form fields
3. Submit the analysis
4. Verify the results match expected outcomes

### Using API Directly:
```bash
curl -X POST http://localhost:8000/analyze/comprehensive \
  -H "Content-Type: application/json" \
  -d '[TEST_CASE_JSON]'
```

### Expected Validation Points:
- ✅ Only relevant modalities are analyzed
- ✅ Risk scores are appropriate for the input data
- ✅ Treatment recommendations match risk levels
- ✅ Empty/missing data doesn't trigger false analyses
- ✅ Multi-modal cases show unified risk assessment
- ✅ High-risk cases trigger urgent recommendations
- ✅ Low-risk cases suggest routine follow-up

### Performance Benchmarks:
- Analysis should complete in <5 seconds
- Memory usage should remain stable
- No errors or crashes with any test case
- Consistent results on repeated runs