const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  setManifest: (data) => ipcRenderer.send('set-manifest', data)
})