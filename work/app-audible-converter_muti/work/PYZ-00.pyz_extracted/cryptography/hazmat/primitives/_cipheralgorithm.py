# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\_cipheralgorithm.py
import abc, typing

class CipherAlgorithm(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def name(self) -> str:
        """
        A string naming this mode (e.g. "AES", "Camellia").
        """
        pass

    @abc.abstractproperty
    def key_sizes(self) -> typing.FrozenSet[int]:
        """
        Valid key sizes for this algorithm in bits
        """
        pass

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        The size of the key being used as an integer in bits (e.g. 128, 256).
        """
        pass


class BlockCipherAlgorithm(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def block_size(self) -> int:
        """
        The size of a block as an integer in bits (e.g. 64, 128).
        """
        pass