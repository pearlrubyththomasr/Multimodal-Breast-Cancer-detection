# 🚀 Quick Fix for npm Issue

## Your Current Issue
- ✅ Node.js v23.1.0 is installed
- ❌ npm is not found/working

## 🔧 Immediate Solutions (Try in Order)

### Solution 1: Reinstall Node.js (Recommended)
```bash
# This will fix npm automatically
```
1. Go to https://nodejs.org/
2. Download the **LTS version** (not v23.1.0 - that's too new)
3. Install it (will include npm)
4. Restart PowerShell
5. Test: `npm --version`

### Solution 2: Use PowerShell as Administrator
```powershell
# Run PowerShell as Administrator, then:
npm --version
```

### Solution 3: Fix npm Path (Windows)
```powershell
# Check if npm exists in Node.js folder
where node
# Look for npm.cmd in the same folder

# If found, add to PATH or run directly:
C:\Program Files\nodejs\npm.cmd --version
```

### Solution 4: Install npm Separately
```powershell
# Using winget (Windows 10/11)
winget install OpenJS.NodeJS

# This will install both Node.js and npm
```

## 🚀 Quick Test
After fixing npm, test it:
```bash
npm --version
node --version
```

## 🎯 Then Continue with Frontend
Once npm works:
```bash
python start_frontend.py
```

## 🔧 Alternative: Manual Frontend Setup
If npm still doesn't work:

```bash
# 1. Go to frontend directory
cd frontend

# 2. Try these commands in order:
npm install
# OR
npx npm install  
# OR
yarn install

# 3. Start the server:
npm start
# OR
yarn start
```

## 🆘 Still Not Working?

Run the diagnostic tool:
```bash
python fix_npm.py
```

This will:
- ✅ Check your system
- ✅ Diagnose the exact issue  
- ✅ Provide specific solutions
- ✅ Test npm functionality

## 💡 Pro Tip
The issue is likely that Node.js v23.1.0 is very new and may have npm compatibility issues. **Installing the LTS version (v20.x) usually fixes this.**

---

**Next Step**: Try Solution 1 (reinstall Node.js LTS), then run `python start_frontend.py` again.