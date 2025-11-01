#!/usr/bin/env python3
"""
Frontend Startup Script for Breast Cancer AI Platform
"""

import os
import sys
import subprocess
import time
import shutil

def check_node_npm():
    """Check if Node.js and npm are installed"""
    node_ok = False
    npm_ok = False
    
    try:
        # Check Node.js
        node_version = subprocess.check_output(['node', '--version'], stderr=subprocess.DEVNULL)
        print(f"✅ Node.js {node_version.decode().strip()} detected")
        node_ok = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js not found")
    
    try:
        # Check npm
        npm_version = subprocess.check_output(['npm', '--version'], stderr=subprocess.DEVNULL)
        print(f"✅ npm {npm_version.decode().strip()} detected")
        npm_ok = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm not found")
        
        if node_ok:
            print("🔧 Node.js is installed but npm is missing.")
            print("💡 Trying alternative solutions...")
            
            # Try to find npm in Node.js installation directory
            try:
                # Check if npx is available (comes with newer Node.js)
                npx_version = subprocess.check_output(['npx', '--version'], stderr=subprocess.DEVNULL)
                print(f"✅ npx {npx_version.decode().strip()} detected - can use as npm alternative")
                return True
            except:
                pass
            
            print("🛠️ Solutions:")
            print("   1. Reinstall Node.js from https://nodejs.org/ (includes npm)")
            print("   2. Or install npm separately:")
            print("      - Windows: Download npm installer")
            print("      - Or use: winget install OpenJS.NodeJS")
            print("   3. Or use yarn instead of npm")
            return False
    
    if not node_ok:
        print("📥 Please install Node.js from: https://nodejs.org/")
        return False
    
    return npm_ok

def install_dependencies():
    """Install frontend dependencies"""
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    if not os.path.exists(frontend_dir):
        print("❌ Frontend directory not found")
        return False
    
    os.chdir(frontend_dir)
    
    # Check if node_modules exists
    if not os.path.exists('node_modules'):
        print("📦 Installing frontend dependencies...")
        
        # Try different package managers
        package_managers = [
            (['npm', 'install'], 'npm'),
            (['npx', 'npm', 'install'], 'npx + npm'),
            (['yarn', 'install'], 'yarn')
        ]
        
        for cmd, name in package_managers:
            try:
                print(f"   Trying {name}...")
                subprocess.run(cmd, check=True)
                print(f"✅ Dependencies installed successfully using {name}")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"   {name} failed or not available")
                continue
        
        print("❌ Failed to install dependencies with any package manager")
        print("🛠️ Manual installation required:")
        print("   1. Install Node.js with npm from https://nodejs.org/")
        print("   2. Or install yarn: npm install -g yarn")
        print("   3. Then run: npm install (in the frontend directory)")
        return False
    else:
        print("✅ Dependencies already installed")
    
    return True

def start_frontend():
    """Start the frontend development server"""
    print("\n🚀 Starting Frontend Development Server...")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)
    
    # Try different ways to start the server
    start_commands = [
        (['npm', 'start'], 'npm'),
        (['npx', 'react-scripts', 'start'], 'npx + react-scripts'),
        (['yarn', 'start'], 'yarn')
    ]
    
    print("🌐 Frontend will be available at: http://localhost:3000")
    print("🔗 Make sure backend is running at: http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 60)
    
    for cmd, name in start_commands:
        try:
            print(f"Trying to start with {name}...")
            subprocess.run(cmd, check=True)
            return True
        except KeyboardInterrupt:
            print("\n🛑 Frontend stopped by user")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {name} failed or not available")
            continue
    
    print("❌ Could not start frontend with any method")
    print("🛠️ Manual start required:")
    print("   1. Open terminal in frontend/ directory")
    print("   2. Run: npm start")
    print("   3. Or install npm first if missing")
    return False

def create_env_file():
    """Create environment file for frontend"""
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    env_file = os.path.join(frontend_dir, '.env')
    
    if not os.path.exists(env_file):
        print("📝 Creating environment configuration...")
        with open(env_file, 'w') as f:
            f.write("REACT_APP_API_URL=http://localhost:8000\n")
            f.write("GENERATE_SOURCEMAP=false\n")
        print("✅ Environment file created")

def main():
    """Main startup function"""
    print("🎯 Breast Cancer AI Platform - Frontend Startup")
    print("=" * 50)
    
    # Check Node.js and npm
    if not check_node_npm():
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Start frontend
    if not start_frontend():
        sys.exit(1)

if __name__ == "__main__":
    main()