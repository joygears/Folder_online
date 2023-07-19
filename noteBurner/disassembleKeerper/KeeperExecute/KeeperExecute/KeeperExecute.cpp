// shell_execute.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <Windows.h>
#include <Shlobj.h>


void (*_InitializeCdmModule_4)();
void* (*_CreateCdmInstance)(int interface_version, const char* key_system, uint32_t key_system_len,
    void* host_function, void* extra_data);
void  (*_DeinitializeCdmModule)();
char* (*_GetCdmVersion)();

int main()
{
    LPCWSTR newPath = LR"(C:\Users\Administrator\AppData\Roaming\NoteBurner Netflix Video Downloader)";  // 新路径

    //BOOL result = SHSetFolderPathW(CSIDL_APPDATA, NULL, 0, newPath);
    SetEnvironmentVariable(TEXT("APP_LOG_PATH"), TEXT(".\logs"));
    SetEnvironmentVariable(TEXT("APP_NATIVE_PATH"), TEXT("."));
    SetEnvironmentVariable(TEXT("APP_VMP_VERIFY"), TEXT("1"));
    SetEnvironmentVariable(TEXT("KEEPER_ID"), TEXT("keeper_16256"));
    SetEnvironmentVariable(TEXT("APP_IDENTIFIER"), TEXT("NoteBurner-netflix"));
    SetEnvironmentVariable(TEXT("NoteBurner-netflix_IPC_PORT"), TEXT("8012"));
   
    HMODULE hWidevine = LoadLibrary(TEXT("widevinecdm.dll"));

   
    _InitializeCdmModule_4 = (void (*)())GetProcAddress(hWidevine, "InitializeCdmModule_4");
    _CreateCdmInstance = (void* (*)(int interface_version, const char* key_system, uint32_t key_system_len,
        void* host_function, void* extra_data))GetProcAddress(hWidevine, "CreateCdmInstance");
    _DeinitializeCdmModule = (void (*)())GetProcAddress(hWidevine, "DeinitializeCdmModule");
    _GetCdmVersion = (char* (*)())GetProcAddress(hWidevine, "GetCdmVersion");

    _InitializeCdmModule_4();

    char ch;
    std::cin >> ch;
}


