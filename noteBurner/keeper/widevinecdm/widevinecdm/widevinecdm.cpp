// widevinecdm.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include "widevinecdm.h"
#include "fucntion.h"
#include "cdmHost.h"
#include "tool/base64.h"
#include "InlineHook.hpp"
#include "webNetwork.h"

bool (*_VerifyCdmHost_0)(verifyWrap*, int flag);
void (*_InitializeCdmModule_4)();
void* (*_CreateCdmInstance)(int interface_version, const char* key_system, uint32_t key_system_len,
    void* host_function, void* extra_data);
void  (*_DeinitializeCdmModule)();
char* (*_GetCdmVersion)();
void* (*originHostFunction)(int host_version, void* user_data);
void* HostFunction(int host_version, void* user_data);

typedef DWORD(__stdcall* MyGetFileAttributes)(LPCWSTR lpFileName);
typedef DWORD(__stdcall* MyGetModuleFileName)(HMODULE hModule, LPWSTR  lpFilename, DWORD  nSize);
DWORD __stdcall  fake_GetModuleFileNameW(
    HMODULE hModule,
    LPWSTR  lpFilename,
    DWORD   nSize
);
DWORD __stdcall fake_GetFileAttributesW(LPCWSTR lpFileName);
hook::InlineHook GetFileAttributeshooker = hook::InlineHook();
hook::InlineHook GetModuleFileNamehooker = hook::InlineHook();
wstring dycVfchm;
struct Keys_info {
    const char* key_id;
    int size;
    int status;
    int system_code;
    int m10;
    int m_14;
};

void initializeApp() {

    wstring dycWidevine = TEXT(R"(C:\Program Files (x86)\NoteBurner\NoteBurner Netflix Video Downloader\resources\com.noteburner.netflix\native\sig_files\widevinecdm.dll)");
    wstring sigWidevine = TEXT(R"(C:\Program Files (x86)\NoteBurner\NoteBurner Netflix Video Downloader\resources\com.noteburner.netflix\native\sig_files\widevinecdm.dll.sig)");
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
}

int main()
{
   
    Sleep(100);
    sendMessageAndWaitForResponse("123");
	
    initializeApp();
    InitializeCdmModule_4();
    string key_system("com.widevine.alpha");
    CreateCdmInstance(10, key_system.c_str(), key_system.size(), HostFunction, 0);
    

    return 0;

}




void* HostFunction(int host_version, void* user_data)
{
    Log("GetCdmHost called, version %d, user_data %p", host_version, (const void*)user_data);
    void * originHost = originHostFunction(host_version, user_data);
    Log("originHostFunction called, originHost %p",originHost );
    g_CDMHost = new cdmHost((Host*)originHost);
    Log("new CDMHost %p", g_CDMHost);
    return g_CDMHost;
}

DLL_EXPORT void InitializeCdmModule_4()
{
    thread tr([]() {
        connectToServer("127.0.0.1", 8012);
        });
    tr.detach();
    Sleep(200);
    Log("InitializeCdmModule_4\n");
    _InitializeCdmModule_4();
}

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
        initializeApp();
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
    m_host->QueryOutputProtectionStatus();
    if (!m_instance)
    {
        Log("instance is null, %d", 76);
        return;
    }
   
    Log("init module(%p), %d, %d, %d", this, allow_distinctive_identifier, allow_persistent_state, flag);

    m_instance->Initialize(allow_distinctive_identifier, allow_persistent_state, flag);
    //allow_distinctive_identifier = 1;
    //this->GetStatusForPolicy(-1, (int *)&allow_distinctive_identifier);
}

void MyContentDecryptionModuleProxy::GetStatusForPolicy(uint32_t promise_id, int* policy)
{
    Log("module(%p) GetStatusForPolicy", this);
    
   // m_host->OnResolveKeyStatusPromise(promise_id, 0);
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
   
  /*  string aGetstatusforpo = "GetStatusForPolicy_";

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

    
    m_host->setMapIdHdcp(promise_id, aGetstatusforpo);*/

    m_instance->GetStatusForPolicy(promise_id, policy);

}

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
    string license((char *)response, response_size);
    string base64License = base64_encode(license);
    Log("UpdateSession(%p) %s:", (const void*)this, base64License.c_str());
    
    sendMessageAndWaitForResponse("licenseResult:" + base64License);

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
   
    m_host->SetTimer(1000, (void *)((int)context + 1));
    if (!m_instance)
    {
        Log("instance is contextnull, %d", 96);
        return;
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