// urlopen.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <windows.h>
int  urlOpen(LPCSTR lpString2, bool);

int main()
{
    urlOpen("http://baidu.com", true);
    return 0;
}



int  urlOpen(LPCSTR aUrl, bool flag) {
    HKEY phkResult;
    char data[MAX_PATH * 2] = {0,};
    long cbData;
    STARTUPINFOA starup;
    PROCESS_INFORMATION ProcessInformation;
    if (strlen(aUrl) == 0) return 0;
    if (RegOpenKeyExA(HKEY_CLASSES_ROOT, "Applications\\iexplore.exe\\shell\\open\\command", 0, KEY_READ, &phkResult) != ERROR_SUCCESS) return 0;
    RegQueryValueA(phkResult, 0, data, &cbData);
    RegCloseKey(phkResult);
    if (strlen(data) == 0) return 0;
    if(strstr(data, "%1")==0) return 0;
    strcpy_s(strstr(data, "%1"), MAX_PATH * 2- MAX_PATH, aUrl);
    memset(&starup.lpReserved, 0, 16 * 4);
    starup.cb = 68;
    if (flag) {
        starup.lpDesktop = (char *)"WinSta0\\Default";
    }
    CreateProcessA(0, data, 0, 0, 0, 0, 0, 0, &starup, &ProcessInformation);
    return 0;
}