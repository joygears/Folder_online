const {app, components, BrowserWindow} = require('electron');

app.commandLine.appendSwitch('--no-sandbox')

function createWindow () {
  const mainWindow = new BrowserWindow();
  mainWindow.loadURL('https://www.netflix.com/watch/80135737?trackId=254015180&tctx=0%2C0%2Cfb19f04d-8d55-48c5-a280-3e19c03229e0-36434688%2CNES_CD7808804E33D216EE3F3607A9522F-951BB306AEF2A8-80F3040924_p_1690784237045%2CNES_CD7808804E33D216EE3F3607A9522F_p_1690784237045%2C%2C%2C%2C%2CVideo%3A80135674%2CbillboardPlayButton');
}

app.whenReady().then(async () => {
  await components.whenReady();
  console.log('components ready', components.status());
  createWindow();
});
