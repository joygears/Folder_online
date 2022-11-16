# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\connection.py
from __future__ import absolute_import
import datetime, logging, os, re, socket, warnings
from socket import error as SocketError
from socket import timeout as SocketTimeout
from .packages import six
from .packages.six.moves.http_client import HTTPConnection as _HTTPConnection
from .packages.six.moves.http_client import HTTPException
from .util.proxy import create_proxy_ssl_context
try:
    import ssl
    BaseSSLError = ssl.SSLError
except (ImportError, AttributeError):
    ssl = None

    class BaseSSLError(BaseException):
        pass


try:
    ConnectionError = ConnectionError
except NameError:

    class ConnectionError(Exception):
        pass


try:
    BrokenPipeError = BrokenPipeError
except NameError:

    class BrokenPipeError(Exception):
        pass


from ._collections import HTTPHeaderDict
from ._version import __version__
from .exceptions import ConnectTimeoutError, NewConnectionError, SubjectAltNameWarning, SystemTimeWarning
from .util import SKIP_HEADER, SKIPPABLE_HEADERS, connection
from .util.ssl_ import assert_fingerprint, create_urllib3_context, is_ipaddress, resolve_cert_reqs, resolve_ssl_version, ssl_wrap_socket
from .util.ssl_match_hostname import CertificateError, match_hostname
log = logging.getLogger(__name__)
port_by_scheme = {'http':80, 
 'https':443}
RECENT_DATE = datetime.date(2020, 7, 1)
_CONTAINS_CONTROL_CHAR_RE = re.compile("[^-!#$%&'*+.^_`|~0-9a-zA-Z]")

class HTTPConnection(_HTTPConnection, object):
    __doc__ = "\n    Based on :class:`http.client.HTTPConnection` but provides an extra constructor\n    backwards-compatibility layer between older and newer Pythons.\n\n    Additional keyword parameters are used to configure attributes of the connection.\n    Accepted parameters include:\n\n    - ``strict``: See the documentation on :class:`urllib3.connectionpool.HTTPConnectionPool`\n    - ``source_address``: Set the source address for the current connection.\n    - ``socket_options``: Set specific options on the underlying socket. If not specified, then\n      defaults are loaded from ``HTTPConnection.default_socket_options`` which includes disabling\n      Nagle's algorithm (sets TCP_NODELAY to 1) unless the connection is behind a proxy.\n\n      For example, if you wish to enable TCP Keep Alive in addition to the defaults,\n      you might pass:\n\n      .. code-block:: python\n\n         HTTPConnection.default_socket_options + [\n             (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),\n         ]\n\n      Or you may want to disable the defaults by passing an empty list (e.g., ``[]``).\n    "
    default_port = port_by_scheme['http']
    default_socket_options = [
     (
      socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)]
    is_verified = False
    proxy_is_verified = None

    def __init__(self, *args, **kw):
        if not six.PY2:
            kw.pop('strict', None)
        self.source_address = kw.get('source_address')
        self.socket_options = kw.pop('socket_options', self.default_socket_options)
        self.proxy = kw.pop('proxy', None)
        self.proxy_config = kw.pop('proxy_config', None)
        (_HTTPConnection.__init__)(self, *args, **kw)

    @property
    def host(self):
        """
        Getter method to remove any trailing dots that indicate the hostname is an FQDN.

        In general, SSL certificates don't include the trailing dot indicating a
        fully-qualified domain name, and thus, they don't validate properly when
        checked against a domain name that includes the dot. In addition, some
        servers may not expect to receive the trailing dot when provided.

        However, the hostname with trailing dot is critical to DNS resolution; doing a
        lookup with the trailing dot will properly only resolve the appropriate FQDN,
        whereas a lookup without a trailing dot will search the system's search domain
        list. Thus, it's important to keep the original host around for use only in
        those cases where it's appropriate (i.e., when doing DNS lookup to establish the
        actual TCP connection across which we're going to send HTTP requests).
        """
        return self._dns_host.rstrip('.')

    @host.setter
    def host(self, value):
        """
        Setter for the `host` property.

        We assume that only urllib3 uses the _dns_host attribute; httplib itself
        only uses `host`, and it seems reasonable that other libraries follow suit.
        """
        self._dns_host = value

    def _new_conn(self):
        """Establish a socket connection and set nodelay settings on it.

        :return: New socket connection.
        """
        extra_kw = {}
        if self.source_address:
            extra_kw['source_address'] = self.source_address
        if self.socket_options:
            extra_kw['socket_options'] = self.socket_options
        try:
            conn = (connection.create_connection)(
             (
              self._dns_host, self.port), (self.timeout), **extra_kw)
        except SocketTimeout:
            raise ConnectTimeoutError(self, 'Connection to %s timed out. (connect timeout=%s)' % (
             self.host, self.timeout))
        except SocketError as e:
            raise NewConnectionError(self, 'Failed to establish a new connection: %s' % e)

        return conn

    def _is_using_tunnel(self):
        return getattr(self, '_tunnel_host', None)

    def _prepare_conn(self, conn):
        self.sock = conn
        if self._is_using_tunnel():
            self._tunnel()
            self.auto_open = 0

    def connect(self):
        conn = self._new_conn()
        self._prepare_conn(conn)

    def putrequest(self, method, url, *args, **kwargs):
        """ """
        match = _CONTAINS_CONTROL_CHAR_RE.search(method)
        if match:
            raise ValueError('Method cannot contain non-token characters %r (found at least %r)' % (
             method, match.group()))
        return (_HTTPConnection.putrequest)(self, method, url, *args, **kwargs)

    def putheader(self, header, *values):
        """ """
        if not any(isinstance(v, str) and v == SKIP_HEADER for v in values):
            (_HTTPConnection.putheader)(self, header, *values)
        elif six.ensure_str(header.lower()) not in SKIPPABLE_HEADERS:
            raise ValueError("urllib3.util.SKIP_HEADER only supports '%s'" % (
             "', '".join(map(str.title, sorted(SKIPPABLE_HEADERS))),))

    def request(self, method, url, body=None, headers=None):
        if headers is None:
            headers = {}
        else:
            headers = headers.copy()
        if 'user-agent' not in (six.ensure_str(k.lower()) for k in headers):
            headers['User-Agent'] = _get_default_user_agent()
        super(HTTPConnection, self).request(method, url, body=body, headers=headers)

    def request_chunked(self, method, url, body=None, headers=None):
        """
        Alternative to the common request method, which sends the
        body with chunked encoding and not as one block
        """
        headers = headers or {}
        header_keys = set([six.ensure_str(k.lower()) for k in headers])
        skip_accept_encoding = 'accept-encoding' in header_keys
        skip_host = 'host' in header_keys
        self.putrequest(method,
          url, skip_accept_encoding=skip_accept_encoding, skip_host=skip_host)
        if 'user-agent' not in header_keys:
            self.putheader('User-Agent', _get_default_user_agent())
        for header, value in headers.items():
            self.putheader(header, value)

        if 'transfer-encoding' not in header_keys:
            self.putheader('Transfer-Encoding', 'chunked')
        self.endheaders()
        if body is not None:
            stringish_types = six.string_types + (bytes,)
            if isinstance(body, stringish_types):
                body = (
                 body,)
            for chunk in body:
                if not chunk:
                    pass
                else:
                    if not isinstance(chunk, bytes):
                        chunk = chunk.encode('utf8')
                    len_str = hex(len(chunk))[2:]
                    to_send = bytearray(len_str.encode())
                    to_send += b'\r\n'
                    to_send += chunk
                    to_send += b'\r\n'
                    self.send(to_send)

        self.send(b'0\r\n\r\n')


class HTTPSConnection(HTTPConnection):
    __doc__ = '\n    Many of the parameters to this constructor are passed to the underlying SSL\n    socket by means of :py:func:`urllib3.util.ssl_wrap_socket`.\n    '
    default_port = port_by_scheme['https']
    cert_reqs = None
    ca_certs = None
    ca_cert_dir = None
    ca_cert_data = None
    ssl_version = None
    assert_fingerprint = None
    tls_in_tls_required = False

    def __init__(self, host, port=None, key_file=None, cert_file=None, key_password=None, strict=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, ssl_context=None, server_hostname=None, **kw):
        (HTTPConnection.__init__)(self, host, port, strict=strict, timeout=timeout, **kw)
        self.key_file = key_file
        self.cert_file = cert_file
        self.key_password = key_password
        self.ssl_context = ssl_context
        self.server_hostname = server_hostname
        self._protocol = 'https'

    def set_cert(self, key_file=None, cert_file=None, cert_reqs=None, key_password=None, ca_certs=None, assert_hostname=None, assert_fingerprint=None, ca_cert_dir=None, ca_cert_data=None):
        """
        This method should only be called once, before the connection is used.
        """
        if cert_reqs is None:
            if self.ssl_context is not None:
                cert_reqs = self.ssl_context.verify_mode
            else:
                cert_reqs = resolve_cert_reqs(None)
        self.key_file = key_file
        self.cert_file = cert_file
        self.cert_reqs = cert_reqs
        self.key_password = key_password
        self.assert_hostname = assert_hostname
        self.assert_fingerprint = assert_fingerprint
        self.ca_certs = ca_certs and os.path.expanduser(ca_certs)
        self.ca_cert_dir = ca_cert_dir and os.path.expanduser(ca_cert_dir)
        self.ca_cert_data = ca_cert_data

    def connect(self):
        conn = self._new_conn()
        hostname = self.host
        tls_in_tls = False
        if self._is_using_tunnel():
            if self.tls_in_tls_required:
                conn = self._connect_tls_proxy(hostname, conn)
                tls_in_tls = True
            self.sock = conn
            self._tunnel()
            self.auto_open = 0
            hostname = self._tunnel_host
        server_hostname = hostname
        if self.server_hostname is not None:
            server_hostname = self.server_hostname
        is_time_off = datetime.date.today() < RECENT_DATE
        if is_time_off:
            warnings.warn('System time is way off (before {0}). This will probably lead to SSL verification errors'.format(RECENT_DATE), SystemTimeWarning)
        else:
            default_ssl_context = False
            if self.ssl_context is None:
                default_ssl_context = True
                self.ssl_context = create_urllib3_context(ssl_version=(resolve_ssl_version(self.ssl_version)),
                  cert_reqs=(resolve_cert_reqs(self.cert_reqs)))
            context = self.ssl_context
            context.verify_mode = resolve_cert_reqs(self.cert_reqs)
            if not self.ca_certs:
                if not self.ca_cert_dir:
                    if not self.ca_cert_data:
                        if default_ssl_context:
                            if hasattr(context, 'load_default_certs'):
                                context.load_default_certs()
            self.sock = ssl_wrap_socket(sock=conn,
              keyfile=(self.key_file),
              certfile=(self.cert_file),
              key_password=(self.key_password),
              ca_certs=(self.ca_certs),
              ca_cert_dir=(self.ca_cert_dir),
              ca_cert_data=(self.ca_cert_data),
              server_hostname=server_hostname,
              ssl_context=context,
              tls_in_tls=tls_in_tls)
            if default_ssl_context:
                if self.ssl_version is None:
                    if hasattr(self.sock, 'version'):
                        if self.sock.version() in frozenset({'TLSv1.1', 'TLSv1'}):
                            warnings.warn("Negotiating TLSv1/TLSv1.1 by default is deprecated and will be disabled in urllib3 v2.0.0. Connecting to '%s' with '%s' can be enabled by explicitly opting-in with 'ssl_version'" % (
                             self.host, self.sock.version()), DeprecationWarning)
            if self.assert_fingerprint:
                assert_fingerprint(self.sock.getpeercert(binary_form=True), self.assert_fingerprint)
            elif context.verify_mode != ssl.CERT_NONE:
                if not getattr(context, 'check_hostname', False):
                    if self.assert_hostname is not False:
                        cert = self.sock.getpeercert()
                        if not cert.get('subjectAltName', ()):
                            warnings.warn('Certificate for {0} has no `subjectAltName`, falling back to check for a `commonName` for now. This feature is being removed by major browsers and deprecated by RFC 2818. (See https://github.com/urllib3/urllib3/issues/497 for details.)'.format(hostname), SubjectAltNameWarning)
                        _match_hostname(cert, self.assert_hostname or server_hostname)
        self.is_verified = context.verify_mode == ssl.CERT_REQUIRED or self.assert_fingerprint is not None

    def _connect_tls_proxy(self, hostname, conn):
        """
        Establish a TLS connection to the proxy using the provided SSL context.
        """
        proxy_config = self.proxy_config
        ssl_context = proxy_config.ssl_context
        if ssl_context:
            return ssl_wrap_socket(sock=conn,
              server_hostname=hostname,
              ssl_context=ssl_context)
        else:
            ssl_context = create_proxy_ssl_context(self.ssl_version, self.cert_reqs, self.ca_certs, self.ca_cert_dir, self.ca_cert_data)
            socket = ssl_wrap_socket(sock=conn,
              ca_certs=(self.ca_certs),
              ca_cert_dir=(self.ca_cert_dir),
              ca_cert_data=(self.ca_cert_data),
              server_hostname=hostname,
              ssl_context=ssl_context)
            if ssl_context.verify_mode != ssl.CERT_NONE:
                if not getattr(ssl_context, 'check_hostname', False):
                    cert = socket.getpeercert()
                    if not cert.get('subjectAltName', ()):
                        warnings.warn('Certificate for {0} has no `subjectAltName`, falling back to check for a `commonName` for now. This feature is being removed by major browsers and deprecated by RFC 2818. (See https://github.com/urllib3/urllib3/issues/497 for details.)'.format(hostname), SubjectAltNameWarning)
                    _match_hostname(cert, hostname)
            self.proxy_is_verified = ssl_context.verify_mode == ssl.CERT_REQUIRED
            return socket


def _match_hostname(cert, asserted_hostname):
    stripped_hostname = asserted_hostname.strip('u[]')
    if is_ipaddress(stripped_hostname):
        asserted_hostname = stripped_hostname
    try:
        match_hostname(cert, asserted_hostname)
    except CertificateError as e:
        log.warning('Certificate did not match expected hostname: %s. Certificate: %s', asserted_hostname, cert)
        e._peer_cert = cert
        raise


def _get_default_user_agent():
    return 'python-urllib3/%s' % __version__


class DummyConnection(object):
    __doc__ = 'Used to detect a failed ConnectionCls import.'


if not ssl:
    HTTPSConnection = DummyConnection
VerifiedHTTPSConnection = HTTPSConnection