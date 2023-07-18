const {app, components, BrowserWindow} = require('electron');

function createWindow () {
  const mainWindow = new BrowserWindow();
  mainWindow.loadURL('https://www.netflix.com/watch/81671428?trackId=254015180&tctx=0%2C0%2C4820e4c6-15ee-4eff-adf2-d7040759e242-53401222%2CNES_D0D2EFBEF842DA67B4FEAE6CC4A7FE-951BB306AEF2A8-3C293B84E7_p_1689674174359%2CNES_D0D2EFBEF842DA67B4FEAE6CC4A7FE_p_1689674174359%2C%2C%2C%2C%2CVideo%3A81671426%2CbillboardPlayButton');
// mainWindow.loadURL('chrome://components');
}

app.whenReady().then(async () => {
  await components.whenReady();
  console.log('components ready:', components.status());
  createWindow();
});