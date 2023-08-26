const { app, components,BrowserWindow,ipcMain } = require('electron');
const path = require('path')
const fs = require("fs")

function parseMain(jsonObject){
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
    //mainWindow.webContents.openDevTools()
    mainWindow.webContents.on("did-finish-load", function() {
   const js = fs.readFileSync(path.join(__dirname, 'netflixHook.js')).toString();
    mainWindow.webContents.executeJavaScript(js);

  });
  }

  function handleSetManifest (event, data) {
    const webContents = event.sender
    input={"type":"finished","msg":data}
    const jsonString = JSON.stringify(input);
    console.log(jsonString)
    mainWindow.close();
  }

  app.whenReady().then(async () => {
    await components.whenReady();
    console.log('components ready:', components.status());
    ipcMain.on('set-manifest', handleSetManifest)
    createWindow();
  });


  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
    app.quit();
    }
  });

}

module.exports = {
  parseMain:parseMain
};