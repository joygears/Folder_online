## 劫持widevinecdm.dll

### 禁用沙盒化

electron默认是开启[沙盒化]([进程沙盒化 | Electron (electronjs.org)](https://www.electronjs.org/zh/docs/latest/tutorial/sandbox))的,在沙盒化中那是啥也不能干，所以要关闭它

~~~js
app.commandLine.appendSwitch('--no-sandbox')
~~~

在入口文件中加入这一行代码就可以了

### 验证两个文件

~~~c++
 wstring dycWidevine = TEXT(R"(C:\Program Files (x86)\NoteBurner\NoteBurner Netflix Video Downloader\resources\com.noteburner.netflix\native\sig_files\widevinecdm.dll)");
    wstring sigWidevine = TEXT(R"(C:\Program Files (x86)\NoteBurner\NoteBurner Netflix Video Downloader\resources\com.noteburner.netflix\native\sig_files\widevinecdm.dll.sig)");
    // dycVfchm = TEXT(R"(C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe)");
    dycVfchm = TEXT(R"(C:\Program Files (x86)\NoteBurner\NoteBurner Netflix Video Downloader\resources\com.noteburner.netflix\native\sig_files\vfchm.dll)");
    wstring sigVfchm = TEXT(R"(C:\Program Files (x86)\NoteBurner\NoteBurner Netflix Video Downloader\resources\com.noteburner.netflix\native\sig_files\vfchm.dll.sig)");
    verifyWrap wrap;
   
    GetFileAttributeshooker.hook(::GetFileAttributesW, fake_GetFileAttributesW);
    GetModuleFileNamehooker.hook(::GetModuleFileNameW, fake_GetModuleFileNameW);

    
    
    HANDLE HDycWidevinecdm = CreateFile(dycWidevine.c_str(), GENERIC_READ, 1, 0, 3, 0x80, 0);
    HANDLE HSigWidevinecdm = CreateFile(sigWidevine.c_str(), GENERIC_READ, 1, 0, 3, 0x80, 0);
    HANDLE hFVfchm = CreateFile(dycVfchm.c_str(), GENERIC_READ, 1, 0, 3, 0x80, 0);
    HANDLE hSigVfchm = CreateFile(sigVfchm.c_str(), GENERIC_READ, 1, 0, 3, 0x80, 0);

    Log("open file, %p, %p, %p, %p\n", HDycWidevinecdm, HSigWidevinecdm, hFVfchm, hSigVfchm);


    wrap.chDycVfchm = dycVfchm.c_str();
    wrap.hFVfchm = hFVfchm;
    wrap.hSigVfchm = hSigVfchm;
    wrap.chdycWidevine = dycWidevine.c_str();
    wrap.HDycWidevinecdm = HDycWidevinecdm;
    wrap.HSigWidevinecdm = HSigWidevinecdm;

   
    HMODULE hWidevine = LoadLibrary(dycWidevine.c_str());

    if(!hWidevine)
    Log("LoadLibrary widevinecdm.dll error  GetLasterror %d\n", GetLastError());
    
    _VerifyCdmHost_0 = (bool (*)(verifyWrap*, int flag))GetProcAddress(hWidevine, "VerifyCdmHost_0");
    _InitializeCdmModule_4 = (void (*)())GetProcAddress(hWidevine, "InitializeCdmModule_4");
    _CreateCdmInstance = (void* (*)(int interface_version, const char* key_system, uint32_t key_system_len,
            void* host_function, void* extra_data))GetProcAddress(hWidevine, "CreateCdmInstance");
    _DeinitializeCdmModule = (void (*)())GetProcAddress(hWidevine, "DeinitializeCdmModule");
    _GetCdmVersion = (char * (*)())GetProcAddress(hWidevine, "GetCdmVersion");

    Log("load widevinecdm success, %p, %p, %p, %p \n", _InitializeCdmModule_4, _CreateCdmInstance, _DeinitializeCdmModule, _GetCdmVersion);

    bool retcode = _VerifyCdmHost_0(&wrap, 2);

    Log("widevine VerifyCdmHost_0 retcode value %d\n",retcode);
~~~



调用_VerifyCdmHost_0进行验证，参数位`verifyWrap`,`verifyCount`,`verifyWrap`的定义如下

~~~c++
struct verifyWrap {
	const wchar_t* chDycVfchm;
	HANDLE hFVfchm;
	HANDLE hSigVfchm;
	const wchar_t* chdycWidevine;
	HANDLE HDycWidevinecdm;
	HANDLE HSigWidevinecdm;
};
~~~

- chDycVfchm 

  vfchm.dll的路径

- hFVfchm

  vfchm.dll的文件句柄

- hSigVfchm
  vfchm.dll.sig的文件句柄
  
- chdycWidevine 

  widevinecdm.dll的路径

- HDycWidevinecdm

  widevinecdm.dll的文件句柄

- HSigWidevinecdm
  widevinecdm.dll.sig的文件句柄

这两个文件怎么获得呢，`vfchm.dll`和`vfchm.dll.sig`可以用你经过`EVS`签名的主程序和签名文件改个名字而得来(也可以直接使用竞品的)，`widevinecdm.dll`和`widevinecdm.dll.sig` 在第一次启动[ECS]([castlabs/electron-releases: castLabs Electron for Content Security (github.com)](https://github.com/castlabs/electron-releases))时,`electron`在`%APPDATA%\<appName>`处创建WidevineCdm文件夹，而`widevinecdm.dll`的路径就在`%APPDATA%\<appName>\WidevineCdm\4.10.2652.2\_platform_specific\win_x86`

### hook 两个函数

对`GetModuleFileNameW`和`GetFileAttributesW`进行hook，hook代码如下

```c++
 GetFileAttributeshooker.hook(::GetFileAttributesW, fake_GetFileAttributesW);
 GetModuleFileNamehooker.hook(::GetModuleFileNameW, fake_GetModuleFileNameW);
```

~~~c++
DWORD __stdcall fake_GetFileAttributesW(LPCWSTR lpFileName) {
    if (lpFileName)
        Log("GetFileAttributesW called, file %S", lpFileName);

    if (wcsstr(lpFileName, TEXT("cshell.dll")) == 0 && wcsstr(lpFileName, TEXT("decrypt.dll")) == 0 && wcsstr(lpFileName, TEXT("widevinecdm.dll")) == 0) {
        return  ((MyGetFileAttributes)GetFileAttributeshooker.originalFunction())(lpFileName);
    }
    Log("GetFileAttributesW called, file %S, %08x", lpFileName, ((MyGetFileAttributes)GetFileAttributeshooker.originalFunction())(lpFileName));

    return 0x80;
}

DWORD __stdcall  fake_GetModuleFileNameW(
    HMODULE hModule,
    LPWSTR  lpFilename,
    DWORD   nSize
) {
    wchar_t absolutePath[MAX_PATH];
    GetFullPathName(dycVfchm.c_str(), MAX_PATH, absolutePath, nullptr);

    DWORD result = ((MyGetModuleFileName)GetModuleFileNamehooker.originalFunction())(hModule, lpFilename, nSize);
    if (result) {
        wstring originFileName = lpFilename;

        if (wcsstr(lpFilename, L"")) {
            Log("GetModuleFileNameW called, hook %S to %S", originFileName.c_str(), absolutePath);
            wcscpy(lpFilename, absolutePath);
        }
    }
    return result;
}
~~~

至此，你就可以放心进行劫持了