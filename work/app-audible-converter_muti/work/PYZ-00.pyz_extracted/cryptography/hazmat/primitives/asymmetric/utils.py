# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\utils.py
from cryptography.hazmat.bindings._rust import asn1
from cryptography.hazmat.primitives import hashes
decode_dss_signature = asn1.decode_dss_signature
encode_dss_signature = asn1.encode_dss_signature

class Prehashed(object):

    def __init__(self, algorithm: hashes.HashAlgorithm):
        if not isinstance(algorithm, hashes.HashAlgorithm):
            raise TypeError('Expected instance of HashAlgorithm.')
        self._algorithm = algorithm
        self._digest_size = algorithm.digest_size

    digest_size = property(lambda self: self._digest_size)