import asyncio,base64
import json
import threading

import websockets
import json
import requests
from urllib.parse import urlparse, urlunparse
shell_websocket = None
keeper_websocket = None
electron_websocket = None
licenseRequest = None

import os
import requests
import subprocess

def execute_command(command):
    try:
        # 使用subprocess.run()执行命令行
        # completed_process = subprocess.run(command, shell=True, check=True)
        completed_process = subprocess.run(command, creationflags=subprocess.CREATE_NEW_CONSOLE, check=True)
        return True  # 返回执行成功
    except subprocess.CalledProcessError:
        return False  # 返回执行失败
async def download_file(url, save_path, progress_callback=None):
    try:
        # 发起HTTP GET请求下载文件
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 确保请求成功

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                downloaded_size += len(chunk)
                if progress_callback:
                    progress = min(downloaded_size / total_size, 1.0)
                    await progress_callback(progress)

        return save_path

    except requests.exceptions.RequestException:
        # 下载失败时返回None
        return None

async def progress_callback(progress):
    # 在此处自定义进度的处理，例如打印百分比或更新进度条等
    # print(f"Downloading progress: {progress*100:.2f}%")
    await  asyncio.ensure_future(electron_websocket.send(str(progress*0.3)))

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
    global electron_websocket
    global  licenseRequest
    # 这是处理每个客户端连接的函数
    # 在这里编写服务器与客户端交互的逻辑

    async for message in websocket:
        response = None
        print("Received message:", message)
        # 处理收到的消息
        if message.startswith("licenseRequest:"):
            keeper_websocket = websocket
            licenseRequest = message
            # 启动shell
            os.chdir(r"D:\Users\Downloads\project\st\Folder_online\noteBurner\sheller\widevinecdm\Debug")
            thread = threading.Thread(target=lambda : execute_command(r"D:\Users\Downloads\project\st\Folder_online\noteBurner\sheller\widevinecdm\Debug\widevinecdm.exe"))
            thread.start()

            # response = licenseRequest
            # await shell_websocket.send(response)
        if message.startswith("shell"):
            try:
                if shell_websocket is not None:
                    await shell_websocket.send("exit")
            except:
                pass
            shell_websocket = websocket
            response = licenseRequest
            await shell_websocket.send(response)
        if message.startswith("licenseRequestResult:"):
            response = message
            await keeper_websocket.send(response)
        if message.startswith("licenseResult:"):
            response = message
            await shell_websocket.send(response)
        if message.startswith("convert:"):
            electron_websocket = websocket
            base64data = message.split(":")[1]
            data = base64.standard_b64decode(base64data).decode("utf-8")
            print(data)
            data = json.loads(data)
            url = data["video"]['streams'][-1]['urls'][0]['url']
            await download_file(url,"all.mp4",progress_callback)
            await shell_websocket.send("")
        if message.startswith("decryptProgress:"):
            progress=float(message.split(":")[1])
            await  electron_websocket.send(str(progress * 0.7+0.3))
        if message.startswith("initFinished"):
            await  electron_websocket.send("initFinished")









if __name__ == "__main__":

    # WebSocket服务器的地址和端口
    host = "localhost"
    port = 8012

    # 启动WebSocket服务器
    start_server = websockets.serve(handle_client, host, port)

    # 运行事件循环
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
