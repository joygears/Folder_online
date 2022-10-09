#include <winsock2.h>
#include<iostream>
#include<string>
using namespace std;
#pragma comment(lib, "ws2_32.lib")

int main()
{
    WSAData wsaData;
    sockaddr saddr = {0,};
    int optBuf;

    WSAStartup(0x202, &wsaData);
    SOCKET soc = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (soc == 0)
        return 0;
    hostent* hent = gethostbyname("127.0.0.1");
    if (hent == 0)
        return 0;

    saddr.sa_family = 2;
    saddr.sa_data[0] = htons(5566);
    saddr.sa_data[2] = hent->h_addr_list[0][0];
    if (connect(soc, &saddr, 16) == -1) {
        return 0;
    }
    if (setsockopt(soc, SOL_SOCKET, SO_KEEPALIVE, (const char*)&optBuf, 4)) {
        WSAIoctl(soc, SIO_KEEPALIVE_VALS, &vInBuffer, 12, 0, 0, &optBuf, 0, 0);
    
    }
    return 0;
}