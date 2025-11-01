import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm, useFieldArray } from 'react-hook-form';
import toast from 'react-hot-toast';
import { 
  User, 
  Dna, 
  Scan, 
  FileText, 
  Plus, 
  Trash2, 
  Brain,
  AlertCircle,
  CheckCircle,
  Loader
} from 'lucide-react';
import { useAnalysis } from '../context/AnalysisContext';

const PatientAnalysis = () => {
  const navigate = useNavigate();
  const { performAnalysis, backendHealth, availableModalities } = useAnalysis();
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [activeTab, setActiveTab] = useState('patient-info');

  const { register, control, handleSubmit, watch, formState: { errors } } = useForm({
    defaultValues: {
      patientId: `PATIENT_${Date.now()}`,
      genomicAlterations: [{ gene: '', mutation: '', alleleFrequency: '' }],
      clinicalNotes: [{ text: '', noteType: 'clinical_note' }]
    }
  });

  const { fields: genomicFields, append: appendGenomic, remove: removeGenomic } = useFieldArray({
    control,
    name: 'genomicAlterations'
  });

  const { fields: notesFields, append: appendNote, remove: removeNote } = useFieldArray({
    control,
    name: 'clinicalNotes'
  });

  const tabs = [
    { id: 'patient-info', label: 'Patient Info', icon: User },
    { id: 'genomics', label: 'Genomics', icon: Dna },
    { id: 'imaging', label: 'Imaging', icon: Scan },
    { id: 'clinical', label: 'Clinical Notes', icon: FileText },
  ];

  const onSubmit = async (data) => {
    if (!backendHealth.isHealthy) {
      toast.error('AI system is offline. Please check connection.');
      return;
    }

    setIsAnalyzing(true);
    
    try {
      const result = await performAnalysis(data);
      
      if (result.success) {
        toast.success('Analysis completed successfully!');
        navigate(`/results/${result.data.patient_id}`);
      } else {
        toast.error(result.error || 'Analysis failed');
      }
    } catch (error) {
      toast.error('Analysis failed: ' + error.message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const renderPatientInfo = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-medical-700 mb-2">
            Patient ID *
          </label>
          <input
            {...register('patientId', { required: 'Patient ID is required' })}
            className="input-field"
            placeholder="Enter patient ID"
          />
          {errors.patientId && (
            <p className="text-red-600 text-sm mt-1">{errors.patientId.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-medical-700 mb-2">
            Age
          </label>
          <input
            {...register('age', { 
              min: { value: 0, message: 'Age must be positive' },
              max: { value: 120, message: 'Age must be realistic' }
            })}
            type="number"
            className="input-field"
            placeholder="Enter age"
          />
          {errors.age && (
            <p className="text-red-600 text-sm mt-1">{errors.age.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-medical-700 mb-2">
            Tumor Size (cm)
          </label>
          <input
            {...register('tumorSize', { 
              min: { value: 0, message: 'Size must be positive' }
            })}
            type="number"
            step="0.1"
            className="input-field"
            placeholder="Enter tumor size"
          />
          {errors.tumorSize && (
            <p className="text-red-600 text-sm mt-1">{errors.tumorSize.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-medical-700 mb-2">
            Tumor Mutational Burden
          </label>
          <input
            {...register('tumorMutationalBurden', { 
              min: { value: 0, message: 'TMB must be positive' }
            })}
            type="number"
            step="0.1"
            className="input-field"
            placeholder="Enter TMB value"
          />
          {errors.tumorMutationalBurden && (
            <p className="text-red-600 text-sm mt-1">{errors.tumorMutationalBurden.message}</p>
          )}
        </div>
      </div>

      {/* Biomarkers */}
      <div>
        <h3 className="text-lg font-medium text-medical-900 mb-4">Biomarkers</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {['erStatus', 'prStatus', 'her2Status', 'brcaStatus'].map((marker) => (
            <div key={marker}>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                {marker.replace('Status', '').toUpperCase()} Status
              </label>
              <select {...register(`biomarkers.${marker}`)} className="input-field">
                <option value="">Select status</option>
                <option value="Positive">Positive</option>
                <option value="Negative">Negative</option>
                <option value="Unknown">Unknown</option>
              </select>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderGenomics = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-medical-900">Genomic Alterations</h3>
        <button
          type="button"
          onClick={() => appendGenomic({ gene: '', mutation: '', alleleFrequency: '' })}
          className="btn-secondary flex items-center space-x-2"
        >
          <Plus className="w-4 h-4" />
          <span>Add Alteration</span>
        </button>
      </div>

      {genomicFields.map((field, index) => (
        <div key={field.id} className="card bg-medical-50">
          <div className="flex items-center justify-between mb-4">
            <h4 className="font-medium text-medical-900">Alteration {index + 1}</h4>
            {genomicFields.length > 1 && (
              <button
                type="button"
                onClick={() => removeGenomic(index)}
                className="text-red-600 hover:text-red-700"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                Gene
              </label>
              <input
                {...register(`genomicAlterations.${index}.gene`)}
                className="input-field"
                placeholder="e.g., BRCA1"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                Mutation Type
              </label>
              <select {...register(`genomicAlterations.${index}.mutation`)} className="input-field">
                <option value="">Select mutation</option>
                <option value="Pathogenic">Pathogenic</option>
                <option value="Likely_pathogenic">Likely Pathogenic</option>
                <option value="VUS">VUS (Uncertain Significance)</option>
                <option value="Likely_benign">Likely Benign</option>
                <option value="Benign">Benign</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                Allele Frequency
              </label>
              <input
                {...register(`genomicAlterations.${index}.alleleFrequency`)}
                type="number"
                step="0.01"
                min="0"
                max="1"
                className="input-field"
                placeholder="0.0 - 1.0"
              />
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  const renderImaging = () => (
    <div className="space-y-8">
      {/* Ultrasound Findings */}
      <div>
        <h3 className="text-lg font-medium text-medical-900 mb-4">Ultrasound Findings</h3>
        <div className="card bg-medical-50">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="flex items-center space-x-2">
              <input
                {...register('ultrasoundFindings.massPresent')}
                type="checkbox"
                className="rounded border-medical-300"
              />
              <label className="text-sm font-medium text-medical-700">
                Mass Present
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                Mass Size (cm)
              </label>
              <input
                {...register('ultrasoundFindings.massSize')}
                type="number"
                step="0.1"
                className="input-field"
                placeholder="Size in cm"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                BI-RADS Score
              </label>
              <select {...register('ultrasoundFindings.biradesScore')} className="input-field">
                <option value="">Select BI-RADS</option>
                <option value="1">1 - Negative</option>
                <option value="2">2 - Benign</option>
                <option value="3">3 - Probably Benign</option>
                <option value="4">4 - Suspicious</option>
                <option value="5">5 - Highly Suspicious</option>
              </select>
            </div>

            <div className="flex items-center space-x-2">
              <input
                {...register('ultrasoundFindings.massShapeIrregular')}
                type="checkbox"
                className="rounded border-medical-300"
              />
              <label className="text-sm font-medium text-medical-700">
                Irregular Shape
              </label>
            </div>

            <div className="flex items-center space-x-2">
              <input
                {...register('ultrasoundFindings.massMargins')}
                type="checkbox"
                className="rounded border-medical-300"
              />
              <label className="text-sm font-medium text-medical-700">
                Irregular Margins
              </label>
            </div>

            <div className="flex items-center space-x-2">
              <input
                {...register('ultrasoundFindings.calcifications')}
                type="checkbox"
                className="rounded border-medical-300"
              />
              <label className="text-sm font-medium text-medical-700">
                Calcifications
              </label>
            </div>
          </div>
        </div>
      </div>

      {/* Mammography Findings */}
      <div>
        <h3 className="text-lg font-medium text-medical-900 mb-4">Mammography Findings</h3>
        <div className="card bg-medical-50">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="flex items-center space-x-2">
              <input
                {...register('mammographyFindings.massPresent')}
                type="checkbox"
                className="rounded border-medical-300"
              />
              <label className="text-sm font-medium text-medical-700">
                Mass Present
              </label>
            </div>

            <div className="flex items-center space-x-2">
              <input
                {...register('mammographyFindings.calcifications')}
                type="checkbox"
                className="rounded border-medical-300"
              />
              <label className="text-sm font-medium text-medical-700">
                Calcifications
              </label>
            </div>

            <div className="flex items-center space-x-2">
              <input
                {...register('mammographyFindings.architecturalDistortion')}
                type="checkbox"
                className="rounded border-medical-300"
              />
              <label className="text-sm font-medium text-medical-700">
                Architectural Distortion
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                BI-RADS Score
              </label>
              <select {...register('mammographyFindings.biradesScore')} className="input-field">
                <option value="">Select BI-RADS</option>
                <option value="1">1 - Negative</option>
                <option value="2">2 - Benign</option>
                <option value="3">3 - Probably Benign</option>
                <option value="4">4 - Suspicious</option>
                <option value="5">5 - Highly Suspicious</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                Breast Density
              </label>
              <select {...register('mammographyFindings.breastDensity')} className="input-field">
                <option value="">Select density</option>
                <option value="1">A - Almost entirely fatty</option>
                <option value="2">B - Scattered fibroglandular</option>
                <option value="3">C - Heterogeneously dense</option>
                <option value="4">D - Extremely dense</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* X-ray Findings */}
      <div>
        <h3 className="text-lg font-medium text-medical-900 mb-4">Chest X-ray Findings</h3>
        <div className="card bg-medical-50">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="flex items-center space-x-2">
              <input
                {...register('xrayFindings.lungMetastasis')}
                type="checkbox"
                className="rounded border-medical-300"
              />
              <label className="text-sm font-medium text-medical-700">
                Lung Metastasis
              </label>
            </div>

            <div className="flex items-center space-x-2">
              <input
                {...register('xrayFindings.pleuralEffusion')}
                type="checkbox"
                className="rounded border-medical-300"
              />
              <label className="text-sm font-medium text-medical-700">
                Pleural Effusion
              </label>
            </div>

            <div className="flex items-center space-x-2">
              <input
                {...register('xrayFindings.lymphadenopathy')}
                type="checkbox"
                className="rounded border-medical-300"
              />
              <label className="text-sm font-medium text-medical-700">
                Lymphadenopathy
              </label>
            </div>

            <div className="flex items-center space-x-2">
              <input
                {...register('xrayFindings.boneMetastasis')}
                type="checkbox"
                className="rounded border-medical-300"
              />
              <label className="text-sm font-medium text-medical-700">
                Bone Metastasis
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                Cancer Stage
              </label>
              <select {...register('xrayFindings.cancerStage')} className="input-field">
                <option value="">Select stage</option>
                <option value="1">Stage I</option>
                <option value="2">Stage II</option>
                <option value="3">Stage III</option>
                <option value="4">Stage IV</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderClinical = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-medical-900">Clinical Notes</h3>
        <button
          type="button"
          onClick={() => appendNote({ text: '', noteType: 'clinical_note' })}
          className="btn-secondary flex items-center space-x-2"
        >
          <Plus className="w-4 h-4" />
          <span>Add Note</span>
        </button>
      </div>

      {notesFields.map((field, index) => (
        <div key={field.id} className="card bg-medical-50">
          <div className="flex items-center justify-between mb-4">
            <h4 className="font-medium text-medical-900">Note {index + 1}</h4>
            {notesFields.length > 1 && (
              <button
                type="button"
                onClick={() => removeNote(index)}
                className="text-red-600 hover:text-red-700"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                Note Type
              </label>
              <select {...register(`clinicalNotes.${index}.noteType`)} className="input-field">
                <option value="clinical_note">Clinical Note</option>
                <option value="pathology_report">Pathology Report</option>
                <option value="radiology_report">Radiology Report</option>
                <option value="consultation_note">Consultation Note</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                Clinical Text
              </label>
              <textarea
                {...register(`clinicalNotes.${index}.text`)}
                rows={4}
                className="input-field"
                placeholder="Enter clinical notes, symptoms, observations..."
              />
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-medical-900">
            New Patient Analysis
          </h1>
          <p className="text-medical-600 mt-2">
            Multi-modal breast cancer AI analysis
          </p>
        </div>

        {/* System Status */}
        <div className="flex items-center space-x-3">
          {backendHealth.isHealthy ? (
            <div className="flex items-center space-x-2 text-green-600">
              <CheckCircle className="w-5 h-5" />
              <span className="text-sm font-medium">AI System Ready</span>
            </div>
          ) : (
            <div className="flex items-center space-x-2 text-red-600">
              <AlertCircle className="w-5 h-5" />
              <span className="text-sm font-medium">AI System Offline</span>
            </div>
          )}
        </div>
      </div>

      {/* System Offline Warning */}
      {!backendHealth.isHealthy && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <div>
              <h3 className="font-medium text-red-800">AI System Unavailable</h3>
              <p className="text-red-600 text-sm mt-1">
                The backend AI system is not responding. Analysis cannot be performed until the connection is restored.
              </p>
            </div>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {/* Tab Navigation */}
        <div className="border-b border-medical-200">
          <nav className="flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-medical-500 hover:text-medical-700 hover:border-medical-300'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="min-h-96">
          {activeTab === 'patient-info' && renderPatientInfo()}
          {activeTab === 'genomics' && renderGenomics()}
          {activeTab === 'imaging' && renderImaging()}
          {activeTab === 'clinical' && renderClinical()}
        </div>

        {/* Submit Button */}
        <div className="flex items-center justify-between pt-6 border-t border-medical-200">
          <div className="text-sm text-medical-600">
            Available modalities: {availableModalities.join(', ') || 'None'}
          </div>
          
          <button
            type="submit"
            disabled={isAnalyzing || !backendHealth.isHealthy}
            className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Brain className="w-5 h-5" />
                <span>Start AI Analysis</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PatientAnalysis;