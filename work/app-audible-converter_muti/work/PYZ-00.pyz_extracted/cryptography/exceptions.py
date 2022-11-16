# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\exceptions.py
from cryptography import utils

class _Reasons(utils.Enum):
    BACKEND_MISSING_INTERFACE = 0
    UNSUPPORTED_HASH = 1
    UNSUPPORTED_CIPHER = 2
    UNSUPPORTED_PADDING = 3
    UNSUPPORTED_MGF = 4
    UNSUPPORTED_PUBLIC_KEY_ALGORITHM = 5
    UNSUPPORTED_ELLIPTIC_CURVE = 6
    UNSUPPORTED_SERIALIZATION = 7
    UNSUPPORTED_X509 = 8
    UNSUPPORTED_EXCHANGE_ALGORITHM = 9
    UNSUPPORTED_DIFFIE_HELLMAN = 10
    UNSUPPORTED_MAC = 11


class UnsupportedAlgorithm(Exception):

    def __init__(self, message, reason=None):
        super(UnsupportedAlgorithm, self).__init__(message)
        self._reason = reason


class AlreadyFinalized(Exception):
    pass


class AlreadyUpdated(Exception):
    pass


class NotYetFinalized(Exception):
    pass


class InvalidTag(Exception):
    pass


class InvalidSignature(Exception):
    pass


class InternalError(Exception):

    def __init__(self, msg, err_code):
        super(InternalError, self).__init__(msg)
        self.err_code = err_code


class InvalidKey(Exception):
    pass