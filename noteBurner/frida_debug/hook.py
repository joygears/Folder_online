import frida
import sys
import psutil

def get_cdm_process_pid(name=""):
    """
    获取cdm进程的pid
        @name 进程的名称
        @ret  目标进程pid
    """
    for pid in psutil.pids():
        p = psutil.Process(pid)
        try:
            with p.oneshot():
                cmdline = " ".join(p.cmdline())
                if "CdmServiceBroker" in cmdline and name in cmdline:
                    print("pid:%d name:%s" % (pid,p.name()))
                    return pid
        except:
            pass
def get_js_script(path="hook.js"):
    with open(path,"r",encoding="utf-8") as fp:
        js_code = fp.read()
    return js_code
def on_message(message, data):
    print(message)

if __name__ == "__main__":
    pid = get_cdm_process_pid("NoteBurner Netflix Video Downloader.exe")
    if pid is None:
        print("cdm进程未启动，请启动cdm进程")
        sys.exit(1)
    js_code = get_js_script("hook.js")
    session = frida.attach(pid)
    script = session.create_script(js_code)

    script.on('message', on_message)
    script.load()
    sys.stdin.read()
