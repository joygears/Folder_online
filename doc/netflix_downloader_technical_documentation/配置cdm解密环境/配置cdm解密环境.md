## 配置`cdm`解密环境

现在我将劫持的进程称为`keeper`，将解密的进程成为`sheller`，下面详细讲解`keeper`和`sheller`进程是如何协作的

### keeper进程

~~~
void MyContentDecryptionModuleProxy::SetServerCertificate(uint32_t promise_id, const uint8_t* server_certificate_data, uint32_t server_certificate_data_size)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }

    //保存ServerCertificate
    string strCertificateData((const char*)server_certificate_data, server_certificate_data_size);
    string base64Data = base64_encode(strCertificateData);
    Log("SetServerCertificate(%p): %s", this, base64Data.c_str());
    m_d4 = string("Set", 3);
    m_baseServerCertificate = base64Data;

    m_instance->SetServerCertificate(promise_id, server_certificate_data, server_certificate_data_size);
}
~~~



在keeper进程中浏览器会调用`SetServerCertificate`,此时我们将`server_certificate_data`转成`base64`保存起来



~~~c++
void MyContentDecryptionModuleProxy::CreateSessionAndGenerateRequest(uint32_t promise_id, int session_type, int init_data_type, const uint8_t* init_data, uint32_t init_data_size)
{
   
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    
    string pssh((char *)init_data, init_data_size);
    m_base64Pssh = base64_encode(pssh);

    Log("CreateSessionAndGenerateRequest(%p) pssh: %s ", this, m_base64Pssh.c_str());
    m_instance->CreateSessionAndGenerateRequest(promise_id, session_type, init_data_type, init_data, init_data_size);

}
~~~

在keeper进程中浏览器会调用`CreateSessionAndGenerateRequest`,此时我们将`pssh`转成`base64`保存起来

> 可以在此时使用命令行调用将sheller进程调起来，当收到sheller进程调用成功的消息后继续执行

~~~c++
void cdmHost::OnSessionMessage(const char* session_id, uint32_t session_id_size, int message_type, const char* message, uint32_t message_size)
{
    Log(
        "[%08x] Host::OnSessionMessage, session_id %s, session_id_size %u, message_type %u, message_size %u, message %p ",
        this,
        (const char*)session_id,
        session_id_size,
        message_type,
        message_size,
        (const void*)message);
   
    string licenseRequestResult =  sendMessageAndWaitForResponse("licenseRequest:" + m_MyProxy->m_baseServerCertificate + ":" + m_MyProxy->m_base64Pssh);
    string licenseRequest = "";
    Log("%s", licenseRequestResult.c_str());
    std::vector<std::string> tokens;
    std::stringstream ss(licenseRequestResult);
    std::string token;

    while (std::getline(ss, token, ':')) {
        tokens.push_back(token);
    }
   
   /* session_id = tokens[1].c_str();
    session_id_size = strlen(session_id);*/
    licenseRequest = base64_decode(tokens[2]);
    message = licenseRequest.c_str();
    message_size = licenseRequest.size();
    
    Log("session_id:%s licenseRequestResult:%s ", session_id, tokens[2].c_str());
    if (m_host) {
        
        m_host->OnSessionMessage(session_id,session_id_size,message_type, message,message_size);
    }
}
~~~



在keeper进程中，`CreateSessionAndGenerateRequest`会调用`OnSessionMessage`将生成的`licenseRequest`发给浏览器

此时我们将保存的`server_certificate_data`和`pssh`发送给sheller进程,由sheller进程生成`licenseRequest`发送到keeper进程，然后发送给浏览器

~~~c++

void MyContentDecryptionModuleProxy::UpdateSession(uint32_t promise_id, const char* session_id, uint32_t session_id_size, const uint8_t* response, uint32_t response_size)
{

    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    string license((char *)response, response_size);
    string base64License = base64_encode(license);
    Log("UpdateSession(%p) %s:", (const void*)this, base64License.c_str());
    
    sendMessage("licenseResult:" + base64License);

    m_instance->UpdateSession(promise_id, session_id, session_id_size, response, response_size);
}

~~~

在`keeper`进程中,浏览器会调用`UpdateSession`将`license`传递给`cdm模块`,此时我们将得到的`license`发送给`sheller`进程即可

> 可以通过环境变量设置转换模式，当为普通模式，则正常执行所有的`api`，当为转化模式才会执行`license`交换协议，此时发送完`license`,可等待`sheller`配置cdm解密环境完成，然后keeper进程将转换模式设置为普通模式

### sheller进程

~~~c++
void initializeApp() {

    
   
   
    GetFileAttributeshooker.hook(::GetFileAttributesW, fake_GetFileAttributesW);
    GetModuleFileNamehooker.hook(::GetModuleFileNameW, fake_GetModuleFileNameW);

    wstring dycWidevine = TEXT(R"(.\..\..\..\sig_files\widevinecdm.dll)");
    wstring sigWidevine = TEXT(R"(.\..\..\..\sig_files\widevinecdm.dll.sig)");
    dycVfchm = TEXT(R"(.\..\..\..\sig_files\vfchm.dll)");
    wstring sigVfchm = TEXT(R"(.\..\..\..\sig_files\vfchm.dll.sig)");
    verifyWrap wrap;
   
   
    
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
    
    VerifyCdmHost_0 = (bool (*)(verifyWrap*, int flag))GetProcAddress(hWidevine, "VerifyCdmHost_0");
    _InitializeCdmModule_4 = (void (*)())GetProcAddress(hWidevine, "InitializeCdmModule_4");
    _CreateCdmInstance = (void* (*)(int interface_version, const char* key_system, uint32_t key_system_len,
            void* host_function, void* extra_data))GetProcAddress(hWidevine, "CreateCdmInstance");
    _DeinitializeCdmModule = (void (*)())GetProcAddress(hWidevine, "DeinitializeCdmModule");
    _GetCdmVersion = (char * (*)())GetProcAddress(hWidevine, "GetCdmVersion");

    Log("load widevinecdm success, %p, %p, %p, %p \n", _InitializeCdmModule_4, _CreateCdmInstance, _DeinitializeCdmModule, _GetCdmVersion);

    bool retcode = VerifyCdmHost_0(&wrap, 2);

    Log("widevine VerifyCdmHost_0 retcode value %d\n",retcode);
}
~~~

sheller进程需要和keeper进程一样初始化，其它劫持部分的代码都是一样的，不过`sheller`是`exe`，主动在`main`函数中调用的这些函数

~~~c++
   string input_string  =  sendMessageAndWaitForResponse("sheller");
    std::vector<std::string> tokens;
    std::stringstream ss(input_string);
    std::string token;

    while (std::getline(ss, token, ':')) {
        tokens.push_back(token);
    }
    if (tokens[0] == "licenseRequest") {
        cert = tokens[1];
        pssh = tokens[2];
    }

    cert = base64_decode(cert);
    pssh = base64_decode(pssh);
        
   InitializeCdmModule_4();
    string key_system("com.widevine.alpha");
  proxy = (MyContentDecryptionModuleProxy*)CreateCdmInstance(10, key_system.c_str(), key_system.size(), HostFunction, 0);
   proxy->Initialize(0, 0, 0);
   proxy->SetServerCertificate(1, (const UINT8*)cert.c_str(), cert.size());
   proxy->CreateSessionAndGenerateRequest(1, 0, 0, (const UINT8*)pssh.c_str(), pssh.size());
~~~

接收到`keeper`发来的`cert`和`pssh`后，调用`CreateCdmInstance`创建`MyContentDecryptionModuleProxy*`对象，调用`Initialize`初始化，调用`SetServerCertificate`设置`cert`,调用`CreateSessionAndGenerateRequest`设置`pssh`，并生成`liecenseRequest`

~~~c++
void cdmHost::OnSessionMessage(const char* session_id, uint32_t session_id_size, int message_type, const char* message, uint32_t message_size)
{
   
    Log(
        "[%08x] Host::OnSessionMessage, session_id %s, session_id_size %u, message_type %u, message_size %u, message %p ",
        this,
        (const char*)session_id,
        session_id_size,
        message_type,
        message_size,
        (const void*)message);
    string licenseRequest = base64_encode(string(message, message_size));

    Log("licenseRequest: %s",licenseRequest.c_str());
    g_session_id = session_id;

    string msg = sendMessageAndWaitForResponse("licenseRequestResult:" + g_session_id + ":" + licenseRequest);

    std::vector<std::string> tokens;
    std::stringstream ss(msg);
    std::string token;

    while (std::getline(ss, token, ':')) {
        tokens.push_back(token);
    }
    


    license = tokens[1];
    Log("license: %s", license.c_str());
    if (m_host) {

        m_host->OnSessionMessage(session_id, session_id_size, message_type, message, message_size);
    }
}
~~~

sheller进程在`OnSessionMessage`中将生成的`liecenseRequest`发送给`sheller`，并等待`sheller`进程发送`license`过来

~~~c++
  license = base64_decode(license);
    proxy->UpdateSession(1, g_session_id.c_str(), g_session_id.size(), (uint8_t*)license.c_str(), license.size());

    Log("decrypt environments config finished");
    string res = sendMessageAndWaitForResponse("initFinished");
~~~

拿到`license`后调用UpdateSession设置license，此时解密环境已经配置完成，此时告诉服务器sheller已初始化完成，等待服务器发送相关信息开始解密

