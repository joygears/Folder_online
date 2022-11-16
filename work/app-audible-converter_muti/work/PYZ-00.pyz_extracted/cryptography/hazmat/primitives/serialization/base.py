# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\serialization\base.py
import typing
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import Backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.asymmetric.types import PRIVATE_KEY_TYPES, PUBLIC_KEY_TYPES

def load_pem_private_key(data: bytes, password: typing.Optional[bytes], backend: typing.Optional[Backend]=None) -> PRIVATE_KEY_TYPES:
    backend = _get_backend(backend)
    return backend.load_pem_private_key(data, password)


def load_pem_public_key(data: bytes, backend: typing.Optional[Backend]=None) -> PUBLIC_KEY_TYPES:
    backend = _get_backend(backend)
    return backend.load_pem_public_key(data)


def load_pem_parameters(data: bytes, backend: typing.Optional[Backend]=None) -> 'dh.DHParameters':
    backend = _get_backend(backend)
    return backend.load_pem_parameters(data)


def load_der_private_key(data: bytes, password: typing.Optional[bytes], backend: typing.Optional[Backend]=None) -> PRIVATE_KEY_TYPES:
    backend = _get_backend(backend)
    return backend.load_der_private_key(data, password)


def load_der_public_key(data: bytes, backend: typing.Optional[Backend]=None) -> PUBLIC_KEY_TYPES:
    backend = _get_backend(backend)
    return backend.load_der_public_key(data)


def load_der_parameters(data: bytes, backend: typing.Optional[Backend]=None) -> 'dh.DHParameters':
    backend = _get_backend(backend)
    return backend.load_der_parameters(data)