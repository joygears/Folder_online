// widevinecdm.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include "widevinecdm.h"
#include "fucntion.h"
#include "cdmHost.h"
#include "tool/base64.h"


bool (*_VerifyCdmHost_0)(verifyWrap*, int flag);
void (*_InitializeCdmModule_4)();
void* (*_CreateCdmInstance)(int interface_version, const char* key_system, uint32_t key_system_len,
    void* host_function, void* extra_data);
void  (*_DeinitializeCdmModule)();
char* (*_GetCdmVersion)();
void* (*originHostFunction)(int host_version, void* user_data);
void* HostFunction(int host_version, void* user_data);

void initializeApp() {
    wstring dycWidevine = TEXT(R"(.\..\..\sig_files\widevinecdm.dll)");
    wstring sigWidevine = TEXT(R"(.\..\..\sig_files\widevinecdm.dll.sig)");
    wstring dycVfchm = TEXT(R"(.\..\..\sig_files\vfchm.dll)");
    wstring sigVfchm = TEXT(R"(.\..\..\sig_files\vfchm.dll.sig)");
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
    
    _VerifyCdmHost_0 = (bool (*)(verifyWrap*, int flag))GetProcAddress(hWidevine, "VerifyCdmHost_0");
    _InitializeCdmModule_4 = (void (*)())GetProcAddress(hWidevine, "InitializeCdmModule_4");
    _CreateCdmInstance = (void* (*)(int interface_version, const char* key_system, uint32_t key_system_len,
            void* host_function, void* extra_data))GetProcAddress(hWidevine, "CreateCdmInstance");
    _DeinitializeCdmModule = (void (*)())GetProcAddress(hWidevine, "DeinitializeCdmModule");
    _GetCdmVersion = (char * (*)())GetProcAddress(hWidevine, "GetCdmVersion");

    Log("load widevinecdm success, %p, %p, %p, %p \n", _InitializeCdmModule_4, _CreateCdmInstance, _DeinitializeCdmModule, _GetCdmVersion);

    bool retcode = _VerifyCdmHost_0(&wrap, 2);

    Log("widevine VerifyCdmHost_0 retcode value %d\n",retcode);
}

int main()
{
	
    initializeApp();
    InitializeCdmModule_4();
    string key_system("com.widevine.alpha");
    CreateCdmInstance(10, key_system.c_str(), key_system.size(), HostFunction, 0);
    

    return 0;

}




void* HostFunction(int host_version, void* user_data)
{
    Log("GetCdmHost called, version %d, user_data %p", host_version, (const void*)user_data);
    g_CDMHost = new cdmHost(0);
    Log("new CDMHost %p", g_CDMHost);
    return g_CDMHost;
}

DLL_EXPORT void InitializeCdmModule_4()
{
    Log("InitializeCdmModule_4\n");
   // _InitializeCdmModule_4();
}

DLL_EXPORT void* CreateCdmInstance(int interface_version, const char* key_system, uint32_t key_system_len, void* host_function, void* extra_data)
{
    Log("CreateCdmInstance %d, %s, %lld, \n", interface_version, key_system, key_system_len);

    originHostFunction = (void* (*)(int host_version, void* user_data))host_function;
    void* instance = nullptr;

    cdmHost* host =  (cdmHost *)originHostFunction(10,0);
   
   // void* instance = _CreateCdmInstance(interface_version, key_system, key_system_len, HostFunction, extra_data);
   /* if (!instance)
    {
        Log("no origin instance created\n");
        return nullptr;
    }
    Log("module version, %d", interface_version);

    if (interface_version != 10)
    {
        Log("unhandled version, %d", interface_version);
        return instance;
    }*/

    MyContentDecryptionModuleProxy* proxy = new MyContentDecryptionModuleProxy(static_cast<ContentDecryptionModule_10*>(instance));
    proxy->setHost(host);
    return proxy;
}

DLL_EXPORT void DeinitializeCdmModule()
{
    Log("DeinitializeCdmModule\n");
    //_DeinitializeCdmModule();
}

DLL_EXPORT char* GetCdmVersion()
{
    return _GetCdmVersion();
}

DLL_EXPORT bool VerifyCdmHost_0(verifyWrap*, int flag)
{
    return true;
}


BOOL WINAPI DllMain(
    HINSTANCE hinstDLL,  // handle to DLL module
    DWORD fdwReason,     // reason for calling function
    LPVOID lpvReserved)  // reserved
{
    // Perform actions based on the reason for calling.
    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        // Initialize once for each new process.
        // Return FALSE to fail DLL load.
        DisableThreadLibraryCalls((HMODULE)hinstDLL);
        //initializeApp();
        break;

    case DLL_THREAD_ATTACH:
        // Do thread-specific initialization.
        break;

    case DLL_THREAD_DETACH:
        // Do thread-specific cleanup.
        break;

    case DLL_PROCESS_DETACH:

        if (lpvReserved != nullptr)
        {
            break; // do not do cleanup if process termination scenario
        }

        // Perform any necessary cleanup.
        break;
    }
    return TRUE;  // Successful DLL_PROCESS_ATTACH.
}

void MyContentDecryptionModuleProxy::Initialize(bool allow_distinctive_identifier, bool allow_persistent_state, bool flag)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 76);
        return;
    }
   
    Log("init module(%p), %d, %d, %d", this, allow_distinctive_identifier, allow_persistent_state, flag);

    m_instance->Initialize(allow_distinctive_identifier, allow_persistent_state, flag);
    allow_distinctive_identifier = 1;
    this->GetStatusForPolicy(-1, (int *)&allow_distinctive_identifier);
}

void MyContentDecryptionModuleProxy::GetStatusForPolicy(uint32_t promise_id, int* policy)
{
    Log("module(%p) GetStatusForPolicy", this);
    
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
   
    string aGetstatusforpo = "GetStatusForPolicy_";

    switch (*policy) {
    case 0:
        aGetstatusforpo.append("HDCP_None");
        break;
    case 1:
        aGetstatusforpo.append("HDCP_1_0");
        break;
    case 2:
        aGetstatusforpo.append("HDCP_1_1");
        break;
    case 3:
        aGetstatusforpo.append("HDCP_1_2");
        break;
    case 4:
        aGetstatusforpo.append("HDCP_1_3");
        break;
    case 5:
        aGetstatusforpo.append("HDCP_1_4");
        break;
    case 6:
        aGetstatusforpo.append("HDCP_2_0");
        break;
    case 7:
        aGetstatusforpo.append("HDCP_2_1");
        break;
    case 8:
        aGetstatusforpo.append("HDCP_2_2");
        break;
    case 9:
        aGetstatusforpo.append("HDCP_2_3");
        break;
    default:
        aGetstatusforpo.append("HDCP_Unknown", 12);
        break;

    };

    
    m_host->setMapIdHdcp(promise_id, aGetstatusforpo);

    m_instance->GetStatusForPolicy(promise_id, policy);

}

void MyContentDecryptionModuleProxy::SetServerCertificate(uint32_t promise_id, const uint8_t* server_certificate_data, uint32_t server_certificate_data_size)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    string strCertificateData((const char *)server_certificate_data, server_certificate_data_size);
    string base64Data = base64_encode(strCertificateData);
    Log("SetServerCertificate(%p): %d",this, base64Data.size());
    m_d4 = string("Set", 3);
    m_baseServerCertificate = base64Data;
    m_instance->SetServerCertificate(promise_id, server_certificate_data, server_certificate_data_size);
}

void MyContentDecryptionModuleProxy::CreateSessionAndGenerateRequest(uint32_t promise_id, int session_type, int init_data_type, const uint8_t* init_data, uint32_t init_data_size)
{
    string sessionId = "4D5D0BF3C3D070205492B55F098238BA";
    string message = "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";

    m_host->OnSessionMessage(sessionId.c_str(), sessionId.size(), 0, message.c_str(), message.size());
    
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("CreateSessionAndGenerateRequest(%p)", this);

    m_instance->CreateSessionAndGenerateRequest(promise_id, session_type, init_data_type, init_data, init_data_size);

}

void MyContentDecryptionModuleProxy::LoadSession(uint32_t promise_id, int session_type, const char* session_id, uint32_t session_id_size)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("LoadSession(%p):", (const void*)this);
    m_instance->LoadSession(promise_id, session_type, session_id, session_id_size);

}

void MyContentDecryptionModuleProxy::UpdateSession(uint32_t promise_id, const char* session_id, uint32_t session_id_size, const uint8_t* response, uint32_t response_size)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("UpdateSession(%p):", (const void*)this);
    m_instance->UpdateSession(promise_id, session_id, session_id_size, response, response_size);
}

void MyContentDecryptionModuleProxy::CloseSession(uint32_t promise_id, const char* session_id, uint32_t session_id_size)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("CloseSession(%p):", (const void*)this);
    m_instance->CloseSession(promise_id, session_id, session_id_size);
}

void MyContentDecryptionModuleProxy::RemoveSession(uint32_t promise_id, const char* session_id, uint32_t session_id_size)
{

    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("RemoveSession(%p):", (const void*)this);
    m_instance->RemoveSession(promise_id, session_id, session_id_size);
}

void MyContentDecryptionModuleProxy::TimerExpired(void* context)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
       
    }
    Log("TimerExpired(%p):", (const void*)this);
    m_instance->TimerExpired(context);
}

int MyContentDecryptionModuleProxy::Decrypt(void* encrypted_buffer, DecryptedBlock * decrypted_buffer)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return 0;
    }
    Log("Decrypt(%p):", (const void*)this);

    int status    = m_instance->Decrypt(encrypted_buffer, decrypted_buffer);
    if (mDecFile == NULL)
    {
        mDecFile = fopen("d:\\cdm_dec.bin", "wb");
    }
    if (mDecFile != NULL)
    {
        fwrite(decrypted_buffer->DecryptedBuffer()->Data(), 1,
            decrypted_buffer->DecryptedBuffer()->Size(), mDecFile);
        Log("Decrypt data size %d:", decrypted_buffer->DecryptedBuffer()->Size());
    }
    return status;
}

int MyContentDecryptionModuleProxy::InitializeAudioDecoder(void* audio_decoder_config)
{

    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return 0;
    }
    Log("InitializeAudioDecoder(%p):", (const void*)this);
   
    return  m_instance->InitializeAudioDecoder(audio_decoder_config);
}

int MyContentDecryptionModuleProxy::InitializeVideoDecoder(void* video_decoder_config)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return 0;
    }
    Log("InitializeVideoDecoder(%p):", (const void*)this);

    return  m_instance->InitializeVideoDecoder(video_decoder_config);
}

void MyContentDecryptionModuleProxy::DeinitializeDecoder(int decoder_type)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("DeinitializeDecoder(%p):", (const void*)this);
    m_instance->DeinitializeDecoder(decoder_type);
}

void MyContentDecryptionModuleProxy::ResetDecoder(int decoder_type)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("ResetDecoder(%p):", (const void*)this);
    m_instance->ResetDecoder(decoder_type);
}

int MyContentDecryptionModuleProxy::DecryptAndDecodeFrame(const void* encrypted_buffer, void* video_frame)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return 0;
    }
    Log("DecryptAndDecodeFrame(%p):", (const void*)this);




    return  m_instance->DecryptAndDecodeFrame(encrypted_buffer, video_frame);

}

int MyContentDecryptionModuleProxy::DecryptAndDecodeSamples(void* encrypted_buffer, void* audio_frames)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return 0;
    }
    Log("DecryptAndDecodeSamples(%p):", (const void*)this);

    return  m_instance->DecryptAndDecodeSamples(encrypted_buffer, audio_frames);
 
}

void MyContentDecryptionModuleProxy::OnPlatformChallengeResponse(void* response)
{

    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("OnPlatformChallengeResponse(%p):", (const void*)this);
    
    m_instance->OnPlatformChallengeResponse(response);
}

void MyContentDecryptionModuleProxy::OnQueryOutputProtectionStatus(int result, uint32_t link_mask, uint32_t output_protection_mask)
{

    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("OnQueryOutputProtectionStatus, %u, %u, %u", result, link_mask, output_protection_mask);
    if (result)
    {
        Log("QueryOutputProtectionStatus failed");
    }
    else {
        Log("output_link_type: %s", getLink_maskMean(link_mask).c_str());
        Log( "output_protection: %s", getOutput_protection_mean(output_protection_mask).c_str());
    }
    m_instance->OnQueryOutputProtectionStatus(result, link_mask, output_protection_mask);
}

void MyContentDecryptionModuleProxy::OnStorageId(uint32_t version, const uint8_t* storage_id, uint32_t storage_id_size)
{

    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("OnStorageId(%p):", (const void*)this);

    m_instance->OnStorageId(version, storage_id, storage_id_size);
}

void MyContentDecryptionModuleProxy::Destroy()
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("Destroy(%p):", (const void*)this);
    if(mDecFile!=NULL)
        fclose(mDecFile);
    mDecFile = NULL;

    m_instance->Destroy();
}

std::string MyContentDecryptionModuleProxy::getLink_maskMean(int link_mask)
{
    string result;
    switch (link_mask)
    {
    case 0:
        result = "None";
        break;
    case 1:
        result = "Unknown";

        break;
    case 2:
        result = "Internal";

        break;
    case 4:
        result = "VGA";
        
        break;
    case 8:
        result = "HDMI";
       
        break;
    case 16:
        result = "DVI";
        
        break;
    case 32:
        result = "DisplayPort";
       
        break;
    case 64:
        result = "Network";
       
        break;
    default:
        result = "Unknown";
        break;
    }
    
    return result;
}

std::string MyContentDecryptionModuleProxy::getOutput_protection_mean(int output_protection_mask)
{
    return output_protection_mask == 1 ? "HDCP" : "None";
}

void MyContentDecryptionModuleProxy::setHost(cdmHost * host)
{
    Log("module SetHost(%p)", host);
    m_host = host;
    if (m_host)
    {
        m_host->m_MyProxy = this;
    }
}

MyContentDecryptionModuleProxy::MyContentDecryptionModuleProxy(ContentDecryptionModule_10* instance) :m_instance(instance) {
    g_mtx.lock();
    g_listInstance.push_back(this);
    Log("construct module, count: %d", g_listInstance.size());
    g_mtx.unlock();
}

MyContentDecryptionModuleProxy::~MyContentDecryptionModuleProxy()
{
    g_mtx.lock();
    for (std::list<MyContentDecryptionModuleProxy*>::iterator it = g_listInstance.begin(); it != g_listInstance.end(); ++it) {
        if (*it == this)
            g_listInstance.erase(it);
    }
    Log( "destruct module. Remained count: %d", g_listInstance.size());

    g_mtx.unlock();
}

void DecryptedProxyBlock::SetDecryptedBuffer(Buffer* buffer) {
    buf = buffer;
}
Buffer* DecryptedProxyBlock::DecryptedBuffer() {
    return buf;
}

void DecryptedProxyBlock::SetTimestamp(int64_t timestamp) {
    ts = timestamp;
}

int64_t DecryptedProxyBlock::Timestamp() const {
    return ts;
}

std::mutex MyContentDecryptionModuleProxy::g_mtx;
std::list< MyContentDecryptionModuleProxy*> MyContentDecryptionModuleProxy::g_listInstance;
