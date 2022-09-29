// ConsoleApplication6.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <io.h>
#include <Windows.h>

void CreateMultiDirectory(const char* filePath) {
	char szFilePath[MAX_PATH] = { 0, };
	int i = 0;
	if (strlen(filePath) > 0) {
		do {
			if (filePath[i] == '\\' or filePath[i] == '/') {

				memmove(szFilePath, filePath, i);
				if (_access(szFilePath, 0))
					CreateDirectoryA(szFilePath, 0);	
			}
			i++;
		} while (i < strlen(filePath));

	}
}

int main()
{
	CreateMultiDirectory(R"(C:\Users\Administrator\source\repos\mypath\Debug\ConsoleApplication6.exe)");
}


