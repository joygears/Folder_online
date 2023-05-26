import frida
import sys

session = frida.attach("hello.exe")

script = session.create_script("""
const targetAddress = Module.findBaseAddress("hello.exe").add(0x14c0);
send(targetAddress);

Interceptor.attach(targetAddress, {
    onEnter(args) {
        args[0] = Memory.allocUtf8String("hello")
        send(ptr(1337))
    }
});

""")

def on_message(message, data):
    print(message)
script.on('message', on_message)
script.load()
sys.stdin.read()