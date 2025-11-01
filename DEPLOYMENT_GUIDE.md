# Deployment Guide

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.7+ installed
- Node.js 14+ and npm installed
- Terminal/Command Prompt access

### Step 1: Start Backend (Terminal 1)
```bash
python start_backend.py
```
**Expected Output:**
```
🚀 Starting Breast Cancer AI API Server...
📍 Server URL: http://localhost:8000
✅ Server started successfully!
🌐 Frontend can connect to: http://localhost:8000
```

### Step 2: Start Frontend (Terminal 2)
```bash
python start_frontend.py
```
**Expected Output:**
```
📦 Installing frontend dependencies...
✅ Dependencies installed successfully
🚀 Starting Frontend Development Server...
🌐 Frontend will be available at: http://localhost:3000
```

### Step 3: Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

## 🔧 Manual Setup (Alternative)

### Backend Setup
```bash
cd backend
pip install numpy pandas scikit-learn joblib
python api_server.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🧪 Verify Installation

### Test Backend
```bash
python test_connection.py
```

### Test Frontend
1. Open http://localhost:3000
2. Check dashboard shows "AI System Online"
3. Navigate to "New Analysis"
4. Fill sample data and run analysis

## 📋 Sample Analysis Data

Use this data to test the system:

### Patient Information
- **Patient ID**: TEST_001
- **Age**: 45
- **Tumor Size**: 2.5 cm

### Genomics Tab
- **Gene**: BRCA1
- **Mutation**: Pathogenic
- **Allele Frequency**: 0.8

### Biomarkers
- **ER Status**: Positive
- **HER2 Status**: Negative

### Imaging Tab (Ultrasound)
- **Mass Present**: ✓ Checked
- **Mass Size**: 2.5 cm
- **BI-RADS Score**: 4
- **Irregular Shape**: ✓ Checked

### Clinical Notes
- **Text**: "Patient presents with palpable breast mass, family history of breast cancer"

## 🎯 Expected Results

After running analysis, you should see:
- **Overall Risk Assessment**: HIGH RISK (typically 85-95%)
- **Modalities Used**: genomics, imaging, nlp
- **Treatment Recommendations**: 4+ recommendations
- **Analysis Time**: < 1 second

## 🔍 Troubleshooting

### Backend Issues

#### "Module not found" errors
```bash
pip install numpy pandas scikit-learn joblib
```

#### "Port already in use"
```bash
# Kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

#### "AI System Offline"
1. Check backend terminal for errors
2. Restart backend: `python start_backend.py`
3. Verify port 8000 is accessible

### Frontend Issues

#### "npm install" fails
```bash
cd frontend
npm cache clean --force
npm install
```

#### "Cannot connect to backend"
1. Verify backend is running on port 8000
2. Check browser console for CORS errors
3. Ensure no firewall blocking localhost:8000

#### Build errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Common Solutions

#### Backend not responding
```bash
# Restart backend
cd backend
python api_server.py --test  # Test functionality
python api_server.py         # Start server
```

#### Frontend shows "System Offline"
1. Backend must be running first
2. Check backend health: http://localhost:8000/health
3. Restart frontend if backend was started after

#### Analysis fails
1. Check backend terminal for error messages
2. Verify sample data format matches expected schema
3. Try simpler analysis with minimal data

## 🌐 Production Deployment

### Backend Production
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api_server:app --bind 0.0.0.0:8000
```

### Frontend Production
```bash
cd frontend
npm run build
# Serve build/ directory with web server
```

### Docker Deployment
```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "api_server.py"]
```

```dockerfile
# Frontend Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY frontend/ .
RUN npm install && npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 📊 Performance Optimization

### Backend Optimization
- Use production WSGI server (Gunicorn)
- Enable model caching
- Configure proper logging
- Set up health monitoring

### Frontend Optimization
- Build for production (`npm run build`)
- Enable gzip compression
- Configure CDN for static assets
- Implement service worker for caching

## 🔒 Security Configuration

### Backend Security
```python
# In config.py, restrict CORS origins
ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://app.yourdomain.com"
]
```

### Frontend Security
```javascript
// In .env for production
REACT_APP_API_URL=https://api.yourdomain.com
```

## 📈 Monitoring & Logging

### Backend Monitoring
- Health endpoint: `/health`
- Metrics endpoint: `/metrics` (if implemented)
- Log analysis performance
- Monitor model loading status

### Frontend Monitoring
- User analytics
- Error tracking
- Performance monitoring
- API response times

## 🔄 Updates & Maintenance

### Backend Updates
1. Update model files in `backend/models/`
2. Restart backend server
3. Verify health check passes

### Frontend Updates
1. Update code in `frontend/src/`
2. Restart development server
3. For production: rebuild and redeploy

### Model Updates
1. Place new model files in `backend/models/`
2. Update `config.py` if needed
3. Restart backend
4. Fallback models ensure continuity

## 📞 Support & Resources

### Getting Help
- Check console logs for detailed errors
- Review `backend_status_report.md` for system status
- Run `python detailed_check.py` for comprehensive testing

### Documentation
- **API Documentation**: Check `/health` endpoint
- **Model Performance**: See `PROJECT_STRUCTURE.md`
- **Architecture**: Review `README.md`

### Community
- GitHub Issues for bug reports
- Feature requests and improvements
- Contributing guidelines in README

---

## ✅ Success Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads at http://localhost:3000
- [ ] Dashboard shows "AI System Online"
- [ ] Sample analysis completes successfully
- [ ] Results display with risk assessment
- [ ] All modalities (genomics, imaging, nlp) working
- [ ] No console errors in browser
- [ ] API endpoints respond correctly

**🎉 Congratulations! Your Breast Cancer AI Platform is ready to use!**