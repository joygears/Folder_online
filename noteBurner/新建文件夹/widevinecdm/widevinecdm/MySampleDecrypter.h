#pragma once
#include <bento4/Ap4.h>
#include "bento4/Ap4Atom.h"
class MySampleDecrypter
{
public:
	MySampleDecrypter(const AP4_UI08* keyid, uint32_t key_id_size, AP4_CencSampleInfoTable* table, AP4_UI32 timeScale) :m_key_id(keyid), m_key_id_size(key_id_size), m_table(table), m_timeScale(timeScale) {
	
	};

	const AP4_UI08* m_key_id;
	uint32_t m_key_id_size;
	uint32_t index = 0;
	AP4_CencSampleInfoTable* m_table;
	AP4_UI32 m_timeScale;
};

