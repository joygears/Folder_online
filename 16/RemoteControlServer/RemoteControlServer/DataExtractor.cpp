#include "DataExtractor.h"
#include "DataContainer.h"
#include "rc4crpt.h"
#include "utils.h"

int DataExtractor::decryptData(void* data, int len)
{
	DataContainer encrypteContainer;
	char keyAarry[256] = { 0, };
	int dataLen = 0;
	char* buf;

	if (len <= 0)  return -1;

	this->plainTextContainer.appendData(data, len);
	rc4_init(keyAarry, (char*)RC4_KEY, strlen(RC4_KEY));
	rc4_cryp(keyAarry, (char*)data, len < 9 ? len : 9);
	encrypteContainer.appendData(data, len);
	memmove(&dataLen, encrypteContainer.getAddressOfIndex(5), 4);
	if (memcmp((const char*)encrypteContainer.getAddressOfIndex(0), "KuGou",5) == 0) {

		if (dataLen == 0)
			return -1;
		if (encrypteContainer.getDataLen() < dataLen)
			return -1;
		rc4_init(keyAarry, (char*)RC4_KEY, strlen(RC4_KEY));
		rc4_cryp(keyAarry, (char*)this->plainTextContainer.getAddressOfIndex(0), dataLen);
	}
    return dataLen;
}

int DataExtractor::parse_data()
{	
	void* data = this->plainTextContainer.getAddressOfIndex(0);
	size_t size = this->plainTextContainer.getDataLen();
	char* pSrc = 0;
	char magic[6] = {0,};
	size_t dataLen = 0;
	int compressFlag = 0;
	do {
		if (size <= 17) return size;

		memmove(magic, data, 5);
		memmove(&size, this->plainTextContainer.getAddressOfIndex(5), 4);

		if (size == 0 || this->plainTextContainer.getDataLen() < size) return this->plainTextContainer.getDataLen();
		this->plainTextContainer.buffer_read(magic, 5);
		this->plainTextContainer.buffer_read(&size, 4);
		this->plainTextContainer.buffer_read(&dataLen, 4);
		pSrc = new char[size - 17];
		this->plainTextContainer.buffer_read(pSrc, size - 17);
		this->plainTextContainer.buffer_read(&compressFlag, 4);
		if (compressFlag == 0x2189) {
			this->parsedData.appendData(pSrc, size - 17);
		}
	} while (true);
	return 0;
}

