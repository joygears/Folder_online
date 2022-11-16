# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\utils.py
import abc, enum, inspect, sys, types, typing, warnings

class CryptographyDeprecationWarning(UserWarning):
    pass


PersistentlyDeprecated2017 = CryptographyDeprecationWarning
PersistentlyDeprecated2019 = CryptographyDeprecationWarning
DeprecatedIn34 = CryptographyDeprecationWarning
DeprecatedIn35 = CryptographyDeprecationWarning

def _check_bytes(name: str, value: bytes) -> None:
    if not isinstance(value, bytes):
        raise TypeError('{} must be bytes'.format(name))


def _check_byteslike(name: str, value: bytes) -> None:
    try:
        memoryview(value)
    except TypeError:
        raise TypeError('{} must be bytes-like'.format(name))


def read_only_property(name: str):
    return property(lambda self: getattr(self, name))


if typing.TYPE_CHECKING:
    from typing_extensions import Protocol
    _T_class = typing.TypeVar('_T_class', bound=type)

    class _RegisterDecoratorType(Protocol):

        def __call__(self, klass: _T_class, *, check_annotations: bool=False) -> _T_class:
            pass


def register_interface(iface: abc.ABCMeta) -> '_RegisterDecoratorType':

    def register_decorator(klass, *, check_annotations=False):
        verify_interface(iface, klass, check_annotations=check_annotations)
        iface.register(klass)
        return klass

    return register_decorator


def int_to_bytes(integer: int, length: typing.Optional[int]=None) -> bytes:
    return integer.to_bytes(length or (integer.bit_length() + 7) // 8 or 1, 'big')


class InterfaceNotImplemented(Exception):
    pass


def strip_annotation(signature):
    return inspect.Signature([param.replace(annotation=(inspect.Parameter.empty)) for param in signature.parameters.values()])


def verify_interface(iface, klass, *, check_annotations=False):
    for method in iface.__abstractmethods__:
        if not hasattr(klass, method):
            raise InterfaceNotImplemented('{} is missing a {!r} method'.format(klass, method))
        else:
            if isinstance(getattr(iface, method), abc.abstractproperty):
                pass
            else:
                sig = inspect.signature(getattr(iface, method))
                actual = inspect.signature(getattr(klass, method))
                if check_annotations:
                    ok = sig == actual
                else:
                    ok = strip_annotation(sig) == strip_annotation(actual)
        if not ok:
            raise InterfaceNotImplemented("{}.{}'s signature differs from the expected. Expected: {!r}. Received: {!r}".format(klass, method, sig, actual))


class _DeprecatedValue(object):

    def __init__(self, value, message, warning_class):
        self.value = value
        self.message = message
        self.warning_class = warning_class


class _ModuleWithDeprecations(types.ModuleType):

    def __init__(self, module):
        super().__init__(module.__name__)
        self.__dict__['_module'] = module

    def __getattr__(self, attr):
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn((obj.message), (obj.warning_class), stacklevel=2)
            obj = obj.value
        return obj

    def __setattr__(self, attr, value):
        setattr(self._module, attr, value)

    def __delattr__(self, attr):
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn((obj.message), (obj.warning_class), stacklevel=2)
        delattr(self._module, attr)

    def __dir__(self):
        return [
         '_module'] + dir(self._module)


def deprecated(value, module_name, message, warning_class):
    module = sys.modules[module_name]
    if not isinstance(module, _ModuleWithDeprecations):
        sys.modules[module_name] = _ModuleWithDeprecations(module)
    return _DeprecatedValue(value, message, warning_class)


def cached_property(func):
    cached_name = '_cached_{}'.format(func)
    sentinel = object()

    def inner(instance):
        cache = getattr(instance, cached_name, sentinel)
        if cache is not sentinel:
            return cache
        else:
            result = func(instance)
            setattr(instance, cached_name, result)
            return result

    return property(inner)


int_from_bytes = deprecated(int.from_bytes, __name__, 'int_from_bytes is deprecated, use int.from_bytes instead', DeprecatedIn34)

class Enum(enum.Enum):

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self._name_}: {self._value_!r}>"

    def __str__(self):
        return f"{self.__class__.__name__}.{self._name_}"