# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: typing.py
import abc
from abc import abstractmethod, abstractproperty
import collections, contextlib, functools, re as stdlib_re, sys, types
try:
    import collections.abc as collections_abc
except ImportError:
    import collections as collections_abc

if sys.version_info[:2] >= (3, 6):
    import _collections_abc
try:
    from types import WrapperDescriptorType, MethodWrapperType, MethodDescriptorType
except ImportError:
    WrapperDescriptorType = type(object.__init__)
    MethodWrapperType = type(object().__str__)
    MethodDescriptorType = type(str.join)

__all__ = [
 'Any',
 'Callable',
 'ClassVar',
 'Generic',
 'Optional',
 'Tuple',
 'Type',
 'TypeVar',
 'Union',
 'AbstractSet',
 'GenericMeta',
 'ByteString',
 'Container',
 'ContextManager',
 'Hashable',
 'ItemsView',
 'Iterable',
 'Iterator',
 'KeysView',
 'Mapping',
 'MappingView',
 'MutableMapping',
 'MutableSequence',
 'MutableSet',
 'Sequence',
 'Sized',
 'ValuesView',
 'Reversible',
 'SupportsAbs',
 'SupportsBytes',
 'SupportsComplex',
 'SupportsFloat',
 'SupportsInt',
 'SupportsRound',
 'Counter',
 'Deque',
 'Dict',
 'DefaultDict',
 'List',
 'Set',
 'FrozenSet',
 'NamedTuple',
 'Generator',
 'AnyStr',
 'cast',
 'get_type_hints',
 'NewType',
 'no_type_check',
 'no_type_check_decorator',
 'overload',
 'Text',
 'TYPE_CHECKING']

def _qualname(x):
    if sys.version_info[:2] >= (3, 3):
        return x.__qualname__
    else:
        return x.__name__


def _trim_name(nm):
    whitelist = ('_TypeAlias', '_ForwardRef', '_TypingBase', '_FinalTypingBase')
    if nm.startswith('_'):
        if nm not in whitelist:
            nm = nm[1:]
    return nm


class TypingMeta(type):
    __doc__ = "Metaclass for most types defined in typing module\n    (not a part of public API).\n\n    This overrides __new__() to require an extra keyword parameter\n    '_root', which serves as a guard against naive subclassing of the\n    typing classes.  Any legitimate class defined using a metaclass\n    derived from TypingMeta must pass _root=True.\n\n    This also defines a dummy constructor (all the work for most typing\n    constructs is done in __new__) and a nicer repr().\n    "
    _is_protocol = False

    def __new__(cls, name, bases, namespace, *, _root=False):
        if not _root:
            raise TypeError('Cannot subclass %s' % (', '.join(map(_type_repr, bases)) or '()'))
        return super().__new__(cls, name, bases, namespace)

    def __init__(self, *args, **kwds):
        pass

    def _eval_type(self, globalns, localns):
        """Override this in subclasses to interpret forward references.

        For example, List['C'] is internally stored as
        List[_ForwardRef('C')], which should evaluate to List[C],
        where C is an object found in globalns or localns (searching
        localns first, of course).
        """
        return self

    def _get_type_vars(self, tvars):
        pass

    def __repr__(self):
        qname = _trim_name(_qualname(self))
        return '%s.%s' % (self.__module__, qname)


class _TypingBase(metaclass=TypingMeta, _root=True):
    __doc__ = 'Internal indicator of special typing constructs.'
    __slots__ = ('__weakref__', )

    def __init__(self, *args, **kwds):
        pass

    def __new__(cls, *args, **kwds):
        if len(args) == 3:
            if isinstance(args[0], str):
                if isinstance(args[1], tuple):
                    raise TypeError('Cannot subclass %r' % cls)
        return super().__new__(cls)

    def _eval_type(self, globalns, localns):
        return self

    def _get_type_vars(self, tvars):
        pass

    def __repr__(self):
        cls = type(self)
        qname = _trim_name(_qualname(cls))
        return '%s.%s' % (cls.__module__, qname)

    def __call__(self, *args, **kwds):
        raise TypeError('Cannot instantiate %r' % type(self))


class _FinalTypingBase(_TypingBase, _root=True):
    __doc__ = 'Internal mix-in class to prevent instantiation.\n\n    Prevents instantiation unless _root=True is given in class call.\n    It is used to create pseudo-singleton instances Any, Union, Optional, etc.\n    '
    __slots__ = ()

    def __new__(cls, *args, _root=False, **kwds):
        self = (super().__new__)(cls, *args, **kwds)
        if _root is True:
            return self
        raise TypeError('Cannot instantiate %r' % cls)

    def __reduce__(self):
        return _trim_name(type(self).__name__)


class _ForwardRef(_TypingBase, _root=True):
    __doc__ = 'Internal wrapper to hold a forward reference.'
    __slots__ = ('__forward_arg__', '__forward_code__', '__forward_evaluated__', '__forward_value__')

    def __init__(self, arg):
        super().__init__(arg)
        if not isinstance(arg, str):
            raise TypeError('Forward reference must be a string -- got %r' % (arg,))
        try:
            code = compile(arg, '<string>', 'eval')
        except SyntaxError:
            raise SyntaxError('Forward reference must be an expression -- got %r' % (
             arg,))

        self.__forward_arg__ = arg
        self.__forward_code__ = code
        self.__forward_evaluated__ = False
        self.__forward_value__ = None

    def _eval_type(self, globalns, localns):
        if not self.__forward_evaluated__ or localns is not globalns:
            if globalns is None:
                if localns is None:
                    globalns = localns = {}
            if globalns is None:
                globalns = localns
            else:
                if localns is None:
                    localns = globalns
            self.__forward_value__ = _type_check(eval(self.__forward_code__, globalns, localns), 'Forward references must evaluate to types.')
            self.__forward_evaluated__ = True
        return self.__forward_value__

    def __eq__(self, other):
        if not isinstance(other, _ForwardRef):
            return NotImplemented
        else:
            return self.__forward_arg__ == other.__forward_arg__ and self.__forward_value__ == other.__forward_value__

    def __hash__(self):
        return hash((self.__forward_arg__, self.__forward_value__))

    def __instancecheck__(self, obj):
        raise TypeError('Forward references cannot be used with isinstance().')

    def __subclasscheck__(self, cls):
        raise TypeError('Forward references cannot be used with issubclass().')

    def __repr__(self):
        return '_ForwardRef(%r)' % (self.__forward_arg__,)


class _TypeAlias(_TypingBase, _root=True):
    __doc__ = "Internal helper class for defining generic variants of concrete types.\n\n    Note that this is not a type; let's call it a pseudo-type.  It cannot\n    be used in instance and subclass checks in parameterized form, i.e.\n    ``isinstance(42, Match[str])`` raises ``TypeError`` instead of returning\n    ``False``.\n    "
    __slots__ = ('name', 'type_var', 'impl_type', 'type_checker')

    def __init__(self, name, type_var, impl_type, type_checker):
        """Initializer.

        Args:
            name: The name, e.g. 'Pattern'.
            type_var: The type parameter, e.g. AnyStr, or the
                specific type, e.g. str.
            impl_type: The implementation type.
            type_checker: Function that takes an impl_type instance.
                and returns a value that should be a type_var instance.
        """
        if not isinstance(name, str):
            raise AssertionError(repr(name))
        else:
            if not isinstance(impl_type, type):
                raise AssertionError(repr(impl_type))
            elif not not isinstance(impl_type, TypingMeta):
                raise AssertionError(repr(impl_type))
            assert isinstance(type_var, (type, _TypingBase)), repr(type_var)
        self.name = name
        self.type_var = type_var
        self.impl_type = impl_type
        self.type_checker = type_checker

    def __repr__(self):
        return '%s[%s]' % (self.name, _type_repr(self.type_var))

    def __getitem__(self, parameter):
        if not isinstance(self.type_var, TypeVar):
            raise TypeError('%s cannot be further parameterized.' % self)
        else:
            if self.type_var.__constraints__:
                if isinstance(parameter, type):
                    if not issubclass(parameter, self.type_var.__constraints__):
                        raise TypeError('%s is not a valid substitution for %s.' % (
                         parameter, self.type_var))
            if isinstance(parameter, TypeVar):
                if parameter is not self.type_var:
                    raise TypeError('%s cannot be re-parameterized.' % self)
        return self.__class__(self.name, parameter, self.impl_type, self.type_checker)

    def __eq__(self, other):
        if not isinstance(other, _TypeAlias):
            return NotImplemented
        else:
            return self.name == other.name and self.type_var == other.type_var

    def __hash__(self):
        return hash((self.name, self.type_var))

    def __instancecheck__(self, obj):
        if not isinstance(self.type_var, TypeVar):
            raise TypeError('Parameterized type aliases cannot be used with isinstance().')
        return isinstance(obj, self.impl_type)

    def __subclasscheck__(self, cls):
        if not isinstance(self.type_var, TypeVar):
            raise TypeError('Parameterized type aliases cannot be used with issubclass().')
        return issubclass(cls, self.impl_type)


def _get_type_vars(types, tvars):
    for t in types:
        if isinstance(t, TypingMeta) or isinstance(t, _TypingBase):
            t._get_type_vars(tvars)


def _type_vars(types):
    tvars = []
    _get_type_vars(types, tvars)
    return tuple(tvars)


def _eval_type(t, globalns, localns):
    if isinstance(t, TypingMeta) or isinstance(t, _TypingBase):
        return t._eval_type(globalns, localns)
    else:
        return t


def _type_check(arg, msg):
    """Check that the argument is a type, and return it (internal helper).

    As a special case, accept None and return type(None) instead.
    Also, _TypeAlias instances (e.g. Match, Pattern) are acceptable.

    The msg argument is a human-readable error message, e.g.

        "Union[arg, ...]: arg should be a type."

    We append the repr() of the actual value (truncated to 100 chars).
    """
    if arg is None:
        return type(None)
    else:
        if isinstance(arg, str):
            arg = _ForwardRef(arg)
        else:
            if isinstance(arg, _TypingBase) and type(arg).__name__ == '_ClassVar' or not isinstance(arg, (type, _TypingBase)) and not callable(arg):
                raise TypeError(msg + ' Got %.100r.' % (arg,))
            if type(arg).__name__ in ('_Union', '_Optional') and not getattr(arg, '__origin__', None) or isinstance(arg, TypingMeta) and arg._gorg in (Generic, _Protocol):
                raise TypeError('Plain %s is not valid as type argument' % arg)
        return arg


def _type_repr(obj):
    """Return the repr() of an object, special-casing types (internal helper).

    If obj is a type, we return a shorter version than the default
    type.__repr__, based on the module and qualified name, which is
    typically enough to uniquely identify a type.  For everything
    else, we fall back on repr(obj).
    """
    if isinstance(obj, type) and not isinstance(obj, TypingMeta):
        if obj.__module__ == 'builtins':
            return _qualname(obj)
        return '%s.%s' % (obj.__module__, _qualname(obj))
    else:
        if obj is ...:
            return '...'
        if isinstance(obj, types.FunctionType):
            return obj.__name__
        return repr(obj)


class _Any(_FinalTypingBase, _root=True):
    __doc__ = 'Special type indicating an unconstrained type.\n\n    - Any is compatible with every type.\n    - Any assumed to have all methods.\n    - All values assumed to be instances of Any.\n\n    Note that all the above statements are true from the point of view of\n    static type checkers. At runtime, Any should not be used with instance\n    or class checks.\n    '
    __slots__ = ()

    def __instancecheck__(self, obj):
        raise TypeError('Any cannot be used with isinstance().')

    def __subclasscheck__(self, cls):
        raise TypeError('Any cannot be used with issubclass().')


Any = _Any(_root=True)

class _NoReturn(_FinalTypingBase, _root=True):
    __doc__ = "Special type indicating functions that never return.\n    Example::\n\n      from typing import NoReturn\n\n      def stop() -> NoReturn:\n          raise Exception('no way')\n\n    This type is invalid in other positions, e.g., ``List[NoReturn]``\n    will fail in static type checkers.\n    "
    __slots__ = ()

    def __instancecheck__(self, obj):
        raise TypeError('NoReturn cannot be used with isinstance().')

    def __subclasscheck__(self, cls):
        raise TypeError('NoReturn cannot be used with issubclass().')


NoReturn = _NoReturn(_root=True)

class TypeVar(_TypingBase, _root=True):
    __doc__ = "Type variable.\n\n    Usage::\n\n      T = TypeVar('T')  # Can be anything\n      A = TypeVar('A', str, bytes)  # Must be str or bytes\n\n    Type variables exist primarily for the benefit of static type\n    checkers.  They serve as the parameters for generic types as well\n    as for generic function definitions.  See class Generic for more\n    information on generic types.  Generic functions work as follows:\n\n      def repeat(x: T, n: int) -> List[T]:\n          '''Return a list containing n references to x.'''\n          return [x]*n\n\n      def longest(x: A, y: A) -> A:\n          '''Return the longest of two strings.'''\n          return x if len(x) >= len(y) else y\n\n    The latter example's signature is essentially the overloading\n    of (str, str) -> str and (bytes, bytes) -> bytes.  Also note\n    that if the arguments are instances of some subclass of str,\n    the return type is still plain str.\n\n    At runtime, isinstance(x, T) and issubclass(C, T) will raise TypeError.\n\n    Type variables defined with covariant=True or contravariant=True\n    can be used do declare covariant or contravariant generic types.\n    See PEP 484 for more details. By default generic types are invariant\n    in all type variables.\n\n    Type variables can be introspected. e.g.:\n\n      T.__name__ == 'T'\n      T.__constraints__ == ()\n      T.__covariant__ == False\n      T.__contravariant__ = False\n      A.__constraints__ == (str, bytes)\n    "
    __slots__ = ('__name__', '__bound__', '__constraints__', '__covariant__', '__contravariant__')

    def __init__(self, name, *constraints, bound=None, covariant=False, contravariant=False):
        (super().__init__)(name, *constraints, **{'bound':bound,  'covariant':covariant, 
         'contravariant':contravariant})
        self.__name__ = name
        if covariant:
            if contravariant:
                raise ValueError('Bivariant types are not supported.')
        self.__covariant__ = bool(covariant)
        self.__contravariant__ = bool(contravariant)
        if constraints:
            if bound is not None:
                raise TypeError('Constraints cannot be combined with bound=...')
        else:
            if constraints:
                if len(constraints) == 1:
                    raise TypeError('A single constraint is not allowed')
            msg = 'TypeVar(name, constraint, ...): constraints must be types.'
            self.__constraints__ = tuple(_type_check(t, msg) for t in constraints)
            if bound:
                self.__bound__ = _type_check(bound, 'Bound must be a type.')
            else:
                self.__bound__ = None

    def _get_type_vars(self, tvars):
        if self not in tvars:
            tvars.append(self)

    def __repr__(self):
        if self.__covariant__:
            prefix = '+'
        else:
            if self.__contravariant__:
                prefix = '-'
            else:
                prefix = '~'
        return prefix + self.__name__

    def __instancecheck__(self, instance):
        raise TypeError('Type variables cannot be used with isinstance().')

    def __subclasscheck__(self, cls):
        raise TypeError('Type variables cannot be used with issubclass().')


T = TypeVar('T')
KT = TypeVar('KT')
VT = TypeVar('VT')
T_co = TypeVar('T_co', covariant=True)
V_co = TypeVar('V_co', covariant=True)
VT_co = TypeVar('VT_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)
AnyStr = TypeVar('AnyStr', bytes, str)

def _replace_arg(arg, tvars, args):
    """An internal helper function: replace arg if it is a type variable
    found in tvars with corresponding substitution from args or
    with corresponding substitution sub-tree if arg is a generic type.
    """
    if tvars is None:
        tvars = []
    else:
        if hasattr(arg, '_subs_tree'):
            if isinstance(arg, (GenericMeta, _TypingBase)):
                return arg._subs_tree(tvars, args)
        if isinstance(arg, TypeVar):
            for i, tvar in enumerate(tvars):
                if arg == tvar:
                    return args[i]

    return arg


def _subs_tree(cls, tvars=None, args=None):
    """An internal helper function: calculate substitution tree
    for generic cls after replacing its type parameters with
    substitutions in tvars -> args (if any).
    Repeat the same following __origin__'s.

    Return a list of arguments with all possible substitutions
    performed. Arguments that are generic classes themselves are represented
    as tuples (so that no new classes are created by this function).
    For example: _subs_tree(List[Tuple[int, T]][str]) == [(Tuple, int, str)]
    """
    if cls.__origin__ is None:
        return cls
    else:
        current = cls.__origin__
        orig_chain = []
        while current.__origin__ is not None:
            orig_chain.append(current)
            current = current.__origin__

        tree_args = []
        for arg in cls.__args__:
            tree_args.append(_replace_arg(arg, tvars, args))

        for ocls in orig_chain:
            new_tree_args = []
            for arg in ocls.__args__:
                new_tree_args.append(_replace_arg(arg, ocls.__parameters__, tree_args))

            tree_args = new_tree_args

        return tree_args


def _remove_dups_flatten(parameters):
    """An internal helper for Union creation and substitution: flatten Union's
    among parameters, then remove duplicates and strict subclasses.
    """
    params = []
    for p in parameters:
        if isinstance(p, _Union) and p.__origin__ is Union:
            params.extend(p.__args__)
        elif isinstance(p, tuple) and len(p) > 0 and p[0] is Union:
            params.extend(p[1:])
        else:
            params.append(p)

    all_params = set(params)
    if len(all_params) < len(params):
        new_params = []
        for t in params:
            if t in all_params:
                new_params.append(t)
                all_params.remove(t)

        params = new_params
        if not not all_params:
            raise AssertionError(all_params)
    all_params = set(params)
    for t1 in params:
        if not isinstance(t1, type):
            pass
        else:
            if any(isinstance(t2, type) and issubclass(t1, t2) for t2 in all_params - {t1} if not (isinstance(t2, GenericMeta) and t2.__origin__ is not None)):
                all_params.remove(t1)

    return tuple(t for t in params if t in all_params)


def _check_generic(cls, parameters):
    if not cls.__parameters__:
        raise TypeError('%s is not a generic class' % repr(cls))
    alen = len(parameters)
    elen = len(cls.__parameters__)
    if alen != elen:
        raise TypeError('Too %s parameters for %s; actual %s, expected %s' % (
         'many' if alen > elen else 'few', repr(cls), alen, elen))


_cleanups = []

def _tp_cache(func):
    """Internal wrapper caching __getitem__ of generic types with a fallback to
    original function for non-hashable arguments.
    """
    cached = functools.lru_cache()(func)
    _cleanups.append(cached.cache_clear)

    @functools.wraps(func)
    def inner(*args, **kwds):
        try:
            return cached(*args, **kwds)
        except TypeError:
            pass

        return func(*args, **kwds)

    return inner


class _Union(_FinalTypingBase, _root=True):
    __doc__ = 'Union type; Union[X, Y] means either X or Y.\n\n    To define a union, use e.g. Union[int, str].  Details:\n\n    - The arguments must be types and there must be at least one.\n\n    - None as an argument is a special case and is replaced by\n      type(None).\n\n    - Unions of unions are flattened, e.g.::\n\n        Union[Union[int, str], float] == Union[int, str, float]\n\n    - Unions of a single argument vanish, e.g.::\n\n        Union[int] == int  # The constructor actually returns int\n\n    - Redundant arguments are skipped, e.g.::\n\n        Union[int, str, int] == Union[int, str]\n\n    - When comparing unions, the argument order is ignored, e.g.::\n\n        Union[int, str] == Union[str, int]\n\n    - When two arguments have a subclass relationship, the least\n      derived argument is kept, e.g.::\n\n        class Employee: pass\n        class Manager(Employee): pass\n        Union[int, Employee, Manager] == Union[int, Employee]\n        Union[Manager, int, Employee] == Union[int, Employee]\n        Union[Employee, Manager] == Employee\n\n    - Similar for object::\n\n        Union[int, object] == object\n\n    - You cannot subclass or instantiate a union.\n\n    - You can use Optional[X] as a shorthand for Union[X, None].\n    '
    __slots__ = ('__parameters__', '__args__', '__origin__', '__tree_hash__')

    def __new__(cls, parameters=None, origin=None, *args, _root=False):
        self = (super().__new__)(cls, parameters, origin, *args, **{'_root': _root})
        if origin is None:
            self.__parameters__ = None
            self.__args__ = None
            self.__origin__ = None
            self.__tree_hash__ = hash(frozenset(('Union', )))
            return self
        else:
            if not isinstance(parameters, tuple):
                raise TypeError('Expected parameters=<tuple>')
            else:
                if origin is Union:
                    parameters = _remove_dups_flatten(parameters)
                    if len(parameters) == 1:
                        return parameters[0]
                self.__parameters__ = _type_vars(parameters)
                self.__args__ = parameters
                self.__origin__ = origin
                subs_tree = self._subs_tree()
                if isinstance(subs_tree, tuple):
                    self.__tree_hash__ = hash(frozenset(subs_tree))
                else:
                    self.__tree_hash__ = hash(subs_tree)
            return self

    def _eval_type(self, globalns, localns):
        if self.__args__ is None:
            return self
        else:
            ev_args = tuple(_eval_type(t, globalns, localns) for t in self.__args__)
            ev_origin = _eval_type(self.__origin__, globalns, localns)
            if ev_args == self.__args__:
                if ev_origin == self.__origin__:
                    return self
            return self.__class__(ev_args, ev_origin, _root=True)

    def _get_type_vars(self, tvars):
        if self.__origin__:
            if self.__parameters__:
                _get_type_vars(self.__parameters__, tvars)

    def __repr__(self):
        if self.__origin__ is None:
            return super().__repr__()
        else:
            tree = self._subs_tree()
            if not isinstance(tree, tuple):
                return repr(tree)
            return tree[0]._tree_repr(tree)

    def _tree_repr(self, tree):
        arg_list = []
        for arg in tree[1:]:
            if not isinstance(arg, tuple):
                arg_list.append(_type_repr(arg))
            else:
                arg_list.append(arg[0]._tree_repr(arg))

        return super().__repr__() + '[%s]' % ', '.join(arg_list)

    @_tp_cache
    def __getitem__(self, parameters):
        if parameters == ():
            raise TypeError('Cannot take a Union of no types.')
        else:
            if not isinstance(parameters, tuple):
                parameters = (
                 parameters,)
            else:
                if self.__origin__ is None:
                    msg = 'Union[arg, ...]: each arg must be a type.'
                else:
                    msg = 'Parameters to generic types must be types.'
            parameters = tuple(_type_check(p, msg) for p in parameters)
            if self is not Union:
                _check_generic(self, parameters)
        return self.__class__(parameters, origin=self, _root=True)

    def _subs_tree(self, tvars=None, args=None):
        if self is Union:
            return Union
        else:
            tree_args = _subs_tree(self, tvars, args)
            tree_args = _remove_dups_flatten(tree_args)
            if len(tree_args) == 1:
                return tree_args[0]
            return (
             Union,) + tree_args

    def __eq__(self, other):
        if isinstance(other, _Union):
            return self.__tree_hash__ == other.__tree_hash__
        else:
            if self is not Union:
                return self._subs_tree() == other
            return self is other

    def __hash__(self):
        return self.__tree_hash__

    def __instancecheck__(self, obj):
        raise TypeError('Unions cannot be used with isinstance().')

    def __subclasscheck__(self, cls):
        raise TypeError('Unions cannot be used with issubclass().')


Union = _Union(_root=True)

class _Optional(_FinalTypingBase, _root=True):
    __doc__ = 'Optional type.\n\n    Optional[X] is equivalent to Union[X, None].\n    '
    __slots__ = ()

    @_tp_cache
    def __getitem__(self, arg):
        arg = _type_check(arg, 'Optional[t] requires a single type.')
        return Union[(arg, type(None))]


Optional = _Optional(_root=True)

def _next_in_mro(cls):
    """Helper for Generic.__new__.

    Returns the class after the last occurrence of Generic or
    Generic[...] in cls.__mro__.
    """
    next_in_mro = object
    for i, c in enumerate(cls.__mro__[:-1]):
        if isinstance(c, GenericMeta) and c._gorg is Generic:
            next_in_mro = cls.__mro__[(i + 1)]

    return next_in_mro


def _make_subclasshook(cls):
    """Construct a __subclasshook__ callable that incorporates
    the associated __extra__ class in subclass checks performed
    against cls.
    """
    if isinstance(cls.__extra__, abc.ABCMeta):

        def __extrahook__(subclass):
            res = cls.__extra__.__subclasshook__(subclass)
            if res is not NotImplemented:
                return res
            else:
                if cls.__extra__ in subclass.__mro__:
                    return True
                for scls in cls.__extra__.__subclasses__():
                    if isinstance(scls, GenericMeta):
                        pass
                    else:
                        if issubclass(subclass, scls):
                            return True

                return NotImplemented

    else:

        def __extrahook__(subclass):
            if cls.__extra__:
                if issubclass(subclass, cls.__extra__):
                    return True
            return NotImplemented

    return __extrahook__


def _no_slots_copy(dct):
    """Internal helper: copy class __dict__ and clean slots class variables.
    (They will be re-created if necessary by normal class machinery.)
    """
    dict_copy = dict(dct)
    if '__slots__' in dict_copy:
        for slot in dict_copy['__slots__']:
            dict_copy.pop(slot, None)

    return dict_copy


class GenericMeta(TypingMeta, abc.ABCMeta):
    __doc__ = 'Metaclass for generic types.\n\n    This is a metaclass for typing.Generic and generic ABCs defined in\n    typing module. User defined subclasses of GenericMeta can override\n    __new__ and invoke super().__new__. Note that GenericMeta.__new__\n    has strict rules on what is allowed in its bases argument:\n    * plain Generic is disallowed in bases;\n    * Generic[...] should appear in bases at most once;\n    * if Generic[...] is present, then it should list all type variables\n      that appear in other bases.\n    In addition, type of all generic bases is erased, e.g., C[int] is\n    stripped to plain C.\n    '

    def __new__(cls, name, bases, namespace, tvars=None, args=None, origin=None, extra=None, orig_bases=None):
        """Create a new generic class. GenericMeta.__new__ accepts
        keyword arguments that are used for internal bookkeeping, therefore
        an override should pass unused keyword arguments to super().
        """
        if tvars is not None:
            assert origin is not None
            assert all(isinstance(t, TypeVar) for t in tvars), tvars
        else:
            if not tvars is None:
                raise AssertionError(tvars)
            elif not args is None:
                raise AssertionError(args)
            else:
                if not origin is None:
                    raise AssertionError(origin)
                else:
                    tvars = _type_vars(bases)
                    gvars = None
                    for base in bases:
                        if base is Generic:
                            raise TypeError('Cannot inherit from plain Generic')
                        if isinstance(base, GenericMeta):
                            if base.__origin__ is Generic:
                                if gvars is not None:
                                    raise TypeError('Cannot inherit from Generic[...] multiple types.')
                            gvars = base.__parameters__

                    if gvars is None:
                        gvars = tvars
                    else:
                        tvarset = set(tvars)
                        gvarset = set(gvars)
                        if not tvarset <= gvarset:
                            raise TypeError('Some type variables (%s) are not listed in Generic[%s]' % (
                             ', '.join(str(t) for t in tvars if t not in gvarset),
                             ', '.join(str(g) for g in gvars)))
                        tvars = gvars
                    initial_bases = bases
                    if extra is not None:
                        if type(extra) is abc.ABCMeta:
                            if extra not in bases:
                                bases = (
                                 extra,) + bases
                    bases = tuple((b._gorg if isinstance(b, GenericMeta) else b) for b in bases)
                    if any(isinstance(b, GenericMeta) and b is not Generic for b in bases):
                        bases = tuple(b for b in bases if b is not Generic)
                    namespace.update({'__origin__':origin,  '__extra__':extra,  '_gorg':None if not origin else origin._gorg})
                    self = super().__new__(cls, name, bases, namespace, _root=True)
                    super(GenericMeta, self).__setattr__('_gorg', self if not origin else origin._gorg)
                    self.__parameters__ = tvars
                    self.__args__ = tuple((... if a is _TypingEllipsis else () if a is _TypingEmpty else a) for a in args) if args else None
                    self.__next_in_mro__ = _next_in_mro(self)
                    if orig_bases is None:
                        self.__orig_bases__ = initial_bases
                    if '__subclasshook__' not in namespace and extra or getattr(self.__subclasshook__, '__name__', '') == '__extrahook__':
                        self.__subclasshook__ = _make_subclasshook(self)
                    if isinstance(extra, abc.ABCMeta):
                        self._abc_registry = extra._abc_registry
                        self._abc_cache = extra._abc_cache
                    elif origin is not None:
                        self._abc_registry = origin._abc_registry
                        self._abc_cache = origin._abc_cache
                if origin:
                    if hasattr(origin, '__qualname__'):
                        self.__qualname__ = origin.__qualname__
            self.__tree_hash__ = hash(self._subs_tree()) if origin else super(GenericMeta, self).__hash__()
            return self

    @property
    def _abc_negative_cache(self):
        if isinstance(self.__extra__, abc.ABCMeta):
            return self.__extra__._abc_negative_cache
        else:
            return self._gorg._abc_generic_negative_cache

    @_abc_negative_cache.setter
    def _abc_negative_cache(self, value):
        if self.__origin__ is None:
            if isinstance(self.__extra__, abc.ABCMeta):
                self.__extra__._abc_negative_cache = value
            else:
                self._abc_generic_negative_cache = value

    @property
    def _abc_negative_cache_version(self):
        if isinstance(self.__extra__, abc.ABCMeta):
            return self.__extra__._abc_negative_cache_version
        else:
            return self._gorg._abc_generic_negative_cache_version

    @_abc_negative_cache_version.setter
    def _abc_negative_cache_version(self, value):
        if self.__origin__ is None:
            if isinstance(self.__extra__, abc.ABCMeta):
                self.__extra__._abc_negative_cache_version = value
            else:
                self._abc_generic_negative_cache_version = value

    def _get_type_vars(self, tvars):
        if self.__origin__:
            if self.__parameters__:
                _get_type_vars(self.__parameters__, tvars)

    def _eval_type(self, globalns, localns):
        ev_origin = self.__origin__._eval_type(globalns, localns) if self.__origin__ else None
        ev_args = tuple(_eval_type(a, globalns, localns) for a in self.__args__) if self.__args__ else None
        if ev_origin == self.__origin__:
            if ev_args == self.__args__:
                return self
        return self.__class__((self.__name__), (self.__bases__),
          (_no_slots_copy(self.__dict__)),
          tvars=(_type_vars(ev_args) if ev_args else None),
          args=ev_args,
          origin=ev_origin,
          extra=(self.__extra__),
          orig_bases=(self.__orig_bases__))

    def __repr__(self):
        if self.__origin__ is None:
            return super().__repr__()
        else:
            return self._tree_repr(self._subs_tree())

    def _tree_repr(self, tree):
        arg_list = []
        for arg in tree[1:]:
            if arg == ():
                arg_list.append('()')
            else:
                if not isinstance(arg, tuple):
                    arg_list.append(_type_repr(arg))
                else:
                    arg_list.append(arg[0]._tree_repr(arg))

        return super().__repr__() + '[%s]' % ', '.join(arg_list)

    def _subs_tree(self, tvars=None, args=None):
        if self.__origin__ is None:
            return self
        else:
            tree_args = _subs_tree(self, tvars, args)
            return (self._gorg,) + tuple(tree_args)

    def __eq__(self, other):
        if not isinstance(other, GenericMeta):
            return NotImplemented
        else:
            if self.__origin__ is None or other.__origin__ is None:
                return self is other
            return self.__tree_hash__ == other.__tree_hash__

    def __hash__(self):
        return self.__tree_hash__

    @_tp_cache
    def __getitem__(self, params):
        if not isinstance(params, tuple):
            params = (
             params,)
        else:
            if not params:
                if self._gorg is not Tuple:
                    raise TypeError('Parameter list to %s[...] cannot be empty' % _qualname(self))
            msg = 'Parameters to generic types must be types.'
            params = tuple(_type_check(p, msg) for p in params)
            if self is Generic:
                if not all(isinstance(p, TypeVar) for p in params):
                    raise TypeError('Parameters to Generic[...] must all be type variables')
                if len(set(params)) != len(params):
                    raise TypeError('Parameters to Generic[...] must all be unique')
                tvars = params
                args = params
            else:
                if self in (Tuple, Callable):
                    tvars = _type_vars(params)
                    args = params
                else:
                    if self is _Protocol:
                        tvars = params
                        args = params
                    else:
                        if self.__origin__ in (Generic, _Protocol):
                            raise TypeError('Cannot subscript already-subscripted %s' % repr(self))
                        else:
                            _check_generic(self, params)
                            tvars = _type_vars(params)
                            args = params
        prepend = (self,) if self.__origin__ is None else ()
        return self.__class__((self.__name__), (prepend + self.__bases__),
          (_no_slots_copy(self.__dict__)),
          tvars=tvars,
          args=args,
          origin=self,
          extra=(self.__extra__),
          orig_bases=(self.__orig_bases__))

    def __subclasscheck__(self, cls):
        if self.__origin__ is not None:
            if sys._getframe(1).f_globals['__name__'] not in ('abc', 'functools'):
                raise TypeError('Parameterized generics cannot be used with class or instance checks')
            return False
        else:
            if self is Generic:
                raise TypeError('Class %r cannot be used with class or instance checks' % self)
            return super().__subclasscheck__(cls)

    def __instancecheck__(self, instance):
        return issubclass(instance.__class__, self)

    def __setattr__(self, attr, value):
        if attr.startswith('__') and attr.endswith('__') or attr.startswith('_abc_') or self._gorg is None:
            super(GenericMeta, self).__setattr__(attr, value)
        else:
            super(GenericMeta, self._gorg).__setattr__(attr, value)


Generic = None

def _generic_new(base_cls, cls, *args, **kwds):
    if cls.__origin__ is None:
        if base_cls.__new__ is object.__new__:
            if cls.__init__ is not object.__init__:
                return base_cls.__new__(cls)
        return (base_cls.__new__)(cls, *args, **kwds)
    else:
        origin = cls._gorg
        if base_cls.__new__ is object.__new__:
            if cls.__init__ is not object.__init__:
                obj = base_cls.__new__(origin)
        else:
            obj = (base_cls.__new__)(origin, *args, **kwds)
        try:
            obj.__orig_class__ = cls
        except AttributeError:
            pass

        (obj.__init__)(*args, **kwds)
        return obj


class Generic(metaclass=GenericMeta):
    __doc__ = 'Abstract base class for generic types.\n\n    A generic type is typically declared by inheriting from\n    this class parameterized with one or more type variables.\n    For example, a generic mapping type might be defined as::\n\n      class Mapping(Generic[KT, VT]):\n          def __getitem__(self, key: KT) -> VT:\n              ...\n          # Etc.\n\n    This class can then be used as follows::\n\n      def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:\n          try:\n              return mapping[key]\n          except KeyError:\n              return default\n    '
    __slots__ = ()

    def __new__(cls, *args, **kwds):
        if cls._gorg is Generic:
            raise TypeError('Type Generic cannot be instantiated; it can be used only as a base class')
        return _generic_new(cls.__next_in_mro__, cls, *args, **kwds)


class _TypingEmpty:
    __doc__ = 'Internal placeholder for () or []. Used by TupleMeta and CallableMeta\n    to allow empty list/tuple in specific places, without allowing them\n    to sneak in where prohibited.\n    '


class _TypingEllipsis:
    __doc__ = 'Internal placeholder for ... (ellipsis).'


class TupleMeta(GenericMeta):
    __doc__ = 'Metaclass for Tuple (internal).'

    @_tp_cache
    def __getitem__(self, parameters):
        if self.__origin__ is not None or self._gorg is not Tuple:
            return super().__getitem__(parameters)
        else:
            if parameters == ():
                return super().__getitem__((_TypingEmpty,))
            else:
                if not isinstance(parameters, tuple):
                    parameters = (
                     parameters,)
                if len(parameters) == 2:
                    if parameters[1] is ...:
                        msg = 'Tuple[t, ...]: t must be a type.'
                        p = _type_check(parameters[0], msg)
                        return super().__getitem__((p, _TypingEllipsis))
            msg = 'Tuple[t0, t1, ...]: each t must be a type.'
            parameters = tuple(_type_check(p, msg) for p in parameters)
            return super().__getitem__(parameters)

    def __instancecheck__(self, obj):
        if self.__args__ is None:
            return isinstance(obj, tuple)
        raise TypeError('Parameterized Tuple cannot be used with isinstance().')

    def __subclasscheck__(self, cls):
        if self.__args__ is None:
            return issubclass(cls, tuple)
        raise TypeError('Parameterized Tuple cannot be used with issubclass().')


class Tuple(tuple, extra=tuple, metaclass=TupleMeta):
    __doc__ = 'Tuple type; Tuple[X, Y] is the cross-product type of X and Y.\n\n    Example: Tuple[T1, T2] is a tuple of two elements corresponding\n    to type variables T1 and T2.  Tuple[int, float, str] is a tuple\n    of an int, a float and a string.\n\n    To specify a variable-length tuple of homogeneous type, use Tuple[T, ...].\n    '
    __slots__ = ()

    def __new__(cls, *args, **kwds):
        if cls._gorg is Tuple:
            raise TypeError('Type Tuple cannot be instantiated; use tuple() instead')
        return _generic_new(tuple, cls, *args, **kwds)


class CallableMeta(GenericMeta):
    __doc__ = 'Metaclass for Callable (internal).'

    def __repr__(self):
        if self.__origin__ is None:
            return super().__repr__()
        else:
            return self._tree_repr(self._subs_tree())

    def _tree_repr(self, tree):
        if self._gorg is not Callable:
            return super()._tree_repr(tree)
        else:
            arg_list = []
            for arg in tree[1:]:
                if not isinstance(arg, tuple):
                    arg_list.append(_type_repr(arg))
                else:
                    arg_list.append(arg[0]._tree_repr(arg))

            if arg_list[0] == '...':
                return repr(tree[0]) + '[..., %s]' % arg_list[1]
            return repr(tree[0]) + '[[%s], %s]' % (', '.join(arg_list[:-1]), arg_list[(-1)])

    def __getitem__(self, parameters):
        if self.__origin__ is not None or self._gorg is not Callable:
            return super().__getitem__(parameters)
        else:
            if not isinstance(parameters, tuple) or len(parameters) != 2:
                raise TypeError('Callable must be used as Callable[[arg, ...], result].')
            args, result = parameters
            if args is Ellipsis:
                parameters = (
                 Ellipsis, result)
            else:
                if not isinstance(args, list):
                    raise TypeError('Callable[args, result]: args must be a list. Got %.100r.' % (
                     args,))
                parameters = (
                 tuple(args), result)
            return self.__getitem_inner__(parameters)

    @_tp_cache
    def __getitem_inner__(self, parameters):
        args, result = parameters
        msg = 'Callable[args, result]: result must be a type.'
        result = _type_check(result, msg)
        if args is Ellipsis:
            return super().__getitem__((_TypingEllipsis, result))
        else:
            msg = 'Callable[[arg, ...], result]: each arg must be a type.'
            args = tuple(_type_check(arg, msg) for arg in args)
            parameters = args + (result,)
            return super().__getitem__(parameters)


class Callable(extra=collections_abc.Callable, metaclass=CallableMeta):
    __doc__ = 'Callable type; Callable[[int], str] is a function of (int) -> str.\n\n    The subscription syntax must always be used with exactly two\n    values: the argument list and the return type.  The argument list\n    must be a list of types or ellipsis; the return type must be a single type.\n\n    There is no syntax to indicate optional or keyword arguments,\n    such function types are rarely used as callback types.\n    '
    __slots__ = ()

    def __new__(cls, *args, **kwds):
        if cls._gorg is Callable:
            raise TypeError('Type Callable cannot be instantiated; use a non-abstract subclass instead')
        return _generic_new(cls.__next_in_mro__, cls, *args, **kwds)


class _ClassVar(_FinalTypingBase, _root=True):
    __doc__ = 'Special type construct to mark class variables.\n\n    An annotation wrapped in ClassVar indicates that a given\n    attribute is intended to be used as a class variable and\n    should not be set on instances of that class. Usage::\n\n      class Starship:\n          stats: ClassVar[Dict[str, int]] = {} # class variable\n          damage: int = 10                     # instance variable\n\n    ClassVar accepts only types and cannot be further subscribed.\n\n    Note that ClassVar is not a class itself, and should not\n    be used with isinstance() or issubclass().\n    '
    __slots__ = ('__type__', )

    def __init__(self, tp=None, **kwds):
        self.__type__ = tp

    def __getitem__(self, item):
        cls = type(self)
        if self.__type__ is None:
            return cls((_type_check(item, '{} accepts only single type.'.format(cls.__name__[1:]))),
              _root=True)
        raise TypeError('{} cannot be further subscripted'.format(cls.__name__[1:]))

    def _eval_type(self, globalns, localns):
        new_tp = _eval_type(self.__type__, globalns, localns)
        if new_tp == self.__type__:
            return self
        else:
            return type(self)(new_tp, _root=True)

    def __repr__(self):
        r = super().__repr__()
        if self.__type__ is not None:
            r += '[{}]'.format(_type_repr(self.__type__))
        return r

    def __hash__(self):
        return hash((type(self).__name__, self.__type__))

    def __eq__(self, other):
        if not isinstance(other, _ClassVar):
            return NotImplemented
        else:
            if self.__type__ is not None:
                return self.__type__ == other.__type__
            return self is other


ClassVar = _ClassVar(_root=True)

def cast(typ, val):
    """Cast a value to a type.

    This returns the value unchanged.  To the type checker this
    signals that the return value has the designated type, but at
    runtime we intentionally don't check anything (we want this
    to be as fast as possible).
    """
    return val


def _get_defaults(func):
    """Internal helper to extract the default arguments, by name."""
    try:
        code = func.__code__
    except AttributeError:
        return {}
    else:
        pos_count = code.co_argcount
        arg_names = code.co_varnames
        arg_names = arg_names[:pos_count]
        defaults = func.__defaults__ or ()
        kwdefaults = func.__kwdefaults__
        res = dict(kwdefaults) if kwdefaults else {}
        pos_offset = pos_count - len(defaults)
        for name, value in zip(arg_names[pos_offset:], defaults):
            assert name not in res
            res[name] = value

        return res


_allowed_types = (
 types.FunctionType, types.BuiltinFunctionType,
 types.MethodType, types.ModuleType,
 WrapperDescriptorType, MethodWrapperType, MethodDescriptorType)

def get_type_hints(obj, globalns=None, localns=None):
    """Return type hints for an object.

    This is often the same as obj.__annotations__, but it handles
    forward references encoded as string literals, and if necessary
    adds Optional[t] if a default value equal to None is set.

    The argument may be a module, class, method, or function. The annotations
    are returned as a dictionary. For classes, annotations include also
    inherited members.

    TypeError is raised if the argument is not of a type that can contain
    annotations, and an empty dictionary is returned if no annotations are
    present.

    BEWARE -- the behavior of globalns and localns is counterintuitive
    (unless you are familiar with how eval() and exec() work).  The
    search order is locals first, then globals.

    - If no dict arguments are passed, an attempt is made to use the
      globals from obj (or the respective module's globals for classes),
      and these are also used as the locals.  If the object does not appear
      to have globals, an empty dictionary is used.

    - If one dict argument is passed, it is used for both globals and
      locals.

    - If two dict arguments are passed, they specify globals and
      locals, respectively.
    """
    if getattr(obj, '__no_type_check__', None):
        return {}
    else:
        if isinstance(obj, type):
            hints = {}
            for base in reversed(obj.__mro__):
                if globalns is None:
                    base_globals = sys.modules[base.__module__].__dict__
                else:
                    base_globals = globalns
                ann = base.__dict__.get('__annotations__', {})
                for name, value in ann.items():
                    if value is None:
                        value = type(None)
                    if isinstance(value, str):
                        value = _ForwardRef(value)
                    value = _eval_type(value, base_globals, localns)
                    hints[name] = value

            return hints
        else:
            if globalns is None:
                if isinstance(obj, types.ModuleType):
                    globalns = obj.__dict__
                else:
                    globalns = getattr(obj, '__globals__', {})
                if localns is None:
                    localns = globalns
            else:
                if localns is None:
                    localns = globalns
            hints = getattr(obj, '__annotations__', None)
            if hints is None:
                if isinstance(obj, _allowed_types):
                    return {}
                raise TypeError('{!r} is not a module, class, method, or function.'.format(obj))
        defaults = _get_defaults(obj)
        hints = dict(hints)
        for name, value in hints.items():
            if value is None:
                value = type(None)
            else:
                if isinstance(value, str):
                    value = _ForwardRef(value)
                value = _eval_type(value, globalns, localns)
                if name in defaults:
                    if defaults[name] is None:
                        value = Optional[value]
            hints[name] = value

        return hints


def no_type_check(arg):
    """Decorator to indicate that annotations are not type hints.

    The argument must be a class or function; if it is a class, it
    applies recursively to all methods and classes defined in that class
    (but not to methods defined in its superclasses or subclasses).

    This mutates the function(s) or class(es) in place.
    """
    if isinstance(arg, type):
        arg_attrs = arg.__dict__.copy()
        for attr, val in arg.__dict__.items():
            if val in arg.__bases__ + (arg,):
                arg_attrs.pop(attr)

        for obj in arg_attrs.values():
            if isinstance(obj, types.FunctionType):
                obj.__no_type_check__ = True
            if isinstance(obj, type):
                no_type_check(obj)

    try:
        arg.__no_type_check__ = True
    except TypeError:
        pass

    return arg


def no_type_check_decorator(decorator):
    """Decorator to give another decorator the @no_type_check effect.

    This wraps the decorator with something that wraps the decorated
    function in @no_type_check.
    """

    @functools.wraps(decorator)
    def wrapped_decorator(*args, **kwds):
        func = decorator(*args, **kwds)
        func = no_type_check(func)
        return func

    return wrapped_decorator


def _overload_dummy(*args, **kwds):
    """Helper for @overload to raise when called."""
    raise NotImplementedError('You should not call an overloaded function. A series of @overload-decorated functions outside a stub module should always be followed by an implementation that is not @overload-ed.')


def overload(func):
    """Decorator for overloaded functions/methods.

    In a stub file, place two or more stub definitions for the same
    function in a row, each decorated with @overload.  For example:

      @overload
      def utf8(value: None) -> None: ...
      @overload
      def utf8(value: bytes) -> bytes: ...
      @overload
      def utf8(value: str) -> bytes: ...

    In a non-stub file (i.e. a regular .py file), do the same but
    follow it with an implementation.  The implementation should *not*
    be decorated with @overload.  For example:

      @overload
      def utf8(value: None) -> None: ...
      @overload
      def utf8(value: bytes) -> bytes: ...
      @overload
      def utf8(value: str) -> bytes: ...
      def utf8(value):
          # implementation goes here
    """
    return _overload_dummy


class _ProtocolMeta(GenericMeta):
    __doc__ = 'Internal metaclass for _Protocol.\n\n    This exists so _Protocol classes can be generic without deriving\n    from Generic.\n    '

    def __instancecheck__(self, obj):
        if _Protocol not in self.__bases__:
            return super().__instancecheck__(obj)
        raise TypeError('Protocols cannot be used with isinstance().')

    def __subclasscheck__(self, cls):
        if not self._is_protocol:
            return NotImplemented
        else:
            if self is _Protocol:
                return True
            attrs = self._get_protocol_attrs()
            for attr in attrs:
                if not any(attr in d.__dict__ for d in cls.__mro__):
                    return False

            return True

    def _get_protocol_attrs(self):
        protocol_bases = []
        for c in self.__mro__:
            if getattr(c, '_is_protocol', False) and c.__name__ != '_Protocol':
                protocol_bases.append(c)

        attrs = set()
        for base in protocol_bases:
            for attr in base.__dict__.keys():
                for c in self.__mro__:
                    if c is not base:
                        if attr in c.__dict__:
                            if not getattr(c, '_is_protocol', False):
                                break
                else:
                    if not attr.startswith('_abc_') and attr != '__abstractmethods__' and attr != '__annotations__' and attr != '__weakref__' and attr != '_is_protocol' and attr != '_gorg' and attr != '__dict__' and attr != '__args__' and attr != '__slots__' and attr != '_get_protocol_attrs' and attr != '__next_in_mro__' and attr != '__parameters__' and attr != '__origin__' and attr != '__orig_bases__' and attr != '__extra__' and attr != '__tree_hash__' and attr != '__module__':
                        attrs.add(attr)

        return attrs


class _Protocol(metaclass=_ProtocolMeta):
    __doc__ = 'Internal base class for protocol classes.\n\n    This implements a simple-minded structural issubclass check\n    (similar but more general than the one-offs in collections.abc\n    such as Hashable).\n    '
    __slots__ = ()
    _is_protocol = True


Hashable = collections_abc.Hashable
if hasattr(collections_abc, 'Awaitable'):

    class Awaitable(Generic[T_co], extra=collections_abc.Awaitable):
        __slots__ = ()


    __all__.append('Awaitable')
if hasattr(collections_abc, 'Coroutine'):

    class Coroutine(Awaitable[V_co], Generic[(T_co, T_contra, V_co)], extra=collections_abc.Coroutine):
        __slots__ = ()


    __all__.append('Coroutine')
else:
    if hasattr(collections_abc, 'AsyncIterable'):

        class AsyncIterable(Generic[T_co], extra=collections_abc.AsyncIterable):
            __slots__ = ()


        class AsyncIterator(AsyncIterable[T_co], extra=collections_abc.AsyncIterator):
            __slots__ = ()


        __all__.append('AsyncIterable')
        __all__.append('AsyncIterator')

    class Iterable(Generic[T_co], extra=collections_abc.Iterable):
        __slots__ = ()


    class Iterator(Iterable[T_co], extra=collections_abc.Iterator):
        __slots__ = ()


    class SupportsInt(_Protocol):
        __slots__ = ()

        @abstractmethod
        def __int__(self) -> int:
            pass


    class SupportsFloat(_Protocol):
        __slots__ = ()

        @abstractmethod
        def __float__(self) -> float:
            pass


    class SupportsComplex(_Protocol):
        __slots__ = ()

        @abstractmethod
        def __complex__(self) -> complex:
            pass


    class SupportsBytes(_Protocol):
        __slots__ = ()

        @abstractmethod
        def __bytes__(self) -> bytes:
            pass


    class SupportsAbs(_Protocol[T_co]):
        __slots__ = ()

        @abstractmethod
        def __abs__(self) -> T_co:
            pass


    class SupportsRound(_Protocol[T_co]):
        __slots__ = ()

        @abstractmethod
        def __round__(self, ndigits: int=0) -> T_co:
            pass


    if hasattr(collections_abc, 'Reversible'):

        class Reversible(Iterable[T_co], extra=collections_abc.Reversible):
            __slots__ = ()


    else:

        class Reversible(_Protocol[T_co]):
            __slots__ = ()

            @abstractmethod
            def __reversed__(self) -> 'Iterator[T_co]':
                pass


Sized = collections_abc.Sized

class Container(Generic[T_co], extra=collections_abc.Container):
    __slots__ = ()


if hasattr(collections_abc, 'Collection'):

    class Collection(Sized, Iterable[T_co], Container[T_co], extra=collections_abc.Collection):
        __slots__ = ()


    __all__.append('Collection')
else:
    if hasattr(collections_abc, 'Collection'):

        class AbstractSet(Collection[T_co], extra=collections_abc.Set):
            __slots__ = ()


    else:

        class AbstractSet(Sized, Iterable[T_co], Container[T_co], extra=collections_abc.Set):
            __slots__ = ()


    class MutableSet(AbstractSet[T], extra=collections_abc.MutableSet):
        __slots__ = ()


    if hasattr(collections_abc, 'Collection'):

        class Mapping(Collection[KT], Generic[(KT, VT_co)], extra=collections_abc.Mapping):
            __slots__ = ()


    else:

        class Mapping(Sized, Iterable[KT], Container[KT], Generic[(KT, VT_co)], extra=collections_abc.Mapping):
            __slots__ = ()


    class MutableMapping(Mapping[(KT, VT)], extra=collections_abc.MutableMapping):
        __slots__ = ()


    if hasattr(collections_abc, 'Reversible'):
        if hasattr(collections_abc, 'Collection'):

            class Sequence(Reversible[T_co], Collection[T_co], extra=collections_abc.Sequence):
                __slots__ = ()


        else:

            class Sequence(Sized, Reversible[T_co], Container[T_co], extra=collections_abc.Sequence):
                __slots__ = ()


    else:

        class Sequence(Sized, Iterable[T_co], Container[T_co], extra=collections_abc.Sequence):
            __slots__ = ()


    class MutableSequence(Sequence[T], extra=collections_abc.MutableSequence):
        __slots__ = ()


    class ByteString(Sequence[int], extra=collections_abc.ByteString):
        __slots__ = ()


    class List(list, MutableSequence[T], extra=list):
        __slots__ = ()

        def __new__(cls, *args, **kwds):
            if cls._gorg is List:
                raise TypeError('Type List cannot be instantiated; use list() instead')
            return _generic_new(list, cls, *args, **kwds)


    class Deque(collections.deque, MutableSequence[T], extra=collections.deque):
        __slots__ = ()

        def __new__(cls, *args, **kwds):
            if cls._gorg is Deque:
                return (collections.deque)(*args, **kwds)
            else:
                return _generic_new(collections.deque, cls, *args, **kwds)


    class Set(set, MutableSet[T], extra=set):
        __slots__ = ()

        def __new__(cls, *args, **kwds):
            if cls._gorg is Set:
                raise TypeError('Type Set cannot be instantiated; use set() instead')
            return _generic_new(set, cls, *args, **kwds)


    class FrozenSet(frozenset, AbstractSet[T_co], extra=frozenset):
        __slots__ = ()

        def __new__(cls, *args, **kwds):
            if cls._gorg is FrozenSet:
                raise TypeError('Type FrozenSet cannot be instantiated; use frozenset() instead')
            return _generic_new(frozenset, cls, *args, **kwds)


    class MappingView(Sized, Iterable[T_co], extra=collections_abc.MappingView):
        __slots__ = ()


    class KeysView(MappingView[KT], AbstractSet[KT], extra=collections_abc.KeysView):
        __slots__ = ()


    class ItemsView(MappingView[Tuple[(KT, VT_co)]], AbstractSet[Tuple[(KT, VT_co)]], Generic[(KT, VT_co)], extra=collections_abc.ItemsView):
        __slots__ = ()


    class ValuesView(MappingView[VT_co], extra=collections_abc.ValuesView):
        __slots__ = ()


    if hasattr(contextlib, 'AbstractContextManager'):

        class ContextManager(Generic[T_co], extra=contextlib.AbstractContextManager):
            __slots__ = ()


    else:

        class ContextManager(Generic[T_co]):
            __slots__ = ()

            def __enter__(self):
                return self

            @abc.abstractmethod
            def __exit__(self, exc_type, exc_value, traceback):
                pass

            @classmethod
            def __subclasshook__(cls, C):
                if cls is ContextManager:
                    if any('__enter__' in B.__dict__ for B in C.__mro__):
                        if any('__exit__' in B.__dict__ for B in C.__mro__):
                            return True
                return NotImplemented


    if hasattr(contextlib, 'AbstractAsyncContextManager'):

        class AsyncContextManager(Generic[T_co], extra=contextlib.AbstractAsyncContextManager):
            __slots__ = ()


        __all__.append('AsyncContextManager')
    else:
        if sys.version_info[:2] >= (3, 5):
            exec('\nclass AsyncContextManager(Generic[T_co]):\n    __slots__ = ()\n\n    async def __aenter__(self):\n        return self\n\n    @abc.abstractmethod\n    async def __aexit__(self, exc_type, exc_value, traceback):\n        return None\n\n    @classmethod\n    def __subclasshook__(cls, C):\n        if cls is AsyncContextManager:\n            if sys.version_info[:2] >= (3, 6):\n                return _collections_abc._check_methods(C, "__aenter__", "__aexit__")\n            if (any("__aenter__" in B.__dict__ for B in C.__mro__) and\n                    any("__aexit__" in B.__dict__ for B in C.__mro__)):\n                return True\n        return NotImplemented\n\n__all__.append(\'AsyncContextManager\')\n')

    class Dict(dict, MutableMapping[(KT, VT)], extra=dict):
        __slots__ = ()

        def __new__(cls, *args, **kwds):
            if cls._gorg is Dict:
                raise TypeError('Type Dict cannot be instantiated; use dict() instead')
            return _generic_new(dict, cls, *args, **kwds)


    class DefaultDict(collections.defaultdict, MutableMapping[(KT, VT)], extra=collections.defaultdict):
        __slots__ = ()

        def __new__(cls, *args, **kwds):
            if cls._gorg is DefaultDict:
                return (collections.defaultdict)(*args, **kwds)
            else:
                return _generic_new(collections.defaultdict, cls, *args, **kwds)


    class Counter(collections.Counter, Dict[(T, int)], extra=collections.Counter):
        __slots__ = ()

        def __new__(cls, *args, **kwds):
            if cls._gorg is Counter:
                return (collections.Counter)(*args, **kwds)
            else:
                return _generic_new(collections.Counter, cls, *args, **kwds)


    if hasattr(collections, 'ChainMap'):
        __all__.append('ChainMap')

        class ChainMap(collections.ChainMap, MutableMapping[(KT, VT)], extra=collections.ChainMap):
            __slots__ = ()

            def __new__(cls, *args, **kwds):
                if cls._gorg is ChainMap:
                    return (collections.ChainMap)(*args, **kwds)
                else:
                    return _generic_new(collections.ChainMap, cls, *args, **kwds)


    if hasattr(collections_abc, 'Generator'):
        _G_base = collections_abc.Generator
    else:
        _G_base = types.GeneratorType

class Generator(Iterator[T_co], Generic[(T_co, T_contra, V_co)], extra=_G_base):
    __slots__ = ()

    def __new__(cls, *args, **kwds):
        if cls._gorg is Generator:
            raise TypeError('Type Generator cannot be instantiated; create a subclass instead')
        return _generic_new(_G_base, cls, *args, **kwds)


if hasattr(collections_abc, 'AsyncGenerator'):

    class AsyncGenerator(AsyncIterator[T_co], Generic[(T_co, T_contra)], extra=collections_abc.AsyncGenerator):
        __slots__ = ()


    __all__.append('AsyncGenerator')
CT_co = TypeVar('CT_co', covariant=True, bound=type)

class Type(Generic[CT_co], extra=type):
    __doc__ = "A special construct usable to annotate class objects.\n\n    For example, suppose we have the following classes::\n\n      class User: ...  # Abstract base for User classes\n      class BasicUser(User): ...\n      class ProUser(User): ...\n      class TeamUser(User): ...\n\n    And a function that takes a class argument that's a subclass of\n    User and returns an instance of the corresponding class::\n\n      U = TypeVar('U', bound=User)\n      def new_user(user_class: Type[U]) -> U:\n          user = user_class()\n          # (Here we could write the user object to a database)\n          return user\n\n      joe = new_user(BasicUser)\n\n    At this point the type checker knows that joe has type BasicUser.\n    "
    __slots__ = ()


def _make_nmtuple(name, types):
    msg = "NamedTuple('Name', [(f0, t0), (f1, t1), ...]); each t must be a type"
    types = [(n, _type_check(t, msg)) for n, t in types]
    nm_tpl = collections.namedtuple(name, [n for n, t in types])
    nm_tpl.__annotations__ = nm_tpl._field_types = collections.OrderedDict(types)
    try:
        nm_tpl.__module__ = sys._getframe(2).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass

    return nm_tpl


_PY36 = sys.version_info[:2] >= (3, 6)
_prohibited = ('__new__', '__init__', '__slots__', '__getnewargs__', '_fields', '_field_defaults',
               '_field_types', '_make', '_replace', '_asdict', '_source')
_special = ('__module__', '__name__', '__qualname__', '__annotations__')

class NamedTupleMeta(type):

    def __new__(cls, typename, bases, ns):
        if ns.get('_root', False):
            return super().__new__(cls, typename, bases, ns)
        else:
            if not _PY36:
                raise TypeError('Class syntax for NamedTuple is only supported in Python 3.6+')
            types = ns.get('__annotations__', {})
            nm_tpl = _make_nmtuple(typename, types.items())
            defaults = []
            defaults_dict = {}
            for field_name in types:
                if field_name in ns:
                    default_value = ns[field_name]
                    defaults.append(default_value)
                    defaults_dict[field_name] = default_value
                else:
                    if defaults:
                        raise TypeError('Non-default namedtuple field {field_name} cannot follow default field(s) {default_names}'.format(field_name=field_name,
                          default_names=(', '.join(defaults_dict.keys()))))

            nm_tpl.__new__.__annotations__ = collections.OrderedDict(types)
            nm_tpl.__new__.__defaults__ = tuple(defaults)
            nm_tpl._field_defaults = defaults_dict
            for key in ns:
                if key in _prohibited:
                    raise AttributeError('Cannot overwrite NamedTuple attribute ' + key)
                else:
                    if key not in _special and key not in nm_tpl._fields:
                        setattr(nm_tpl, key, ns[key])

            return nm_tpl


class NamedTuple(metaclass=NamedTupleMeta):
    __doc__ = "Typed version of namedtuple.\n\n    Usage in Python versions >= 3.6::\n\n        class Employee(NamedTuple):\n            name: str\n            id: int\n\n    This is equivalent to::\n\n        Employee = collections.namedtuple('Employee', ['name', 'id'])\n\n    The resulting class has extra __annotations__ and _field_types\n    attributes, giving an ordered dict mapping field names to types.\n    __annotations__ should be preferred, while _field_types\n    is kept to maintain pre PEP 526 compatibility. (The field names\n    are in the _fields attribute, which is part of the namedtuple\n    API.) Alternative equivalent keyword syntax is also accepted::\n\n        Employee = NamedTuple('Employee', name=str, id=int)\n\n    In Python versions <= 3.5 use::\n\n        Employee = NamedTuple('Employee', [('name', str), ('id', int)])\n    "
    _root = True

    def __new__(self, typename, fields=None, **kwargs):
        if kwargs:
            if not _PY36:
                raise TypeError('Keyword syntax for NamedTuple is only supported in Python 3.6+')
        if fields is None:
            fields = kwargs.items()
        else:
            if kwargs:
                raise TypeError('Either list of fields or keywords can be provided to NamedTuple, not both')
        return _make_nmtuple(typename, fields)


def NewType(name, tp):
    """NewType creates simple unique types with almost zero
    runtime overhead. NewType(name, tp) is considered a subtype of tp
    by static type checkers. At runtime, NewType(name, tp) returns
    a dummy function that simply returns its argument. Usage::

        UserId = NewType('UserId', int)

        def name_by_id(user_id: UserId) -> str:
            ...

        UserId('user')          # Fails type check

        name_by_id(42)          # Fails type check
        name_by_id(UserId(42))  # OK

        num = UserId(5) + 1     # type: int
    """

    def new_type(x):
        return x

    new_type.__name__ = name
    new_type.__supertype__ = tp
    return new_type


Text = str
TYPE_CHECKING = False

class IO(Generic[AnyStr]):
    __doc__ = 'Generic base class for TextIO and BinaryIO.\n\n    This is an abstract, generic version of the return of open().\n\n    NOTE: This does not distinguish between the different possible\n    classes (text vs. binary, read vs. write vs. read/write,\n    append-only, unbuffered).  The TextIO and BinaryIO subclasses\n    below capture the distinctions between text vs. binary, which is\n    pervasive in the interface; however we currently do not offer a\n    way to track the other distinctions in the type system.\n    '
    __slots__ = ()

    @abstractproperty
    def mode(self) -> str:
        pass

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def closed(self) -> bool:
        pass

    @abstractmethod
    def fileno(self) -> int:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass

    @abstractmethod
    def isatty(self) -> bool:
        pass

    @abstractmethod
    def read(self, n: int=-1) -> AnyStr:
        pass

    @abstractmethod
    def readable(self) -> bool:
        pass

    @abstractmethod
    def readline(self, limit: int=-1) -> AnyStr:
        pass

    @abstractmethod
    def readlines(self, hint: int=-1) -> List[AnyStr]:
        pass

    @abstractmethod
    def seek(self, offset: int, whence: int=0) -> int:
        pass

    @abstractmethod
    def seekable(self) -> bool:
        pass

    @abstractmethod
    def tell(self) -> int:
        pass

    @abstractmethod
    def truncate(self, size: int=None) -> int:
        pass

    @abstractmethod
    def writable(self) -> bool:
        pass

    @abstractmethod
    def write(self, s: AnyStr) -> int:
        pass

    @abstractmethod
    def writelines(self, lines: List[AnyStr]) -> None:
        pass

    @abstractmethod
    def __enter__(self) -> 'IO[AnyStr]':
        pass

    @abstractmethod
    def __exit__(self, type, value, traceback) -> None:
        pass


class BinaryIO(IO[bytes]):
    __doc__ = 'Typed version of the return of open() in binary mode.'
    __slots__ = ()

    @abstractmethod
    def write(self, s: Union[(bytes, bytearray)]) -> int:
        pass

    @abstractmethod
    def __enter__(self) -> 'BinaryIO':
        pass


class TextIO(IO[str]):
    __doc__ = 'Typed version of the return of open() in text mode.'
    __slots__ = ()

    @abstractproperty
    def buffer(self) -> BinaryIO:
        pass

    @abstractproperty
    def encoding(self) -> str:
        pass

    @abstractproperty
    def errors(self) -> Optional[str]:
        pass

    @abstractproperty
    def line_buffering(self) -> bool:
        pass

    @abstractproperty
    def newlines(self) -> Any:
        pass

    @abstractmethod
    def __enter__(self) -> 'TextIO':
        pass


class io:
    __doc__ = 'Wrapper namespace for IO generic classes.'
    __all__ = [
     'IO', 'TextIO', 'BinaryIO']
    IO = IO
    TextIO = TextIO
    BinaryIO = BinaryIO


io.__name__ = __name__ + '.io'
sys.modules[io.__name__] = io
Pattern = _TypeAlias('Pattern', AnyStr, type(stdlib_re.compile('')), lambda p: p.pattern)
Match = _TypeAlias('Match', AnyStr, type(stdlib_re.match('', '')), lambda m: m.re.pattern)

class re:
    __doc__ = 'Wrapper namespace for re type aliases.'
    __all__ = [
     'Pattern', 'Match']
    Pattern = Pattern
    Match = Match


re.__name__ = __name__ + '.re'
sys.modules[re.__name__] = re