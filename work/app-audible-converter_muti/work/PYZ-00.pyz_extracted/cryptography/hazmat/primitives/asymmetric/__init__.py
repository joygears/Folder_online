# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\__init__.py
import abc

class AsymmetricSignatureContext(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self, data: bytes) -> None:
        """
        Processes the provided bytes and returns nothing.
        """
        pass

    @abc.abstractmethod
    def finalize(self) -> bytes:
        """
        Returns the signature as bytes.
        """
        pass


class AsymmetricVerificationContext(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self, data: bytes) -> None:
        """
        Processes the provided bytes and returns nothing.
        """
        pass

    @abc.abstractmethod
    def verify(self) -> None:
        """
        Raises an exception if the bytes provided to update do not match the
        signature or the signature does not match the public key.
        """
        pass