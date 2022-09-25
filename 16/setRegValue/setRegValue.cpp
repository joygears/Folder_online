#include <iostream>
#include <Windows.h>

bool setRegValue(HKEY hKey, const char* lpSubKey, const char* lpValueName, int  dwType, const char* lpValue, bool noCreating);

int main()
{
	bool succ = setRegValue(HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\SuperProServer", "ConnectGroup", REG_SZ, "默认分组", false);
	std::cout << succ;
}




/*
	名称：setRegValue
	功能：设置注册表某个项的值
	参数：
			HKEY hKey  根路径
			const char * lpSubKey 子路径
			const char * lpValueName 项名称
			int  dwType  设置的值类型
			const char * lpValue 项值
			bool noCreating 是否创建该项
	返回值：
			bool 是否设置成功
*/
bool setRegValue(HKEY hKey, const char* lpSubKey, const char* lpValueName, int  dwType, const char* lpValue, bool noCreating) {
	DWORD dwDisposition;
	HKEY phkResult = HKEY_LOCAL_MACHINE;
	int success = 0;

	switch (noCreating) {
	case 0:
		if (RegCreateKeyExA(hKey, lpSubKey, 0, 0, 0, KEY_ALL_ACCESS, 0, &phkResult, &dwDisposition))
			break;
	case 1:
		if (RegOpenKeyExA(hKey, lpSubKey, 0, STANDARD_RIGHTS_WRITE | KEY_QUERY_VALUE | KEY_SET_VALUE | KEY_CREATE_SUB_KEY | KEY_NOTIFY | KEY_ENUMERATE_SUB_KEYS, &phkResult))
			break;
		if (dwType <= 0 || dwType >= 2)
			break;
		if (RegSetValueExA(phkResult, lpValueName, 0, dwType, (byte*)lpValue, strlen(lpValue) + 1)) break;
		success = 1;
	}
	RegCloseKey(hKey);
	RegCloseKey(phkResult);
	return success;
}
