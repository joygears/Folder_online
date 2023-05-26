import frida

def on_message(message, data):
    print("[on_message] message:", message, "data:", data)

session = frida.attach(r"notepad.exe")

script = session.create_script("""
rpc.exports.enumerateModuless = () => {
  return Process.enumerateModules();
};
""")
#script.on("message", on_message)
script.load()

print([m["name"] for m in script.exports.enumerate_moduless()])