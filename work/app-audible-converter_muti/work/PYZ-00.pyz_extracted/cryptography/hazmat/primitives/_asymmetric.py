# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\_asymmetric.py
import abc

class AsymmetricPadding(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def name(self) -> str:
        """
        A string naming this padding (e.g. "PSS", "PKCS1").
        """
        pass