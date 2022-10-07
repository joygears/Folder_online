// ConsoleApplication6.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <Windows.h>

void escalationOfRights() {
    TOKEN_PRIVILEGES NewState;
    HANDLE TokenHandle;
    HANDLE hProcess = GetCurrentProcess();
    if (OpenProcessToken(hProcess, TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &TokenHandle) != 0) {
       
        if (LookupPrivilegeValueA(0, "SeDebugPrivilege", &NewState.Privileges[0].Luid)) {
            NewState.PrivilegeCount = 1;
            NewState.Privileges[0].Attributes = 2;

            int a = AdjustTokenPrivileges(TokenHandle, 0, &NewState, 0, 0, 0);
            printf("%d",GetLastError());
        }
        CloseHandle(TokenHandle);
    }
}
bool occupyFile(const char* lpFileName) {
    bool isSucc;
    HANDLE TargetHandle;

    escalationOfRights();
    
    HANDLE hSysProcess = OpenProcess(PROCESS_DUP_HANDLE, false, 4);
    int a = GetLastError();
    
    if (!hSysProcess)
        return MessageBox(0, 0, 0, 0);

    HANDLE hFile = CreateFileA(lpFileName, GENERIC_READ, 0, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);
    if (!hFile)
        return 0;
    isSucc = DuplicateHandle(GetCurrentProcess(), hFile, hSysProcess, &TargetHandle, 0, false, DUPLICATE_CLOSE_SOURCE | DUPLICATE_SAME_ACCESS);
    CloseHandle(hSysProcess);

    return isSucc;
}

int main()
{
    const char* lpFileName = R"(E:\projects\ConsoleApplication6\Debug\ConsoleApplication6.exe)";
    occupyFile(lpFileName);
    getchar();
}


