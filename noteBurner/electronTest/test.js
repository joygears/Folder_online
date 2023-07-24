const { app, BrowserWindow, components,ipcMain } = require('electron');
const path = require('path');
const fs = require("fs");
const WebSocket = require('ws');
let mainWindow;

function createWindow() {
mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
	nodeIntegration: true,
	contextIsolation: false,
      
}});

  mainWindow.loadFile('index.html');

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function handleSetManifest (event, title) {
  const webContents = event.sender
  const win = BrowserWindow.fromWebContents(webContents)
	 console.log(title);
}

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});


app.whenReady().then(async () => {
  await components.whenReady();
  console.log('components ready:', components.status());
  ipcMain.on('set-manifest', handleSetManifest)
  createWindow();
});

 // // Create WebSocket server
  // wsServer = new WebSocket.Server({ port: 8080 });

  // wsServer.on('connection', (socket) => {
    // console.log('WebSocket connection established');

    // // Handle messages from the renderer process
    // socket.on('message', (message) => {
      // console.log('Received from renderer:', message);

      // // Send response back to the renderer process
      // socket.send('Message received by server: ' + message);
    // });
  // });


ipcMain.on('search', (event, searchTerm) => {
  // In this example, we will open a new window with the search term as the URL
  const searchWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
    
	contextIsolation: true,
	 preload: path.join(__dirname, 'preload.js')
    },
  });

  // Load the search term as the URL in the new window
  searchWindow.loadURL(searchTerm);
  searchWindow.webContents.openDevTools();
  searchWindow.webContents.on("did-finish-load", function() {
 const js = fs.readFileSync(path.join(__dirname, 'netflixHook.js')).toString();
searchWindow.webContents.executeJavaScript(js);

});
});