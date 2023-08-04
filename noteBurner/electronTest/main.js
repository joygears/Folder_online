const { app, components,BrowserWindow } = require('electron');
const path = require('path')
const fs = require("fs")
let mainWindow;
app.commandLine.appendSwitch('--no-sandbox')
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
  webPreferences: {
    
	contextIsolation: true,
    },
  });
// Load Netflix URL
  mainWindow.loadURL('https://www.netflix.com/watch/80991329?trackId=255824129&tctx=0%2C0%2Cb7d1867f-9dea-49a6-817e-55b09fc7fc1f-68236850%2Cb7d1867f-9dea-49a6-817e-55b09fc7fc1f-68236850%7C2%2Cunknown%2C%2C%2CtitlesResults%2C80991329%2CVideo%3A80991329%2CminiDpPlayButton');
  //mainWindow.webContents.openDevTools()
  //mainWindow.webContents.on("did-finish-load", function() {
 //const js = fs.readFileSync(path.join(__dirname, 'netflixHook.js')).toString();
//mainWindow.webContents.executeJavaScript(js);

//});
}

app.whenReady().then(async () => {
  await components.whenReady();
  console.log('components ready:', components.status());
  createWindow();
});
