## 劫持widevinecdm.dll

### 禁用沙盒化

electron默认是开启[沙盒化]([进程沙盒化 | Electron (electronjs.org)](https://www.electronjs.org/zh/docs/latest/tutorial/sandbox))的,在沙盒化中那是啥也不能干，所以要关闭它

~~~js
app.commandLine.appendSwitch('--no-sandbox')
~~~

在入口文件中加入这一行代码就可以了

在第一次启动[ECS]([castlabs/electron-releases: castLabs Electron for Content Security (github.com)](https://github.com/castlabs/electron-releases))时,`electron`在`%APPDATA%\<appName>`处创建WidevineCdm文件夹，而`widevinecdm.dll`的路径就在`%APPDATA%\<appName>\WidevineCdm\4.10.2652.2\_platform_specific\win_x86`

劫持的思路主要时创建一个同名的widevinecdm.dll,并且实现所有的导出函数



