# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\util\connection.py
from __future__ import absolute_import
import socket
from ..contrib import _appengine_environ
from ..exceptions import LocationParseError
from ..packages import six
from .wait import NoWayToWaitForSocketError, wait_for_read

def is_connection_dropped(conn):
    """
    Returns True if the connection is dropped and should be closed.

    :param conn:
        :class:`http.client.HTTPConnection` object.

    Note: For platforms like AppEngine, this will always return ``False`` to
    let the platform handle connection recycling transparently for us.
    """
    sock = getattr(conn, 'sock', False)
    if sock is False:
        return False
    if sock is None:
        return True
    try:
        return wait_for_read(sock, timeout=0.0)
    except NoWayToWaitForSocketError:
        return False


def create_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None, socket_options=None):
    """Connect to *address* and return the socket object.

    Convenience function.  Connect to *address* (a 2-tuple ``(host,
    port)``) and return the socket object.  Passing the optional
    *timeout* parameter will set the timeout on the socket instance
    before attempting to connect.  If no *timeout* is supplied, the
    global default timeout setting returned by :func:`socket.getdefaulttimeout`
    is used.  If *source_address* is set it must be a tuple of (host, port)
    for the socket to bind as a source address before making the connection.
    An host of '' or port 0 tells the OS to use the default.
    """
    host, port = address
    if host.startswith('['):
        host = host.strip('[]')
    err = None
    family = allowed_gai_family()
    try:
        host.encode('idna')
    except UnicodeError:
        return six.raise_from(LocationParseError("'%s', label empty or too long" % host), None)
    else:
        for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            sock = None
            try:
                sock = socket.socket(af, socktype, proto)
                _set_socket_options(sock, socket_options)
                if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                    sock.settimeout(timeout)
                if source_address:
                    sock.bind(source_address)
                sock.connect(sa)
                return sock
            except socket.error as e:
                err = e
                if sock is not None:
                    sock.close()
                    sock = None

        if err is not None:
            raise err
        raise socket.error('getaddrinfo returns an empty list')


def _set_socket_options(sock, options):
    if options is None:
        return
    for opt in options:
        (sock.setsockopt)(*opt)


def allowed_gai_family():
    """This function is designed to work in the context of
    getaddrinfo, where family=socket.AF_UNSPEC is the default and
    will perform a DNS search for both IPv6 and IPv4 records."""
    family = socket.AF_INET
    if HAS_IPV6:
        family = socket.AF_UNSPEC
    return family


def _has_ipv6(host):
    """Returns True if the system can bind an IPv6 address."""
    sock = None
    has_ipv6 = False
    if _appengine_environ.is_appengine_sandbox():
        return False
    else:
        if socket.has_ipv6:
            try:
                sock = socket.socket(socket.AF_INET6)
                sock.bind((host, 0))
                has_ipv6 = True
            except Exception:
                pass

        if sock:
            sock.close()
        return has_ipv6


HAS_IPV6 = _has_ipv6('::1')