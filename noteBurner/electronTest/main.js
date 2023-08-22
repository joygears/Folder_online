const { app, components,BrowserWindow,ipcMain } = require('electron');
const path = require('path')
const fs = require("fs")

// 获取命令行参数数组
const commandLineArgs = process.argv;

// 获取应用程序参数（不包括 Electron 内部参数）
const appArgs = commandLineArgs.slice(2);

let url = appArgs[0]
let mainWindow;
app.commandLine.appendSwitch('--no-sandbox')
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
  mainWindow.loadURL(url);
  //mainWindow.webContents.openDevTools()
  mainWindow.webContents.on("did-finish-load", function() {
 const js = fs.readFileSync(path.join(__dirname, 'netflixHook.js')).toString();
  mainWindow.webContents.executeJavaScript(js);

});
}

function handleSetManifest (event, data) {
  const webContents = event.sender
  input={}
  input.video=data.result.video_tracks[0]
  input.audio=data.result.audio_tracks[0]
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