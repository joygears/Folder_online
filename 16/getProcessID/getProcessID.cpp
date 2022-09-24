// ConsoleApplication1.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。

#include <Windows.h>
#include <tlhelp32.h>
#include <iostream>




DWORD GetPidByPName(const wchar_t* processName);

int main()
{
	DWORD pid;
	pid  = GetPidByPName(TEXT("Everything.exe"));
	std::cout << pid;
}


/*
	name:GetPidByPName
	功能：通过进程名获取进程id
	参数：const wchar_t* processName 进程名称
	返回值： DWORD 若获取成功 返回 进程id, 若失败，或找不到则返回0
*/
DWORD GetPidByPName(const wchar_t* processName) {
	LPPROCESSENTRY32 proEntry = { 0, };
	HANDLE hSnapshot = 0;
	DWORD th32ProcessID = 0;

	hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	proEntry = new PROCESSENTRY32();
	proEntry->dwSize = sizeof(PROCESSENTRY32);

	if (Process32First(hSnapshot, proEntry)) {
		if (lstrcmpi(proEntry->szExeFile, processName) == 0) { //当进程名相等的时候
			th32ProcessID = proEntry->th32ProcessID;
			delete proEntry;
			return th32ProcessID;
		}
		while (Process32Next(hSnapshot, proEntry)) {
			if (lstrcmpi(proEntry->szExeFile, processName) == 0) {
				th32ProcessID = proEntry->th32ProcessID;
				delete proEntry;
				return th32ProcessID;
			}
		}
	}
	int error = ::GetLastError();
	CloseHandle(hSnapshot);
	delete proEntry;
	return 0;
}

