#pragma once


#include <Windows.h>
#include <iostream>

using namespace std;

#define DLL_EXPORT extern "C" __declspec( dllexport )

struct verifyWrap {
	const wchar_t* chDycVfchm;
	HANDLE hFVfchm;
	HANDLE hSigVfchm;
	const wchar_t* chdycWidevine;
	HANDLE HDycWidevinecdm;
	HANDLE HSigWidevinecdm;
};

bool (*VerifyCdmHost_0)(verifyWrap*, int flag);
DLL_EXPORT int InitializeCdmModule_4();

