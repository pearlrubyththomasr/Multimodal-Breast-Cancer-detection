#!/usr/bin/env python3
"""
NPM Installation Fixer for Breast Cancer AI Platform
Helps diagnose and fix npm installation issues
"""

import subprocess
import sys
import os
import platform

def check_system():
    """Check system information"""
    print("🔍 System Information")
    print("-" * 30)
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Architecture: {platform.machine()}")
    print()

def check_node_installation():
    """Detailed Node.js installation check"""
    print("🔍 Node.js Installation Check")
    print("-" * 30)
    
    try:
        # Check Node.js
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js: {version}")
            
            # Check if version is compatible
            version_num = version.replace('v', '').split('.')[0]
            if int(version_num) >= 14:
                print(f"✅ Version compatible (>= 14)")
            else:
                print(f"⚠️ Version may be too old (< 14)")
            
            return True
        else:
            print(f"❌ Node.js command failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Node.js not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Node.js command timed out")
        return False
    except Exception as e:
        print(f"❌ Node.js check error: {e}")
        return False

def check_npm_installation():
    """Detailed npm installation check"""
    print("\n🔍 npm Installation Check")
    print("-" * 30)
    
    try:
        # Check npm
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ npm: {version}")
            return True
        else:
            print(f"❌ npm command failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ npm not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ npm command timed out")
        return False
    except Exception as e:
        print(f"❌ npm check error: {e}")
        return False

def check_alternative_managers():
    """Check for alternative package managers"""
    print("\n🔍 Alternative Package Managers")
    print("-" * 30)
    
    managers = [
        ('npx', 'npx --version'),
        ('yarn', 'yarn --version'),
        ('pnpm', 'pnpm --version')
    ]
    
    available = []
    
    for name, cmd in managers:
        try:
            result = subprocess.run(cmd.split(), 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ {name}: {version}")
                available.append(name)
            else:
                print(f"❌ {name}: Not working")
        except:
            print(f"❌ {name}: Not found")
    
    return available

def suggest_solutions(node_ok, npm_ok, alternatives):
    """Suggest solutions based on findings"""
    print("\n💡 Recommended Solutions")
    print("-" * 30)
    
    if not node_ok:
        print("🔧 Node.js Issues:")
        print("   1. Install Node.js from https://nodejs.org/")
        print("   2. Choose LTS version (includes npm)")
        print("   3. Restart terminal after installation")
        if platform.system() == "Windows":
            print("   4. Or use: winget install OpenJS.NodeJS")
        return
    
    if not npm_ok:
        print("🔧 npm Issues (Node.js is installed):")
        print("   1. Reinstall Node.js (recommended - includes npm)")
        print("   2. Or repair npm installation:")
        
        if platform.system() == "Windows":
            print("      - Download npm from https://nodejs.org/")
            print("      - Or use: npm install -g npm@latest")
        else:
            print("      - Run: curl -L https://www.npmjs.com/install.sh | sh")
            print("      - Or: sudo npm install -g npm@latest")
        
        if alternatives:
            print(f"   3. Use alternative: {', '.join(alternatives)}")
            if 'yarn' in alternatives:
                print("      - yarn install (instead of npm install)")
                print("      - yarn start (instead of npm start)")
            if 'npx' in alternatives:
                print("      - npx npm install")
                print("      - npx react-scripts start")
    
    if node_ok and npm_ok:
        print("✅ Both Node.js and npm are working!")
        print("   You can proceed with frontend setup")

def test_npm_functionality():
    """Test if npm can actually install packages"""
    if not check_npm_installation():
        return False
    
    print("\n🧪 Testing npm Functionality")
    print("-" * 30)
    
    # Create a temporary directory for testing
    test_dir = "npm_test_temp"
    
    try:
        os.makedirs(test_dir, exist_ok=True)
        os.chdir(test_dir)
        
        # Try to initialize a package
        result = subprocess.run(['npm', 'init', '-y'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ npm init works")
            
            # Try to install a small package
            result = subprocess.run(['npm', 'install', 'lodash'], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ npm install works")
                return True
            else:
                print(f"❌ npm install failed: {result.stderr}")
                return False
        else:
            print(f"❌ npm init failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ npm test error: {e}")
        return False
    finally:
        # Clean up
        os.chdir('..')
        try:
            import shutil
            shutil.rmtree(test_dir, ignore_errors=True)
        except:
            pass

def provide_manual_instructions():
    """Provide manual setup instructions"""
    print("\n📋 Manual Setup Instructions")
    print("-" * 30)
    
    print("If automated fixes don't work, try manual setup:")
    print()
    print("1. Install Node.js:")
    print("   - Go to https://nodejs.org/")
    print("   - Download LTS version")
    print("   - Install with default options")
    print("   - Restart terminal")
    print()
    print("2. Verify installation:")
    print("   - node --version")
    print("   - npm --version")
    print()
    print("3. If npm still missing:")
    print("   - Reinstall Node.js")
    print("   - Or install yarn: npm install -g yarn")
    print()
    print("4. Frontend setup:")
    print("   - cd frontend")
    print("   - npm install (or yarn install)")
    print("   - npm start (or yarn start)")

def main():
    """Main diagnostic and fix function"""
    print("🔧 NPM Installation Fixer")
    print("=" * 40)
    
    # System check
    check_system()
    
    # Check installations
    node_ok = check_node_installation()
    npm_ok = check_npm_installation()
    alternatives = check_alternative_managers()
    
    # Test npm functionality if available
    if npm_ok:
        npm_functional = test_npm_functionality()
        if not npm_functional:
            npm_ok = False
    
    # Provide solutions
    suggest_solutions(node_ok, npm_ok, alternatives)
    
    # Manual instructions
    provide_manual_instructions()
    
    print("\n" + "=" * 40)
    if node_ok and npm_ok:
        print("🎉 Ready to proceed with frontend setup!")
        print("   Run: python start_frontend.py")
    else:
        print("🔧 Please fix Node.js/npm installation first")
        print("   Then run: python start_frontend.py")

if __name__ == "__main__":
    main()