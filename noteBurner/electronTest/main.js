const { app, components,BrowserWindow } = require('electron');
const path = require('path')
const fs = require("fs")
let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    webPreferences: {
      nodeIntegration: true
    },

  });
// Load Netflix URL
  mainWindow.loadURL('https://www.netflix.com/watch/80210938?trackId=254015180&tctx=0%2C0%2C22898ff0-1c41-43eb-b390-bfe8c6bebbad-72361130%2CNES_ABA75BA61D6959C46E272C0D175353-951BB306AEF2A8-5D9479BF5C_p_1690129307742%2CNES_ABA75BA61D6959C46E272C0D175353_p_1690129307742%2C%2C%2C%2C%2CVideo%3A80197526%2CbillboardPlayButton');
  mainWindow.webContents.openDevTools()
  mainWindow.webContents.on("did-finish-load", function() {
 const js = fs.readFileSync(path.join(__dirname, 'netflixHook.js')).toString();
mainWindow.webContents.executeJavaScript(js);

});
}

app.whenReady().then(async () => {
  await components.whenReady();
  console.log('components ready:', components.status());
  createWindow();
});
