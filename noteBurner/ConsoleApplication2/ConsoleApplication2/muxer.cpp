// muxer.cpp

extern "C" {
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/opt.h>
#include <libavutil/timestamp.h>
#include <libavutil/imgutils.h>
#include <libswscale/swscale.h>
}
#include "muxer.h"
#include <tuple>
#include <array>
#include <vector>


muxer::muxer()
	:width_{},
	height_{},
	y_size_{},
	uv_size_{},
	pts_{},
	codec_ctx_{ nullptr },
	fmt_ctx_{ nullptr },
	out_stream_{ nullptr },
	yuv_frame_{ nullptr }
{
}

muxer::~muxer()
{
	uninit();
}


bool muxer::init(int w, int h, int fps, int bit_rate, char* outfile_name)
{
	uninit();

	width_ = w;
	height_ = h;
	y_size_ = w * h;
	uv_size_ = y_size_ / 4;

	// [1] 创建解码器
	const AVCodec* encoder = avcodec_find_encoder(AV_CODEC_ID_H264);
	if (!encoder) {
		fprintf(stderr, "Find encoder AV_CODEC_ID_H264 failed!\n");
		return false;
	}
	// 获取解码器上下文
	codec_ctx_ = avcodec_alloc_context3(encoder);
	if (!codec_ctx_) {
		fprintf(stderr, "Alloc context for encoder contx failed!\n");
		return false;
	}
	// 设置解码器上下文参数
	//codec_ctx_->bit_rate = bit_rate;
	codec_ctx_->width = width_;
	codec_ctx_->height = height_;
	codec_ctx_->time_base = AVRational{ 1, fps };
	codec_ctx_->gop_size = 50;
	codec_ctx_->max_b_frames = 0;
	codec_ctx_->pix_fmt = AV_PIX_FMT_YUV420P;
	codec_ctx_->thread_count = 4;
	codec_ctx_->qmin = 10;
	codec_ctx_->qmax = 51;
	codec_ctx_->qcompress = 0.6f;
	codec_ctx_->flags |= AV_CODEC_FLAG_GLOBAL_HEADER;

	//av_opt_set(codec_ctx_->priv_data, "preset", "ultrafast", 0);
	av_opt_set(codec_ctx_->priv_data, "tune", "zerolatency", 0);

	// 打开解码器
	if (avcodec_open2(codec_ctx_, encoder, nullptr) < 0) {
		fprintf(stderr, "Open encoder failed!\n");
		return false;
	}

	// [2] 创建输出上下文
	avformat_alloc_output_context2(&fmt_ctx_, nullptr, nullptr, outfile_name);

	// [3] 添加输出视频流
	out_stream_ = avformat_new_stream(fmt_ctx_, nullptr);
	out_stream_->id = 0;
	out_stream_->codecpar->codec_tag = 0;
	avcodec_parameters_from_context(out_stream_->codecpar, codec_ctx_);

	av_dump_format(fmt_ctx_, out_stream_->id, outfile_name, 1);

	// 创建YUV格式帧
	yuv_frame_ = av_frame_alloc();
	yuv_frame_->format = AV_PIX_FMT_YUV420P;
	yuv_frame_->width = width_;
	yuv_frame_->height = height_;
	// 为创建的YUV帧分配内存
	if (av_frame_get_buffer(yuv_frame_, 0) < 0) {
		av_frame_free(&yuv_frame_);
		yuv_frame_ = nullptr;
		fprintf(stderr, "Frame get buffer failed!\n");
		return false;
	}

	// [5] 打开输出视频文件并写入视频头信息
	if (avio_open(&fmt_ctx_->pb, outfile_name, AVIO_FLAG_WRITE) < 0) {
		fprintf(stderr, "avio_open  failed!\n");
		return false;
	}
	if (avformat_write_header(fmt_ctx_, nullptr) < 0) {
		fprintf(stderr, "Write header failed!\n");
		return false;
	}

	return true;
}

void muxer::uninit()
{
	if (fmt_ctx_) {
		av_write_trailer(fmt_ctx_);
		avio_close(fmt_ctx_->pb);
		avformat_free_context(fmt_ctx_);
		fmt_ctx_ = nullptr;
	}

	if (codec_ctx_) {
		avcodec_close(codec_ctx_);
		avcodec_free_context(&codec_ctx_);
		codec_ctx_ = nullptr;
	}

	if (yuv_frame_) {
		av_frame_free(&yuv_frame_);
		yuv_frame_ = nullptr;
	}

	width_ = 0;
	height_ = 0;
	y_size_ = 0;
	uv_size_ = 0;
	pts_ = 0;
}

bool muxer::write_image(const uint8_t* bgr)
{
	// 分配YUV格式数据的内存
	thread_local std::vector<uint8_t> yuv_data;
	if (yuv_data.size() != y_size_ * 3 / 2) {
		yuv_data.resize(y_size_ * 3 / 2);
	}
	// BGR格式转YUV格式
	bgr_to_yuv420p(bgr, yuv_data.data());

	return write_yuv(yuv_data.data());
}

bool muxer::write_yuv(const uint8_t* yuv_data)
{
	//拷贝YUV数据到帧，由于帧数据存在内存对齐，故需逐行拷贝
	for (int i = 0; i < height_; i++) {
		memcpy(yuv_frame_->data[0] + i * yuv_frame_->linesize[0], yuv_data + width_ * i, width_);
	}
	const int uv_stride = width_ / 2;
	for (int i = 0; i < height_ / 2; i++) {
		memcpy(yuv_frame_->data[1] + i * yuv_frame_->linesize[1], yuv_data + y_size_ + uv_stride * i, uv_stride);
		memcpy(yuv_frame_->data[2] + i * yuv_frame_->linesize[2], yuv_data + y_size_ + uv_size_ + uv_stride * i, uv_stride);
	}

	yuv_frame_->pts = pts_++;

	return write_frame(yuv_frame_);
}

bool muxer::write_frame(const AVFrame* frame)
{
	char errbuf[64]{ 0 };
	// 将帧数据发送到编码器
	int ret = avcodec_send_frame(codec_ctx_, frame);
	if (ret < 0) {
		fprintf(stderr, "Error sending a frame to the encoder: %s\n", av_make_error_string(errbuf, sizeof(errbuf), ret));
		return false;
	}

	while (true) {
		AVPacket pkt{ 0 };
		// 获取编码后的数据
		ret = avcodec_receive_packet(codec_ctx_, &pkt);
		if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
			return true;
		else if (ret < 0) {
			fprintf(stderr, "Error encoding a frame: %s\n", av_make_error_string(errbuf, sizeof(errbuf), ret));
			return false;
		}
		// 将pts缩放到输出流的time_base上
		av_packet_rescale_ts(&pkt, codec_ctx_->time_base, out_stream_->time_base);
		pkt.stream_index = out_stream_->index;
		// 将数据写入到输出流
		ret = av_interleaved_write_frame(fmt_ctx_, &pkt);
		av_packet_unref(&pkt);
		if (ret < 0) {
			fprintf(stderr, "Error while writing output packet: %s\n", av_make_error_string(errbuf, sizeof(errbuf), ret));
			return false;
		}
	}

	return true;
}

bool muxer::flush()
{
	return write_frame(nullptr);
}

bool muxer::bgr_to_yuv420p(const uint8_t* const buf_bgr, uint8_t* const buf_420p)
{
	//// 分配转换上下文
	//thread_local std::tuple params{ 0, 0, 0 };
	//thread_local std::unique_ptr<SwsContext, decltype(&sws_freeContext)> sws_context{ nullptr, &sws_freeContext };

	//std::tuple new_params{ width_, height_, av_image_get_linesize(AV_PIX_FMT_YUV420P, width_, 0) };
	//if (!sws_context || params != new_params)
	//{
	//	sws_context.reset(sws_getContext(width_, height_, AV_PIX_FMT_BGR24, width_, height_,
	//		AV_PIX_FMT_YUV420P, SWS_FAST_BILINEAR, nullptr, nullptr, nullptr));
	//	params = new_params;
	//}
	//// 转换格式
	//const int stride = std::get<2>(params);//Y平面一行的数据长度
	//const int ret = sws_scale(sws_context.get(),
	//	std::array{ buf_bgr }.data(),/* bgr数据只有一个平面 */
	//	std::array{ width_ * 3 }.data(),/* BGR所以图像宽度*3 */
	//	0, height_,
	//	std::array{ buf_420p, buf_420p + y_size_, buf_420p + y_size_ + uv_size_ }.data(),/* YUV三个平面的起始地址 */
	//	std::array{ stride, stride / 2, stride / 2 }.data());/* YUV每个平面中一行的宽度 */

	return 0;
}

