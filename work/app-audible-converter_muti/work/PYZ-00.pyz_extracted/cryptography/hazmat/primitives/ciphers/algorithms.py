# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\ciphers\algorithms.py
from cryptography import utils
from cryptography.hazmat.primitives.ciphers import BlockCipherAlgorithm, CipherAlgorithm
from cryptography.hazmat.primitives.ciphers.modes import ModeWithNonce

def _verify_key_size(algorithm: CipherAlgorithm, key: bytes) -> bytes:
    utils._check_byteslike('key', key)
    if len(key) * 8 not in algorithm.key_sizes:
        raise ValueError('Invalid key size ({}) for {}.'.format(len(key) * 8, algorithm.name))
    return key


class AES(CipherAlgorithm, BlockCipherAlgorithm):
    name = 'AES'
    block_size = 128
    key_sizes = frozenset([128, 192, 256, 512])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class Camellia(CipherAlgorithm, BlockCipherAlgorithm):
    name = 'camellia'
    block_size = 128
    key_sizes = frozenset([128, 192, 256])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class TripleDES(CipherAlgorithm, BlockCipherAlgorithm):
    name = '3DES'
    block_size = 64
    key_sizes = frozenset([64, 128, 192])

    def __init__(self, key: bytes):
        if len(key) == 8:
            key += key + key
        else:
            if len(key) == 16:
                key += key[:8]
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class Blowfish(CipherAlgorithm, BlockCipherAlgorithm):
    name = 'Blowfish'
    block_size = 64
    key_sizes = frozenset(range(32, 449, 8))

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class CAST5(CipherAlgorithm, BlockCipherAlgorithm):
    name = 'CAST5'
    block_size = 64
    key_sizes = frozenset(range(40, 129, 8))

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class ARC4(CipherAlgorithm):
    name = 'RC4'
    key_sizes = frozenset([40, 56, 64, 80, 128, 160, 192, 256])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class IDEA(CipherAlgorithm):
    name = 'IDEA'
    block_size = 64
    key_sizes = frozenset([128])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class SEED(CipherAlgorithm, BlockCipherAlgorithm):
    name = 'SEED'
    block_size = 128
    key_sizes = frozenset([128])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class ChaCha20(CipherAlgorithm, ModeWithNonce):
    name = 'ChaCha20'
    key_sizes = frozenset([256])

    def __init__(self, key: bytes, nonce: bytes):
        self.key = _verify_key_size(self, key)
        utils._check_byteslike('nonce', nonce)
        if len(nonce) != 16:
            raise ValueError('nonce must be 128-bits (16 bytes)')
        self._nonce = nonce

    @property
    def nonce(self) -> bytes:
        return self._nonce

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class SM4(CipherAlgorithm, BlockCipherAlgorithm):
    name = 'SM4'
    block_size = 128
    key_sizes = frozenset([128])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8