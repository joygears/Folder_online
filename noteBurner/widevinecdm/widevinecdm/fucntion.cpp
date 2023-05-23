#include "fucntion.h"
#include <cstdarg>
#include <iostream>
#include <fstream>
#include <mutex>

void delog(const wchar_t* fmt, ...)
{
    TCHAR _buf[256] = { 0 };
    TCHAR _buf2[256] = TEXT("czl ");
    va_list args;
    int n;
    va_start(args, fmt);
    vwprintf(fmt, args);
    vswprintf_s(_buf, 256, fmt,args);
    vswprintf_s(_buf, 256, _buf, args);
    wcscat(_buf2, _buf);
    //writeToFile(_buf2);
    OutputDebugString(_buf2);
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
    FILE * hFile = _wfopen(lpPath, TEXT("w"));

	if (hFile == nullptr)
	{
		delog(TEXT("hFile == nullptr getLastError %d"), GetLastError());
		return -1;
	}

	
	// 将内容写入文件
	DWORD dwWriten = 0;
    fputs(lpText, hFile);
	

    fclose(hFile);
	return 1;
}
