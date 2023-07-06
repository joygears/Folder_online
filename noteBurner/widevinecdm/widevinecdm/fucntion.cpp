#include "fucntion.h"
#include <cstdarg>
#include <vector>
#include <fstream>
#include <mutex>
#include <cstdio>

void Log(const wchar_t* fmt)
{ 
   
}


void Log(const char * fmt, ...)
{
    CHAR _buf[65536] = { 0 };
    CHAR _buf2[65536] = "czl ";
    va_list args;
    int n;
    va_start(args, fmt);
    vsprintf_s(_buf, 65536, fmt, args);
    vsprintf_s(_buf, 65536, _buf, args);
    strcat(_buf2, _buf);
    wstring str = DecodeUtf8(_buf2);
    str += L"\n";
    writeToFile(str.c_str());
    OutputDebugString(str.c_str());
    wprintf(str.c_str());
    va_end(args);
}

void writeToFile(const wchar_t * buf) {
    static std::mutex mtx;
    std::unique_lock<std::mutex> lk(mtx);

    std::wofstream fileOut;
    fileOut.open(".\\czl.log", std::ios::app);
    if (!fileOut.is_open())
    {
        fileOut.close();
        std::perror("fileOut.open");
        std::exit(0);
    }
    fileOut.write(buf,wcslen(buf));
   
}


int Write( LPTSTR lpPath, LPSTR lpText)
{
	//创建文件
    FILE * hFile = _wfopen(lpPath, TEXT("a+"));

	if (hFile == nullptr)
	{
		Log("hFile == nullptr getLastError %d", GetLastError());
		return -1;
	}

	
	// 将内容写入文件
	DWORD dwWriten = 0;
    fputs(lpText, hFile);
	

    fclose(hFile);
	return 1;
}


std::wstring DecodeUtf8(string in)
{
    wstring s(in.length(), (' ')); //"tchar.h"
    size_t len = ::MultiByteToWideChar(CP_UTF8, 0,
        in.c_str(), in.length(),
        &s[0], s.length());
    s.resize(len);
    return s;
}

std::string EncodeUtf8(std::wstring in)
{
    std::string s(in.length() * 3 + 1, ' ');
    size_t len = ::WideCharToMultiByte(CP_UTF8, 0,
        in.c_str(), in.length(),
        &s[0], s.length(),
        NULL, NULL);
    s.resize(len);
    return s;
}

std::string getCommandOutput(const std::string& command) {
    FILE* pipe = _popen(command.c_str(), "r"); // 以读取模式启动命令

    if (!pipe) {
        std::cout << "无法执行命令！" << std::endl;
        return "";
    }

    char buffer[128];
    std::string result = "";

    while (!feof(pipe)) {
        if (fgets(buffer, 128, pipe) != NULL)
            result += buffer;
    }

    _pclose(pipe); // 关闭管道

    return result;
}

std::vector<std::string> splitString(const std::string& input, char delimiter) {
    std::vector<std::string> result;
    std::string::size_type start = 0;
    std::string::size_type end = input.find(delimiter, start);

    while (end != std::string::npos) {
        result.push_back(input.substr(start, end - start));
        start = end + 1;
        end = input.find(delimiter, start);
    }

    result.push_back(input.substr(start));

    return result;
}


