# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\backends\__init__.py
import typing
from cryptography.hazmat.backends.interfaces import Backend
_default_backend = None
_default_backend: typing.Optional[Backend]

def default_backend() -> Backend:
    global _default_backend
    if _default_backend is None:
        from cryptography.hazmat.backends.openssl.backend import backend
        _default_backend = backend
    return _default_backend


def _get_backend(backend: typing.Optional[Backend]) -> Backend:
    if backend is None:
        return default_backend()
    else:
        return backend