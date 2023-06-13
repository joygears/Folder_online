from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import pad, unpad

# 加密密钥和初始向量
key = b'ec426dd15fd85542'
iv = b'9dd03c4d65be87de'

# 解密函数
def aes_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')

# 读取 main.data 文件
with open(r"C:\Program Files (x86)\NoteBurner\NoteBurner Netflix Video Downloader\resources\com.noteburner.netflix\main\main.data", 'rb') as file:
    ciphertext = file.read()


# 填充密文
padded_ciphertext = ciphertext

# 解密数据
decrypted_data = aes_decrypt(padded_ciphertext, key, iv)

# 保存到 main.js 文件
with open('main.js', 'w',encoding="utf-8") as file:
    file.write(decrypted_data)

print('数据已成功解密并保存到 main.js 文件中。')
