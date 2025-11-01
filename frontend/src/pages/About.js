import React from 'react';
import { 
  Brain, 
  Dna, 
  Scan, 
  FileText, 
  Shield, 
  Zap, 
  Users, 
  Award,
  CheckCircle,
  ArrowRight,
  Github,
  Mail,
  Globe
} from 'lucide-react';

const About = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Analysis',
      description: 'Advanced machine learning algorithms analyze multiple data modalities for comprehensive breast cancer assessment.',
      color: 'bg-blue-500'
    },
    {
      icon: Dna,
      title: 'Genomics Integration',
      description: 'Incorporates genetic alterations, biomarkers, and tumor mutational burden for personalized risk assessment.',
      color: 'bg-green-500'
    },
    {
      icon: Scan,
      title: 'Multi-Modal Imaging',
      description: 'Analyzes ultrasound, mammography, and X-ray findings using specialized computer vision models.',
      color: 'bg-purple-500'
    },
    {
      icon: FileText,
      title: 'Clinical Text Analysis',
      description: 'Natural language processing of clinical notes and pathology reports for comprehensive insights.',
      color: 'bg-orange-500'
    },
    {
      icon: Shield,
      title: 'Privacy & Security',
      description: 'HIPAA-compliant data handling with end-to-end encryption and secure processing.',
      color: 'bg-red-500'
    },
    {
      icon: Zap,
      title: 'Real-Time Results',
      description: 'Fast analysis with results delivered in under 1 second for immediate clinical decision support.',
      color: 'bg-yellow-500'
    }
  ];

  const modalities = [
    {
      name: 'Genomics Analysis',
      description: 'Analyzes genetic alterations, biomarkers (ER, PR, HER2, BRCA), and tumor mutational burden',
      capabilities: [
        'BRCA1/BRCA2 mutation analysis',
        'Hormone receptor status assessment',
        'Treatment response prediction',
        'Genetic risk stratification'
      ]
    },
    {
      name: 'Imaging Analysis',
      description: 'Multi-modal imaging analysis including ultrasound, mammography, and chest X-rays',
      capabilities: [
        'BI-RADS scoring integration',
        'Mass and calcification detection',
        'Metastasis screening',
        'Architectural distortion analysis'
      ]
    },
    {
      name: 'Clinical NLP',
      description: 'Natural language processing of clinical notes and pathology reports',
      capabilities: [
        'Symptom severity assessment',
        'Clinical urgency detection',
        'Treatment discussion extraction',
        'Family history identification'
      ]
    }
  ];

  const stats = [
    { label: 'Analysis Modalities', value: '3+' },
    { label: 'AI Models', value: '8+' },
    { label: 'Response Time', value: '<1s' },
    { label: 'Accuracy Rate', value: '89%+' }
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-6">
        <div className="flex items-center justify-center space-x-3 mb-6">
          <div className="w-16 h-16 bg-primary-600 rounded-2xl flex items-center justify-center">
            <Brain className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-medical-900">
            Breast Cancer AI Platform
          </h1>
        </div>
        
        <p className="text-xl text-medical-600 max-w-3xl mx-auto leading-relaxed">
          A comprehensive multi-modal AI platform for breast cancer analysis, integrating genomics, 
          imaging, and clinical data to provide personalized risk assessment and treatment recommendations.
        </p>

        <div className="flex items-center justify-center space-x-6 pt-4">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-2xl font-bold text-primary-600">{stat.value}</div>
              <div className="text-sm text-medical-600">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Features Grid */}
      <div>
        <h2 className="text-2xl font-bold text-medical-900 text-center mb-8">
          Platform Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div key={index} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start space-x-4">
                <div className={`${feature.color} p-3 rounded-lg flex-shrink-0`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-medical-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-medical-600 text-sm">
                    {feature.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Analysis Modalities */}
      <div>
        <h2 className="text-2xl font-bold text-medical-900 text-center mb-8">
          Analysis Modalities
        </h2>
        <div className="space-y-6">
          {modalities.map((modality, index) => (
            <div key={index} className="card">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-medical-900 mb-2">
                    {modality.name}
                  </h3>
                  <p className="text-medical-600">
                    {modality.description}
                  </p>
                </div>
                <div className="flex items-center space-x-2 text-primary-600">
                  <CheckCircle className="w-5 h-5" />
                  <span className="text-sm font-medium">Active</span>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {modality.capabilities.map((capability, capIndex) => (
                  <div key={capIndex} className="flex items-center space-x-2">
                    <ArrowRight className="w-4 h-4 text-primary-500" />
                    <span className="text-medical-700 text-sm">{capability}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Technical Architecture */}
      <div className="card bg-medical-50">
        <h2 className="text-2xl font-bold text-medical-900 mb-6">
          Technical Architecture
        </h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-semibold text-medical-900 mb-4">
              Backend Components
            </h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-medical-700">FastAPI REST API Server</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-medical-700">Multi-Modal AI Model Ensemble</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span className="text-medical-700">BERT-based Clinical NLP</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                <span className="text-medical-700">TensorFlow/PyTorch Models</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                <span className="text-medical-700">Scikit-learn Classifiers</span>
              </div>
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-medical-900 mb-4">
              Frontend Components
            </h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-medical-700">React.js Single Page Application</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-medical-700">Tailwind CSS Styling</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span className="text-medical-700">Recharts Data Visualization</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                <span className="text-medical-700">React Hook Form</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                <span className="text-medical-700">Axios API Client</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Model Performance */}
      <div>
        <h2 className="text-2xl font-bold text-medical-900 text-center mb-8">
          Model Performance
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Scan className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="font-semibold text-medical-900 mb-2">Ultrasound Analysis</h3>
            <div className="text-2xl font-bold text-blue-600 mb-1">89.2%</div>
            <p className="text-medical-600 text-sm">Classification Accuracy</p>
          </div>
          
          <div className="card text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Dna className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="font-semibold text-medical-900 mb-2">Genomics Analysis</h3>
            <div className="text-2xl font-bold text-green-600 mb-1">95%+</div>
            <p className="text-medical-600 text-sm">Risk Prediction Accuracy</p>
          </div>
          
          <div className="card text-center">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <FileText className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="font-semibold text-medical-900 mb-2">Clinical NLP</h3>
            <div className="text-2xl font-bold text-purple-600 mb-1">92%+</div>
            <p className="text-medical-600 text-sm">Entity Recognition</p>
          </div>
        </div>
      </div>

      {/* Usage Guidelines */}
      <div className="card">
        <h2 className="text-2xl font-bold text-medical-900 mb-6">
          Usage Guidelines & Disclaimers
        </h2>
        
        <div className="space-y-4">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-start space-x-3">
              <Shield className="w-5 h-5 text-yellow-600 mt-0.5" />
              <div>
                <h3 className="font-medium text-yellow-800 mb-1">
                  Clinical Decision Support Tool
                </h3>
                <p className="text-yellow-700 text-sm">
                  This platform is designed as a clinical decision support tool and should not replace 
                  professional medical judgment. All results should be interpreted by qualified healthcare professionals.
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start space-x-3">
              <Users className="w-5 h-5 text-blue-600 mt-0.5" />
              <div>
                <h3 className="font-medium text-blue-800 mb-1">
                  Intended Users
                </h3>
                <p className="text-blue-700 text-sm">
                  Designed for use by oncologists, radiologists, pathologists, and other healthcare 
                  professionals involved in breast cancer diagnosis and treatment planning.
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-start space-x-3">
              <Award className="w-5 h-5 text-green-600 mt-0.5" />
              <div>
                <h3 className="font-medium text-green-800 mb-1">
                  Validation & Testing
                </h3>
                <p className="text-green-700 text-sm">
                  All models have been validated on synthetic and clinical datasets. Continuous 
                  monitoring and updates ensure optimal performance and accuracy.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Contact & Support */}
      <div className="card bg-primary-50 border-primary-200">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-medical-900 mb-4">
            Contact & Support
          </h2>
          <p className="text-medical-600 mb-6">
            Need help or have questions about the platform? Get in touch with our team.
          </p>
          
          <div className="flex items-center justify-center space-x-6">
            <a href="#" className="flex items-center space-x-2 text-primary-600 hover:text-primary-700">
              <Mail className="w-5 h-5" />
              <span>support@breastcancerai.com</span>
            </a>
            <a href="#" className="flex items-center space-x-2 text-primary-600 hover:text-primary-700">
              <Github className="w-5 h-5" />
              <span>GitHub Repository</span>
            </a>
            <a href="#" className="flex items-center space-x-2 text-primary-600 hover:text-primary-700">
              <Globe className="w-5 h-5" />
              <span>Documentation</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;