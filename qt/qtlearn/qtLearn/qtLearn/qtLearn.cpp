#include <stdio.h>
#include <conio.h>
#include <windows.h>




int APIENTRY WinMain(HINSTANCE hInstance,
    HINSTANCE hPrevInstance,
    LPSTR     lpCmdLine,
    int       nCmdShow)
{
    int pNumArgs = 0;
    __int64 argc = 0;


    LPWSTR* hMem = CommandLineToArgvW(GetCommandLineW(),&pNumArgs);
    if (hMem == 0) {
        return 0;
    }
    else {
        argc = pNumArgs + 1;
        LPWSTR* aryArgv  = new LPWSTR[argc];

    }
    return 0;
}