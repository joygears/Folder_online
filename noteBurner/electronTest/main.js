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
  mainWindow.loadURL('https://www.netflix.com/browser');
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
