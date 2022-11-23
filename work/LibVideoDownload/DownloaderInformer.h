#pragma once
#include <string>



class STATECALLBACK;
class DownloaderInformer {

public:
	
	~DownloaderInformer();
	void inform(STATECALLBACK* callBack, char* json);
	std::string addIe_result(std::string json);
private:
	bool processMessage(char* json);
	bool processParsingResult(char* json);
	bool filterSpeed(char* json);
	void filterOptionalInformation(char* json);
	std::string createdownloadingJson();
	std::string createconvertingJson();

	void filterPredownloaded(char* json);
	bool filterConverting(char* json);
public:
	static unsigned long long speedUnitConvertBytes(double speed, std::string unit);
	static std::string bytesConvertSpeedUnit(unsigned int speed);
public :
	std::string save_path = "";
	std::string guid = "";
private:
	unsigned long long totalSize = 1;
	unsigned long long downloadedSize = 0;
	unsigned int speed = 0;
	unsigned short filecount = 1;
	float progress = 0.0;
	unsigned long long predownloadedSize = 0;
	std::string ie_result ="";
	
};

bool IsJsonData(std::string strData);