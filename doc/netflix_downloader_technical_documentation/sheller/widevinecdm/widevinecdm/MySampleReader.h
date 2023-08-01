#pragma once
#include <bento4/Ap4.h>
#include "bento4/Ap4Atom.h"

class MySampleDecrypter;

class MySampleReader:public AP4_LinearReader::SampleReader
{
public:
	MySampleReader(MySampleDecrypter* decrypter):m_decrypter(decrypter){
	
	
	}
	virtual ~MySampleReader() {}
	virtual AP4_Result ReadSampleData(AP4_Sample& sample, AP4_DataBuffer& sample_data);

	MySampleDecrypter* m_decrypter;
};

