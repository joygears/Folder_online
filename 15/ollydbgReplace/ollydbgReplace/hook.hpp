#pragma once
#include <Windows.h>
class hook {
public:
    BOOL hook_by_code(FARPROC pfnOrg, PROC pfnNew) {
        DWORD dwOldProtect, dwAddress;
        BYTE pBuf[6] = { 0xE9,0,0,0,0, 0x90 };
        PBYTE pByte;
        pByte = (PBYTE)pfnOrg;
        if (pByte[0] == 0xE9)//若已被勾取，则返回False
            return FALSE;
        VirtualProtect((LPVOID)pfnOrg, 12, PAGE_EXECUTE_READWRITE, &dwOldProtect);//为了修改字节，先向内存添加“写”的属性
        memcpy(pOrgBytes, pfnOrg, 6);//备份原有代码
        dwAddress = (DWORD64)pfnNew - (DWORD64)pfnOrg - 5;//计算JMP地址   => XXXX = pfnNew - pfnOrg - 5
        memcpy(&pBuf[1], &dwAddress, 4);//E9，剩下后面4个字节为跳转的地址
        memcpy(pfnOrg, pBuf, 6);//复制指令，跳转到hook逻辑

        memcpy(&pByte[6], pOrgBytes, 6);//后面的int 3指令进行修改，跳转到原api逻辑
        pByte[8] -= 6;//修正跳转偏移

        VirtualProtect((LPVOID)pfnOrg, 12, dwOldProtect, &dwOldProtect);//恢复内存属性
        this->pFunc = pfnOrg;
        return TRUE;
    }
    BOOL unhook_by_code() {

        DWORD dwOldProtect;
        PBYTE pByte;
        pByte = (PBYTE)pFunc;
        if (pByte[0] != 0xE9)//若已脱钩，则返回False
            return FALSE;
        VirtualProtect((LPVOID)pFunc, 6, PAGE_EXECUTE_READWRITE, &dwOldProtect);//向内存添加“写”的属性，为恢复原代码做准备
        memcpy(pFunc, pOrgBytes, 6);//脱钩
        VirtualProtect((LPVOID)pFunc, 6, dwOldProtect, &dwOldProtect);//恢复内存属性
        return TRUE;
    }
public:
    BYTE pOrgBytes[6] = {0,};
	 FARPROC pFunc;
};