#include <iostream>
#include <chrono>
#include "json.hpp"
#include "CallCmd.h"
#include "Downloader.h"

using namespace std;
bool stoped = 0;
Downloader* download;
class StateCallBack :public STATECALLBACK {
public:
	virtual void  stateInform(char* json);
};
void StateCallBack::stateInform(char* json) {
	std::cout << json << endl;
	try {
		auto jsonrlt = nlohmann::json::parse(json);
		if (jsonrlt.find("type") != jsonrlt.end() && jsonrlt["type"].get<std::string>() == "stop") {
			stoped = 1;
			int b = 1;
		}
		if (jsonrlt.find("type") != jsonrlt.end() && jsonrlt["type"].get<std::string>() == "finished") {
			//	delete download;
		}
	}
	catch (std::exception e) {

	}
	/*cout << json << endl;
	Json::Reader reader;
	Json::Value value;
	if (reader.parse(json, value)) {

		if(value["type"].asString()=="stop")stoped = 1;
		int b = 1;
	}*/

}

int main()
{

	Downloader::setLogPath((char*)"/Users/czl/Library/Application Support/HitPaw Software/HitPawVideoConverter/logs");
//    Downloader::setexePath("/Users/czl/Desktop/script/Hitpaw fast commit/hitPaw-middleware/build/mac/Debug");
	char  version[1024] = { 0, };
	Downloader::getVersion(version);
    
	std::cout << version;
	int n = 1;
	for (int i = 0; i < n; i++) {
		download = new Downloader();
		StateCallBack* callback = new StateCallBack();
		//readFileJson(R"(D:\Users\Desktop\VideoPlugin\VideoPluginLibrary\LibVideoDownload\Debug\winBin\download.json)");
	   //string json = readFileJson(R"(C:\Users\Administrator\Desktop\VideoPlugin\VideoPluginLibrary\LibVideoDownload\Debug\winBin\extratUrl.json)");
		//string json = 
#ifdef _WIN32
		const char* json = R"""({
   "downloader":{
      "add_playlist_index":"false",
      "read_cookie":"false",
      "save_id3":"true",
      "save_path":"./videos",
      "subtitle":"zh-Hans",
	"sniff_only": "true",
      "url": "https://www.youtube.com/watch?v=GwB3GdPARlw"
   },
   "ffmpeg_location":"./winBin/"
}
)""";
	const char* json2 = R"""({
   "downloader":{
      "add_playlist_index":"false",
      "read_cookie":"false",
      "save_id3":"true",
      "save_path":"./videos",
      "subtitle":"zh-Hans",
	"sniff_only": "false",
      "url": "https://www.youtube.com/watch?v=GwB3GdPARlw"
   },
   "ffmpeg_location":"./winBin/"
}
)""";
#elif defined __APPLE__
        const char* json = R"""({
   "downloader":{
      "add_playlist_index":"false",
      "read_cookie":"false",
      "save_id3":"true",
      "save_path":"./videos",
      "subtitle":"zh-Hans",
    "sniff_only": "true",
      "url": "https://www.youtube.com/watch?v=GwB3GdPARlw"
   },
   "ffmpeg_location":"./macBin/"
}
)""";
    const char* json2 = R"""({
   "downloader":{
      "add_playlist_index":"false",
      "read_cookie":"false",
      "save_id3":"true",
      "save_path":"./videos",
      "subtitle":"zh-Hans",
    "sniff_only": "false",
      "url": "https://www.youtube.com/watch?v=GwB3GdPARlw"
   },
   "ffmpeg_location":"./macBin/"
}
)""";
#endif

		/*download->stop(callback);
		while (true)
		if (stoped == 1) {
			break;
		}
		stoped = 0;*/


		std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();
	
	

		download->parse((char*)json, callback);
		std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();
		std::chrono::duration<double> time_used = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1);
		std::cout << ".******************solve time cost = " << time_used.count() << " seconds. " << std::endl;
      /*  int temp;
        scanf("%d",&temp);*/
		//std::this_thread::sleep_for(std::chrono::microseconds(10));
        getchar();
		download->stop(callback);
		while (true)
			if (stoped == 1) {
				break;
			}
		stoped = 0;
		t1 = std::chrono::steady_clock::now();
		download->download((char*)json2, callback);
		t2 = std::chrono::steady_clock::now();
		time_used = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1);
		std::cout << ".******************solve time cost = " << time_used.count() << " seconds. " << std::endl;
		getchar();
       /* scanf("%d",&temp);*/
		//download->stop(0);
		//download->stop(callback);
		/*while(true)
		if (stoped == 1) {
			delete callback;
			delete download;
			break;
		}*/

		/*download->stop(callback);
		while (true)
			if (stoped == 1) {
				break;
			}
		stoped = 0;*/
		
		delete download;
		delete callback;
		stoped = 0;
		std::cout << i + 1 << endl;
	}
	//getchar();
    return 0;
}

//#include <iostream>
//#include "json.hpp"
//#include "CallCmd.h"
//#include "Downloader.h"
//
//using namespace std;
//bool stoped = 0;
//Downloader* download;
//class StateCallBack :public STATECALLBACK {
//public:
//	virtual void  stateInform(char* json);
//};
//void StateCallBack::stateInform(char* json) {
//	cout << json << endl;
//	try {
//		auto jsonrlt = nlohmann::json::parse(json);
//		if (jsonrlt.find("type") != jsonrlt.end() && jsonrlt["type"].get<std::string>() == "stop") {
//			stoped = 1;
//			int b = 1;
//		}
//		if (jsonrlt.find("type") != jsonrlt.end() && jsonrlt["type"].get<std::string>() == "finished") {
//			//	delete download;
//		}
//	}
//	catch (std::exception e) {
//
//	}
//	/*cout << json << endl;
//	Json::Reader reader;
//	Json::Value value;
//	if (reader.parse(json, value)) {
//
//		if(value["type"].asString()=="stop")stoped = 1;
//		int b = 1;
//	}*/
//
//}

//int main()
//{
//
//	/*char  version[1024] = { 0, };
//	Downloader::getVersion(version);
//	cout << version;*/
//	const int n = 1;
//	;
//	Downloader* downloaders[n] = { 0 };
//	StateCallBack* callbacks[n] = { 0 };
//	for (int i = 0; i < n; i++) {
//		downloaders[i] = new Downloader();
//		callbacks[i] = new StateCallBack();
//
//	}
//	const char* json = R"""({
//   "downloader":{
//      
//      "save_path":"./videos",
//      "subtitle":"zh-Hans",
//	"sniff_only": "true",
//      "url": "https://www.youtube.com/watch?v=GwB3GdPARlw"
//   },
//   "ffmpeg_location":"./macBin/"
//}
//)""";
//	for (int i = 0; i < n; i++) {
//
//		downloaders[i]->parse((char*)json, callbacks[i]);
//	}
//	//std::this_thread::sleep_for(std::chrono::milliseconds(500));
//	getchar();
//	for (int i = 0; i < n; i++) {
//
//
//		delete downloaders[i];
//		delete callbacks[i];
//		cout << "stop successful" << endl;
//	}
//	for (int i = 0; i < n; i++) {
//
//
//		delete downloaders[i];
//		delete callbacks[i];
//		cout << "stop successful" << endl;
//	}
//	//getchar();
//
//	//for (int i = 0; i < n; i++) {
//	//	downloaders[i] = new Downloader();
//	//	callbacks[i] = new StateCallBack();
//
//	//}
//	//for (int i = 0; i < n; i++) {
//
//	//	downloaders[i]->parse((char*)json, callbacks[i]);
//	//}
//	//for (int i = 0; i < n; i++) {
//
//
//	//	delete downloaders[i];
//	//	delete callbacks[i];
//	//	cout << "stop successful" << endl;
//	//}
//
//}
