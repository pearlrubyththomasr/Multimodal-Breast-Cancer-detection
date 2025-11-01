import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Brain, 
  Activity, 
  Users, 
  TrendingUp, 
  Plus, 
  Clock, 
  AlertCircle,
  CheckCircle,
  Zap,
  Shield,
  User
} from 'lucide-react';
import { useAnalysis } from '../context/AnalysisContext';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { 
    backendHealth, 
    availableModalities, 
    analysisHistory, 
    clearHistory 
  } = useAnalysis();
  
  const { user, hasPermission, isDoctor, isNurse, isAdmin } = useAuth();

  const stats = [
    {
      title: 'Total Analyses',
      value: analysisHistory.length,
      icon: Brain,
      color: 'bg-primary-500',
      change: '+12%'
    },
    {
      title: 'Available Modalities',
      value: availableModalities.length,
      icon: Activity,
      color: 'bg-primary-400',
      change: '100%'
    },
    {
      title: 'System Status',
      value: backendHealth.isHealthy ? 'Online' : 'Offline',
      icon: backendHealth.isHealthy ? CheckCircle : AlertCircle,
      color: backendHealth.isHealthy ? 'bg-primary-600' : 'bg-medical-500',
      change: backendHealth.isHealthy ? 'Healthy' : 'Check Connection'
    },
    {
      title: 'Response Time',
      value: '< 1s',
      icon: Zap,
      color: 'bg-primary-700',
      change: 'Fast'
    }
  ];

  const formatDate = (date) => {
    return new Date(date).toLocaleString();
  };

  const getRiskColor = (risk) => {
    if (!risk) return 'bg-gray-100 text-gray-800';
    
    const riskLevel = risk.toLowerCase();
    if (riskLevel.includes('high')) return 'bg-red-100 text-red-800';
    if (riskLevel.includes('moderate') || riskLevel.includes('medium')) return 'bg-yellow-100 text-yellow-800';
    return 'bg-green-100 text-green-800';
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-medical-900">
            Welcome back, {user?.name?.split(' ')[0]}
          </h1>
          <p className="text-medical-600 mt-2">
            Multi-modal breast cancer analysis dashboard for {user?.department}
          </p>
        </div>
        {hasPermission('analysis') && (
          <Link
            to="/analysis"
            className="btn-primary flex items-center space-x-2"
          >
            <Plus className="w-5 h-5" />
            <span>New Analysis</span>
          </Link>
        )}
      </div>

      {/* User Role Banner */}
      <div className={`card border-2 ${
        isDoctor() ? 'bg-primary-50 border-primary-200' :
        isNurse() ? 'bg-primary-100 border-primary-300' :
        isAdmin() ? 'bg-primary-200 border-primary-400' :
        'bg-primary-50 border-primary-200'
      }`}>
        <div className="flex items-center space-x-4">
          <div className={`p-3 rounded-full ${
            isDoctor() ? 'bg-primary-100' :
            isNurse() ? 'bg-primary-200' :
            isAdmin() ? 'bg-primary-300' :
            'bg-primary-100'
          }`}>
            {isAdmin() ? (
              <Shield className={`w-6 h-6 ${
                isDoctor() ? 'text-primary-600' :
                isNurse() ? 'text-primary-700' :
                isAdmin() ? 'text-primary-800' :
                'text-primary-600'
              }`} />
            ) : (
              <User className={`w-6 h-6 ${
                isDoctor() ? 'text-primary-600' :
                isNurse() ? 'text-primary-700' :
                'text-primary-600'
              }`} />
            )}
          </div>
          <div>
            <h3 className="font-semibold text-medical-900">
              {user?.role} - {user?.department}
            </h3>
            <p className="text-medical-600 text-sm">
              License: {user?.license} • Permissions: {user?.permissions?.join(', ')}
            </p>
            <p className="text-medical-500 text-xs mt-1">
              Session started: {new Date(user?.loginTime).toLocaleString()}
            </p>
          </div>
        </div>
      </div>

      {/* System Status Alert */}
      {!backendHealth.isHealthy && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <div>
              <h3 className="font-medium text-red-800">AI System Offline</h3>
              <p className="text-red-600 text-sm mt-1">
                The backend AI system is not responding. Please check the connection or contact support.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div key={index} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-medical-600 text-sm font-medium">
                  {stat.title}
                </p>
                <p className="text-2xl font-bold text-medical-900 mt-1">
                  {stat.value}
                </p>
                <p className="text-medical-500 text-sm mt-1">
                  {stat.change}
                </p>
              </div>
              <div className={`${stat.color} p-3 rounded-lg`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Available Modalities */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-medical-900">
            Available Analysis Modalities
          </h2>
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${
              backendHealth.isHealthy ? 'bg-green-400' : 'bg-red-400'
            }`} />
            <span className="text-sm text-medical-600">
              {backendHealth.isHealthy ? 'All systems operational' : 'System offline'}
            </span>
          </div>
        </div>

        {availableModalities.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {availableModalities.map((modality, index) => (
              <div key={index} className="bg-medical-50 rounded-lg p-4 border border-medical-200">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                    <Activity className="w-4 h-4 text-primary-600" />
                  </div>
                  <div>
                    <h3 className="font-medium text-medical-900 capitalize">
                      {modality.replace('_', ' ')}
                    </h3>
                    <p className="text-sm text-medical-600">
                      AI-powered analysis
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <Activity className="w-12 h-12 text-medical-300 mx-auto mb-4" />
            <p className="text-medical-600">
              {backendHealth.isHealthy 
                ? 'Loading available modalities...' 
                : 'No modalities available - system offline'}
            </p>
          </div>
        )}
      </div>

      {/* Recent Analyses */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-medical-900">
            Recent Analyses
          </h2>
          {analysisHistory.length > 0 && (
            <button
              onClick={clearHistory}
              className="text-sm text-medical-500 hover:text-medical-700"
            >
              Clear History
            </button>
          )}
        </div>

        {analysisHistory.length > 0 ? (
          <div className="space-y-4">
            {analysisHistory.slice(0, 5).map((analysis) => (
              <div key={analysis.id} className="flex items-center justify-between p-4 bg-medical-50 rounded-lg border border-medical-200">
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                    <Brain className="w-5 h-5 text-primary-600" />
                  </div>
                  <div>
                    <h3 className="font-medium text-medical-900">
                      {analysis.patientId}
                    </h3>
                    <div className="flex items-center space-x-2 mt-1">
                      <Clock className="w-3 h-3 text-medical-400" />
                      <span className="text-sm text-medical-600">
                        {formatDate(analysis.timestamp)}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  {analysis.results?.overall_risk_assessment && (
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      getRiskColor(analysis.results.overall_risk_assessment.risk_category)
                    }`}>
                      {analysis.results.overall_risk_assessment.risk_category || 'Unknown'}
                    </span>
                  )}
                  <Link
                    to={`/results/${analysis.patientId}`}
                    className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                  >
                    View Results
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <Brain className="w-16 h-16 text-medical-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-medical-900 mb-2">
              No analyses yet
            </h3>
            <p className="text-medical-600 mb-6">
              Start your first multi-modal breast cancer analysis
            </p>
            <Link
              to="/analysis"
              className="btn-primary inline-flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>Start Analysis</span>
            </Link>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-medical-900 mb-4">
            Quick Actions
          </h3>
          <div className="space-y-3">
            {hasPermission('analysis') && (
              <Link
                to="/analysis"
                className="flex items-center space-x-3 p-3 rounded-lg hover:bg-medical-50 transition-colors"
              >
                <Plus className="w-5 h-5 text-primary-600" />
                <span className="text-medical-700">New Patient Analysis</span>
              </Link>
            )}
            <Link
              to="/analytics"
              className="flex items-center space-x-3 p-3 rounded-lg hover:bg-medical-50 transition-colors"
            >
              <TrendingUp className="w-5 h-5 text-green-600" />
              <span className="text-medical-700">View Analytics</span>
            </Link>
            <Link
              to="/patients"
              className="flex items-center space-x-3 p-3 rounded-lg hover:bg-medical-50 transition-colors"
            >
              <Users className="w-5 h-5 text-blue-600" />
              <span className="text-medical-700">Patient Management</span>
            </Link>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-medical-900 mb-4">
            System Information
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-medical-600">Backend Status</span>
              <span className={`px-2 py-1 rounded text-sm ${
                backendHealth.isHealthy 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {backendHealth.isHealthy ? 'Online' : 'Offline'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-medical-600">Available Models</span>
              <span className="text-medical-900 font-medium">
                {availableModalities.length}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-medical-600">Last Health Check</span>
              <span className="text-medical-900 text-sm">
                {backendHealth.lastChecked 
                  ? formatDate(backendHealth.lastChecked)
                  : 'Never'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;