// shell_execute.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <Windows.h>
#include <Shlobj.h>
int main()
{
    LPCWSTR newPath = LR"(C:\Users\Administrator\AppData\Roaming\NoteBurner Netflix Video Downloader)";  // 新路径

    BOOL result = SHSetFolderPathW(CSIDL_APPDATA, NULL, 0, newPath);
    SetEnvironmentVariable(TEXT("APP_VMP_VERIFY"), TEXT("1"));
    LoadLibrary(TEXT("cshell.dll"));
    char ch;
    std::cin >> ch;
}


