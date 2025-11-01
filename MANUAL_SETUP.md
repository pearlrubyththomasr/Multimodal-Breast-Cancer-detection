# Manual Setup Guide

## 🔧 When Automated Scripts Don't Work

If you're having issues with the automated startup scripts, follow this manual setup guide.

## 📋 Prerequisites Check

### Check Node.js Installation
```bash
node --version
```
**Expected**: v14.0.0 or higher

### Check npm Installation
```bash
npm --version
```
**Expected**: 6.0.0 or higher

## 🛠️ Fix Missing npm

### Option 1: Reinstall Node.js (Recommended)
1. Go to https://nodejs.org/
2. Download the LTS version
3. Install (this includes npm)
4. Restart terminal
5. Verify: `npm --version`

### Option 2: Install npm Separately (Windows)
```bash
# Using winget (Windows 10/11)
winget install OpenJS.NodeJS

# Or download npm installer from:
# https://nodejs.org/en/download/
```

### Option 3: Use Alternative Package Manager
```bash
# Install yarn as npm alternative
npm install -g yarn
# Or if npm doesn't work:
# Download yarn from https://yarnpkg.com/
```

## 🚀 Manual Backend Setup

### Step 1: Navigate to Backend
```bash
cd backend
```

### Step 2: Install Python Dependencies
```bash
# Option 1: Using pip
pip install numpy pandas scikit-learn joblib

# Option 2: Using requirements file (if available)
pip install -r requirements.txt

# Option 3: Install individually if batch fails
pip install numpy
pip install pandas
pip install scikit-learn
pip install joblib
```

### Step 3: Test Backend
```bash
python api_server.py --test
```
**Expected Output**: ✅ Sample analysis successful

### Step 4: Start Backend Server
```bash
python api_server.py
```
**Expected**: Server running on http://localhost:8000

## 🌐 Manual Frontend Setup

### Step 1: Navigate to Frontend
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
# Try these in order until one works:

# Option 1: npm
npm install

# Option 2: yarn (if npm doesn't work)
yarn install

# Option 3: npx (if npm is broken)
npx npm install

# Option 4: Force npm cache clean first
npm cache clean --force
npm install
```

### Step 3: Create Environment File
Create `.env` file in frontend directory:
```
REACT_APP_API_URL=http://localhost:8000
GENERATE_SOURCEMAP=false
```

### Step 4: Start Frontend Server
```bash
# Try these in order:

# Option 1: npm
npm start

# Option 2: yarn
yarn start

# Option 3: npx
npx react-scripts start

# Option 4: Direct node
node node_modules/react-scripts/bin/react-scripts.js start
```

## 🧪 Verify Setup

### Test Backend (Terminal 1)
```bash
curl http://localhost:8000/health
```
**Expected**: `{"status": "healthy", ...}`

### Test Frontend (Browser)
1. Open http://localhost:3000
2. Should see "Breast Cancer AI" dashboard
3. Check for "AI System Online" status

### Test Full Integration
1. Go to "New Analysis" page
2. Fill in sample data:
   - Patient ID: TEST_001
   - Age: 45
   - Add genomic alteration: BRCA1, Pathogenic
3. Click "Start AI Analysis"
4. Should see results page with risk assessment

## 🔍 Troubleshooting Common Issues

### "Module not found" (Backend)
```bash
# Install missing modules individually
pip install numpy
pip install pandas
pip install scikit-learn
pip install joblib

# Or upgrade pip first
python -m pip install --upgrade pip
```

### "npm not found" (Frontend)
```bash
# Check if Node.js is properly installed
where node    # Windows
which node    # Mac/Linux

# If Node.js exists but npm doesn't:
# Reinstall Node.js from https://nodejs.org/
```

### "Port already in use"
```bash
# Windows - Kill process on port
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux - Kill process on port
lsof -ti:8000 | xargs kill -9

# Or use different ports:
# Backend: python api_server.py --port 8001
# Frontend: PORT=3001 npm start
```

### "CORS errors" (Browser Console)
1. Make sure backend is running first
2. Check backend URL in frontend/.env
3. Restart both servers

### "Analysis fails"
1. Check backend terminal for errors
2. Verify sample data format
3. Try simpler analysis with just patient ID and age

## 📦 Alternative Installation Methods

### Using Conda (Python)
```bash
conda create -n breast-cancer-ai python=3.9
conda activate breast-cancer-ai
conda install numpy pandas scikit-learn
pip install joblib
```

### Using Docker (Advanced)
```bash
# Backend
docker build -t breast-cancer-backend backend/
docker run -p 8000:8000 breast-cancer-backend

# Frontend  
docker build -t breast-cancer-frontend frontend/
docker run -p 3000:3000 breast-cancer-frontend
```

## 🆘 Still Having Issues?

### Quick Diagnostic
Run this diagnostic script:
```bash
python -c "
import sys
print(f'Python: {sys.version}')
try:
    import numpy, pandas, sklearn, joblib
    print('✅ All Python packages available')
except ImportError as e:
    print(f'❌ Missing Python package: {e}')
"
```

### Check Node.js Diagnostic
```bash
node -e "
console.log('Node.js:', process.version);
try {
  require('fs');
  console.log('✅ Node.js working');
} catch(e) {
  console.log('❌ Node.js issue:', e.message);
}
"
```

### Minimal Test
If all else fails, test the core functionality:

1. **Backend Only Test**:
   ```bash
   cd backend
   python main_simple.py
   ```

2. **API Test**:
   ```bash
   python test_connection.py
   ```

### Get Help
- Check error messages in terminal
- Look for specific error codes
- Try one component at a time (backend first, then frontend)
- Ensure no antivirus blocking localhost connections

## ✅ Success Indicators

### Backend Working
- ✅ `python api_server.py --test` shows "Sample analysis successful"
- ✅ http://localhost:8000/health returns JSON
- ✅ No error messages in terminal

### Frontend Working  
- ✅ `npm start` opens browser to localhost:3000
- ✅ Dashboard shows "AI System Online"
- ✅ No red errors in browser console

### Integration Working
- ✅ Can complete sample analysis end-to-end
- ✅ Results page shows risk assessment
- ✅ All modalities (genomics, imaging, nlp) working

---

**💡 Pro Tip**: Start with backend first, verify it works, then add frontend. This makes debugging much easier!