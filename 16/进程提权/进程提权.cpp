// ConsoleApplication6.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <Windows.h>
int main()
{
    TOKEN_PRIVILEGES NewState;
    HANDLE TokenHandle;
    HANDLE hProcess = GetCurrentProcess();
    if (OpenProcessToken(hProcess, TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &TokenHandle) != 0) {
        if (LookupPrivilegeValueA(0, "SeDebugPrivilege", (PLUID)&NewState.Privileges)) {
            AdjustTokenPrivileges(TokenHandle, 0, &NewState, 0, 0, 0);
        }
        CloseHandle(TokenHandle);
    }
    getchar();
}


