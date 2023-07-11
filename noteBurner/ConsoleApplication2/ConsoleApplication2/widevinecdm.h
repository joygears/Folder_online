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

extern AVCodecContext* decodecContext;
extern AVCodecContext* encodecContext;
extern AVStream* videoStream;
extern AVFormatContext* outputFormatContext;
extern muxer * encode;