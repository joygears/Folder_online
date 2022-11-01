// RemoteControlServer.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <Windows.h>
#include "rc4crpt.h"
#pragma comment(lib,"ws2_32.lib")

using namespace std;

void getDiskInfo(SOCKET clientSocket);

int main(){
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

    SOCKET clientSocket= 0;
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
    cout << "请输入功能序号" << endl;
    cin >> orinal;
    switch (orinal.c_str()[0]) {
    case '1':
        getDiskInfo(clientSocket);
        break;
    default:
        cout << "无此功能" << endl;
    }


    return  0;
}
#define LEN_DATA 22
void getDiskInfo(SOCKET clientSocket) {

    char msg[8192];//存储传送的消息


    cout << "您选择的是获取磁盘信息功能" << endl;
    char keyAry[256];
    string data = { 0x4B,0x75,0x47,0x6F,0x75,LEN_DATA,0x00,0x00,0x00,LEN_DATA,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x03,0x1C,0x00,0x00 };

    rc4_init(keyAry, (char*)"1593044206", strlen("1593044206"));
    rc4_cryp(keyAry, (char*)data.c_str(), LEN_DATA);
    //getline(cin, data);
    const char* sendData;
    sendData = data.c_str();
    cout << "向客户端发送指令" << endl;
    send(clientSocket, sendData, LEN_DATA, 0);
    int num = recv(clientSocket, msg, 8192, 0);
    if (num > 0)
    {
        msg[num] = '\0';
        cout << "Client say: " << msg << endl;

    }

}

