import asyncio
import time

import websockets
import json
import requests
from urllib.parse import urlparse, urlunparse
shell_websocket = None
keeper_websocket = None
mutex = asyncio.Lock()
async def handle_client(websocket, path):
    global PSSH
    global licenseRequest
    global sessionId
    global KEEP_ID
    global id
    global license
    global  shell_websocket
    global  keeper_websocket
    # 这是处理每个客户端连接的函数
    # 在这里编写服务器与客户端交互的逻辑

    async for message in websocket:
        response = None
        print("Received message:", message)
        # 处理收到的消息
        if message.startswith("licenseRequest:"):
            keeper_websocket = websocket
            response = message
            await shell_websocket.send(response)
        if message.startswith("shell"):
            shell_websocket = websocket
        if message.startswith("licenseRequestResult:"):
            response = message
            await keeper_websocket.send(response)
        if message.startswith("licenseResult:"):
            response = message
            await shell_websocket.send(response)











if __name__ == "__main__":

    # WebSocket服务器的地址和端口
    host = "localhost"
    port = 8012

    # 启动WebSocket服务器
    start_server = websockets.serve(handle_client, host, port)

    # 运行事件循环
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
