#pragma once
#include <iosfwd>
#include <sstream>
#include <fstream>
#include "utils.h"
#include "json.hpp"
#include "log.h"

#ifdef _WIN32
#include <Rpc.h>
#else
#include <uuid/uuid.h>
#endif
#pragma comment(lib,"rpcrt4.lib")


using namespace std;
std::vector<std::string>& split(const std::string& str, char delim, std::vector<std::string>& tokens) {
	
	std::string::size_type pos = 0;
	std::string::size_type prev = 0;
	string last;
	while ((pos = str.find('\n', prev)) != std::string::npos) {
		tokens.push_back(str.substr(prev, pos - prev+1));
		prev = pos + 1;
	}
	last = str.substr(prev);
	if(last != "")
	tokens.push_back(last);

	return tokens;
}
string abs_path(string path)
{
#ifdef _WIN32
#define max_path 4096
	char resolved_path[max_path] = { 0 };
	_fullpath(resolved_path, path.c_str(), max_path);
#else
	//linux release有个坑，需要大点的空间
#define max_path 4096
	char resolved_path[max_path] = { 0 };
	realpath(path.c_str(), resolved_path);
#endif
	return string(resolved_path);
}
string getSavePath(string jsonstr) {
	
		auto jsonrlt = nlohmann::json::parse(jsonstr);
		if (jsonrlt.find("downloader") != jsonrlt.end() ) {
			auto downloader = jsonrlt["downloader"];
			if (downloader.find("save_path") != downloader.end()) {
				return downloader["save_path"].get<string>();
			}
		}
		//logPrint(guid << " : "<< "get save_path failed. please check your json");

	return "";
}

string createDownloadJson(string jsonstr,string dir) {
	string savePath = dir + "/download.json";
	ofstream outfile;
	outfile.open(savePath, ios::out);
	outfile << jsonstr << endl;
	outfile.close();
	return savePath;
}



std::string getGuid()
{
#ifdef _WIN32
    UUID uuid;
    UuidCreate ( &uuid );

    unsigned char * str;
    UuidToStringA ( &uuid, &str );

    std::string s( ( char* ) str );

    RpcStringFreeA ( &str );
#else
    uuid_t uuid;
    uuid_generate_random ( uuid );
    char s[37];
    uuid_unparse ( uuid, s );
#endif
    return s;
}

std::string stripBlank(std::string str) {
	string blanks("\f\v\r\t\n ");
	str.erase(0, str.find_first_not_of(blanks));
	str.erase(str.find_last_not_of(blanks) + 1);
	return str;
}