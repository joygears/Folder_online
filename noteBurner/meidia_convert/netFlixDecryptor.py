import subprocess
import os
import requests
from urllib3 import encode_multipart_formdata
from utils import getSystemProxies


class NetflixDecryptor():
    def __init__(self,keyid,encrypt_path):
        self.keyid = keyid
        self.encrypt_path = encrypt_path
        self.decrypt_path = self._get_decrypt_path(encrypt_path)
        self.key = self._get_key(keyid)
    def _get_decrypt_path(self,encrypt_path):
        forward,ext = os.path.splitext(encrypt_path)
        return forward+"_decrypt"+ext

    def _get_key(self,keyid):
        url = "https://drm-u1.dvdfab.cn/ak/re/netflix/"
        header = {"Content-Type": "multipart/form-data"}
        data = {
            'cmd': 'download',
            'table': 'netflix_keys',
            'kid': keyid,
            'ver': '3'
        }

        # 转换data数据的类型
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        header['Content-Type'] = encode_data[1]

        res = requests.post(url=url, headers=header, data=data,proxies=getSystemProxies())

        rtn = res.json()
        # rtn = '{"R":"0","ret":"success","key":"000000000522b2740000000000000000:02e1bbf738724fcd1f39bdcc2d304b2f|"}'
        # rtn = json.loads(rtn)
        target_key = None
        if rtn["ret"] == "success":
            key_sets = rtn["key"].split("|")
            for key_set in key_sets:
                sets = key_set.split(":")
                if len(sets) == 2:
                    id,key = sets
                    if id == keyid:
                        target_key = key
        return target_key
    def decrypt(self):
        commandline = self.build_commandline_list()
        wvdecrypt_process = subprocess.Popen(commandline)
        wvdecrypt_process.wait()
        os.replace(self.decrypt_path,self.encrypt_path)
    def build_commandline_list(self):
        commandline = ["binaries/mp4decrypt.exe"]
        commandline.append('--show-progress')
        commandline.append('--key')
        commandline.append('{}:{}'.format(self.keyid, self.key))
        commandline.append(self.encrypt_path)
        commandline.append(self.decrypt_path)
        return commandline

if __name__ == "__main__":
    decryptor = NetflixDecryptor("000000000522b2740000000000000000","temp1/123.mp4")
    decryptor.decrypt()


