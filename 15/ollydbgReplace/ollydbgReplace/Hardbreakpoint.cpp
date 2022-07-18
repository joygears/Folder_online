#include "Hardbreakpoint.h"
DWORD * P4D375C = (DWORD*)0x4D375C;
HINSTANCE* hInstance = (HINSTANCE*)0x004D3B78;
HWND *hWndClient = (HWND*)0x004D3B80;
DLGPROC DialogFunc = (DLGPROC)0x00408E1C;
int Hardbreakpoints(int arg_0)
{
    if (*P4D375C == 0) {
        return -1;
    }
    return DialogBoxParamA(*hInstance, "DIA_HARD", *hWndClient, DialogFunc, 0);
}
