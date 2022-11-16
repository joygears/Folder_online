# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\hashes.py
import abc, typing
from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import Backend, HashBackend

class HashAlgorithm(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def name(self) -> str:
        """
        A string naming this algorithm (e.g. "sha256", "md5").
        """
        pass

    @abc.abstractproperty
    def digest_size(self) -> int:
        """
        The size of the resulting digest in bytes.
        """
        pass

    @abc.abstractproperty
    def block_size(self) -> typing.Optional[int]:
        """
        The internal block size of the hash function, or None if the hash
        function does not use blocks internally (e.g. SHA3).
        """
        pass


class HashContext(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def algorithm(self) -> HashAlgorithm:
        """
        A HashAlgorithm that will be used by this context.
        """
        pass

    @abc.abstractmethod
    def update(self, data: bytes) -> None:
        """
        Processes the provided bytes through the hash.
        """
        pass

    @abc.abstractmethod
    def finalize(self) -> bytes:
        """
        Finalizes the hash context and returns the hash digest as bytes.
        """
        pass

    @abc.abstractmethod
    def copy(self) -> 'HashContext':
        """
        Return a HashContext that is a copy of the current context.
        """
        pass


class ExtendableOutputFunction(metaclass=abc.ABCMeta):
    __doc__ = '\n    An interface for extendable output functions.\n    '


class Hash(HashContext):

    def __init__(self, algorithm: HashAlgorithm, backend: typing.Optional[Backend]=None, ctx: typing.Optional['HashContext']=None):
        backend = _get_backend(backend)
        if not isinstance(backend, HashBackend):
            raise UnsupportedAlgorithm('Backend object does not implement HashBackend.', _Reasons.BACKEND_MISSING_INTERFACE)
        else:
            if not isinstance(algorithm, HashAlgorithm):
                raise TypeError('Expected instance of hashes.HashAlgorithm.')
            self._algorithm = algorithm
            self._backend = backend
            if ctx is None:
                self._ctx = self._backend.create_hash_ctx(self.algorithm)
            else:
                self._ctx = ctx

    @property
    def algorithm(self) -> HashAlgorithm:
        return self._algorithm

    def update(self, data: bytes) -> None:
        if self._ctx is None:
            raise AlreadyFinalized('Context was already finalized.')
        utils._check_byteslike('data', data)
        self._ctx.update(data)

    def copy(self) -> 'Hash':
        if self._ctx is None:
            raise AlreadyFinalized('Context was already finalized.')
        return Hash((self.algorithm),
          backend=(self._backend), ctx=(self._ctx.copy()))

    def finalize(self) -> bytes:
        if self._ctx is None:
            raise AlreadyFinalized('Context was already finalized.')
        digest = self._ctx.finalize()
        self._ctx = None
        return digest


class SHA1(HashAlgorithm):
    name = 'sha1'
    digest_size = 20
    block_size = 64


class SHA512_224(HashAlgorithm):
    name = 'sha512-224'
    digest_size = 28
    block_size = 128


class SHA512_256(HashAlgorithm):
    name = 'sha512-256'
    digest_size = 32
    block_size = 128


class SHA224(HashAlgorithm):
    name = 'sha224'
    digest_size = 28
    block_size = 64


class SHA256(HashAlgorithm):
    name = 'sha256'
    digest_size = 32
    block_size = 64


class SHA384(HashAlgorithm):
    name = 'sha384'
    digest_size = 48
    block_size = 128


class SHA512(HashAlgorithm):
    name = 'sha512'
    digest_size = 64
    block_size = 128


class SHA3_224(HashAlgorithm):
    name = 'sha3-224'
    digest_size = 28
    block_size = None


class SHA3_256(HashAlgorithm):
    name = 'sha3-256'
    digest_size = 32
    block_size = None


class SHA3_384(HashAlgorithm):
    name = 'sha3-384'
    digest_size = 48
    block_size = None


class SHA3_512(HashAlgorithm):
    name = 'sha3-512'
    digest_size = 64
    block_size = None


class SHAKE128(HashAlgorithm, ExtendableOutputFunction):
    name = 'shake128'
    block_size = None

    def __init__(self, digest_size: int):
        if not isinstance(digest_size, int):
            raise TypeError('digest_size must be an integer')
        if digest_size < 1:
            raise ValueError('digest_size must be a positive integer')
        self._digest_size = digest_size

    @property
    def digest_size(self) -> int:
        return self._digest_size


class SHAKE256(HashAlgorithm, ExtendableOutputFunction):
    name = 'shake256'
    block_size = None

    def __init__(self, digest_size: int):
        if not isinstance(digest_size, int):
            raise TypeError('digest_size must be an integer')
        if digest_size < 1:
            raise ValueError('digest_size must be a positive integer')
        self._digest_size = digest_size

    @property
    def digest_size(self) -> int:
        return self._digest_size


class MD5(HashAlgorithm):
    name = 'md5'
    digest_size = 16
    block_size = 64


class BLAKE2b(HashAlgorithm):
    name = 'blake2b'
    _max_digest_size = 64
    _min_digest_size = 1
    block_size = 128

    def __init__(self, digest_size: int):
        if digest_size != 64:
            raise ValueError('Digest size must be 64')
        self._digest_size = digest_size

    @property
    def digest_size(self) -> int:
        return self._digest_size


class BLAKE2s(HashAlgorithm):
    name = 'blake2s'
    block_size = 64
    _max_digest_size = 32
    _min_digest_size = 1

    def __init__(self, digest_size: int):
        if digest_size != 32:
            raise ValueError('Digest size must be 32')
        self._digest_size = digest_size

    @property
    def digest_size(self) -> int:
        return self._digest_size


class SM3(HashAlgorithm):
    name = 'sm3'
    digest_size = 32
    block_size = 64