const { app, BrowserWindow, components,ipcMain } = require('electron');
const path = require('path');
const fs = require("fs");
const WebSocket = require('ws');
let mainWindow;
let wsClient;
let searchWindow;
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
 // Create WebSocket client
  wsClient = new WebSocket('ws://127.0.0.1:8012');

  // WebSocket client event handlers
  wsClient.on('open', () => {
    console.log('WebSocket connection opened');
   
  });
function waitForThreeSeconds() {
	if(searchWindow!=null){
	searchWindow.close();
	searchWindow = null;
	}
	
}
 wsClient.on('message', (message) => {
    //console.log('Received message from WebSocket server:', message.toString('utf8'));
	message = message.toString('utf8');
	if (message.startsWith("initFinished"))
	{
		if(searchWindow!=null)
			setTimeout(waitForThreeSeconds, 3000);
	}
else{
	mainWindow.webContents.send('progress', parseFloat(message));
	}	
	
    // Handle the received message here as needed
    // For example, update the UI or perform some actions based on the message content
  });

  wsClient.on('close', () => {
    console.log('WebSocket connection closed');
  });
  
function handleSetManifest (event, data) {
  const webContents = event.sender
	input={}
	input.video=data.result.video_tracks[0]
	input.audio=data.result.audio_tracks[0]
	const jsonString = JSON.stringify(input);
	wsClient.send('convert:'+Buffer.from(jsonString).toString('base64'));
	
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




ipcMain.on('search', (event, searchTerm) => {
  // In this example, we will open a new window with the search term as the URL
   searchWindow = new BrowserWindow({
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