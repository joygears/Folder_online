#include "fucntion.h"
#include <cstdarg>

#include <fstream>
#include <mutex>


void Log(const wchar_t* fmt)
{ 
   
}


void Log(const char * fmt, ...)
{
    CHAR _buf[256] = { 0 };
    CHAR _buf2[256] = "czl ";
    va_list args;
    int n;
    va_start(args, fmt);
    vsprintf_s(_buf, 256, fmt, args);
    vsprintf_s(_buf, 256, _buf, args);
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

template<typename T>
T hookCodePatch(T originFun, T hookFuntion)
{
    const int patchSize = 10; // 假设需要 patch 的字节数
    const int pageSize = 5;
    unsigned char* patchedMemory = new unsigned char[patchSize];
    unsigned char* originFunPtr = reinterpret_cast<unsigned char*>(originFun);

    // 如有必要， 将原函数转到实际的函数地址
    DWORD oldProtect;
    VirtualProtect(patchedMemory, patchSize, PAGE_EXECUTE_READWRITE, &oldProtect);

    if (originFunPtr[0] == 0xFF && originFunPtr[1] == 0x25) {
        originFunPtr = reinterpret_cast<unsigned char*>(**(int**)(originFunPtr + 2));
    }
    if (originFunPtr[0] == 0xEB) {
        originFunPtr = originFunPtr + originFunPtr[1] + 2;
        if (originFunPtr[0] == 0xFF && originFunPtr[1] == 0x25) {
            originFunPtr = reinterpret_cast<unsigned char*>(*(int*)(originFunPtr + 2));
        }
        if (originFunPtr[0] == 0xE9) {
            originFunPtr = originFunPtr + *(int*)(originFunPtr + 1);
        }
    }

    // 复制 originFun 的前五个字节到 patchedMemory
    memcpy(patchedMemory, originFunPtr, 5);

    intptr_t hookOffset = (reinterpret_cast<intptr_t>(originFunPtr) + 5) - reinterpret_cast<intptr_t>(patchedMemory + 0xA);

    // 修改 patchedMemory 的后五个字节为跳转到 originFun + 5 的指令
    patchedMemory[5] = 0xE9; // x86 跳转指令的操作码
    memcpy(patchedMemory + 6, &hookOffset, sizeof(hookOffset));
    // 计算跳转偏移量
    hookOffset = reinterpret_cast<intptr_t>(hookFuntion) - (reinterpret_cast<intptr_t>(originFunPtr) + 5);


    // 修改 originFun 的前五个字节为跳转到 hookFunction 的指令

    VirtualProtect(originFunPtr, pageSize, PAGE_EXECUTE_READWRITE, &oldProtect);
    originFunPtr[0] = 0xE9; // x86 跳转指令的操作码
    memcpy(originFunPtr + 1, &hookOffset, sizeof(hookOffset));
    VirtualProtect(originFunPtr, pageSize, oldProtect, &oldProtect);
    return (T)patchedMemory;
}
