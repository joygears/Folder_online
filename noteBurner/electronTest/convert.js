const { app, components,BrowserWindow,ipcMain } = require('electron');
const path = require('path')
const fs = require("fs")

function convertMain(jsonObject){
  

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

function CopyAllFiles(sourceDir, targetDir) {
    const files = fs.readdirSync(sourceDir);
    
    files.forEach(file => {
        const sourceFilePath = path.join(sourceDir, file);
        const targetFilePath = path.join(targetDir, file);

        try {
            // 同步方式复制文件
            fs.writeFileSync(targetFilePath, fs.readFileSync(sourceFilePath));
            console.log(`File ${file} copied successfully`);
        } catch (err) {
            console.error(`Error copying file ${file}:`, err);
        }
    });
}

function CopyTheHijackedDll() {
    const targetDir = path.join(app.getPath('userData'), 'WidevineCdm\\4.10.2557.0\\_platform_specific\\win_x86');
    const sourceDir = path.join(__dirname, '../widevinecdm');

    CopyAllFiles(sourceDir, targetDir);
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