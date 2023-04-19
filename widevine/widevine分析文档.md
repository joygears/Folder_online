## widevine分析文档

### widevine使用整体流程

https://github.com/tomer8007/widevine-l3-decryptor/wiki/Reversing-the-old-Widevine-Content-Decryption-Module

#### decodingInfo

##### 函数原型

~~~
decodingInfo(configuration)
~~~

[函数详情](https://developer.mozilla.org/en-US/docs/Web/API/MediaCapabilities/decodingInfo)

##### 参数



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

##### 返回值

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

##### 使用例子

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

#### createMediaKeys

##### 函数原型

~~~JS
/**
	为KeySystem创建一个新的MediaKeys对象
	Return type: Promise<MediaKeys>
*/

createMediaKeys()
~~~

##### 对象

~~~json
MediaKeySystemAccess {keySystem: 'com.widevine.alpha'}
	keySystem: "com.widevine.alpha"
	[[Prototype]]: MediaKeySystemAccess
        createMediaKeys: ƒ createMediaKeys()
        getConfiguration: ƒ getConfiguration()
        keySystem: （…）
        constructor: ƒ MediaKeySystemAccess()
        Symbol(Symbol.toStringTag): "MediaKeySystemAccess"
        get keySystem: ƒ keySystem()
        [[Prototype]]: Object
~~~

##### 返回值

~~~json
MediaKeys {}
	[[Prototype]]: MediaKeys
        createSession: ƒ createSession()
        getStatusForPolicy: ƒ getStatusForPolicy()
        setServerCertificate: ƒ setServerCertificate()
        constructor: ƒ MediaKeys()
        Symbol(Symbol.toStringTag): "MediaKeys"
        [[Prototype]]: Object
~~~

#### createSession

##### 函數原型

~~~js
/**
 返回一个新的 MediaKeySession 对象
*/
createSession(sessionType)
~~~

##### 对象

~~~json
MediaKeys {}
	[[Prototype]]: MediaKeys
        createSession: ƒ createSession()
        getStatusForPolicy: ƒ getStatusForPolicy()
        setServerCertificate: ƒ setServerCertificate()
        constructor: ƒ MediaKeys()
        Symbol(Symbol.toStringTag): "MediaKeys"
        [[Prototype]]: Object
~~~



##### 参数

~~~
'temporary'
~~~

##### 返回值

~~~json
MediaKeySession {sessionId: '', expiration: NaN, closed: Promise, keyStatuses: MediaKeyStatusMap, onkeystatuseschange: null, …}
    closed: Promise {<pending>}
    expiration: NaN
    keyStatuses: MediaKeyStatusMap {size: 0}
    onkeystatuseschange: null
    onmessage: null
    sessionId: ""
    [[Prototype]]: MediaKeySession
        close: ƒ close()
        closed: （…）
        expiration: （…）
        generateRequest: ƒ generateRequest()
        keyStatuses: （…）
        load: ƒ load()
        onkeystatuseschange: （…）
        onmessage: （…）
        remove: ƒ remove()
        sessionId: （…）
        update: ƒ update()
        constructor: ƒ MediaKeySession()
        Symbol(Symbol.toStringTag): "MediaKeySession"
        get closed: ƒ closed()
        get expiration: ƒ expiration()
        get keyStatuses: ƒ keyStatuses()
        get onkeystatuseschange: ƒ onkeystatuseschange()
        set onkeystatuseschange: ƒ onkeystatuseschange()
        get onmessage: ƒ onmessage()
        set onmessage: ƒ onmessage()
        get sessionId: ƒ sessionId()
        [[Prototype]]: EventTarget
~~~

#### generateRequest

##### 函数原型

~~~js
/*基于initData生成一个许可证请求。如果算法执行成功且承诺已解决的话，一个类型为 "license-request" 或 "individualization-request"的 message 将在事件队列里*/
session.generateRequest(initDataType, initData)
~~~

##### 对象

~~~json
MediaKeySession {sessionId: '', expiration: NaN, closed: Promise, keyStatuses: MediaKeyStatusMap, onkeystatuseschange: null, …}
    closed: Promise {<pending>}
    expiration: NaN
    keyStatuses: MediaKeyStatusMap {size: 0}
    onkeystatuseschange: null
    onmessage: null
    sessionId: ""
    [[Prototype]]: MediaKeySession
        close: ƒ close()
        closed: （…）
        expiration: （…）
        generateRequest: ƒ generateRequest()
        keyStatuses: （…）
        load: ƒ load()
        onkeystatuseschange: （…）
        onmessage: （…）
        remove: ƒ remove()
        sessionId: （…）
        update: ƒ update()
        constructor: ƒ MediaKeySession()
        Symbol(Symbol.toStringTag): "MediaKeySession"
        get closed: ƒ closed()
        get expiration: ƒ expiration()
        get keyStatuses: ƒ keyStatuses()
        get onkeystatuseschange: ƒ onkeystatuseschange()
        set onkeystatuseschange: ƒ onkeystatuseschange()
        get onmessage: ƒ onmessage()
        set onmessage: ƒ onmessage()
        get sessionId: ƒ sessionId()
        [[Prototype]]: EventTarget
~~~

##### 参数

**initDataType**

~~~~
'cenc'
~~~~

**initData**

~~~js
Uint8Array(167) [0, 0, 0, 167, 112, 115, 115, 104, 0, 0, 0, 0, 237, 239, 139, 169, 121, 214, 74, 206, 163, 200, 39, 220, 213, 29, 33, 237, 0, 0, 0, 135, 18, 16, 81, 116, 83, 134, 45, 66, 86, 253, 139, 173, 79, 88, 66, 32, 4, 215, 18, 16, 240, 147, 126, 154, 119, 200, 85, 240, 166, 212, 56, 100, 197, 217, 243, 101, 18, 16, 77, 75, 12, 162, 90, 193, 88, 240, 185, 193, 152, 60, 81, 126, 226, 181, 18, 16, 144, 42, 5, 26, 107, 54, 86, 174, 172, 25, 38, 252, …]
    [0 … 99]
    [100 … 166]
    buffer: 
    ArrayBuffer(167)
    byteLength: 167
    byteOffset: 0
    length: 167
    Symbol(Symbol.toStringTag): "Uint8Array"
    [[Prototype]]: TypedArray
~~~

>这个数据是从服务器拿的，应该会和链接放在一起

##### 返回值

这个返回值通过监听session对象的 'message' 事件获取

~~~js
this.eventManager_.listen(session, 'message',
    /** @type {shaka.util.EventManager.ListenerType} */(
          (event) => this.onSessionMessage_(event)));
~~~
**event**
~~~js
MediaKeyMessageEvent {isTrusted: true, messageType: 'license-request', message: ArrayBuffer(2), type: 'message', target: MediaKeySession, …}
    isTrusted: true
    bubbles: false
    cancelBubble: false
    cancelable: false
    composed: false
    currentTarget: MediaKeySession {sessionId: '03432D025B26AA2A49B51F056D2A890D', expiration: NaN, closed: Promise, keyStatuses: MediaKeyStatusMap, onkeystatuseschange: null, …}
    defaultPrevented: false
    eventPhase: 2
    message: 
    ArrayBuffer(2)
    messageType: "license-request"
    path: []
    returnValue: true
    srcElement: MediaKeySession {sessionId: '03432D025B26AA2A49B51F056D2A890D', expiration: NaN, closed: Promise, keyStatuses: MediaKeyStatusMap, onkeystatuseschange: null, …}
    target: MediaKeySession {sessionId: '03432D025B26AA2A49B51F056D2A890D', expiration: NaN, closed: Promise, keyStatuses: MediaKeyStatusMap, onkeystatuseschange: null, …}
    timeStamp: 14949163.2
    type: "message"
    [[Prototype]]: MediaKeyMessageEvent
~~~

##### 发送请求

~~~~
请求网址: https://cwip-shaka-proxy.appspot.com/no_auth
请求方法: POST
状态代码: 200 
远程地址: 127.0.0.1:7890
引荐来源网址政策: strict-origin-when-cross-origin

body:MediaKeyMessageEvent.message


~~~~

### netflix license request

###### url

```
https://www.netflix.com/msl/playapi/cadmium/licensedmanifest/1?reqAttempt=1&reqName=prefetch/licensedManifest&clienttype=akira&uiversion=v422d49b0&browsername=edgeoss&browserversion=86.0.622&osname=windows&osversion=10.0
```

###### body

~~~js
{
    "type": "standard",
    "manifestVersion": "v2",
    "viewableId": 81678253,
    "profiles": [
        "heaac-2-dash",
        "heaac-2hq-dash",
        "playready-h264mpl30-dash",
        "playready-h264mpl31-dash",
        "playready-h264hpl30-dash",
        "playready-h264hpl31-dash",
        "vp9-profile0-L30-dash-cenc",
        "vp9-profile0-L31-dash-cenc",
        "av1-main-L30-dash-cbcs-prk",
        "av1-main-L31-dash-cbcs-prk",
        "playready-h264mpl40-dash",
        "playready-h264hpl40-dash",
        "vp9-profile0-L40-dash-cenc",
        "av1-main-L40-dash-cbcs-prk",
        "av1-main-L41-dash-cbcs-prk",
        "h264hpl30-dash-playready-live",
        "h264hpl31-dash-playready-live",
        "h264hpl40-dash-playready-live",
        "dfxp-ls-sdh",
        "simplesdh",
        "nflx-cmisc",
        "imsc1.1",
        "BIF240",
        "BIF320"
    ],
    "flavor": "STANDARD",
    "drmType": "widevine",
    "drmVersion": 25,
    "usePsshBox": true,
    "isBranching": false,
    "useHttpsStreams": true,
    "supportsUnequalizedDownloadables": true,
    "imageSubtitleHeight": 1080,
    "uiVersion": "shakti-v95eeb959",
    "uiPlatform": "SHAKTI",
    "clientVersion": "6.0039.753.911",
    "platform": "112.0.0.0",
    "osVersion": "10.0",
    "osName": "windows",
    "supportsPreReleasePin": true,
    "supportsWatermark": true,
    "videoOutputInfo": [
        {
            "type": "DigitalVideoOutputDescriptor",
            "outputType": "unknown",
            "supportedHdcpVersions": [],
            "isHdcpEngaged": false
        }
    ],
    "titleSpecificData": {
        "81678253": {
            "unletterboxed": false
        }
    },
    "preferAssistiveAudio": false,
    "isUIAutoPlay": false,
    "isNonMember": false,
    "desiredVmaf": "plus_lts",
    "desiredSegmentVmaf": "plus_lts",
    "requestSegmentVmaf": false,
    "supportsPartialHydration": true,
    "contentPlaygraph": [
        "start"
    ],
    "supportsAdBreakHydration": false,
    "liveMetadataFormat": "INDEXED_SEGMENT_TEMPLATE",
    "useBetterTextUrls": true,
    "challenges": {
        "default": [
            {
                "drmSessionId": "A2DD2782120FE0FFFF927B5C7FBC3915",
                "clientTime": 1681872047,
                "challengeBase64": "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"
            }
        ]
    },
    "profileGroups": [
        {
            "name": "default",
            "profiles": [
                "heaac-2-dash",
                "heaac-2hq-dash",
                "playready-h264mpl30-dash",
                "playready-h264mpl31-dash",
                "playready-h264hpl30-dash",
                "playready-h264hpl31-dash",
                "vp9-profile0-L30-dash-cenc",
                "vp9-profile0-L31-dash-cenc",
                "av1-main-L30-dash-cbcs-prk",
                "av1-main-L31-dash-cbcs-prk",
                "playready-h264mpl40-dash",
                "playready-h264hpl40-dash",
                "vp9-profile0-L40-dash-cenc",
                "av1-main-L40-dash-cbcs-prk",
                "av1-main-L41-dash-cbcs-prk",
                "h264hpl30-dash-playready-live",
                "h264hpl31-dash-playready-live",
                "h264hpl40-dash-playready-live",
                "dfxp-ls-sdh",
                "simplesdh",
                "nflx-cmisc",
                "imsc1.1",
                "BIF240",
                "BIF320"
            ]
        }
    ],
    "licenseType": "standard",
    "xid": "168187204640372700"
    	    168189707114169472
}
~~~

###### 响应

~~~js
{
    "id": 168187247314442750,
    "version": 2,
    "serverTime": 1681872475716,
    "result": {
        "audioTextShortcuts": [
            {
                "id": "1f919217-fc5f-426b-8c59-f8cadafe612b",
                "audioTrackId": "A:2:1;2;zh;1;0;",
                "textTrackId": "T:2:1;1;NONE;0;1;0;"
            },
            {
                "id": "dd33765f-1e98-4304-baae-8c07d336128d",
                "audioTrackId": "A:2:1;2;zh;1;0;",
                "textTrackId": "T:2:0;1;en;0;0;0;"
            }
        ],
        "bookmark": -1,
        "cdnResponseData": {
            "pbcid": "6.f0EIcfE7Bhix82cl2OxSd31pFr7IOfaq9fmY6fTjLSc"
        },
        "clientIpAddress": "2a0e:aa00:143:67e1:f3f0:4570:19e7:847e",
        "drmContextId": "default",
        "drmType": "widevine",
        "drmVersion": 25,
        "duration": 2569000,
        "eligibleABTestMap": {
            "44840": "2"
        },
        "expiration": 1681915675662,
        "hasClearProfile": false,
        "hasClearStreams": false,
        "hasDrmProfile": true,
        "hasDrmStreams": true,
        "links": {
            "events": {
                "href": "/events?playbackContextId=E3-BQFRAAELEHVZd1tSaAJ7LDqCmWD2IkyB0LppIXN5owFwBmX_SLTYhFoGofWNOFctLIPcDxT_AOPmx26xlSMY3-rlRQ_cBm-iOiZdwQwBILLLD7VjwTtw_Ys4uZGqT-u9v1XW5gspayOHlFO_F3Mw-JKMjFCFRTFe4DciirlOaIOWkZJ32VUCSzwlbWPclr3lmbMlbkXtnUtPf9elMSPwK9-LuPZhbe0Pg3UtWVma99-64Rns9DcIOfP9ZUhwW1CXYuyZLxd8cbLNIgXglhD05G58cZwnuCu3_wSnazCfJbAHZ9hn97XMSwkq8l1p60JWqIP1cLEU_5xge9FB68ltQfb3GjP7EnPHgR3OAIj3gAIfkl_Qnr_l2YboZB40wVIjD_Mqv3OPYCurwdqCnueWM5t51qHR5ShmP4-Vi23ZDpdbAB9SjYPbzx6E_Qk3Qic7KG8PtLQRiks-lPkSIhlLq-Sxd4s3pPNKGAeKtgFe-t-B1NjlJd8p7IAwb2x3i8k7DWDlFEAinFzPxJ0Ws-hbjRMzbcB8bYRAgE8QT1E3cYXgVAkI0H3zMdIXJxmKVGXixyK_w9M9LS6n0tX4brTdsOkns9zumWLjL2ZRSrq1BnPzRhr00rARpDpGlRPvU82uPlAlS2lXdL3Y&esn=NFCDCH-02-K3YJKVNY4K6VN2T3XQ10T7JQJE52QP",
                "rel": "events"
            },
            "license": {
                "href": "/license?licenseType=standard&playbackContextId=E3-BQFRAAELEHVZd1tSaAJ7LDqCmWD2IkyB0LppIXN5owFwBmX_SLTYhFoGofWNOFctLIPcDxT_AOPmx26xlSMY3-rlRQ_cBm-iOiZdwQwBILLLD7VjwTtw_Ys4uZGqT-u9v1XW5gspayOHlFO_F3Mw-JKMjFCFRTFe4DciirlOaIOWkZJ32VUCSzwlbWPclr3lmbMlbkXtnUtPf9elMSPwK9-LuPZhbe0Pg3UtWVma99-64Rns9DcIOfP9ZUhwW1CXYuyZLxd8cbLNIgXglhD05G58cZwnuCu3_wSnazCfJbAHZ9hn97XMSwkq8l1p60JWqIP1cLEU_5xge9FB68ltQfb3GjP7EnPHgR3OAIj3gAIfkl_Qnr_l2YboZB40wVIjD_Mqv3OPYCurwdqCnueWM5t51qHR5ShmP4-Vi23ZDpdbAB9SjYPbzx6E_Qk3Qic7KG8PtLQRiks-lPkSIhlLq-Sxd4s3pPNKGAeKtgFe-t-B1NjlJd8p7IAwb2x3i8k7DWDlFEAinFzPxJ0Ws-hbjRMzbcB8bYRAgE8QT1E3cYXgVAkI0H3zMdIXJxmKVGXixyK_w9M9LS6n0tX4brTdsOkns9zumWLjL2ZRSrq1BnPzRhr00rARpDpGlRPvU82uPlAlS2lXdL3Y&esn=NFCDCH-02-K3YJKVNY4K6VN2T3XQ10T7JQJE52QP&drmContextId=default",
                "rel": "license"
            },
            "ldl": {
                "href": "/license?licenseType=limited&playbackContextId=E3-BQFRAAELEHVZd1tSaAJ7LDqCmWD2IkyB0LppIXN5owFwBmX_SLTYhFoGofWNOFctLIPcDxT_AOPmx26xlSMY3-rlRQ_cBm-iOiZdwQwBILLLD7VjwTtw_Ys4uZGqT-u9v1XW5gspayOHlFO_F3Mw-JKMjFCFRTFe4DciirlOaIOWkZJ32VUCSzwlbWPclr3lmbMlbkXtnUtPf9elMSPwK9-LuPZhbe0Pg3UtWVma99-64Rns9DcIOfP9ZUhwW1CXYuyZLxd8cbLNIgXglhD05G58cZwnuCu3_wSnazCfJbAHZ9hn97XMSwkq8l1p60JWqIP1cLEU_5xge9FB68ltQfb3GjP7EnPHgR3OAIj3gAIfkl_Qnr_l2YboZB40wVIjD_Mqv3OPYCurwdqCnueWM5t51qHR5ShmP4-Vi23ZDpdbAB9SjYPbzx6E_Qk3Qic7KG8PtLQRiks-lPkSIhlLq-Sxd4s3pPNKGAeKtgFe-t-B1NjlJd8p7IAwb2x3i8k7DWDlFEAinFzPxJ0Ws-hbjRMzbcB8bYRAgE8QT1E3cYXgVAkI0H3zMdIXJxmKVGXixyK_w9M9LS6n0tX4brTdsOkns9zumWLjL2ZRSrq1BnPzRhr00rARpDpGlRPvU82uPlAlS2lXdL3Y&esn=NFCDCH-02-K3YJKVNY4K6VN2T3XQ10T7JQJE52QP&drmContextId=default",
                "rel": "license"
            }
        },
        "locations": [
            {
                "key": "1-41378-high",
                "rank": 1,
                "weight": 180,
                "level": 1
            },
            {
                "key": "2-41378-high",
                "rank": 6,
                "weight": 140,
                "level": 2
            },
            {
                "key": "11-41378-high",
                "rank": 8,
                "weight": 120,
                "level": 3
            }
        ],
        "manifestExpirationDuration": 28799943,
        "movieId": 81678253,
        "packageId": "2159503",
        "playbackContextId": "E3-BQFRAAELEHVZd1tSaAJ7LDqCmWD2IkyB0LppIXN5owFwBmX_SLTYhFoGofWNOFctLIPcDxT_AOPmx26xlSMY3-rlRQ_cBm-iOiZdwQwBILLLD7VjwTtw_Ys4uZGqT-u9v1XW5gspayOHlFO_F3Mw-JKMjFCFRTFe4DciirlOaIOWkZJ32VUCSzwlbWPclr3lmbMlbkXtnUtPf9elMSPwK9-LuPZhbe0Pg3UtWVma99-64Rns9DcIOfP9ZUhwW1CXYuyZLxd8cbLNIgXglhD05G58cZwnuCu3_wSnazCfJbAHZ9hn97XMSwkq8l1p60JWqIP1cLEU_5xge9FB68ltQfb3GjP7EnPHgR3OAIj3gAIfkl_Qnr_l2YboZB40wVIjD_Mqv3OPYCurwdqCnueWM5t51qHR5ShmP4-Vi23ZDpdbAB9SjYPbzx6E_Qk3Qic7KG8PtLQRiks-lPkSIhlLq-Sxd4s3pPNKGAeKtgFe-t-B1NjlJd8p7IAwb2x3i8k7DWDlFEAinFzPxJ0Ws-hbjRMzbcB8bYRAgE8QT1E3cYXgVAkI0H3zMdIXJxmKVGXixyK_w9M9LS6n0tX4brTdsOkns9zumWLjL2ZRSrq1BnPzRhr00rARpDpGlRPvU82uPlAlS2lXdL3Y",
        "servers": [
            {
                "id": 67303,
                "key": "1-41378-high",
                "lowgrade": false,
                "name": "c062.sin001.ix.nflxvideo.net",
                "rank": 1,
                "type": "OPEN_CONNECT_APPLIANCE",
                "dns": {
                    "host": "ipv6-c062-sin001-ix.1.oca.nflxvideo.net",
                    "ipv4": "23.246.55.158",
                    "ipv6": "2a00:86c0:1055:1055::158",
                    "forceLookup": false
                }
            },
            {
                "id": 72988,
                "key": "1-41378-high",
                "lowgrade": false,
                "name": "c075.sin001.ix.nflxvideo.net",
                "rank": 2,
                "type": "OPEN_CONNECT_APPLIANCE",
                "dns": {
                    "host": "ipv6-c075-sin001-ix.1.oca.nflxvideo.net",
                    "ipv4": "23.246.55.165",
                    "ipv6": "2a00:86c0:1055:1055::165",
                    "forceLookup": false
                }
            },
            {
                "id": 62817,
                "key": "1-41378-high",
                "lowgrade": false,
                "name": "c039.sin001.ix.nflxvideo.net",
                "rank": 4,
                "type": "OPEN_CONNECT_APPLIANCE",
                "dns": {
                    "host": "ipv6-c039-sin001-ix.1.oca.nflxvideo.net",
                    "ipv4": "23.246.54.148",
                    "ipv6": "2a00:86c0:1054:1054::148",
                    "forceLookup": false
                }
            },
            {
                "id": 73092,
                "key": "1-41378-high",
                "lowgrade": false,
                "name": "c069.sin001.ix.nflxvideo.net",
                "rank": 5,
                "type": "OPEN_CONNECT_APPLIANCE",
                "dns": {
                    "host": "ipv6-c069-sin001-ix.1.oca.nflxvideo.net",
                    "ipv4": "23.246.54.165",
                    "ipv6": "2a00:86c0:1054:1054::165",
                    "forceLookup": false
                }
            },
            {
                "id": 58951,
                "key": "2-41378-high",
                "lowgrade": false,
                "name": "c030.hkg001.ix.nflxvideo.net",
                "rank": 6,
                "type": "OPEN_CONNECT_APPLIANCE",
                "dns": {
                    "host": "ipv6-c030-hkg001-ix.1.oca.nflxvideo.net",
                    "ipv4": "23.246.57.143",
                    "ipv6": "2a00:86c0:1057:1057::143",
                    "forceLookup": false
                }
            },
            {
                "id": 67239,
                "key": "2-41378-high",
                "lowgrade": false,
                "name": "c060.hkg001.ix.nflxvideo.net",
                "rank": 7,
                "type": "OPEN_CONNECT_APPLIANCE",
                "dns": {
                    "host": "ipv6-c060-hkg001-ix.1.oca.nflxvideo.net",
                    "ipv4": "23.246.57.158",
                    "ipv6": "2a00:86c0:1057:1057::158",
                    "forceLookup": false
                }
            },
            {
                "id": 59677,
                "key": "11-41378-high",
                "lowgrade": false,
                "name": "c012.lax009.ix.nflxvideo.net",
                "rank": 8,
                "type": "OPEN_CONNECT_APPLIANCE",
                "dns": {
                    "host": "ipv6-c012-lax009-ix.1.oca.nflxvideo.net",
                    "ipv4": "45.57.100.137",
                    "ipv6": "2a00:86c0:2100:2100::137",
                    "forceLookup": false
                }
            }
        ],
        "steeringAdditionalInfo": {
            "additionalGroupNames": [],
            "steeringId": "6.f0EIcfE7Bhix82cl2OxSd31pFr7IOfaq9fmY6fTjLSc",
            "streamingClientConfig": {}
        },
        "timedtexttracks": [
            {
                "type": "timedtext",
                "trackType": "PRIMARY",
                "rawTrackType": "subtitles",
                "id": "none",
                "new_track_id": "T:2:1;1;NONE;0;1;0;",
                "language": null,
                "languageDescription": "关闭",
                "downloadableIds": {},
                "ttDownloadables": {},
                "rank": -1,
                "hydrated": true,
                "encodingProfileNames": [],
                "isForcedNarrative": false,
                "isLanguageLeftToRight": true,
                "isNoneTrack": true
            },
            {
                "type": "timedtext",
                "trackType": "PRIMARY",
                "rawTrackType": "subtitles",
                "id": "6e6f6e657c554e4b4e4f574e7c756e6b6e6f776e7c66616c73657c656e7c5375627469746c65737c756e6b6e6f776e7c546578747c7072696d6172797c7c7c6e6f6e657c30",
                "new_track_id": "T:2:0;1;en;0;0;0;",
                "language": "en",
                "languageDescription": "英语",
                "downloadableIds": {
                    "imsc1.1": "1512072585",
                    "simplesdh": "1511789839",
                    "dfxp-ls-sdh": "1512072794"
                },
                "ttDownloadables": {
                    "imsc1.1": {
                        "size": 71276,
                        "hashValue": "0TARsYUJ4Ln98c1Buw2u++7uhL4=",
                        "hashAlgo": "sha1",
                        "urls": [
                            {
                                "cdn_id": 72988,
                                "url": "https://ipv6-c075-sin001-ix.1.oca.nflxvideo.net/?o=1&v=14&e=1681915675&t=AFO-u6CfmQrIUH1UUXmKMHzXsq09kXaeH_SoTpUKzd1hxg4OTlNSkXKTrp1ETFYKl9BmaC6_JX5WUuSQPlMXOWvUPrM8OmfQzTOekglYMmRejWX6PqlCazdoVH3LjSXTlh342yQCkvLGOJMzUw9fM6TM9ydk2fRhirZUUVC7loKsrHX5uUeYjOk9JJGPOdRDl9G7LZrSABR5Az2H7z7U8S_DBwbhM13jruVzMoP1HXqCZ8gOPgPJrD1zuZW43AYoFR4lcfdtZw"
                            },
                            {
                                "cdn_id": 62817,
                                "url": "https://ipv4-c039-sin001-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=jO-BNlEqprazVHRscQhTqZEoAon5QzVlUIbZ3MjAC_n0chAcXAHGa74ZPSncn0RVG2Ew9822wtHK4oNQRUp1ULqBFEaxEsNV4PPEnWh8_GsdDlnlHmglgaDGjWv7iZ5WbzERjZ4L2Qv-Pbuo9LJzSZigzks6THA0ihJ274Ec149xbGPNMK47TTMoBds7zu0wzfG0oFPD5Aqhcsfp2R-Ua2mJ6v9OXWpNFpXhnB-eR_M2H4VwVJnepyjnMI8RIydFC1EcKhjzPg"
                            },
                            {
                                "cdn_id": 58951,
                                "url": "https://ipv6-c030-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=rggg3wkl6yakFMz53Unlu2HKRJh5KHOSktbi1itH-z_7nmsRrX6uTxtzWs1mIIylfFl80jQux1ReyVshQRHSpzXK8ZVhOaRGkaLGkeUgHfFsEoammEG6aGC19ytDva3fN_Cww5YS3tPOGzcMokIKC8901iGJaYOnWwWrU0N90rQF61zk8CYLMS7xA8mxgTvgLqBkqQKuIQcbVwhiKcz4XxZ_vkg99oRWYZM2Ku523DSnJznV4u2Vf1_jmH-mFaoTIUVboMxZCg"
                            }
                        ],
                        "textKey": null,
                        "isImage": false
                    },
                    "simplesdh": {
                        "size": 54233,
                        "hashValue": "M0wVtetqL0Jxr7AW2HcuTkZFbso=",
                        "hashAlgo": "sha1",
                        "urls": [
                            {
                                "cdn_id": 67303,
                                "url": "https://ipv6-c062-sin001-ix.1.oca.nflxvideo.net/?o=1&v=102&e=1681915675&t=sv0DOXxdFKTtFV8_ef_QLk_AUhwfLSf64TmQEihLeEu74DJmAFsCmLN_k9xxAW1WBLubo5pnWRssmYMQgcihKFzZLIi-ovILVzYeTIqs6f7tM64GzB-inEtzoOoQoVuWg4VuLylk54HTiOP0jUZ5NSc7a5Adh96iT9oniXzg-wqmLnDhvZt3wtCMWXmo4_GeI63x4F1glig-TlNNMLwnsZZrr5KLlRM7ixtZgjrMUnxKvOaML_MazlROOSKDS2TtMF8V"
                            },
                            {
                                "cdn_id": 73092,
                                "url": "https://ipv4-c069-sin001-ix.1.oca.nflxvideo.net/?o=1&v=13&e=1681915675&t=jaLOOp8n-jp4if_l77e6IBrVsdGBl1YDY1Bv8zkkLKWP_G3be-ndSe5wF0Mt1lSbh1fe8X90gmxWLtGxMRN5iMJm_XZKToLeIREvBoL2YCYIilupEivuKLIgX9aOpL0m5cSd3N1PCli9oZQ71pXHNHt4FHCtAMz9Yup95s0-M8J2WLZr4WwQ_YaZAvCYC3BN5utxKb8fMd4I4N_zI8xxUDylTOSiBq_aozqTaLOJdhmGEsOK_EOVMENtvYe4gmjj8o1l"
                            },
                            {
                                "cdn_id": 67239,
                                "url": "https://ipv6-c060-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=103&e=1681915675&t=RpZYIN79RhzHqA4jh3QFj3KPzaecqwu3eMRkJTNxH2wKwBgqWWS2anjv_9ZXn6vEkgn52C4fE1rJO-6fTJsC4b5FpUqQYt32Z8IZo-S0znjaaQ-A-4MI0VQMxLIFzwzdSgH61daF6533qNDlQEkOfgIrbWPEwsW7x1fHrzELcSnfkyyKyrdbvZCRCGl3ptqZ5-97Qr6Z7Dj8qh-bgDZJaZlrYKE8ziAd9-Hmvb9UxLxlFhdztsPlb_ATxtsnUkVLN_NW"
                            }
                        ],
                        "textKey": null,
                        "isImage": false
                    },
                    "dfxp-ls-sdh": {
                        "size": 82149,
                        "hashValue": "q99CeLiYfN+lkdQzI5Kr5ukIqsA=",
                        "hashAlgo": "sha1",
                        "urls": [
                            {
                                "cdn_id": 72988,
                                "url": "https://ipv6-c075-sin001-ix.1.oca.nflxvideo.net/?o=1&v=14&e=1681915675&t=3lcdEBgcF6bg6v8aqvDqjeLuIGHiapjDQm7DO8Z__J-D-cdB_AB3A2FFr-xs3roBYpDV9ebyLLggWGmLt4d-Q6artJE7y9wTIPMJnXPiWprycNriuGnxrCFL_P4805Up7-2drsUnnSmpU-t8MGHKs8Om6QOK4n9S65rSwGuUrKVkBekvUpEbWc5Go0r8C5a23y41vVnzI82k8LhNp3584W7lnoGS50wlpX3iTSy59IE97kMMloeVwZaxgZvPnVkN4U3A"
                            },
                            {
                                "cdn_id": 62818,
                                "url": "https://ipv4-c040-sin001-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=6Gvso6vDQI2KdsBef8PzquHK9jIK_jw7bepDCB13kaHyz23foqf9Ogo2kZqu7xWqh4RvwAvZeRmlxVwwEkxdST-WUVD_ZV2XIPC-nkx9NR4eryipkM3Db4gL_KmcdFL7kRN8SSygmwXogBzdzd4IcWM6I9vZh9SGvoqvA4kvVtvy2UiuoqiJeDWh1JdrY43TTGn_poOlp6l8f583wdteoxXFytlOZfqVUdAQSjIbM2kCmPLmJYtffYZpnCy5s-4Td0_6"
                            },
                            {
                                "cdn_id": 58951,
                                "url": "https://ipv6-c030-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=u93dP1f2sEdZWFcbhlSBXUBbb6JDVtkii4iN_8HMw9CGZQ00iHhfwtgc-YE2oMvRpYTKKv1pOjThz932Pxfsb0Nc5895w7Hm-fxu-qNxj32INSgMc4ZOkFTFEQW_2JO0ntk0qOdmRCd21SwTLNlZhXo1O5YDwGHI_pT2AxRqVRkEUrDggnWyPBV_0LydxfaffPrvm2MIBrmgNAHcZYO17q7u5hclWKJcFcs6vsMGBL1NObpDUB3gawvcw71k01xGDTlp"
                            }
                        ],
                        "textKey": null,
                        "isImage": false
                    }
                },
                "rank": 0,
                "hydrated": true,
                "encodingProfileNames": [
                    "dfxp-ls-sdh",
                    "imsc1.1",
                    "simplesdh"
                ],
                "isForcedNarrative": false,
                "isLanguageLeftToRight": true,
                "isNoneTrack": false
            },
            {
                "type": "timedtext",
                "trackType": "PRIMARY",
                "rawTrackType": "subtitles",
                "id": "6e6f6e657c554e4b4e4f574e7c756e6b6e6f776e7c66616c73657c7a682d48616e747c5375627469746c65737c756e6b6e6f776e7c546578747c7072696d6172797c7c7c6e6f6e657c30",
                "new_track_id": "T:2:0;1;zh-Hant;0;0;0;",
                "language": "zh-Hant",
                "languageDescription": "繁体中文",
                "downloadableIds": {
                    "imsc1.1": "1947011364",
                    "nflx-cmisc": "1947011830"
                },
                "ttDownloadables": {
                    "imsc1.1": {
                        "size": 70763,
                        "hashValue": "xNZNcsTLr6cqWm6ON+1ItzyUX8U=",
                        "hashAlgo": "sha1",
                        "urls": [
                            {
                                "cdn_id": 72988,
                                "url": "https://ipv6-c075-sin001-ix.1.oca.nflxvideo.net/?o=1&v=14&e=1681915675&t=P5uLHT8LaSJ1X_IPzPJC5VghVBgbA1moeyZ4UrtT_a8mJp-z64FB8TT4wtyJVUSvoH9ZAkO0wgOqv3ys_3MRevqo1lYFRzEm5nIJsaYXToH5t_f1oosEgqNM0g05l3kVe1FvTcRAp-8hyv8XjrIpcFIY_ytio5NL_OU6Acr6cQ6eWAVjYlsViDGIbUZC8iTDnMwRE4i4CW20fnZ4R33-vUGb2u-WKUsxq-BPoKvIWmCWpzEXcGmz_wJ9ZzN9nv69lAj4aAZAvA"
                            },
                            {
                                "cdn_id": 67239,
                                "url": "https://ipv4-c060-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=103&e=1681915675&t=mLX7AFeYoTL3wgmM0O7M6uK9tOorUEvnelChp7GS2WBZoOlkYGNTRknDf0x5ajP3OuUlBRNAFOChpjsiCrZ-lkMHxnHw3_fjNC7QNW9zFdic-LfJgS56PkEVt3D7o5Kb3vy8f8m_xncbuH9Y_ou9o4OJl6wvnzOK9FQuamiHjojdyK66lsAHtDE29lnIAnX-QSWbYMH8C9RzbC37lsZ2otgrf0pIIM_pBSjemX-qIHnFKce3OywpdAkKBOPt554vmF5Nimi8JA"
                            },
                            {
                                "cdn_id": 59677,
                                "url": "https://ipv6-c012-lax009-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=E4W1v9T_AVGoFTmK3y1WRaN-w7Xcn3xMREUw2HmtB_pV19YW6oBYDitokhamDiZCBIwCrbe9rut14EdSiIKtCZSwrGnIWo1VVrpmJeKIg52jNy27Rc8ibJzBXhvODSjvLpFyT8A4dNAh5NK3v3OyKxiX_USptxzbAr5vR0kfbz2Wb_dpc165P0RFVhqZqG9KeDijrjFFQrjiE4SjDznagjp2EvvLguWRWE4R_G4sJMP9QX9FkKYFOo3XGeayb6A3Ubqw5HICkg"
                            }
                        ],
                        "textKey": null,
                        "isImage": false
                    },
                    "nflx-cmisc": {
                        "size": 10058018,
                        "hashValue": "SyKygKJGQs9KgVjN6uPCj145dMo=",
                        "hashAlgo": "sha1",
                        "id": "1947011830",
                        "urls": [
                            {
                                "cdn_id": 67303,
                                "url": "https://ipv6-c062-sin001-ix.1.oca.nflxvideo.net/?o=1&v=102&e=1681915675&t=yYEZkxB4aEcV54WkOGASQ3LIKtBcLPPrlro2H9sxfXPVNgAoovOhRwBb3mRkzRR3N4XjZ3gM8mTB36_-t4tZNdUJSTm02kYF9qGaupRylZ6IRGE8HMoGzgUhQnELfVnsC--4DrOpY3DKO_H1K9euhe5NLQBPTJps3N0lFsZFQ_NqgG6XS5D12dkPujwo_iOF9tWM2pykTh3KcFOgDZEX_2xYxeOyguNysVGtSeFJJSWdjVe7soUSVFdHPQSjdSrrbhU"
                            },
                            {
                                "cdn_id": 73092,
                                "url": "https://ipv4-c069-sin001-ix.1.oca.nflxvideo.net/?o=1&v=13&e=1681915675&t=MKPXOiU8POly7PEwKvBjugNrq15EFroZtDG30sa-gw9vD8gkMaImxS1AwpDBYWdXY9wgjnqhhoHCya7-R76wXV0_g7zLHi19Qe1eruKUSOo8CtGi3Ih5EpRUXTU05_a7vOeKIycrQzjhaLwmZpcvRW4j7-rxOvnRiMSrNuIn4spCr51p3dXnyGeAduz9tSNBAqrkcpVRKjTnReWHRUbnp9QSdUOMX2M_Q2VAx-HKIE2o3ysyto3FH9WYUBDA4JSklNE"
                            },
                            {
                                "cdn_id": 67239,
                                "url": "https://ipv6-c060-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=103&e=1681915675&t=HcKjYvbRb9OfID00QNpPp27b6PTb4DfTxknw9I8GD1glF782QYKpwj4VOwF3HtcjzWmgHDPq0m7oGNmv2y0rv9gBNRqsnvUE7DMB-pKnDbiy_ODCP9P2xelqTlzfjQRuhVDI3X7vJTflzzQYvKbXt62YyI_2j16lms9p7OJOz-rfJ0UgKEJ9bi9Mj-ZAdKYqUv76k7dLr7_amKO8Zv_D5LLfs2fmfxHiNlgkxLHH4BbR_IkX0ubu50oR5bjS7e8190U"
                            }
                        ],
                        "width": 1920,
                        "height": 1080,
                        "midxSize": 354,
                        "midxOffset": 10026939,
                        "textKey": null,
                        "isImage": true
                    }
                },
                "rank": 1,
                "hydrated": true,
                "encodingProfileNames": [
                    "imsc1.1",
                    "nflx-cmisc"
                ],
                "isForcedNarrative": false,
                "isLanguageLeftToRight": true,
                "isNoneTrack": false
            }
        ],
        "trickplays": [
            {
                "id": "449208437",
                "interval": 10,
                "pixelsAspectX": 1,
                "pixelsAspectY": 1,
                "width": 240,
                "height": 91,
                "size": 982325,
                "downloadable_id": "449208437",
                "urls": [
                    "https://occ-0-64-58.1.nflxso.net/tp/tpa4/437/1631226410752816385.bif"
                ]
            },
            {
                "id": "449208989",
                "interval": 10,
                "pixelsAspectX": 1,
                "pixelsAspectY": 1,
                "width": 320,
                "height": 134,
                "size": 1577547,
                "downloadable_id": "449208989",
                "urls": [
                    "https://occ-0-64-58.1.nflxso.net/tp/tpa4/989/1631226411096749313.bif"
                ]
            }
        ],
        "type": "standard",
        "urlExpirationDuration": 43199947,
        "viewableType": "EPISODE",
        "badgingInfo": {
            "dolbyDigitalAudio": false,
            "hdrVideo": false,
            "dolbyVisionVideo": false,
            "ultraHdVideo": false,
            "dolbyAtmosAudio": false,
            "assistiveAudio": false,
            "sdVideo": true,
            "hdVideo": true,
            "3dVideo": false
        },
        "recommendedMedia": {
            "videoTrackId": "V:2:1;2;;default;-1;none;-1;",
            "audioTrackId": "A:2:1;2;zh;1;0;",
            "timedTextTrackId": "T:2:1;1;NONE;0;1;0;"
        },
        "partiallyHydrated": true,
        "maxRecommendedAudioRank": 0,
        "maxRecommendedTextRank": 1,
        "dpsid": null,
        "auxiliaryManifests": [],
        "adverts": {
            "adBreaks": []
        },
        "streamingType": "VOD",
        "audio_tracks": [
            {
                "trackType": "PRIMARY",
                "rawTrackType": "primary",
                "channels": "2.0",
                "surroundFormatLabel": "2.0",
                "channelsFormat": "2.0",
                "language": "zh",
                "languageDescription": "普通话 [原始]",
                "disallowedSubtitleTracks": [],
                "track_id": "7a687c322e307c5072696d6172797c747275657c6e6f6e657c756e6b6e6f776e7c756e6b6e6f776e7c417564696f7c756e6b6e6f776e7c7c7c6e6f6e657c30",
                "id": "7a687c322e307c5072696d6172797c747275657c6e6f6e657c756e6b6e6f776e7c756e6b6e6f776e7c417564696f7c756e6b6e6f776e7c7c7c6e6f6e657c30",
                "new_track_id": "A:2:1;2;zh;1;0;",
                "type": 0,
                "profileType": "AbstractDynamicEnum{name='AUDIO'}",
                "defaultTimedText": null,
                "stereo": false,
                "profile": "heaac-2-dash",
                "codecName": "AAC",
                "bitrates": [
                    64,
                    96
                ],
                "streams": [
                    {
                        "trackType": "PRIMARY",
                        "content_profile": "heaac-2-dash",
                        "bitrate": 64,
                        "size": 21566177,
                        "downloadable_id": "450425241",
                        "new_stream_id": "450425241",
                        "type": 0,
                        "channels": "2.0",
                        "surroundFormatLabel": "2.0",
                        "channelsFormat": "2.0",
                        "language": "zh",
                        "tags": [],
                        "urls": [
                            {
                                "cdn_id": 67303,
                                "url": "https://ipv6-c062-sin001-ix.1.oca.nflxvideo.net/?o=1&v=102&e=1681915675&t=D0eM6cZi4Mr6KwrT6s2qR-4Wy290x_khppW5870UwbnzriRSV6aB2Ws_kYnUdVN0rnyeY9jW74pKJuGcOUA0zS1sYC0O1Oh9kS4SC4LUWfX6UYJcfWrvEvOJ0GegScYmpJHbHc0Q20PN0bUve0T5Zgx-pSmbhR3vKuHPJ4ka1DO4Fd9imHzy-L17rs214WHcW_YeFA9xUcFXKTIlAjk2sQtydGmqqytNjat7vZPkAqOcPBi7CrZh0Ita2x03TDsvChTL"
                            },
                            {
                                "cdn_id": 73092,
                                "url": "https://ipv4-c069-sin001-ix.1.oca.nflxvideo.net/?o=1&v=13&e=1681915675&t=gfpEWdSjeCsFuyPnZzVzCPLbHTanq7yT-OeoDUZ_aR_2v0GYwep4we9ZOsJRNJhI8OV-pube8m7nqA3lo832-E0uGayyYVWW_8w9LbZoWjOzXHIn9305vHybIgvO3SlD30VJFpwxewXcHG0XJJB0f5L_kfARXOn7Oq31rgtt70opGkbdT7eKa_AWWo10RdgtxX-u0ObtP0ByM4LsaGmslbfbANxSC4ivhi7cG0V2Fk8sDCxU3xHNdutbeQND2J4gIc6o"
                            },
                            {
                                "cdn_id": 67239,
                                "url": "https://ipv6-c060-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=103&e=1681915675&t=L63pbDytzJeW2uw992mDsWYo_93I36P-dmT-HTc2HlV6jFegLIh6aI5SQEX9TI2k1cinwl2igNd1tMN7Xca2iA8mGSD_qKiQz5Hl-N3_1czGqHWm6d-Tf_gO8qpaLkpUzu2DpRynKFkdHo21cwOUHMG6bTPTvyTqpZsbO_YmUVrGu7-AYrXDFdRvSW3cIkaKD2VOAcve5_XOfJE1GKcFHFMm6lol9_a226H7-IH1zISD4EbAZdaUQ93bb_eUYA0Zomxe"
                            }
                        ],
                        "moov": {
                            "offset": 241,
                            "size": 662
                        },
                        "sidx": {
                            "offset": 903,
                            "size": 15460
                        },
                        "ssix": {
                            "offset": 16363,
                            "size": 15436
                        },
                        "audioKey": null,
                        "isDrm": false
                    },
                    {
                        "trackType": "PRIMARY",
                        "content_profile": "heaac-2-dash",
                        "bitrate": 96,
                        "size": 31845431,
                        "downloadable_id": "450424664",
                        "new_stream_id": "450424664",
                        "type": 0,
                        "channels": "2.0",
                        "surroundFormatLabel": "2.0",
                        "channelsFormat": "2.0",
                        "language": "zh",
                        "tags": [],
                        "urls": [
                            {
                                "cdn_id": 72988,
                                "url": "https://ipv6-c075-sin001-ix.1.oca.nflxvideo.net/?o=1&v=14&e=1681915675&t=Tg5vk6tG-Qum3P17QDFQfkNZJT5Og35UCCpSmwc5ehcjkaSQRFQthdSHg0yO-NEGhVTfcIrCuix_7ttDTar0vR1WgzTIhDWCD6Wc2yJ-fv8KKLrIWmbniOq2rdoN506MXynpcGZVqBtVHfEbvsi6A5JMC5UNFerEV3h4VmxgzkG0BpTllq9mqC5jO1cvCSbl9Lb8QWWAgA-7xAgz92l2BuxMF9cIuShB_dFGjgWiyn_TpCLTWR8b0BEEjfIqSS9YS2Fj"
                            },
                            {
                                "cdn_id": 73092,
                                "url": "https://ipv4-c069-sin001-ix.1.oca.nflxvideo.net/?o=1&v=13&e=1681915675&t=x-GNeSWzuNVLk1Y3uWe3tVKiPgDjNU-tAO0XD8q6BDME-4Gfx1bASuv7tjXCyvVCjcpzQbdVhQ5Rl0hvkKZz_nlVcKfbEk3ch78g-4sXkvJJzULVgqmrRpJEDYj4mc0IumvpbOOQoDiNWSTqJM0vXagk3aOErRoikFbTFhhs5HuYeVy_Ab6vzvS1Jty63Dbx760AUEpBg20oZbf8Ru5UcxXr6oVaGHwPycRjoWx6_7ia4Ln0EqEn4NfxExQ_jI8ZdqAr"
                            },
                            {
                                "cdn_id": 67239,
                                "url": "https://ipv6-c060-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=103&e=1681915675&t=j3Tnizc5IvjHiRZn7QVh7K5WXA4qHKxIx3H96-OitkNg34MSBjb-hUHW4QCggPC0SbYC3HRwR-zsofPXxDqjPS1i_i0UrihWmgacdynpRK8hkQenZ5t5X-nFXiR6-5RL1V-rm6m0Ks-zLzonfeDxRJiZjkbIainCehPJDA1PaHJPhFb60SZK_IAHLpNj5Yqm46UrznI9gWV1hKojucJARB15XTiGyC0dEVrUYnWVnGbjqeLkv0U5gABtt6dvAk_ogjU4"
                            }
                        ],
                        "moov": {
                            "offset": 241,
                            "size": 662
                        },
                        "sidx": {
                            "offset": 903,
                            "size": 15460
                        },
                        "ssix": {
                            "offset": 16363,
                            "size": 15436
                        },
                        "audioKey": null,
                        "isDrm": false
                    },
                    {
                        "trackType": "PRIMARY",
                        "content_profile": "heaac-2hq-dash",
                        "bitrate": 128,
                        "size": 42124684,
                        "downloadable_id": "450333356",
                        "new_stream_id": "450333356",
                        "type": 0,
                        "channels": "2.0",
                        "surroundFormatLabel": "2.0",
                        "channelsFormat": "2.0",
                        "language": "zh",
                        "tags": [],
                        "urls": [
                            {
                                "cdn_id": 72988,
                                "url": "https://ipv6-c075-sin001-ix.1.oca.nflxvideo.net/?o=1&v=14&e=1681915675&t=PhP8wuZYQjUGRYQthaJZpLjEuKBOZW-UVFyklcgdee2H844_JzG9IMWvD9GfYjsPzy42ZASz3Z9GEeFhaUTcCLH1X-CorrJbv34NVQTt-zM1Ne1XdBH2LgVrvZycrpdfSpgv8OOE4zG-nsy2b_3Q845cDNRaTo0KUe3ARATNW31MCAB_tMbz8_vYan3tHV3HmTvrWuQSMjQ9ZAtEGKlfNBCJph8aDjeXgClE6cGAc7nrnOEU10-u8rb3V6TKxhsLOYvW3g"
                            },
                            {
                                "cdn_id": 62817,
                                "url": "https://ipv4-c039-sin001-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=yULaGW3RcP0wXOvHTG-s8PXsFpZSOmop1xq1eATGYcrrUOA0Tlloh3yWVvRc3uFa5ZIoy_uB_Lm-2vWbJG_QfqfYPSJgeE2ROO4Z-wtWdycHioe_MO-21QKSw9WKEYEcCchaIMN37CDPX7oGCruf-N7vSbqwNAn_gpXoZsCbzNQm75xyyctrkIs76ZOIk4chZvjxBd19nQqpe2OzzkMxHlqvCcxBf_l5FUZRx4Vb8DPLsa0UGv7b1-88ivHzctf3cz74Ig"
                            },
                            {
                                "cdn_id": 58951,
                                "url": "https://ipv6-c030-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=tsk1hSsPUdLmMl5TA6h7FCcoW4DlcTzppjFNSuXP24W45dZj7PPUOcDRSn_RKQ-RswCurs2Idc20afhjnatO-3EBCMS_dEtyb_pS5xNqSnRoWbLbUgY0OJHZvIfwYwmvRmSt3jJ8w3w0qweqjfxo7ALe2Dtm1rPcjy_BD1IyFbRWUhF0e3hiF39TGR4RSvSxwTLxnYDYsMLaGUqSnmMBfG-ybRapndM5XmDQERt_uil0YuPzi7C4xrEIxcdUQFrNaDsBAQ"
                            }
                        ],
                        "moov": {
                            "offset": 241,
                            "size": 662
                        },
                        "sidx": {
                            "offset": 903,
                            "size": 15460
                        },
                        "ssix": {
                            "offset": 16363,
                            "size": 15436
                        },
                        "audioKey": null,
                        "isDrm": false
                    }
                ],
                "rank": 0,
                "offTrackDisallowed": false,
                "hydrated": true,
                "allowedVideoTrackId": "",
                "isNative": true,
                "isNoneTrack": false
            }
        ],
        "isSupplemental": false,
        "isAd": false,
        "isBranching": false,
        "video_tracks": [
            {
                "trackType": "PRIMARY",
                "track_id": "6e6f6e657c554e4b4e4f574e7c756e6b6e6f776e7c66616c73657c6e6f6e657c756e6b6e6f776e7c32447c566964656f7c756e6b6e6f776e7c7c7c64656661756c74",
                "new_track_id": "V:2:1;2;;default;-1;none;-1;",
                "dimensionsCount": 2,
                "dimensionsLabel": "2D",
                "stereo": false,
                "profileType": "AbstractDynamicEnum{name='VIDEO'}",
                "type": 1,
                "ict": false,
                "hasClearProfile": false,
                "hasDrmProfile": true,
                "hasClearStreams": false,
                "hasDrmStreams": true,
                "groupName": "default",
                "streams": [
                    {
                        "trackType": "PRIMARY",
                        "content_profile": "vp9-profile0-L30-dash-cenc",
                        "bitrate": 138,
                        "peakBitrate": 758,
                        "dimensionsCount": 2,
                        "dimensionsLabel": "2D",
                        "drmHeaderId": "0000000007ea3e960000000000000000",
                        "pix_w": 1,
                        "pix_h": 1,
                        "res_w": 768,
                        "res_h": 432,
                        "framerate_value": 25,
                        "framerate_scale": 1,
                        "size": 45082519,
                        "startByteOffset": 15146,
                        "vmaf": 76,
                        "segmentVmaf": [],
                        "crop_x": 0,
                        "crop_y": 54,
                        "crop_w": 768,
                        "crop_h": 324,
                        "downloadable_id": "2107992205",
                        "tags": [
                            "AL1",
                            "EVE",
                            "MCCLEAREN_VP9",
                            "POI",
                            "ladder"
                        ],
                        "new_stream_id": "todo",
                        "type": 1,
                        "urls": [
                            {
                                "cdn_id": 67303,
                                "url": "https://ipv6-c062-sin001-ix.1.oca.nflxvideo.net/?o=1&v=102&e=1681915675&t=Ss_hJdFQscNEhpChy-CzfUdNvzzBm4vnYXhV07W1t4C9a69i4PrQaM-tC-p1PgWG6UH_sl1xUMG2PYv79ewJdvCpmLSdinK83tNH7YTeQl4ul2CwT0nUyuCFH216meIcNU4awl-l3X2HnB2un2akRGM3XSpF3ZabPeOO0kg0MIvgQapIXXqViZWmHKeDygy2QDrP1mduIyxek6atpJyQP019HJXXyf1d38qF0XDEAwy0N35zi0BZ92WuTa7pBdMi2HcWfDg"
                            },
                            {
                                "cdn_id": 73092,
                                "url": "https://ipv4-c069-sin001-ix.1.oca.nflxvideo.net/?o=1&v=13&e=1681915675&t=abCUnaaMQtE27MPRQ4ns4wG261T-Bw8maL-blofSglGq8Yd0M9cV4osNT6O0J6WNGDXsitx-r1f4iwJwSzUj_XkKv4aY1dTeogfaZi82kpgiSbpMJmB-azcwBwkmtcd8i1fGenmLJ04n-jUx295FP4KB_Tc9Q9eF80oT7qM6Lf3cIUqYS8vqbW7-oP-gYBCBk0Y6V4q8vRqtJ-PIo3SP1kZjfY33dIm_C9Z9W7rV2dusbM9pzBLMBNIyD8ZXuoVyQVya9b0"
                            },
                            {
                                "cdn_id": 58951,
                                "url": "https://ipv6-c030-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=5P9FpgBEKQ2Ga90DGSkUvK8dIFq-hR3ZUlV0O1KIsY_BGMTtSbm5jbUXhFIWat38IAqw6lOTmGbX11hgf11303Y6HTz_eZNe9SVQH0XtJoXyvJrXc9cJLMfjRKOko_Ar-9JbFJLi9OYf3iS8YM74MflPL2U-zkiUQWiAyHNR0WIpmsuqb0rAZGoGRBxRNxB3J7fwH6jwT4hy1t6SKRXapSN1o3eZGVPFhQY64Kq6PK9UMu9Wl48_iYBa67XxGp4vg7wmSi8"
                            }
                        ],
                        "moov": {
                            "offset": 109,
                            "size": 1741
                        },
                        "sidx": {
                            "offset": 1850,
                            "size": 6656
                        },
                        "ssix": {
                            "offset": 8506,
                            "size": 6640
                        },
                        "isDrm": true
                    },
                    {
                        "trackType": "PRIMARY",
                        "content_profile": "vp9-profile0-L30-dash-cenc",
                        "bitrate": 158,
                        "peakBitrate": 634,
                        "dimensionsCount": 2,
                        "dimensionsLabel": "2D",
                        "drmHeaderId": "0000000007ea3e960000000000000000",
                        "pix_w": 1,
                        "pix_h": 1,
                        "res_w": 960,
                        "res_h": 540,
                        "framerate_value": 25,
                        "framerate_scale": 1,
                        "size": 51486508,
                        "startByteOffset": 15146,
                        "vmaf": 79,
                        "segmentVmaf": [],
                        "crop_x": 0,
                        "crop_y": 66,
                        "crop_w": 960,
                        "crop_h": 406,
                        "downloadable_id": "2108042817",
                        "tags": [
                            "AL1",
                            "EVE",
                            "MCCLEAREN_VP9",
                            "POI",
                            "ladder"
                        ],
                        "new_stream_id": "todo",
                        "type": 1,
                        "urls": [
                            {
                                "cdn_id": 67303,
                                "url": "https://ipv6-c062-sin001-ix.1.oca.nflxvideo.net/?o=1&v=102&e=1681915675&t=p8GAebnTjX2uJZJlplSp7B0PYcvwE3m0_MtXtMBfdbEimXdfboo-mqww1rYDr2zV_CNuQaeqqDQEHakUUklN7NMhqJBI6rkKAmT4ilIUk96eb535gy5ZK_I0aHXTLkyBOTQ-csevd5GBCODR3-8IB7DwGvImOUaabBK1PxaoEkp2X8ychIN_xKpb5y8E9XpoeppededumwHYRaAGfigdobXvxJgq4NvZ5v_WaGVfI0FD0dsBpfp6nlX5KI-E2C3XM8HMRu8"
                            },
                            {
                                "cdn_id": 73092,
                                "url": "https://ipv4-c069-sin001-ix.1.oca.nflxvideo.net/?o=1&v=13&e=1681915675&t=nKP1uQCGL4OtBcSx5ztXIa59j8-dTDhwZd_wXMPsAtom7FbMoGv-9yqdBns55bRSdnOf_-aPk-sHl16k8AA5IqWlyRdezdLlfCsXg5SWfC5_4tO6assWb6uUeivmnOD942AdtGHGTMd8J_KCDf4RalNkiz-y53rKG0wvtSFIwZHFihbzj9L73XiUVVG7-dhHuStXt1FiWj3HLgGVAy9keg2SXpxnptHajVdtMrkzgiRmeg9aMVqg-TEVLaMDhLQ-becNybQ"
                            },
                            {
                                "cdn_id": 58951,
                                "url": "https://ipv6-c030-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=dcCfigtyC-q8dQxwR_eWvIHEySG3-OTgNvt_In4VobCJP2tayxi1n7VwpaiG1og80JD1BRwQYlgqDGFV19kRVdctQhF4wPlZK1c2TTyh0v8YU1lQbtOVav4U_Nfmu1g6jIJxeNdQzE4XbVrRajVCqYO4KvJtOxJxi0W6tgIiVrt0h60GApD3Zew8rktQDTCL1-V7fH3PvcRfziWYDej_c_PjgO7vnWMWtBzTHThphol-WcBxnStbvDwzJMjeiNWsB3l2i-g"
                            }
                        ],
                        "moov": {
                            "offset": 109,
                            "size": 1741
                        },
                        "sidx": {
                            "offset": 1850,
                            "size": 6656
                        },
                        "ssix": {
                            "offset": 8506,
                            "size": 6640
                        },
                        "isDrm": true
                    },
                    {
                        "trackType": "PRIMARY",
                        "content_profile": "vp9-profile0-L30-dash-cenc",
                        "bitrate": 255,
                        "peakBitrate": 1322,
                        "dimensionsCount": 2,
                        "dimensionsLabel": "2D",
                        "drmHeaderId": "0000000007ea3e960000000000000000",
                        "pix_w": 1,
                        "pix_h": 1,
                        "res_w": 960,
                        "res_h": 540,
                        "framerate_value": 25,
                        "framerate_scale": 1,
                        "size": 82625636,
                        "startByteOffset": 15146,
                        "vmaf": 84,
                        "segmentVmaf": [],
                        "crop_x": 0,
                        "crop_y": 66,
                        "crop_w": 960,
                        "crop_h": 404,
                        "downloadable_id": "2107804031",
                        "tags": [
                            "AL1",
                            "EVE",
                            "MCCLEAREN_VP9",
                            "POI",
                            "ladder"
                        ],
                        "new_stream_id": "todo",
                        "type": 1,
                        "urls": [
                            {
                                "cdn_id": 67303,
                                "url": "https://ipv6-c062-sin001-ix.1.oca.nflxvideo.net/?o=1&v=102&e=1681915675&t=oQAtOVNqTq2Yqli3zigytOPbl6Hm_wOz9xw_wEnIjMaKycoxelEpbDTO64AN6c6-PsyZ2m2d81B9AB8vLI-q0oV_QbAT4ni0edA2gEalwxdowq2D1Z5lmJXzOteNIdXsCrLwcN1Ozbdbwshu0b0p2yPyQEka8KBUGX0XDlFEDUedWH4q6CHbgd_--9YOcG0JM2_rNuc4I1YNkNL1Rm7kCNtTlPnipbqr3krUbcmZLOkl_5MiSIUObl3q21rkV61AjHRLTqo"
                            },
                            {
                                "cdn_id": 73092,
                                "url": "https://ipv4-c069-sin001-ix.1.oca.nflxvideo.net/?o=1&v=13&e=1681915675&t=p_B_mbB1Joq0u1adMNp-cRJJ3av7rnkarPie97XL6yyS1DKdp1NuoO36QBezpYLFDgD019B_B9Z-9-fZuCvyf17VvIXOgyzsdodHf3M_AbsZqLxf38e4VfwBUSon9eZWUtbWrUj5bq75RqStdROQ3YWxki05suGWG2XbNesDX6cJbHNKMOHE1TBLdFkAPrhvxBGQq8O_Vwic_KXPXQqnmY5zTg1MRqhvRU5wPwKUMyEnRxSsdVHpf7jXNwca8lyOz4B6b8I"
                            },
                            {
                                "cdn_id": 58951,
                                "url": "https://ipv6-c030-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=dXI5hqnABfzSZjO6hLz7lFxY4Ofa3Cg_ANssW4-Cyk0JYRL4TDaVV84o5sxYfgc79MtZDlfZvF5PFxLzC13FekvTW-xFxvZNEDMDV-6ElkU-hocBJe0Fj-U6bEg1mKE7rshhb3Oxn1z4um27UG0GRHaY4WOtY59kGDVXVVS0lCRDnW2eLNKyjTqCl5TX0rRCUKm33q8wSkCBNVAYj2K3luqz3Z1HDFzRqlJ7gJ52y73KjJbMmsYmhIrYrRH_DSzE0YChQug"
                            }
                        ],
                        "moov": {
                            "offset": 109,
                            "size": 1741
                        },
                        "sidx": {
                            "offset": 1850,
                            "size": 6656
                        },
                        "ssix": {
                            "offset": 8506,
                            "size": 6640
                        },
                        "isDrm": true
                    },
                    {
                        "trackType": "PRIMARY",
                        "content_profile": "vp9-profile0-L30-dash-cenc",
                        "bitrate": 368,
                        "peakBitrate": 1985,
                        "dimensionsCount": 2,
                        "dimensionsLabel": "2D",
                        "drmHeaderId": "0000000007ea3e960000000000000000",
                        "pix_w": 1,
                        "pix_h": 1,
                        "res_w": 960,
                        "res_h": 540,
                        "framerate_value": 25,
                        "framerate_scale": 1,
                        "size": 118947781,
                        "startByteOffset": 15146,
                        "vmaf": 86,
                        "segmentVmaf": [],
                        "crop_x": 0,
                        "crop_y": 70,
                        "crop_w": 960,
                        "crop_h": 400,
                        "downloadable_id": "2108041778",
                        "tags": [
                            "AL1",
                            "EVE",
                            "MCCLEAREN_VP9",
                            "POI",
                            "ladder"
                        ],
                        "new_stream_id": "todo",
                        "type": 1,
                        "urls": [
                            {
                                "cdn_id": 72988,
                                "url": "https://ipv6-c075-sin001-ix.1.oca.nflxvideo.net/?o=1&v=14&e=1681915675&t=BSSgL5bJb-NyvbhH5UKg7D-dFOpML75YN0LVtiGN6xWl0tNIgH0mSvRA9pG1qtsLtujW81mGuB09OvAmLEVRtaAZWxiBsmKSoSQaEdA6X6tFwxt1uuChcGK9dNeZOSHS5ZHRIsvXgeU5IHmFzVAZSbp3IdK4LynXwtVa4dj5KZaB7tp2A2GVWDgoCzaxyNwajNPRM3EzlhLKX4ssTjYERjpbBoDGqUXUjiJush2ozKxrvxXpI8n7AO9SaL772F2CdAgCbkY"
                            },
                            {
                                "cdn_id": 73092,
                                "url": "https://ipv4-c069-sin001-ix.1.oca.nflxvideo.net/?o=1&v=13&e=1681915675&t=mkp_9Zl3V5TNnKF9gJI_Ez3S--44XYIay6Iue7eDYV5IxRx8fi2qxNvNw2IghUnphn-vK8u-XTKIcEwb27ZnreKnLuG7GQ-0fIuglhA0yLzYRM_28klwDh2bGxtc3DGJLciEq2neyz3-2nCm6j5cEkSHSlw1jBWIi6V6z40dSmc18pWhl5GtLmQzLY0RPxQSaCJaBMZZMSnCbr8Cyp-8zPARNpmAQEeJCbYJ-LyFA0MqFN96jHDIKmleNPSbTVTy5CjOndQ"
                            },
                            {
                                "cdn_id": 67239,
                                "url": "https://ipv6-c060-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=103&e=1681915675&t=nEYv_JXPkf4aDjDN3uvwFVgQwQUp3N5IhFCzgkQ3gd1Qtjxtudss19LLcnPHr-nW2Sz0bi0QmVyqHBfRI7FZjOJWyppkUuJkYmqdEHtvB_UwSvcjUTPbM0hYvQT4KHt4SrULtPlzJzauHvK_MhGoay5UkGU2eKnGLFb2lNLwRhu23XJGGSkW54R2OE6V9n1cLBbqDE1f6iaYdI2t-mVnPogkwlrG6Hbo99n5f1OBo0OX1QRxn72yPhpX5fjjlxxQ_F0A6ZU"
                            }
                        ],
                        "moov": {
                            "offset": 109,
                            "size": 1741
                        },
                        "sidx": {
                            "offset": 1850,
                            "size": 6656
                        },
                        "ssix": {
                            "offset": 8506,
                            "size": 6640
                        },
                        "isDrm": true
                    },
                    {
                        "trackType": "PRIMARY",
                        "content_profile": "vp9-profile0-L31-dash-cenc",
                        "bitrate": 522,
                        "peakBitrate": 2665,
                        "dimensionsCount": 2,
                        "dimensionsLabel": "2D",
                        "drmHeaderId": "0000000007ea3e980000000000000000",
                        "pix_w": 1,
                        "pix_h": 1,
                        "res_w": 1280,
                        "res_h": 720,
                        "framerate_value": 25,
                        "framerate_scale": 1,
                        "size": 168364802,
                        "startByteOffset": 15146,
                        "vmaf": 92,
                        "segmentVmaf": [],
                        "crop_x": 0,
                        "crop_y": 92,
                        "crop_w": 1280,
                        "crop_h": 538,
                        "downloadable_id": "2107656152",
                        "tags": [
                            "AL1",
                            "EVE",
                            "MCCLEAREN_VP9",
                            "POI",
                            "ladder"
                        ],
                        "new_stream_id": "todo",
                        "type": 1,
                        "urls": [
                            {
                                "cdn_id": 72988,
                                "url": "https://ipv6-c075-sin001-ix.1.oca.nflxvideo.net/?o=1&v=14&e=1681915675&t=6SSgQ9o0syys6U4hpKEqfu4HkPgv4cgTotbwglYSwiN2eDz3mZ6zHP_BH0zIv3WVBWXmm2NS5ApPwHiTvNRPVGfKrAU6EyFxTcdG85JdgIEdG-keXFAbxKyBiXSDcfbXejKscKn4PwCLC06w-YK76zJM8QDMN8Kcvhh9CEI-GobmMJVjr-tUm9pgwGPjFvIDauETPsbP_XNPtl6dwCoKnq8OSR4pxq8fK4Kbbs0goaj7lH8WE0eTPArAY1_GvK1LYUF8lrY"
                            },
                            {
                                "cdn_id": 67239,
                                "url": "https://ipv4-c060-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=103&e=1681915675&t=SeKt0Y5GtyPieCtAga6RFuST38SPr0cI0gTpypm_Urp1thOj-gIZ0WQihe7pJBcxECHnYkvMuAzuD4GCRHmLIKCis_eLnJAz5TVdhRXiWLoH6tv7173LB-jWfC68-7lcXX5hMtMAURTyHUJEGHKRuI9vt6VRM4qVee3Rfn2YMZPspTeD3wyOrKhTPYQ6gcS0dS_mGSTBM-fh32kCST7zGybRr2jXaRg1_V6aa8Jxe6uPxmO-mqMw8x1ku-ruBOCOeVw-WJk"
                            },
                            {
                                "cdn_id": 59677,
                                "url": "https://ipv6-c012-lax009-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=kCBlYYqkt_FMU3TbVRzsMHEwmUqPVAqOcPW2grAhJfG6DwFnoiI7636BNhg92R43JCcmo5X9bBEmHUruz9CL99S0NEZ21l2aqnhHOcVw4n6ZZ6KcWKURustOX17l-z44UPZSF5dpVASJv4CBbDZiot6koH7S8W8TLe9Fwmrj6TZ1EXeNbFEsM0GJeE0dKSXKVAGh92BO1jP08ipthIitbsCwD3jC7peZqV4H8HzMgH6htYZVHarx2WfjoKbwZyUfj2MSBYw"
                            }
                        ],
                        "moov": {
                            "offset": 109,
                            "size": 1741
                        },
                        "sidx": {
                            "offset": 1850,
                            "size": 6656
                        },
                        "ssix": {
                            "offset": 8506,
                            "size": 6640
                        },
                        "isDrm": true
                    },
                    {
                        "trackType": "PRIMARY",
                        "content_profile": "vp9-profile0-L40-dash-cenc",
                        "bitrate": 929,
                        "peakBitrate": 4504,
                        "dimensionsCount": 2,
                        "dimensionsLabel": "2D",
                        "drmHeaderId": "0000000007ea3e980000000000000000",
                        "pix_w": 1,
                        "pix_h": 1,
                        "res_w": 1920,
                        "res_h": 1080,
                        "framerate_value": 25,
                        "framerate_scale": 1,
                        "size": 299307704,
                        "startByteOffset": 15146,
                        "vmaf": 96,
                        "segmentVmaf": [],
                        "crop_x": 0,
                        "crop_y": 138,
                        "crop_w": 1920,
                        "crop_h": 804,
                        "downloadable_id": "2108076049",
                        "tags": [
                            "AL1",
                            "EVE",
                            "MCCLEAREN_VP9",
                            "POI",
                            "ladder"
                        ],
                        "new_stream_id": "todo",
                        "type": 1,
                        "urls": [
                            {
                                "cdn_id": 72988,
                                "url": "https://ipv6-c075-sin001-ix.1.oca.nflxvideo.net/?o=1&v=14&e=1681915675&t=d3WdtwMfGknbhoFNqFZhHi2Q2AwV7wgYSf5DwrdVajrU9nIivZp3yKHJj5g_GwXIEg6xsMYQbAw1eVERRhf9BoLulO-d6vuR-8qkF5l7U0EUUIIXU3CXybCS3iIW665tIDv73GgnVOu6AWT4JkwJVuIsRnUzcqYgqBMw_4CgFEWpojvqc5gxhjN78onMiuM7XrfX1MYRvpU4mSgdQ-ZnNfr7jIZ1XFFpwlmu_cIVxs6tyGVuZqktU9glHypNWI6onMqAwww"
                            },
                            {
                                "cdn_id": 67239,
                                "url": "https://ipv4-c060-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=103&e=1681915675&t=0Vz-i62YpDg2TlxzVkKB9gkWkhABD4YddL7U2f02ZhbHJMpCko2WGriGAc9zRVGOq7JZTMiw7z2M8tRmt4g5tnHWByKl6qrj3_xNNcdebb6fyG37eb54XIPnMOHw9PX8n2l9DbdpST0ZQETapspX5Jhn6dRg4P0jvhm8YMO2i4Rieg_cgk64bOyc1e0akPRAGfxuGATF81joX6aY2TCJOts8Uu-DkGUoSi_2bBtcpVSJckB7MEm6Q1t9J26lZuUMU-HSwS4"
                            },
                            {
                                "cdn_id": 59677,
                                "url": "https://ipv6-c012-lax009-ix.1.oca.nflxvideo.net/?o=1&v=141&e=1681915675&t=ICRRzvZoVCI2fZqPgpDqv16jfGmvH4DHiJ310Wo09ZDZTliAhmUlrqUVdK3L2eavxRZX0RP4WlpoZ3WdA2IkybAJuBDWufNhL8GwqngQuuvcjgAPXEbHlc6l0PGD_S2qKGWWGJMTM5-AE9HnifL6LmQqSuCQT54tqlA3S5eiOxnhpVbiKwHzn5z_cKykL2ptluu0PRb4KRNNYkhv3Hyo-4l8_uT0SYz3T6ttb0u0LC6SBial-btxVc0M-6mVFgFiTVm0kjc"
                            }
                        ],
                        "moov": {
                            "offset": 109,
                            "size": 1741
                        },
                        "sidx": {
                            "offset": 1850,
                            "size": 6656
                        },
                        "ssix": {
                            "offset": 8506,
                            "size": 6640
                        },
                        "isDrm": true
                    }
                ],
                "profile": "vp9-profile0-L40-dash-cenc",
                "pixelAspectX": 1,
                "pixelAspectY": 1,
                "maxWidth": 1920,
                "maxHeight": 1080,
                "maxCroppedWidth": 1920,
                "maxCroppedHeight": 804,
                "maxCroppedX": 0,
                "maxCroppedY": 138,
                "max_framerate_value": 25,
                "max_framerate_scale": 1,
                "minWidth": 768,
                "minHeight": 432,
                "minCroppedWidth": 768,
                "minCroppedHeight": 324,
                "minCroppedX": 0,
                "minCroppedY": 54,
                "flavor": "al1-vp9-eve",
                "drmHeader": {
                    "bytes": "AAAANHBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAABQIARIQAAAAAAfqPpYAAAAAAAAAAA==",
                    "checksum": "",
                    "drmHeaderId": "0000000007ea3e960000000000000000",
                    "keyId": "AAAAAAfqPpYAAAAAAAAAAA==",
                    "resolution": {
                        "height": 540,
                        "width": 960
                    }
                },
                "license": {
                    "drmSessionId": "A2DD2782120FE0FFFF927B5C7FBC3915",
                    "licenseResponseBase64": "CAISmAQKwQEKEKDpgKOSMMXShgKzC7Rmh2ISmgF7InZlcnNpb24iOiIxLjAiLCJlc24iOiJORkNEQ0gtMDItSzNZSktWTlk0SzZWTjJUM1hRMTBUN0pRSkU1MlFQIiwic2FsdCI6IjEyMjgzOTU4ODMwMjQzMzM2ODI5NDA4MTUyNjA1MjEyMjYiLCJpc3N1ZVRpbWUiOjE2ODE4NzIwNDcsIm1vdmllSWQiOiI4MTY3ODI1MyJ9IAEoADjA0QJAwNECSK+p/aEGEhQIARAAGAAgwNECKMDRAlgAYAF4ARpmEhBoemIJSpa23n6uSINTOeXiGlB2kj9L9pJiI+OyJE3r/nunW30ddpknGMuq+bBKlGgSRnD30YJlGdEQv2QaVXFW74IwStzvd7Kr6lnW1QMSi1ng3YDuAqxf6dbZYfpXAcG0HCABGmQKEAAAAAAH6j6WAAAAAAAAAAASENTiQBqem5/+GGQy5SAatCkaIEvDvPHS1Ef2us9uVS/hv4Dp1m2thq+VYg7E/SeOvLlrIAIoAjoECAAQKkISChBrYzE2AAAAALF3v5KEAAAIGmQKEAAAAAAH6j6YAAAAAAAAAAASEEbOFGF+jIXDa6aXtZ7kUCcaIMsR6LulVOOscmbhx/DyqVGlW0SPOC51xxsUGBI5dL0vIAIoAjoECAAQKkISChBrYzE2AAAAALF3v5KEAAAIIK+p/aEGOABQBRogUqBEF86NotYK7cH1cIZThJrJ5Sv6JDcNF7iqFXq/pMwigAGvG1jJkGCTgjk5M5gXuEDMgh66npnKKMYNyWy8KOP6jtutseC98Bi+mgkeXSmpfKD47BskkU8i6C8ArDoRKEgLsK185wmmU0ef9VW+DHUEdSYlYFe2Lwe1V0cJ5rTr9j8wBggM+pG07RU+VYEJcTgHPeUWJfi7ta1IfUKBspNNCzoICgYxNy40LjBAAUrYAQAAAAIAAADYAAUAELF3v5LTki4xAAAA3gAAABAAAADwAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAEAAAAAAAAAAAAAAAAAAAAAAACowAAAAAAAAKjAAAAAAAAAAAAAAAACAAABRgAAABAAAAFYAAAAEAAAAWoAAAAQAAAAAAAAAAAAAAGYAAAAEAAAAawAAAAQAAABvgAAABAAAAHQAAAAEAAAAAAAAAAAAAABmAAAABAG8yVWOhFxVdwpHljaGXz3CzlhFUdv7//NN53VuPDdKVgB",
                    "links": {
                        "releaseLicense": {
                            "href": "/releaseLicense?drmLicenseContextId=E3-BQFRAAELEN62oEaJ8QQ2rI6OfKyMGySBnmefcww8eCoRCDeo63w94dOpOPH9Koi5RgVeHcLUT_F9uQbm8ByBq9NX7uGUCRW_47b35rSkV79gGjbmSIevAssc8Dw3kduI4UIHK8VEfvV6YlR8p-WpIkeVK2pvRzNIgWrIPfaBd35TzmRYS76KbSiFpOzpQOLU995vYUxjtw8c4FNgkzRsPqDSM0dwvuIFEmwQofpiqSRBI9QRcpdyiF9aLSAbWSRXtkG6LlpxLhIBeYR1ZBj6fKPlBQdtwzc6OOVpn_m1Os1CnRCMkVIMXyVI4zrE5fxlqiBWTbYNYtOXNYvJuIM_R8h1z1frq3W8ZwTUheM8HaPwQAZz_Jg6Z5IvV-uDly5ByUyGtp4EC_AY1oxj10HW2Ch0m0UI2zPHPhUvAezm8qFOjXkZDwOVzeun3c-1X1_zFRgzVqzsV3KLLXRM2kkwTCBnQ1BuZ0K1ME2orU5ptsgx3V33Cd7WjDWKcXASoDaqBF6ajnTL3AcVyt_DiCI3vztPlczuNv3UbmXQ_TLJ4bSN5Z8cLyryD8nNIy32srBaZ3L76IcniQ%3D%3D;EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED;STANDARD;1681872475665&licenseId=wv_sd_",
                            "rel": "releaseLicense"
                        }
                    },
                    "secureStopExpected": true,
                    "providerSessionToken": null
                }
            }
        ]
    },
    "from": "playapi"
}
~~~

### ceitificate_data

~~~
Cr0CCAMSEOVEukALwQ8307Y2+LVP+0MYh/HPkwUijgIwggEKAoIBAQDm875btoWUbGqQD8eAGuBlGY+Pxo8YF1LQR+Ex0pDONMet8EHslcZRBKNQ/09RZFTP0vrYimyYiBmk9GG+S0wB3CRITgweNE15cD33MQYyS3zpBd4z+sCJam2+jj1ZA4uijE2dxGC+gRBRnw9WoPyw7D8RuhGSJ95OEtzg3Ho+mEsxuE5xg9LM4+Zuro/9msz2bFgJUjQUVHo5j+k4qLWu4ObugFmc9DLIAohL58UR5k0XnvizulOHbMMxdzna9lwTw/4SALadEV/CZXBmswUtBgATDKNqjXwokohncpdsWSauH6vfS6FXwizQoZJ9TdjSGC60rUB2t+aYDm74cIuxAgMBAAE6EHRlc3QubmV0ZmxpeC5jb20SgAOE0y8yWw2Win6M2/bw7+aqVuQPwzS/YG5ySYvwCGQd0Dltr3hpik98WijUODUr6PxMn1ZYXOLo3eED6xYGM7Riza8XskRdCfF8xjj7L7/THPbixyn4mULsttSmWFhexzXnSeKqQHuoKmerqu0nu39iW3pcxDV/K7E6aaSr5ID0SCi7KRcL9BCUCz1g9c43sNj46BhMCWJSm0mx1XFDcoKZWhpj5FAgU4Q4e6f+S8eX39nf6D6SJRb4ap7Znzn7preIvmS93xWjm75I6UBVQGo6pn4qWNCgLYlGGCQCUm5tg566j+/g5jvYZkTJvbiZFwtjMW5njbSRwB3W4CrKoyxw4qsJNSaZRTKAvSjTKdqVDXV/U5HK7SaBA6iJ981/aforXbd2vZlRXO/2S+Maa2mHULzsD+S5l4/YGpSt7PnkCe25F+nAovtl/ogZgjMeEdFyd/9YMYjOS4krYmwp3yJ7m9ZzYCQ6I8RQN4x/yLlHG5RH/+WNLNUs6JAZ0fFdCmw=
~~~

