# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\_collections.py
from __future__ import absolute_import
try:
    from collections.abc import Mapping, MutableMapping
except ImportError:
    from collections import Mapping, MutableMapping

try:
    from threading import RLock
except ImportError:

    class RLock:

        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_value, traceback):
            pass


from collections import OrderedDict
from .exceptions import InvalidHeader
from .packages import six
from .packages.six import iterkeys, itervalues
__all__ = [
 'RecentlyUsedContainer', 'HTTPHeaderDict']
_Null = object()

class RecentlyUsedContainer(MutableMapping):
    __doc__ = '\n    Provides a thread-safe dict-like container which maintains up to\n    ``maxsize`` keys while throwing away the least-recently-used keys beyond\n    ``maxsize``.\n\n    :param maxsize:\n        Maximum number of recent elements to retain.\n\n    :param dispose_func:\n        Every time an item is evicted from the container,\n        ``dispose_func(value)`` is called.  Callback which will get called\n    '
    ContainerCls = OrderedDict

    def __init__(self, maxsize=10, dispose_func=None):
        self._maxsize = maxsize
        self.dispose_func = dispose_func
        self._container = self.ContainerCls()
        self.lock = RLock()

    def __getitem__(self, key):
        with self.lock:
            item = self._container.pop(key)
            self._container[key] = item
            return item

    def __setitem__(self, key, value):
        evicted_value = _Null
        with self.lock:
            evicted_value = self._container.get(key, _Null)
            self._container[key] = value
            if len(self._container) > self._maxsize:
                _key, evicted_value = self._container.popitem(last=False)
        if self.dispose_func:
            if evicted_value is not _Null:
                self.dispose_func(evicted_value)

    def __delitem__(self, key):
        with self.lock:
            value = self._container.pop(key)
        if self.dispose_func:
            self.dispose_func(value)

    def __len__(self):
        with self.lock:
            return len(self._container)

    def __iter__(self):
        raise NotImplementedError('Iteration over this class is unlikely to be threadsafe.')

    def clear(self):
        with self.lock:
            values = list(itervalues(self._container))
            self._container.clear()
        if self.dispose_func:
            for value in values:
                self.dispose_func(value)

    def keys(self):
        with self.lock:
            return list(iterkeys(self._container))


class HTTPHeaderDict(MutableMapping):
    __doc__ = "\n    :param headers:\n        An iterable of field-value pairs. Must not contain multiple field names\n        when compared case-insensitively.\n\n    :param kwargs:\n        Additional field-value pairs to pass in to ``dict.update``.\n\n    A ``dict`` like container for storing HTTP Headers.\n\n    Field names are stored and compared case-insensitively in compliance with\n    RFC 7230. Iteration provides the first case-sensitive key seen for each\n    case-insensitive pair.\n\n    Using ``__setitem__`` syntax overwrites fields that compare equal\n    case-insensitively in order to maintain ``dict``'s api. For fields that\n    compare equal, instead create a new ``HTTPHeaderDict`` and use ``.add``\n    in a loop.\n\n    If multiple fields that are equal case-insensitively are passed to the\n    constructor or ``.update``, the behavior is undefined and some will be\n    lost.\n\n    >>> headers = HTTPHeaderDict()\n    >>> headers.add('Set-Cookie', 'foo=bar')\n    >>> headers.add('set-cookie', 'baz=quxx')\n    >>> headers['content-length'] = '7'\n    >>> headers['SET-cookie']\n    'foo=bar, baz=quxx'\n    >>> headers['Content-Length']\n    '7'\n    "

    def __init__(self, headers=None, **kwargs):
        super(HTTPHeaderDict, self).__init__()
        self._container = OrderedDict()
        if headers is not None:
            if isinstance(headers, HTTPHeaderDict):
                self._copy_from(headers)
            else:
                self.extend(headers)
        if kwargs:
            self.extend(kwargs)

    def __setitem__(self, key, val):
        self._container[key.lower()] = [key, val]
        return self._container[key.lower()]

    def __getitem__(self, key):
        val = self._container[key.lower()]
        return ', '.join(val[1:])

    def __delitem__(self, key):
        del self._container[key.lower()]

    def __contains__(self, key):
        return key.lower() in self._container

    def __eq__(self, other):
        if not isinstance(other, Mapping):
            if not hasattr(other, 'keys'):
                return False
        if not isinstance(other, type(self)):
            other = type(self)(other)
        return dict((k.lower(), v) for k, v in self.itermerged()) == dict((k.lower(), v) for k, v in other.itermerged())

    def __ne__(self, other):
        return not self.__eq__(other)

    if six.PY2:
        iterkeys = MutableMapping.iterkeys
        itervalues = MutableMapping.itervalues
    _HTTPHeaderDict__marker = object()

    def __len__(self):
        return len(self._container)

    def __iter__(self):
        for vals in self._container.values():
            yield vals[0]

    def pop(self, key, default=_HTTPHeaderDict__marker):
        """D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised.
        """
        try:
            value = self[key]
        except KeyError:
            if default is self._HTTPHeaderDict__marker:
                raise
            return default
        else:
            del self[key]
            return value

    def discard(self, key):
        try:
            del self[key]
        except KeyError:
            pass

    def add(self, key, val):
        """Adds a (name, value) pair, doesn't overwrite the value if it already
        exists.

        >>> headers = HTTPHeaderDict(foo='bar')
        >>> headers.add('Foo', 'baz')
        >>> headers['foo']
        'bar, baz'
        """
        key_lower = key.lower()
        new_vals = [key, val]
        vals = self._container.setdefault(key_lower, new_vals)
        if new_vals is not vals:
            vals.append(val)

    def extend(self, *args, **kwargs):
        """Generic import function for any type of header-like object.
        Adapted version of MutableMapping.update in order to insert items
        with self.add instead of self.__setitem__
        """
        if len(args) > 1:
            raise TypeError('extend() takes at most 1 positional arguments ({0} given)'.format(len(args)))
        else:
            other = args[0] if len(args) >= 1 else ()
            if isinstance(other, HTTPHeaderDict):
                for key, val in other.iteritems():
                    self.add(key, val)

            else:
                if isinstance(other, Mapping):
                    for key in other:
                        self.add(key, other[key])

                else:
                    if hasattr(other, 'keys'):
                        for key in other.keys():
                            self.add(key, other[key])

                    else:
                        for key, value in other:
                            self.add(key, value)

        for key, value in kwargs.items():
            self.add(key, value)

    def getlist(self, key, default=_HTTPHeaderDict__marker):
        """Returns a list of all the values for the named field. Returns an
        empty list if the key doesn't exist."""
        try:
            vals = self._container[key.lower()]
        except KeyError:
            if default is self._HTTPHeaderDict__marker:
                return []
            return default
        else:
            return vals[1:]

    getheaders = getlist
    getallmatchingheaders = getlist
    iget = getlist
    get_all = getlist

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, dict(self.itermerged()))

    def _copy_from(self, other):
        for key in other:
            val = other.getlist(key)
            if isinstance(val, list):
                val = list(val)
            self._container[key.lower()] = [
             key] + val

    def copy(self):
        clone = type(self)()
        clone._copy_from(self)
        return clone

    def iteritems(self):
        """Iterate over all header lines, including duplicate ones."""
        for key in self:
            vals = self._container[key.lower()]
            for val in vals[1:]:
                yield (
                 vals[0], val)

    def itermerged(self):
        """Iterate over all headers, merging duplicate ones together."""
        for key in self:
            val = self._container[key.lower()]
            yield (val[0], ', '.join(val[1:]))

    def items(self):
        return list(self.iteritems())

    @classmethod
    def from_httplib(cls, message):
        """Read headers from a Python 2 httplib message object."""
        obs_fold_continued_leaders = (' ', '\t')
        headers = []
        for line in message.headers:
            if line.startswith(obs_fold_continued_leaders):
                if not headers:
                    raise InvalidHeader('Header continuation with no previous header: %s' % line)
                else:
                    key, value = headers[(-1)]
                    headers[-1] = (key, value + ' ' + line.strip())
                    continue
            key, value = line.split(':', 1)
            headers.append((key, value.strip()))

        return cls(headers)