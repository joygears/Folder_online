#include <winsock2.h>
#include<iostream>
#include<string>
using namespace std;
#pragma comment(lib, "ws2_32.lib")
#define SIO_KEEPALIVE_VALS 0x98000004
int main()
{
    WSAData wsaData;
    sockaddr saddr = {0,};
    int optBuf;
    int vInBuffer[3] = { 0, };

    WSAStartup(0x202, &wsaData);
    SOCKET soc = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (soc == 0)
        return 0;
    hostent* hent = gethostbyname("127.0.0.1");
    if (hent == 0)
        return 0;
    short port = htons(5566);
    saddr.sa_family = 2;
    memcpy(saddr.sa_data, &port, 2);
    memcpy(&saddr.sa_data[2], &hent->h_addr_list[0][0], 4);
  
    if (connect(soc, &saddr, 16) == -1) {
        return 0;
    }
    if (!setsockopt(soc, SOL_SOCKET, SO_KEEPALIVE, (const char*)&optBuf, 4)) {
        vInBuffer[0] = 1;
        vInBuffer[1] = 0x0EA60;
        vInBuffer[2] = 0x1388;
        WSAIoctl(soc, SIO_KEEPALIVE_VALS, vInBuffer, 12, 0, 0, (LPDWORD)&optBuf, 0, 0);
        
    }
    int a = GetLastError();
    return 0;
}