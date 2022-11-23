#include <thread>
#include <vector>
#include <map>
#include <filesystem>
#include <fstream>
#include <regex>
#include "json.hpp"
#include "log.h"
#include "base64.h"
#include "Downloader.h"
#include "CallCmd.h"
#include "DownloaderInformer.h"


using namespace std;
#ifdef _WIN32
#define EXE string("\"")+get_executable_dir()+"/winBin/tubepaw.exe\""
#elif defined __APPLE__
#define EXE  string("\"")+CallCmd::exePath+"/macBin/tubepaw\""
#endif

void automaticallySetParameters(char* json, CallCmd* cmd);

bool Downloader::parse(char* json, STATECALLBACK* callback)
{
	
	string jsonStr = json;
		string encodedJson;
		logPrint(((DownloaderInformer*)informer)->guid << " : " << "--------------------- run tubepaw ----------------------------");
		encodedJson = base64_encode(jsonStr);
		logPrint(((DownloaderInformer*)informer)->guid << " : " << "input json >> " << jsonStr);
		 (*(CallCmd*)this->cmd).setExePath(EXE);

		#ifdef _WIN32
		#elif defined __APPLE__
		automaticallySetParameters(json, (CallCmd*)cmd);
		#endif
		
		(*(CallCmd*)this->cmd).runCMD(encodedJson, [=](const char* bytes) {
			//callback->stateInform((char*)bytes);
			((DownloaderInformer*)informer)->inform(callback, (char *)bytes);
			});

	//free(json_bak);

	return true;
}

bool Downloader::download(char* json, STATECALLBACK* callback)
{	//获取save_path
	((DownloaderInformer*)informer)->save_path = getSavePath(json);
	 parse(json, callback);

	//string jsonStr = json;
	//string encodedJson;
	//jsonStr = ((DownloaderInformer*)this->informer)->addIe_result(jsonStr);
	////encodedJson = base64_encode(jsonStr);

	////创建download.json并放入save_path
	// savePath = createDownloadJson(jsonStr, savePath);

	//logPrint(guid << " : "<< "cmd.SetExePath(_T(EXE));");
	//(*(CallCmd*)this->cmd).setExePath(EXE);
	//logPrint(guid << " : "<< "cmd.RunCMD");
	//(*(CallCmd*)this->cmd).runCMD(savePath, [=](const char* bytes) {
	//	//callback->stateInform((char*)bytes);
	//	((DownloaderInformer*)informer)->inform(callback, (char*)bytes);
	//	});
	return true;
}


bool Downloader::stop(STATECALLBACK* callBack)
{
	
	if (callBack != NULL) {


		thread threadObj([=]() {

			string state = R"({ "type":"stop","msg":{"ret":0}})";
			(*(CallCmd*)this->cmd).stopCMD();

			callBack->stateInform((char*)state.c_str());

			});
		threadObj.detach();
	}
	else {
		(*(CallCmd*)this->cmd).stopCMD();
	}
	return true;
}

Downloader::Downloader()
{
	logPrint("!!!!!!!!!!!!!!!!!!! will getGuid !!!!!!!!!!!!!!!!!!!!!!!!!");
	std::string guid = getGuid();
	logPrint(guid << " : "<< "-------------------------- create Downloader ------------------------------");
	logPrint(guid << " : "<< "current Version : " << getVideoDownloadVersion());
	cmd = new CallCmd();
	((CallCmd*)cmd)->guid = guid;
	informer = new DownloaderInformer();
	((DownloaderInformer*)informer)->guid = guid;
}

Downloader::~Downloader()
{
	
	this->stop(nullptr);
	logPrint(((DownloaderInformer*)informer)->guid << " : " << "-------------------------- destroy Downloader ------------------------------");
	delete (CallCmd*)this->cmd;
	delete (DownloaderInformer *)informer;
	//MessageBoxA(0, "delete object", "", 0);
}




int startsWith(string s, string sub) {
	return s.find(sub) == 0 ? 1 : 0;
}

bool  isYoutube(string url) {
	bool bl = 1;
	string::size_type pos = string::npos;
	if (!startsWith(url, "https://www.youtube.com")) {
		pos = url.find("music.youtube.com/", 0);
		if (pos == string::npos) {
			pos = url.find("https://m.youtube.com/", 0);
			if (pos == string::npos) {
				if (!startsWith(url, "https://youtube.com/")) {
					if (!startsWith(url, "https://youtu.be/")) {
						bl = 0;
					}
				}
			}
		}
	}
	return bl;
}

bool  isContainListKey(string url, vector<string> keys) {
	bool ret = 0;
	for (string key : keys) {
		if (url.find(key, 0) != string::npos) {
			ret = 1;
			break;
		}
	}
	return ret;
}
bool isTargetWebsite(string url, string rex) {
	bool bl = 0;
	string::size_type pos = string::npos;
	pos = url.find(rex, 0);
	if (pos != string::npos) {
		pos = url.find("http://", 0);
		if (pos == string::npos) {
			pos = url.find("https://", 0);
			if (pos != string::npos) {
				bl = 1;
			}
			else {
				bl = 0;
			}
		}
		else {
			bl = 1;
		}

	}
	else {
		bl = 0;
	}
	return bl;
}
//************************************
// Method:    isPlaylist
// FullName:  isPlaylist
// Access:    public 
// Returns:   bool
// Qualifier:  判断一个url是否是视频列表
// Parameter: char * url
//************************************
bool Downloader::checkPlaylist(const char* url) {

	string::size_type pos = string::npos;
	bool bl = 0;

	if (isYoutube(url)) {
		if (isContainListKey(url, { "list", "/channel/", "/user/","/c/","/results?search_query="})) {
			return true;
		}
	}
	map<string, vector<string>> websites = {
			{"spotify.com",{ "/playlist/", "/artist/", "/album/" }},
			{"soundcloud.com",{ "/sets/", "/playlists/" }},
			{"bandcamp.com",{ "/album/" }},
			{"gaana.com",{ "/album/", "/artist/", "/playlist/" }},
			{"audiomack.com",{ "/album/", "/playlist/" }},
	};

	for (auto iter = websites.begin(); iter != websites.end(); iter++) {
		if (isTargetWebsite(url, iter->first)) {
			if (isContainListKey(url, iter->second)) {
				return true;
			}
		}
	}
	return false;
}
//************************************
// Method:    checkFullPlaylist
// FullName:  Downloader::checkFullPlaylist
// Access:    public static 
// Returns:   bool
// Qualifier: 判断一个url是否是纯视频列表
// Parameter: const char * url
//************************************
bool Downloader::checkFullPlaylist(const char* url) {

	string::size_type pos = string::npos;
	bool bl = 0;


	if (isYoutube(url)) {
		if (isContainListKey(url, { "/channel/", "/user/","/c/","/results?search_query=" })) {

			return true;
		}
		if (isContainListKey(url, { "list" }) && !isContainListKey(url, { "/watch?v=" }))
			return true;
	}
	map<string, vector<string>> websites = {
			{"spotify.com",{ "/playlist/", "/artist/", "/album/" }},
			{"soundcloud.com",{ "/sets/", "/playlists/" }},
			{"bandcamp.com",{ "/album/" }},
			{"gaana.com",{ "/album/", "/artist/", "/playlist/" }},
			{"audiomack.com",{ "/album/", "/playlist/" }},
	};

	for (auto iter = websites.begin(); iter != websites.end(); iter++) {
		if (isTargetWebsite(url, iter->first)) {
			if (isContainListKey(url, iter->second)) {
				return true;
			}
		}
	}
	return false;
}

UrlType Downloader::getUrlType(const char* url)
{
	string strUrl = stripBlank(url);

	if (checkPlaylist(strUrl.c_str())) {
		if (checkFullPlaylist(strUrl.c_str()))
		{
			return UrlType::FULL;
		}
		return UrlType::PART;
	}
	return UrlType::SINGLE;
}


void Downloader::getVersion(char* szVersion)
{
	std::string rlt = "";
#ifdef _WIN32
	ifstream outfile;
	outfile.open("./winBin/version", ios::app);
	outfile >> rlt;
	outfile.close();
	std::memcpy(szVersion, rlt.c_str(), rlt.length()+1);
	std::string fname = szVersion;
	std::regex base_regex(R"(\d+.\d+.\d+)");
	std::smatch base_match;
	if (regex_match(fname, base_match, base_regex)) {
		return;
	}
#endif 
	CallCmd cmd;
	cmd.setExePath(EXE);
	
	rlt = cmd.runCMD("");
	rlt.erase(std::remove(rlt.begin(), rlt.end(), '\r'), rlt.end());
	rlt.erase(std::remove(rlt.begin(), rlt.end(), '\n'), rlt.end());
	std::memcpy(szVersion, rlt.c_str(), rlt.length()+1);

	
}

void Downloader::setLogPath(char* logPath)
{
//	string filepath = logPath;
//	filepath += "/";
//	filepath += LOG_NAME;
	Log::setFilename(logPath);
}

void Downloader::setexePath(char* exePath)
{
	CallCmd::exePath = exePath;
}


void automaticallySetParameters(char *json, CallCmd* cmd){
	
	string log_path;
	string executable;
	
		if (IsJsonData(json)) {
			auto jsonrlt = nlohmann::json::parse(json);
			if (jsonrlt.find("log_path") != jsonrlt.end()) {
				 log_path = jsonrlt["log_path"].get<string>();
				 Downloader::setLogPath((char *)log_path.c_str());
			}
			if (jsonrlt.find("ffmpeg_location") != jsonrlt.end()) {
				executable = jsonrlt["ffmpeg_location"].get<string>();
				executable += "tubepaw";
                executable.insert(0,"\"");
                executable += "\"";
				cmd->setExePath((char *)executable.c_str());
			}
		}
}
