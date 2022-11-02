#pragma once
#include <Windows.h>
class DataContainer
{
public:
	DataContainer();
	int getDataLen();
	int getMemorySize();
	void* getAddressOfIndex(int step);
	int appendData(void* recvData, size_t recvLen);
	int  DataContainerExpansion(size_t size);
	int buffer_read(void* data, size_t size);
	virtual ~DataContainer();
private:
	void* DataBegin = 0;
	void* DataEnd = 0;
	int containerSize = 0;
	CRITICAL_SECTION  lpCriticalSection;
};

