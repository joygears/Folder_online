const { app, components,BrowserWindow,ipcMain } = require('electron');
const parseMain = require('./parse');
const convertMain = require('./convert');

  // 设置非沙盒化
  app.commandLine.appendSwitch('--no-sandbox')
// 获取命令行参数数组
const commandLineArgs = process.argv;

// 获取应用程序参数（不包括 Electron 内部参数）
const appArgs = commandLineArgs.slice(2);

//let url = appArgs[0]
const base64String = appArgs[0]

// 将Base64字符串解码为Buffer
const decodedBuffer = Buffer.from(base64String, 'base64');
// 将Buffer转换为字符串
const decodedString = decodedBuffer.toString('utf-8');

console.log("decodedString:",decodedString)
 let jsonObject;
try {
  jsonObject = JSON.parse(decodedString);
} catch (error) {
  console.error("Error parsing JSON:", error.message);
}

if(jsonObject['mode']=="parse")
  parseMain.parseMain(jsonObject);
else if(jsonObject['mode']=="convert")
  convertMain.convertMain(jsonObject);


