//
//  utils_win.cpp
//  LibVideoDownload
//
//  Created by czl on 2022/8/25.
//
#include <Windows.h>
#include <guiddef.h>
#include <combaseapi.h>

#pragma comment(lib, "version.lib")

#include "utils.h"


std::string GetFileVersion(char* strFilePath)
{
    DWORD dwSize;
    DWORD dwRtn;
    std::string szVersion;
    //ªÒ»°∞Ê±æ–≈œ¢¥Û–°
    dwSize = GetFileVersionInfoSize(strFilePath, NULL);
    if (dwSize == 0)
    {
        return "GetFileVersionInfoSize failed";
    }
    char* pBuf;
    pBuf = new char[dwSize + 1];
    if (pBuf == NULL)
        return "";
    memset(pBuf, 0, dwSize + 1);
    //ªÒ»°∞Ê±æ–≈œ¢
    dwRtn = GetFileVersionInfo(strFilePath, NULL, dwSize, pBuf);
    if (dwRtn == 0)
    {
        return "";
    }
    LPVOID lpBuffer = NULL;
    UINT uLen = 0;
    //∞Ê±æ◊ ‘¥÷–ªÒ»°–≈œ¢

    dwRtn = VerQueryValue(pBuf,
        TEXT("\\StringFileInfo\\080404b0\\ProductVersion"), // 0804÷–Œƒ
        // 04b0º¥1252,ANSI
        //ø…“‘¥”ResourceView÷–µƒVersion÷–BlockHeader÷–ø¥µΩ
        //ø…“‘≤‚ ‘µƒ Ù–‘
        /*
        CompanyName
        FileDescription
        FileVersion
        InternalName
        LegalCopyright
        OriginalFilename
        ProductName
        ProductVersion
        Comments
        LegalTrademarks
        PrivateBuild
        SpecialBuild
        */
        & lpBuffer,
        &uLen);
    if (dwRtn == 0)
    {
        return "";
    }
    szVersion = (char*)lpBuffer;
    delete pBuf;
    return szVersion;
}

string getVideoDownloadVersion() {
    char  szFileName[MAX_PATH];
    GetModuleFileName(NULL, szFileName, MAX_PATH);
    string strFileName = szFileName;
    string Dir = strFileName.substr(0, strFileName.find_last_of("\\")+1);
    string VideoDownload = Dir + "LibVideoDownload.dll";
    return GetFileVersion((char *)VideoDownload.c_str());
}


std::string UnicodeToUtf8(const std::wstring& in_wStr)
{
    int nNeedChars = WideCharToMultiByte(CP_UTF8, 0, in_wStr.c_str(), -1, 0, 0, 0, 0);
    if (nNeedChars > 0)//再次判断一下
    {
        std::vector<char> temp(nNeedChars);
        ::WideCharToMultiByte(CP_UTF8, 0, in_wStr.c_str(), -1, &temp[0], nNeedChars, 0, 0);
        return std::string(&temp[0]);
    }

    return std::string();
}
int Utf8_To_Unicode(string strSrc, wstring& strRet)
{
    wchar_t wBuff[102400] = { 0 };
    int iRet = MultiByteToWideChar(CP_UTF8, 0, strSrc.c_str(), -1, wBuff, 102400);
    if (iRet > 0) {
        strRet = wBuff;
        return TRUE;
    }
    return FALSE;
}


std::string get_executable_dir() {

    std::wstring exeDir = L"";
    wchar_t szExeName[MAX_PATH] = { 0, };
    volatile int lastIndex = 0;
    ::GetModuleFileNameW(NULL, szExeName, MAX_PATH);
    exeDir = szExeName;
    lastIndex = exeDir.find_last_of(L"\\");
    exeDir = exeDir.substr(0, lastIndex);
    return UnicodeToUtf8(exeDir);
}
//string getGuid() {
//    char buffer[64] = { 0, };
//    GUID pguid;
//
//    CoCreateGuid(&pguid);
//
//    sprintf_s(buffer, 64, "{%08X%04X%04X%02X%02X%02X%02X%02X%02X%02X%02X}", pguid.Data1,
//        pguid.Data2,
//        pguid.Data3,
//        pguid.Data4[0],
//        pguid.Data4[1],
//        pguid.Data4[2],
//        pguid.Data4[3],
//        pguid.Data4[4],
//        pguid.Data4[5],
//        pguid.Data4[6],
//        pguid.Data4[7]);
//
//    return buffer;
//}
