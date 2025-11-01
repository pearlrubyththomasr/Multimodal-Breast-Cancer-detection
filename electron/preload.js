const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Navigation
  navigate: (path) => ipcRenderer.send('navigate', path),
  
  // App info
  getVersion: () => ipcRenderer.invoke('get-version'),
  
  // Platform info
  getPlatform: () => process.platform,
  
  // Window controls
  minimize: () => ipcRenderer.send('minimize-window'),
  maximize: () => ipcRenderer.send('maximize-window'),
  close: () => ipcRenderer.send('close-window'),
  
  // Listen to navigation events
  onNavigate: (callback) => ipcRenderer.on('navigate', callback)
});