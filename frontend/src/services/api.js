import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`Response from ${response.config.url}:`, response.status);
    return response;
  },
  (error) => {
    console.error('Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API endpoints
export const apiEndpoints = {
  // Health check
  healthCheck: () => api.get('/health'),
  
  // Analysis endpoints
  comprehensiveAnalysis: (patientData) => 
    api.post('/analyze/comprehensive', patientData),
  
  genomicsAnalysis: (patientData) => 
    api.post('/analyze/genomics', patientData),
  
  imagingAnalysis: (patientData) => 
    api.post('/analyze/imaging', patientData),
  
  clinicalTextAnalysis: (patientData) => 
    api.post('/analyze/clinical-text', patientData),
  
  // Model information
  getAvailableModels: () => api.get('/models/available'),
};

// Utility functions for API calls
export const apiUtils = {
  // Check if backend is available
  async checkBackendHealth() {
    try {
      const response = await apiEndpoints.healthCheck();
      return {
        isHealthy: response.data.status === 'healthy',
        data: response.data
      };
    } catch (error) {
      return {
        isHealthy: false,
        error: error.message
      };
    }
  },

  // Get available analysis modalities
  async getAvailableModalities() {
    try {
      const response = await apiEndpoints.getAvailableModels();
      return {
        success: true,
        modalities: response.data.available_modalities || [],
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  },

  // Perform comprehensive analysis
  async performComprehensiveAnalysis(patientData) {
    try {
      const response = await apiEndpoints.comprehensiveAnalysis(patientData);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message
      };
    }
  },

  // Perform individual modality analysis
  async performModalityAnalysis(modality, patientData) {
    try {
      let response;
      switch (modality) {
        case 'genomics':
          response = await apiEndpoints.genomicsAnalysis(patientData);
          break;
        case 'imaging':
          response = await apiEndpoints.imagingAnalysis(patientData);
          break;
        case 'clinical-text':
          response = await apiEndpoints.clinicalTextAnalysis(patientData);
          break;
        default:
          throw new Error(`Unknown modality: ${modality}`);
      }
      
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message
      };
    }
  },

  // Format patient data for API
  formatPatientData(formData) {
    const patientData = {
      patient_id: formData.patientId || `PATIENT_${Date.now()}`,
      age: formData.age ? parseInt(formData.age) : null,
      tumor_size: formData.tumorSize ? parseFloat(formData.tumorSize) : null,
      tumor_mutational_burden: formData.tumorMutationalBurden ? 
        parseFloat(formData.tumorMutationalBurden) : null,
    };

    // Add genomic data
    if (formData.genomicAlterations && formData.genomicAlterations.length > 0) {
      patientData.genomic_alterations = formData.genomicAlterations.map(alt => ({
        gene: alt.gene,
        mutation: alt.mutation,
        allele_frequency: alt.alleleFrequency ? parseFloat(alt.alleleFrequency) : null
      }));
    }

    // Add biomarkers
    if (formData.biomarkers) {
      patientData.biomarkers = {
        ER_status: formData.biomarkers.erStatus || null,
        PR_status: formData.biomarkers.prStatus || null,
        HER2_status: formData.biomarkers.her2Status || null,
        BRCA_status: formData.biomarkers.brcaStatus || null,
      };
    }

    // Add ultrasound findings
    if (formData.ultrasoundFindings) {
      patientData.ultrasound_findings = {
        mass_present: formData.ultrasoundFindings.massPresent ? 1 : 0,
        mass_size: formData.ultrasoundFindings.massSize ? 
          parseFloat(formData.ultrasoundFindings.massSize) : 0,
        mass_shape_irregular: formData.ultrasoundFindings.massShapeIrregular ? 1 : 0,
        mass_margins: formData.ultrasoundFindings.massMargins ? 1 : 0,
        echo_pattern: formData.ultrasoundFindings.echoPattern ? 1 : 0,
        calcifications: formData.ultrasoundFindings.calcifications ? 1 : 0,
        birads_score: formData.ultrasoundFindings.biradesScore ? 
          parseInt(formData.ultrasoundFindings.biradesScore) : 2,
      };
    }

    // Add mammography findings
    if (formData.mammographyFindings) {
      patientData.mammography_findings = {
        mass_present: formData.mammographyFindings.massPresent ? 1 : 0,
        calcifications: formData.mammographyFindings.calcifications ? 1 : 0,
        architectural_distortion: formData.mammographyFindings.architecturalDistortion ? 1 : 0,
        asymmetry: formData.mammographyFindings.asymmetry ? 1 : 0,
        skin_thickening: formData.mammographyFindings.skinThickening ? 1 : 0,
        birads_score: formData.mammographyFindings.biradesScore ? 
          parseInt(formData.mammographyFindings.biradesScore) : 2,
        breast_density: formData.mammographyFindings.breastDensity ? 
          parseInt(formData.mammographyFindings.breastDensity) : 2,
      };
    }

    // Add X-ray findings
    if (formData.xrayFindings) {
      patientData.xray_findings = {
        lung_metastasis: formData.xrayFindings.lungMetastasis ? 1 : 0,
        pleural_effusion: formData.xrayFindings.pleuralEffusion ? 1 : 0,
        lymphadenopathy: formData.xrayFindings.lymphadenopathy ? 1 : 0,
        bone_metastasis: formData.xrayFindings.boneMetastasis ? 1 : 0,
        cancer_stage: formData.xrayFindings.cancerStage ? 
          parseInt(formData.xrayFindings.cancerStage) : 1,
      };
    }

    // Add clinical notes
    if (formData.clinicalNotes && formData.clinicalNotes.length > 0) {
      patientData.clinical_notes = formData.clinicalNotes.map(note => ({
        text: note.text,
        note_type: note.noteType || 'clinical_note'
      }));
    }

    return patientData;
  }
};

export default api;