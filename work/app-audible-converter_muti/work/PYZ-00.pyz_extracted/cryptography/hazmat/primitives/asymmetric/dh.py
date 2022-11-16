# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\dh.py
import abc, typing
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import Backend
from cryptography.hazmat.primitives import serialization
_MIN_MODULUS_SIZE = 512

def generate_parameters(generator: int, key_size: int, backend: typing.Optional[Backend]=None) -> 'DHParameters':
    backend = _get_backend(backend)
    return backend.generate_dh_parameters(generator, key_size)


class DHParameterNumbers(object):

    def __init__(self, p: int, g: int, q: typing.Optional[int]=None) -> None:
        if not isinstance(p, int) or not isinstance(g, int):
            raise TypeError('p and g must be integers')
        else:
            if q is not None:
                if not isinstance(q, int):
                    raise TypeError('q must be integer or None')
            if g < 2:
                raise ValueError('DH generator must be 2 or greater')
            if p.bit_length() < _MIN_MODULUS_SIZE:
                raise ValueError('p (modulus) must be at least {}-bit'.format(_MIN_MODULUS_SIZE))
        self._p = p
        self._g = g
        self._q = q

    def __eq__(self, other):
        if not isinstance(other, DHParameterNumbers):
            return NotImplemented
        else:
            return self._p == other._p and self._g == other._g and self._q == other._q

    def __ne__(self, other):
        return not self == other

    def parameters(self, backend: typing.Optional[Backend]=None) -> 'DHParameters':
        backend = _get_backend(backend)
        return backend.load_dh_parameter_numbers(self)

    p = property(lambda self: self._p)
    g = property(lambda self: self._g)
    q = property(lambda self: self._q)


class DHPublicNumbers(object):

    def __init__(self, y: int, parameter_numbers: DHParameterNumbers) -> None:
        if not isinstance(y, int):
            raise TypeError('y must be an integer.')
        if not isinstance(parameter_numbers, DHParameterNumbers):
            raise TypeError('parameters must be an instance of DHParameterNumbers.')
        self._y = y
        self._parameter_numbers = parameter_numbers

    def __eq__(self, other):
        if not isinstance(other, DHPublicNumbers):
            return NotImplemented
        else:
            return self._y == other._y and self._parameter_numbers == other._parameter_numbers

    def __ne__(self, other):
        return not self == other

    def public_key(self, backend: typing.Optional[Backend]=None) -> 'DHPublicKey':
        backend = _get_backend(backend)
        return backend.load_dh_public_numbers(self)

    y = property(lambda self: self._y)
    parameter_numbers = property(lambda self: self._parameter_numbers)


class DHPrivateNumbers(object):

    def __init__(self, x: int, public_numbers: DHPublicNumbers) -> None:
        if not isinstance(x, int):
            raise TypeError('x must be an integer.')
        if not isinstance(public_numbers, DHPublicNumbers):
            raise TypeError('public_numbers must be an instance of DHPublicNumbers.')
        self._x = x
        self._public_numbers = public_numbers

    def __eq__(self, other):
        if not isinstance(other, DHPrivateNumbers):
            return NotImplemented
        else:
            return self._x == other._x and self._public_numbers == other._public_numbers

    def __ne__(self, other):
        return not self == other

    def private_key(self, backend: typing.Optional[Backend]=None) -> 'DHPrivateKey':
        backend = _get_backend(backend)
        return backend.load_dh_private_numbers(self)

    public_numbers = property(lambda self: self._public_numbers)
    x = property(lambda self: self._x)


class DHParameters(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def generate_private_key(self) -> 'DHPrivateKey':
        """
        Generates and returns a DHPrivateKey.
        """
        pass

    @abc.abstractmethod
    def parameter_bytes(self, encoding: 'serialization.Encoding', format: 'serialization.ParameterFormat') -> bytes:
        """
        Returns the parameters serialized as bytes.
        """
        pass

    @abc.abstractmethod
    def parameter_numbers(self) -> DHParameterNumbers:
        """
        Returns a DHParameterNumbers.
        """
        pass


DHParametersWithSerialization = DHParameters

class DHPublicKey(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        The bit length of the prime modulus.
        """
        pass

    @abc.abstractmethod
    def parameters(self) -> DHParameters:
        """
        The DHParameters object associated with this public key.
        """
        pass

    @abc.abstractmethod
    def public_numbers(self) -> DHPublicNumbers:
        """
        Returns a DHPublicNumbers.
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding: 'serialization.Encoding', format: 'serialization.PublicFormat') -> bytes:
        """
        Returns the key serialized as bytes.
        """
        pass


DHPublicKeyWithSerialization = DHPublicKey

class DHPrivateKey(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        The bit length of the prime modulus.
        """
        pass

    @abc.abstractmethod
    def public_key(self) -> DHPublicKey:
        """
        The DHPublicKey associated with this private key.
        """
        pass

    @abc.abstractmethod
    def parameters(self) -> DHParameters:
        """
        The DHParameters object associated with this private key.
        """
        pass

    @abc.abstractmethod
    def exchange(self, peer_public_key: DHPublicKey) -> bytes:
        """
        Given peer's DHPublicKey, carry out the key exchange and
        return shared key as bytes.
        """
        pass

    @abc.abstractmethod
    def private_numbers(self) -> DHPrivateNumbers:
        """
        Returns a DHPrivateNumbers.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding: 'serialization.Encoding', format: 'serialization.PrivateFormat', encryption_algorithm: 'serialization.KeySerializationEncryption') -> bytes:
        """
        Returns the key serialized as bytes.
        """
        pass


DHPrivateKeyWithSerialization = DHPrivateKey