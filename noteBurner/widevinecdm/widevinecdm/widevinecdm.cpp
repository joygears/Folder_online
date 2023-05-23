// widevinecdm.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include "widevinecdm.h"
#include "fucntion.h"


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

    delog("open file, %p, %p, %p, %p\n", HDycWidevinecdm, HSigWidevinecdm, hFVfchm, hSigVfchm);


    wrap.chDycVfchm = dycVfchm.c_str();
    wrap.hFVfchm = hFVfchm;
    wrap.hSigVfchm = hSigVfchm;
    wrap.chdycWidevine = dycWidevine.c_str();
    wrap.HDycWidevinecdm = HDycWidevinecdm;
    wrap.HSigWidevinecdm = HSigWidevinecdm;

   
    HMODULE hWidevine = LoadLibrary(dycWidevine.c_str());

    if(!hWidevine)
    delog("LoadLibrary widevinecdm.dll error  GetLasterror %d\n", GetLastError());
    
    VerifyCdmHost_0 = (bool (*)(verifyWrap*, int flag))GetProcAddress(hWidevine, "VerifyCdmHost_0");
    _InitializeCdmModule_4 = (void (*)())GetProcAddress(hWidevine, "InitializeCdmModule_4");
    _CreateCdmInstance = (void* (*)(int interface_version, const char* key_system, uint32_t key_system_len,
            void* host_function, void* extra_data))GetProcAddress(hWidevine, "CreateCdmInstance");
    _DeinitializeCdmModule = (void (*)())GetProcAddress(hWidevine, "DeinitializeCdmModule");
    _GetCdmVersion = (char * (*)())GetProcAddress(hWidevine, "GetCdmVersion");

    delog("load widevinecdm success, %p, %p, %p, %p \n", _InitializeCdmModule_4, _CreateCdmInstance, _DeinitializeCdmModule, _GetCdmVersion);

    bool retcode = VerifyCdmHost_0(&wrap, 2);

    delog("widevine VerifyCdmHost_0 retcode value %d\n",retcode);
}

int main()
{
	
    initializeApp();
    InitializeCdmModule_4();

    DeinitializeCdmModule();

    return 0;

}




DLL_EXPORT void InitializeCdmModule_4()
{
    delog("InitializeCdmModule_4\n");
    _InitializeCdmModule_4();
}

DLL_EXPORT void* CreateCdmInstance(int interface_version, const char* key_system, uint32_t key_system_len, void* host_function, void* extra_data)
{
    delog("CreateCdmInstance %d, %s, %lld, \n", interface_version, key_system, key_system_len);
    void* instance = _CreateCdmInstance(interface_version, key_system, key_system_len, host_function, extra_data);
    if (!instance)
    {
        delog("no origin instance created\n");
        return nullptr;
    }

    return instance;
}

DLL_EXPORT void DeinitializeCdmModule()
{
    delog("DeinitializeCdmModule\n");
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
        delog("instance is null, %d", 76);
        return;
    }
   
    delog("init module(%p), %d, %d, %d", this, allow_distinctive_identifier, allow_persistent_state, flag);

    m_instance->Initialize(allow_distinctive_identifier, allow_persistent_state, flag);
    this->GetStatusForPolicy(-1, (int *)&allow_distinctive_identifier);
}

void MyContentDecryptionModuleProxy::GetStatusForPolicy(uint32_t promise_id, int* policy)
{
    delog("module(%p) GetStatusForPolicy", this);
    
    if (!m_instance)
    {
        delog("instance is null, %d", 96);
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

    delog("%s promise_id:%d", aGetstatusforpo.c_str(), promise_id);

    m_instance->GetStatusForPolicy(promise_id, policy);

}
