#!/usr/bin/env python3
"""
Breast Cancer AI Platform - Build Script
Creates distributable desktop app packages
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class AppBuilder:
    def __init__(self):
        self.root_path = Path(__file__).parent
        self.frontend_path = self.root_path / "frontend"
        self.dist_path = self.root_path / "dist"
        
    def clean_build(self):
        """Clean previous build artifacts"""
        print("🧹 Cleaning previous builds...")
        
        paths_to_clean = [
            self.dist_path,
            self.frontend_path / "build",
            self.root_path / "node_modules" / ".cache"
        ]
        
        for path in paths_to_clean:
            try:
                if path.exists():
                    shutil.rmtree(path)
                    print(f"   Removed {path}")
            except Exception as e:
                print(f"   Warning: Could not remove {path}: {e}")
        
        print("✅ Clean completed")
        return True
    
    def install_dependencies(self):
        """Install all required dependencies"""
        print("📦 Installing dependencies...")
        
        # Install root dependencies (Electron, etc.)
        try:
            subprocess.run(["npm", "install"], check=True, cwd=str(self.root_path), shell=True)
            print("✅ Root dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install root dependencies: {e}")
            return False
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js and npm first.")
            return False
        
        # Install frontend dependencies
        try:
            subprocess.run(["npm", "install"], check=True, cwd=str(self.frontend_path), shell=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install frontend dependencies: {e}")
            return False
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js and npm first.")
            return False
        
        return True
    
    def build_frontend(self):
        """Build the React frontend for production"""
        print("⚛️  Building React frontend...")
        
        try:
            subprocess.run(["npm", "run", "build"], check=True, cwd=str(self.frontend_path), shell=True)
            print("✅ Frontend build completed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Frontend build failed: {e}")
            return False
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js and npm first.")
            return False
    
    def build_electron_app(self):
        """Build the Electron desktop application"""
        print("🖥️  Building Electron application...")
        
        try:
            subprocess.run(["npm", "run", "build-electron"], check=True, cwd=str(self.root_path), shell=True)
            print("✅ Electron app build completed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Electron app build failed: {e}")
            return False
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js and npm first.")
            return False
    
    def create_portable_version(self):
        """Create a portable version with Python backend"""
        print("📦 Creating portable version...")
        
        portable_path = self.dist_path / "portable"
        portable_path.mkdir(parents=True, exist_ok=True)
        
        # Copy backend
        backend_dest = portable_path / "backend"
        shutil.copytree(self.root_path / "backend", backend_dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        
        # Copy frontend build
        frontend_dest = portable_path / "frontend"
        shutil.copytree(self.frontend_path / "build", frontend_dest)
        
        # Copy launcher
        shutil.copy2(self.root_path / "app-launcher.py", portable_path / "run-app.py")
        
        # Copy requirements.txt if it exists
        backend_req = self.root_path / "backend" / "requirements.txt"
        if backend_req.exists():
            shutil.copy2(backend_req, portable_path / "requirements.txt")
        
        # Create batch file for Windows
        batch_content = """@echo off
echo Starting Breast Cancer AI Platform...
echo.
echo Installing Python dependencies...
pip install -r requirements.txt
echo.
echo Starting application...
python run-app.py
pause"""
        
        with open(portable_path / "run-app.bat", "w") as f:
            f.write(batch_content)
        
        # Create shell script for Unix
        shell_content = """#!/bin/bash
echo "Starting Breast Cancer AI Platform..."
echo
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
echo
echo "Starting application..."
python3 run-app.py"""
        
        with open(portable_path / "run-app.sh", "w") as f:
            f.write(shell_content)
        
        # Make shell script executable
        os.chmod(portable_path / "run-app.sh", 0o755)
        
        # Create README for portable version
        readme_content = """# Breast Cancer AI Platform - Portable Version

## Quick Start

### Windows:
1. Double-click `run-app.bat`
2. Wait for dependencies to install
3. The application will start automatically

### Linux/Mac:
1. Open terminal in this directory
2. Run: `./run-app.sh`
3. Wait for dependencies to install
4. The application will start automatically

## Manual Setup (if needed):
1. Install Python dependencies: `pip install -r requirements.txt`
2. Run the application: `python run-app.py`

## Requirements:
- Python 3.7 or higher
- Internet connection (for first-time dependency installation)

## Troubleshooting:
- If you get permission errors on Linux/Mac, run: `chmod +x run-app.sh`
- If Python is not found, make sure Python is installed and in your PATH
- For dependency issues, try: `pip install --upgrade pip` then retry
"""
        
        with open(portable_path / "README.md", "w") as f:
            f.write(readme_content)
        
        print("✅ Portable version created")
        return True
    
    def show_build_info(self):
        """Show information about the built application"""
        print("\n" + "=" * 60)
        print("🎉 BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        if self.dist_path.exists():
            print(f"\n📁 Build artifacts location: {self.dist_path}")
            
            # List built files
            for item in self.dist_path.iterdir():
                if item.is_file():
                    size = item.stat().st_size / (1024 * 1024)  # MB
                    print(f"   📄 {item.name} ({size:.1f} MB)")
                elif item.is_dir():
                    print(f"   📁 {item.name}/")
        
        print("\n🚀 How to use:")
        print("   Desktop App: Install the generated installer")
        print("   Portable: Run the files in dist/portable/")
        print("   Web Version: python app-launcher.py --web")
        
        print("\n📋 Distribution options:")
        print("   • Desktop installer (Windows/Mac/Linux)")
        print("   • Portable version (no installation required)")
        print("   • Web deployment (host on server)")
    
    def build_all(self):
        """Build everything"""
        print("🏥 Breast Cancer AI Platform - Build Script")
        print("=" * 50)
        
        steps = [
            ("Cleaning previous builds", self.clean_build),
            ("Installing dependencies", self.install_dependencies),
            ("Building frontend", self.build_frontend),
            ("Creating portable version", self.create_portable_version)
        ]
        
        # Try Electron build but don't fail if it doesn't work
        print(f"\n🔄 Building Electron app...")
        if not self.build_electron_app():
            print("⚠️  Electron build failed (likely due to Windows permissions)")
            print("   Continuing with portable version only...")
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            if not step_func():
                print(f"❌ Build failed at: {step_name}")
                return False
        
        self.show_build_info()
        return True

def main():
    builder = AppBuilder()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--clean":
            builder.clean_build()
            return True
        elif sys.argv[1] == "--frontend-only":
            return builder.build_frontend()
        elif sys.argv[1] == "--help":
            print("Breast Cancer AI Platform Build Script")
            print("\nUsage:")
            print("  python build-app.py              # Build everything")
            print("  python build-app.py --clean      # Clean build artifacts")
            print("  python build-app.py --frontend-only  # Build frontend only")
            print("  python build-app.py --help       # Show this help")
            return True
    
    # Default: build everything
    return builder.build_all()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)