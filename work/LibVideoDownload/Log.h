#pragma once
#include <mutex>
#include <thread>
#include <plog/Log.h> // Step1: include the headers
#include "plog/Initializers/RollingFileInitializer.h"
#include <sstream>
#define LOG_NAME "log.txt"
#define FORDER_NAME "download"
std::string subFilename(std::string filePath);
//#define logPrint(content) Log::write(subFilename(std::string(__FILE__))+" "+__FUNCTION__+" line:"+std::to_string(__LINE__)+" >> "+content)

//extern thread_local std::string guid;
//#define logPrint(content) PLOGD << guid +" : "<< content
#ifdef _WIN32
#define logPrint(content) PLOGD << content    

#elif defined __APPLE__
#define logPrint(content) Log::write((std::stringstream() << subFilename(std::string(__FILE__))+" "+__FUNCTION__+" line:"+std::to_string(__LINE__)+" >> "+ content).str())
#endif

class Log
{
public:
	static void write(std::string content);
	static void setFilename(std::string filename);
	static int createDirectory(std::string path);
    static void sizeManage(std::string filename,int size);
public:
	static std::string filepath;
private:
	static std::mutex lock;

};

