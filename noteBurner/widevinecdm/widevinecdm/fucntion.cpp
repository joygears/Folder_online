#include "fucntion.h"
#include <cstdarg>

#include <fstream>
#include <mutex>


void delog(const wchar_t* fmt)
{ 
   
}


void delog(const char * fmt, ...)
{
    CHAR _buf[256] = { 0 };
    CHAR _buf2[256] = "czl ";
    va_list args;
    int n;
    va_start(args, fmt);
    vprintf(fmt, args);
    vsprintf_s(_buf, 256, fmt, args);
    vsprintf_s(_buf, 256, _buf, args);
    strcat(_buf2, _buf);
    wstring str = DecodeUtf8(_buf2);
    writeToFile(str.c_str());
    OutputDebugString(str.c_str());
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
		delog("hFile == nullptr getLastError %d", GetLastError());
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