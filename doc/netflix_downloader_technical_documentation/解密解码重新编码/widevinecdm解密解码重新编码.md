## `widevinecdm`解密解码重新编码

### 初始化视频解码器

在解密之前需要初始化视频解码器

~~~c++
int MyContentDecryptionModuleProxy::InitializeVideoDecoder(VideoDecoderConfig* config)
~~~

下面是`VideoDecoderConfig`的定义

~~~c++
 struct VideoDecoderConfig_2 {
    VideoCodec codec;
    VideoCodecProfile profile;
    VideoFormat format;
    uint32_t : 32;  // Padding.

                    
    Size coded_size;

   	// Optional byte data required to initialize video decoders, such as H.264
     // AAVC data.
    uint8_t* extra_data;
    uint32_t extra_data_size;

    // Encryption scheme.
    EncryptionScheme encryption_scheme;
  };
~~~

+ `VideoCodec codec`

  视频的编码类型

  ~~~c++
  enum VideoCodec : uint32_t {
      kUnknownVideoCodec = 0,
      kCodecVp8,
      kCodecH264,
      kCodecVp9,
      kCodecAv1
    };
  ~~~

  这个该如何获取呢

  可以使用`bento4`这个库

  `AP4_SampleDescription::GetCodecString()`: 获取样本描述的编解码器字符串。

  

- `VideoCodecProfile profile`

  视频的质量

  ~~~c++
    enum VideoCodecProfile : uint32_t {
      kUnknownVideoCodecProfile = 0,
      kProfileNotNeeded,
      kH264ProfileBaseline,
      kH264ProfileMain,
      kH264ProfileExtended,
      kH264ProfileHigh,
      kH264ProfileHigh10,
      kH264ProfileHigh422,
      kH264ProfileHigh444Predictive,
      // VP9 Profiles are only passed in starting from CDM_9.
      kVP9Profile0,
      kVP9Profile1,
      kVP9Profile2,
      kVP9Profile3,
      kAv1ProfileMain,
      kAv1ProfileHigh,
      kAv1ProfilePro
    };
  ~~~
  
  ~~~mermaid
  graph TD;
      start[开始] --> input[输入编码类型];
      input -- vp9 --> process_vp9{处理VP9};
      input -- avc --> process_avc{处理AVC};
      input -- av1 --> process_av1{处理AV1};
      
      process_vp9 --> profile1[设置profile为1];
      
      process_avc --> get_profile[调用AP4_AvcSampleDescription::GetProfile];
      get_profile --> transToVideoProfile[调用transToVideoProfile转换profile];
      transToVideoProfile --> set_profile[设置profile];
      
      process_av1 --> get_av1_profile[调用AP4_Av1SampleDescription::GetSeqProfile + 13];
      get_av1_profile --> set_av1_profile[设置profile];
      
    	profile1 --> endl[结束];
      set_profile --> endl;
      set_av1_profile --> endl;
  
     
  
  ~~~

~~~c++
int __cdecl transToVideoProfile(char a1)
{
    int result; // eax

    switch (a1)
    {
    case 66:
        result = 2;
        break;
    case 77:
        result = 3;
        break;
    case 88:
        result = 4;
        break;
    case 100:
        result = 5;
        break;
    case 110:
        result = 6;
        break;
    case 122:
        result = 7;
        break;
    case -112:
        result = 8;
        break;
    default:
        result = 0;
        break;
    }
    return result;
}
~~~

+ `VideoFormat format`

  裸流的编码

  ~~~c++
  enum VideoFormat : uint32_t {
      kUnknownVideoFormat = 0,  // Unknown format value. Used for error reporting.
      kYv12 = 1,                // 12bpp YVU planar 1x1 Y, 2x2 VU samples.
      kI420 = 2,                // 12bpp YUV planar 1x1 Y, 2x2 UV samples.
  
                                // In the following formats, each sample uses 16-bit in storage, while the
                                // sample value is stored in the least significant N bits where N is
                                // specified by the number after "P". For example, for YUV420P9, each Y, U,
                                // and V sample is stored in the least significant 9 bits in a 2-byte block.
                                kYUV420P9 = 16,
                                kYUV420P10 = 17,
                                kYUV422P9 = 18,
                                kYUV422P10 = 19,
                                kYUV444P9 = 20,
                                kYUV444P10 = 21,
                                kYUV420P12 = 22,
                                kYUV422P12 = 23,
                                kYUV444P12 = 24,
    };
  ~~~

  这个固定填`kI420`就行了

  

- `Size coded_size`

  ~~~c++
  struct Size{
  	int width;
  	int height;
  };
  ~~~

  视频的分辨率

  通过`AP4_VideoSampleDescription::GetWidth`、`AP4_VideoSampleDescription::GetHeight`获取就行了

- `uint8_t* extra_data`和`uint32_t extra_data_size`
      填零

- `EncryptionScheme encryption_scheme`

  ~~~c++
  enum class EncryptionScheme : uint32_t {
      kUnencrypted = 0,
      kCenc,  // 'cenc' subsample encryption using AES-CTR mode.
      kCbcs   // 'cbcs' pattern encryption using AES-CBC mode.
  };
  ~~~

  加密协议

  通过`AP4_SampleDescription::GetType()` 判断是否为加密协议

  `AP4_ProtectedSampleDescription::GetSchemeType`获取加密协议id,`0x63656E63`表示`AES-CTR`,`0x63626373`表示`AES-CBC`



返回值为0，表示成功



### 解密与解码

~~~c++
int MyContentDecryptionModuleProxy::DecryptAndDecodeFrame(const InputBuffer_2* encrypted_buffer, VideoFrame* video_frame)
~~~
#### encrypted_buffer
~~~c++
struct InputBuffer_2 {
    const uint8_t* data;  // Pointer to the beginning of the input data. 
    uint32_t data_size;   // 4 Size (in bytes) of |data|.

    EncryptionScheme encryption_scheme; //8

    const uint8_t* key_id;  // c Key ID to identify the decryption key.
    uint32_t key_id_size;   // 10 Size (in bytes) of |key_id|.
    uint32_t : 32;          // 14 Padding.

    const uint8_t* iv;  // 18 Initialization vector.
    uint32_t iv_size;   // 1cSize (in bytes) of |iv|.
    uint32_t : 32;      // 20 Padding.

    const struct SubsampleEntry* subsamples; //24
    uint32_t num_subsamples;  // 28 Number of subsamples in |subsamples|.
    uint32_t : 32;            // 2c Padding.

                              // |pattern| is required if |encryption_scheme| specifies pattern encryption.
    Pattern pattern; //30

    int64_t timestamp;  // 38  Presentation timestamp in microseconds.
};
~~~

- `const uint8_t* data` 和 `uint32_t data_size`、

  视频Sample数据

  如何获取呢

  首先要用新的类,例如`MyLinearReader`重写`AP4_LinearReader`的`AP4_Result AP4_LinearReader::ProcessMoof(AP4_ContainerAtom* moof, AP4_Position moof_offset, AP4_Position mdat_payload_offset)`,若原来的`ProcessMoof`执行成功,则用新的类,例如`MySampleReader`重写`AP4_Result MySampleReader::ReadSampleData(AP4_Sample& sample, AP4_DataBuffer& sample_data)`,创建一个`MySampleReader`并将它赋值给`this->m_Trackers[0]->m_Reader`(在`ProcessMoof`执行)，这样当你调用`MyLinearReader::ReadNextSample`时，`ReadSampleData`就会被调用，而`ReadSampleData`的参数`AP4_Sample& sample`就是我们需要的对象

  通过下面的代码可以获取`data`和`size`

~~~c++
  int dataSize = sample.GetSize();
  char* data = new char[dataSize + 1];
  memset(data, 0, dataSize + 1);
  sample.GetDataStream()->Seek(sample.GetOffset());
  sample.GetDataStream()->Read(data, dataSize);
~~~

- `EncryptionScheme encryption_scheme`

  这里的encryption_scheme是不一样的，之前是表示这个视频的加密协议，而这个表示这个sample的加密协议，因为即使是加密视频，前面也会有几分钟的试看未加密片段

 在`ProcessMoof`执行下面的代码，即可判断加密协议

~~~c++
		moof = 0;
		AP4_TfhdAtom* tfhd = 0;
		AP4_TrexAtom* trex = 0;
		this->m_Fragment->GetTrafAtom(this->m_Trackers[0]->m_Track->GetId(), moof);
		if (moof) {
			tfhd = dynamic_cast<AP4_TfhdAtom*>(moof->GetChild(AP4_ATOM_TYPE_TFHD));
			AP4_MoovAtom* m_MoovAtom = this->m_Movie.GetMoovAtom();
			AP4_ContainerAtom * mvex = dynamic_cast<AP4_ContainerAtom*>(m_MoovAtom->GetChild(AP4_ATOM_TYPE_MVEX));
			if(trex)
				trex = dynamic_cast<AP4_TrexAtom*>(mvex->GetChild(AP4_ATOM_TYPE_TREX));
		}
		int index = 0;
		if (trex)
			index = trex->GetDefaultSampleDescriptionIndex();
		if (tfhd && (tfhd->GetFlags() & 2 )!= 0) {
			index = tfhd->GetSampleDescriptionIndex();
		}
		if (index) {
			index--;
		}
		AP4_SampleDescription* sdescription = this->m_Trackers[0]->m_Track->GetSampleDescription(index);
		if (sdescription->GetType() == AP4_SampleDescription::Type::TYPE_PROTECTED) {
        	AP4_ProtectedSampleDescription* ProtectedSampleDescription = dynamic_cast<AP4_ProtectedSampleDescription*>(sdescription);
            EncryptionScheme protectedType = (EncryptionScheme)(ProtectedSampleDescription->GetSchemeType() == 0x63656E63 ? EncryptionScheme::kCenc : EncryptionScheme::kCbcs);
        
        }
		else{
            EncryptionScheme protectedType = EncryptionScheme::kUnencrypted;
            
        }
~~~
- `const uint8_t* key_id 和 uint32_t key_id_size`

  对称加密算法的`key id`和` size`

  ~~~c++
  			AP4_ProtectedSampleDescription* ProtectedSampleDescription = dynamic_cast<AP4_ProtectedSampleDescription*>(sdescription);
  			AP4_ProtectionSchemeInfo* SchemeInfo = ProtectedSampleDescription->GetSchemeInfo();
  			AP4_ContainerAtom* SchiAtom = SchemeInfo->GetSchiAtom();
  			AP4_CencTrackEncryption* cenc = dynamic_cast<AP4_CencTrackEncryption*>(SchiAtom->GetChild(AP4_ATOM_TYPE_TENC));
  			const AP4_UI08* kid = cenc->GetDefaultKid();
  ~~~

  上面的代码是获取`kid`的,`size`固定为16

- `const uint8_t* iv和uint32_t iv_size`

  在`ProcessMoof`中

  ~~~c++
  AP4_SencAtom* SencAtom = dynamic_cast<AP4_SencAtom*>(moof->GetChild(AP4_ATOM_TYPE_SENC));
  			
  			AP4_CencSampleEncryption* CencSampleEncryption = (AP4_CencSampleEncryption*)(((char*)SencAtom) + 0x28);
  			AP4_CencSampleInfoTable* table = 0;
  			AP4_UI08 m_DefaultCryptByteBlock = 0;
  			AP4_UI08 m_DefaultSkipByteBlock = 0;
  			if (!CencSampleEncryption || (CencSampleEncryption->GetOuter().GetFlags() & 1)==0){
  				AP4_UI08 DefaultPerSampleIvSize = cenc->GetDefaultPerSampleIvSize();
  				AP4_UI08 m_DefaultConstantIvSize = cenc->GetDefaultConstantIvSize();
  				 m_DefaultCryptByteBlock = cenc->GetDefaultCryptByteBlock();
  				 m_DefaultSkipByteBlock = cenc->GetDefaultSkipByteBlock();
  				const AP4_UI08* m_DefaultConstantIv = 0;
  				if (m_DefaultConstantIvSize) {
  					m_DefaultConstantIv = cenc->GetDefaultConstantIv();
  				}
  				if (CencSampleEncryption) {
  					CencSampleEncryption->CreateSampleInfoTable(0, m_DefaultCryptByteBlock, m_DefaultSkipByteBlock, DefaultPerSampleIvSize, m_DefaultConstantIvSize, m_DefaultConstantIv, table);
  				}
  			}
  			
  ~~~

  在`ReadSampleData`中

  ~~~C++
      const AP4_UI08* iv = m_decrypter->m_table->GetIv(m_decrypter->index);
      uint32_t ivSize = m_decrypter->m_table->GetIvSize();
             
  ~~~

  `m_decrypter->index`在`ProcessMoof`中初始化为0，在`ReadSampleData`中递增

- `const struct SubsampleEntry* subsamples 和 uint32_t num_subsamples`

  在`ReadSampleData`中

  ~~~c++
  AP4_Cardinal subsample_count = 0;
  const AP4_UI16* bytes_of_cleartext_data;
  const AP4_UI32* bytes_of_encrypted_data;
  m_decrypter->m_table->GetSampleInfo(m_decrypter->index, subsample_count, bytes_of_cleartext_data, bytes_of_encrypted_data);
   SubsampleEntry* subsamples = new SubsampleEntry[subsample_count];
  for (int i = 0; i < subsample_count; i++) {
      subsamples[i].clear_bytes = bytes_of_cleartext_data[i];
      subsamples[i].cipher_bytes = bytes_of_encrypted_data[i];
  }
  ~~~

- `Pattern pattern`

  ~~~C++
  input.pattern.crypt_byte_block = m_decrypter->m_DefaultCryptByteBlock;
  input.pattern.skip_byte_block = m_decrypter->m_DefaultSkipByteBlock;
  ~~~



- `int64_t timestamp`

  在`ProcessMoof`中

  ~~~C++
	AP4_UI32 timeScale  = this->m_Trackers[0]->m_Track->GetMovieTimeScale();
  ~~~
   在`ReadSampleData`中
  ~~~C++
	 int64_t timestamp = ((double)sample.GetDts() * ((double)1000000 / (double)m_decrypter->m_timeScale) + 0.5);
	~~~





 若`encryption_scheme`为`EncryptionScheme::kUnencrypted`，则不用填` key_id、key_id_size、iv、iv_size、subsamples、num_subsamples、pattern`。


~~~mermaid
graph TD
开始 --> data
开始 --> data_size
开始 --> encryption_scheme
开始 --> timestamp
encryption_scheme -->|等于 kUnencrypted| 无需填充
encryption_scheme -->|不等于 kUnencrypted| 需要填充
需要填充 --> key_id
需要填充 --> key_id_size
需要填充 --> iv
需要填充 --> iv_size
需要填充 --> subsamples
需要填充 --> num_subsamples
需要填充 --> pattern
无需填充 --> 结束
需要填充 --> 结束
data --> 结束
data_size --> 结束
timestamp --> 结束
key_id --> 结束
key_id_size --> 结束
iv --> 结束
iv_size --> 结束
subsamples --> 结束
num_subsamples --> 结束
pattern --> 结束
~~~



#### video_frame

`VideoFrame`是一个带虚表的类，用来保存视频解码后的帧的，这个没什么好讲的，我直接贴代码

~~~c++
class Size {
public:
    Size() : width(0), height(0) {}
    Size(int32_t width, int32_t height) : width(width), height(height) {}

    int32_t width;
    int32_t height;
};
class  Buffer {
public:
    // Destroys the buffer in the same context as it was created.
    virtual void Destroy() = 0;

    virtual uint32_t Capacity() const = 0;
    virtual uint8_t* Data() = 0;
    virtual void SetSize(uint32_t size) = 0;
    virtual uint32_t Size() const = 0;

    Buffer() {}
    virtual ~Buffer() {}

private:
    Buffer(const Buffer&);
    void operator=(const Buffer&);
};
enum VideoFormat {
    kUnknownVideoFormat = 0,  // Unknown format value. Used for error reporting.
    kYv12 = 1,                // 12bpp YVU planar 1x1 Y, 2x2 VU samples.
    kI420 = 2,                // 12bpp YUV planar 1x1 Y, 2x2 UV samples.

    // In the following formats, each sample uses 16-bit in storage, while the
    // sample value is stored in the least significant N bits where N is
    // specified by the number after "P". For example, for YUV420P9, each Y, U,
    // and V sample is stored in the least significant 9 bits in a 2-byte block.
    kYUV420P9 = 16,
    kYUV420P10 = 17,
    kYUV422P9 = 18,
    kYUV422P10 = 19,
    kYUV444P9 = 20,
    kYUV444P10 = 21,
    kYUV420P12 = 22,
    kYUV422P12 = 23,
    kYUV444P12 = 24,
};
class  VideoFrame {
public:
    enum VideoPlane {
        kYPlane = 0,
        kUPlane = 1,
        kVPlane = 2,
        kMaxPlanes = 3,
    };

    virtual void SetFormat(VideoFormat format) = 0;
    virtual VideoFormat Format() const = 0;

    virtual void SetSize(Size size) = 0;
    virtual Size SSize() const = 0;

    virtual void SetFrameBuffer(Buffer* frame_buffer) = 0;
    virtual Buffer* FrameBuffer() = 0;

    virtual void SetPlaneOffset(VideoPlane plane, uint32_t offset) = 0;
    virtual uint32_t PlaneOffset(VideoPlane plane) = 0;

    virtual void SetStride(VideoPlane plane, uint32_t stride) = 0;
    virtual uint32_t Stride(VideoPlane plane) = 0;

    virtual void SetTimestamp(int64_t timestamp) = 0;
    virtual int64_t Timestamp() const = 0;

    public:
    VideoFrame() {}
    virtual ~VideoFrame() {}
};
~~~

~~~c++
class MyVideoFrame:VideoFrame {
public:
    virtual void SetFormat(VideoFormat format);
    virtual VideoFormat Format() const;

    virtual void SetSize(Size size);
    virtual Size SSize() const;

    virtual void SetFrameBuffer(Buffer* frame_buffer);
    virtual Buffer* FrameBuffer();

    virtual void SetPlaneOffset(VideoPlane plane, uint32_t offset);
    virtual uint32_t PlaneOffset(VideoPlane plane);

    virtual void SetStride(VideoPlane plane, uint32_t stride);
    virtual uint32_t Stride(VideoPlane plane);

    virtual void SetTimestamp(int64_t timestamp);
    virtual int64_t Timestamp() const;

public:
    MyVideoFrame() {}
    virtual ~MyVideoFrame() {
        if (m_frame_buffer != nullptr)
            delete m_frame_buffer;
    }
    VideoFormat m_format; //0x4
    Size m_size; //0x8
    int64_t m_timestamp; //0x10
    Buffer* m_frame_buffer = nullptr; //0x18
    uint32_t m_planeOffsets[VideoFrame::VideoPlane::kMaxPlanes];
    uint32_t m_stride[VideoPlane::kMaxPlanes];

};
~~~

~~~c++

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
~~~

### 编码

#### 1. 初始化输出格式和文件

首先，代码通过`avformat_alloc_output_context2`函数初始化输出格式上下文`outputFormatContext`，并指定输出文件名为"tmp.mp4"。然后使用`avio_open`函数打开输出文件，若打开失败则输出错误信息并返回。

```c++
cCopy codeAVFormatContext* outputFormatContext = nullptr;
avformat_alloc_output_context2(&outputFormatContext, nullptr, nullptr, "tmp.mp4");

if (outputFormatContext == nullptr) {
    Log("无法分配输出格式上下文\n");
    return -1;
}

if (avio_open(&outputFormatContext->pb, "tmp.mp4", AVIO_FLAG_WRITE) < 0) {
    Log("无法打开输出文件\n");
    avformat_free_context(outputFormatContext);
    return -1;
}
```

#### 2. 创建视频流

接下来，代码通过`avformat_new_stream`函数创建视频流`videoStream`，若创建失败则输出错误信息并返回。

```c++
cCopy codeAVStream* videoStream = avformat_new_stream(outputFormatContext, nullptr);
if (!videoStream) {
    Log("无法创建视频流\n");
    avio_closep(&outputFormatContext->pb);
    avformat_free_context(outputFormatContext);
    return -1;
}
```

#### 3. 打开编码器

通过`avcodec_open2`函数打开编码器，若打开失败则输出错误信息并返回。

```c++
//获取ffmpeg 流信息
   AVFormatContext* Formatcontext = 0;
   int result1 = avformat_open_input(&Formatcontext, input_file.c_str(), 0, 0);
   int result2 = avformat_find_stream_info(Formatcontext, 0);
   AVStream* stream = Formatcontext->streams[0];
   AVRational sample_aspect_ratio = av_guess_sample_aspect_ratio(Formatcontext, stream, 0);
   int64_t bit_rate = Formatcontext->bit_rate;
   if (sample_aspect_ratio.den == 0 || sample_aspect_ratio.num == 0) {
       sample_aspect_ratio = AVRational{ 1, 0x1 }; // 从licensedMainfest获取
   }


   // 获取裸流编码
   AVCodecContext* avctx;
   int ret;

   avctx = avcodec_alloc_context3(NULL);
   if (!avctx)
       return -1;

   ret = avcodec_parameters_to_context(avctx, stream->codecpar);
   if (ret < 0) {
       avcodec_free_context(&avctx);
       return -1;
   }

const AVCodec* encodec = avcodec_find_encoder(AV_CODEC_ID_H264);
AVCodecContext* encodecContext = avcodec_alloc_context3(encodec);

if (encodecContext) {
    // 设置编码器的参数
    encodecContext->codec_type = AVMediaType::AVMEDIA_TYPE_VIDEO;
           encodecContext->codec_id = encodec->id;
           encodecContext->pix_fmt = *encodec->pix_fmts;

           encodecContext->width = g_width;
           encodecContext->height = g_height;

           encodecContext->level = 0x1E;

           encodecContext->framerate = AVRational{ stream->avg_frame_rate.den, stream->avg_frame_rate.num };
           encodecContext->time_base = AVRational{ stream->avg_frame_rate.den, stream->avg_frame_rate.num };
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
           //int64_t val = 22 - 4;
           av_opt_set_int(encodecContext->priv_data, "crf", val, 0);

           if ((*(char*)&outputFormatContext->oformat->flags & 0x40) != 0)
               encodecContext->flags |= 0x400000;
    int enaocode = avcodec_open2(encodecContext, encodec, nullptr);

    if (enaocode < 0) {
        Log("avcodec_open2 encode failed\n");
        avcodec_free_context(&encodecContext);
        avio_closep(&outputFormatContext->pb);
        avformat_free_context(outputFormatContext);
        return -1;
    }
}
```

#### 4. 写入文件头部

使用`avformat_write_header`函数将文件头部信息写入输出文件。

```c++
avformat_write_header(outputFormatContext, nullptr);
```

#### 5. 解码帧并进行格式转换

在每次循环中，从解码器接收解码后的视频帧`video_frame`，然后将其进行格式转换。

对于YUV420P像素格式，通过自定义函数`transtoYUV`将帧数据转换为YUV格式，然后使用`transYUVToAVFrame`函数将YUV数据填充到`AVFrame`中。

```c++

// 解码后的视频帧存储在video_frame中
AVFrame* video_frame = av_frame_alloc();
// 解码操作...

// 进行格式转换，得到AVFrame frame
AVFrame* frame = nullptr;

if (avctx->pix_fmt == AV_PIX_FMT_YUV420P) {
    // 转换为YUV格式
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
```

~~~c++

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
~~~

~~~c++
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
~~~

#### 6. 编码并写入输出流

将转换后的帧数据送入编码器，编码后的数据存储在`AVPacket`中。通过`avcodec_receive_packet`函数获取编码后的数据，然后将其写入输出文件。

```c++
AVPacket pkt{ 0 };
av_init_packet(&pkt);

// 将frame送入编码器
avcodec_send_frame(encodecContext, frame);

while (1) {
    // 获取编码后的数据
    ret = avcodec_receive_packet(encodecContext, &pkt);
    if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) {
        break;
    } else if (ret < 0) {
        Log("Error encoding a frame\n");
        break;
    }

    // 将数据写入输出流
    ret = av_interleaved_write_frame(outputFormatContext, &pkt);
    av_packet_unref(&pkt);
}
```

#### 7. 写入文件尾部

在循环结束后，使用`av_write_trailer`函数写入文件尾部信息。随后释放相关的上下文和内存。

```c++
av_write_trailer(outputFormatContext);
avcodec_free_context(&encodecContext);
avio_closep(&outputFormatContext->pb);
avformat_free_context(outputFormatContext);
```





