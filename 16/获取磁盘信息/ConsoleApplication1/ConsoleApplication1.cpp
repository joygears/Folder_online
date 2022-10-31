// ConsoleApplication1.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <Windows.h>

#define STR_LEN 256


struct packed {
    char Drive;
    byte nDriveType;
    long TotalNumberOfMBs;
    long FreeMBsAvailableToCaller;
    char buffer[8];
};


int main()
{
    byte command;
    char Src[1024];
    char szLogicalDrive[STR_LEN];
    char* pLogicalDrive = szLogicalDrive;
    char szFileSystemNameBuffer[MAX_PATH] = {0,};
    SHFILEINFOA psfi;
    int lenTypeName, lenFileSystemName;
    ULARGE_INTEGER FreeBytesAvailableToCaller = { 0, },TotalNumberOfBytes = {0,};
    long FreeMBsAvailableToCaller = 0, TotalNumberOfMBs = 0;
    int pos = 1;

    Src[0] = 103;

    ::GetLogicalDriveStringsA(STR_LEN, szLogicalDrive);
    if (pLogicalDrive[0] != 0) {
        do {
            ::GetVolumeInformationA(pLogicalDrive, 0, 0, 0, 0, 0, szFileSystemNameBuffer,MAX_PATH);
            ::SHGetFileInfoA(pLogicalDrive, 128, &psfi, 352,1040);
            lenTypeName = strlen(psfi.szTypeName) + 1;
            lenFileSystemName = strlen(szFileSystemNameBuffer) + 1;
            if (pLogicalDrive[0] != 'A' && pLogicalDrive[0] != 'B' && ::GetDiskFreeSpaceExA(pLogicalDrive, &FreeBytesAvailableToCaller, &TotalNumberOfBytes, 0) != 0) {
                FreeMBsAvailableToCaller = FreeBytesAvailableToCaller.QuadPart >> 20;
                TotalNumberOfMBs = TotalNumberOfBytes.QuadPart >> 20;
            }
            
            Src[pos] = pLogicalDrive[0];
            Src[pos+1] = ::GetDriveTypeA(pLogicalDrive);
            memcpy(&Src[pos + 2], &TotalNumberOfMBs, 4);
            memcpy(&Src[pos + 6], &TotalNumberOfMBs, 4);
            memcpy(&Src[pos+10], psfi.szTypeName, lenTypeName);
            memcpy(&Src[pos+10+ lenTypeName], szFileSystemNameBuffer, lenFileSystemName);
            pos += lenFileSystemName + lenTypeName + 10;
            pLogicalDrive = strlen(pLogicalDrive) + 1 + pLogicalDrive;
        } while (pLogicalDrive[0] != 0);


    }
    return 0;
}


