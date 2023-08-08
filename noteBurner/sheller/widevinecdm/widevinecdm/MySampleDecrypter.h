#pragma once
#include <bento4/Ap4.h>
#include "bento4/Ap4Atom.h"
#include "widevinecdm.h"
class MySampleDecrypter
{
public:
	MySampleDecrypter(const AP4_UI08* keyid, uint32_t key_id_size, AP4_CencSampleInfoTable* table, AP4_UI32 timeScale, AP4_UI08 DefaultCryptByteBlock, AP4_UI08 DefaultSkipByteBlock, EncryptionScheme protectedType) :m_key_id(keyid), \
		m_key_id_size(key_id_size), m_table(table), m_timeScale(timeScale), m_DefaultCryptByteBlock(DefaultCryptByteBlock), m_DefaultSkipByteBlock(DefaultSkipByteBlock), m_protectedType(protectedType) {

	};

	const AP4_UI08* m_key_id;
	uint32_t m_key_id_size;
	uint32_t index = 0;
	AP4_CencSampleInfoTable* m_table;
	AP4_UI32 m_timeScale;
	AP4_UI08 m_DefaultCryptByteBlock;
	AP4_UI08 m_DefaultSkipByteBlock;
	EncryptionScheme m_protectedType;
};

