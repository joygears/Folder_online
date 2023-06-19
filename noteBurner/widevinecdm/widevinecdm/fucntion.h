#pragma once
#include <Windows.h>
#include <tchar.h>
#include <iostream>
using namespace std;

void Log(const char* fmt, ...);
void writeToFile(const wchar_t* buf);

int Write( LPTSTR lpPath, LPSTR lpText);
std::wstring DecodeUtf8(string in);
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
        originFunPtr = reinterpret_cast<unsigned char*>(**(int**)(originFunPtr + 2)) ;
    }
    if (originFunPtr[0] == 0xEB) {
        originFunPtr = originFunPtr + originFunPtr[1] + 2;
        if (originFunPtr[0] == 0xFF && originFunPtr[1] == 0x25) {
            originFunPtr = reinterpret_cast<unsigned char*>(*(int*)(originFunPtr + 2));
        }
        if (originFunPtr[0] == 0xE9) {
            originFunPtr = originFunPtr + *(int*)(originFunPtr + 1) + 5;
        }
    }
    if (originFunPtr[0] == 0xE9) {
        originFunPtr = originFunPtr + *(int*)(originFunPtr + 1) + 5;
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