# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\exceptions.py
from __future__ import absolute_import
from .packages.six.moves.http_client import IncompleteRead as httplib_IncompleteRead

class HTTPError(Exception):
    __doc__ = 'Base exception used by this module.'


class HTTPWarning(Warning):
    __doc__ = 'Base warning used by this module.'


class PoolError(HTTPError):
    __doc__ = 'Base exception for errors caused within a pool.'

    def __init__(self, pool, message):
        self.pool = pool
        HTTPError.__init__(self, '%s: %s' % (pool, message))

    def __reduce__(self):
        return (
         self.__class__, (None, None))


class RequestError(PoolError):
    __doc__ = 'Base exception for PoolErrors that have associated URLs.'

    def __init__(self, pool, url, message):
        self.url = url
        PoolError.__init__(self, pool, message)

    def __reduce__(self):
        return (
         self.__class__, (None, self.url, None))


class SSLError(HTTPError):
    __doc__ = 'Raised when SSL certificate fails in an HTTPS connection.'


class ProxyError(HTTPError):
    __doc__ = 'Raised when the connection to a proxy fails.'

    def __init__(self, message, error, *args):
        (super(ProxyError, self).__init__)(message, error, *args)
        self.original_error = error


class DecodeError(HTTPError):
    __doc__ = 'Raised when automatic decoding based on Content-Type fails.'


class ProtocolError(HTTPError):
    __doc__ = 'Raised when something unexpected happens mid-request/response.'


ConnectionError = ProtocolError

class MaxRetryError(RequestError):
    __doc__ = 'Raised when the maximum number of retries is exceeded.\n\n    :param pool: The connection pool\n    :type pool: :class:`~urllib3.connectionpool.HTTPConnectionPool`\n    :param string url: The requested Url\n    :param exceptions.Exception reason: The underlying error\n\n    '

    def __init__(self, pool, url, reason=None):
        self.reason = reason
        message = 'Max retries exceeded with url: %s (Caused by %r)' % (url, reason)
        RequestError.__init__(self, pool, url, message)


class HostChangedError(RequestError):
    __doc__ = 'Raised when an existing pool gets a request for a foreign host.'

    def __init__(self, pool, url, retries=3):
        message = 'Tried to open a foreign host with url: %s' % url
        RequestError.__init__(self, pool, url, message)
        self.retries = retries


class TimeoutStateError(HTTPError):
    __doc__ = 'Raised when passing an invalid state to a timeout'


class TimeoutError(HTTPError):
    __doc__ = 'Raised when a socket timeout error occurs.\n\n    Catching this error will catch both :exc:`ReadTimeoutErrors\n    <ReadTimeoutError>` and :exc:`ConnectTimeoutErrors <ConnectTimeoutError>`.\n    '


class ReadTimeoutError(TimeoutError, RequestError):
    __doc__ = 'Raised when a socket timeout occurs while receiving data from a server'


class ConnectTimeoutError(TimeoutError):
    __doc__ = 'Raised when a socket timeout occurs while connecting to a server'


class NewConnectionError(ConnectTimeoutError, PoolError):
    __doc__ = 'Raised when we fail to establish a new connection. Usually ECONNREFUSED.'


class EmptyPoolError(PoolError):
    __doc__ = 'Raised when a pool runs out of connections and no more are allowed.'


class ClosedPoolError(PoolError):
    __doc__ = 'Raised when a request enters a pool after the pool has been closed.'


class LocationValueError(ValueError, HTTPError):
    __doc__ = 'Raised when there is something wrong with a given URL input.'


class LocationParseError(LocationValueError):
    __doc__ = 'Raised when get_host or similar fails to parse the URL input.'

    def __init__(self, location):
        message = 'Failed to parse: %s' % location
        HTTPError.__init__(self, message)
        self.location = location


class URLSchemeUnknown(LocationValueError):
    __doc__ = 'Raised when a URL input has an unsupported scheme.'

    def __init__(self, scheme):
        message = 'Not supported URL scheme %s' % scheme
        super(URLSchemeUnknown, self).__init__(message)
        self.scheme = scheme


class ResponseError(HTTPError):
    __doc__ = 'Used as a container for an error reason supplied in a MaxRetryError.'
    GENERIC_ERROR = 'too many error responses'
    SPECIFIC_ERROR = 'too many {status_code} error responses'


class SecurityWarning(HTTPWarning):
    __doc__ = 'Warned when performing security reducing actions'


class SubjectAltNameWarning(SecurityWarning):
    __doc__ = 'Warned when connecting to a host with a certificate missing a SAN.'


class InsecureRequestWarning(SecurityWarning):
    __doc__ = 'Warned when making an unverified HTTPS request.'


class SystemTimeWarning(SecurityWarning):
    __doc__ = 'Warned when system time is suspected to be wrong'


class InsecurePlatformWarning(SecurityWarning):
    __doc__ = 'Warned when certain TLS/SSL configuration is not available on a platform.'


class SNIMissingWarning(HTTPWarning):
    __doc__ = 'Warned when making a HTTPS request without SNI available.'


class DependencyWarning(HTTPWarning):
    __doc__ = '\n    Warned when an attempt is made to import a module with missing optional\n    dependencies.\n    '


class ResponseNotChunked(ProtocolError, ValueError):
    __doc__ = 'Response needs to be chunked in order to read it as chunks.'


class BodyNotHttplibCompatible(HTTPError):
    __doc__ = '\n    Body should be :class:`http.client.HTTPResponse` like\n    (have an fp attribute which returns raw chunks) for read_chunked().\n    '


class IncompleteRead(HTTPError, httplib_IncompleteRead):
    __doc__ = "\n    Response length doesn't match expected Content-Length\n\n    Subclass of :class:`http.client.IncompleteRead` to allow int value\n    for ``partial`` to avoid creating large objects on streamed reads.\n    "

    def __init__(self, partial, expected):
        super(IncompleteRead, self).__init__(partial, expected)

    def __repr__(self):
        return 'IncompleteRead(%i bytes read, %i more expected)' % (
         self.partial,
         self.expected)


class InvalidChunkLength(HTTPError, httplib_IncompleteRead):
    __doc__ = 'Invalid chunk length in a chunked response.'

    def __init__(self, response, length):
        super(InvalidChunkLength, self).__init__(response.tell(), response.length_remaining)
        self.response = response
        self.length = length

    def __repr__(self):
        return 'InvalidChunkLength(got length %r, %i bytes read)' % (
         self.length,
         self.partial)


class InvalidHeader(HTTPError):
    __doc__ = 'The header provided was somehow invalid.'


class ProxySchemeUnknown(AssertionError, URLSchemeUnknown):
    __doc__ = 'ProxyManager does not support the supplied scheme'

    def __init__(self, scheme):
        if scheme == 'localhost':
            scheme = None
        else:
            if scheme is None:
                message = 'Proxy URL had no scheme, should start with http:// or https://'
            else:
                message = 'Proxy URL had unsupported scheme %s, should use http:// or https://' % scheme
        super(ProxySchemeUnknown, self).__init__(message)


class ProxySchemeUnsupported(ValueError):
    __doc__ = 'Fetching HTTPS resources through HTTPS proxies is unsupported'


class HeaderParsingError(HTTPError):
    __doc__ = 'Raised by assert_header_parsing, but we convert it to a log.warning statement.'

    def __init__(self, defects, unparsed_data):
        message = '%s, unparsed data: %r' % (defects or 'Unknown', unparsed_data)
        super(HeaderParsingError, self).__init__(message)


class UnrewindableBodyError(HTTPError):
    __doc__ = 'urllib3 encountered an error when trying to rewind a body'