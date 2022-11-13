#include<winsock2.h>
#include<iostream>
#include <stdio.h>
#include<string>
using namespace std;
#pragma comment(lib,"ws2_32.lib")

#define LEN_DATA 22

void rc4_init(char* keyAry, char* key, int len);
void rc4_cryp(char* keyAry, char* data, int len);

//int main(int argc, char* argv[]) {
//    int i = 0x00408238;
//    char keyAry[256];
//   
//    float f = (float)0x0211DBD0;
//   
//    memcpy(&f, &i, 4);
//    i = f;
//    //初始化DLL
//    WORD sockVersion = MAKEWORD(2, 2);
//    WSADATA wsdata;
//    if (WSAStartup(sockVersion, &wsdata) != 0)
//    {
//        return 1;
//    }
//
//    //创建套接字
//    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
//    if (serverSocket == INVALID_SOCKET)
//    {
//        cout << "Socket error" << endl;
//        return 1;
//    }
//
//
//    //绑定套接字
//    sockaddr_in sockAddr;
//    sockAddr.sin_family = AF_INET;
//    sockAddr.sin_port = htons(5566);
//    sockAddr.sin_addr.S_un.S_addr = INADDR_ANY;
//
//    if (bind(serverSocket, (sockaddr*)&sockAddr, sizeof(sockAddr)) == SOCKET_ERROR) {
//        cout << "Bind error" << endl;
//        return 1;
//    }
//
//    //开始监听
//    if (listen(serverSocket, 10) == SOCKET_ERROR) {
//        cout << "Listen error" << endl;
//        return 1;
//    }
//
//
//    SOCKET clientSocket;
//    sockaddr_in client_sin;
//    char msg[8192];//存储传送的消息
//    int flag = 0;//是否已经连接上
//    int len = sizeof(client_sin);
//    while (true) {
//        if (!flag)
//            cout << "等待连接..." << endl;
//        clientSocket = accept(serverSocket, (sockaddr*)&client_sin, &len);
//        if (clientSocket == INVALID_SOCKET) {
//            cout << "Accept error" << endl;
//            flag = 0;
//            return 1;
//        }
//        if (!flag) {
//            cout << "接收到一个链接：" << inet_ntoa(client_sin.sin_addr) << endl;
//
//
//
//            string data = { 0x4B,0x75,0x47,0x6F,0x75,LEN_DATA,0x00,0x00,0x00,LEN_DATA,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x03,0x1C,0x00,0x00 };
//
//            rc4_init(keyAry, (char*)"1593044206", strlen("1593044206"));
//            rc4_cryp(keyAry, (char*)data.c_str(), LEN_DATA);
//            //getline(cin, data);
//            const char* sendData;
//            sendData = data.c_str();
//            send(clientSocket, sendData, LEN_DATA, 0);
//        }
//        flag = 1;
//        int num = recv(clientSocket, msg, 8192, 0);
//        if (num > 0)
//        {
//            msg[num] = '\0';
//            cout << "Client say: " << msg << endl;
//
//        }
//
//        
//        closesocket(clientSocket);
//    }
//
//    closesocket(serverSocket);
//    WSACleanup();
//
//
//
//    return 0;
//}


int main()
{
    char key[10] = { 0x4D,0x6F ,0x74 ,0x68 ,0x65 ,0x72 ,0x33 ,0x36 ,0x30 ,0 };
    char keyAry[256];
    char data[1000] = { 0x31, 0x39, 0x32, 0x2E, 0x31, 0x36, 0x38, 0x2E, 0x31, 0x2E, 0x31, 0x30,0x31,0x00};
    rc4_init(keyAry, key, 10);

    rc4_cryp(keyAry, data, 14);

    rc4_init(keyAry, key, 10);
    rc4_cryp(keyAry, data, 14);
    int a = 0;
}

void rc4_init(char* keyAry, char* key, int len) {
    int  data[256] = { 0, };
    int i = 0;
    do {
        keyAry[i] = i;
        data[i] = key[i % len];
        i++;
    } while (i < 256);

    int j = 0;
    int mod = 0;
    int temp = 0;
    do {

        mod += (unsigned char)keyAry[j] + data[j];
        mod %= 256;
        temp = keyAry[j];
        //printf("%X\n", mod);
        keyAry[j] = keyAry[mod];
        keyAry[mod] = temp;
        j++;
    } while (j < 256);
}

void rc4_cryp(char* keyAry, char* data, int len) {

    unsigned int i = 0, j = 0, k = 0, temp = 0;
    if (len > 0) {
        do {
            j++;
            j = j % 256;
            temp = (unsigned char)keyAry[j];
            k += temp;
            k %= 256;
            keyAry[j] = keyAry[k];
            keyAry[k] = temp;
            data[i] = data[i] ^ keyAry[((unsigned char)keyAry[j] + temp) % 256];
            i++;
        } while (i < len);
    }
}
