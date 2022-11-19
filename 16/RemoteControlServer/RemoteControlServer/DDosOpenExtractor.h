#pragma once
#include "DataExtractor.h"

SOCKET getDDosOpenInfo(SOCKET clientSocket, SOCKET serverSocket);
class DDosOpenExtractor :
    public DataExtractor
{
public:
    bool isMatch();
};

