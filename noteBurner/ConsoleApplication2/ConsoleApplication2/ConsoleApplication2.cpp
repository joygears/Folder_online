//#include <Windows.h>
//#include <iostream>
//#include <fstream>
//#include <bento4/Ap4.h>
//#include "bento4/Ap4Atom.h"
//#include <map>
//#include "MyLinearReader.h"
//#include "widevinecdm.h"
//#include "muxer.h"
//
//using namespace std;
//int __cdecl transToVideoProfile(char a1);
//
//AVCodecContext* decodecContext = 0;
//AVCodecContext* encodecContext = 0;
//AVStream* videoStream = 0;
//AVFormatContext* outputFormatContext = 0;
//muxer* encode = new muxer;
//int main() {
//
//	AP4_ByteStream* input_stream = NULL;
//	AP4_Result result = AP4_FileByteStream::Create(R"(0-44306.mp4)",
//		AP4_FileByteStream::STREAM_MODE_READ,
//		input_stream);
//
//	if (result != AP4_SUCCESS || input_stream == nullptr) {
//		// 处理文件打开错误
//		return result;
//	}
//	AP4_File file(*input_stream);
//	AP4_Movie* movie = file.GetMovie();
//	//
//	//AP4_MoovAtom* moovAtom = movie->GetMoovAtom();
//	//if (moovAtom == nullptr) {
//	//	// 处理 MoovAtom 获取错误
//	//	return result;
//	//}
//
//
//	//AP4_List<AP4_Atom>::Item* currentItem = (AP4_List<AP4_Atom>::Item*) * (int*)((char*)moovAtom + 0x34);
//	//while (currentItem) {
//
//	//	if (currentItem->GetData()->GetType() == AP4_ATOM_TYPE_PSSH) {
//	//		AP4_PsshAtom* PsshAtom = dynamic_cast<AP4_PsshAtom*>(currentItem->GetData());
//	//		AP4_DataBuffer  Ap4DataBuffer = PsshAtom->GetData();
//
//
//	//	}
//	//	currentItem = currentItem->GetNext();
//	//}
//
//
//	AP4_Cardinal track_count = movie->GetTracks().ItemCount();
//	if (!track_count)
//		return 1600;
//	AP4_ProtectedSampleDescription* ProtectedSampleDescription;
//	AP4_Track* pTrack;
//	while (1) {
//
//		AP4_List<AP4_Track>::Item* item = movie->GetTracks().FirstItem();
//		pTrack = item->GetData();
//		if (!pTrack)
//			return 1600;
//		AP4_SampleDescription * SampleDescription = pTrack->GetSampleDescription(0);
//		if (SampleDescription && SampleDescription->GetType() != AP4_SampleDescription::Type::TYPE_PROTECTED) {
//			//处理未加密的track流
//		}
//		else {
//			 ProtectedSampleDescription = dynamic_cast<AP4_ProtectedSampleDescription*>(SampleDescription);
//			if (ProtectedSampleDescription)
//				break;
//		}
//	}
//	//AP4_UI32 schemeType = ProtectedSampleDescription->GetSchemeType();
//	//if (schemeType == 0x63656E63
//	//	|| schemeType == 0x63626331
//	//	|| schemeType == 0x63656E73
//	//	|| schemeType == 0x63626373
//	//	|| schemeType == 0x70696666)
//	//{
//	//	printf("protection scheme type: %u\n", schemeType);
//	//}
//	//else
//	//{
//	//	printf("unhandled protection scheme type: %u\n", schemeType);
//	//}
//
//	//AP4_SampleDescription* OriginalSampleDescription = ProtectedSampleDescription->GetOriginalSampleDescription();
//	//char* format;
//	//AP4_String codec;
//	//if (OriginalSampleDescription) {
//	//	format = (char *)AP4_GetFormatName(OriginalSampleDescription->GetFormat());
//	//	OriginalSampleDescription->GetCodecString(codec);
//
//	//	printf( "format:%s, codec:%s, type:%d \n", format, codec.GetChars(), OriginalSampleDescription->GetType());
//	//}
//	//AP4_Atom::Type trackType = pTrack->GetType();
//	//if (trackType != AP4_Track::TYPE_AUDIO ) {
//	//	if(trackType != AP4_Track::TYPE_VIDEO)
//	//	return 1600;
//	//	AP4_VideoSampleDescription* VideoSampleDescription = dynamic_cast<AP4_VideoSampleDescription*>(OriginalSampleDescription);
//	//	AP4_UI16 width = VideoSampleDescription->GetWidth();
//	//	AP4_UI16 hegiht = VideoSampleDescription->GetHeight();
//	//	std:: string codecStr = codec.GetChars();
//	//	if (codecStr.find("avc1",0) == std::string::npos) {
//
//	//		if(codecStr.find("vp09",0) == std::string::npos)
//	//			printf( "codec %s not yet handled ", codecStr.c_str());
//	//		/*video_decoder_config[1] = 1;
//	//		video_decoder_config[0] = 3;
//	//		video_decoder_config[2] = 2;*/
//	//	
//	//	}
//	//	else {
//	//		AP4_AvcSampleDescription * AvcSampleDescription = dynamic_cast<AP4_AvcSampleDescription*>(OriginalSampleDescription);
//	//		AP4_UI08 profile = AvcSampleDescription->GetProfile();
//	//		AP4_UI08 level = AvcSampleDescription->GetLevel();
//	//		int videoProfile = transToVideoProfile(profile);
//	//		
//	//	}
//
//	//}
//	//
//	//AP4_List<AP4_Atom>::Item*  curItem = file.GetTopLevelAtoms().FirstItem();
//	//AP4_List<AP4_TrakAtom>::Item* trakAtomitem =  moovAtom->GetTrakAtoms().FirstItem();
//	//AP4_TrakAtom* trakAtom = trakAtomitem->GetData();
//	// AP4_MdhdAtom* MdhdAtom = (AP4_MdhdAtom*)*(int*)((char*)trakAtom + 0x44);
//	// AP4_UI32  TimeScale = MdhdAtom->GetTimeScale();
//
//	// while (curItem) {
//
//	//	 if (curItem->GetData()->GetType() == AP4_ATOM_TYPE_SIDX) {
//	//		 AP4_SidxAtom* SidxAtom = dynamic_cast<AP4_SidxAtom*>(curItem->GetData());
//	//		
//	//		
//	//	 }
//	//	 else if (curItem->GetData()->GetType() == AP4_ATOM_TYPE_SSIX) {
//	//		 
//	//	 }
//	//	 curItem = curItem->GetNext();
//	// }
//
//
//
//	// AP4_ByteStream* input_stream2 = NULL;
//	//  result = AP4_FileByteStream::Create(R"(0-44306.mp4)",
//	//	 AP4_FileByteStream::STREAM_MODE_READ,
//	//	  input_stream2);
//
//	// AP4_AtomFactory factory;
//	// AP4_Atom * currentAtom;
//	// AP4_SidxAtom* SidxAtom = 0;;
//	// AP4_LargeSize size = 0;
//	// AP4_Position pos = 0;
//	// AP4_UI64 FirstOffset = 0;
//	// while (!factory.CreateAtomFromStream(*input_stream2, currentAtom)) {
//
//	//	 if (currentAtom->GetType() == AP4_ATOM_TYPE_SIDX) {
//	//		 SidxAtom = dynamic_cast<AP4_SidxAtom*>(currentAtom);
//	//		 size = SidxAtom->GetSize();
//	//		 FirstOffset = SidxAtom->GetFirstOffset();
//	//		 SidxAtom->GetReferences();
//	//		 break;
//	//	 }
//	//	 else if (currentAtom->GetType() == AP4_ATOM_TYPE_SSIX) {
//
//	//	 }
//	//	 input_stream2->Tell(pos);
//	// }
//
//	// AP4_UI64 segPos = pos + size + FirstOffset;
//
//	// const AP4_Array<AP4_SidxAtom::Reference>& References = SidxAtom->GetReferences();
//	// std::map<AP4_UI32, AP4_UI32> segs;
//	// AP4_UI32 curOffset = segPos;
//	// AP4_UI32 segsSize = 0;
//	// for (int i = 0; i < References.ItemCount(); i++) {
//	//	 segsSize += References[i].m_ReferencedSize;
//	//	if (segsSize >= 0x100000)
//	//	 {
//	//		segs[curOffset] = segsSize;
//	//		 printf("seg  offset %d  length %d\n", curOffset, segsSize);
//	//		 curOffset += segsSize;
//	//		 segsSize = 0;
//	//		 
//	//	 }
//	// }
//
//	 AP4_ByteStream* input_stream3 = NULL;
//	 result = AP4_FileByteStream::Create(R"(44306-1993788.mp4)",
//		 AP4_FileByteStream::STREAM_MODE_READ,
//		 input_stream3);
//	 AP4_Sample sample;
//	 AP4_DataBuffer sample_data;
//	 
//	 MyLinearReader LinearReader(*movie, input_stream3);
//	 LinearReader.EnableTrack(pTrack->GetId());
//	 AP4_ByteStream* m_FragmentStream = *(AP4_ByteStream**)(((char*)&LinearReader) + 0x14);
//	 AP4_Atom *pAtom;
//	 AP4_AtomFactory factory2;
//	 factory2.CreateAtomFromStream(*m_FragmentStream, pAtom);
//	 AP4_ContainerAtom* moov = dynamic_cast<AP4_ContainerAtom*>(pAtom);
//
//	 
//
//	 avformat_alloc_output_context2(&outputFormatContext, NULL, NULL, "tmp.mp4");
//	
//	 // 打开输出文件
//	 if (avio_open(&outputFormatContext->pb, "tmp.mp4", AVIO_FLAG_WRITE) < 0) {
//		 fprintf(stderr, "无法打开输出文件\n");
//		 return -1;
//	 }
//
//	 // 创建视频流
//	 videoStream = avformat_new_stream(outputFormatContext, nullptr);
//	 if (!videoStream) {
//		 fprintf(stderr, "无法创建视频流\n");
//		 return -1;
//	 }
//
//	 AVCodec* (*myf)(enum AVCodecID id);
//
//	 HMODULE avcodec58 = ::LoadLibrary(LR"(D:\Users\Downloads\project\st\Folder_online\noteBurner\ConsoleApplication2\Debug\avcodec-58.dll)");
//	 myf = (AVCodec * (*)(enum AVCodecID id))GetProcAddress(avcodec58, "avcodec_find_decoder");
//	 const AVCodec* testcodec  = myf(AV_CODEC_ID_H264);
//	 const AVCodec* decodec = avcodec_find_decoder(AV_CODEC_ID_VP9);
//	 const AVCodec* encodec = avcodec_find_decoder(AV_CODEC_ID_H264);
//	 decodecContext = avcodec_alloc_context3(decodec);
//	 encodecContext = avcodec_alloc_context3(encodec);
//	 encodecContext->codec_type = AVMediaType::AVMEDIA_TYPE_VIDEO;
//	 encodecContext->codec_id = AV_CODEC_ID_H264;
//	 encodecContext->pix_fmt = AV_PIX_FMT_YUV420P;
//	 encodecContext->width = 0x3c0;
//	 encodecContext->height = 0x21c;
//	 encodecContext->level = 0x1E;
//	 encodecContext->bit_rate = 0;
//	 encodecContext->framerate = AVRational{ 1, 0x18 };
//	 encodecContext->time_base = AVRational{1, 0x18};
//	encodecContext->sample_aspect_ratio = AVRational{ 1, 0x1 };
//
//	av_opt_set_int(encodecContext->priv_data, "crf", 0x16, 0);
//	 encodecContext->flags |= 0x400000;
//	 int enaocode = avcodec_open2(encodecContext, encodec, 0);
//
//	 if (enaocode < 0) {
//		 printf("avcodec_open2 encode failed \n");
//		 return 0;
//	 }
//	 int deaocode = avcodec_open2(decodecContext, decodec, 0);
//
//	 if (deaocode < 0) {
//		 printf("avcodec_open2 decode failed \n");
//		 return 0;
//	 }
//
//
//
//	 avcodec_parameters_from_context(videoStream->codecpar, encodecContext);
//	// av_dump_format(outputFormatContext, videoStream->id, "output.mp4", 1);
//	 //encode->init(0x3c0, 0x21c, 0x18, 0, (char *)"out.mp4");
//
//	
//
//	 // 写入文件头部信息
//	 avformat_write_header(outputFormatContext, NULL);
//
//	 while (!LinearReader.ReadNextSample(pTrack->GetId(), sample, sample_data)) {
//		
//			 
//		 
//	 }
//	 //encode->flush();
//	 //encode->uninit();
//	 // 写入文件尾部信息
//	 av_write_trailer(outputFormatContext);
//	 avcodec_free_context(&encodecContext);
//	 avcodec_free_context(&decodecContext);
//	 avformat_free_context(outputFormatContext);
//	 LinearReader.ReadNextSample(pTrack->GetId(), sample, sample_data);
//	 char ecryptBuffer[0x49d1] = {0,};
//	 ifstream inFile("MEM_11F971D8_000049D1.mem", ios::in | ios::binary); //二进制读方式打开
//	 if (!inFile) {
//		 cout << "error" << endl;
//		
//	 }
//	 while (inFile.read((char*)ecryptBuffer, sizeof(ecryptBuffer))) { //一直读到文件结束
//		 int readedBytes = inFile.gcount(); //看刚才读了多少字节
//		
//	 }
//	 inFile.close();
//
//	// LinearReader.ReadNextSample(pTrack->GetId(), sample, sample_data);
//	
//	return 0;
//}
//
//
//
//int __cdecl transToVideoProfile(char a1)
//{
//	int result; // eax
//
//	switch (a1)
//	{
//	case 66:
//		result = 2;
//		break;
//	case 77:
//		result = 3;
//		break;
//	case 88:
//		result = 4;
//		break;
//	case 100:
//		result = 5;
//		break;
//	case 110:
//		result = 6;
//		break;
//	case 122:
//		result = 7;
//		break;
//	case -112:
//		result = 8;
//		break;
//	default:
//		result = 0;
//		break;
//	}
//	return result;
//}

#include<iostream>

extern "C"
{
#include"libavutil\imgutils.h"
#include"libavutil\samplefmt.h"
#include"libavformat\avformat.h"
#include"libavutil\opt.h"
#include<libavformat/avformat.h>
#include<libswscale/swscale.h>
#include <libswresample/swresample.h>
}

char errorbuf[1024];

AVCodec* Encodec = NULL;  //编解码器1

AVCodecContext* Enc = NULL; //编码的

void SaveH264(AVPacket* packet)
{
	FILE* fpSave;
	if ((fpSave = fopen("BB.h264", "wb")) == NULL) //h264保存的文件名  
	{
		std::cout << "fopen  SaveH264 NO";
		return;
	}
	fwrite(packet->data, 1, packet->size, fpSave);//写数据到文件中  

	fclose(fpSave);
}

int  main()
{

	static int i = 0;


	av_register_all();

	avcodec_register_all();


	//fps每秒25帧
	int fps = 25;


	Encodec = avcodec_find_encoder(AV_CODEC_ID_H264);
	if (!Encodec)
	{

		printf("avcodec_find_encoder AV_CODEC_ID_H264 failed!\n");
		exit(0);
	}

	Enc = avcodec_alloc_context3(Encodec);
	if (!Enc)
	{

		printf("avcodec_alloc_context3  failed!\n");
		exit(0);
	}

	//设置编码器上下文参数
	Enc->width = 1920;
	Enc->height = 1080;
	Enc->bit_rate = 576000;
	AVRational r = { 1, 25 };//每秒25帧
	Enc->time_base = r;
	Enc->gop_size = 50;//GOP组
	Enc->max_b_frames = 1;
	Enc->pix_fmt = AV_PIX_FMT_YUV420P;//视频格式
	av_opt_set(Enc->priv_data, "preset", "ultrafast", 0);
	av_opt_set(Enc->priv_data, "tune", "stillimage,fastdecode,zerolatency", 0);
	av_opt_set(Enc->priv_data, "x264opts", "crf=26:vbv-maxrate=728:vbv-bufsize=364:keyint=25", 0);


	//Enc->flags |= AV_CODEC_FLAG_GLOBAL_HEADER;

	int ret = avcodec_open2(Enc, Encodec, NULL);
	if (ret < 0)
	{

		printf("avcodec_open2  failed!\n");
		exit(0);
	}
	printf("avcodec_open2 success!\n");


	AVFrame* pict = av_frame_alloc();

	FILE* fyuv = fopen("Out_fileTT.yuv", "rb");
	int nfilelen = (1920 * 1080 * 3) / 2;
	uint8_t* pbuf = new uint8_t[nfilelen];
	fread(pbuf, 1, nfilelen, fyuv);
	fclose(fyuv);

	int size = 1920 * 1080;

	pict->data[0] = pbuf;
	pict->data[1] = pict->data[0] + size;
	pict->data[2] = pict->data[1] + size / 4;
	pict->linesize[0] = 1920;
	pict->linesize[1] = 1920 / 2;
	pict->linesize[2] = 1920 / 2;

	pict->format = AV_PIX_FMT_YUV420P;
	pict->width = 1920;
	pict->height = 1080;

	clock_t start_time = clock();

	int p = 0;
	int Top = 1;
	while (Top != 0)
	{
		//6 encode frame
		pict->pts = p;

		p = p + 3600;

		Top = avcodec_send_frame(Enc, pict);
		if (Top != 0)
		{
			continue;
		}
		AVPacket Packetpkt;
		av_init_packet(&Packetpkt);


		Top = avcodec_receive_packet(Enc, &Packetpkt);
		if (Top != 0)
		{
			av_strerror(Top, errorbuf, sizeof(errorbuf));
			std::cout << "avcodec_receive_packet  NO ->" << errorbuf << Top << std::endl;
			std::cout << " Number :" << i << Top << std::endl;
			i++;
			continue;
		}



		SaveH264(&Packetpkt);

		//*********  Encodec Packetpkt  start   ***************
		std::cout << " Packetpkt size : " << Packetpkt.size << " " << std::endl;
		std::cout << " Packetpkt KB size : " << Packetpkt.size / 1024 << std::endl;
		std::cout << " Packetpkt data : " << Packetpkt.data << std::endl;
		std::cout << " Packetpkt pts  : " << Packetpkt.pts << std::endl;
		std::cout << " Packetpkt dts  : " << Packetpkt.dts << std::endl;


		//*********  Encodec Packetpkt  End   ***************



		clock_t end_time = clock();
		std::cout << "Codec Time: " << static_cast<double>(end_time - start_time) / CLOCKS_PER_SEC * 1000 << "ms" << std::endl;
		std::cout << " ********************* " << std::endl;



		av_packet_unref(&Packetpkt);
		std::cout << " ImageEnde  End " << std::endl;
	}


	av_free(pict);

	avcodec_close(Enc);
	avcodec_free_context(&Enc);

	return 0;
}