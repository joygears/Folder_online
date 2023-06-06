import asyncio
import websockets
import json


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
    # 这是处理每个客户端连接的函数
    # 在这里编写服务器与客户端交互的逻辑

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

        except websockets.exceptions.ConnectionClosedOK:
            # 客户端断开连接
            print("Client disconnected")
            break


if __name__ == "__main__":
    # WebSocket服务器的地址和端口
    host = "localhost"
    port = 8012

    # 启动WebSocket服务器
    start_server = websockets.serve(handle_client, host, port)

    # 运行事件循环
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
