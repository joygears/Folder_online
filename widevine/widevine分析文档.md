## widevine分析文档

### widevine使用整体流程

https://github.com/tomer8007/widevine-l3-decryptor/wiki/Reversing-the-old-Widevine-Content-Decryption-Module

### decodingInfo

#### **函数原型**

~~~
decodingInfo(configuration)
~~~

[函数详情](https://developer.mozilla.org/en-US/docs/Web/API/MediaCapabilities/decodingInfo)

#### **参数**



~~~json
{
    "type": "media-source",
    "video": {
        "contentType": "video/mp4; codecs=\"avc1.42c01e\"",
        "width": 256,
        "height": 110,
        "bitrate": 103942,
        "framerate": 24
    },
    "audio": {
        "contentType": "audio/mp4; codecs=\"mp4a.40.2\"",
        "channels": 2,
        "bitrate": 135512,
        "samplerate": 48000,
        "spatialRendering": false
    },
    "keySystemConfiguration": {
        "keySystem": "com.widevine.alpha",
        "initDataType": " ",
        "persistentState": "optional",
        "distinctiveIdentifier": "optional",
        "sessionTypes": [
            "temporary"
        ],
        "audio": {},
        "video": {}
    }
}
~~~

#### **返回值**

~~~json
{
    "powerEfficient": true,
    "smooth": true,
    "supported": true,
    "keySystemAccess": {
        keySystemAccess: MediaKeySystemAccess
		keySystem: "com.widevine.alpha"
		[[Prototype]]: MediaKeySystemAccess} 
}
~~~



####  **使用例子**

~~~javascript
//Create media configuration to be tested
const mediaConfig = {
  type: "file", // or 'media-source' or 'webrtc'
  audio: {
    contentType: "audio/ogg; codecs=vorbis", // valid content type
    channels: 2, // audio channels used by the track
    bitrate: 132700, // number of bits used to encode 1s of audio
    samplerate: 5200, // number of audio samples making up that 1s.
  },
};

// check support and performance
navigator.mediaCapabilities.decodingInfo(mediaConfig).then((result) => {
  console.log(
    `This configuration is ${result.supported ? "" : "not "}supported,`
  );
  console.log(`${result.smooth ? "" : "not "}smooth, and`);
  console.log(`${result.powerEfficient ? "" : "not "}power efficient.`);
});

~~~

这个函数最主要获取了keySystemAccess对象