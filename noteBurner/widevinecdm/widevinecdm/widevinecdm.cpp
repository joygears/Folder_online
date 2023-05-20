// widevinecdm.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include "widevinecdm.h"





int main()
{
	wstring dycWidevine = TEXT(R"(C:\Program Files (x86)\NoteBurner\NoteBurner Netflix Video Downloader\resources\app\com.noteburner.netflix\native\sig_files\widevinecdm.dll)");
	wstring sigWidevine = TEXT(R"(C:\Program Files (x86)\NoteBurner\NoteBurner Netflix Video Downloader\resources\app\com.noteburner.netflix\native\sig_files\widevinecdm.dll.sig)");
	wstring dycVfchm = TEXT(R"(C:\Program Files (x86)\NoteBurner\NoteBurner Netflix Video Downloader\resources\app\com.noteburner.netflix\native\sig_files\vfchm.dll)");
	wstring sigVfchm = TEXT(R"(C:\Program Files (x86)\NoteBurner\NoteBurner Netflix Video Downloader\resources\app\com.noteburner.netflix\native\sig_files\vfchm.dll.sig)");
	verifyWrap wrap;
    TCHAR _buf[256] = { 0 };
   



	HANDLE HDycWidevinecdm = CreateFile(dycWidevine.c_str(), GENERIC_READ,1,0,3,0x80,0);
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
	VerifyCdmHost_0 = (bool (*)(verifyWrap*, int flag))GetProcAddress(hWidevine, "VerifyCdmHost_0");
    
	int retcode = VerifyCdmHost_0(&wrap, 2);

    swprintf_s(_buf, 256, L"widevine VerifyCdmHost_0 retcode %d", retcode);
    OutputDebugString(_buf);
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
		main();
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

DLL_EXPORT int InitializeCdmModule_4()
{
    return 1;
}
