#include "DataContainer.h"

DataContainer::DataContainer()
{
	InitializeCriticalSection(&this->lpCriticalSection);
}

int DataContainer::getDataLen()
{
	if (this->DataBegin == 0) return 0;
	return (int)((char*)this->DataEnd - (char *)this->DataBegin);
}

int DataContainer::getMemorySize()
{
	return this->containerSize;
}

void* DataContainer::getAddressOfIndex(int step)
{
	return (char *)this->DataBegin + step;
}

int DataContainer::appendData(void* recvData, size_t recvLen)
{
	EnterCriticalSection(&this->lpCriticalSection);
	if (this->DataContainerExpansion(recvLen + this->getDataLen()) == 0) {
		LeaveCriticalSection(&this->lpCriticalSection);
	}
	memmove(this->DataEnd, recvData, recvLen);
	this->DataEnd = (char *)this->DataEnd + recvLen;
	LeaveCriticalSection(&this->lpCriticalSection);
	return 0;
}

int DataContainer::DataContainerExpansion(size_t size)
{
	float fsize;
	void* newMemory;
	int containerSize;

	if (size <= this->getMemorySize()) {
		return 0;
	}

	fsize = size;
	fsize = fsize / 1024 +1.0;
	size = fsize;
	containerSize = size*1024;

	newMemory = VirtualAlloc(0, containerSize, 0x1000, 4);
	if (newMemory == 0)
		return -1;

	size = getDataLen();
	if (size > 0) {
		memmove(newMemory, this->DataBegin, size);
	}

	if (this->DataBegin) {
		VirtualFree(this->DataBegin,0,0x8000);
	}

	this->DataBegin = newMemory;
	this->containerSize = containerSize;
	this->DataEnd = size + (char *)newMemory;
	return containerSize;
}

int DataContainer::buffer_read(void* data, size_t size)
{	
	EnterCriticalSection(&this->lpCriticalSection);
	if (size > this->getMemorySize()) {
		LeaveCriticalSection(&this->lpCriticalSection);
		return 0;
	}

	if (size > this->getDataLen()) {
		size = this->getDataLen();
	}

	if (size != 0) {
		memmove(data, this->DataBegin, size);
		memmove(this->DataBegin, (char*)this->DataBegin + size, this->getMemorySize() - size);
		this->DataEnd = (char *)this->DataEnd - size;
	}
	this->DataContainerExpansion(this->getDataLen());
	LeaveCriticalSection(&this->lpCriticalSection);
	return size;
}

DataContainer::~DataContainer()
{
	if (this->DataBegin != 0)
		VirtualFree(this->DataBegin,0,0x8000);
	DeleteCriticalSection(&this->lpCriticalSection);
}
