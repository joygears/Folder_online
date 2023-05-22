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

    wrap.chDycVfchm = dycVfchm.c_str();
    wrap.hFVfchm = hFVfchm;
    wrap.hSigVfchm = hSigVfchm;
    wrap.chdycWidevine = dycWidevine.c_str();
    wrap.HDycWidevinecdm = HDycWidevinecdm;
    wrap.HSigWidevinecdm = HSigWidevinecdm;


    HMODULE hWidevine = LoadLibrary(dycWidevine.c_str());

    if(!hWidevine)
    delog(L"LoadLibrary widevinecdm.dll error  GetLasterror %d\n", GetLastError());

    VerifyCdmHost_0 = (bool (*)(verifyWrap*, int flag))GetProcAddress(hWidevine, "VerifyCdmHost_0");
    _InitializeCdmModule_4 = (void (*)())GetProcAddress(hWidevine, "InitializeCdmModule_4");
    _CreateCdmInstance = (void* (*)(int interface_version, const char* key_system, uint32_t key_system_len,
            void* host_function, void* extra_data))GetProcAddress(hWidevine, "CreateCdmInstance");
    _DeinitializeCdmModule = (void (*)())GetProcAddress(hWidevine, "DeinitializeCdmModule");
    _GetCdmVersion = (char * (*)())GetProcAddress(hWidevine, "GetCdmVersion");

    delog(TEXT("load widevinecdm success, %p, %p, %p, %p \n"), _InitializeCdmModule_4, _CreateCdmInstance, _DeinitializeCdmModule, _GetCdmVersion);

    bool retcode = VerifyCdmHost_0(&wrap, 2);

    delog(L"widevine VerifyCdmHost_0 retcode value %d\n",retcode);
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
    _InitializeCdmModule_4();
}

DLL_EXPORT void* CreateCdmInstance(int interface_version, const char* key_system, uint32_t key_system_len, void* host_function, void* extra_data)
{
    delog(TEXT("CreateCdmInstance %d, %s, %lld, \n"), interface_version, key_system, key_system_len);
    void* instance = _CreateCdmInstance(interface_version, key_system, key_system_len, host_function, extra_data);
    if (!instance)
    {
        delog(TEXT("no origin instance created\n"));
        return nullptr;
    }

    return instance;
}

DLL_EXPORT void DeinitializeCdmModule()
{
    delog(TEXT("DeinitializeCdmModule\n"));
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