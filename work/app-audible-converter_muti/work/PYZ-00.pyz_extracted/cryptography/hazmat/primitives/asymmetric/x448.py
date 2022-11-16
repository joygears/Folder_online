# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\x448.py
import abc
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.primitives import _serialization

class X448PublicKey(metaclass=abc.ABCMeta):

    @classmethod
    def from_public_bytes(cls, data: bytes) -> 'X448PublicKey':
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.x448_supported():
            raise UnsupportedAlgorithm('X448 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM)
        return backend.x448_load_public_bytes(data)

    @abc.abstractmethod
    def public_bytes(self, encoding: _serialization.Encoding, format: _serialization.PublicFormat) -> bytes:
        """
        The serialized bytes of the public key.
        """
        pass


class X448PrivateKey(metaclass=abc.ABCMeta):

    @classmethod
    def generate(cls) -> 'X448PrivateKey':
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.x448_supported():
            raise UnsupportedAlgorithm('X448 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM)
        return backend.x448_generate_key()

    @classmethod
    def from_private_bytes(cls, data: bytes) -> 'X448PrivateKey':
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.x448_supported():
            raise UnsupportedAlgorithm('X448 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM)
        return backend.x448_load_private_bytes(data)

    @abc.abstractmethod
    def public_key(self) -> X448PublicKey:
        """
        The serialized bytes of the public key.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding: _serialization.Encoding, format: _serialization.PrivateFormat, encryption_algorithm: _serialization.KeySerializationEncryption) -> bytes:
        """
        The serialized bytes of the private key.
        """
        pass

    @abc.abstractmethod
    def exchange(self, peer_public_key: X448PublicKey) -> bytes:
        """
        Performs a key exchange operation using the provided peer's public key.
        """
        pass