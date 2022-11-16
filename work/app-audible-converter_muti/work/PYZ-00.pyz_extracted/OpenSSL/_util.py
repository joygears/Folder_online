# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: OpenSSL\_util.py
import os, sys, warnings
from cryptography.hazmat.bindings.openssl.binding import Binding
binding = Binding()
ffi = binding.ffi
lib = binding.lib
no_zero_allocator = ffi.new_allocator(should_clear_after_alloc=False)

def text(charp):
    """
    Get a native string type representing of the given CFFI ``char*`` object.

    :param charp: A C-style string represented using CFFI.

    :return: :class:`str`
    """
    if not charp:
        return ''
    else:
        return ffi.string(charp).decode('utf-8')


def exception_from_error_queue(exception_type):
    """
    Convert an OpenSSL library failure into a Python exception.

    When a call to the native OpenSSL library fails, this is usually signalled
    by the return value, and an error code is stored in an error queue
    associated with the current thread. The err library provides functions to
    obtain these error codes and textual error messages.
    """
    errors = []
    while True:
        error = lib.ERR_get_error()
        if error == 0:
            break
        errors.append((
         text(lib.ERR_lib_error_string(error)),
         text(lib.ERR_func_error_string(error)),
         text(lib.ERR_reason_error_string(error))))

    raise exception_type(errors)


def make_assert(error):
    """
    Create an assert function that uses :func:`exception_from_error_queue` to
    raise an exception wrapped by *error*.
    """

    def openssl_assert(ok):
        if ok is not True:
            exception_from_error_queue(error)

    return openssl_assert


def path_bytes(s):
    """
    Convert a Python path to a :py:class:`bytes` for the path which can be
    passed into an OpenSSL API accepting a filename.

    :param s: A path (valid for os.fspath).

    :return: An instance of :py:class:`bytes`.
    """
    b = os.fspath(s)
    if isinstance(b, str):
        return b.encode(sys.getfilesystemencoding())
    else:
        return b


def byte_string(s):
    return s.encode('charmap')


UNSPECIFIED = object()
_TEXT_WARNING = 'str for {0} is no longer accepted, use bytes'

def text_to_bytes_and_warn(label, obj):
    """
    If ``obj`` is text, emit a warning that it should be bytes instead and try
    to convert it to bytes automatically.

    :param str label: The name of the parameter from which ``obj`` was taken
        (so a developer can easily find the source of the problem and correct
        it).

    :return: If ``obj`` is the text string type, a ``bytes`` object giving the
        UTF-8 encoding of that text is returned.  Otherwise, ``obj`` itself is
        returned.
    """
    if isinstance(obj, str):
        warnings.warn((_TEXT_WARNING.format(label)),
          category=DeprecationWarning,
          stacklevel=3)
        return obj.encode('utf-8')
    else:
        return obj