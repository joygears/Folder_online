const { app, components,BrowserWindow,ipcMain } = require('electron');
const path = require('path')
const fs = require("fs")

function convertMain(jsonObject){
  
  // 设置非沙盒化
  app.commandLine.appendSwitch('--no-sandbox')

  let mainWindow;

  // 获取所有环境变量
  const userDataPath = app.getPath('userData');

  const newPath = path.join(path.dirname(userDataPath), 'AnalyzeBrowser');
  app.setPath('userData', newPath);
  function createWindow() {
    mainWindow = new BrowserWindow({
      width: 1280,
      height: 720,
    webPreferences: {
      
    contextIsolation: true,
     preload: path.join(__dirname, 'preload.js')
      },
    });

  // Load Netflix URL
    mainWindow.loadURL(jsonObject['url']);
   
  }


  app.whenReady().then(async () => {
    await components.whenReady();
    console.log('components ready:', components.status());
    createWindow();
  });


  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
    app.quit();
    }
  });

}

module.exports = {
  convertMain:convertMain
};