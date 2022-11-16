# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\connectionpool.py
from __future__ import absolute_import
import errno, logging, re, socket, sys, warnings
from socket import error as SocketError
from socket import timeout as SocketTimeout
from .connection import BaseSSLError, BrokenPipeError, DummyConnection, HTTPConnection, HTTPException, HTTPSConnection, VerifiedHTTPSConnection, port_by_scheme
from .exceptions import ClosedPoolError, EmptyPoolError, HeaderParsingError, HostChangedError, InsecureRequestWarning, LocationValueError, MaxRetryError, NewConnectionError, ProtocolError, ProxyError, ReadTimeoutError, SSLError, TimeoutError
from .packages import six
from .packages.six.moves import queue
from .request import RequestMethods
from .response import HTTPResponse
from .util.connection import is_connection_dropped
from .util.proxy import connection_requires_http_tunnel
from .util.queue import LifoQueue
from .util.request import set_file_position
from .util.response import assert_header_parsing
from .util.retry import Retry
from .util.ssl_match_hostname import CertificateError
from .util.timeout import Timeout
from .util.url import Url, _encode_target
from .util.url import _normalize_host as normalize_host
from .util.url import get_host, parse_url
xrange = six.moves.xrange
log = logging.getLogger(__name__)
_Default = object()

class ConnectionPool(object):
    __doc__ = "\n    Base class for all connection pools, such as\n    :class:`.HTTPConnectionPool` and :class:`.HTTPSConnectionPool`.\n\n    .. note::\n       ConnectionPool.urlopen() does not normalize or percent-encode target URIs\n       which is useful if your target server doesn't support percent-encoded\n       target URIs.\n    "
    scheme = None
    QueueCls = LifoQueue

    def __init__(self, host, port=None):
        if not host:
            raise LocationValueError('No host specified.')
        self.host = _normalize_host(host, scheme=(self.scheme))
        self._proxy_host = host.lower()
        self.port = port

    def __str__(self):
        return '%s(host=%r, port=%r)' % (type(self).__name__, self.host, self.port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def close(self):
        """
        Close all pooled connections and disable the pool.
        """
        pass


_blocking_errnos = {
 errno.EAGAIN, errno.EWOULDBLOCK}

class HTTPConnectionPool(ConnectionPool, RequestMethods):
    __doc__ = '\n    Thread-safe connection pool for one host.\n\n    :param host:\n        Host used for this HTTP Connection (e.g. "localhost"), passed into\n        :class:`http.client.HTTPConnection`.\n\n    :param port:\n        Port used for this HTTP Connection (None is equivalent to 80), passed\n        into :class:`http.client.HTTPConnection`.\n\n    :param strict:\n        Causes BadStatusLine to be raised if the status line can\'t be parsed\n        as a valid HTTP/1.0 or 1.1 status line, passed into\n        :class:`http.client.HTTPConnection`.\n\n        .. note::\n           Only works in Python 2. This parameter is ignored in Python 3.\n\n    :param timeout:\n        Socket timeout in seconds for each individual connection. This can\n        be a float or integer, which sets the timeout for the HTTP request,\n        or an instance of :class:`urllib3.util.Timeout` which gives you more\n        fine-grained control over request timeouts. After the constructor has\n        been parsed, this is always a `urllib3.util.Timeout` object.\n\n    :param maxsize:\n        Number of connections to save that can be reused. More than 1 is useful\n        in multithreaded situations. If ``block`` is set to False, more\n        connections will be created but they will not be saved once they\'ve\n        been used.\n\n    :param block:\n        If set to True, no more than ``maxsize`` connections will be used at\n        a time. When no free connections are available, the call will block\n        until a connection has been released. This is a useful side effect for\n        particular multithreaded situations where one does not want to use more\n        than maxsize connections per host to prevent flooding.\n\n    :param headers:\n        Headers to include with all requests, unless other headers are given\n        explicitly.\n\n    :param retries:\n        Retry configuration to use by default with requests in this pool.\n\n    :param _proxy:\n        Parsed proxy URL, should not be used directly, instead, see\n        :class:`urllib3.ProxyManager`\n\n    :param _proxy_headers:\n        A dictionary with proxy headers, should not be used directly,\n        instead, see :class:`urllib3.ProxyManager`\n\n    :param \\**conn_kw:\n        Additional parameters are used to create fresh :class:`urllib3.connection.HTTPConnection`,\n        :class:`urllib3.connection.HTTPSConnection` instances.\n    '
    scheme = 'http'
    ConnectionCls = HTTPConnection
    ResponseCls = HTTPResponse

    def __init__(self, host, port=None, strict=False, timeout=Timeout.DEFAULT_TIMEOUT, maxsize=1, block=False, headers=None, retries=None, _proxy=None, _proxy_headers=None, _proxy_config=None, **conn_kw):
        ConnectionPool.__init__(self, host, port)
        RequestMethods.__init__(self, headers)
        self.strict = strict
        if not isinstance(timeout, Timeout):
            timeout = Timeout.from_float(timeout)
        if retries is None:
            retries = Retry.DEFAULT
        self.timeout = timeout
        self.retries = retries
        self.pool = self.QueueCls(maxsize)
        self.block = block
        self.proxy = _proxy
        self.proxy_headers = _proxy_headers or {}
        self.proxy_config = _proxy_config
        for _ in xrange(maxsize):
            self.pool.put(None)

        self.num_connections = 0
        self.num_requests = 0
        self.conn_kw = conn_kw
        if self.proxy:
            self.conn_kw.setdefault('socket_options', [])
            self.conn_kw['proxy'] = self.proxy
            self.conn_kw['proxy_config'] = self.proxy_config

    def _new_conn(self):
        """
        Return a fresh :class:`HTTPConnection`.
        """
        self.num_connections += 1
        log.debug('Starting new HTTP connection (%d): %s:%s', self.num_connections, self.host, self.port or '80')
        conn = (self.ConnectionCls)(host=self.host, 
         port=self.port, 
         timeout=self.timeout.connect_timeout, 
         strict=self.strict, **self.conn_kw)
        return conn

    def _get_conn(self, timeout=None):
        """
        Get a connection. Will return a pooled connection if one is available.

        If no connections are available and :prop:`.block` is ``False``, then a
        fresh connection is returned.

        :param timeout:
            Seconds to wait before giving up and raising
            :class:`urllib3.exceptions.EmptyPoolError` if the pool is empty and
            :prop:`.block` is ``True``.
        """
        conn = None
        try:
            conn = self.pool.get(block=(self.block), timeout=timeout)
        except AttributeError:
            raise ClosedPoolError(self, 'Pool is closed.')
        except queue.Empty:
            if self.block:
                raise EmptyPoolError(self, 'Pool reached maximum size and no more connections are allowed.')

        if conn:
            if is_connection_dropped(conn):
                log.debug('Resetting dropped connection: %s', self.host)
                conn.close()
                if getattr(conn, 'auto_open', 1) == 0:
                    conn = None
        return conn or self._new_conn()

    def _put_conn(self, conn):
        """
        Put a connection back into the pool.

        :param conn:
            Connection object for the current host and port as returned by
            :meth:`._new_conn` or :meth:`._get_conn`.

        If the pool is already full, the connection is closed and discarded
        because we exceeded maxsize. If connections are discarded frequently,
        then maxsize should be increased.

        If the pool is closed, then the connection will be closed and discarded.
        """
        try:
            self.pool.put(conn, block=False)
            return
        except AttributeError:
            pass
        except queue.Full:
            log.warning('Connection pool is full, discarding connection: %s. Connection pool size: %s', self.host, self.pool.qsize())

        if conn:
            conn.close()

    def _validate_conn(self, conn):
        """
        Called right before a request is made, after the socket is created.
        """
        pass

    def _prepare_proxy(self, conn):
        pass

    def _get_timeout(self, timeout):
        """Helper that always returns a :class:`urllib3.util.Timeout`"""
        if timeout is _Default:
            return self.timeout.clone()
        else:
            if isinstance(timeout, Timeout):
                return timeout.clone()
            return Timeout.from_float(timeout)

    def _raise_timeout(self, err, url, timeout_value):
        """Is the error actually a timeout? Will raise a ReadTimeout or pass"""
        if isinstance(err, SocketTimeout):
            raise ReadTimeoutError(self, url, 'Read timed out. (read timeout=%s)' % timeout_value)
        else:
            if hasattr(err, 'errno'):
                if err.errno in _blocking_errnos:
                    raise ReadTimeoutError(self, url, 'Read timed out. (read timeout=%s)' % timeout_value)
            if 'timed out' in str(err) or 'did not complete (read)' in str(err):
                raise ReadTimeoutError(self, url, 'Read timed out. (read timeout=%s)' % timeout_value)

    def _make_request(self, conn, method, url, timeout=_Default, chunked=False, **httplib_request_kw):
        """
        Perform a request on a given urllib connection object taken from our
        pool.

        :param conn:
            a connection from one of our connection pools

        :param timeout:
            Socket timeout in seconds for the request. This can be a
            float or integer, which will set the same timeout value for
            the socket connect and the socket read, or an instance of
            :class:`urllib3.util.Timeout`, which gives you more fine-grained
            control over your timeouts.
        """
        self.num_requests += 1
        timeout_obj = self._get_timeout(timeout)
        timeout_obj.start_connect()
        conn.timeout = timeout_obj.connect_timeout
        try:
            self._validate_conn(conn)
        except (SocketTimeout, BaseSSLError) as e:
            self._raise_timeout(err=e, url=url, timeout_value=(conn.timeout))
            raise

        try:
            if chunked:
                (conn.request_chunked)(method, url, **httplib_request_kw)
            else:
                (conn.request)(method, url, **httplib_request_kw)
        except BrokenPipeError:
            pass
        except IOError as e:
            if e.errno not in {
             errno.EPIPE,
             errno.ESHUTDOWN,
             errno.EPROTOTYPE}:
                raise

        read_timeout = timeout_obj.read_timeout
        if getattr(conn, 'sock', None):
            if read_timeout == 0:
                raise ReadTimeoutError(self, url, 'Read timed out. (read timeout=%s)' % read_timeout)
            else:
                if read_timeout is Timeout.DEFAULT_TIMEOUT:
                    conn.sock.settimeout(socket.getdefaulttimeout())
                else:
                    conn.sock.settimeout(read_timeout)
        try:
            try:
                httplib_response = conn.getresponse(buffering=True)
            except TypeError:
                try:
                    httplib_response = conn.getresponse()
                except BaseException as e:
                    six.raise_from(e, None)

        except (SocketTimeout, BaseSSLError, SocketError) as e:
            self._raise_timeout(err=e, url=url, timeout_value=read_timeout)
            raise

        http_version = getattr(conn, '_http_vsn_str', 'HTTP/?')
        log.debug('%s://%s:%s "%s %s %s" %s %s', self.scheme, self.host, self.port, method, url, http_version, httplib_response.status, httplib_response.length)
        try:
            assert_header_parsing(httplib_response.msg)
        except (HeaderParsingError, TypeError) as hpe:
            log.warning('Failed to parse headers (url=%s): %s',
              (self._absolute_url(url)),
              hpe,
              exc_info=True)

        return httplib_response

    def _absolute_url(self, path):
        return Url(scheme=(self.scheme), host=(self.host), port=(self.port), path=path).url

    def close(self):
        """
        Close all pooled connections and disable the pool.
        """
        if self.pool is None:
            return
        old_pool, self.pool = self.pool, None
        try:
            while 1:
                conn = old_pool.get(block=False)
                if conn:
                    conn.close()

        except queue.Empty:
            pass

    def is_same_host(self, url):
        """
        Check if the given ``url`` is a member of the same host as this
        connection pool.
        """
        if url.startswith('/'):
            return True
        else:
            scheme, host, port = get_host(url)
            if host is not None:
                host = _normalize_host(host, scheme=scheme)
            if self.port:
                if not port:
                    port = port_by_scheme.get(scheme)
            if not self.port:
                if port == port_by_scheme.get(scheme):
                    port = None
            return (
             scheme, host, port) == (self.scheme, self.host, self.port)

    def urlopen(self, method, url, body=None, headers=None, retries=None, redirect=True, assert_same_host=True, timeout=_Default, pool_timeout=None, release_conn=None, chunked=False, body_pos=None, **response_kw):
        r"""
        Get a connection from the pool and perform an HTTP request. This is the
        lowest level call for making a request, so you'll need to specify all
        the raw details.

        .. note::

           More commonly, it's appropriate to use a convenience method provided
           by :class:`.RequestMethods`, such as :meth:`request`.

        .. note::

           `release_conn` will only behave as expected if
           `preload_content=False` because we want to make
           `preload_content=False` the default behaviour someday soon without
           breaking backwards compatibility.

        :param method:
            HTTP request method (such as GET, POST, PUT, etc.)

        :param url:
            The URL to perform the request on.

        :param body:
            Data to send in the request body, either :class:`str`, :class:`bytes`,
            an iterable of :class:`str`/:class:`bytes`, or a file-like object.

        :param headers:
            Dictionary of custom headers to send, such as User-Agent,
            If-None-Match, etc. If None, pool headers are used. If provided,
            these headers completely replace any pool-specific headers.

        :param retries:
            Configure the number of retries to allow before raising a
            :class:`~urllib3.exceptions.MaxRetryError` exception.

            Pass ``None`` to retry until you receive a response. Pass a
            :class:`~urllib3.util.retry.Retry` object for fine-grained control
            over different types of retries.
            Pass an integer number to retry connection errors that many times,
            but no other types of errors. Pass zero to never retry.

            If ``False``, then retries are disabled and any exception is raised
            immediately. Also, instead of raising a MaxRetryError on redirects,
            the redirect response will be returned.

        :type retries: :class:`~urllib3.util.retry.Retry`, False, or an int.

        :param redirect:
            If True, automatically handle redirects (status codes 301, 302,
            303, 307, 308). Each redirect counts as a retry. Disabling retries
            will disable redirect, too.

        :param assert_same_host:
            If ``True``, will make sure that the host of the pool requests is
            consistent else will raise HostChangedError. When ``False``, you can
            use the pool on an HTTP proxy and request foreign hosts.

        :param timeout:
            If specified, overrides the default timeout for this one
            request. It may be a float (in seconds) or an instance of
            :class:`urllib3.util.Timeout`.

        :param pool_timeout:
            If set and the pool is set to block=True, then this method will
            block for ``pool_timeout`` seconds and raise EmptyPoolError if no
            connection is available within the time period.

        :param release_conn:
            If False, then the urlopen call will not release the connection
            back into the pool once a response is received (but will release if
            you read the entire contents of the response such as when
            `preload_content=True`). This is useful if you're not preloading
            the response's content immediately. You will need to call
            ``r.release_conn()`` on the response ``r`` to return the connection
            back into the pool. If None, it takes the value of
            ``response_kw.get('preload_content', True)``.

        :param chunked:
            If True, urllib3 will send the body using chunked transfer
            encoding. Otherwise, urllib3 will send the body using the standard
            content-length form. Defaults to False.

        :param int body_pos:
            Position to seek to in file-like body in the event of a retry or
            redirect. Typically this won't need to be set because urllib3 will
            auto-populate the value when needed.

        :param \**response_kw:
            Additional parameters are passed to
            :meth:`urllib3.response.HTTPResponse.from_httplib`
        """
        parsed_url = parse_url(url)
        destination_scheme = parsed_url.scheme
        if headers is None:
            headers = self.headers
        else:
            if not isinstance(retries, Retry):
                retries = Retry.from_int(retries, redirect=redirect, default=(self.retries))
            else:
                if release_conn is None:
                    release_conn = response_kw.get('preload_content', True)
                if assert_same_host:
                    if not self.is_same_host(url):
                        raise HostChangedError(self, url, retries)
            if url.startswith('/'):
                url = six.ensure_str(_encode_target(url))
            else:
                url = six.ensure_str(parsed_url.url)
        conn = None
        release_this_conn = release_conn
        http_tunnel_required = connection_requires_http_tunnel(self.proxy, self.proxy_config, destination_scheme)
        if not http_tunnel_required:
            headers = headers.copy()
            headers.update(self.proxy_headers)
        err = None
        clean_exit = False
        body_pos = set_file_position(body, body_pos)
        try:
            try:
                timeout_obj = self._get_timeout(timeout)
                conn = self._get_conn(timeout=pool_timeout)
                conn.timeout = timeout_obj.connect_timeout
                is_new_proxy_conn = self.proxy is not None and not getattr(conn, 'sock', None)
                if is_new_proxy_conn:
                    if http_tunnel_required:
                        self._prepare_proxy(conn)
                httplib_response = self._make_request(conn,
                  method,
                  url,
                  timeout=timeout_obj,
                  body=body,
                  headers=headers,
                  chunked=chunked)
                response_conn = conn if not release_conn else None
                response_kw['request_method'] = method
                response = (self.ResponseCls.from_httplib)(
 httplib_response, pool=self, 
                 connection=response_conn, 
                 retries=retries, **response_kw)
                clean_exit = True
            except EmptyPoolError:
                clean_exit = True
                release_this_conn = False
                raise
            except (
             TimeoutError,
             HTTPException,
             SocketError,
             ProtocolError,
             BaseSSLError,
             SSLError,
             CertificateError) as e:
                clean_exit = False

                def _is_ssl_error_message_from_http_proxy(ssl_error):
                    message = ' '.join(re.split('[^a-z]', str(ssl_error).lower()))
                    return 'wrong version number' in message or 'unknown protocol' in message

                if isinstance(e, BaseSSLError):
                    if self.proxy:
                        if _is_ssl_error_message_from_http_proxy(e):
                            e = ProxyError('Your proxy appears to only use HTTP and not HTTPS, try changing your proxy URL to be HTTP. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#https-proxy-error-http-proxy', SSLError(e))
                if isinstance(e, (BaseSSLError, CertificateError)):
                    e = SSLError(e)
                else:
                    if isinstance(e, (SocketError, NewConnectionError)):
                        if self.proxy:
                            e = ProxyError('Cannot connect to proxy.', e)
                if isinstance(e, (SocketError, HTTPException)):
                    e = ProtocolError('Connection aborted.', e)
                retries = retries.increment(method,
                  url, error=e, _pool=self, _stacktrace=(sys.exc_info()[2]))
                retries.sleep()
                err = e

        finally:
            if not clean_exit:
                conn = conn and conn.close()
                release_this_conn = True
            if release_this_conn:
                self._put_conn(conn)

        if not conn:
            log.warning("Retrying (%r) after connection broken by '%r': %s", retries, err, url)
            return (self.urlopen)(
 method,
 url,
 body,
 headers,
 retries,
 redirect,
 assert_same_host, timeout=timeout, 
             pool_timeout=pool_timeout, 
             release_conn=release_conn, 
             chunked=chunked, 
             body_pos=body_pos, **response_kw)
        redirect_location = redirect and response.get_redirect_location()
        if redirect_location:
            if response.status == 303:
                method = 'GET'
            try:
                retries = retries.increment(method, url, response=response, _pool=self)
            except MaxRetryError:
                if retries.raise_on_redirect:
                    response.drain_conn()
                    raise
                return response
            else:
                response.drain_conn()
                retries.sleep_for_retry(response)
                log.debug('Redirecting %s -> %s', url, redirect_location)
            return (self.urlopen)(
 method,
 redirect_location,
 body,
 headers, retries=retries, 
             redirect=redirect, 
             assert_same_host=assert_same_host, 
             timeout=timeout, 
             pool_timeout=pool_timeout, 
             release_conn=release_conn, 
             chunked=chunked, 
             body_pos=body_pos, **response_kw)
        else:
            has_retry_after = bool(response.getheader('Retry-After'))
            if retries.is_retry(method, response.status, has_retry_after):
                try:
                    retries = retries.increment(method, url, response=response, _pool=self)
                except MaxRetryError:
                    if retries.raise_on_status:
                        response.drain_conn()
                        raise
                    return response
                else:
                    response.drain_conn()
                    retries.sleep(response)
                    log.debug('Retry: %s', url)
                    return (self.urlopen)(
 method,
 url,
 body,
 headers, retries=retries, 
                     redirect=redirect, 
                     assert_same_host=assert_same_host, 
                     timeout=timeout, 
                     pool_timeout=pool_timeout, 
                     release_conn=release_conn, 
                     chunked=chunked, 
                     body_pos=body_pos, **response_kw)
            return response


class HTTPSConnectionPool(HTTPConnectionPool):
    __doc__ = '\n    Same as :class:`.HTTPConnectionPool`, but HTTPS.\n\n    :class:`.HTTPSConnection` uses one of ``assert_fingerprint``,\n    ``assert_hostname`` and ``host`` in this order to verify connections.\n    If ``assert_hostname`` is False, no verification is done.\n\n    The ``key_file``, ``cert_file``, ``cert_reqs``, ``ca_certs``,\n    ``ca_cert_dir``, ``ssl_version``, ``key_password`` are only used if :mod:`ssl`\n    is available and are fed into :meth:`urllib3.util.ssl_wrap_socket` to upgrade\n    the connection socket into an SSL socket.\n    '
    scheme = 'https'
    ConnectionCls = HTTPSConnection

    def __init__(self, host, port=None, strict=False, timeout=Timeout.DEFAULT_TIMEOUT, maxsize=1, block=False, headers=None, retries=None, _proxy=None, _proxy_headers=None, key_file=None, cert_file=None, cert_reqs=None, key_password=None, ca_certs=None, ssl_version=None, assert_hostname=None, assert_fingerprint=None, ca_cert_dir=None, **conn_kw):
        (HTTPConnectionPool.__init__)(
         self, 
         host, 
         port, 
         strict, 
         timeout, 
         maxsize, 
         block, 
         headers, 
         retries, 
         _proxy, 
         _proxy_headers, **conn_kw)
        self.key_file = key_file
        self.cert_file = cert_file
        self.cert_reqs = cert_reqs
        self.key_password = key_password
        self.ca_certs = ca_certs
        self.ca_cert_dir = ca_cert_dir
        self.ssl_version = ssl_version
        self.assert_hostname = assert_hostname
        self.assert_fingerprint = assert_fingerprint

    def _prepare_conn(self, conn):
        """
        Prepare the ``connection`` for :meth:`urllib3.util.ssl_wrap_socket`
        and establish the tunnel if proxy is used.
        """
        if isinstance(conn, VerifiedHTTPSConnection):
            conn.set_cert(key_file=(self.key_file),
              key_password=(self.key_password),
              cert_file=(self.cert_file),
              cert_reqs=(self.cert_reqs),
              ca_certs=(self.ca_certs),
              ca_cert_dir=(self.ca_cert_dir),
              assert_hostname=(self.assert_hostname),
              assert_fingerprint=(self.assert_fingerprint))
            conn.ssl_version = self.ssl_version
        return conn

    def _prepare_proxy(self, conn):
        """
        Establishes a tunnel connection through HTTP CONNECT.

        Tunnel connection is established early because otherwise httplib would
        improperly set Host: header to proxy's IP:port.
        """
        conn.set_tunnel(self._proxy_host, self.port, self.proxy_headers)
        if self.proxy.scheme == 'https':
            conn.tls_in_tls_required = True
        conn.connect()

    def _new_conn(self):
        """
        Return a fresh :class:`http.client.HTTPSConnection`.
        """
        self.num_connections += 1
        log.debug('Starting new HTTPS connection (%d): %s:%s', self.num_connections, self.host, self.port or '443')
        if not self.ConnectionCls or self.ConnectionCls is DummyConnection:
            raise SSLError("Can't connect to HTTPS URL because the SSL module is not available.")
        actual_host = self.host
        actual_port = self.port
        if self.proxy is not None:
            actual_host = self.proxy.host
            actual_port = self.proxy.port
        conn = (self.ConnectionCls)(host=actual_host, 
         port=actual_port, 
         timeout=self.timeout.connect_timeout, 
         strict=self.strict, 
         cert_file=self.cert_file, 
         key_file=self.key_file, 
         key_password=self.key_password, **self.conn_kw)
        return self._prepare_conn(conn)

    def _validate_conn(self, conn):
        super(HTTPSConnectionPool, self)._validate_conn(conn)
        if not getattr(conn, 'sock', None):
            conn.connect()
        if not conn.is_verified:
            warnings.warn("Unverified HTTPS request is being made to host '%s'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings" % conn.host, InsecureRequestWarning)
        if getattr(conn, 'proxy_is_verified', None) is False:
            warnings.warn('Unverified HTTPS connection done to an HTTPS proxy. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings', InsecureRequestWarning)


def connection_from_url(url, **kw):
    r"""
    Given a url, return an :class:`.ConnectionPool` instance of its host.

    This is a shortcut for not having to parse out the scheme, host, and port
    of the url before creating an :class:`.ConnectionPool` instance.

    :param url:
        Absolute URL string that must include the scheme. Port is optional.

    :param \**kw:
        Passes additional parameters to the constructor of the appropriate
        :class:`.ConnectionPool`. Useful for specifying things like
        timeout, maxsize, headers, etc.

    Example::

        >>> conn = connection_from_url('http://google.com/')
        >>> r = conn.request('GET', '/')
    """
    scheme, host, port = get_host(url)
    port = port or port_by_scheme.get(scheme, 80)
    if scheme == 'https':
        return HTTPSConnectionPool(host, port=port, **kw)
    else:
        return HTTPConnectionPool(host, port=port, **kw)


def _normalize_host(host, scheme):
    """
    Normalize hosts for comparisons and use with sockets.
    """
    host = normalize_host(host, scheme)
    if host.startswith('['):
        if host.endswith(']'):
            host = host[1:-1]
    return host