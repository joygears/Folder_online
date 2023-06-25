#pragma once
#include <Windows.h>
#include <tchar.h>
#include <iostream>
#include <vector>
using namespace std;

void Log(const char* fmt, ...);
void writeToFile(const wchar_t* buf);

int Write( LPTSTR lpPath, LPSTR lpText);
std::wstring DecodeUtf8(string in);

std::string getCommandOutput(const std::string& command);
std::vector<std::string> splitString(const std::string& input, char delimiter);