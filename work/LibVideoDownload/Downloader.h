#pragma once

#ifndef  DLL_EXPORT
	#ifdef _WIN32
	#define  DLL_EXPORT __declspec(dllexport)
	#elif defined __APPLE__
	#define  DLL_EXPORT 
	#endif 
#endif 

enum class UrlType{
	SINGLE, //不是视频列表
	FULL, //完整视频列表
	PART //视频列表的一部分
};

class DLL_EXPORT STATECALLBACK {
public:
	virtual void  stateInform(char* json) = 0;
};

class DLL_EXPORT Downloader
{
public:
	bool parse(char* json, STATECALLBACK* callback);
	bool download(char* json, STATECALLBACK* callback);
	bool stop(STATECALLBACK* callBack);
	Downloader();
	~Downloader();
	static bool checkPlaylist(const char* url);
	static bool checkFullPlaylist(const char* url);
	static UrlType getUrlType(const char* url);
	static void  getVersion(char* szVersion);
	static void setLogPath(char* logPath);
	static void setexePath(char* exePath);
private:
	void * cmd = nullptr;
	void* informer = nullptr;
};

