#pragma once
#include <iostream>


	bool connectToServer(const std::string& serverAddress, uint16_t port);
	std::string sendMessageAndWaitForResponse(const std::string& message);
	void closeClient();
	void sendMessage(const std::string& message);


