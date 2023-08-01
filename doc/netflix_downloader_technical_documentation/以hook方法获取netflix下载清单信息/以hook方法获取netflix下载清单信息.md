## 以hook方法获取netflix下载清单信息

- `netflixHook.js`

  ~~~js
  
  const injection = () => {
    const WEBVTT = 'webvtt-lssdh-ios8';
    const MANIFEST_URL = "manifest";
    const forceSubs = localStorage.getItem('NSD_force-all-lang') !== 'false';
  
    // hijack JSON.parse and JSON.stringify functions
    ((parse, stringify) => {
      JSON.parse = function (text) {
        const data = parse(text);
        if (data && data.result && data.result.timedtexttracks && data.result.movieId) {
          window.dispatchEvent(new CustomEvent('netflix_sub_downloader_data', {detail: data.result}));
          console.log('manifest:')
          console.log(data)
          console.log(stringify(data))
  		window.electronAPI.setManifest(data)
        }
        return data;
      };
      JSON.stringify = function (data) {
        if (data && typeof data.url === 'string' && data.url.indexOf(MANIFEST_URL) > -1) {
          for (let v of Object.values(data)) {
            try {
              if (v.profiles)
                v.profiles.unshift(WEBVTT);
              if (v.showAllSubDubTracks != null && forceSubs)
                v.showAllSubDubTracks = true;
            }
            catch (e) {
              if (e instanceof TypeError)
                continue;
              else
                throw e;
            }
          }
          console.log('manifest_req:')
          console.log(data)
  		
        }
        if(data && typeof data.movieId === 'number') {
          try {
            let videoId = data.params.sessionParams.uiplaycontext.video_id;
            if(typeof videoId === 'number' && videoId !== data.movieId)
              window.dispatchEvent(new CustomEvent('netflix_sub_downloader_data', {detail: {id_override: [videoId, data.movieId]}}));
          }
          catch(ignore) {}
        }
        return stringify(data);
      };
    })(JSON.parse, JSON.stringify);
  }
  
  injection();
  
  ~~~

  

核心的代码主要在`netflixHook.js`中，上面主要是hook了`JSON.parse`和`JSON.stringify`两个函数以获取netflix的下载链接信息，获取到后通过`window.electronAPI.setManifest(data)`发送给主进程

接下来的问题是如何将`netflixHook.js`注入到渲染进程中呢

- `main.js`

~~~js
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
  searchWindow.webContents.on("did-finish-load", function() {
 const js = fs.readFileSync(path.join(__dirname, 'netflixHook.js')).toString();
searchWindow.webContents.executeJavaScript(js);
~~~

看上面的代码，在创建渲染进程窗口后，使用`webContents`组件，在网页DOM加载完毕(`did-finish-load`)时,通过`searchWindow.webContents.executeJavaScript`执行`netflixHook.js`，将hook代码注入进去

- `preload.js`

~~~js
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  setManifest: (data) => ipcRenderer.send('set-manifest', data)
})
~~~

在`preload.js`函数中将`setManifest`绑定到`electronAPI`中，方便渲染进程将下载链接信息传回