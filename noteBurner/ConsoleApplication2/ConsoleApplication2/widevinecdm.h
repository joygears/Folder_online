#pragma once

class muxer;
extern "C"
{
#include <libavcodec\avcodec.h>
#include <libavformat\avformat.h>
#include <libswscale\swscale.h>
#include <libavutil\pixfmt.h>

#include <libavutil\opt.h>

};



struct VideoDecoderConfig {
    int codec;
    int profile;
    int alpha_mode;
    int color_space;
    int width;
    int height;
    int m_18;
    int m_1C;
    int m_20;
};

extern AVCodecContext* decodecContext;
extern AVCodecContext* encodecContext;
extern AVStream* videoStream;
extern AVFormatContext* outputFormatContext;
extern muxer * encode;
extern AP4_UI16 width;
extern AP4_UI16 height;
extern int segCount;