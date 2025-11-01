import React, { useState, useEffect } from 'react';
import { apiUtils } from '../services/api';

const ApiTest = () => {
  const [testResults, setTestResults] = useState({
    health: null,
    modalities: null,
    analysis: null
  });
  const [isLoading, setIsLoading] = useState(false);

  const runTests = async () => {
    setIsLoading(true);
    const results = {};

    // Test health check
    try {
      const healthResult = await apiUtils.checkBackendHealth();
      results.health = healthResult;
    } catch (error) {
      results.health = { isHealthy: false, error: error.message };
    }

    // Test modalities
    try {
      const modalitiesResult = await apiUtils.getAvailableModalities();
      results.modalities = modalitiesResult;
    } catch (error) {
      results.modalities = { success: false, error: error.message };
    }

    // Test analysis
    try {
      const sampleData = {
        patientId: 'FRONTEND_TEST_001',
        age: 45,
        genomicAlterations: [
          { gene: 'BRCA1', mutation: 'Pathogenic', alleleFrequency: 0.8 }
        ],
        biomarkers: {
          erStatus: 'Positive',
          her2Status: 'Negative'
        }
      };

      const analysisResult = await apiUtils.performComprehensiveAnalysis(
        apiUtils.formatPatientData(sampleData)
      );
      results.analysis = analysisResult;
    } catch (error) {
      results.analysis = { success: false, error: error.message };
    }

    setTestResults(results);
    setIsLoading(false);
  };

  useEffect(() => {
    runTests();
  }, []);

  const getStatusIcon = (success) => {
    return success ? '✅' : '❌';
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="card">
        <h2 className="text-2xl font-bold text-medical-900 mb-6">
          Frontend-Backend API Test
        </h2>

        <div className="space-y-6">
          {/* Health Check */}
          <div className="border border-medical-200 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-medical-900 mb-3">
              {getStatusIcon(testResults.health?.isHealthy)} Health Check
            </h3>
            {isLoading ? (
              <div className="text-medical-600">Testing...</div>
            ) : testResults.health ? (
              <div className="space-y-2">
                <div>Status: {testResults.health.isHealthy ? 'Healthy' : 'Unhealthy'}</div>
                {testResults.health.data && (
                  <div>Available Modalities: {testResults.health.data.available_modalities?.join(', ')}</div>
                )}
                {testResults.health.error && (
                  <div className="text-red-600">Error: {testResults.health.error}</div>
                )}
              </div>
            ) : (
              <div>No results</div>
            )}
          </div>

          {/* Modalities Check */}
          <div className="border border-medical-200 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-medical-900 mb-3">
              {getStatusIcon(testResults.modalities?.success)} Available Modalities
            </h3>
            {isLoading ? (
              <div className="text-medical-600">Testing...</div>
            ) : testResults.modalities ? (
              <div className="space-y-2">
                {testResults.modalities.success ? (
                  <div>Modalities: {testResults.modalities.modalities?.join(', ')}</div>
                ) : (
                  <div className="text-red-600">Error: {testResults.modalities.error}</div>
                )}
              </div>
            ) : (
              <div>No results</div>
            )}
          </div>

          {/* Analysis Test */}
          <div className="border border-medical-200 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-medical-900 mb-3">
              {getStatusIcon(testResults.analysis?.success)} Sample Analysis
            </h3>
            {isLoading ? (
              <div className="text-medical-600">Testing...</div>
            ) : testResults.analysis ? (
              <div className="space-y-2">
                {testResults.analysis.success ? (
                  <div>
                    <div>Patient ID: {testResults.analysis.data?.patient_id}</div>
                    <div>Risk Score: {testResults.analysis.data?.overall_risk_assessment?.overall_risk}</div>
                    <div>Modalities Used: {testResults.analysis.data?.modalities_used?.join(', ')}</div>
                  </div>
                ) : (
                  <div className="text-red-600">Error: {testResults.analysis.error}</div>
                )}
              </div>
            ) : (
              <div>No results</div>
            )}
          </div>
        </div>

        <div className="mt-6 flex justify-center">
          <button
            onClick={runTests}
            disabled={isLoading}
            className="btn-primary disabled:opacity-50"
          >
            {isLoading ? 'Testing...' : 'Run Tests Again'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ApiTest;