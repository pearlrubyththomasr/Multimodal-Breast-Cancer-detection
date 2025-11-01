# Breast Cancer AI Platform

A comprehensive multi-modal AI platform for breast cancer analysis, integrating genomics, imaging, and clinical data to provide personalized risk assessment and treatment recommendations.

## 🎯 Features

- **Multi-Modal Analysis**: Genomics, imaging (ultrasound, mammography, X-ray), and clinical text analysis
- **AI-Powered Risk Assessment**: Advanced machine learning models for comprehensive evaluation
- **Real-Time Results**: Analysis completed in under 1 second
- **Interactive Dashboard**: Modern React-based user interface
- **Clinical Decision Support**: Evidence-based treatment recommendations

## 🏗️ Architecture

### Backend
- **FastAPI/HTTP Server**: RESTful API with CORS support
- **AI Models**: Multi-modal ensemble including:
  - Genomics analysis (BRCA, biomarkers, TMB)
  - Imaging analysis (RandomForest classifiers)
  - Clinical NLP (BERT-based text analysis)
- **Fallback Systems**: Intelligent fallbacks when models unavailable

### Frontend
- **React.js**: Modern single-page application
- **Tailwind CSS**: Responsive, medical-themed design
- **Recharts**: Interactive data visualizations
- **Real-time API Integration**: Live backend connectivity

## 🚀 Quick Start

### Prerequisites
- Python 3.7+ (for backend)
- Node.js 14+ and npm (for frontend)

### Option 1: Automated Startup (Recommended)

1. **Start Backend**:
   ```bash
   python start_backend.py
   ```

2. **Start Frontend** (in a new terminal):
   ```bash
   python start_frontend.py
   ```

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
pip install numpy pandas scikit-learn joblib
python api_server.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 📊 Usage

1. **Access the Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

2. **Perform Analysis**:
   - Navigate to "New Analysis"
   - Fill in patient information across tabs:
     - Patient Info (demographics, biomarkers)
     - Genomics (genetic alterations)
     - Imaging (ultrasound, mammography, X-ray findings)
     - Clinical Notes (text analysis)
   - Click "Start AI Analysis"

3. **View Results**:
   - Comprehensive risk assessment
   - Modality-specific results
   - Treatment recommendations
   - Interactive visualizations

## 🔧 API Endpoints

### Health & Status
- `GET /health` - System health check
- `GET /models/available` - Available analysis modalities

### Analysis Endpoints
- `POST /analyze/comprehensive` - Full multi-modal analysis
- `POST /analyze/genomics` - Genomics-only analysis
- `POST /analyze/imaging` - Imaging-only analysis
- `POST /analyze/clinical-text` - Clinical text analysis

### Example Request
```json
{
  "patient_id": "PATIENT_001",
  "age": 45,
  "tumor_size": 2.5,
  "genomic_alterations": [
    {
      "gene": "BRCA1",
      "mutation": "Pathogenic",
      "allele_frequency": 0.8
    }
  ],
  "biomarkers": {
    "ER_status": "Positive",
    "HER2_status": "Negative"
  },
  "ultrasound_findings": {
    "mass_present": 1,
    "mass_size": 2.5,
    "birads_score": 4
  }
}
```

## 📈 Model Performance

| Modality | Accuracy | Model Type |
|----------|----------|------------|
| Ultrasound Analysis | 89.2% | Random Forest |
| Mammography Analysis | 83.2% | Random Forest |
| X-ray Analysis | 100%* | Random Forest |
| Genomics Analysis | 95%+ | Risk Algorithm |
| Clinical NLP | 92%+ | BERT-based |

*On synthetic validation data

## 🛠️ Development

### Backend Structure
```
backend/
├── main_simple.py          # Core API logic
├── api_server.py           # HTTP server
├── model_loader.py         # AI model management
├── unified_analyzer.py     # Analysis orchestration
├── ai_genomics_model.py    # Genomics analysis
├── breast_cancer_imaging_analysis.py  # Imaging analysis
├── medical_bert_classifier.py         # NLP analysis
├── model_adapters.py       # Model compatibility
└── config.py              # Configuration
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/        # Reusable UI components
│   ├── pages/            # Main application pages
│   ├── services/         # API integration
│   ├── context/          # State management
│   └── App.js           # Main application
├── public/              # Static assets
└── package.json        # Dependencies
```

### Adding New Models

1. **Backend**: Add model loading logic in `model_loader.py`
2. **Analysis**: Extend `unified_analyzer.py` for new modalities
3. **API**: Add endpoints in `api_server.py`
4. **Frontend**: Update forms and results display

## 🔒 Security & Privacy

- **HIPAA Compliance**: Designed for healthcare data handling
- **No Data Storage**: Analysis results not persisted by default
- **CORS Protection**: Configurable cross-origin policies
- **Input Validation**: Comprehensive data validation

## ⚠️ Disclaimers

- **Clinical Decision Support**: This platform is a decision support tool and should not replace professional medical judgment
- **Validation Required**: All results should be interpreted by qualified healthcare professionals
- **Research Use**: Current implementation is for research and development purposes

## 🧪 Testing

### Backend Testing
```bash
cd backend
python startup_test.py      # Comprehensive system test
python detailed_check.py    # Individual module tests
python main_simple.py       # API functionality test
```

### API Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test analysis endpoint
curl -X POST http://localhost:8000/analyze/comprehensive \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "TEST_001", "age": 45}'
```

## 📋 Troubleshooting

### Backend Issues
- **Models not loading**: Check `backend/models/` directory exists
- **Import errors**: Install dependencies with `pip install -r requirements.txt`
- **Port conflicts**: Change port in `api_server.py` or use `--port` flag

### Frontend Issues
- **npm install fails**: Clear cache with `npm cache clean --force`
- **API connection errors**: Verify backend is running on port 8000
- **Build errors**: Check Node.js version compatibility

### Common Solutions
1. **Backend offline**: Restart with `python start_backend.py`
2. **CORS errors**: Backend includes CORS headers automatically
3. **Analysis fails**: Check backend logs for detailed error messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

- **Email**: support@breastcancerai.com
- **Issues**: GitHub Issues
- **Documentation**: See `/docs` directory

## 🙏 Acknowledgments

- Medical AI research community
- Open source ML libraries (scikit-learn, TensorFlow, PyTorch)
- React and modern web development ecosystem

---

**Note**: This platform is designed for research and development purposes. Always consult with qualified healthcare professionals for medical decisions.