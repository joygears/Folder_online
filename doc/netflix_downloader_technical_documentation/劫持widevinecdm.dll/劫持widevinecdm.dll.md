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

`fake_GetModuleFileNameW`的作用是将自身用来劫持的dll隐藏起来，我这里写的比较粗糙，直接把所有dll的路径都替换为`vfchm.dll`了

至此，你就可以放心进行劫持了



### 劫持导出函数

~~~c++
DLL_EXPORT void InitializeCdmModule_4()
{
   /* thread tr([]() {
        connectToServer("127.0.0.1", 8012);
        });
    tr.detach();
    Sleep(200);*/
    Log("InitializeCdmModule_4\n");
    _InitializeCdmModule_4();
}

DLL_EXPORT void DeinitializeCdmModule()
{
    Log("DeinitializeCdmModule\n");
    _DeinitializeCdmModule();
}

DLL_EXPORT char* GetCdmVersion()
{
    Log("GetCdmVersion\n");
    return _GetCdmVersion();
}

 bool VerifyCdmHost_0(verifyWrap*, int flag)
{
     Log("VerifyCdmHost_0\n");
    
    return true;
}
~~~

导出函数分别有5个，其中`InitializeCdmModule_4` 、`DeinitializeCdmModule` 、`GetCdmVersion`调用原函数就行，而`VerifyCdmHost_0`需要恒返回`ture`

~~~c++
DLL_EXPORT void* CreateCdmInstance(int interface_version, const char* key_system, uint32_t key_system_len, void* host_function, void* extra_data)
{
    Log("CreateCdmInstance %d, %s, %lld, \n", interface_version, key_system, key_system_len);

   originHostFunction = (void* (*)(int host_version, void* user_data))host_function;
    void* instance = nullptr;

    
   
    instance = _CreateCdmInstance(interface_version, key_system, key_system_len, HostFunction, extra_data);
    if (!instance)
    {
        Log("no origin instance created\n");
        return nullptr;
    }
    Log("module version, %d", interface_version);

    if (interface_version != 10)
    {
        Log("unhandled version, %d", interface_version);
        return instance;
    }

    MyContentDecryptionModuleProxy* proxy = new MyContentDecryptionModuleProxy(static_cast<ContentDecryptionModule_10*>(instance));
    proxy->setHost(g_CDMHost);
    g_CDMHost->m_MyProxy = proxy;
    return proxy;

   

}

~~~

CreateCdmInstance比较复杂，下面我详细介绍他的参数，其它的参数不用关，但是`host_function`,和`CreateCdmInstance`的`返回值`很重要

#### cdmHost 

~~~c++
void* HostFunction(int host_version, void* user_data)
{
    Log("GetCdmHost called, version %d, user_data %p", host_version, (const void*)user_data);
    void * originHost = originHostFunction(host_version, user_data);
    Log("originHostFunction called, originHost %p",originHost );
    g_CDMHost = new cdmHost((Host*)originHost);
    Log("new CDMHost %p", g_CDMHost);
    return g_CDMHost;
}
~~~

`host_function`的返回值为`cdmHost  *`，这是一个回调函数，不过由`cdm模块`调用，返回一个`cdmHost  *`对象，cdm通过`cdmHost  *`对象通知浏览器，所以我们需要用`HostFunction`去替换`host_function`,在`HostFunction`中，我们使用自己创建的`cdmHost`将原来的`cdmHost`组合起来(包装起来),下面是`cdmHost`的函数

~~~c++
class MyContentDecryptionModuleProxy;
class cdmHost
{
public:

    virtual CDMHostBuffer* Allocate(int capacity);

    // Requests the host to call ContentDecryptionModule::TimerFired() |delay_ms|
    // from now with |context|.
    virtual void SetTimer(__int64 delay_ms, void* context);

    // Returns the current wall time.
    virtual __time64_t GetCurrentWallTime();

    // Called by the CDM with the result after the CDM instance was initialized.
    virtual void OnInitialized(bool success);


    virtual void OnResolveKeyStatusPromise(int promise_id,
        int key_status);

    virtual void OnResolveNewSessionPromise(int promise_id,
        const char* session_id,
        int session_id_size);

    // Called by the CDM when a session is updated or released.
    virtual void OnResolvePromise(int promise_id);

    virtual void OnRejectPromise(uint32_t promise_id,
        int exception,
        uint32_t system_code,
        const char* error_message,
        uint32_t error_message_size);


    virtual void OnSessionMessage(const char* session_id,
        uint32_t session_id_size,
        int message_type,
        const char* message,
        uint32_t message_size);


    virtual void OnSessionKeysChange(const char* session_id,
        uint32_t session_id_size,
        bool has_additional_usable_key,
        const void* keys_info,
        uint32_t keys_info_count);

    virtual void OnExpirationChange(const char* session_id,
        uint32_t session_id_size,
        __time64_t new_expiry_time);

    virtual void OnSessionClosed(const char* session_id,
        uint32_t session_id_size);


    virtual void SendPlatformChallenge(const char* service_id,
        uint32_t service_id_size,
        const char* challenge,
        uint32_t challenge_size);


    virtual void EnableOutputProtection(uint32_t desired_protection_mask);


    virtual void QueryOutputProtectionStatus();

    virtual void OnDeferredInitializationDone(int stream_type,
        int decoder_status);

    virtual void* CreateFileIO(void* client);

    virtual void RequestStorageId(uint32_t version);

public:
    void setMapIdHdcp(int promise_id, std::string hdcp);
    cdmHost(Host * host):m_host(host){}
    virtual ~cdmHost() {}
private:
    Host* m_host;
    void* m_context;
    std::string m_session_id;
    std::map<int, std::string> m_24;
    std::map<int, std::string> m_mapIdHdcp;
    std::mutex m_mtx;
public:
    MyContentDecryptionModuleProxy* m_MyProxy;
};

~~~

将上面所有虚函数都实现并调用原来的cdmHost的虚函数即可

#### MyContentDecryptionModuleProxy

`CreateCdmInstance`的返回值为`ContentDecryptionModule *`,这个对象由浏览器调用，同样的，我们使用自己创建的`MyContentDecryptionModuleProxy`将原来的`ContentDecryptionModule `组合起来(包装起来),下面是`MyContentDecryptionModuleProxy`的函数

~~~c++
class cdmHost;

class  MyContentDecryptionModuleProxy:ContentDecryptionModule_10 {
public:

    virtual void Initialize(bool allow_distinctive_identifier,
        bool allow_persistent_state, bool flag);


    virtual void GetStatusForPolicy(uint32_t promise_id,
        int* policy);

    virtual void SetServerCertificate(uint32_t promise_id,
        const uint8_t* server_certificate_data,
        uint32_t server_certificate_data_size);

    virtual void CreateSessionAndGenerateRequest(uint32_t promise_id,
        int session_type,
        int init_data_type,
        const uint8_t* init_data,
        uint32_t init_data_size);


    virtual void LoadSession(uint32_t promise_id,
        int session_type,
        const char* session_id,
        uint32_t session_id_size);

  
    virtual void UpdateSession(uint32_t promise_id,
        const char* session_id,
        uint32_t session_id_size,
        const uint8_t* response,
        uint32_t response_size);


    virtual void CloseSession(uint32_t promise_id,
        const char* session_id,
        uint32_t session_id_size);


    virtual void RemoveSession(uint32_t promise_id,
        const char* session_id,
        uint32_t session_id_size);

    virtual void TimerExpired(void* context);

   
    virtual int Decrypt(void* encrypted_buffer,
        DecryptedBlock* decrypted_buffer);

   
    virtual int InitializeAudioDecoder(
        void* audio_decoder_config);

   
    virtual int InitializeVideoDecoder(
        void* video_decoder_config);

   
    virtual void DeinitializeDecoder(int decoder_type);

    
    virtual void ResetDecoder(int decoder_type);

    
    virtual int DecryptAndDecodeFrame(const void* encrypted_buffer,
        void* video_frame);

  
    virtual int DecryptAndDecodeSamples(void* encrypted_buffer,
        void* audio_frames);

    virtual void OnPlatformChallengeResponse(
        void* response);

    virtual void OnQueryOutputProtectionStatus(
        int result,
        uint32_t link_mask,
        uint32_t output_protection_mask);

    virtual void OnStorageId(uint32_t version,
        const uint8_t* storage_id,
        uint32_t storage_id_size);

 
    virtual void Destroy();
    std::string getLink_maskMean(int link_mask);
    std::string getOutput_protection_mean(int output_protection_mask);
    void setHost(cdmHost* host);
    explicit  MyContentDecryptionModuleProxy(ContentDecryptionModule_10* instance);
    virtual ~MyContentDecryptionModuleProxy();
private:
    ContentDecryptionModule_10* m_instance;
    cdmHost* m_host;
    std::mutex m_mtx;
    std::string m_d4;
    std::string m_baseServerCertificate;
    std::string m_base64Pssh;
    friend class cdmHost;
private:
    static std::list<MyContentDecryptionModuleProxy*> g_listInstance;
    static std::mutex g_mtx;
};
~~~

将上面所有虚函数都实现并调用原来的`ContentDecryptionModule`的虚函数即可

