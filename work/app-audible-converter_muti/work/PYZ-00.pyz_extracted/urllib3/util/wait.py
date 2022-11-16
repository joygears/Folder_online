# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\util\wait.py
import errno, select, sys
from functools import partial
try:
    from time import monotonic
except ImportError:
    from time import time as monotonic

__all__ = [
 'NoWayToWaitForSocketError', 'wait_for_read', 'wait_for_write']

class NoWayToWaitForSocketError(Exception):
    pass


if sys.version_info >= (3, 5):

    def _retry_on_intr(fn, timeout):
        return fn(timeout)


else:

    def _retry_on_intr(fn, timeout):
        if timeout is None:
            deadline = float('inf')
        else:
            deadline = monotonic() + timeout
        while True:
            try:
                return fn(timeout)
            except (OSError, select.error) as e:
                if e.args[0] != errno.EINTR:
                    raise
                else:
                    timeout = deadline - monotonic()
                    if timeout < 0:
                        timeout = 0
                    if timeout == float('inf'):
                        timeout = None
                    continue


def select_wait_for_socket(sock, read=False, write=False, timeout=None):
    if not read:
        if not write:
            raise RuntimeError('must specify at least one of read=True, write=True')
    else:
        rcheck = []
        wcheck = []
        if read:
            rcheck.append(sock)
        if write:
            wcheck.append(sock)
    fn = partial(select.select, rcheck, wcheck, wcheck)
    rready, wready, xready = _retry_on_intr(fn, timeout)
    return bool(rready or wready or xready)


def poll_wait_for_socket(sock, read=False, write=False, timeout=None):
    if not read:
        if not write:
            raise RuntimeError('must specify at least one of read=True, write=True')
    else:
        mask = 0
        if read:
            mask |= select.POLLIN
        if write:
            mask |= select.POLLOUT
    poll_obj = select.poll()
    poll_obj.register(sock, mask)

    def do_poll(t):
        if t is not None:
            t *= 1000
        return poll_obj.poll(t)

    return bool(_retry_on_intr(do_poll, timeout))


def null_wait_for_socket(*args, **kwargs):
    raise NoWayToWaitForSocketError('no select-equivalent available')


def _have_working_poll():
    try:
        poll_obj = select.poll()
        _retry_on_intr(poll_obj.poll, 0)
    except (AttributeError, OSError):
        return False
    else:
        return True


def wait_for_socket(*args, **kwargs):
    global wait_for_socket
    if _have_working_poll():
        wait_for_socket = poll_wait_for_socket
    else:
        if hasattr(select, 'select'):
            wait_for_socket = select_wait_for_socket
        else:
            wait_for_socket = null_wait_for_socket
    return wait_for_socket(*args, **kwargs)


def wait_for_read(sock, timeout=None):
    """Waits for reading to be available on a given socket.
    Returns True if the socket is readable, or False if the timeout expired.
    """
    return wait_for_socket(sock, read=True, timeout=timeout)


def wait_for_write(sock, timeout=None):
    """Waits for writing to be available on a given socket.
    Returns True if the socket is readable, or False if the timeout expired.
    """
    return wait_for_socket(sock, write=True, timeout=timeout)