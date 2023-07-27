## 配置electron以播放netflix视频

### 创建项目

 - 安装yarn 
 
  ```bat
  npm install -g yarn
  ```
  
 - 初始化项目
  
  ```bat
  yarn init
  ```
 - 添加scripts脚本
 
  ```
  {
  "name": "netflix_browser",
  "version": "1.0.0",
  "main": "main.js",
  "license": "MIT",
  "scripts" : { "start" : "electron ./main.js" }
  }
  ```
 - 创建入口文件
 
 `main.js`
 ```js
 const {app, components, BrowserWindow} = require('electron');

function createWindow () {
  const mainWindow = new BrowserWindow();
  mainWindow.loadURL('https://www.netflix.com/browse');
}

app.whenReady().then(async () = {
  await components.whenReady();
  console.log('components ready', components.status());
  createWindow();
});
 ```
  
 ### 安装electron
 
 - 配置git ssh 密钥
 
 > [参考链接](https://www.cnblogs.com/yuqiliu/p/12551258.html)
 
 - 设置代理
 
 ```bat
 npm config edit
 ```
 
 在打开的文本中添加`proxy=http://<ip>:<port>/`
 
 
 - 安装EVS
 
 我的是32位的
 
 ```bat
 npm install "https://github.com/castlabs/electron-releases#v25.0.0+wvcus" --save-dev --arch=ia32
 ```  

### 打包项目
 ~~~
    
 ~~~
 
 