#include "DownloaderInformer.h"
#include <sstream>
#include <fstream>
#include <regex>
#include "json.hpp"
#include "Log.h"
#include "Downloader.h"
#include "utils.h"
#ifdef _WIN32
#include <Windows.h>
#endif
#include <iostream>

bool IsJsonData(std::string strData)
{
	try
	{ 
	auto jsonrlt = nlohmann::json::parse(strData);
	}
	catch (std::exception& e)
	{
		return false;

	}
	/*if (strData[0] != '{')
		return false;

	int num = 1;
	for (int i = 1; i < strData.length(); ++i)
	{
		if (strData[i] == '{')
		{
			++num;
		}
		else if (strData[i] == '}')
		{
			--num;
		}

		if (num == 0)
		{
			return true;
		}
	}*/

	return true;
}

int stateInform_s(void* memory_pointer, char* json)
{
	if (NULL == memory_pointer) {
		return 0;
	}


	if (IsJsonData(json))
	((STATECALLBACK*)memory_pointer)->stateInform(json);
	return 1;



}





DownloaderInformer::~DownloaderInformer()
{
//	std::string filename = this->save_path + "/download.json";
//	std::ifstream f(filename);
//	bool exist = f.good();
//	f.close();
//	if (exist) {
//		
//		int ret =remove(filename.c_str());
//#ifdef _WIN32
//        std::cout << ret << " " <<GetLastError()<< std::endl;
//#endif
//	}
	
}

void DownloaderInformer::inform(STATECALLBACK* callBack, char* json)
{
	logPrint(guid << " : "<< json);
	stateInform_s(callBack, json);
	/*logPrint(guid << " : "<< "开始通知");
	filterPredownloaded(json);
	if (!processMessage(json) && !processParsingResult(json))
		stateInform_s(callBack,json);
	logPrint(json);
	if (filterSpeed(json)) {
		logPrint(guid << " : "<< "filterOptionalInformation(json);");
		filterOptionalInformation(json);
		std::string stateJson = this->createdownloadingJson();
		stateInform_s(callBack, json);
	}
	if (filterConverting(json)) {
		logPrint(guid << " : "<< "filterConverting");
		std::string stateJson = this->createconvertingJson();
		stateInform_s(callBack, json);
	}
	logPrint(guid << " : "<< "通知结束");*/
}

bool DownloaderInformer::processMessage(char* json)
{
	if (IsJsonData(json)) {
		auto jsonrlt = nlohmann::json::parse(json);
		if (jsonrlt.find("type") != jsonrlt.end() && jsonrlt["type"].get<std::string>() == "message") {
			auto msg = jsonrlt["msg"];
			if (msg.find("totalSize") != msg.end() && msg.find("filecount") != msg.end() && msg.find("downloadedSize") != msg.end()) {
				this->totalSize = msg["totalSize"].get<unsigned long long>();
				this->filecount = msg["filecount"].get<unsigned short>();
				this->downloadedSize = msg["downloadedSize"].get<unsigned long long>();
				return true;
			}
		}
	}
	return false;
}
bool DownloaderInformer::processParsingResult(char* json)
{
	if (IsJsonData(json)) {
		auto jsonrlt = nlohmann::json::parse(json);
		if (jsonrlt.find("type") != jsonrlt.end() && jsonrlt["type"].get<std::string>() == "parsingResult") {
			auto msg = jsonrlt["msg"];
			if (msg.find("ie_result") != msg.end()) {
				this->ie_result =msg["ie_result"].dump();
				return true;
			}
		}
	} 
	return false;
}
std::string DownloaderInformer::addIe_result(std::string json)
{
	if (IsJsonData(json) && this->ie_result!="") {
		auto jsonrlt = nlohmann::json::parse(json);
		if (jsonrlt.find("downloader") != jsonrlt.end()) {
			auto downloader = jsonrlt["downloader"];
			jsonrlt["downloader"]["ie_result"] = nlohmann::json::parse(this->ie_result);
		}
		json = jsonrlt.dump();
	}
	return json;
}




bool DownloaderInformer::filterSpeed(char* json)
{
	std::string unit = "";
	float speed = 0;
	std::string fname = json;
	std::regex base_regex(R"(.+DL:([0-9]+\.?[0-9]*)([a-zA-Z]+).+)");
	std::smatch base_match;
	if (std::regex_match(fname, base_match, base_regex)) {
		// std::smatch 的第一个元素匹配整个字符串
		// std::smatch 的第二个元素匹配了第一个括号表达式
		if (base_match.size() > 2) {
			std::string base = base_match[1].str();
			//std::cout << "sub-match[0]: " << base_match[0].str() << std::endl;
			speed = std::stof(base);
			unit = base_match[2];
			this->speed = speedUnitConvertBytes(speed, unit);
			if (this->speed == 0)
				return false;
			this->downloadedSize += this->speed;

			return true;
		}
	}
	return false;
}

void DownloaderInformer::filterOptionalInformation(char* json)
{
	std::string unit = "";
	double downloadedSize = 0;
	double totalSize = 0;
	std::string fname = json;
	std::regex base_regex(R"(.+ ([0-9]+\.?[0-9]*)([a-zA-Z]+)/([0-9]+\.?[0-9]*)([a-zA-Z]+).[0-9]+\.?[0-9]*%. .+ DL:[0-9]+\.?[0-9]*[a-zA-Z]+.+)");
	std::smatch base_match;
	if (std::regex_match(fname, base_match, base_regex)) {
		// std::smatch 的第一个元素匹配整个字符串
		// std::smatch 的第二个元素匹配了第一个括号表达式
		if (base_match.size() > 0) {
			std::string base = base_match[1].str();
			/*std::cout << "sub-match[0]: " << base_match[0].str() << std::endl;
			std::cout << "sub-match[1]: " << base_match[1].str() << std::endl;*/
			downloadedSize = std::stod(base);
			unit = base_match[2];
			totalSize = std::stod(base_match[3]);
			this->downloadedSize = speedUnitConvertBytes(downloadedSize, unit) + this->predownloadedSize;
			if (this->filecount == 1) {
				unit = base_match[4];
				this->totalSize = speedUnitConvertBytes(totalSize, unit);
			}
			return;
		}
	}
}

std::string DownloaderInformer::createdownloadingJson()
{
	if (this->downloadedSize > this->totalSize) {
		this->totalSize += (downloadedSize - totalSize + 5760);
	}
	this->progress = (this->downloadedSize * 1.0 / this->totalSize);
	std::string process = std::to_string(this->progress);
	std::string speed = bytesConvertSpeedUnit(this->speed);
	nlohmann::json root, msg;
	root["type"] = "downloading";
	msg["filesize"] = this->totalSize;
	msg["progress"] = process;
	msg["speed"] = speed;
	root["msg"] = msg;

	return root.dump();
}
std::string DownloaderInformer::createconvertingJson()
{
	nlohmann::json root, msg;
	root["type"] = "converting";
	msg["ret_code"] = "1";
	root["msg"] = msg;
	return root.dump();
}

void DownloaderInformer::filterPredownloaded(char* json)
{
	std::string unit = "";
	double downloadedSize = 0;
	double totalSize = 0;
	std::string fname = json;
	std::regex base_regex(R"(.+.download.\s+100% of ([0-9]+\.?[0-9]*)([a-zA-Z]+).*)");
	std::smatch base_match;
	if (std::regex_match(fname, base_match, base_regex)) {
		// std::smatch 的第一个元素匹配整个字符串
		// std::smatch 的第二个元素匹配了第一个括号表达式
		if (base_match.size() > 0) {
			std::string base = base_match[1].str();
			/*std::cout << "sub-match[0]: " << base_match[0].str() << std::endl;
			std::cout << "sub-match[1]: " << base_match[1].str() << std::endl;*/
			downloadedSize = std::stod(base);
			unit = base_match[2];
			this->predownloadedSize = speedUnitConvertBytes(downloadedSize, unit);
			return;
		}
	}

}
bool DownloaderInformer::filterConverting(char* json) {
	std::string fname = json;
	std::regex base_regex(R"(.+\[ExtractAudio\].+)");
	std::smatch base_match;
	if (std::regex_match(fname, base_match, base_regex)) {
		return true;
	}
	return false;
}

unsigned long long DownloaderInformer::speedUnitConvertBytes(double speed, std::string unit)
{
	unsigned short  count = 0;
	if (unit == "B" || unit == "b") {
		count = 0;
	}
	else if (unit == "KiB") {
		count = 1;
	}
	else if (unit == "MiB") {
		count = 2;
	}
	else if (unit == "GiB" || unit == "GB") {
		count = 3;
	}
	else if (unit == "TiB" || unit == "TB") {
		count = 4;
	}

	for (int i = 0; i < count; i++) {
		speed *= 1024;
	}
	return (unsigned long long)speed;
}

std::string DownloaderInformer::bytesConvertSpeedUnit(unsigned int speed)
{
	int count = 0;
	float fullSpeed = speed;
	std::string unit = "";
	while (fullSpeed >= 1024) {
		fullSpeed /= 1024;
		count++;
	}
	if (count == 0) {
		unit = "B/s";
	}
	else if (count == 1) {
		unit = "KB/s";
	}
	else if (count == 2) {
		unit = "MB/s";
	}
	std::stringstream buf;
	buf.precision(2);
	buf.setf(std::ios::fixed);//保留小数位
	buf << fullSpeed << unit;
	return buf.str();
}
