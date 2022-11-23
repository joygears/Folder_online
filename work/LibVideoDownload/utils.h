#pragma once
#include <string>
#include <vector>
using namespace std;
std::vector<std::string>& split(const std::string& s, char delim, std::vector<std::string>& elems);

string getSavePath(string jsonstr);

string createDownloadJson(string jsonstr, string dir);

string abs_path(string path);

string getVideoDownloadVersion();

std::string getGuid();
std::string stripBlank(std::string str);
std::string get_executable_dir();
int Utf8_To_Unicode(string strSrc, wstring& strRet);