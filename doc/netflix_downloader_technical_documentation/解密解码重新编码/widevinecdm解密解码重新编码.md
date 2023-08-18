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
int MyContentDecryptionModuleProxy::DecryptAndDecodeFrame(const InputBuffer_2* encrypted_buffer, void* video_frame)
~~~

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