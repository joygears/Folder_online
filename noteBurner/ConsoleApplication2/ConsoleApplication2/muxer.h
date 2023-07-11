// muxer.h
#pragma once
#include <memory>

class AVFrame;
class AVStream;
class AVCodecContext;
class AVFormatContext;

class muxer
{
public:
	muxer();
	~muxer();

	bool init(int w, int h, int fps, int bit_rate, char* outfile_name);
	void uninit();
	bool write_image(const uint8_t* bgr);
	bool write_yuv(const uint8_t* yuv_data);
	bool write_frame(const AVFrame* frame);
	bool flush();

private:
	bool bgr_to_yuv420p(const uint8_t* const buf_bgr, uint8_t* const buf_420p);

private:
	int width_;
	int height_;
	int y_size_;
	int uv_size_;
	int pts_;
	AVCodecContext* codec_ctx_;
	AVFormatContext* fmt_ctx_;
	AVStream* out_stream_;
	AVFrame* yuv_frame_;
};

