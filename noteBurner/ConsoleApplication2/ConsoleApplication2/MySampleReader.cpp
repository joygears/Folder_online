#include <iostream>
#include <iomanip>
#include "MySampleReader.h"
#include "MySampleDecrypter.h"
using namespace std;
#include "widevinecdm.h"
#include "muxer.h"

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
	

	
	AVFrame* frame;
	frame = av_frame_alloc();
	AVPacket* packet = av_packet_alloc();
	
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


		packet->data = (uint8_t*)data;
		packet->size = dataSize;
		packet->duration = 0xa2c3;
		int error_code = av_packet_make_refcounted(packet);


		int sendCode = avcodec_send_packet(decodecContext, packet);
		if (sendCode >= 0) {
			while (1) {
				int arfcode = avcodec_receive_frame(decodecContext, frame);
				if (arfcode == 0|| arfcode == 0xDFB9B0BB || arfcode == AVERROR(EAGAIN)) {
					break;
				}
				if (arfcode < 0) {
					printf("receive frame failed \n");
					return 0;
				}

			}
		}
		//// 输入AVFrame的宽、高和像素格式
		//int src_w = frame->width;
		//int src_h = frame->height;
		//AVPixelFormat src_pix_fmt = (AVPixelFormat)frame->format;
		//// 目标输出YUV420P格式
		//int dst_w = src_w;
		//int dst_h = src_h;
		//AVPixelFormat dst_pix_fmt = AV_PIX_FMT_YUV420P;
		//// 创建SwsContext对象
		//struct SwsContext* sws_ctx = sws_getContext(src_w, src_h, src_pix_fmt,
		//	dst_w, dst_h, dst_pix_fmt,
		//	SWS_BILINEAR, NULL, NULL, NULL);
		//// 分配输出YUV数据缓冲区
		//uint8_t* data[AV_NUM_DATA_POINTERS] = { 0 };
		//data[0] = new uint8_t[dst_w * dst_h];
		//data[1] = new uint8_t[dst_w / 2 * dst_h / 2];
		//data[2] = new uint8_t[dst_w / 2 * dst_h / 2];
		//int linesize[AV_NUM_DATA_POINTERS] = { 0 };
		//linesize[0] = dst_w;
		//linesize[1] = dst_w / 2;
		//linesize[2] = dst_w / 2;
		//// 调用sws_scale()函数进行像素格式转换和缩放操作
		//sws_scale(sws_ctx, frame->data, frame->linesize,
		//	0, src_h, data, linesize);
		//// 释放SwsContext对象和输出YUV数据缓冲区
		//sws_freeContext(sws_ctx);
		//const char* output_filename = "output.yuv";
		//FILE* fp_out = fopen(output_filename, "ab");
		//if (!fp_out) {
		//	printf("Could not open %s\n", output_filename);
		//	return -1;
		//}
		//// 写入YUV420P数据
		//fwrite(data[0], 1, dst_w * dst_h, fp_out);
		//fwrite(data[1], 1, dst_w / 2 * dst_h / 2, fp_out);
		//fwrite(data[2], 1, dst_w / 2 * dst_h / 2, fp_out);
		//// 关闭输出文件
		//fclose(fp_out);

		/*if (!encode->write_frame(frame))
			fprintf(stderr, "write frame fail.\n");*/
		char errbuf[64]{ 0 };
		cout << "error_code : " << error_code << endl;
		printf("read sample offset: 0x%llX size: 0x%X isEncrypted: false\n", sample.GetOffset(), sample.GetSize());
		int ret = avcodec_send_frame(encodecContext, frame);
		if (ret < 0) {
			fprintf(stderr, "Error sending a frame to the encoder: %s\n", av_make_error_string(errbuf, sizeof(errbuf), ret));
			return false;
		}
		while (true) {
			AVPacket pkt{ 0 };
			// 获取编码后的数据
			ret = avcodec_receive_packet(encodecContext, &pkt);
			if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
				return true;
			else if (ret < 0) {
				fprintf(stderr, "Error encoding a frame: %d\n", ret);
				return false;
			}
			// 将pts缩放到输出流的time_base上
			av_packet_rescale_ts(&pkt, encodecContext->time_base, videoStream->time_base);
			pkt.stream_index = videoStream->index;
			// 将数据写入到输出流
			ret = av_interleaved_write_frame(outputFormatContext, &pkt);
			av_packet_unref(&pkt);
			if (ret < 0) {
				fprintf(stderr, "Error while writing output packet: %d\n", ret);
				return false;
			}
		}

	}

	av_packet_free(&packet);
	av_frame_free(&frame);
	delete data;
	
	return AP4_Result();
}
