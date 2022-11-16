# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\backends\openssl\hashes.py
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.primitives import hashes

class _HashContext(hashes.HashContext):

    def __init__(self, backend, algorithm: hashes.HashAlgorithm, ctx=None):
        self._algorithm = algorithm
        self._backend = backend
        if ctx is None:
            ctx = self._backend._lib.EVP_MD_CTX_new()
            ctx = self._backend._ffi.gc(ctx, self._backend._lib.EVP_MD_CTX_free)
            evp_md = self._backend._evp_md_from_algorithm(algorithm)
            if evp_md == self._backend._ffi.NULL:
                raise UnsupportedAlgorithm('{} is not a supported hash on this backend.'.format(algorithm.name), _Reasons.UNSUPPORTED_HASH)
            res = self._backend._lib.EVP_DigestInit_ex(ctx, evp_md, self._backend._ffi.NULL)
            self._backend.openssl_assert(res != 0)
        self._ctx = ctx

    @property
    def algorithm(self) -> hashes.HashAlgorithm:
        return self._algorithm

    def copy(self) -> '_HashContext':
        copied_ctx = self._backend._lib.EVP_MD_CTX_new()
        copied_ctx = self._backend._ffi.gc(copied_ctx, self._backend._lib.EVP_MD_CTX_free)
        res = self._backend._lib.EVP_MD_CTX_copy_ex(copied_ctx, self._ctx)
        self._backend.openssl_assert(res != 0)
        return _HashContext((self._backend), (self.algorithm), ctx=copied_ctx)

    def update(self, data: bytes) -> None:
        data_ptr = self._backend._ffi.from_buffer(data)
        res = self._backend._lib.EVP_DigestUpdate(self._ctx, data_ptr, len(data))
        self._backend.openssl_assert(res != 0)

    def finalize(self) -> bytes:
        if isinstance(self.algorithm, hashes.ExtendableOutputFunction):
            return self._finalize_xof()
        else:
            buf = self._backend._ffi.new('unsigned char[]', self._backend._lib.EVP_MAX_MD_SIZE)
            outlen = self._backend._ffi.new('unsigned int *')
            res = self._backend._lib.EVP_DigestFinal_ex(self._ctx, buf, outlen)
            self._backend.openssl_assert(res != 0)
            self._backend.openssl_assert(outlen[0] == self.algorithm.digest_size)
            return self._backend._ffi.buffer(buf)[:outlen[0]]

    def _finalize_xof(self) -> bytes:
        buf = self._backend._ffi.new('unsigned char[]', self.algorithm.digest_size)
        res = self._backend._lib.EVP_DigestFinalXOF(self._ctx, buf, self.algorithm.digest_size)
        self._backend.openssl_assert(res != 0)
        return self._backend._ffi.buffer(buf)[:self.algorithm.digest_size]