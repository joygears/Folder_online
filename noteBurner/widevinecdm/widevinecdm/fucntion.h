#pragma once
#include <Windows.h>
#include <tchar.h>
#include <iostream>
using namespace std;

void Log(const char* fmt, ...);
void writeToFile(const wchar_t* buf);

int Write( LPTSTR lpPath, LPSTR lpText);
std::wstring DecodeUtf8(string in);
template <typename T>
T hookCodePatch(T originFun, T hookFuntion);
