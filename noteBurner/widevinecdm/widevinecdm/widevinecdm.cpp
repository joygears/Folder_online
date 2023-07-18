// widevinecdm.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include <iostream>
#include <fstream>
#include <fstream>
#include "widevinecdm.h"
#include "fucntion.h"
#include "cdmHost.h"
#include "tool/base64.h"
#include "InlineHook.hpp"
#include "base64.h"
#include <bento4/Ap4.h>
#include "bento4/Ap4Atom.h"
#include <map>
#include "MyLinearReader.h"


bool (*VerifyCdmHost_0)(verifyWrap*, int flag);
void (*_InitializeCdmModule_4)();
void* (*_CreateCdmInstance)(int interface_version, const char* key_system, uint32_t key_system_len,
    void* host_function, void* extra_data);
void  (*_DeinitializeCdmModule)();
char* (*_GetCdmVersion)();
void* (*originHostFunction)(int host_version, void* user_data);
void* HostFunction(int host_version, void* user_data);

typedef DWORD(__stdcall* MyGetFileAttributes)(LPCWSTR lpFileName);
typedef DWORD(__stdcall* MyGetModuleFileName)(HMODULE hModule,LPWSTR  lpFilename,DWORD  nSize);
DWORD __stdcall  fake_GetModuleFileNameW(
    HMODULE hModule,
    LPWSTR  lpFilename,
    DWORD   nSize
);
DWORD __stdcall fake_GetFileAttributesW(LPCWSTR lpFileName);
hook::InlineHook GetFileAttributeshooker = hook::InlineHook();
hook::InlineHook GetModuleFileNamehooker = hook::InlineHook();

wstring dycVfchm;
string license;
string g_session_id;

AVCodecContext* decodecContext = 0;
AVCodecContext* encodecContext = 0;
AVStream* videoStream = 0;
AVFormatContext* outputFormatContext = 0;

 MyContentDecryptionModuleProxy* proxy = nullptr;
void initializeApp() {

    
   
   
    GetFileAttributeshooker.hook(::GetFileAttributesW, fake_GetFileAttributesW);
    GetModuleFileNamehooker.hook(::GetModuleFileNameW, fake_GetModuleFileNameW);

    wstring dycWidevine = TEXT(R"(.\..\..\sig_files\widevinecdm.dll)");
    wstring sigWidevine = TEXT(R"(.\..\..\sig_files\widevinecdm.dll.sig)");
    dycVfchm = TEXT(R"(.\..\..\sig_files\vfchm.dll)");
    wstring sigVfchm = TEXT(R"(.\..\..\sig_files\vfchm.dll.sig)");
    verifyWrap wrap;
   
   
    
    HANDLE HDycWidevinecdm = CreateFile(dycWidevine.c_str(), GENERIC_READ, 1, 0, 3, 0x80, 0);
    HANDLE HSigWidevinecdm = CreateFile(sigWidevine.c_str(), GENERIC_READ, 1, 0, 3, 0x80, 0);
    HANDLE hFVfchm = CreateFile(dycVfchm.c_str(), GENERIC_READ, 1, 0, 3, 0x80, 0);
    HANDLE hSigVfchm = CreateFile(sigVfchm.c_str(), GENERIC_READ, 1, 0, 3, 0x80, 0);

    Log("open file, %p, %p, %p, %p\n", HDycWidevinecdm, HSigWidevinecdm, hFVfchm, hSigVfchm);


    wrap.chDycVfchm = dycVfchm.c_str();
    wrap.hFVfchm = hFVfchm;
    wrap.hSigVfchm = hSigVfchm;
    wrap.chdycWidevine = dycWidevine.c_str();
    wrap.HDycWidevinecdm = HDycWidevinecdm;
    wrap.HSigWidevinecdm = HSigWidevinecdm;

    


    HMODULE hWidevine = LoadLibrary(dycWidevine.c_str());

    if(!hWidevine)
    Log("LoadLibrary widevinecdm.dll error  GetLasterror %d\n", GetLastError());
    
    VerifyCdmHost_0 = (bool (*)(verifyWrap*, int flag))GetProcAddress(hWidevine, "VerifyCdmHost_0");
    _InitializeCdmModule_4 = (void (*)())GetProcAddress(hWidevine, "InitializeCdmModule_4");
    _CreateCdmInstance = (void* (*)(int interface_version, const char* key_system, uint32_t key_system_len,
            void* host_function, void* extra_data))GetProcAddress(hWidevine, "CreateCdmInstance");
    _DeinitializeCdmModule = (void (*)())GetProcAddress(hWidevine, "DeinitializeCdmModule");
    _GetCdmVersion = (char * (*)())GetProcAddress(hWidevine, "GetCdmVersion");

    Log("load widevinecdm success, %p, %p, %p, %p \n", _InitializeCdmModule_4, _CreateCdmInstance, _DeinitializeCdmModule, _GetCdmVersion);

    bool retcode = VerifyCdmHost_0(&wrap, 2);

    Log("widevine VerifyCdmHost_0 retcode value %d\n",retcode);
}




int main()
{
    string input_file = "all.mp4";
    string cert = "Cr0CCAMSEOVEukALwQ8307Y2+LVP+0MYh/HPkwUijgIwggEKAoIBAQDm875btoWUbGqQD8eAGuBlGY+Pxo8YF1LQR+Ex0pDONMet8EHslcZRBKNQ/09RZFTP0vrYimyYiBmk9GG+S0wB3CRITgweNE15cD33MQYyS3zpBd4z+sCJam2+jj1ZA4uijE2dxGC+gRBRnw9WoPyw7D8RuhGSJ95OEtzg3Ho+mEsxuE5xg9LM4+Zuro/9msz2bFgJUjQUVHo5j+k4qLWu4ObugFmc9DLIAohL58UR5k0XnvizulOHbMMxdzna9lwTw/4SALadEV/CZXBmswUtBgATDKNqjXwokohncpdsWSauH6vfS6FXwizQoZJ9TdjSGC60rUB2t+aYDm74cIuxAgMBAAE6EHRlc3QubmV0ZmxpeC5jb20SgAOE0y8yWw2Win6M2/bw7+aqVuQPwzS/YG5ySYvwCGQd0Dltr3hpik98WijUODUr6PxMn1ZYXOLo3eED6xYGM7Riza8XskRdCfF8xjj7L7/THPbixyn4mULsttSmWFhexzXnSeKqQHuoKmerqu0nu39iW3pcxDV/K7E6aaSr5ID0SCi7KRcL9BCUCz1g9c43sNj46BhMCWJSm0mx1XFDcoKZWhpj5FAgU4Q4e6f+S8eX39nf6D6SJRb4ap7Znzn7preIvmS93xWjm75I6UBVQGo6pn4qWNCgLYlGGCQCUm5tg566j+/g5jvYZkTJvbiZFwtjMW5njbSRwB3W4CrKoyxw4qsJNSaZRTKAvSjTKdqVDXV/U5HK7SaBA6iJ981/aforXbd2vZlRXO/2S+Maa2mHULzsD+S5l4/YGpSt7PnkCe25F+nAovtl/ogZgjMeEdFyd/9YMYjOS4krYmwp3yJ7m9ZzYCQ6I8RQN4x/yLlHG5RH/+WNLNUs6JAZ0fFdCmw=";
    string pssh = "AAAANHBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAABQIARIQAAAAAAZulPgAAAAAAAAAAA==";
    cert = base64_decode(cert);
    pssh = base64_decode(pssh);
  /*  VideoDecoderConfig video_decoder_config;
    video_decoder_config.codec = 2;
    video_decoder_config.profile = 5;
    video_decoder_config.alpha_mode = 2;
    video_decoder_config.color_space = 0;
    video_decoder_config.width = 0x3c0;
    video_decoder_config.height = 0x21c;
    video_decoder_config.m_18 = 0;
    video_decoder_config.m_1C = 0;
    video_decoder_config.m_20 = 0xF;

    char video_decoder_config[] = { 0x03,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0x03,0x00,0x00,0x1C,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x0F,0x00,0x00,0x00 };
    */


    AP4_ByteStream* input_stream = NULL;
    AP4_Result result = AP4_FileByteStream::Create(input_file.c_str(),
        AP4_FileByteStream::STREAM_MODE_READ,
        input_stream);

    if (result != AP4_SUCCESS || input_stream == nullptr) {
        // 处理文件打开错误
        return result;
    }
    AP4_File file(*input_stream);
    AP4_Movie* movie = file.GetMovie();

    
    //获取ProtectedSampleDescription
    AP4_Cardinal track_count = movie->GetTracks().ItemCount();
    if (!track_count)
        return 1600;
    AP4_ProtectedSampleDescription* ProtectedSampleDescription;
    AP4_Track* pTrack;
    while (1) {

        AP4_List<AP4_Track>::Item* item = movie->GetTracks().FirstItem();
        pTrack = item->GetData();
        if (!pTrack)
            return 1600;
        AP4_SampleDescription* SampleDescription = pTrack->GetSampleDescription(0);
        if (SampleDescription && SampleDescription->GetType() != AP4_SampleDescription::Type::TYPE_PROTECTED) {
            //处理未加密的track流
        }
        else {
            ProtectedSampleDescription = dynamic_cast<AP4_ProtectedSampleDescription*>(SampleDescription);
            if (ProtectedSampleDescription)
                break;
        }
    }
    AP4_UI32 schemeType = ProtectedSampleDescription->GetSchemeType();
    if (schemeType == 0x63656E63
        || schemeType == 0x63626331
        || schemeType == 0x63656E73
        || schemeType == 0x63626373
        || schemeType == 0x70696666)
    {
        printf("protection scheme type: %u\n", schemeType);
    }
    else
    {
        printf("unhandled protection scheme type: %u\n", schemeType);
    }


    //配置video_decoder_config
    VideoDecoderConfig video_decoder_config{ 0 };
    AP4_SampleDescription* OriginalSampleDescription = ProtectedSampleDescription->GetOriginalSampleDescription();
    char* format;
    AP4_String codec;
    if (OriginalSampleDescription) {
        format = (char*)AP4_GetFormatName(OriginalSampleDescription->GetFormat());
        OriginalSampleDescription->GetCodecString(codec);

        printf("format:%s, codec:%s, type:%d \n", format, codec.GetChars(), OriginalSampleDescription->GetType());
    }
    AP4_UI16 width;
    AP4_UI16 height;
    AP4_Atom::Type trackType = pTrack->GetType();
    if (trackType != AP4_Track::TYPE_AUDIO) {
        if (trackType != AP4_Track::TYPE_VIDEO)
            return 1600;
        AP4_VideoSampleDescription* VideoSampleDescription = dynamic_cast<AP4_VideoSampleDescription*>(OriginalSampleDescription);
         width = VideoSampleDescription->GetWidth();
         height = VideoSampleDescription->GetHeight();
        std::string codecStr = codec.GetChars();
        video_decoder_config.width = width;
        video_decoder_config.height = height;
        video_decoder_config.m_18 = 0;
        video_decoder_config.m_1C = 0;
        if (codecStr.find("av", 0) == std::string::npos) {

            if (codecStr.find("vp09", 0) == std::string::npos)
                printf("codec %s not yet handled ", codecStr.c_str());
            video_decoder_config.profile = 1;
            video_decoder_config.codec = 3;


        }
        else {
            AP4_AvcSampleDescription* AvcSampleDescription = dynamic_cast<AP4_AvcSampleDescription*>(OriginalSampleDescription);
            AP4_UI08 profile = AvcSampleDescription->GetProfile();
            AP4_UI08 level = AvcSampleDescription->GetLevel();
            int videoProfile = transToVideoProfile(profile);

            video_decoder_config.codec = 2;
            video_decoder_config.profile = videoProfile;

        }
        video_decoder_config.alpha_mode = 2;
    }


    initializeApp();
   InitializeCdmModule_4();
    string key_system("com.widevine.alpha");
  proxy = (MyContentDecryptionModuleProxy*)CreateCdmInstance(10, key_system.c_str(), key_system.size(), HostFunction, 0);
   proxy->Initialize(0, 0, 0);
   proxy->SetServerCertificate(1, (const UINT8*)cert.c_str(), cert.size());
   proxy->CreateSessionAndGenerateRequest(1, 0, 0, (const UINT8*)pssh.c_str(), pssh.size());
    license = base64_decode(license);
    proxy->UpdateSession(1, g_session_id.c_str(), g_session_id.size(), (uint8_t*)license.c_str(), license.size());
   proxy->InitializeVideoDecoder(&video_decoder_config);



   

       AP4_ByteStream* input_stream3 = NULL;
       result = AP4_FileByteStream::Create(input_file.c_str(),
           AP4_FileByteStream::STREAM_MODE_READ,
           input_stream3);
       AP4_Sample sample;
       AP4_DataBuffer sample_data;

       MyLinearReader LinearReader(*movie, input_stream3);
       LinearReader.EnableTrack(pTrack->GetId());
       AP4_ByteStream* m_FragmentStream = *(AP4_ByteStream**)(((char*)&LinearReader) + 0x14);
       AP4_Atom* pAtom;
       AP4_AtomFactory factory2;
       factory2.CreateAtomFromStream(*m_FragmentStream, pAtom);
       AP4_ContainerAtom* moov = dynamic_cast<AP4_ContainerAtom*>(pAtom);
      

       avformat_alloc_output_context2(&outputFormatContext, NULL, NULL, "tmp.mp4");

       // 打开输出文件
       if (avio_open(&outputFormatContext->pb, "tmp.mp4", AVIO_FLAG_WRITE) < 0) {
           fprintf(stderr, "无法打开输出文件\n");
           return -1;
       }

       // 创建视频流
       videoStream = avformat_new_stream(outputFormatContext, nullptr);
       if (!videoStream) {
           fprintf(stderr, "无法创建视频流\n");
           return -1;
       }

       //获取sample_aspect_ratio
       AVFormatContext* Formatcontext = 0;
       int result1 = avformat_open_input(&Formatcontext, input_file.c_str(), 0, 0);
       int result2 = avformat_find_stream_info(Formatcontext, 0);
       AVStream* stream = Formatcontext->streams[0];
       AVRational sample_aspect_ratio = av_guess_sample_aspect_ratio(Formatcontext, stream, 0);
       int64_t bit_rate = Formatcontext->bit_rate;
       if (sample_aspect_ratio.den == 0 || sample_aspect_ratio.num == 0) {
           sample_aspect_ratio = AVRational{ 1, 0x1 }; // 从licensedMainfest获取
       }
      
       const AVCodec* decodec = avcodec_find_decoder(stream->codecpar->codec_id);
       const AVCodec* encodec = avcodec_find_encoder(AV_CODEC_ID_H264);
       decodecContext = avcodec_alloc_context3(decodec);
       encodecContext = avcodec_alloc_context3(encodec);
       if (encodecContext) {
           encodecContext->codec_type = AVMediaType::AVMEDIA_TYPE_VIDEO;
           encodecContext->codec_id = encodec->id;
           encodecContext->pix_fmt = *encodec->pix_fmts;

           encodecContext->width = width;
           encodecContext->height = height;

           encodecContext->level = 0x1E;

           encodecContext->framerate = AVRational{ 1, stream->avg_frame_rate.num };
           encodecContext->time_base = AVRational{ 1, stream->avg_frame_rate.num };
           encodecContext->sample_aspect_ratio = sample_aspect_ratio;
           auto getQualityFromBitrate = [](int64_t bitrate)->int {
               if ((bitrate & 0x8000000000000000ui64) == 0i64)
               {
                   if (*((int*)(&bitrate) + 1) > 0)
                       return 4;
                   if ((unsigned int)bitrate >= 0x16E360)
                   {
                       if ((unsigned int)bitrate < 0x2625A0)
                           return 1;
                       if ((unsigned int)bitrate < 0x3D0900)
                           return 2;
                       if ((unsigned int)bitrate < 0x5B8D80)
                           return 3;
                       return 4;
                   }
               }
               return 0;
           };

           int64_t val = 22 - getQualityFromBitrate(bit_rate);
           av_opt_set_int(encodecContext->priv_data, "crf", val, 0);

           if ((*(char*)&outputFormatContext->oformat->flags & 0x40) != 0)
               encodecContext->flags |= 0x400000;
       }
     
       int enaocode = avcodec_open2(encodecContext, encodec, 0);

       if (enaocode < 0) {
           printf("avcodec_open2 encode failed \n");
           return 0;
       }
      
       int deaocode = avcodec_open2(decodecContext, decodec, 0);
      
       if (deaocode < 0) {
           printf("avcodec_open2 decode failed \n");
           return 0;
       }

      

       avcodec_parameters_from_context(videoStream->codecpar, encodecContext);
       // av_dump_format(outputFormatContext, videoStream->id, "output.mp4", 1);



       
        // 写入文件头部信息
       avformat_write_header(outputFormatContext, NULL);
       while (!LinearReader.ReadNextSample(pTrack->GetId(), sample, sample_data)) {



            }

       // 写入文件尾部信息
       av_write_trailer(outputFormatContext);
       avcodec_free_context(&encodecContext);
       avcodec_free_context(&decodecContext);
       avformat_free_context(outputFormatContext);

       printf("\nall frame decrypted");


//    char ecryptBuffer[0x49d1] = { 0, };
//    ifstream inFile("MEM_11F971D8_000049D1.mem", ios::in | ios::binary); //二进制读方式打开
//    if (!inFile) {
//        cout << "error" << endl;
//        return 0;
//    }
//    while (inFile.read((char*)ecryptBuffer, sizeof(ecryptBuffer))) { //一直读到文件结束
//        int readedBytes = inFile.gcount(); //看刚才读了多少字节
//       
//    }
//    inFile.close();
//    char key_id[] = {
//        0x00, 0x00, 0x00, 0x00, 0x05, 0x6F, 0x60, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
//    };
//    unsigned char iv[] = {
//0x01, 0xAC, 0x60, 0x6C, 0x64, 0x88, 0x37, 0xBE
//    };
//    
//    SubsampleEntry subsamples[1];
//    subsamples->clear_bytes = 0x21;
//    subsamples->cipher_bytes = 0x49b0;
//
//    InputBuffer_2 input;
//    input.data = (uint8_t *)ecryptBuffer;
//    input.data_size = 0x49d1;
//    input.encryption_scheme = EncryptionScheme::kCenc;
//    input.key_id = (uint8_t*)key_id;
//    input.key_id_size = 0x10;
//    input.iv = iv;
//    input.iv_size = 0x8;
//    input.subsamples = subsamples;
//    input.num_subsamples = 1;
//    input.pattern.crypt_byte_block = 0;
//    input.pattern.skip_byte_block = 0;
//    input.timestamp = 0x073A393;
//    MyVideoFrame videoFrame;
//    MyVideoFrame* video_frame = &videoFrame;
//   int result = proxy->DecryptAndDecodeFrame(&input, &videoFrame);
//    Log("DecryptAndDecodeFrame result %d", result);
//    cout << "width * height:" << videoFrame.SSize().width  << "*" << videoFrame.SSize().height << endl;
//    cout << "videoFrame.m_format : " << videoFrame.Format() << endl;
//    cout << "Timestamp : " << videoFrame.Timestamp() << endl;
//    for (int i = 0; i < VideoFrame::VideoPlane::kMaxPlanes; i++) {
//        cout << "videoFrame.PlaneOffset((VideoFrame::VideoPlane)"<<i<<")" << videoFrame.PlaneOffset((VideoFrame::VideoPlane)i) << endl;
//        cout << "videoFrame.Stride((VideoFrame::VideoPlane)" << i << ")" << videoFrame.Stride((VideoFrame::VideoPlane)i) << endl;
//   }
//    FILE* pVideo;
//    pVideo = fopen("frame.yuv", "wb");
//    unsigned char* buffer=NULL;
//    transtoYUV(video_frame, buffer);
//    fwrite(buffer, 1, video_frame->SSize().width * video_frame->SSize().height * 1.5, pVideo);
//    fclose(pVideo);
    return 0;

}
//#include <ctime>
//
//int main() {
//    
//   unsigned __int64 b = 4744864539823046656;
//   __int64 timestamp = (__int64)*(double *)&b;
//    
//    struct tm* timeinfo = _gmtime64(&timestamp);
//    int a = GetLastError();
//    char buffer[80];
//    printf("%f", b);
//
//    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", timeinfo);
//    std::cout << "Converted timestamp: " << buffer << std::endl;
//
//    return 0;
//}
//


void* HostFunction(int host_version, void* user_data)
{
    Log("GetCdmHost called, version %d, user_data %p", host_version, (const void*)user_data);
    g_CDMHost = new cdmHost(0);
    Log("new CDMHost %p", g_CDMHost);
    return g_CDMHost;
}

DLL_EXPORT void InitializeCdmModule_4()
{
    Log("InitializeCdmModule_4\n");
    _InitializeCdmModule_4();
}

DLL_EXPORT void* CreateCdmInstance(int interface_version, const char* key_system, uint32_t key_system_len, void* host_function, void* extra_data)
{
    Log("CreateCdmInstance %d, %s, %lld, \n", interface_version, key_system, key_system_len);

    originHostFunction = (void* (*)(int host_version, void* user_data))host_function;

    void* instance = _CreateCdmInstance(interface_version, key_system, key_system_len, HostFunction, extra_data);
    if (!instance)
    {
        Log("no origin instance created\n");
        return nullptr;
    }
    Log("module version, %d", interface_version);

    if (interface_version != 10)
    {
        Log("unhandled version, %d", interface_version);
        return instance;
    }

    MyContentDecryptionModuleProxy* proxy = new MyContentDecryptionModuleProxy(static_cast<ContentDecryptionModule_10*>(instance));
    proxy->setHost(g_CDMHost);
    return proxy;
}

DLL_EXPORT void DeinitializeCdmModule()
{
    Log("DeinitializeCdmModule\n");
    _DeinitializeCdmModule();
}

DLL_EXPORT char* GetCdmVersion()
{
    return _GetCdmVersion();
}


BOOL WINAPI DllMain(
    HINSTANCE hinstDLL,  // handle to DLL module
    DWORD fdwReason,     // reason for calling function
    LPVOID lpvReserved)  // reserved
{
    // Perform actions based on the reason for calling.
    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        // Initialize once for each new process.
        // Return FALSE to fail DLL load.
        DisableThreadLibraryCalls((HMODULE)hinstDLL);
        initializeApp();
        break;

    case DLL_THREAD_ATTACH:
        // Do thread-specific initialization.
        break;

    case DLL_THREAD_DETACH:
        // Do thread-specific cleanup.
        break;

    case DLL_PROCESS_DETACH:

        if (lpvReserved != nullptr)
        {
            break; // do not do cleanup if process termination scenario
        }

        // Perform any necessary cleanup.
        break;
    }
    return TRUE;  // Successful DLL_PROCESS_ATTACH.
}

void MyContentDecryptionModuleProxy::Initialize(bool allow_distinctive_identifier, bool allow_persistent_state, bool flag)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 76);
        return;
    }
   
    Log("init module(%p), %d, %d, %d", this, allow_distinctive_identifier, allow_persistent_state, flag);

    m_instance->Initialize(allow_distinctive_identifier, allow_persistent_state, flag);
    allow_distinctive_identifier = 1;
    this->GetStatusForPolicy(-1, (int *)&allow_distinctive_identifier);
}

void MyContentDecryptionModuleProxy::GetStatusForPolicy(uint32_t promise_id, int* policy)
{
    Log("module(%p) GetStatusForPolicy", this);
    
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
   
    string aGetstatusforpo = "GetStatusForPolicy_";

    switch (*policy) {
    case 0:
        aGetstatusforpo.append("HDCP_None");
        break;
    case 1:
        aGetstatusforpo.append("HDCP_1_0");
        break;
    case 2:
        aGetstatusforpo.append("HDCP_1_1");
        break;
    case 3:
        aGetstatusforpo.append("HDCP_1_2");
        break;
    case 4:
        aGetstatusforpo.append("HDCP_1_3");
        break;
    case 5:
        aGetstatusforpo.append("HDCP_1_4");
        break;
    case 6:
        aGetstatusforpo.append("HDCP_2_0");
        break;
    case 7:
        aGetstatusforpo.append("HDCP_2_1");
        break;
    case 8:
        aGetstatusforpo.append("HDCP_2_2");
        break;
    case 9:
        aGetstatusforpo.append("HDCP_2_3");
        break;
    default:
        aGetstatusforpo.append("HDCP_Unknown", 12);
        break;

    };

    
    m_host->setMapIdHdcp(promise_id, aGetstatusforpo);

    m_instance->GetStatusForPolicy(promise_id, policy);

}

void MyContentDecryptionModuleProxy::SetServerCertificate(uint32_t promise_id, const uint8_t* server_certificate_data, uint32_t server_certificate_data_size)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    string strCertificateData((const char *)server_certificate_data, server_certificate_data_size);
    string base64Data = base64_encode(strCertificateData);
    Log("SetServerCertificate(%p): %d",this, base64Data.size());
    m_d4 = string("Set", 3);
    m_baseServerCertificate = base64Data;
    m_instance->SetServerCertificate(promise_id, server_certificate_data, server_certificate_data_size);
}

void MyContentDecryptionModuleProxy::CreateSessionAndGenerateRequest(uint32_t promise_id, int session_type, int init_data_type, const uint8_t* init_data, uint32_t init_data_size)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("CreateSessionAndGenerateRequest(%p)", this);

    m_instance->CreateSessionAndGenerateRequest(promise_id, session_type, init_data_type, init_data, init_data_size);

}

void MyContentDecryptionModuleProxy::LoadSession(uint32_t promise_id, int session_type, const char* session_id, uint32_t session_id_size)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("LoadSession(%p):", (const void*)this);
    m_instance->LoadSession(promise_id, session_type, session_id, session_id_size);

}

void MyContentDecryptionModuleProxy::UpdateSession(uint32_t promise_id, const char* session_id, uint32_t session_id_size, const uint8_t* response, uint32_t response_size)
{
    
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("UpdateSession(%p):", (const void*)this);
    m_instance->UpdateSession(promise_id, session_id, session_id_size, response, response_size);
}

void MyContentDecryptionModuleProxy::CloseSession(uint32_t promise_id, const char* session_id, uint32_t session_id_size)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("CloseSession(%p):", (const void*)this);
    m_instance->CloseSession(promise_id, session_id, session_id_size);
}

void MyContentDecryptionModuleProxy::RemoveSession(uint32_t promise_id, const char* session_id, uint32_t session_id_size)
{

    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("RemoveSession(%p):", (const void*)this);
    m_instance->RemoveSession(promise_id, session_id, session_id_size);
}

void MyContentDecryptionModuleProxy::TimerExpired(void* context)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
       
    }
    Log("TimerExpired(%p):", (const void*)this);
    m_instance->TimerExpired(context);
}

int MyContentDecryptionModuleProxy::Decrypt(void* encrypted_buffer, DecryptedBlock * decrypted_buffer)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return 0;
    }
    Log("Decrypt(%p):", (const void*)this);

    //int status    = m_instance->Decrypt(encrypted_buffer, decrypted_buffer);
    //if (mDecFile == NULL)
    //{
    //    mDecFile = fopen("d:\\cdm_dec.bin", "wb");
    //}
    //if (mDecFile != NULL)
    //{
    //    fwrite(decrypted_buffer->DecryptedBuffer()->Data(), 1,
    //        decrypted_buffer->DecryptedBuffer()->Size(), mDecFile);
    //    Log("Decrypt data size %d:", decrypted_buffer->DecryptedBuffer()->Size());
    //}
    return 1;
}

int MyContentDecryptionModuleProxy::InitializeAudioDecoder(void* audio_decoder_config)
{

    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return 0;
    }
    Log("InitializeAudioDecoder(%p):", (const void*)this);
   
    return  m_instance->InitializeAudioDecoder(audio_decoder_config);
}

int MyContentDecryptionModuleProxy::InitializeVideoDecoder(void* video_decoder_config)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return 0;
    }
    Log("InitializeVideoDecoder(%p):", (const void*)this);

    return  m_instance->InitializeVideoDecoder(video_decoder_config);
}

void MyContentDecryptionModuleProxy::DeinitializeDecoder(int decoder_type)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("DeinitializeDecoder(%p):", (const void*)this);
    m_instance->DeinitializeDecoder(decoder_type);
}

void MyContentDecryptionModuleProxy::ResetDecoder(int decoder_type)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("ResetDecoder(%p):", (const void*)this);
    m_instance->ResetDecoder(decoder_type);
}

int MyContentDecryptionModuleProxy::DecryptAndDecodeFrame(const void* encrypted_buffer, void* video_frame)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return 0;
    }
    Log("DecryptAndDecodeFrame(%p):", (const void*)this);




    return  m_instance->DecryptAndDecodeFrame(encrypted_buffer, video_frame);

}

int MyContentDecryptionModuleProxy::DecryptAndDecodeSamples(void* encrypted_buffer, void* audio_frames)
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return 0;
    }
    Log("DecryptAndDecodeSamples(%p):", (const void*)this);

    return  m_instance->DecryptAndDecodeSamples(encrypted_buffer, audio_frames);
 
}

void MyContentDecryptionModuleProxy::OnPlatformChallengeResponse(void* response)
{

    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("OnPlatformChallengeResponse(%p):", (const void*)this);
    
    m_instance->OnPlatformChallengeResponse(response);
}

void MyContentDecryptionModuleProxy::OnQueryOutputProtectionStatus(int result, uint32_t link_mask, uint32_t output_protection_mask)
{

    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("OnQueryOutputProtectionStatus, %u, %u, %u", result, link_mask, output_protection_mask);
    if (result)
    {
        Log("QueryOutputProtectionStatus failed");
    }
    else {
        Log("output_link_type: %s", getLink_maskMean(link_mask).c_str());
        Log( "output_protection: %s", getOutput_protection_mean(output_protection_mask).c_str());
    }
    m_instance->OnQueryOutputProtectionStatus(result, link_mask, output_protection_mask);
}

void MyContentDecryptionModuleProxy::OnStorageId(uint32_t version, const uint8_t* storage_id, uint32_t storage_id_size)
{

    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("OnStorageId(%p):", (const void*)this);

    m_instance->OnStorageId(version, storage_id, storage_id_size);
}

void MyContentDecryptionModuleProxy::Destroy()
{
    if (!m_instance)
    {
        Log("instance is null, %d", 96);
        return;
    }
    Log("Destroy(%p):", (const void*)this);
    if(mDecFile!=NULL)
        fclose(mDecFile);
    mDecFile = NULL;

    m_instance->Destroy();
}

std::string MyContentDecryptionModuleProxy::getLink_maskMean(int link_mask)
{
    string result;
    switch (link_mask)
    {
    case 0:
        result = "None";
        break;
    case 1:
        result = "Unknown";

        break;
    case 2:
        result = "Internal";

        break;
    case 4:
        result = "VGA";
        
        break;
    case 8:
        result = "HDMI";
       
        break;
    case 16:
        result = "DVI";
        
        break;
    case 32:
        result = "DisplayPort";
       
        break;
    case 64:
        result = "Network";
       
        break;
    default:
        result = "Unknown";
        break;
    }
    
    return result;
}

std::string MyContentDecryptionModuleProxy::getOutput_protection_mean(int output_protection_mask)
{
    return output_protection_mask == 1 ? "HDCP" : "None";
}

void MyContentDecryptionModuleProxy::setHost(cdmHost * host)
{
    Log("module SetHost(%p)", host);
    m_host = host;
    if (m_host)
    {
        m_host->m_MyProxy = this;
    }
}

MyContentDecryptionModuleProxy::MyContentDecryptionModuleProxy(ContentDecryptionModule_10* instance) :m_instance(instance) {
    g_mtx.lock();
    g_listInstance.push_back(this);
    Log("construct module, count: %d", g_listInstance.size());
    g_mtx.unlock();
}

MyContentDecryptionModuleProxy::~MyContentDecryptionModuleProxy()
{
    g_mtx.lock();
    for (std::list<MyContentDecryptionModuleProxy*>::iterator it = g_listInstance.begin(); it != g_listInstance.end(); ++it) {
        if (*it == this)
            g_listInstance.erase(it);
    }
    Log( "destruct module. Remained count: %d", g_listInstance.size());

    g_mtx.unlock();
}

void DecryptedProxyBlock::SetDecryptedBuffer(Buffer* buffer) {
    buf = buffer;
}
Buffer* DecryptedProxyBlock::DecryptedBuffer() {
    return buf;
}

void DecryptedProxyBlock::SetTimestamp(int64_t timestamp) {
    ts = timestamp;
}

int64_t DecryptedProxyBlock::Timestamp() const {
    return ts;
}

std::mutex MyContentDecryptionModuleProxy::g_mtx;
std::list< MyContentDecryptionModuleProxy*> MyContentDecryptionModuleProxy::g_listInstance;



DWORD __stdcall fake_GetFileAttributesW(LPCWSTR lpFileName) {
    if (lpFileName)
        Log("GetFileAttributesW called, file %S", lpFileName);
    
    if (wcsstr(lpFileName, TEXT("cshell.dll"))==0 && wcsstr(lpFileName, TEXT("decrypt.dll"))==0 && wcsstr(lpFileName, TEXT("widevinecdm.dll"))==0) {
       return  ((MyGetFileAttributes)GetFileAttributeshooker.originalFunction())(lpFileName);
    }
    Log("GetFileAttributesW called, file %S, %08x", lpFileName, ((MyGetFileAttributes)GetFileAttributeshooker.originalFunction())(lpFileName));

    return 0x80;
}

DWORD __stdcall  fake_GetModuleFileNameW(
    HMODULE hModule,
    LPWSTR  lpFilename,
    DWORD   nSize
) {
    wchar_t absolutePath[MAX_PATH];
     GetFullPathName(dycVfchm.c_str(), MAX_PATH, absolutePath, nullptr);

    DWORD result = ((MyGetModuleFileName)GetModuleFileNamehooker.originalFunction())(hModule, lpFilename, nSize);
    if (result) {
        wstring originFileName = lpFilename;
        
        if (wcsstr(lpFilename, L"")) {
            Log("GetModuleFileNameW called, hook %S to %S", originFileName.c_str(), absolutePath);
            wcscpy(lpFilename, absolutePath);
        }
    }
    return result;
}

void MyVideoFrame::SetFormat(VideoFormat format)
{
    m_format = format;
}

VideoFormat MyVideoFrame::Format() const
{
    return m_format;
}

void MyVideoFrame::SetSize(Size size)
{
    m_size = size;
}

Size MyVideoFrame::SSize() const
{
    return m_size;
}

void MyVideoFrame::SetFrameBuffer(Buffer* frame_buffer)
{
    m_frame_buffer = frame_buffer;
}

Buffer* MyVideoFrame::FrameBuffer()
{
    return m_frame_buffer;
}

void MyVideoFrame::SetPlaneOffset(VideoPlane plane, uint32_t offset)
{
    m_planeOffsets[plane] = offset;
}

uint32_t MyVideoFrame::PlaneOffset(VideoPlane plane)
{
    return m_planeOffsets[plane];
}

void MyVideoFrame::SetStride(VideoPlane plane, uint32_t stride)
{
    m_stride[plane] = stride;
}

uint32_t MyVideoFrame::Stride(VideoPlane plane)
{
    return m_stride[plane];
}

void MyVideoFrame::SetTimestamp(int64_t timestamp)
{
    m_timestamp = timestamp;
}

int64_t MyVideoFrame::Timestamp() const
{
    return m_timestamp;
}


void transtoYUV(MyVideoFrame* video_frame, unsigned char*& buffer) {
    uint32_t c = video_frame->SSize().width * video_frame->SSize().height;
    if (buffer == NULL)
        buffer = (unsigned char*)malloc(video_frame->SSize().width * video_frame->SSize().height * 1.5);
    //Y Plane
    uint32_t offset = 0;
    for (int i = 0; i < video_frame->SSize().height; i++) {
        memcpy(buffer + video_frame->SSize().width * i, video_frame->FrameBuffer()->Data() + offset, video_frame->SSize().width);
        offset += video_frame->Stride(VideoFrame::kYPlane);
    }
    //U Plane
    offset = 0;
    for (int i = 0; i < video_frame->SSize().height / 2; i++) {
        memcpy(buffer + c + (video_frame->SSize().width / 2) * i, video_frame->FrameBuffer()->Data() + video_frame->PlaneOffset(VideoFrame::kUPlane) + offset, video_frame->SSize().width / 2);
        offset += video_frame->Stride(VideoFrame::kUPlane);
    }
    //V Plane
    offset = 0;
    for (int i = 0; i < video_frame->SSize().height / 2; i++) {
        memcpy(buffer + c + (c / 4) + (video_frame->SSize().width / 2) * i, video_frame->FrameBuffer()->Data() + video_frame->PlaneOffset(VideoFrame::kVPlane) + offset, video_frame->SSize().width / 2);
        offset += video_frame->Stride(VideoFrame::kVPlane);
    }
};