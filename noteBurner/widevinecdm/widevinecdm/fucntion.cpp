#include "fucntion.h"
#include <Windows.h>
#include <cstdarg>
#include <iostream>

void delog(const wchar_t* fmt, ...)
{
    TCHAR _buf[256] = { 0 };
    va_list args;
    int n;
    va_start(args, fmt);
    wprintf(fmt, args);
    swprintf_s(_buf, 256, fmt,args);
    OutputDebugString(_buf);
    va_end(args);
}
