const {app, components, BrowserWindow} = require('electron');

function createWindow () {
  const mainWindow = new BrowserWindow();
  mainWindow.loadURL('https://www.netflix.com/browse');
}

app.whenReady().then(async () => {
  await components.whenReady();
  console.log('components ready', components.status());
  createWindow();
});
