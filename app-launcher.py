#!/usr/bin/env python3
"""
Breast Cancer AI Platform - Desktop App Launcher
Automatically starts backend and launches the Electron app
"""

import os
import sys
import subprocess
import time
import threading
import signal
import webbrowser
from pathlib import Path

class AppLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.electron_process = None
        self.running = True
        self.npm_cmd = self._find_npm_command()
    
    def _find_npm_command(self):
        """Find the correct npm command to use"""
        npm_commands = ["npm", r"C:\Program Files\nodejs\npm.cmd"]
        
        for npm_cmd in npm_commands:
            try:
                subprocess.run([npm_cmd, "--version"], check=True, capture_output=True)
                return npm_cmd
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        return "npm"  # fallback
        
    def start_backend(self):
        """Start the Python backend server"""
        print("🚀 Starting AI Backend Server...")
        try:
            backend_path = Path(__file__).parent / "backend" / "main.py"
            self.backend_process = subprocess.Popen([
                sys.executable, str(backend_path)
            ], cwd=str(Path(__file__).parent / "backend"))
            print("✅ Backend server started successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
    
    def start_electron_app(self):
        """Start the Electron desktop app"""
        print("🖥️  Starting Desktop Application...")
        try:
            # Wait a moment for backend to fully start
            time.sleep(2)
            
            self.electron_process = subprocess.Popen([
                self.npm_cmd, "run", "electron"
            ], cwd=str(Path(__file__).parent))
            print("✅ Desktop application launched successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to start desktop app: {e}")
            return False
    
    def start_web_version(self):
        """Start the web version instead of desktop app"""
        print("🌐 Starting Web Version...")
        try:
            # Start frontend dev server
            self.frontend_process = subprocess.Popen([
                self.npm_cmd, "start"
            ], cwd=str(Path(__file__).parent / "frontend"))
            
            # Wait for frontend to start, then open browser
            print("⏳ Waiting for web server to start...")
            time.sleep(5)
            webbrowser.open("http://localhost:3000")
            print("✅ Web version started - opened in browser")
            return True
        except Exception as e:
            print(f"❌ Failed to start web version: {e}")
            return False
    
    def cleanup(self):
        """Clean up all processes"""
        print("\n🧹 Cleaning up processes...")
        
        processes = [
            ("Backend", self.backend_process),
            ("Frontend", self.frontend_process), 
            ("Electron", self.electron_process)
        ]
        
        for name, process in processes:
            if process:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ {name} stopped")
                except subprocess.TimeoutExpired:
                    process.kill()
                    print(f"🔥 {name} force killed")
                except Exception as e:
                    print(f"⚠️  Error stopping {name}: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n📡 Received signal {signum}")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        # Check Node.js and npm
        try:
            subprocess.run(["node", "--version"], check=True, capture_output=True)
            print("✅ Node.js found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Node.js not found. Please install Node.js first.")
            return False
        
        # Check npm
        try:
            subprocess.run([self.npm_cmd, "--version"], check=True, capture_output=True)
            print("✅ npm found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ npm not found. Please install Node.js first.")
            return False
        
        # Check if npm packages are installed
        if not (Path(__file__).parent / "node_modules").exists():
            print("📦 Installing npm dependencies...")
            try:
                subprocess.run([self.npm_cmd, "install"], check=True, cwd=str(Path(__file__).parent))
                print("✅ Dependencies installed")
            except subprocess.CalledProcessError:
                print("❌ Failed to install dependencies")
                return False
        
        # Check frontend dependencies
        frontend_path = Path(__file__).parent / "frontend"
        if not (frontend_path / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            try:
                subprocess.run([self.npm_cmd, "install"], check=True, cwd=str(frontend_path))
                print("✅ Frontend dependencies installed")
            except subprocess.CalledProcessError:
                print("❌ Failed to install frontend dependencies")
                return False
        
        return True
    
    def run_desktop_app(self):
        """Run the desktop application"""
        print("🏥 Breast Cancer AI Platform - Desktop App")
        print("=" * 50)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Start backend
        if not self.start_backend():
            return False
        
        # Start desktop app
        if not self.start_electron_app():
            self.cleanup()
            return False
        
        # Wait for processes
        try:
            print("\n✨ Application is running!")
            print("💡 Close the desktop app window to exit")
            print("🔄 Press Ctrl+C to force quit")
            
            # Wait for electron process to finish
            if self.electron_process:
                self.electron_process.wait()
                
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
        
        return True
    
    def run_web_app(self):
        """Run the web application"""
        print("🏥 Breast Cancer AI Platform - Web Version")
        print("=" * 50)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Start backend
        if not self.start_backend():
            return False
        
        # Start web version
        if not self.start_web_version():
            self.cleanup()
            return False
        
        # Wait for processes
        try:
            print("\n✨ Web application is running!")
            print("🌐 Open http://localhost:3000 in your browser")
            print("🔄 Press Ctrl+C to stop")
            
            # Keep running until interrupted
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
        
        return True

def main():
    launcher = AppLauncher()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--web":
            return launcher.run_web_app()
        elif sys.argv[1] == "--help":
            print("Breast Cancer AI Platform Launcher")
            print("\nUsage:")
            print("  python app-launcher.py        # Launch desktop app")
            print("  python app-launcher.py --web  # Launch web version")
            print("  python app-launcher.py --help # Show this help")
            return True
    
    # Default: run desktop app
    return launcher.run_desktop_app()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)