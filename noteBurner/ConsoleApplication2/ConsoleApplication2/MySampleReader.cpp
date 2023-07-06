#include <iostream>
#include <iomanip>
#include "MySampleReader.h"
#include "MySampleDecrypter.h"

AP4_Result MySampleReader::ReadSampleData(AP4_Sample& sample, AP4_DataBuffer& sample_data)
{
	auto printfHex = [](char *byteArray, int length) {
		
		// 打印十六进制字符串
		for (int i = 0; i < length; ++i) {
			std::cout << std::hex << std::setw(2) << std::setfill('0')
				<< static_cast<int>(byteArray[i]);
		}

		std::cout << std::endl;
	};

	if (this->m_decrypter != nullptr) {
		AP4_Cardinal subsample_count =0;
		const AP4_UI16* bytes_of_cleartext_data;
		const AP4_UI32* bytes_of_encrypted_data;

		const AP4_UI08* iv = m_decrypter->m_table->GetIv(m_decrypter->index);
		uint32_t ivSize = m_decrypter->m_table->GetIvSize();
		int64_t timestamp = ((double)sample.GetDts() * ((double)1000000 / (double)m_decrypter->m_timeScale) + 0.5);


		m_decrypter->m_table->GetSampleInfo(m_decrypter->index, subsample_count, bytes_of_cleartext_data, bytes_of_encrypted_data);


		printf("read sample offset: 0x%llX size: 0x%X isEncrypted: true\n", sample.GetOffset(), sample.GetSize());
		printf("keyid: ");
		printfHex((char *)m_decrypter->m_key_id, m_decrypter->m_key_id_size);
		printf("iv: ");
		printfHex((char*)iv, ivSize);

		for (int i = 0; i < subsample_count; i++) {
			printf("subsample[%d] bytes_of_cleartext_data %X bytes_of_encrypted_data %X\n", i, bytes_of_cleartext_data[i], bytes_of_encrypted_data[i]);
		}
		m_decrypter->index++;
	}
	else {
		printf("read sample offset: 0x%llX size: 0x%X isEncrypted: false\n", sample.GetOffset(), sample.GetSize());
	}
	return AP4_Result();
}
