# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\kdf\scrypt.py
import sys, typing
from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, InvalidKey, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import Backend, ScryptBackend
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction
_MEM_LIMIT = sys.maxsize // 2

class Scrypt(KeyDerivationFunction):

    def __init__(self, salt: bytes, length: int, n: int, r: int, p: int, backend: typing.Optional[Backend]=None):
        backend = _get_backend(backend)
        if not isinstance(backend, ScryptBackend):
            raise UnsupportedAlgorithm('Backend object does not implement ScryptBackend.', _Reasons.BACKEND_MISSING_INTERFACE)
        self._length = length
        utils._check_bytes('salt', salt)
        if n < 2 or n & n - 1 != 0:
            raise ValueError('n must be greater than 1 and be a power of 2.')
        if r < 1:
            raise ValueError('r must be greater than or equal to 1.')
        if p < 1:
            raise ValueError('p must be greater than or equal to 1.')
        self._used = False
        self._salt = salt
        self._n = n
        self._r = r
        self._p = p
        self._backend = backend

    def derive(self, key_material: bytes) -> bytes:
        if self._used:
            raise AlreadyFinalized('Scrypt instances can only be used once.')
        self._used = True
        utils._check_byteslike('key_material', key_material)
        return self._backend.derive_scrypt(key_material, self._salt, self._length, self._n, self._r, self._p)

    def verify(self, key_material: bytes, expected_key: bytes) -> None:
        derived_key = self.derive(key_material)
        if not constant_time.bytes_eq(derived_key, expected_key):
            raise InvalidKey('Keys do not match.')