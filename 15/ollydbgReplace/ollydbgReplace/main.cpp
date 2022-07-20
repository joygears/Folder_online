#include "hook.hpp"
#include "Hardbreakpoint.h"
FARPROC g_func = (FARPROC)0x004089EC;
hook hk;
BOOL APIENTRY DllMain(HMODULE hModule,
    DWORD  ul_reason_for_call,
    LPVOID lpReserved
)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        hk.hook_by_code(g_func, (PROC)Deletehardwarebreakpoint);
        break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
        break;
    case DLL_PROCESS_DETACH:
        hk.unhook_by_code();
        break;
    }
    return TRUE;
}
