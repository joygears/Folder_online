# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 20:34:20) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\ws\AppData\Local\Temp\tmphkf2lm_t\Cookies\aesgcm.py
# Compiled at: 2022-04-11 10:34:06
# Size of source mod 2**32: 701 bytes
import os, sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
NONCE_BYTE_SIZE = 12

def encrypt(cipher, plaintext, nonce):
    cipher.mode = modes.GCM(nonce)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    return (
     cipher, ciphertext, nonce)


def decrypt(cipher, ciphertext, nonce):
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)


def get_cipher(key):
    cipher = Cipher((algorithms.AES(key)),
      None,
      backend=(default_backend()))
    return cipher