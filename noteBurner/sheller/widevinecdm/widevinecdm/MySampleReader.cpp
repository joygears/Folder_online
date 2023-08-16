#include <iostream>
#include <sstream>
#include <iomanip>
#include "MySampleReader.h"
#include "MySampleDecrypter.h"
#include "widevinecdm.h"
#include "webNetwork.h"
#include "fucntion.h"

AVFrame* convertYUV420P10LEtoYUV420P(const uint8_t* srcBuffer, int width, int height) {
    // 创建源 AVFrame（YUV420P10LE 格式）
    AVFrame* srcFrame = av_frame_alloc();
    if (!srcFrame) {
        fprintf(stderr, "Could not allocate source frame\n");
        return nullptr;
    }
   
    // 设置源 AVFrame 的参数
    srcFrame->width = width;
    srcFrame->height = height;
    srcFrame->format = AV_PIX_FMT_YUV420P10LE;

    // 分配源帧数据的内存
    int ret = av_frame_get_buffer(srcFrame, 0);
    if (ret < 0) {
        fprintf(stderr, "Could not allocate source frame data\n");
        av_frame_free(&srcFrame);
        return nullptr;
    }
   
    // 将 YUV420P10LE 数据填充到 srcFrame->data[0]、srcFrame->data[1]、srcFrame->data[2]
    int planeSizeY = width * height * 2; // 10 bits per pixel
    int planeSizeUV = width * height / 2; // 10 bits per pixel
    memcpy(srcFrame->data[0], srcBuffer, planeSizeY);
    memcpy(srcFrame->data[1], srcBuffer + planeSizeY, planeSizeUV);
    memcpy(srcFrame->data[2], srcBuffer + planeSizeY + planeSizeUV, planeSizeUV);
   
    
    // 创建目标 AVFrame（YUV420P 格式）
    AVFrame* dstFrame = av_frame_alloc();
    if (!dstFrame) {
        fprintf(stderr, "Could not allocate destination frame\n");
        av_frame_free(&srcFrame);
        return nullptr;
    }

    // 设置目标 AVFrame 的参数
    dstFrame->width = width;
    dstFrame->height = height;
    dstFrame->format = AV_PIX_FMT_YUV420P;

    // 分配目标帧数据的内存
    ret = av_frame_get_buffer(dstFrame, 0);
    if (ret < 0) {
        fprintf(stderr, "Could not allocate destination frame data\n");
        av_frame_free(&srcFrame);
        av_frame_free(&dstFrame);
        return nullptr;
    }

    // 创建像素格式转换上下文
    struct SwsContext* sws_ctx = sws_getContext(
        width, height, AV_PIX_FMT_YUV420P10LE,
        width, height, AV_PIX_FMT_YUV420P,
        SWS_BILINEAR, nullptr, nullptr, nullptr
    );

    // 进行像素格式转换
    sws_scale(sws_ctx, srcFrame->data, srcFrame->linesize, 0, height,
        dstFrame->data, dstFrame->linesize);

    // 释放像素格式转换上下文
    sws_freeContext(sws_ctx);

    // 释放源 AVFrame
    av_frame_free(&srcFrame);

    return dstFrame;
}

void saveFrameAsYUV420P10LE(const char* outputFilename, AVFrame* frame) {
    // 打开输出 YUV 文件
    FILE* yuvFile = fopen(outputFilename, "ab");
    if (!yuvFile) {
        fprintf(stderr, "Could not open output YUV file\n");
        return;
    }

    // 将 YUV420P10LE 数据写入输出文件
    for (int i = 0; i < frame->height; i++) {
        fwrite(frame->data[0] + i * frame->linesize[0], 1, frame->width * 2, yuvFile);
    }
    for (int i = 0; i < frame->height / 2; i++) {
        fwrite(frame->data[1] + i * frame->linesize[1], 1, frame->width / 2 * 2, yuvFile);
        fwrite(frame->data[2] + i * frame->linesize[2], 1, frame->width / 2 * 2, yuvFile);
    }

    // 关闭文件
    fclose(yuvFile);
}

void saveAVFrameAsYUV(AVFrame* frame, const std::string& saveFileName) {
    // 初始化FFmpeg库
  

    // 初始化像素格式转换上下文
    AVCodecContext* codecContext = avcodec_alloc_context3(NULL);
    if (!codecContext) {
        fprintf(stderr, "Could not allocate codec context\n");
        return;
    }

    codecContext->width = frame->width;
    codecContext->height = frame->height;
    codecContext->pix_fmt = AV_PIX_FMT_YUV420P; // 目标像素格式

    struct SwsContext* sws_ctx = sws_getContext(
        frame->width, frame->height, (AVPixelFormat)frame->format,
        codecContext->width, codecContext->height, codecContext->pix_fmt,
        SWS_BILINEAR, NULL, NULL, NULL
    );

    // 分配一个AVFrame用于存储转换后的图像数据
    AVFrame* convertedFrame = av_frame_alloc();
    convertedFrame->width = codecContext->width;
    convertedFrame->height = codecContext->height;
    convertedFrame->format = codecContext->pix_fmt;
    av_frame_get_buffer(convertedFrame, 32); // 分配图像数据内存

    // 进行像素格式转换
    sws_scale(sws_ctx, frame->data, frame->linesize, 0, frame->height,
        convertedFrame->data, convertedFrame->linesize);

    // 保存转换后的图像数据到文件
    FILE* outputFile = fopen(saveFileName.c_str(), "ab");
    if (!outputFile) {
        fprintf(stderr, "Could not open output file\n");
        av_frame_free(&convertedFrame);
        avcodec_free_context(&codecContext);
        sws_freeContext(sws_ctx);
        return;
    }

    for (int i = 0; i < codecContext->height; i++) {
        fwrite(convertedFrame->data[0] + i * convertedFrame->linesize[0], 1, codecContext->width, outputFile);
    }
    for (int i = 0; i < codecContext->height / 2; i++) {
        fwrite(convertedFrame->data[1] + i * convertedFrame->linesize[1], 1, codecContext->width / 2, outputFile);
        fwrite(convertedFrame->data[2] + i * convertedFrame->linesize[2], 1, codecContext->width / 2, outputFile);
    }

    fclose(outputFile);

    // 清理资源
    av_frame_free(&convertedFrame);
    avcodec_free_context(&codecContext);
    sws_freeContext(sws_ctx);
}

AVFrame* createAVFrameFromYUV420P10LE(uint8_t* yuv_data, int width, int height) {
    int frame_size = width * height * 3 / 2;

    // Create AVFrame
    AVFrame* frame = av_frame_alloc();
    if (!frame) {
        fprintf(stderr, "Failed to allocate AVFrame\n");
        return NULL;
    }
  
    // Set frame properties
    frame->width = width;
    frame->height = height;
    frame->format = AV_PIX_FMT_YUV420P10LE;
   
    // Allocate buffer for frame data
    int ret = av_frame_get_buffer(frame, 32); // 32-byte alignement
    if (ret < 0) {
        av_frame_free(&frame);
        fprintf(stderr, "Failed to allocate frame buffer\n");
        return NULL;
    }

    // Copy YUV data to AVFrame
    for (int i = 0; i < height; i++) {
        memcpy(frame->data[0] + i * frame->linesize[0], yuv_data + i * width * 2, width * 2);
    }
    for (int i = 0; i < height / 2; i++) {
        memcpy(frame->data[1] + i * frame->linesize[1], yuv_data + width * height * 2 + i * width, width / 2 * 2);
        memcpy(frame->data[2] + i * frame->linesize[2], yuv_data + width * height * 5 / 2 + i * width, width / 2 * 2);
    }
  
    return frame;
}

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

    auto printProgressBar = [](double progress) {
        const int barWidth = 50; // 进度条宽度
        std::cout << "[";

        int pos = barWidth * progress;
        for (int i = 0; i < barWidth; ++i) {
            if (i < pos) std::cout << "=";
            else if (i == pos) std::cout << ">";
            else std::cout << " ";
        }

        std::cout << "] " << static_cast<int>(progress * 100.0) << " %\r";
        std::cout.flush();
    };

    printProgressBar(curSegIndex / segCount);
   
   

    int dataSize = sample.GetSize();
    char* data = new char[dataSize + 1];
    memset(data, 0, dataSize + 1);
    sample.GetDataStream()->Seek(sample.GetOffset());
    sample.GetDataStream()->Read(data, dataSize);



    AVFrame* frame;
    //frame = av_frame_alloc();
    AVPacket* packet = av_packet_alloc();

    InputBuffer_2 input{ 0 };
    MyVideoFrame videoFrame;
    MyVideoFrame* video_frame = &videoFrame;
    int64_t timestamp = ((double)sample.GetDts() * ((double)1000000 / (double)m_decrypter->m_timeScale) + 0.5);
    do {
        if (this->m_decrypter->m_protectedType != EncryptionScheme::kUnencrypted) {

            AP4_Cardinal subsample_count = 0;
            const AP4_UI16* bytes_of_cleartext_data;
            const AP4_UI32* bytes_of_encrypted_data;

            const AP4_UI08* iv = m_decrypter->m_table->GetIv(m_decrypter->index);
            uint32_t ivSize = m_decrypter->m_table->GetIvSize();
            


            m_decrypter->m_table->GetSampleInfo(m_decrypter->index, subsample_count, bytes_of_cleartext_data, bytes_of_encrypted_data);


            Log("read sample offset: 0x%llX size: 0x%X isEncrypted: true m_DefaultCryptByteBlock %d m_DefaultSkipByteBlock %d \n", sample.GetOffset(), sample.GetSize(), m_decrypter->m_DefaultCryptByteBlock, m_decrypter->m_DefaultSkipByteBlock);
            printf("keyid: ");
            printfHex((char*)m_decrypter->m_key_id, m_decrypter->m_key_id_size);
            printf("iv: ");
            printfHex((char*)iv, ivSize);

            for (int i = 0; i < subsample_count; i++) {
                printf("subsample[%d] bytes_of_cleartext_data %X bytes_of_encrypted_data %X\n", i, bytes_of_cleartext_data[i], bytes_of_encrypted_data[i]);
            }
            m_decrypter->index++;



            char* key_id = (char*)m_decrypter->m_key_id;


            SubsampleEntry* subsamples = new SubsampleEntry[subsample_count];
            for (int i = 0; i < subsample_count; i++) {
                subsamples[i].clear_bytes = bytes_of_cleartext_data[i];
                subsamples[i].cipher_bytes = bytes_of_encrypted_data[i];
            }



           
            input.data = (UINT8*)data;
            input.data_size = dataSize;
            input.encryption_scheme = m_decrypter->m_protectedType;
            input.key_id = (uint8_t*)key_id;
            input.key_id_size = 0x10;
            input.iv = iv;
            input.iv_size = ivSize;
            input.subsamples = subsamples;
            input.num_subsamples = subsample_count;
            input.pattern.crypt_byte_block = m_decrypter->m_DefaultCryptByteBlock;
            input.pattern.skip_byte_block = m_decrypter->m_DefaultSkipByteBlock;
            input.timestamp = timestamp;
          

          


        }
        else {

          /*  packet->data = (uint8_t*)data;
            packet->size = dataSize;
            packet->duration = sample.GetDuration();;
            int error_code = av_packet_make_refcounted(packet);


            int sendCode = avcodec_send_packet(decodecContext, packet);
            if (sendCode >= 0) {
                while (1) {
                    int arfcode = avcodec_receive_frame(decodecContext, frame);
                    if (arfcode == 0 || arfcode == 0xDFB9B0BB || arfcode == AVERROR(EAGAIN)) {
                        break;
                    }
                    if (arfcode < 0) {
                        printf("receive frame failed \n");
                        return 0;
                    }

                }
            }*/

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
            //    dst_w, dst_h, dst_pix_fmt,
            //    SWS_BILINEAR, NULL, NULL, NULL);
            //// 分配输出YUV数据缓冲区
            //uint8_t* buffer[AV_NUM_DATA_POINTERS] = { 0 };
            //buffer[0] = new uint8_t[dst_w * dst_h];
            //buffer[1] = new uint8_t[dst_w / 2 * dst_h / 2];
            //buffer[2] = new uint8_t[dst_w / 2 * dst_h / 2];
            //int linesize[AV_NUM_DATA_POINTERS] = { 0 };
            //linesize[0] = dst_w;
            //linesize[1] = dst_w / 2;
            //linesize[2] = dst_w / 2;
            //// 调用sws_scale()函数进行像素格式转换和缩放操作
            //sws_scale(sws_ctx, frame->data, frame->linesize,
            //    0, src_h, buffer, linesize);
            //// 释放SwsContext对象和输出YUV数据缓冲区
            //sws_freeContext(sws_ctx);
            //const char* output_filename = "frame.yuv";
            //FILE* fp_out = fopen(output_filename, "ab");
            //if (!fp_out) {
            //    printf("Could not open %s\n", output_filename);
            //    return -1;
            //}
            //// 写入YUV420P数据
            //fwrite(buffer[0], 1, dst_w * dst_h, fp_out);
            //fwrite(buffer[1], 1, dst_w / 2 * dst_h / 2, fp_out);
            //fwrite(buffer[2], 1, dst_w / 2 * dst_h / 2, fp_out);
            //// 关闭输出文件
            //fclose(fp_out);

            //delete[] buffer[0];
            //delete[] buffer[1];
            //delete[] buffer[2];

            input.data = (UINT8*)data;
            input.data_size = dataSize;
            input.encryption_scheme = m_decrypter->m_protectedType;
            input.timestamp = timestamp;

            printf("read sample offset: 0x%llX size: 0x%X isEncrypted: false\n", sample.GetOffset(), sample.GetSize());
        }

        int result = proxy->DecryptAndDecodeFrame(&input, &videoFrame);
        Log("DecryptAndDecodeFrame result %d\n", result);
        if (result == 1)
            break;
        /*cout << "width * height:" << videoFrame.SSize().width << "*" << videoFrame.SSize().height << endl;
        cout << "videoFrame.m_format : " << videoFrame.Format() << endl;
        cout << "Timestamp : " << videoFrame.Timestamp() << endl;
        for (int i = 0; i < VideoFrame::VideoPlane::kMaxPlanes; i++) {
            cout << "videoFrame.PlaneOffset((VideoFrame::VideoPlane)" << i << ")" << videoFrame.PlaneOffset((VideoFrame::VideoPlane)i) << endl;
            cout << "videoFrame.Stride((VideoFrame::VideoPlane)" << i << ")" << videoFrame.Stride((VideoFrame::VideoPlane)i) << endl;
        }*/
    
        //if (sample.GetOffset() == 0xADBE9) {
           // FILE* pVideo;
           //pVideo = fopen("frame.yuv", "ab");
           // fwrite(video_frame->FrameBuffer()->Data(), 1, video_frame->SSize().width * video_frame->SSize().height * 1.5*2, pVideo);


           // fclose(pVideo);
      //   //   exit(0);
      ////  }
        if (decodecContext->pix_fmt == AV_PIX_FMT_YUV420P) {
            Log("pix_fmt==AV_PIX_FMT_YUV420P");
            unsigned char* buffer = NULL;
            transtoYUV(video_frame, buffer);


            // if (this->m_decrypter->m_protectedType != EncryptionScheme::kUnencrypted)


            auto transYUVToAVFrame = [](uint8_t* yuvData, AVFrame*& frame)->int {
                frame = av_frame_alloc();
                if (!frame) {
                    Log( "conot getframe AVFrame\n");
                    return -1;
                }

                int width = g_width;  // 视频帧宽度
                int height = g_height; // 视频帧高度

                frame->format = AV_PIX_FMT_YUV420P;
                frame->width = width;
                frame->height = height;

                int dataSize = av_image_get_buffer_size((AVPixelFormat)frame->format, frame->width, frame->height, 1);
                uint8_t* data = (uint8_t*)av_malloc(dataSize);
                frame->data[0] = data;                                        // Y分量
                frame->data[1] = data + width * height;                       // U分量
                frame->data[2] = data + width * height + (width / 2) * (height / 2); // V分量
                frame->linesize[0] = width;                            // Y分量的行大小
                frame->linesize[1] = width / 2;                        // U分量的行大小
                frame->linesize[2] = width / 2;

                memcpy(frame->data[0], yuvData, width * height);                           // 拷贝Y分量
                memcpy(frame->data[1], yuvData + width * height, (width / 2) * (height / 2));  // 拷贝U分量
                memcpy(frame->data[2], yuvData + width * height + (width / 2) * (height / 2), (width / 2) * (height / 2)); // 拷贝V分量
                return 0;
            };


            transYUVToAVFrame(buffer, frame);

            // saveFrameAsYUV420P10LE("frame.yuv", frame);
            delete buffer;

        }
        else {
            Log("pix_fmt==AV_PIX_FMT_YUV420P10LE");
            frame = convertYUV420P10LEtoYUV420P(video_frame->FrameBuffer()->Data(), g_width, g_height);
        }
        Log("decode finished \n");

        char errbuf[64]{ 0 };
        static int p = 0;
        int ret = 1;

        frame->pts = p;
       
        p++;
        ret = avcodec_send_frame(encodecContext, frame);
        while (1) {


            AVPacket pkt{ 0 };
            av_init_packet(&pkt);
            // 获取编码后的数据
            ret = avcodec_receive_packet(encodecContext, &pkt);
            if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) {
                break;
            }

            else
                if (ret < 0) {
                    Log("Error encoding a frame: %s\n", av_make_error_string(errbuf, sizeof(errbuf), ret));
                    return 1007;
                }

            // 将pts缩放到输出流的time_base上
            av_packet_rescale_ts(&pkt, encodecContext->time_base, videoStream->time_base);
            pkt.stream_index = videoStream->index;
            // 将数据写入到输出流
            ret = av_interleaved_write_frame(outputFormatContext, &pkt);
            av_packet_unref(&pkt);
          

        }

      
        Log("encode finished \n");
      if (this->m_decrypter != nullptr && decodecContext->pix_fmt == AV_PIX_FMT_YUV420P)
         av_free(frame->data[0]);
   
    av_frame_free(&frame);
    
     }while (false);
    av_packet_free(&packet);
    delete data;
	return AP4_Result();
}
