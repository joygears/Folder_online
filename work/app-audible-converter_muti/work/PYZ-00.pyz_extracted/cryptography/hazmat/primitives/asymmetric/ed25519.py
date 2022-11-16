# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\ed25519.py
import abc
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.primitives import _serialization
_ED25519_KEY_SIZE = 32
_ED25519_SIG_SIZE = 64

class Ed25519PublicKey(metaclass=abc.ABCMeta):

    @classmethod
    def from_public_bytes(cls, data: bytes) -> 'Ed25519PublicKey':
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.ed25519_supported():
            raise UnsupportedAlgorithm('ed25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM)
        return backend.ed25519_load_public_bytes(data)

    @abc.abstractmethod
    def public_bytes(self, encoding: _serialization.Encoding, format: _serialization.PublicFormat) -> bytes:
        """
        The serialized bytes of the public key.
        """
        pass

    @abc.abstractmethod
    def verify(self, signature: bytes, data: bytes) -> None:
        """
        Verify the signature.
        """
        pass


class Ed25519PrivateKey(metaclass=abc.ABCMeta):

    @classmethod
    def generate(cls) -> 'Ed25519PrivateKey':
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.ed25519_supported():
            raise UnsupportedAlgorithm('ed25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM)
        return backend.ed25519_generate_key()

    @classmethod
    def from_private_bytes(cls, data: bytes) -> 'Ed25519PrivateKey':
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.ed25519_supported():
            raise UnsupportedAlgorithm('ed25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM)
        return backend.ed25519_load_private_bytes(data)

    @abc.abstractmethod
    def public_key(self) -> Ed25519PublicKey:
        """
        The Ed25519PublicKey derived from the private key.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding: _serialization.Encoding, format: _serialization.PrivateFormat, encryption_algorithm: _serialization.KeySerializationEncryption) -> bytes:
        """
        The serialized bytes of the private key.
        """
        pass

    @abc.abstractmethod
    def sign(self, data: bytes) -> bytes:
        """
        Signs the data.
        """
        pass