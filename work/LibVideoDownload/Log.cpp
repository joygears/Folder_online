#include "Log.h"
#include <iostream>
#include <iosfwd>
#include <fstream>
#include <sstream>
#ifdef _WIN32
    #include <direct.h>
	#include <windows.h>
	#include <shlobj_core.h>
#endif

using namespace std;

static plog::RollingFileAppender<plog::TxtFormatter> fileAppender(LOG_NAME);
// thread_local std::string guid = getGuid();
std::string defaultLogPath() {
#ifdef _WIN32
	char buffer[MAX_PATH];
	BOOL result = SHGetSpecialFolderPathA(0, buffer, CSIDL_LOCAL_APPDATA, false);
	string appLocal = buffer;
	appLocal += R"(\HitPaw Software\HitPawVideoConverter\logs)";
	appLocal += std::string("/") + FORDER_NAME;
	appLocal += std::string("/") + LOG_NAME;
    Log::createDirectory(appLocal);
	fileAppender.setFileName(appLocal.c_str());
	fileAppender.setMaxFiles(1);
	fileAppender.setMaxFileSize(1024 * 1024*8);
	plog::init(plog::debug, &fileAppender);

	return appLocal;
#elif defined __APPLE__
	return LOG_NAME;
#endif 

	
}
std::string Log::filepath = defaultLogPath();
std::mutex  Log::lock;


std::string getCurrentTime() {
	time_t now = time(0);
	// 把 now 转换为字符串形式
	char* dt = ctime(&now);
	std::string curTime = dt;
	curTime.erase(std::remove(curTime.begin(), curTime.end(), '\n'), curTime.end());
	return curTime;

}

std::string subFilename(std::string filePath) {
	string::size_type iPos = filePath.find_last_of('\\') + 1;
	string filename = filePath.substr(iPos, filePath.length() - iPos);
	return filename;
}

void Log::write(std::string content)
{
	lock.lock();
	ofstream outfile;
	outfile.open(filepath, ios::app);
	outfile << getCurrentTime()<< " " << content << endl;
	outfile.close();
	lock.unlock();
}
bool DirExist(char * tempDirPath){
    struct stat info;
    if (stat(tempDirPath, &info) != 0) {  // does not exist
        return false;
    }
    return true;
}
int Log::createDirectory(std::string path)
{    int len = path.length();
    char tmpDirPath[256] = { 0 };
    if (DirExist((char *)path.c_str())== false)
   {
	for (int i = 0; i < len; i++)
	{
		tmpDirPath[i] = path[i];
		if (tmpDirPath[i] == '\\' || tmpDirPath[i] == '/')
		{
			if (DirExist(tmpDirPath) == false)
			{
#ifdef _WIN32
                int ret = _mkdir(tmpDirPath);
                if (ret == -1) return ret;
#elif defined __APPLE__
                int ret = mkdir(tmpDirPath, 0775);
                if (ret == -1) return ret;
#endif
				
				
			}
		}
	}
}
	return 0;
}


void Log::setFilename(std::string filename)
{
	
	filename += std::string("/") + FORDER_NAME;
	filename += std::string("/")+ LOG_NAME;
    
    Log::filepath = filename;
    createDirectory(filename);
   
#ifdef _WIN32
    fileAppender.setFileName(filename.c_str());
#elif defined __APPLE__
    sizeManage(filename,1024*1024*8);
    
#endif
	
}


void Log::sizeManage(std::string filename,int maxSize){
    lock.lock();
    FILE *fp=fopen(filename.c_str(),"r");
    if(fp) {
    fseek(fp,0L,SEEK_END);
    long size=ftell(fp);
    fclose(fp);
    if(size > maxSize){
        remove(filename.c_str());
    }
    }
    lock.unlock();
}
