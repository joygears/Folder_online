#pragma once
#include <Windows.h>
#include "ollydbg.h"
extern DWORD* P4D375C ;
extern HINSTANCE* hInstance ;
extern HWND* hWndClient;
extern DLGPROC DialogFunc;
extern DWORD* dword_4D375C;
extern t_hardbpoint * hardpointAry;
extern t_thread** ppthreadAry;
extern void  (*Error)(const char*);
extern t_status* g_debugedProcessStatus;
int Hardbreakpoints(int);
int Sethardwarebreakpoint(unsigned long addr, int size, int type);
int Deletehardwarebreakpoint(int index);