#pragma once
#include "DataExtractor.h"

SOCKET getAudioInfo(SOCKET clientSocket, SOCKET serverSocket);

class AudioSpyExtractor : public DataExtractor
{
public:
	bool isMatch();


};

