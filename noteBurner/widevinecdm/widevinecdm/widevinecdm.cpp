// widevinecdm.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include <fstream>
#include "widevinecdm.h"
#include "fucntion.h"
#include "cdmHost.h"
#include "tool/base64.h"
#include "InlineHook.hpp"
#include "base64.h"


bool (*VerifyCdmHost_0)(verifyWrap*, int flag);
void (*_InitializeCdmModule_4)();
void* (*_CreateCdmInstance)(int interface_version, const char* key_system, uint32_t key_system_len,
    void* host_function, void* extra_data);
void  (*_DeinitializeCdmModule)();
char* (*_GetCdmVersion)();
void* (*originHostFunction)(int host_version, void* user_data);
void* HostFunction(int host_version, void* user_data);

typedef DWORD(__stdcall* MyGetFileAttributes)(LPCWSTR lpFileName);
typedef DWORD(__stdcall* MyGetModuleFileName)(HMODULE hModule,LPWSTR  lpFilename,DWORD  nSize);
DWORD __stdcall  fake_GetModuleFileNameW(
    HMODULE hModule,
    LPWSTR  lpFilename,
    DWORD   nSize
);
DWORD __stdcall fake_GetFileAttributesW(LPCWSTR lpFileName);
hook::InlineHook GetFileAttributeshooker = hook::InlineHook();
hook::InlineHook GetModuleFileNamehooker = hook::InlineHook();

wstring dycVfchm;
string license;
string g_session_id;
void initializeApp() {

    
   
   
    GetFileAttributeshooker.hook(::GetFileAttributesW, fake_GetFileAttributesW);
    GetModuleFileNamehooker.hook(::GetModuleFileNameW, fake_GetModuleFileNameW);

    wstring dycWidevine = TEXT(R"(.\..\..\sig_files\widevinecdm.dll)");
    wstring sigWidevine = TEXT(R"(.\..\..\sig_files\widevinecdm.dll.sig)");
    dycVfchm = TEXT(R"(.\..\..\sig_files\vfchm.dll)");
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




int main()
{
    string cert = "Cr0CCAMSEOVEukALwQ8307Y2+LVP+0MYh/HPkwUijgIwggEKAoIBAQDm875btoWUbGqQD8eAGuBlGY+Pxo8YF1LQR+Ex0pDONMet8EHslcZRBKNQ/09RZFTP0vrYimyYiBmk9GG+S0wB3CRITgweNE15cD33MQYyS3zpBd4z+sCJam2+jj1ZA4uijE2dxGC+gRBRnw9WoPyw7D8RuhGSJ95OEtzg3Ho+mEsxuE5xg9LM4+Zuro/9msz2bFgJUjQUVHo5j+k4qLWu4ObugFmc9DLIAohL58UR5k0XnvizulOHbMMxdzna9lwTw/4SALadEV/CZXBmswUtBgATDKNqjXwokohncpdsWSauH6vfS6FXwizQoZJ9TdjSGC60rUB2t+aYDm74cIuxAgMBAAE6EHRlc3QubmV0ZmxpeC5jb20SgAOE0y8yWw2Win6M2/bw7+aqVuQPwzS/YG5ySYvwCGQd0Dltr3hpik98WijUODUr6PxMn1ZYXOLo3eED6xYGM7Riza8XskRdCfF8xjj7L7/THPbixyn4mULsttSmWFhexzXnSeKqQHuoKmerqu0nu39iW3pcxDV/K7E6aaSr5ID0SCi7KRcL9BCUCz1g9c43sNj46BhMCWJSm0mx1XFDcoKZWhpj5FAgU4Q4e6f+S8eX39nf6D6SJRb4ap7Znzn7preIvmS93xWjm75I6UBVQGo6pn4qWNCgLYlGGCQCUm5tg566j+/g5jvYZkTJvbiZFwtjMW5njbSRwB3W4CrKoyxw4qsJNSaZRTKAvSjTKdqVDXV/U5HK7SaBA6iJ981/aforXbd2vZlRXO/2S+Maa2mHULzsD+S5l4/YGpSt7PnkCe25F+nAovtl/ogZgjMeEdFyd/9YMYjOS4krYmwp3yJ7m9ZzYCQ6I8RQN4x/yLlHG5RH/+WNLNUs6JAZ0fFdCmw=";
    string pssh = "AAAANHBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAABQIARIQAAAAAAVvYDgAAAAAAAAAAA==";
    cert = base64_decode(cert);
    pssh = base64_decode(pssh);
  /*  VideoDecoderConfig video_decoder_config;
    video_decoder_config.codec = 2;
    video_decoder_config.profile = 5;
    video_decoder_config.alpha_mode = 2;
    video_decoder_config.color_space = 0;
    video_decoder_config.width = 0x3c0;
    video_decoder_config.height = 0x21c;
    video_decoder_config.m_18 = 0;
    video_decoder_config.m_1C = 0;
    video_decoder_config.m_20 = 0xF;*/

    char video_decoder_config[] = { 0x03,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0x03,0x00,0x00,0x1C,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x0F,0x00,0x00,0x00 };

    initializeApp();
    InitializeCdmModule_4();
    string key_system("com.widevine.alpha");
    MyContentDecryptionModuleProxy* proxy = (MyContentDecryptionModuleProxy*)CreateCdmInstance(10, key_system.c_str(), key_system.size(), HostFunction, 0);
    proxy->Initialize(0, 0, 0);
    proxy->SetServerCertificate(1, (const UINT8*)cert.c_str(), cert.size());
    proxy->CreateSessionAndGenerateRequest(1, 0, 0, (const UINT8*)pssh.c_str(), pssh.size());
    license = base64_decode(license);
    proxy->UpdateSession(1, g_session_id.c_str(), g_session_id.size(), (uint8_t*)license.c_str(), license.size());
    proxy->InitializeVideoDecoder((void *)video_decoder_config);

    char ecryptBuffer[0x49d1] = { 0, };
    ifstream inFile("MEM_11F971D8_000049D1.mem", ios::in | ios::binary); //二进制读方式打开
    if (!inFile) {
        cout << "error" << endl;
        return 0;
    }
    while (inFile.read((char*)ecryptBuffer, sizeof(ecryptBuffer))) { //一直读到文件结束
        int readedBytes = inFile.gcount(); //看刚才读了多少字节
        return 0;
    }
    inFile.close();
    char key_id[] = {
        0x00, 0x00, 0x00, 0x00, 0x05, 0x6F, 0x60, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    };
    unsigned char iv[] = {
0x01, 0xAC, 0x60, 0x6C, 0x64, 0x88, 0x37, 0xBE
    };
    
    SubsampleEntry subsamples[1];
    subsamples->clear_bytes = 0x21;
    subsamples->cipher_bytes = 0x49b0;

    InputBuffer_2 input;
    input.data = (uint8_t *)ecryptBuffer;
    input.data_size = 0x49d1;
    input.encryption_scheme = EncryptionScheme::kCenc;
    input.key_id = (uint8_t*)key_id;
    input.key_id_size = 0x10;
    input.iv = iv;
    input.iv_size = 0x8;
    input.subsamples = subsamples;
    input.num_subsamples = 1;
    input.pattern.crypt_byte_block = 0;
    input.pattern.skip_byte_block = 0;
    input.timestamp = 0x073A393;

    proxy->DecryptAndDecodeFrame(input,)
    return 0;

}
//#include <ctime>
//
//int main() {
//    
//   unsigned __int64 b = 4744864539823046656;
//   __int64 timestamp = (__int64)*(double *)&b;
//    
//    struct tm* timeinfo = _gmtime64(&timestamp);
//    int a = GetLastError();
//    char buffer[80];
//    printf("%f", b);
//
//    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", timeinfo);
//    std::cout << "Converted timestamp: " << buffer << std::endl;
//
//    return 0;
//}
//


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
    _InitializeCdmModule_4();
}

DLL_EXPORT void* CreateCdmInstance(int interface_version, const char* key_system, uint32_t key_system_len, void* host_function, void* extra_data)
{
    Log("CreateCdmInstance %d, %s, %lld, \n", interface_version, key_system, key_system_len);

    originHostFunction = (void* (*)(int host_version, void* user_data))host_function;

    void* instance = _CreateCdmInstance(interface_version, key_system, key_system_len, HostFunction, extra_data);
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
    return proxy;
}

DLL_EXPORT void DeinitializeCdmModule()
{
    Log("DeinitializeCdmModule\n");
    _DeinitializeCdmModule();
}

DLL_EXPORT char* GetCdmVersion()
{
    return _GetCdmVersion();
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



DWORD __stdcall fake_GetFileAttributesW(LPCWSTR lpFileName) {
    if (lpFileName)
        Log("GetFileAttributesW called, file %S", lpFileName);
    
    if (wcsstr(lpFileName, TEXT("cshell.dll"))==0 && wcsstr(lpFileName, TEXT("decrypt.dll"))==0 && wcsstr(lpFileName, TEXT("widevinecdm.dll"))==0) {
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






