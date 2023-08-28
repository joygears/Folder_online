const { app, components,BrowserWindow,ipcMain } = require('electron');
const path = require('path')
const fs = require("fs")

function convertMain(jsonObject){
  
  // 设置非沙盒化
  app.commandLine.appendSwitch('--no-sandbox')

  let mainWindow;

  // 设置AnalyzeBrowser为新的userData目录
  const userDataPath = app.getPath('userData');
  const newPath = path.join(path.dirname(userDataPath), 'AnalyzeBrowser');
  app.setPath('userData', newPath);




  app.whenReady().then(async () => {
    await components.whenReady();
    console.log('components ready:', components.status());
    CopyTheHijackedDll();
    createWindow();
  });


  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
    app.quit();
    }
  });

  function CopyTheHijackedDll(){
      const targetPath = path.join(app.getPath('userData'),'WidevineCdm\\4.10.2557.0\\_platform_specific\\win_x86\\widevinecdm.dll');
      const sourceDll =path.join(__dirname,'../widevinecdm.dll')
      try {
      // 同步方式复制文件
      fs.writeFileSync(targetPath, fs.readFileSync(sourceDll));
      console.log('File copied successfully');
      } catch (err) {
      console.error('Error copying file:', err);
    }
  }

    //创建窗口
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



}

module.exports = {
  convertMain:convertMain
};