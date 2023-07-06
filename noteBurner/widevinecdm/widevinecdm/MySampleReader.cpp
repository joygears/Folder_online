#include <iostream>
#include <iomanip>
#include "MySampleReader.h"
#include "MySampleDecrypter.h"
#include "widevinecdm.h"
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


       
        char* key_id = (char *)m_decrypter->m_key_id;
      

        SubsampleEntry* subsamples = new SubsampleEntry[subsample_count];
        for (int i = 0; i < subsample_count; i++) {
            subsamples[i].clear_bytes = bytes_of_cleartext_data[i];
            subsamples[i].cipher_bytes = bytes_of_encrypted_data[i];
        }

       

        InputBuffer_2 input;
        input.data = (uint8_t*)sample_data.GetData();
        input.data_size = sample_data.GetDataSize();
        input.encryption_scheme = EncryptionScheme::kCenc;
        input.key_id = (uint8_t*)key_id;
        input.key_id_size = 0x10;
        input.iv = iv;
        input.iv_size = ivSize;
        input.subsamples = subsamples;
        input.num_subsamples = subsample_count;
        input.pattern.crypt_byte_block = 0;
        input.pattern.skip_byte_block = 0;
        input.timestamp = timestamp;
        MyVideoFrame videoFrame;
        MyVideoFrame* video_frame = &videoFrame;
        int result = proxy->DecryptAndDecodeFrame(&input, &videoFrame);
        printf("DecryptAndDecodeFrame result %d", result);
        cout << "width * height:" << videoFrame.SSize().width << "*" << videoFrame.SSize().height << endl;
        cout << "videoFrame.m_format : " << videoFrame.Format() << endl;
        cout << "Timestamp : " << videoFrame.Timestamp() << endl;
        for (int i = 0; i < VideoFrame::VideoPlane::kMaxPlanes; i++) {
            cout << "videoFrame.PlaneOffset((VideoFrame::VideoPlane)" << i << ")" << videoFrame.PlaneOffset((VideoFrame::VideoPlane)i) << endl;
            cout << "videoFrame.Stride((VideoFrame::VideoPlane)" << i << ")" << videoFrame.Stride((VideoFrame::VideoPlane)i) << endl;
        }
        FILE* pVideo;
        pVideo = fopen("frame.yuv", "ab");
        unsigned char* buffer = NULL;
        transtoYUV(video_frame, buffer);
        fwrite(buffer, 1, video_frame->SSize().width * video_frame->SSize().height * 1.5, pVideo);
        fclose(pVideo);



	}
	else {
		printf("read sample offset: 0x%llX size: 0x%X isEncrypted: false\n", sample.GetOffset(), sample.GetSize());
	}
	return AP4_Result();
}
