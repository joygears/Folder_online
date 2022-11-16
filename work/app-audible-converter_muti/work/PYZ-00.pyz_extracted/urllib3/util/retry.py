# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\util\retry.py
from __future__ import absolute_import
import email, logging, re, time, warnings
from collections import namedtuple
from itertools import takewhile
from ..exceptions import ConnectTimeoutError, InvalidHeader, MaxRetryError, ProtocolError, ProxyError, ReadTimeoutError, ResponseError
from ..packages import six
log = logging.getLogger(__name__)
RequestHistory = namedtuple('RequestHistory', ['method', 'url', 'error', 'status', 'redirect_location'])
_Default = object()

class _RetryMeta(type):

    @property
    def DEFAULT_METHOD_WHITELIST(cls):
        warnings.warn("Using 'Retry.DEFAULT_METHOD_WHITELIST' is deprecated and will be removed in v2.0. Use 'Retry.DEFAULT_ALLOWED_METHODS' instead", DeprecationWarning)
        return cls.DEFAULT_ALLOWED_METHODS

    @DEFAULT_METHOD_WHITELIST.setter
    def DEFAULT_METHOD_WHITELIST(cls, value):
        warnings.warn("Using 'Retry.DEFAULT_METHOD_WHITELIST' is deprecated and will be removed in v2.0. Use 'Retry.DEFAULT_ALLOWED_METHODS' instead", DeprecationWarning)
        cls.DEFAULT_ALLOWED_METHODS = value

    @property
    def DEFAULT_REDIRECT_HEADERS_BLACKLIST(cls):
        warnings.warn("Using 'Retry.DEFAULT_REDIRECT_HEADERS_BLACKLIST' is deprecated and will be removed in v2.0. Use 'Retry.DEFAULT_REMOVE_HEADERS_ON_REDIRECT' instead", DeprecationWarning)
        return cls.DEFAULT_REMOVE_HEADERS_ON_REDIRECT

    @DEFAULT_REDIRECT_HEADERS_BLACKLIST.setter
    def DEFAULT_REDIRECT_HEADERS_BLACKLIST(cls, value):
        warnings.warn("Using 'Retry.DEFAULT_REDIRECT_HEADERS_BLACKLIST' is deprecated and will be removed in v2.0. Use 'Retry.DEFAULT_REMOVE_HEADERS_ON_REDIRECT' instead", DeprecationWarning)
        cls.DEFAULT_REMOVE_HEADERS_ON_REDIRECT = value

    @property
    def BACKOFF_MAX(cls):
        warnings.warn("Using 'Retry.BACKOFF_MAX' is deprecated and will be removed in v2.0. Use 'Retry.DEFAULT_BACKOFF_MAX' instead", DeprecationWarning)
        return cls.DEFAULT_BACKOFF_MAX

    @BACKOFF_MAX.setter
    def BACKOFF_MAX(cls, value):
        warnings.warn("Using 'Retry.BACKOFF_MAX' is deprecated and will be removed in v2.0. Use 'Retry.DEFAULT_BACKOFF_MAX' instead", DeprecationWarning)
        cls.DEFAULT_BACKOFF_MAX = value


@six.add_metaclass(_RetryMeta)
class Retry(object):
    __doc__ = "Retry configuration.\n\n    Each retry attempt will create a new Retry object with updated values, so\n    they can be safely reused.\n\n    Retries can be defined as a default for a pool::\n\n        retries = Retry(connect=5, read=2, redirect=5)\n        http = PoolManager(retries=retries)\n        response = http.request('GET', 'http://example.com/')\n\n    Or per-request (which overrides the default for the pool)::\n\n        response = http.request('GET', 'http://example.com/', retries=Retry(10))\n\n    Retries can be disabled by passing ``False``::\n\n        response = http.request('GET', 'http://example.com/', retries=False)\n\n    Errors will be wrapped in :class:`~urllib3.exceptions.MaxRetryError` unless\n    retries are disabled, in which case the causing exception will be raised.\n\n    :param int total:\n        Total number of retries to allow. Takes precedence over other counts.\n\n        Set to ``None`` to remove this constraint and fall back on other\n        counts.\n\n        Set to ``0`` to fail on the first retry.\n\n        Set to ``False`` to disable and imply ``raise_on_redirect=False``.\n\n    :param int connect:\n        How many connection-related errors to retry on.\n\n        These are errors raised before the request is sent to the remote server,\n        which we assume has not triggered the server to process the request.\n\n        Set to ``0`` to fail on the first retry of this type.\n\n    :param int read:\n        How many times to retry on read errors.\n\n        These errors are raised after the request was sent to the server, so the\n        request may have side-effects.\n\n        Set to ``0`` to fail on the first retry of this type.\n\n    :param int redirect:\n        How many redirects to perform. Limit this to avoid infinite redirect\n        loops.\n\n        A redirect is a HTTP response with a status code 301, 302, 303, 307 or\n        308.\n\n        Set to ``0`` to fail on the first retry of this type.\n\n        Set to ``False`` to disable and imply ``raise_on_redirect=False``.\n\n    :param int status:\n        How many times to retry on bad status codes.\n\n        These are retries made on responses, where status code matches\n        ``status_forcelist``.\n\n        Set to ``0`` to fail on the first retry of this type.\n\n    :param int other:\n        How many times to retry on other errors.\n\n        Other errors are errors that are not connect, read, redirect or status errors.\n        These errors might be raised after the request was sent to the server, so the\n        request might have side-effects.\n\n        Set to ``0`` to fail on the first retry of this type.\n\n        If ``total`` is not set, it's a good idea to set this to 0 to account\n        for unexpected edge cases and avoid infinite retry loops.\n\n    :param iterable allowed_methods:\n        Set of uppercased HTTP method verbs that we should retry on.\n\n        By default, we only retry on methods which are considered to be\n        idempotent (multiple requests with the same parameters end with the\n        same state). See :attr:`Retry.DEFAULT_ALLOWED_METHODS`.\n\n        Set to a ``False`` value to retry on any verb.\n\n        .. warning::\n\n            Previously this parameter was named ``method_whitelist``, that\n            usage is deprecated in v1.26.0 and will be removed in v2.0.\n\n    :param iterable status_forcelist:\n        A set of integer HTTP status codes that we should force a retry on.\n        A retry is initiated if the request method is in ``allowed_methods``\n        and the response status code is in ``status_forcelist``.\n\n        By default, this is disabled with ``None``.\n\n    :param float backoff_factor:\n        A backoff factor to apply between attempts after the second try\n        (most errors are resolved immediately by a second try without a\n        delay). urllib3 will sleep for::\n\n            {backoff factor} * (2 ** ({number of total retries} - 1))\n\n        seconds. If the backoff_factor is 0.1, then :func:`.sleep` will sleep\n        for [0.0s, 0.2s, 0.4s, ...] between retries. It will never be longer\n        than :attr:`Retry.DEFAULT_BACKOFF_MAX`.\n\n        By default, backoff is disabled (set to 0).\n\n    :param bool raise_on_redirect: Whether, if the number of redirects is\n        exhausted, to raise a MaxRetryError, or to return a response with a\n        response code in the 3xx range.\n\n    :param bool raise_on_status: Similar meaning to ``raise_on_redirect``:\n        whether we should raise an exception, or return a response,\n        if status falls in ``status_forcelist`` range and retries have\n        been exhausted.\n\n    :param tuple history: The history of the request encountered during\n        each call to :meth:`~Retry.increment`. The list is in the order\n        the requests occurred. Each list item is of class :class:`RequestHistory`.\n\n    :param bool respect_retry_after_header:\n        Whether to respect Retry-After header on status codes defined as\n        :attr:`Retry.RETRY_AFTER_STATUS_CODES` or not.\n\n    :param iterable remove_headers_on_redirect:\n        Sequence of headers to remove from the request when a response\n        indicating a redirect is returned before firing off the redirected\n        request.\n    "
    DEFAULT_ALLOWED_METHODS = frozenset([
     'HEAD', 'GET', 'PUT', 'DELETE', 'OPTIONS', 'TRACE'])
    RETRY_AFTER_STATUS_CODES = frozenset([413, 429, 503])
    DEFAULT_REMOVE_HEADERS_ON_REDIRECT = frozenset(['Authorization'])
    DEFAULT_BACKOFF_MAX = 120

    def __init__(self, total=10, connect=None, read=None, redirect=None, status=None, other=None, allowed_methods=_Default, status_forcelist=None, backoff_factor=0, raise_on_redirect=True, raise_on_status=True, history=None, respect_retry_after_header=True, remove_headers_on_redirect=_Default, method_whitelist=_Default):
        if method_whitelist is not _Default:
            if allowed_methods is not _Default:
                raise ValueError("Using both 'allowed_methods' and 'method_whitelist' together is not allowed. Instead only use 'allowed_methods'")
            warnings.warn("Using 'method_whitelist' with Retry is deprecated and will be removed in v2.0. Use 'allowed_methods' instead",
              DeprecationWarning,
              stacklevel=2)
            allowed_methods = method_whitelist
        else:
            if allowed_methods is _Default:
                allowed_methods = self.DEFAULT_ALLOWED_METHODS
            if remove_headers_on_redirect is _Default:
                remove_headers_on_redirect = self.DEFAULT_REMOVE_HEADERS_ON_REDIRECT
            self.total = total
            self.connect = connect
            self.read = read
            self.status = status
            self.other = other
            if redirect is False or total is False:
                redirect = 0
                raise_on_redirect = False
        self.redirect = redirect
        self.status_forcelist = status_forcelist or set()
        self.allowed_methods = allowed_methods
        self.backoff_factor = backoff_factor
        self.raise_on_redirect = raise_on_redirect
        self.raise_on_status = raise_on_status
        self.history = history or tuple()
        self.respect_retry_after_header = respect_retry_after_header
        self.remove_headers_on_redirect = frozenset([h.lower() for h in remove_headers_on_redirect])

    def new(self, **kw):
        params = dict(total=(self.total),
          connect=(self.connect),
          read=(self.read),
          redirect=(self.redirect),
          status=(self.status),
          other=(self.other),
          status_forcelist=(self.status_forcelist),
          backoff_factor=(self.backoff_factor),
          raise_on_redirect=(self.raise_on_redirect),
          raise_on_status=(self.raise_on_status),
          history=(self.history),
          remove_headers_on_redirect=(self.remove_headers_on_redirect),
          respect_retry_after_header=(self.respect_retry_after_header))
        if 'method_whitelist' not in kw:
            if 'allowed_methods' not in kw:
                if 'method_whitelist' in self.__dict__:
                    warnings.warn("Using 'method_whitelist' with Retry is deprecated and will be removed in v2.0. Use 'allowed_methods' instead", DeprecationWarning)
                    params['method_whitelist'] = self.allowed_methods
                else:
                    params['allowed_methods'] = self.allowed_methods
        params.update(kw)
        return (type(self))(**params)

    @classmethod
    def from_int(cls, retries, redirect=True, default=None):
        """Backwards-compatibility for the old retries format."""
        if retries is None:
            retries = default if default is not None else cls.DEFAULT
        if isinstance(retries, Retry):
            return retries
        else:
            redirect = bool(redirect) and None
            new_retries = cls(retries, redirect=redirect)
            log.debug('Converted retries value: %r -> %r', retries, new_retries)
            return new_retries

    def get_backoff_time(self):
        """Formula for computing the current backoff

        :rtype: float
        """
        consecutive_errors_len = len(list(takewhile(lambda x: x.redirect_location is None, reversed(self.history))))
        if consecutive_errors_len <= 1:
            return 0
        else:
            backoff_value = self.backoff_factor * 2 ** (consecutive_errors_len - 1)
            return min(self.DEFAULT_BACKOFF_MAX, backoff_value)

    def parse_retry_after(self, retry_after):
        if re.match('^\\s*[0-9]+\\s*$', retry_after):
            seconds = int(retry_after)
        else:
            retry_date_tuple = email.utils.parsedate_tz(retry_after)
            if retry_date_tuple is None:
                raise InvalidHeader('Invalid Retry-After header: %s' % retry_after)
            if retry_date_tuple[9] is None:
                retry_date_tuple = retry_date_tuple[:9] + (0, ) + retry_date_tuple[10:]
            retry_date = email.utils.mktime_tz(retry_date_tuple)
            seconds = retry_date - time.time()
        if seconds < 0:
            seconds = 0
        return seconds

    def get_retry_after(self, response):
        """Get the value of Retry-After in seconds."""
        retry_after = response.getheader('Retry-After')
        if retry_after is None:
            return
        else:
            return self.parse_retry_after(retry_after)

    def sleep_for_retry(self, response=None):
        retry_after = self.get_retry_after(response)
        if retry_after:
            time.sleep(retry_after)
            return True
        else:
            return False

    def _sleep_backoff(self):
        backoff = self.get_backoff_time()
        if backoff <= 0:
            return
        time.sleep(backoff)

    def sleep(self, response=None):
        """Sleep between retry attempts.

        This method will respect a server's ``Retry-After`` response header
        and sleep the duration of the time requested. If that is not present, it
        will use an exponential backoff. By default, the backoff factor is 0 and
        this method will return immediately.
        """
        if self.respect_retry_after_header:
            if response:
                slept = self.sleep_for_retry(response)
                if slept:
                    return
        self._sleep_backoff()

    def _is_connection_error(self, err):
        """Errors when we're fairly sure that the server did not receive the
        request, so it should be safe to retry.
        """
        if isinstance(err, ProxyError):
            err = err.original_error
        return isinstance(err, ConnectTimeoutError)

    def _is_read_error(self, err):
        """Errors that occur after the request has been started, so we should
        assume that the server began processing it.
        """
        return isinstance(err, (ReadTimeoutError, ProtocolError))

    def _is_method_retryable(self, method):
        """Checks if a given HTTP method should be retried upon, depending if
        it is included in the allowed_methods
        """
        if 'method_whitelist' in self.__dict__:
            warnings.warn("Using 'method_whitelist' with Retry is deprecated and will be removed in v2.0. Use 'allowed_methods' instead", DeprecationWarning)
            allowed_methods = self.method_whitelist
        else:
            allowed_methods = self.allowed_methods
        if allowed_methods:
            if method.upper() not in allowed_methods:
                return False
        return True

    def is_retry(self, method, status_code, has_retry_after=False):
        """Is this method/status code retryable? (Based on allowlists and control
        variables such as the number of total retries to allow, whether to
        respect the Retry-After header, whether this header is present, and
        whether the returned status code is on the list of status codes to
        be retried upon on the presence of the aforementioned header)
        """
        if not self._is_method_retryable(method):
            return False
        else:
            if self.status_forcelist:
                if status_code in self.status_forcelist:
                    return True
            return self.total and self.respect_retry_after_header and has_retry_after and status_code in self.RETRY_AFTER_STATUS_CODES

    def is_exhausted(self):
        """Are we out of retries?"""
        retry_counts = (
         self.total,
         self.connect,
         self.read,
         self.redirect,
         self.status,
         self.other)
        retry_counts = list(filter(None, retry_counts))
        if not retry_counts:
            return False
        else:
            return min(retry_counts) < 0

    def increment(self, method=None, url=None, response=None, error=None, _pool=None, _stacktrace=None):
        """Return a new Retry object with incremented retry counters.

        :param response: A response object, or None, if the server did not
            return a response.
        :type response: :class:`~urllib3.response.HTTPResponse`
        :param Exception error: An error encountered during the request, or
            None if the response was received successfully.

        :return: A new ``Retry`` object.
        """
        if self.total is False:
            if error:
                raise six.reraise(type(error), error, _stacktrace)
            total = self.total
            if total is not None:
                total -= 1
            connect = self.connect
            read = self.read
            redirect = self.redirect
            status_count = self.status
            other = self.other
            cause = 'unknown'
            status = None
            redirect_location = None
            if error and self._is_connection_error(error):
                if connect is False:
                    raise six.reraise(type(error), error, _stacktrace)
                else:
                    if connect is not None:
                        connect -= 1
        else:
            if error and self._is_read_error(error):
                if read is False or not self._is_method_retryable(method):
                    raise six.reraise(type(error), error, _stacktrace)
                else:
                    if read is not None:
                        read -= 1
        if error:
            if other is not None:
                other -= 1
        else:
            if response:
                if response.get_redirect_location():
                    if redirect is not None:
                        redirect -= 1
                    cause = 'too many redirects'
                    redirect_location = response.get_redirect_location()
                    status = response.status
            else:
                cause = ResponseError.GENERIC_ERROR
                if response:
                    if response.status:
                        if status_count is not None:
                            status_count -= 1
                        cause = ResponseError.SPECIFIC_ERROR.format(status_code=(response.status))
                        status = response.status
                history = self.history + (
                 RequestHistory(method, url, error, status, redirect_location),)
                new_retry = self.new(total=total,
                  connect=connect,
                  read=read,
                  redirect=redirect,
                  status=status_count,
                  other=other,
                  history=history)
                if new_retry.is_exhausted():
                    raise MaxRetryError(_pool, url, error or ResponseError(cause))
            log.debug("Incremented Retry for (url='%s'): %r", url, new_retry)
            return new_retry

    def __repr__(self):
        return '{cls.__name__}(total={self.total}, connect={self.connect}, read={self.read}, redirect={self.redirect}, status={self.status})'.format(cls=(type(self)),
          self=self)

    def __getattr__(self, item):
        if item == 'method_whitelist':
            warnings.warn("Using 'method_whitelist' with Retry is deprecated and will be removed in v2.0. Use 'allowed_methods' instead", DeprecationWarning)
            return self.allowed_methods
        try:
            return getattr(super(Retry, self), item)
        except AttributeError:
            return getattr(Retry, item)


Retry.DEFAULT = Retry(3)