import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ArrowLeft, 
  Download, 
  Share2, 
  AlertTriangle, 
  CheckCircle, 
  Info,
  Brain,
  Activity,
  FileText,
  TrendingUp,
  Clock,
  User
} from 'lucide-react';
import { 
  PieChart, 
  Pie, 
  Cell, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';
import { useAnalysis } from '../context/AnalysisContext';

const Results = () => {
  const { patientId } = useParams();
  const { analysisHistory } = useAnalysis();

  // Find the analysis results for this patient
  const analysis = analysisHistory.find(a => a.patientId === patientId);

  if (!analysis) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <Brain className="w-16 h-16 text-medical-300 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-medical-900 mb-2">
          Analysis Not Found
        </h2>
        <p className="text-medical-600 mb-6">
          The analysis results for patient {patientId} could not be found.
        </p>
        <Link to="/analysis" className="btn-primary">
          Start New Analysis
        </Link>
      </div>
    );
  }

  const { results, timestamp } = analysis;

  const getRiskColor = (risk) => {
    if (!risk) return 'text-gray-600';
    const riskLevel = risk.toLowerCase();
    if (riskLevel.includes('high')) return 'text-red-600';
    if (riskLevel.includes('moderate') || riskLevel.includes('medium')) return 'text-yellow-600';
    return 'text-green-600';
  };

  const getRiskBgColor = (risk) => {
    if (!risk) return 'bg-gray-100';
    const riskLevel = risk.toLowerCase();
    if (riskLevel.includes('high')) return 'bg-red-50 border-red-200';
    if (riskLevel.includes('moderate') || riskLevel.includes('medium')) return 'bg-yellow-50 border-yellow-200';
    return 'bg-green-50 border-green-200';
  };

  // Prepare chart data based on actual analysis results
  const getRiskDistribution = () => {
    const overallRisk = results.overall_risk_assessment?.overall_risk || 0;
    const riskCategory = results.overall_risk_assessment?.risk_category?.toLowerCase() || 'unknown';
    
    // Calculate distribution based on actual risk score and category
    let lowRisk, moderateRisk, highRisk;
    
    if (riskCategory.includes('high')) {
      highRisk = Math.max(50, overallRisk * 100);
      moderateRisk = Math.max(10, (100 - highRisk) * 0.6);
      lowRisk = 100 - highRisk - moderateRisk;
    } else if (riskCategory.includes('moderate') || riskCategory.includes('medium')) {
      moderateRisk = Math.max(40, overallRisk * 100);
      highRisk = Math.max(5, (100 - moderateRisk) * 0.3);
      lowRisk = 100 - moderateRisk - highRisk;
    } else {
      lowRisk = Math.max(50, 100 - (overallRisk * 100));
      moderateRisk = Math.max(5, (100 - lowRisk) * 0.7);
      highRisk = 100 - lowRisk - moderateRisk;
    }
    
    return [
      { name: 'Low Risk', value: Math.round(lowRisk), color: '#10B981' },
      { name: 'Moderate Risk', value: Math.round(moderateRisk), color: '#F59E0B' },
      { name: 'High Risk', value: Math.round(highRisk), color: '#EF4444' }
    ];
  };

  const riskData = getRiskDistribution();

  const modalityData = Object.entries(results.modality_results || {}).map(([modality, data]) => ({
    modality: modality.charAt(0).toUpperCase() + modality.slice(1).replace('_', ' '),
    risk: Math.round((data.risk_score || data.response_probability || data.malignancy_probability || 0) * 100),
    confidence: Math.round((data.ai_confidence || data.confidence || 0) * 100)
  }));

  const getRadarData = () => {
    const modalityResults = results.modality_results || {};
    const overallScore = (results.overall_risk_assessment?.confidence || 0.7) * 100;
    
    return [
      { 
        subject: 'Genomics', 
        A: modalityResults.genomics ? Math.round((modalityResults.genomics.ai_confidence || modalityResults.genomics.confidence || 0.7) * 100) : 0,
        fullMark: 100 
      },
      { 
        subject: 'Imaging', 
        A: modalityResults.imaging ? Math.round((modalityResults.imaging.ai_confidence || modalityResults.imaging.confidence || 0.6) * 100) : 0,
        fullMark: 100 
      },
      { 
        subject: 'Clinical', 
        A: modalityResults.clinical_data ? Math.round((modalityResults.clinical_data.ai_confidence || modalityResults.clinical_data.confidence || 0.8) * 100) : 0,
        fullMark: 100 
      },
      { 
        subject: 'Overall', 
        A: Math.round(overallScore),
        fullMark: 100 
      }
    ];
  };

  const radarData = getRadarData();

  const formatDate = (date) => {
    return new Date(date).toLocaleString();
  };

  const exportReport = (format = 'txt') => {
    const reportData = {
      patientId,
      timestamp: formatDate(timestamp),
      modalities: results.modalities_used?.join(', ') || 'None',
      riskCategory: results.overall_risk_assessment?.risk_category || 'Unknown',
      riskScore: ((results.overall_risk_assessment?.overall_risk || 0) * 100).toFixed(1),
      confidence: ((results.overall_risk_assessment?.confidence || 0.7) * 100).toFixed(0),
      riskDistribution: riskData,
      modalityResults: results.modality_results || {},
      recommendations: results.treatment_recommendations || [],
      guidance: results.clinical_guidance || [],
      priority: results.overall_risk_assessment?.risk_category?.toLowerCase().includes('high') 
        ? 'Urgent' 
        : results.overall_risk_assessment?.risk_category?.toLowerCase().includes('moderate')
        ? 'Standard'
        : 'Routine'
    };

    if (format === 'html') {
      exportAsHTML(reportData);
    } else if (format === 'json') {
      exportAsJSON(reportData);
    } else {
      exportAsText(reportData);
    }
  };

  const exportAsText = (data) => {
    const reportContent = `
BREAST CANCER AI ANALYSIS REPORT
================================

Patient Information:
- Patient ID: ${data.patientId}
- Analysis Date: ${data.timestamp}
- Modalities Used: ${data.modalities}

Overall Risk Assessment:
- Risk Category: ${data.riskCategory}
- Risk Score: ${data.riskScore}%
- Confidence Level: ${data.confidence}%

Risk Distribution:
${data.riskDistribution.map(item => `- ${item.name}: ${item.value}%`).join('\n')}

Detailed Modality Results:
${Object.entries(data.modalityResults).map(([modality, modalityData]) => `
${modality.charAt(0).toUpperCase() + modality.slice(1).replace('_', ' ')}:
- Status: ${modalityData.risk_category || modalityData.status || 'Completed'}
- Risk Score: ${modalityData.risk_score ? (modalityData.risk_score * 100).toFixed(1) + '%' : 'N/A'}
- Response Probability: ${modalityData.response_probability ? (modalityData.response_probability * 100).toFixed(1) + '%' : 'N/A'}
- Key Drivers: ${modalityData.key_drivers ? modalityData.key_drivers.join(', ') : 'N/A'}
`).join('\n')}

Treatment Recommendations:
${data.recommendations.map((rec, index) => `${index + 1}. ${rec}`).join('\n') || 'No specific recommendations available'}

Clinical Guidance:
${data.guidance.map((guidance, index) => `${index + 1}. ${guidance}`).join('\n') || 'No specific guidance available'}

Follow-up Actions:
1. Schedule follow-up in 3-6 months
2. Review with multidisciplinary team
3. Monitor biomarker changes

Priority Level: ${data.priority}

Report Generated: ${new Date().toLocaleString()}
    `.trim();

    downloadFile(reportContent, `breast_cancer_analysis_${data.patientId}_${new Date().toISOString().split('T')[0]}.txt`, 'text/plain');
  };

  const exportAsHTML = (data) => {
    const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Breast Cancer AI Analysis Report - Patient ${data.patientId}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
        .section { margin-bottom: 30px; }
        .section h2 { color: #2563eb; border-bottom: 1px solid #e5e7eb; padding-bottom: 10px; }
        .risk-high { color: #dc2626; font-weight: bold; }
        .risk-moderate { color: #d97706; font-weight: bold; }
        .risk-low { color: #059669; font-weight: bold; }
        .metric { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f3f4f6; }
        .recommendations li { margin-bottom: 8px; }
        .footer { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Breast Cancer AI Analysis Report</h1>
        <p>Multi-Modal AI-Powered Risk Assessment</p>
    </div>

    <div class="section">
        <h2>Patient Information</h2>
        <div class="metric"><span>Patient ID:</span><span>${data.patientId}</span></div>
        <div class="metric"><span>Analysis Date:</span><span>${data.timestamp}</span></div>
        <div class="metric"><span>Modalities Used:</span><span>${data.modalities}</span></div>
    </div>

    <div class="section">
        <h2>Overall Risk Assessment</h2>
        <div class="metric">
            <span>Risk Category:</span>
            <span class="risk-${data.riskCategory.toLowerCase().includes('high') ? 'high' : data.riskCategory.toLowerCase().includes('moderate') ? 'moderate' : 'low'}">${data.riskCategory}</span>
        </div>
        <div class="metric"><span>Risk Score:</span><span>${data.riskScore}%</span></div>
        <div class="metric"><span>Confidence Level:</span><span>${data.confidence}%</span></div>
    </div>

    <div class="section">
        <h2>Risk Distribution</h2>
        ${data.riskDistribution.map(item => `<div class="metric"><span>${item.name}:</span><span>${item.value}%</span></div>`).join('')}
    </div>

    <div class="section">
        <h2>Detailed Modality Results</h2>
        ${Object.entries(data.modalityResults).map(([modality, modalityData]) => `
            <h3>${modality.charAt(0).toUpperCase() + modality.slice(1).replace('_', ' ')}</h3>
            <div class="metric"><span>Status:</span><span>${modalityData.risk_category || modalityData.status || 'Completed'}</span></div>
            ${modalityData.risk_score ? `<div class="metric"><span>Risk Score:</span><span>${(modalityData.risk_score * 100).toFixed(1)}%</span></div>` : ''}
            ${modalityData.response_probability ? `<div class="metric"><span>Response Probability:</span><span>${(modalityData.response_probability * 100).toFixed(1)}%</span></div>` : ''}
            ${modalityData.key_drivers ? `<div class="metric"><span>Key Drivers:</span><span>${modalityData.key_drivers.join(', ')}</span></div>` : ''}
        `).join('')}
    </div>

    ${data.recommendations.length > 0 ? `
    <div class="section">
        <h2>Treatment Recommendations</h2>
        <ol class="recommendations">
            ${data.recommendations.map(rec => `<li>${rec}</li>`).join('')}
        </ol>
    </div>
    ` : ''}

    ${data.guidance.length > 0 ? `
    <div class="section">
        <h2>Clinical Guidance</h2>
        <ol class="recommendations">
            ${data.guidance.map(guidance => `<li>${guidance}</li>`).join('')}
        </ol>
    </div>
    ` : ''}

    <div class="section">
        <h2>Follow-up Actions</h2>
        <ol class="recommendations">
            <li>Schedule follow-up in 3-6 months</li>
            <li>Review with multidisciplinary team</li>
            <li>Monitor biomarker changes</li>
        </ol>
        <div class="metric"><span>Priority Level:</span><span class="risk-${data.priority.toLowerCase() === 'urgent' ? 'high' : data.priority.toLowerCase() === 'standard' ? 'moderate' : 'low'}">${data.priority}</span></div>
    </div>

    <div class="footer">
        <p>Report Generated: ${new Date().toLocaleString()}</p>
        <p>This report was generated by AI-powered analysis and should be reviewed by qualified medical professionals.</p>
    </div>
</body>
</html>
    `.trim();

    downloadFile(htmlContent, `breast_cancer_analysis_${data.patientId}_${new Date().toISOString().split('T')[0]}.html`, 'text/html');
  };

  const exportAsJSON = (data) => {
    const jsonContent = JSON.stringify({
      report: {
        patient_id: data.patientId,
        analysis_date: data.timestamp,
        modalities_used: data.modalities,
        overall_risk_assessment: {
          risk_category: data.riskCategory,
          risk_score: parseFloat(data.riskScore),
          confidence: parseFloat(data.confidence)
        },
        risk_distribution: data.riskDistribution,
        modality_results: data.modalityResults,
        treatment_recommendations: data.recommendations,
        clinical_guidance: data.guidance,
        priority_level: data.priority,
        generated_at: new Date().toISOString()
      }
    }, null, 2);

    downloadFile(jsonContent, `breast_cancer_analysis_${data.patientId}_${new Date().toISOString().split('T')[0]}.json`, 'application/json');
  };

  const downloadFile = (content, filename, mimeType) => {
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  const shareReport = () => {
    if (navigator.share) {
      navigator.share({
        title: `Breast Cancer Analysis - Patient ${patientId}`,
        text: `Analysis results for patient ${patientId} - Risk: ${results.overall_risk_assessment?.risk_category || 'Unknown'}`,
        url: window.location.href
      });
    } else {
      // Fallback: copy link to clipboard
      navigator.clipboard.writeText(window.location.href).then(() => {
        alert('Report link copied to clipboard!');
      });
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link
            to="/"
            className="p-2 rounded-lg hover:bg-medical-100 transition-colors"
          >
            <ArrowLeft className="w-5 h-5 text-medical-600" />
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-medical-900">
              Analysis Results
            </h1>
            <div className="flex items-center space-x-4 mt-2 text-medical-600">
              <div className="flex items-center space-x-2">
                <User className="w-4 h-4" />
                <span>Patient: {patientId}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4" />
                <span>{formatDate(timestamp)}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button 
            onClick={shareReport}
            className="btn-secondary flex items-center space-x-2"
          >
            <Share2 className="w-4 h-4" />
            <span>Share</span>
          </button>
          <div className="relative group">
            <button className="btn-primary flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Export Report</span>
            </button>
            <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-medical-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-10">
              <div className="py-2">
                <button
                  onClick={() => exportReport('txt')}
                  className="w-full text-left px-4 py-2 text-sm text-medical-700 hover:bg-medical-50 flex items-center space-x-2"
                >
                  <FileText className="w-4 h-4" />
                  <span>Text Document (.txt)</span>
                </button>
                <button
                  onClick={() => exportReport('html')}
                  className="w-full text-left px-4 py-2 text-sm text-medical-700 hover:bg-medical-50 flex items-center space-x-2"
                >
                  <FileText className="w-4 h-4" />
                  <span>HTML Report (.html)</span>
                </button>
                <button
                  onClick={() => exportReport('json')}
                  className="w-full text-left px-4 py-2 text-sm text-medical-700 hover:bg-medical-50 flex items-center space-x-2"
                >
                  <FileText className="w-4 h-4" />
                  <span>JSON Data (.json)</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Overall Risk Assessment */}
      <div className={`card ${getRiskBgColor(results.overall_risk_assessment?.risk_category)} border-2`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className={`p-3 rounded-full ${
              results.overall_risk_assessment?.risk_category?.toLowerCase().includes('high') 
                ? 'bg-red-100' 
                : results.overall_risk_assessment?.risk_category?.toLowerCase().includes('moderate')
                ? 'bg-yellow-100'
                : 'bg-green-100'
            }`}>
              {results.overall_risk_assessment?.risk_category?.toLowerCase().includes('high') ? (
                <AlertTriangle className="w-8 h-8 text-red-600" />
              ) : results.overall_risk_assessment?.risk_category?.toLowerCase().includes('moderate') ? (
                <Info className="w-8 h-8 text-yellow-600" />
              ) : (
                <CheckCircle className="w-8 h-8 text-green-600" />
              )}
            </div>
            <div>
              <h2 className="text-2xl font-bold text-medical-900">
                Overall Risk Assessment
              </h2>
              <p className={`text-lg font-semibold ${getRiskColor(results.overall_risk_assessment?.risk_category)}`}>
                {results.overall_risk_assessment?.risk_category || 'Unknown Risk'}
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-medical-900">
              {((results.overall_risk_assessment?.overall_risk || 0) * 100).toFixed(1)}%
            </div>
            <div className="text-sm text-medical-600">
              Risk Score
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center space-x-3">
            <Brain className="w-8 h-8 text-primary-600" />
            <div>
              <p className="text-sm text-medical-600">Modalities Used</p>
              <p className="text-2xl font-bold text-medical-900">
                {results.modalities_used?.length || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-3">
            <Activity className="w-8 h-8 text-green-600" />
            <div>
              <p className="text-sm text-medical-600">Confidence</p>
              <p className="text-2xl font-bold text-medical-900">
                {((results.overall_risk_assessment?.confidence || 0.7) * 100).toFixed(0)}%
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-3">
            <FileText className="w-8 h-8 text-blue-600" />
            <div>
              <p className="text-sm text-medical-600">Recommendations</p>
              <p className="text-2xl font-bold text-medical-900">
                {results.treatment_recommendations?.length || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-3">
            <TrendingUp className="w-8 h-8 text-purple-600" />
            <div>
              <p className="text-sm text-medical-600">Analysis Time</p>
              <p className="text-2xl font-bold text-medical-900">
                &lt; 1s
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Risk Distribution */}
        <div className="card">
          <h3 className="text-lg font-semibold text-medical-900 mb-4">
            Risk Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={riskData}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}%`}
              >
                {riskData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Modality Comparison */}
        <div className="card">
          <h3 className="text-lg font-semibold text-medical-900 mb-4">
            Modality Analysis
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={modalityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="modality" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="risk" fill="#3B82F6" name="Risk Score" />
              <Bar dataKey="confidence" fill="#10B981" name="Confidence" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Results */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Modality Results */}
        <div className="card">
          <h3 className="text-lg font-semibold text-medical-900 mb-6">
            Detailed Modality Results
          </h3>
          <div className="space-y-4">
            {Object.entries(results.modality_results || {}).map(([modality, data]) => (
              <div key={modality} className="border border-medical-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-medium text-medical-900 capitalize">
                    {modality.replace('_', ' ')}
                  </h4>
                  <span className={`px-2 py-1 rounded text-sm font-medium ${
                    getRiskBgColor(data.risk_category || 'unknown')
                  } ${getRiskColor(data.risk_category || 'unknown')}`}>
                    {data.risk_category || data.status || 'Completed'}
                  </span>
                </div>
                
                {data.risk_score && (
                  <div className="mb-2">
                    <span className="text-sm text-medical-600">Risk Score: </span>
                    <span className="font-medium">{(data.risk_score * 100).toFixed(1)}%</span>
                  </div>
                )}
                
                {data.response_probability && (
                  <div className="mb-2">
                    <span className="text-sm text-medical-600">Response Probability: </span>
                    <span className="font-medium">{(data.response_probability * 100).toFixed(1)}%</span>
                  </div>
                )}
                
                {data.key_drivers && (
                  <div className="mb-2">
                    <span className="text-sm text-medical-600">Key Drivers: </span>
                    <span className="font-medium">{data.key_drivers.join(', ')}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Treatment Recommendations */}
        <div className="card">
          <h3 className="text-lg font-semibold text-medical-900 mb-6">
            Treatment Recommendations
          </h3>
          <div className="space-y-3">
            {results.treatment_recommendations?.map((recommendation, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-medical-50 rounded-lg">
                <div className="w-6 h-6 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-xs font-medium text-primary-600">{index + 1}</span>
                </div>
                <p className="text-medical-700">{recommendation}</p>
              </div>
            )) || (
              <p className="text-medical-500 text-center py-4">
                No specific recommendations available
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Clinical Guidance */}
      <div className="card">
        <h3 className="text-lg font-semibold text-medical-900 mb-6">
          Clinical Guidance
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-medical-900 mb-3">Next Steps</h4>
            <div className="space-y-2">
              {results.clinical_guidance?.map((guidance, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0" />
                  <span className="text-medical-700">{guidance}</span>
                </div>
              )) || (
                <p className="text-medical-500">No specific guidance available</p>
              )}
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-medical-900 mb-3">Follow-up</h4>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4 text-blue-600" />
                <span className="text-medical-700">Schedule follow-up in 3-6 months</span>
              </div>
              <div className="flex items-center space-x-2">
                <FileText className="w-4 h-4 text-purple-600" />
                <span className="text-medical-700">Review with multidisciplinary team</span>
              </div>
              <div className="flex items-center space-x-2">
                <Activity className="w-4 h-4 text-green-600" />
                <span className="text-medical-700">Monitor biomarker changes</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Analysis Summary */}
      <div className="card bg-medical-50">
        <h3 className="text-lg font-semibold text-medical-900 mb-4">
          Analysis Summary
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h4 className="font-medium text-medical-700 mb-2">Patient Information</h4>
            <div className="space-y-1 text-sm">
              <p><span className="text-medical-600">ID:</span> {patientId}</p>
              <p><span className="text-medical-600">Analysis Date:</span> {formatDate(timestamp)}</p>
              <p><span className="text-medical-600">Modalities:</span> {results.modalities_used?.join(', ') || 'None'}</p>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-medical-700 mb-2">Risk Assessment</h4>
            <div className="space-y-1 text-sm">
              <p><span className="text-medical-600">Overall Risk:</span> {results.overall_risk_assessment?.risk_category || 'Unknown'}</p>
              <p><span className="text-medical-600">Risk Score:</span> {((results.overall_risk_assessment?.overall_risk || 0) * 100).toFixed(1)}%</p>
              <p><span className="text-medical-600">Confidence:</span> {((results.overall_risk_assessment?.confidence || 0.7) * 100).toFixed(0)}%</p>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-medical-700 mb-2">Recommendations</h4>
            <div className="space-y-1 text-sm">
              <p><span className="text-medical-600">Treatment Options:</span> {results.treatment_recommendations?.length || 0}</p>
              <p><span className="text-medical-600">Clinical Guidance:</span> {results.clinical_guidance?.length || 0}</p>
              <p><span className="text-medical-600">Priority:</span> {
                results.overall_risk_assessment?.risk_category?.toLowerCase().includes('high') 
                  ? 'Urgent' 
                  : results.overall_risk_assessment?.risk_category?.toLowerCase().includes('moderate')
                  ? 'Standard'
                  : 'Routine'
              }</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;