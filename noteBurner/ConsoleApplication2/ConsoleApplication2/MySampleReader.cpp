#include <iostream>
#include <iomanip>
#include "MySampleReader.h"
#include "MySampleDecrypter.h"
using namespace std;
extern "C"
{
#include <libavcodec\avcodec.h>
#include <libavformat\avformat.h>
#include <libswscale\swscale.h>
#include <libavutil\pixfmt.h>
#include <libavutil\imgutils.h>
};
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
	int dataSize = sample.GetSize();
	char* data = new char[dataSize + 1];
	memset(data, 0, dataSize + 1);
	sample.GetDataStream()->Seek(sample.GetOffset());
	sample.GetDataStream()->Read(data, dataSize);
	

	

	
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
		const AVCodec*  codec = avcodec_find_decoder(AV_CODEC_ID_VP9);
		AVCodecContext* codecContext;
		codecContext = avcodec_alloc_context3(codec);
		AVFrame* frame;
		frame = av_frame_alloc();
		AVPacket* packet = av_packet_alloc();

		packet->data = (uint8_t*)data;
		packet->size = dataSize;
		packet->duration = 0xa2c3;
		int error_code = av_packet_make_refcounted(packet);


		int sendCode = avcodec_send_packet(codecContext, packet);
		if (sendCode >= 0) {
			while (1) {
				int arfcode = avcodec_receive_frame(codecContext, frame);
				if (arfcode == -11 || arfcode == 0xDFB9B0BB) {
					break;
				}
				if (arfcode < 0) {
					printf("receive frame failed \n");
					return 0;
				}

				av_frame_unref(frame);

			}
		}
		cout << "error_code : " << error_code << endl;
		printf("read sample offset: 0x%llX size: 0x%X isEncrypted: false\n", sample.GetOffset(), sample.GetSize());
	}
	delete data;
	
	return AP4_Result();
}
