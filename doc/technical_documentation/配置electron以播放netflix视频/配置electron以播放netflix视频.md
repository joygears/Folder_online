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

  ```json
  {
  "name": "netflix_browser",
  "version": "1.0.0",
  "main": "main.js",
  "license": "MIT",
  "scripts" : { "start" : "electron ./main.js --no-sandbox" }
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

- 安装electron-builder

 ~~~
 npm install -g electron-builder --arch=ia32
 ~~~

- 配置electron-builder

修改package.json

~~~josn
{
  "name": "netflix_browser",
  "version": "1.0.0",
  "main": "main.js",
  "license": "MIT",
  "scripts": {
   "start" : "electron ./main.js --no-sandbox",
    "pack": "electron-builder --dir",
    "package": "electron-packager . --out ./OutApp --overwrite",
    "dist": "electron-builder --win --ia32"
  },

  "devDependencies": {
    "electron": "github:castlabs/electron-releases#v25.0.0+wvcus"
  }
}

~~~

- 执行打包

~~~bash
yarn dist
~~~

很不幸会报错

~~~bash
$ electron-builder --win --ia32
  • electron-builder  version=24.6.3 os=10.0.19044
  • description is missed in the package.json  appPackageFile=D:\Users\Downloads\project\st\Folder_online\doc\technical_documentation\netflix_browser\package.json
  • author is missed in the package.json  appPackageFile=D:\Users\Downloads\project\st\Folder_online\doc\technical_documentation\netflix_browser\package.json
  • writing effective config  file=dist\builder-effective-config.yaml
  • packaging       platform=win32 arch=ia32 electron=25.0.0+wvcus appOutDir=dist\win-ia32-unpacked
  ⨯ cannot resolve https://github.com/electron/electron/releases/download/v25.0.0+wvcus/electron-v25.0.0+wvcus-win32-ia32.zip: status code 404
github.com/develar/app-builder/pkg/download.(*Downloader).follow
        /Volumes/data/Documents/app-builder/pkg/download/downloader.go:237
github.com/develar/app-builder/pkg/download.(*Downloader).DownloadNoRetry
        /Volumes/data/Documents/app-builder/pkg/download/downloader.go:128
github.com/develar/app-builder/pkg/download.(*Downloader).Download
        /Volumes/data/Documents/app-builder/pkg/download/downloader.go:112
github.com/develar/app-builder/pkg/electron.(*ElectronDownloader).doDownload
        /Volumes/data/Documents/app-builder/pkg/electron/electronDownloader.go:192
github.com/develar/app-builder/pkg/electron.(*ElectronDownloader).Download
        /Volumes/data/Documents/app-builder/pkg/electron/electronDownloader.go:177
github.com/develar/app-builder/pkg/electron.downloadElectron.func1.1
        /Volumes/data/Documents/app-builder/pkg/electron/electronDownloader.go:73
github.com/develar/app-builder/pkg/util.MapAsyncConcurrency.func2
        /Volumes/data/Documents/app-builder/pkg/util/async.go:68
runtime.goexit
        /usr/local/Cellar/go/1.17/libexec/src/runtime/asm_amd64.s:1581
  ⨯ C:\Users\Administrator\AppData\Roaming\npm\node_modules\electron-builder\node_modules\app-builder-bin\win\x64\app-builder.exe process failed ERR_ELECTRON_BUILDER_CANNOT_EXECUTE
Exit code:
1  failedTask=build stackTrace=Error: C:\Users\Administrator\AppData\Roaming\npm\node_modules\electron-builder\node_modules\app-builder-bin\win\x64\app-builder.exe process failed ERR_ELECTRON_BUILDER_CANNOT_EXECUTE
Exit code:
1
    at ChildProcess.<anonymous> (C:\Users\Administrator\AppData\Roaming\npm\node_modules\electron-builder\node_modules\builder-util\src\util.ts:250:14)
    at Object.onceWrapper (node:events:628:26)
    at ChildProcess.emit (node:events:513:28)
    at ChildProcess.cp.emit (C:\Users\Administrator\AppData\Roaming\npm\node_modules\electron-builder\node_modules\cross-spawn\lib\enoent.js:34:29)
    at maybeClose (node:internal/child_process:1091:16)
    at Process.ChildProcess._handle.onexit (node:internal/child_process:302:5)
error Command failed with exit code 1.
info Visit https://yarnpkg.com/en/docs/cli/run for documentation about this command.
~~~

去[electron-release官网]([castlabs/electron-releases: castLabs Electron for Content Security (github.com)](https://github.com/castlabs/electron-releases))下载对应版本的`electron-v25.0.0+wvcus-win32-ia32.zip`,放入`%LOCALAPPDATA%/electron/Cache`，再执行一次`yarn dist`即可

> 参考资料 [Electron使用electron-builder打包时下载electron失败或慢的解决方案_size=71 mb parts=8_WMSmile的博客-CSDN博客](https://blog.csdn.net/wm9028/article/details/114583011)

打包完后在`dist\win-ia32-unpacked`文件夹，

### 进行EVS签名

~~~bash
pip install --upgrade castlabs-evs
~~~

~~~
python -m castlabs_evs.account signup
~~~

填入邮箱，密码

~~~
python -m castlabs_evs.vmp sign-pkg path/to/package-directroy
~~~

> 注意 如果你用的是python3.7 使用系统代理会有bug，记得关闭系统代理，使用 Proxifier 之类的流量转发代理进行联网

> 参考资料 [EVS · castlabs/electron-releases Wiki (github.com)](https://github.com/castlabs/electron-releases/wiki/EVS)

