#include <stdio.h>
#include <conio.h>
#include <windows.h>
#include <QtWidgets/qapplication.h>
#include "QtWidgetsApplication1.h"

char* wideToMulti(UINT codePage, LPWSTR lpWideCharStr);
int main(int argc, char** argv);


int APIENTRY WinMain(HINSTANCE hInstance,
    HINSTANCE hPrevInstance,
    LPSTR     lpCmdLine,
    int       nCmdShow)
{
    int pNumArgs = 0;
    __int64 argc = 0;
    LPSTR* argv = 0;
    int retCode = 0;
 
    LPWSTR* hMem = CommandLineToArgvW(GetCommandLineW(),&pNumArgs);
    if (hMem == 0) {
        return -1;
    }
    else {
        argc = pNumArgs + 1;
        LPSTR* aryArgv  = new LPSTR[argc];
        argv = aryArgv;
        for (int i = 0; i != pNumArgs; i++) {
            argv[i] = wideToMulti(0, hMem[i]);
        }
        argv[pNumArgs] = 0;
        LocalFree(hMem);
        retCode =  main(pNumArgs, argv);

        for (int i = 0; i != pNumArgs && argv[i] != 0; i++) {
            delete[] argv[i];
        }
        delete[] argv;
        return retCode;
    }
}

int main(int argc, char** argv) {
    QApplication a(argc,argv);
    QtWidgetsApplication1 w;
    w.show();
    return a.exec();
}
char* wideToMulti(UINT codePage, LPWSTR lpWideCharStr) {
    int size = 0;
    char* lpCharStr = 0;

    size = WideCharToMultiByte(codePage, 0, lpWideCharStr, -1, 0, 0, 0, 0);
    lpCharStr = new char[size];

    WideCharToMultiByte(codePage, 0, lpWideCharStr, -1, lpCharStr, size, 0, 0);
    return lpCharStr;
}