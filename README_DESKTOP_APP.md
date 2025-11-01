# 🖥️ Breast Cancer AI Platform - Desktop App

Transform your web application into a powerful desktop app that runs natively on your laptop!

## 🚀 Quick Start (Desktop App)

### Option 1: One-Click Launch
```bash
# Install dependencies (first time only)
npm run install-deps

# Launch desktop app
python app-launcher.py
```

### Option 2: Manual Steps
```bash
# Install root dependencies
npm install

# Install frontend dependencies  
cd frontend && npm install && cd ..

# Launch desktop app
npm run electron-dev
```

## 🌐 Web Version (When Needed)

```bash
# Launch as website
python app-launcher.py --web

# Or manually
npm run start-web
```

## 📦 Build Distributable App

```bash
# Build everything (creates installer)
python build-app.py

# Build specific parts
python build-app.py --frontend-only
python build-app.py --clean
```

## 🎯 What You Get

### 🖥️ **Desktop App Features**
- ✅ **Native Desktop Experience** - Runs like any other desktop app
- ✅ **No Browser Required** - Standalone application
- ✅ **Auto-Start Backend** - Python backend starts automatically
- ✅ **System Integration** - Desktop shortcuts, taskbar, etc.
- ✅ **Offline Capable** - Works without internet (for local analysis)
- ✅ **Professional Menus** - File, View, Window, Help menus
- ✅ **Keyboard Shortcuts** - Ctrl+N for new analysis, etc.

### 🌐 **Web Version Features**
- ✅ **Host on Server** - Deploy to hospital intranet
- ✅ **Multi-User Access** - Multiple users simultaneously
- ✅ **Remote Access** - Access from any device
- ✅ **Easy Updates** - Update once, affects all users

## 📁 Project Structure

```
breast-cancer-ai-platform/
├── 🖥️ Desktop App Files
│   ├── package.json              # Electron app config
│   ├── electron/
│   │   ├── main.js              # Main Electron process
│   │   ├── preload.js           # Security layer
│   │   └── assets/              # App icons
│   ├── app-launcher.py          # Easy launcher script
│   └── build-app.py             # Build distributable app
│
├── 🌐 Web App Files  
│   ├── frontend/                # React frontend
│   ├── backend/                 # Python AI backend
│   ├── start_frontend.py        # Web frontend launcher
│   └── start_backend.py         # Web backend launcher
│
└── 📋 Documentation
    ├── README.md                # Main documentation
    ├── AUTHENTICATION_GUIDE.md  # Login system guide
    └── README_DESKTOP_APP.md    # This file
```

## 🔧 Available Commands

### Desktop App Commands
```bash
# Development
npm run electron-dev          # Run in development mode
npm run electron             # Run production build

# Building
npm run build-electron       # Build desktop app
npm run package-app         # Create installer package

# Easy launcher
python app-launcher.py       # Launch desktop app
python app-launcher.py --web # Launch web version
```

### Web App Commands  
```bash
# Development
npm run start-web           # Start both backend and frontend
npm run start-frontend      # Start only frontend
npm run start-backend       # Start only backend

# Building
npm run build-web          # Build for web deployment
npm run build-frontend     # Build only frontend
```

## 🎨 Desktop App Screenshots

### Main Application Window
- **Professional Interface** - Clean, medical-themed design
- **Integrated Navigation** - No browser chrome, just your app
- **Native Menus** - File, View, Window menus like desktop apps

### Login Screen
- **Hospital Branding** - Professional login with pastel pink theme
- **Security Features** - HIPAA compliant design
- **Demo Credentials** - Easy testing with hospital staff accounts

### Dashboard
- **Role-Based Interface** - Different views for doctors, nurses, admins
- **Real-time Status** - Backend health monitoring
- **Quick Actions** - Easy access to common tasks

## 🔒 Security Features

### Desktop App Security
- ✅ **Sandboxed Environment** - Electron security best practices
- ✅ **No Remote Code** - All code runs locally
- ✅ **Secure Context** - Context isolation enabled
- ✅ **Local Data** - Patient data stays on your machine

### Authentication
- ✅ **Hospital Staff Only** - Role-based access control
- ✅ **Session Management** - Automatic logout after inactivity
- ✅ **Permission System** - Granular access control
- ✅ **Audit Trail** - All access logged

## 🚀 Deployment Options

### 1. Desktop App Distribution
```bash
# Build installers for all platforms
python build-app.py

# Generated files:
# - Windows: .exe installer
# - macOS: .dmg package  
# - Linux: .AppImage
```

### 2. Portable Version
```bash
# Create portable version (no installation)
python build-app.py

# Use: dist/portable/run-app.bat (Windows)
# Use: dist/portable/run-app.sh (Linux/Mac)
```

### 3. Web Deployment
```bash
# Build for web hosting
npm run build-web

# Deploy frontend/build/ to web server
# Run backend on server with python backend/main.py
```

## 🔧 Customization

### App Icon
Replace files in `electron/assets/`:
- `icon.png` (512x512 for Linux)
- `icon.ico` (for Windows)
- `icon.icns` (for macOS)

### App Name & Details
Edit `package.json`:
```json
{
  "name": "your-app-name",
  "productName": "Your App Display Name",
  "description": "Your app description"
}
```

### Menu Customization
Edit `electron/main.js` - modify the `createMenu()` function

## 🆘 Troubleshooting

### Desktop App Issues
```bash
# Clean and rebuild
python build-app.py --clean
npm install
python app-launcher.py

# Check Electron installation
npx electron --version

# Debug mode
npm run electron-dev
```

### Web Version Issues
```bash
# Check ports
netstat -an | grep 3000  # Frontend
netstat -an | grep 8000  # Backend

# Restart services
python app-launcher.py --web
```

### Build Issues
```bash
# Clean everything
python build-app.py --clean
rm -rf node_modules frontend/node_modules
npm run install-deps
```

## 🎯 Best Practices

### For Desktop Use
1. **Use app-launcher.py** - Easiest way to start
2. **Build once, use daily** - Create installer for daily use
3. **Keep data local** - Better performance and privacy
4. **Regular updates** - Rebuild when you add features

### For Web Deployment
1. **Use HTTPS** - Required for medical applications
2. **Secure backend** - Add authentication to API endpoints
3. **Database integration** - Replace mock data with real database
4. **Load balancing** - For multiple users

## 📋 Next Steps

1. **Try the desktop app**: `python app-launcher.py`
2. **Build an installer**: `python build-app.py`
3. **Customize the interface** - Add your hospital branding
4. **Deploy to production** - Choose desktop or web deployment
5. **Add real data sources** - Connect to hospital systems

---

## 🎉 You Now Have Both!

✅ **Desktop App** - Perfect for individual use on your laptop
✅ **Web Version** - Perfect for hosting and sharing
✅ **Easy Switching** - Use the same codebase for both
✅ **Professional Quality** - Ready for hospital environments

The best of both worlds - use as a desktop app daily, deploy as a website when needed!