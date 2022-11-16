# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\rsa.py
import abc, typing
from math import gcd
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import Backend, RSABackend
from cryptography.hazmat.primitives import _serialization, hashes
from cryptography.hazmat.primitives._asymmetric import AsymmetricPadding
from cryptography.hazmat.primitives.asymmetric import AsymmetricSignatureContext, AsymmetricVerificationContext, utils as asym_utils

class RSAPrivateKey(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def signer(self, padding: AsymmetricPadding, algorithm: hashes.HashAlgorithm) -> AsymmetricSignatureContext:
        """
        Returns an AsymmetricSignatureContext used for signing data.
        """
        pass

    @abc.abstractmethod
    def decrypt(self, ciphertext: bytes, padding: AsymmetricPadding) -> bytes:
        """
        Decrypts the provided ciphertext.
        """
        pass

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        The bit length of the public modulus.
        """
        pass

    @abc.abstractmethod
    def public_key(self) -> 'RSAPublicKey':
        """
        The RSAPublicKey associated with this private key.
        """
        pass

    @abc.abstractmethod
    def sign(self, data: bytes, padding: AsymmetricPadding, algorithm: typing.Union[(asym_utils.Prehashed, hashes.HashAlgorithm)]) -> bytes:
        """
        Signs the data.
        """
        pass

    @abc.abstractmethod
    def private_numbers(self) -> 'RSAPrivateNumbers':
        """
        Returns an RSAPrivateNumbers.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding: _serialization.Encoding, format: _serialization.PrivateFormat, encryption_algorithm: _serialization.KeySerializationEncryption) -> bytes:
        """
        Returns the key serialized as bytes.
        """
        pass


RSAPrivateKeyWithSerialization = RSAPrivateKey

class RSAPublicKey(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def verifier(self, signature: bytes, padding: AsymmetricPadding, algorithm: hashes.HashAlgorithm) -> AsymmetricVerificationContext:
        """
        Returns an AsymmetricVerificationContext used for verifying signatures.
        """
        pass

    @abc.abstractmethod
    def encrypt(self, plaintext: bytes, padding: AsymmetricPadding) -> bytes:
        """
        Encrypts the given plaintext.
        """
        pass

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        The bit length of the public modulus.
        """
        pass

    @abc.abstractmethod
    def public_numbers(self) -> 'RSAPublicNumbers':
        """
        Returns an RSAPublicNumbers
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding: _serialization.Encoding, format: _serialization.PublicFormat) -> bytes:
        """
        Returns the key serialized as bytes.
        """
        pass

    @abc.abstractmethod
    def verify(self, signature: bytes, data: bytes, padding: AsymmetricPadding, algorithm: typing.Union[(asym_utils.Prehashed, hashes.HashAlgorithm)]) -> None:
        """
        Verifies the signature of the data.
        """
        pass

    @abc.abstractmethod
    def recover_data_from_signature(self, signature: bytes, padding: AsymmetricPadding, algorithm: typing.Optional[hashes.HashAlgorithm]) -> bytes:
        """
        Recovers the original data from the signature.
        """
        pass


RSAPublicKeyWithSerialization = RSAPublicKey

def generate_private_key(public_exponent: int, key_size: int, backend: typing.Optional[Backend]=None) -> RSAPrivateKey:
    backend = _get_backend(backend)
    if not isinstance(backend, RSABackend):
        raise UnsupportedAlgorithm('Backend object does not implement RSABackend.', _Reasons.BACKEND_MISSING_INTERFACE)
    _verify_rsa_parameters(public_exponent, key_size)
    return backend.generate_rsa_private_key(public_exponent, key_size)


def _verify_rsa_parameters(public_exponent: int, key_size: int) -> None:
    if public_exponent not in (3, 65537):
        raise ValueError('public_exponent must be either 3 (for legacy compatibility) or 65537. Almost everyone should choose 65537 here!')
    if key_size < 512:
        raise ValueError('key_size must be at least 512-bits.')


def _check_private_key_components(p: int, q: int, private_exponent: int, dmp1: int, dmq1: int, iqmp: int, public_exponent: int, modulus: int) -> None:
    if modulus < 3:
        raise ValueError('modulus must be >= 3.')
    else:
        if p >= modulus:
            raise ValueError('p must be < modulus.')
        else:
            if q >= modulus:
                raise ValueError('q must be < modulus.')
            else:
                if dmp1 >= modulus:
                    raise ValueError('dmp1 must be < modulus.')
                else:
                    if dmq1 >= modulus:
                        raise ValueError('dmq1 must be < modulus.')
                    else:
                        if iqmp >= modulus:
                            raise ValueError('iqmp must be < modulus.')
                        if private_exponent >= modulus:
                            raise ValueError('private_exponent must be < modulus.')
                        if public_exponent < 3 or public_exponent >= modulus:
                            raise ValueError('public_exponent must be >= 3 and < modulus.')
                    if public_exponent & 1 == 0:
                        raise ValueError('public_exponent must be odd.')
                if dmp1 & 1 == 0:
                    raise ValueError('dmp1 must be odd.')
            if dmq1 & 1 == 0:
                raise ValueError('dmq1 must be odd.')
        if p * q != modulus:
            raise ValueError('p*q must equal modulus.')


def _check_public_key_components(e: int, n: int) -> None:
    if n < 3:
        raise ValueError('n must be >= 3.')
    else:
        if e < 3 or e >= n:
            raise ValueError('e must be >= 3 and < n.')
        if e & 1 == 0:
            raise ValueError('e must be odd.')


def _modinv(e: int, m: int) -> int:
    """
    Modular Multiplicative Inverse. Returns x such that: (x*e) mod m == 1
    """
    x1, x2 = (1, 0)
    a, b = e, m
    while b > 0:
        q, r = divmod(a, b)
        xn = x1 - q * x2
        a, b, x1, x2 = (b, r, x2, xn)

    return x1 % m


def rsa_crt_iqmp(p: int, q: int) -> int:
    """
    Compute the CRT (q ** -1) % p value from RSA primes p and q.
    """
    return _modinv(q, p)


def rsa_crt_dmp1(private_exponent: int, p: int) -> int:
    """
    Compute the CRT private_exponent % (p - 1) value from the RSA
    private_exponent (d) and p.
    """
    return private_exponent % (p - 1)


def rsa_crt_dmq1(private_exponent: int, q: int) -> int:
    """
    Compute the CRT private_exponent % (q - 1) value from the RSA
    private_exponent (d) and q.
    """
    return private_exponent % (q - 1)


_MAX_RECOVERY_ATTEMPTS = 1000

def rsa_recover_prime_factors(n: int, e: int, d: int) -> typing.Tuple[(int, int)]:
    """
    Compute factors p and q from the private exponent d. We assume that n has
    no more than two factors. This function is adapted from code in PyCrypto.
    """
    ktot = d * e - 1
    t = ktot
    while t % 2 == 0:
        t = t // 2

    spotted = False
    a = 2
    while not spotted and a < _MAX_RECOVERY_ATTEMPTS:
        k = t
        while k < ktot:
            cand = pow(a, k, n)
            if cand != 1:
                if cand != n - 1:
                    if pow(cand, 2, n) == 1:
                        p = gcd(cand + 1, n)
                        spotted = True
                        break
            k *= 2

        a += 2

    if not spotted:
        raise ValueError('Unable to compute factors p and q from exponent d.')
    else:
        q, r = divmod(n, p)
        assert r == 0
    p, q = sorted((p, q), reverse=True)
    return (p, q)


class RSAPrivateNumbers(object):

    def __init__(self, p: int, q: int, d: int, dmp1: int, dmq1: int, iqmp: int, public_numbers: 'RSAPublicNumbers'):
        if not isinstance(p, int) or not isinstance(q, int) or not isinstance(d, int) or not isinstance(dmp1, int) or not isinstance(dmq1, int) or not isinstance(iqmp, int):
            raise TypeError('RSAPrivateNumbers p, q, d, dmp1, dmq1, iqmp arguments must all be an integers.')
        if not isinstance(public_numbers, RSAPublicNumbers):
            raise TypeError('RSAPrivateNumbers public_numbers must be an RSAPublicNumbers instance.')
        self._p = p
        self._q = q
        self._d = d
        self._dmp1 = dmp1
        self._dmq1 = dmq1
        self._iqmp = iqmp
        self._public_numbers = public_numbers

    p = property(lambda self: self._p)
    q = property(lambda self: self._q)
    d = property(lambda self: self._d)
    dmp1 = property(lambda self: self._dmp1)
    dmq1 = property(lambda self: self._dmq1)
    iqmp = property(lambda self: self._iqmp)
    public_numbers = property(lambda self: self._public_numbers)

    def private_key(self, backend: typing.Optional[Backend]=None) -> RSAPrivateKey:
        backend = _get_backend(backend)
        return backend.load_rsa_private_numbers(self)

    def __eq__(self, other):
        if not isinstance(other, RSAPrivateNumbers):
            return NotImplemented
        else:
            return self.p == other.p and self.q == other.q and self.d == other.d and self.dmp1 == other.dmp1 and self.dmq1 == other.dmq1 and self.iqmp == other.iqmp and self.public_numbers == other.public_numbers

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((
         self.p,
         self.q,
         self.d,
         self.dmp1,
         self.dmq1,
         self.iqmp,
         self.public_numbers))


class RSAPublicNumbers(object):

    def __init__(self, e: int, n: int):
        if not isinstance(e, int) or not isinstance(n, int):
            raise TypeError('RSAPublicNumbers arguments must be integers.')
        self._e = e
        self._n = n

    e = property(lambda self: self._e)
    n = property(lambda self: self._n)

    def public_key(self, backend: typing.Optional[Backend]=None) -> RSAPublicKey:
        backend = _get_backend(backend)
        return backend.load_rsa_public_numbers(self)

    def __repr__(self):
        return '<RSAPublicNumbers(e={0.e}, n={0.n})>'.format(self)

    def __eq__(self, other):
        if not isinstance(other, RSAPublicNumbers):
            return NotImplemented
        else:
            return self.e == other.e and self.n == other.n

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.e, self.n))