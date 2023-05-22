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

// ContentDecryptionModule interface that all CDMs need to implement.
// The interface is versioned for backward compatibility.
// Note: ContentDecryptionModule implementations must use the allocator
// provided in CreateCdmInstance() to allocate any Buffer that needs to
// be passed back to the caller. Implementations must call Buffer::Destroy()
// when a Buffer is created that will never be returned to the caller.



bool (*VerifyCdmHost_0)(verifyWrap*, int flag);
void (*_InitializeCdmModule_4)();
void*  (*_CreateCdmInstance)(int interface_version, const char* key_system, uint32_t key_system_len,
	void* host_function, void* extra_data);

DLL_EXPORT void InitializeCdmModule_4();
DLL_EXPORT void* CreateCdmInstance(int interface_version, const char* key_system, uint32_t key_system_len,
	void * host_function, void* extra_data);
