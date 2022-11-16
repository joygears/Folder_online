# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\padding.py
import typing
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives._asymmetric import AsymmetricPadding
from cryptography.hazmat.primitives.asymmetric import rsa

class PKCS1v15(AsymmetricPadding):
    name = 'EMSA-PKCS1-v1_5'


class PSS(AsymmetricPadding):
    MAX_LENGTH = object()
    name = 'EMSA-PSS'

    def __init__(self, mgf, salt_length):
        self._mgf = mgf
        if not isinstance(salt_length, int):
            if salt_length is not self.MAX_LENGTH:
                raise TypeError('salt_length must be an integer.')
        if salt_length is not self.MAX_LENGTH:
            if salt_length < 0:
                raise ValueError('salt_length must be zero or greater.')
        self._salt_length = salt_length


class OAEP(AsymmetricPadding):
    name = 'EME-OAEP'

    def __init__(self, mgf: 'MGF1', algorithm: hashes.HashAlgorithm, label: typing.Optional[bytes]):
        if not isinstance(algorithm, hashes.HashAlgorithm):
            raise TypeError('Expected instance of hashes.HashAlgorithm.')
        self._mgf = mgf
        self._algorithm = algorithm
        self._label = label


class MGF1(object):
    MAX_LENGTH = object()

    def __init__(self, algorithm: hashes.HashAlgorithm):
        if not isinstance(algorithm, hashes.HashAlgorithm):
            raise TypeError('Expected instance of hashes.HashAlgorithm.')
        self._algorithm = algorithm


def calculate_max_pss_salt_length(key: typing.Union[('rsa.RSAPrivateKey', 'rsa.RSAPublicKey')], hash_algorithm: hashes.HashAlgorithm) -> int:
    if not isinstance(key, (rsa.RSAPrivateKey, rsa.RSAPublicKey)):
        raise TypeError('key must be an RSA public or private key')
    else:
        emlen = (key.key_size + 6) // 8
        salt_length = emlen - hash_algorithm.digest_size - 2
        assert salt_length >= 0
    return salt_length