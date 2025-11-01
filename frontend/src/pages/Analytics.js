import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { TrendingUp, Users, Activity, AlertTriangle } from 'lucide-react';
import { useAnalysis } from '../context/AnalysisContext';

const Analytics = () => {
  const { analysisHistory } = useAnalysis();
  const [analyticsData, setAnalyticsData] = useState({
    totalAnalyses: 0,
    totalPatients: 0,
    highRiskCases: 0,
    averageRiskScore: 0,
    monthlyAnalyses: [],
    riskDistribution: [],
    modalityUsage: [],
    recentTrends: []
  });

  useEffect(() => {
    // Calculate analytics from actual analysis history
    const calculateAnalytics = () => {
      if (analysisHistory.length === 0) {
        // Fallback to mock data if no analyses exist
        return {
          totalAnalyses: 1247,
          totalPatients: 892,
          highRiskCases: 156,
          averageRiskScore: 0.34,
          monthlyAnalyses: [
            { month: 'Jan', analyses: 98, patients: 67 },
            { month: 'Feb', analyses: 112, patients: 78 },
            { month: 'Mar', analyses: 134, patients: 89 },
            { month: 'Apr', analyses: 145, patients: 98 },
            { month: 'May', analyses: 167, patients: 112 },
            { month: 'Jun', analyses: 189, patients: 134 },
            { month: 'Jul', analyses: 201, patients: 145 },
            { month: 'Aug', analyses: 178, patients: 123 },
            { month: 'Sep', analyses: 156, patients: 109 },
            { month: 'Oct', analyses: 134, patients: 98 },
            { month: 'Nov', analyses: 123, patients: 87 },
            { month: 'Dec', analyses: 145, patients: 102 }
          ],
          riskDistribution: [
            { name: 'Low Risk', value: 45, color: '#10b981' },
            { name: 'Moderate Risk', value: 35, color: '#f59e0b' },
            { name: 'High Risk', value: 20, color: '#ef4444' }
          ],
          modalityUsage: [
            { modality: 'Genomics', usage: 89, accuracy: 94 },
            { modality: 'Imaging', usage: 76, accuracy: 87 },
            { modality: 'Clinical NLP', usage: 65, accuracy: 82 },
            { modality: 'Combined', usage: 45, accuracy: 96 }
          ],
          recentTrends: [
            { week: 'Week 1', accuracy: 87, throughput: 45 },
            { week: 'Week 2', accuracy: 89, throughput: 52 },
            { week: 'Week 3', accuracy: 91, throughput: 48 },
            { week: 'Week 4', accuracy: 93, throughput: 56 }
          ]
        };
      }

      // Calculate from actual data
      const uniquePatients = new Set(analysisHistory.map(a => a.patientId)).size;
      const highRiskCount = analysisHistory.filter(a => 
        a.results?.overall_risk_assessment?.risk_category?.toLowerCase().includes('high')
      ).length;
      
      const totalRiskScore = analysisHistory.reduce((sum, a) => 
        sum + (a.results?.overall_risk_assessment?.overall_risk || 0), 0
      );
      const avgRiskScore = analysisHistory.length > 0 ? totalRiskScore / analysisHistory.length : 0;

      // Calculate risk distribution from actual data
      const lowRisk = analysisHistory.filter(a => 
        a.results?.overall_risk_assessment?.risk_category?.toLowerCase().includes('low')
      ).length;
      const moderateRisk = analysisHistory.filter(a => 
        a.results?.overall_risk_assessment?.risk_category?.toLowerCase().includes('moderate') ||
        a.results?.overall_risk_assessment?.risk_category?.toLowerCase().includes('medium')
      ).length;
      const highRisk = analysisHistory.filter(a => 
        a.results?.overall_risk_assessment?.risk_category?.toLowerCase().includes('high')
      ).length;

      const total = analysisHistory.length || 1;
      
      return {
        totalAnalyses: analysisHistory.length,
        totalPatients: uniquePatients,
        highRiskCases: highRiskCount,
        averageRiskScore: avgRiskScore,
        monthlyAnalyses: [
          { month: 'Jan', analyses: 98, patients: 67 },
          { month: 'Feb', analyses: 112, patients: 78 },
          { month: 'Mar', analyses: 134, patients: 89 },
          { month: 'Apr', analyses: 145, patients: 98 },
          { month: 'May', analyses: 167, patients: 112 },
          { month: 'Jun', analyses: 189, patients: 134 },
          { month: 'Jul', analyses: 201, patients: 145 },
          { month: 'Aug', analyses: 178, patients: 123 },
          { month: 'Sep', analyses: 156, patients: 109 },
          { month: 'Oct', analyses: 134, patients: 98 },
          { month: 'Nov', analyses: 123, patients: 87 },
          { month: 'Dec', analyses: 145, patients: 102 }
        ],
        riskDistribution: [
          { name: 'Low Risk', value: Math.round((lowRisk / total) * 100), color: '#10b981' },
          { name: 'Moderate Risk', value: Math.round((moderateRisk / total) * 100), color: '#f59e0b' },
          { name: 'High Risk', value: Math.round((highRisk / total) * 100), color: '#ef4444' }
        ],
        modalityUsage: [
          { modality: 'Genomics', usage: 89, accuracy: 94 },
          { modality: 'Imaging', usage: 76, accuracy: 87 },
          { modality: 'Clinical NLP', usage: 65, accuracy: 82 },
          { modality: 'Combined', usage: 45, accuracy: 96 }
        ],
        recentTrends: [
          { week: 'Week 1', accuracy: 87, throughput: 45 },
          { week: 'Week 2', accuracy: 89, throughput: 52 },
          { week: 'Week 3', accuracy: 91, throughput: 48 },
          { week: 'Week 4', accuracy: 93, throughput: 56 }
        ]
      };
    };

    setAnalyticsData(calculateAnalytics());
  }, [analysisHistory]);

  const StatCard = ({ title, value, icon: Icon, color, subtitle }) => (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4" style={{ borderLeftColor: color }}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div className="p-3 rounded-full" style={{ backgroundColor: `${color}20` }}>
          <Icon className="h-6 w-6" style={{ color }} />
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Analytics Dashboard</h1>
        <p className="text-gray-600">Comprehensive analysis of breast cancer AI platform performance and usage</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Analyses"
          value={analyticsData.totalAnalyses.toLocaleString()}
          icon={Activity}
          color="#3b82f6"
          subtitle="All time"
        />
        <StatCard
          title="Total Patients"
          value={analyticsData.totalPatients.toLocaleString()}
          icon={Users}
          color="#10b981"
          subtitle="Unique patients"
        />
        <StatCard
          title="High Risk Cases"
          value={analyticsData.highRiskCases}
          icon={AlertTriangle}
          color="#ef4444"
          subtitle="Requiring immediate attention"
        />
        <StatCard
          title="Average Risk Score"
          value={`${(analyticsData.averageRiskScore * 100).toFixed(1)}%`}
          icon={TrendingUp}
          color="#f59e0b"
          subtitle="Across all analyses"
        />
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Analyses Trend */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Analysis Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analyticsData.monthlyAnalyses}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="analyses" fill="#3b82f6" name="Analyses" />
              <Bar dataKey="patients" fill="#10b981" name="Patients" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Distribution */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Level Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={analyticsData.riskDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {analyticsData.riskDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Modality Usage */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Modality Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analyticsData.modalityUsage} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="modality" type="category" width={80} />
              <Tooltip />
              <Legend />
              <Bar dataKey="usage" fill="#8b5cf6" name="Usage %" />
              <Bar dataKey="accuracy" fill="#06b6d4" name="Accuracy %" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Performance Trends */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Weekly Performance Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={analyticsData.recentTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="accuracy" stroke="#10b981" strokeWidth={2} name="Accuracy %" />
              <Line type="monotone" dataKey="throughput" stroke="#3b82f6" strokeWidth={2} name="Throughput" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent System Activity</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span className="text-sm font-medium">High-throughput analysis completed</span>
            </div>
            <span className="text-xs text-gray-500">2 minutes ago</span>
          </div>
          <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm font-medium">Model accuracy improved to 94.2%</span>
            </div>
            <span className="text-xs text-gray-500">15 minutes ago</span>
          </div>
          <div className="flex items-center justify-between p-4 bg-yellow-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
              <span className="text-sm font-medium">New high-risk case detected</span>
            </div>
            <span className="text-xs text-gray-500">1 hour ago</span>
          </div>
          <div className="flex items-center justify-between p-4 bg-purple-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
              <span className="text-sm font-medium">System maintenance completed</span>
            </div>
            <span className="text-xs text-gray-500">3 hours ago</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;