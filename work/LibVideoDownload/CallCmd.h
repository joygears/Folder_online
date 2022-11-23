#pragma once
#include <iostream>
#include <string>
#include "process.hpp"
#include "utils.h"
using namespace std;
using namespace TinyProcessLib;

class CallCmd
{
public:
	
	~CallCmd();
	void setExePath(string exepath);
	void stopCMD();
	int runCMD(string  Utf8str, Callback stateback);
	string runCMD(string  Utf8str);
public:
	std::string guid="";
private:
	Process* process=nullptr;
	std::function<void(const char* bytes, size_t n)> callback = nullptr;
	string path="";
	
public:
	static string exePath;
};

