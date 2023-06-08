import asyncio
import websockets
import json

from netFlixParser import getTrackInfo

PSSH = ""
licenseRequest=""
sessionId=""
def packMessage(fro, to, message):
    data = {
        "content": json.dumps(message),
        "header": {
            "from": fro,
            "to": to
        }
    }
    return json.dumps(data)


async def handle_client(websocket, path):
    global PSSH
    global licenseRequest
    global  sessionId
    # 这是处理每个客户端连接的函数
    # 在这里编写服务器与客户端交互的逻辑
    KEEP_ID = None
    id = None
    while True:
        try:
            # 接收客户端消息
            message = await websocket.recv()
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
                    KEEP_ID=header['to'].split("_")[1]
                    print("get connnect to keeper_%s" % KEEP_ID)
                    message = {
                        "opData": {
                            "cert": "Cr0CCAMSEOVEukALwQ8307Y2+LVP+0MYh/HPkwUijgIwggEKAoIBAQDm875btoWUbGqQD8eAGuBlGY+Pxo8YF1LQR+Ex0pDONMet8EHslcZRBKNQ/09RZFTP0vrYimyYiBmk9GG+S0wB3CRITgweNE15cD33MQYyS3zpBd4z+sCJam2+jj1ZA4uijE2dxGC+gRBRnw9WoPyw7D8RuhGSJ95OEtzg3Ho+mEsxuE5xg9LM4+Zuro/9msz2bFgJUjQUVHo5j+k4qLWu4ObugFmc9DLIAohL58UR5k0XnvizulOHbMMxdzna9lwTw/4SALadEV/CZXBmswUtBgATDKNqjXwokohncpdsWSauH6vfS6FXwizQoZJ9TdjSGC60rUB2t+aYDm74cIuxAgMBAAE6EHRlc3QubmV0ZmxpeC5jb20SgAOE0y8yWw2Win6M2/bw7+aqVuQPwzS/YG5ySYvwCGQd0Dltr3hpik98WijUODUr6PxMn1ZYXOLo3eED6xYGM7Riza8XskRdCfF8xjj7L7/THPbixyn4mULsttSmWFhexzXnSeKqQHuoKmerqu0nu39iW3pcxDV/K7E6aaSr5ID0SCi7KRcL9BCUCz1g9c43sNj46BhMCWJSm0mx1XFDcoKZWhpj5FAgU4Q4e6f+S8eX39nf6D6SJRb4ap7Znzn7preIvmS93xWjm75I6UBVQGo6pn4qWNCgLYlGGCQCUm5tg566j+/g5jvYZkTJvbiZFwtjMW5njbSRwB3W4CrKoyxw4qsJNSaZRTKAvSjTKdqVDXV/U5HK7SaBA6iJ981/aforXbd2vZlRXO/2S+Maa2mHULzsD+S5l4/YGpSt7PnkCe25F+nAovtl/ogZgjMeEdFyd/9YMYjOS4krYmwp3yJ7m9ZzYCQ6I8RQN4x/yLlHG5RH/+WNLNUs6JAZ0fFdCmw=",
                            "certMode": "Set",
                            "pssh": PSSH
                        },
                        "opType": "LicenseRequest",
                        "token": KEEP_ID+"_1"
                    }
                    response = packMessage("keeper_"+KEEP_ID, id, message)
                    await websocket.send(response)
                elif opType == "LicenseRequestResult":
                    licenseRequest = opData['data']['licenseRequest']
                    sessionId = opData['data']['sessionId']



        except websockets.exceptions.ConnectionClosedOK:
            # 客户端断开连接
            print("Client disconnected")
            break
def initConfig():
    global PSSH
    url = "https://www.netflix.com/watch/60034587?trackId=255824129&tctx=0%2C0%2CNAPA%40%40%7C01fa823c-2c60-4711-9729-ce2dd8af52a1-291837750_titles%2F1%2F%2F%E5%B0%8F%E5%A7%90%E5%A5%BD%E7%99%BD%2F0%2F0%2CNAPA%40%40%7C01fa823c-2c60-4711-9729-ce2dd8af52a1-291837750_titles%2F1%2F%2F%E5%B0%8F%E5%A7%90%E5%A5%BD%E7%99%BD%2F0%2F0%2Cunknown%2C%2C01fa823c-2c60-4711-9729-ce2dd8af52a1-291837750%7C1%2CtitlesResults%2C60034587%2CVideo%3A60034587%2CminiDpPlayButton"

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
