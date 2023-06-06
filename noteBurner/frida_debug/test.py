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



message = {
    "opData": {
        "appIdentify": "com.noteburner.netflix"
    },
    "opType": "Initialize",
    "token": "4224_1"
}
data = packMessage("mediaconvert_NoteBurner-netflix", "shell_10532", message)
print(data)
