#pragma once
#include <Windows.h>
#include <tchar.h>
#include <iostream>
using namespace std;

void delog(const char* fmt, ...);
void writeToFile(const wchar_t* buf);

int Write( LPTSTR lpPath, LPSTR lpText);
std::wstring DecodeUtf8(string in);
