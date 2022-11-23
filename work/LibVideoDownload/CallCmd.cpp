#include "CallCmd.h"
#include "Downloader.h"
#include <sstream>
#include "log.h"

string CallCmd::exePath = ".";

CallCmd::~CallCmd()
{
	if (this->process != nullptr) {
		delete this->process;
	}
}

void CallCmd::setExePath(string exepath)
{
	this->path = exepath+" ";
}

void CallCmd::stopCMD()
{
	if (this->process != nullptr) {
		this->process->kill();
		//cout << "this->process->get_exit_status();";
		this->process->get_exit_status();
		
	}
}

int CallCmd::runCMD(string Utf8str, Callback stateback)
{
//	logPrint(abs_path(this->path));
//	this->path = abs_path(this->path);  


	this->process = new Process(this->path + Utf8str,"", [=](const char* bytes, size_t n) {
			stateback(bytes);
		});
	return 1;
}
	

string CallCmd::runCMD(string Utf8str)
{
	string *res = new string();
	string rlt;
	Process process(this->path + Utf8str, "", [=](const char* bytes, size_t n) {
		*res += string(bytes, n);
		});
	 int state = process.get_exit_status();
	 
	 rlt = *res;
	 delete res;
	return rlt;
}
