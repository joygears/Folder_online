#pragma once
#include "DataContainer.h"


class DataExtractor
{
public:
	int decryptData(void* data, int len);
	int parse_data();
public :
	DataContainer plainTextContainer;
	DataContainer parsedData;
};

