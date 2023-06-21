import asyncio
import websockets
import json
import requests
from urllib.parse import urlparse, urlunparse
from netFlixParser import getTrackInfo
import threading

from  gloVar import defalut_lan_map,language_map

PSSH = ""
licenseRequest = ""
sessionId = ""
url = "https://www.netflix.com/watch/60034587?trackId=255824129&tctx=0%2C0%2CNAPA%40%40%7Ce8b3ba74-0e8c-42a7-8fb4-65da324e0a37-282234721_titles%2F1%2F%2F%E5%B0%8F%E5%A7%90%E5%A5%BD%E7%99%BD%2F0%2F0%2CNAPA%40%40%7Ce8b3ba74-0e8c-42a7-8fb4-65da324e0a37-282234721_titles%2F1%2F%2F%E5%B0%8F%E5%A7%90%E5%A5%BD%E7%99%BD%2F0%2F0%2Cunknown%2C%2Ce8b3ba74-0e8c-42a7-8fb4-65da324e0a37-282234721%7C1%2CtitlesResults%2C60034587%2CVideo%3A60034587%2CminiDpPlayButton"
license = ""
track_info = ""
KEEP_ID = None
id = None



def packMessage(fro, to, message):
    data = {
        "content": json.dumps(message),
        "header": {
            "from": fro,
            "to": to
        }
    }
    return json.dumps(data)
# 定义一个线程函数
async def my_thread_function(message,websocket):
    global PSSH
    global licenseRequest
    global sessionId
    global KEEP_ID
    global id
    global license

    print("Received message:", message)

    # 处理收到的消息
    if message.startswith("shell_"):
        id = message
        print("connect %s succsess" % id)
        # 发送响应消息给客户端
        response = "mediaconvert_NoteBurner-netflix"
        await websocket.send(response)
        message = {
            "opData": {
                "appIdentify": "com.noteburner.netflix"
            },
            "opType": "Initialize",
            "token": "4224_1"
        }
        response = packMessage("mediaconvert_NoteBurner-netflix", id, message)
        await websocket.send(response)
    else:
        data = json.loads(message)
        content = json.loads(data['content'])
        header = data['header']
        opType = content['opType']
        opData = content['opData']
        if opType == "Echo":
            KEEP_ID = header['to'].split("_")[1]
            print("get connnect to keeper_%s" % KEEP_ID)
            message = {
                "opData": {
                    "cert": "Cr0CCAMSEOVEukALwQ8307Y2+LVP+0MYh/HPkwUijgIwggEKAoIBAQDm875btoWUbGqQD8eAGuBlGY+Pxo8YF1LQR+Ex0pDONMet8EHslcZRBKNQ/09RZFTP0vrYimyYiBmk9GG+S0wB3CRITgweNE15cD33MQYyS3zpBd4z+sCJam2+jj1ZA4uijE2dxGC+gRBRnw9WoPyw7D8RuhGSJ95OEtzg3Ho+mEsxuE5xg9LM4+Zuro/9msz2bFgJUjQUVHo5j+k4qLWu4ObugFmc9DLIAohL58UR5k0XnvizulOHbMMxdzna9lwTw/4SALadEV/CZXBmswUtBgATDKNqjXwokohncpdsWSauH6vfS6FXwizQoZJ9TdjSGC60rUB2t+aYDm74cIuxAgMBAAE6EHRlc3QubmV0ZmxpeC5jb20SgAOE0y8yWw2Win6M2/bw7+aqVuQPwzS/YG5ySYvwCGQd0Dltr3hpik98WijUODUr6PxMn1ZYXOLo3eED6xYGM7Riza8XskRdCfF8xjj7L7/THPbixyn4mULsttSmWFhexzXnSeKqQHuoKmerqu0nu39iW3pcxDV/K7E6aaSr5ID0SCi7KRcL9BCUCz1g9c43sNj46BhMCWJSm0mx1XFDcoKZWhpj5FAgU4Q4e6f+S8eX39nf6D6SJRb4ap7Znzn7preIvmS93xWjm75I6UBVQGo6pn4qWNCgLYlGGCQCUm5tg566j+/g5jvYZkTJvbiZFwtjMW5njbSRwB3W4CrKoyxw4qsJNSaZRTKAvSjTKdqVDXV/U5HK7SaBA6iJ981/aforXbd2vZlRXO/2S+Maa2mHULzsD+S5l4/YGpSt7PnkCe25F+nAovtl/ogZgjMeEdFyd/9YMYjOS4krYmwp3yJ7m9ZzYCQ6I8RQN4x/yLlHG5RH/+WNLNUs6JAZ0fFdCmw=",
                    "certMode": "Set",
                    "pssh": PSSH
                },
                "opType": "LicenseRequest",
                "token": KEEP_ID + "_1"
            }
            response = packMessage("keeper_" + KEEP_ID, id, message)
            await websocket.send(response)
        elif opType == "LicenseRequestResult":
            licenseRequest = opData['data']['licenseRequest']
            sessionId = opData['data']['sessionId']
            license = "CAISjAQKtQEKEKZuunXS6IKoTGb0Ii+gK58SnAF7InZlcnNpb24iOiIxLjAiLCJlc24iOiJORkNEQ0gtMDItSzNFWjM0UVZWRk5BM0UyN0dFNjZGUU44QUFLV1dBIiwic2FsdCI6Ijk3Nzk5MTc2MzY0ODg4MTMxOTYwODM3NjI0NzU1OTYwOCIsImlzc3VlVGltZSI6MTY4NTcyODY0NDAwMCwibW92aWVJZCI6IjYwMDM0NTg3In0gASgAEhQIARAAGAAgwNECKMDRAlgAYAF4ARpmEhC7UIvzBj/LltnpNIA6Zp5gGlCN/3axROQ3HKZ2lfHiUSWqk8ozgVGqFccmhrGbypGtHUc/7I0ZPM33jQZGSfdk+aHaEPkZ1hr8xMXSFo4YH9/VdBDa1jeFeHXQU5ghhpDLNiABGmQKEAAAAAAEnltPAAAAAAAAAAASEKbPHKHeQEph3s9TGn2GKFwaIKlfoNV1mIDdBVnaQIuy7N6AaqRYT4LyeTZapgMjLgjgIAIoAjIECAAQKkISChBrYzE2AAAAAFMSH56kAAAIGmQKEAAAAAAERyj0AAAAAAAAAAASEDmGEgbDz+SW8y2QfkWN/+EaIEfWWoiTgAmiKTvInSuY7tNgKBj5V8h44urss+amAJ3pIAIoAjoECAAQKkISChBrYzE2AAAAAFMSH56EAAAIIITb6KMGOABQBRogDcptt1XQJpoES16vJIswZjh2rVtxAlg1RKekQfe/bjcigAEyVqbdUN7bv0kQJT8SyxFc20QPTct7n8CdWqSMGFQmD7WvK+fBZIPFFOAEUTQiQQVzZKtdC+MKfVP437e8L/ppHwqKcGllSfnUH4dHWhCTIvS7FsOJ+YvmBpvlBT3oI2+vDuNCMLJYfWsLhFfMIDq9z7SxbKbbPtaF6sJD9EJkHjoICgYxOC4wLjFAAUrYAQAAAAIAAADYAAUAEFMSH57hdbeqAAAA0gAAABAAAADkAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAEAAAAAAAAAAAAAAAAAAAAAAACowAAAAAAAAKjAAAAAAAAAAAAAAAACAAABOgAAABAAAAFMAAAAEAAAAV4AAAAQAAAAAAAAAAAAAAGMAAAAEAAAAaAAAAAQAAABsgAAABAAAAHEAAAAEAAAAAAAAAAAAAAB8gAAABAHfxawYqBd+LZn4NCPsmv3lvrUfgB9zGgvOapiI/HAL1gB"
            request_license()
            message = {
                "opData": {
                    "license": license,
                    "sessionId": sessionId
                },
                "opType": "License",
                "token": KEEP_ID + "_1"
            }
            response = packMessage("keeper_" + KEEP_ID, id, message)
            await websocket.send(response)

        elif opType == "LicenseResult":
            message = tanstoDownloadInfo()
            response = packMessage("keeper_" + KEEP_ID, id, message)
            await websocket.send(response)
        elif opType == "GetGlobalInfo":
            token = content['token']
            message = {
                "opData": {
                    "data": {
                        "convertMode": "C",
                        "deviceInfo": {
                            "ap": "com.noteburner.netflix",
                            "apv": "2.0.3",
                            "guid": "3ad6f53a-8dd1-4a6a-978c-664327a8cdb7",
                            "uid": "00:e0:4c:06:91:8c",
                            "website": "netflix"
                        },
                        "hwaccel": 3,
                        "nodePath": "\"C:\\Program Files (x86)\\NoteBurner\\NoteBurner Netflix Video Downloader\\NoteBurner Netflix Video Downloader.exe\""
                    },
                    "error": False,
                    "errorCode": 0
                },
                "opType": "GetGlobalInfoResult",
                "token": token
            }
            response = packMessage("mediaconvert_NoteBurner-netflix", id, message)
            await websocket.send(response)
        elif opType == "Download":
            token = content['token']
            path = opData['path']
            offset = opData['offset']
            length = opData['length']
            url = opData['url']
            if length != 0:
                parsed_url = urlparse(url)
                new_path = f'range/{offset}-{offset + length}' + parsed_url.path[1:]
                new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, parsed_url.params,
                                      parsed_url.query, parsed_url.fragment))
                response = requests.get(new_url, stream=True)
                response.raise_for_status()
                with open(path, 'wb') as file:
                    file.write(response.content)
                print('File downloaded and saved successfully. url %s to path %s' % (new_url, path))
            else:
                print('Length is 0. No file download required.')

            message = {
                "opData": {
                    "data": {
                        "context": opData['context'],
                        "path": path,
                        "progress": 1000,
                        "reqId": opData['reqId'],
                        "token": token,
                        "url": url
                    },
                    "error": False,
                    "errorCode": 0
                },
                "opType": "DownloadResult",
                "token": token
            }
            response = packMessage("mediaconvert_NoteBurner-netflix", id, message)
            await websocket.send(response)

mutex = asyncio.Lock()
async def handle_client(websocket, path):
    global PSSH
    global licenseRequest
    global sessionId
    global KEEP_ID
    global id
    global license
    # 这是处理每个客户端连接的函数
    # 在这里编写服务器与客户端交互的逻辑
    async with mutex:
        async for message in websocket:
            response = None
            print("Received message:", message)

            # 处理收到的消息
            if message.startswith("shell_"):
                id = message
                print("connect %s succsess" % id)
                # 发送响应消息给客户端
                response = "mediaconvert_NoteBurner-netflix"
                await websocket.send(response)
                message = {
                    "opData": {
                        "appIdentify": "com.noteburner.netflix"
                    },
                    "opType": "Initialize",
                    "token": "4224_1"
                }
                response = packMessage("mediaconvert_NoteBurner-netflix", id, message)
            else:
                data = json.loads(message)
                content = json.loads(data['content'])
                header = data['header']
                opType = content['opType']
                opData = content['opData']
                if opType == "Echo":
                    KEEP_ID = header['to'].split("_")[1]
                    print("get connnect to keeper_%s" % KEEP_ID)
                    message = {
                        "opData": {
                            "cert": "Cr0CCAMSEOVEukALwQ8307Y2+LVP+0MYh/HPkwUijgIwggEKAoIBAQDm875btoWUbGqQD8eAGuBlGY+Pxo8YF1LQR+Ex0pDONMet8EHslcZRBKNQ/09RZFTP0vrYimyYiBmk9GG+S0wB3CRITgweNE15cD33MQYyS3zpBd4z+sCJam2+jj1ZA4uijE2dxGC+gRBRnw9WoPyw7D8RuhGSJ95OEtzg3Ho+mEsxuE5xg9LM4+Zuro/9msz2bFgJUjQUVHo5j+k4qLWu4ObugFmc9DLIAohL58UR5k0XnvizulOHbMMxdzna9lwTw/4SALadEV/CZXBmswUtBgATDKNqjXwokohncpdsWSauH6vfS6FXwizQoZJ9TdjSGC60rUB2t+aYDm74cIuxAgMBAAE6EHRlc3QubmV0ZmxpeC5jb20SgAOE0y8yWw2Win6M2/bw7+aqVuQPwzS/YG5ySYvwCGQd0Dltr3hpik98WijUODUr6PxMn1ZYXOLo3eED6xYGM7Riza8XskRdCfF8xjj7L7/THPbixyn4mULsttSmWFhexzXnSeKqQHuoKmerqu0nu39iW3pcxDV/K7E6aaSr5ID0SCi7KRcL9BCUCz1g9c43sNj46BhMCWJSm0mx1XFDcoKZWhpj5FAgU4Q4e6f+S8eX39nf6D6SJRb4ap7Znzn7preIvmS93xWjm75I6UBVQGo6pn4qWNCgLYlGGCQCUm5tg566j+/g5jvYZkTJvbiZFwtjMW5njbSRwB3W4CrKoyxw4qsJNSaZRTKAvSjTKdqVDXV/U5HK7SaBA6iJ981/aforXbd2vZlRXO/2S+Maa2mHULzsD+S5l4/YGpSt7PnkCe25F+nAovtl/ogZgjMeEdFyd/9YMYjOS4krYmwp3yJ7m9ZzYCQ6I8RQN4x/yLlHG5RH/+WNLNUs6JAZ0fFdCmw=",
                            "certMode": "Set",
                            "pssh": PSSH
                        },
                        "opType": "LicenseRequest",
                        "token": KEEP_ID + "_1"
                    }
                    response = packMessage("keeper_" + KEEP_ID, id, message)
                elif opType == "LicenseRequestResult":
                    licenseRequest = opData['data']['licenseRequest']
                    sessionId = opData['data']['sessionId']
                    license = "CAISjAQKtQEKEKZuunXS6IKoTGb0Ii+gK58SnAF7InZlcnNpb24iOiIxLjAiLCJlc24iOiJORkNEQ0gtMDItSzNFWjM0UVZWRk5BM0UyN0dFNjZGUU44QUFLV1dBIiwic2FsdCI6Ijk3Nzk5MTc2MzY0ODg4MTMxOTYwODM3NjI0NzU1OTYwOCIsImlzc3VlVGltZSI6MTY4NTcyODY0NDAwMCwibW92aWVJZCI6IjYwMDM0NTg3In0gASgAEhQIARAAGAAgwNECKMDRAlgAYAF4ARpmEhC7UIvzBj/LltnpNIA6Zp5gGlCN/3axROQ3HKZ2lfHiUSWqk8ozgVGqFccmhrGbypGtHUc/7I0ZPM33jQZGSfdk+aHaEPkZ1hr8xMXSFo4YH9/VdBDa1jeFeHXQU5ghhpDLNiABGmQKEAAAAAAEnltPAAAAAAAAAAASEKbPHKHeQEph3s9TGn2GKFwaIKlfoNV1mIDdBVnaQIuy7N6AaqRYT4LyeTZapgMjLgjgIAIoAjIECAAQKkISChBrYzE2AAAAAFMSH56kAAAIGmQKEAAAAAAERyj0AAAAAAAAAAASEDmGEgbDz+SW8y2QfkWN/+EaIEfWWoiTgAmiKTvInSuY7tNgKBj5V8h44urss+amAJ3pIAIoAjoECAAQKkISChBrYzE2AAAAAFMSH56EAAAIIITb6KMGOABQBRogDcptt1XQJpoES16vJIswZjh2rVtxAlg1RKekQfe/bjcigAEyVqbdUN7bv0kQJT8SyxFc20QPTct7n8CdWqSMGFQmD7WvK+fBZIPFFOAEUTQiQQVzZKtdC+MKfVP437e8L/ppHwqKcGllSfnUH4dHWhCTIvS7FsOJ+YvmBpvlBT3oI2+vDuNCMLJYfWsLhFfMIDq9z7SxbKbbPtaF6sJD9EJkHjoICgYxOC4wLjFAAUrYAQAAAAIAAADYAAUAEFMSH57hdbeqAAAA0gAAABAAAADkAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAEAAAAAAAAAAAAAAAAAAAAAAACowAAAAAAAAKjAAAAAAAAAAAAAAAACAAABOgAAABAAAAFMAAAAEAAAAV4AAAAQAAAAAAAAAAAAAAGMAAAAEAAAAaAAAAAQAAABsgAAABAAAAHEAAAAEAAAAAAAAAAAAAAB8gAAABAHfxawYqBd+LZn4NCPsmv3lvrUfgB9zGgvOapiI/HAL1gB"
                    #request_license()
                    message = {
                        "opData": {
                            "license": license,
                            "sessionId": sessionId
                        },
                        "opType": "License",
                        "token": KEEP_ID + "_1"
                    }
                    response = packMessage("keeper_" + KEEP_ID, id, message)
                elif opType == "LicenseResult":
                    message = tanstoDownloadInfo()
                    response = packMessage("keeper_" + KEEP_ID, id, message)
                elif opType == "GetGlobalInfo":
                    token = content['token']
                    message = {
                        "opData": {
                            "data": {
                                "convertMode": "C",
                                "deviceInfo": {
                                    "ap": "com.noteburner.netflix",
                                    "apv": "2.0.3",
                                    "guid": "3ad6f53a-8dd1-4a6a-978c-664327a8cdb7",
                                    "uid": "00:e0:4c:06:91:8c",
                                    "website": "netflix"
                                },
                                "hwaccel": 3,
                                "nodePath": "\"C:\\Program Files (x86)\\NoteBurner\\NoteBurner Netflix Video Downloader\\NoteBurner Netflix Video Downloader.exe\""
                            },
                            "error": False,
                            "errorCode": 0
                        },
                        "opType": "GetGlobalInfoResult",
                        "token": token
                    }
                    response = packMessage("mediaconvert_NoteBurner-netflix", id, message)
                elif opType == "Download":
                    token = content['token']
                    path = opData['path']
                    offset = opData['offset']
                    length = opData['length']
                    url = opData['url']
                    if length != 0:
                        parsed_url = urlparse(url)
                        new_path = f'range/{offset}-{offset + length}' + parsed_url.path[1:]
                        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, parsed_url.params,
                                              parsed_url.query, parsed_url.fragment))
                        response = requests.get(new_url, stream=True)
                        response.raise_for_status()
                        with open(path, 'wb') as file:
                            file.write(response.content)
                        print('File downloaded and saved successfully. url %s to path %s' % (new_url, path))
                    else:
                        print('Length is 0. No file download required.')

                    message = {
                        "opData": {
                            "data": {
                                "context": opData['context'],
                                "path": path,
                                "progress": 1000,
                                "reqId": opData['reqId'],
                                "token": token,
                                "url": url
                            },
                            "error": False,
                            "errorCode": 0
                        },
                        "opType": "DownloadResult",
                        "token": token
                    }
                    response = packMessage("mediaconvert_NoteBurner-netflix", id, message)
            if response is not None:
                    await websocket.send(response)


def tanstoDownloadInfo():
    global track_info
    global PSSH
    result = track_info['result']
    audio_tracks = result['audio_tracks']
    audio_track = audio_tracks[0]
    stream = audio_track['streams'][-1]
    audio_url = stream['urls'][0]['url']

    video_track = result['video_tracks'][0]
    video_stream = video_track['streams'][-1]
    video_url = video_stream['urls'][0]['url']

    timedtexttrack = result['timedtexttracks'][0]

    lanLabel = ""
    qualityIcon = getVideoQuality(video_stream['res_w'],video_stream['res_h'])
    download_info = {
        "opData": {
            "input": {
                "tracks": [
                    {
                        "bitRate": stream['bitrate'] * 1000,
                        "bitrate": stream['bitrate'] * 1000,
                        "channels": stream['channels'],
                        "codec": codecTrans(stream['content_profile']),
                        "content_profile": audio_track['profile'],
                        "desc": audio_track['languageDescription'],
                        "headUrl": {
                            "length": stream['urls'][0]['cdn_id'],
                            "offset": 0,
                            "url": audio_url
                        },
                        "is5_1": True if stream['channels'] == "5.1" else False,
                        "isAD": True if stream['trackType'] == "ASSISTIVE" else False,
                        "isDefault": audio_track['isNative'],
                        "isDrm": stream['isDrm'],
                        "isOriginal":  audio_track['isNative'],
                        "language": (lambda e: e.split("-")[0] if e and "-" in e else "")(stream['language']),
                        "languageDescription": audio_track['languageDescription'],
                        "languageLabel": lanLabel,
                        "new_track_id": audio_track['new_track_id'],
                        "oriLanguage": audio_track["language"],
                        "size": stream['size'],
                        "trackId": f"{audio_track['new_track_id']}-{stream['bitrate']}-{stream['size']}",
                        "type": 0,
                        "uri":f"{audio_track['new_track_id']}-{stream['bitrate']}-{stream['size']}"
                    },
                    {
                        "bitRate": video_stream['bitrate'] * 1000,
                        "bitrate": video_stream['bitrate'] * 1000,
                        "codec": "",
                        "desc": str(video_stream['res_w']) + "x" + str(video_stream['res_h']) + "_" + qualityIcon + "_" + str(video_stream['bitrate']) + "_" + str(video_stream['crop_h'])  + "_" + str(video_stream['framerate_value']) + "/" + str(video_stream['framerate_scale']),
                        "frameRate": str(video_stream['framerate_value']) + "/" + str(video_stream['framerate_scale']),
                        "headUrl": {
                            "length": video_stream['startByteOffset'],
                            "offset": 0,
                            "url": video_url
                        },
                        "isDrm": video_stream['isDrm'],
                        "pssh": PSSH,
                        "qualityIcon": qualityIcon,
                        "sar": f"{video_track['pixelAspectX']}:{video_track['pixelAspectY']}",
                        "size": video_stream['size'],
                        "trackId": f"{video_track['new_track_id']}-{video_stream['bitrate']}",
                        "type": 1,
                        "uri": f"{video_track['new_track_id']}-{video_stream['bitrate']}"
                    }
                    # ,
                    # {
                    #     "cdnlist": timedtexttrack['cdnlist'],
                    #     "codec": "ttml-image",
                    #     "desc": "Chinese (Simplified)_zh-Hans_cc_false_forced_false_uriT:2:0;1;zh-Hans;0;0;0;_ttml-image",
                    #     "downloadableIds": {
                    #         "nflx-cmisc": "2070723521",
                    #         "webvtt-lssdh-ios8": "2070720789"
                    #     },
                    #     "encodingProfileNames": [
                    #         "nflx-cmisc",
                    #         "webvtt-lssdh-ios8"
                    #     ],
                    #     "headUrl": {
                    #         "length": 0,
                    #         "offset": 0,
                    #         "url": "http://23.246.55.165/?o=1&v=22&e=1686522996&t=sG76IZhq0JRQNt7wKstWU_E8mm0fWfCeLhC64_2PzKLnh1MqxATeiZBwhs_9tFcsNC5Ru5JwjIOhzan-ADdtlwB-cEsXUwP-DA8iEoHnnN_lf8M3OtdzpC96nhjnLbzZEkx8J53CdY2mV_-S3v_xsQ3Pszl7NPcHieJL9OE5HRN_dAWSFFJgyELUT6rLWe1p0MNYoDCKNfEcKF-xJ5FggbucnCo5TRlWQTup34J88_kCot4jfMLShQ"
                    #     },
                    #     "hydrated": True,
                    #     "id": "T:2:0;1;zh-Hans;0;0;0;",
                    #     "isCC": True,
                    #     "isDefault": True,
                    #     "isForced": False,
                    #     "isForcedNarrative": False,
                    #     "isImage": False,
                    #     "isLanguageLeftToRight": True,
                    #     "isNoneTrack": False,
                    #     "language": "zh",
                    #     "languageDescription": "Chinese (Simplified)",
                    #     "languageLabel": "Chinese (Simplified)",
                    #     "new_track_id": "T:2:0;1;zh-Hans;0;0;0;",
                    #     "oriLanguage": "zh-Hans",
                    #     "rank": 1,
                    #     "rawTrackType": "subtitles",
                    #     "size": 31209667,
                    #     "trackId": "T:2:0;1;zh-Hans;0;0;0;_ttml-image",
                    #     "trackType": "PRIMARY",
                    #     "ttDownloadables": timedtexttrack['ttDownloadables'],
                    #     "type": 2,
                    #     "uri": "T:2:0;1;zh-Hans;0;0;0;_ttml-image"
                    # }
                ]
            },
            "isTrial": True,
            "mediaId": str(result['movieId']),
            "metaData": {
                "description": "两名黑人 FBI 警探受命保护一对头脑简单的上流社会姐妹，他们把自己化妆成这对白人姐妹，出入各种派对，试图搜捕想要绑架她们的绑匪。",
                "thumbnail": r"D:\Users\Downloads\st\Folder_online\noteBurner\meidia_convert\81004276_1.jpg",
                "thumbnailType": "url",
                "title": "小姐好白",
                "year": 2004
            },
            "output": {
                "folder": r"D:\Users\Documents\NoteBurner Netflix Video Downloader",
                "format": "mp4",
                "hwaccel": True,
                "ignorPartialFail": True,
                "path": r"D:\Users\Documents\NoteBurner Netflix Video Downloader\小姐好白_9.mp4",
                "subtitleForm": 2,
                "subtitleFormat": 0,
                "videoCodec": "h264"
            }
        },
        "opType": "Convert",
        "token": KEEP_ID + "_1"
    }
    return download_info


def getVideoQuality(e, t):
    n = "720P"
    try:
        a = e * t
        r = ["240P", "360P", "480P", "720P", "1080P"]
        o = [84480, 172800, 411840, 921600, 2073600]
        s = next((i for i, val in enumerate(o) if val > a), -1)

        if s == -1:
            n = r[-1]
        elif s == 0:
            n = r[0]
        else:
            l = s - 1
            n = r[l] if o[s] - a > a - o[l] else r[s]
    except Exception as e:
        print("getVideoQuality error:", e)
        n = "720P"

    return n

def codecTrans(e):
    t = "AAC"
    if e == "heaac-2-dash":
        t = "AAC"
    elif e == "heaac-2hq-dash":
        t = "AAC HQ"
    elif e == "heaac-5.1-dash":
        t = "AAC 5.1"
    elif e == "heaac-5.1hq-dash":
        t = "AAC 5.1 HQ"
    elif e == "ddplus-2-dash":
        t = "DD+"
    elif e == "ddplus-2hq-dash":
        t = "DD+ HQ"
    elif e == "ddplus-5.1-dash":
        t = "DD+ 5.1"
    elif e == "ddplus-5.1hq-dash":
        t = "DD+ 5.1 HQ"
    else:
        t = "AAC"
    return t
def request_license():
    global url
    global sessionId
    global licenseRequest
    global license
    track_info = getTrackInfo(url, sessionId, licenseRequest)
    license = track_info['result']['video_tracks'][0]['license']['licenseResponseBase64']
    print("license get susscess %s " % license)


def initConfig():
    global PSSH
    global url
    global track_info

    track_info = getTrackInfo(url)
    PSSH = track_info['result']['video_tracks'][0]['drmHeader']['bytes']

    print("pssh get susscess %s " % PSSH)


if __name__ == "__main__":
    initConfig()

    # WebSocket服务器的地址和端口
    host = "localhost"
    port = 8012

    # 启动WebSocket服务器
    start_server = websockets.serve(handle_client, host, port)

    # 运行事件循环
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
