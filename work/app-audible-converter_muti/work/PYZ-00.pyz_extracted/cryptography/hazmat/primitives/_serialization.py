# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\_serialization.py
import abc
from cryptography import utils

class Encoding(utils.Enum):
    PEM = 'PEM'
    DER = 'DER'
    OpenSSH = 'OpenSSH'
    Raw = 'Raw'
    X962 = 'ANSI X9.62'
    SMIME = 'S/MIME'


class PrivateFormat(utils.Enum):
    PKCS8 = 'PKCS8'
    TraditionalOpenSSL = 'TraditionalOpenSSL'
    Raw = 'Raw'
    OpenSSH = 'OpenSSH'


class PublicFormat(utils.Enum):
    SubjectPublicKeyInfo = 'X.509 subjectPublicKeyInfo with PKCS#1'
    PKCS1 = 'Raw PKCS#1'
    OpenSSH = 'OpenSSH'
    Raw = 'Raw'
    CompressedPoint = 'X9.62 Compressed Point'
    UncompressedPoint = 'X9.62 Uncompressed Point'


class ParameterFormat(utils.Enum):
    PKCS3 = 'PKCS3'


class KeySerializationEncryption(metaclass=abc.ABCMeta):
    pass


class BestAvailableEncryption(KeySerializationEncryption):

    def __init__(self, password: bytes):
        if not isinstance(password, bytes) or len(password) == 0:
            raise ValueError('Password must be 1 or more bytes.')
        self.password = password


class NoEncryption(KeySerializationEncryption):
    pass