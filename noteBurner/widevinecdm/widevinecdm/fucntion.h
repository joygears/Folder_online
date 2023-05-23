#pragma once
#include <Windows.h>
#include <tchar.h>
void delog(const wchar_t* fmt, ...);
void writeToFile(const wchar_t* buf);

int Write( LPTSTR lpPath, LPSTR lpText);
