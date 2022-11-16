# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\util\timeout.py
from __future__ import absolute_import
import time
from socket import _GLOBAL_DEFAULT_TIMEOUT
from ..exceptions import TimeoutStateError
_Default = object()
current_time = getattr(time, 'monotonic', time.time)

class Timeout(object):
    __doc__ = 'Timeout configuration.\n\n    Timeouts can be defined as a default for a pool:\n\n    .. code-block:: python\n\n       timeout = Timeout(connect=2.0, read=7.0)\n       http = PoolManager(timeout=timeout)\n       response = http.request(\'GET\', \'http://example.com/\')\n\n    Or per-request (which overrides the default for the pool):\n\n    .. code-block:: python\n\n       response = http.request(\'GET\', \'http://example.com/\', timeout=Timeout(10))\n\n    Timeouts can be disabled by setting all the parameters to ``None``:\n\n    .. code-block:: python\n\n       no_timeout = Timeout(connect=None, read=None)\n       response = http.request(\'GET\', \'http://example.com/, timeout=no_timeout)\n\n\n    :param total:\n        This combines the connect and read timeouts into one; the read timeout\n        will be set to the time leftover from the connect attempt. In the\n        event that both a connect timeout and a total are specified, or a read\n        timeout and a total are specified, the shorter timeout will be applied.\n\n        Defaults to None.\n\n    :type total: int, float, or None\n\n    :param connect:\n        The maximum amount of time (in seconds) to wait for a connection\n        attempt to a server to succeed. Omitting the parameter will default the\n        connect timeout to the system default, probably `the global default\n        timeout in socket.py\n        <http://hg.python.org/cpython/file/603b4d593758/Lib/socket.py#l535>`_.\n        None will set an infinite timeout for connection attempts.\n\n    :type connect: int, float, or None\n\n    :param read:\n        The maximum amount of time (in seconds) to wait between consecutive\n        read operations for a response from the server. Omitting the parameter\n        will default the read timeout to the system default, probably `the\n        global default timeout in socket.py\n        <http://hg.python.org/cpython/file/603b4d593758/Lib/socket.py#l535>`_.\n        None will set an infinite timeout.\n\n    :type read: int, float, or None\n\n    .. note::\n\n        Many factors can affect the total amount of time for urllib3 to return\n        an HTTP response.\n\n        For example, Python\'s DNS resolver does not obey the timeout specified\n        on the socket. Other factors that can affect total request time include\n        high CPU load, high swap, the program running at a low priority level,\n        or other behaviors.\n\n        In addition, the read and total timeouts only measure the time between\n        read operations on the socket connecting the client and the server,\n        not the total amount of time for the request to return a complete\n        response. For most requests, the timeout is raised because the server\n        has not sent the first byte in the specified time. This is not always\n        the case; if a server streams one byte every fifteen seconds, a timeout\n        of 20 seconds will not trigger, even though the request will take\n        several minutes to complete.\n\n        If your goal is to cut off any request after a set amount of wall clock\n        time, consider having a second "watcher" thread to cut off a slow\n        request.\n    '
    DEFAULT_TIMEOUT = _GLOBAL_DEFAULT_TIMEOUT

    def __init__(self, total=None, connect=_Default, read=_Default):
        self._connect = self._validate_timeout(connect, 'connect')
        self._read = self._validate_timeout(read, 'read')
        self.total = self._validate_timeout(total, 'total')
        self._start_connect = None

    def __repr__(self):
        return '%s(connect=%r, read=%r, total=%r)' % (
         type(self).__name__,
         self._connect,
         self._read,
         self.total)

    __str__ = __repr__

    @classmethod
    def _validate_timeout(cls, value, name):
        """Check that a timeout attribute is valid.

        :param value: The timeout value to validate
        :param name: The name of the timeout attribute to validate. This is
            used to specify in error messages.
        :return: The validated and casted version of the given value.
        :raises ValueError: If it is a numeric value less than or equal to
            zero, or the type is not an integer, float, or None.
        """
        if value is _Default:
            return cls.DEFAULT_TIMEOUT
        else:
            if value is None or value is cls.DEFAULT_TIMEOUT:
                return value
            else:
                if isinstance(value, bool):
                    raise ValueError('Timeout cannot be a boolean value. It must be an int, float or None.')
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise ValueError('Timeout value %s was %s, but it must be an int, float or None.' % (
                     name, value))

            try:
                if value <= 0:
                    raise ValueError('Attempted to set %s timeout to %s, but the timeout cannot be set to a value less than or equal to 0.' % (
                     name, value))
            except TypeError:
                raise ValueError('Timeout value %s was %s, but it must be an int, float or None.' % (
                 name, value))

            return value

    @classmethod
    def from_float(cls, timeout):
        """Create a new Timeout from a legacy timeout value.

        The timeout value used by httplib.py sets the same timeout on the
        connect(), and recv() socket requests. This creates a :class:`Timeout`
        object that sets the individual timeouts to the ``timeout`` value
        passed to this function.

        :param timeout: The legacy timeout value.
        :type timeout: integer, float, sentinel default object, or None
        :return: Timeout object
        :rtype: :class:`Timeout`
        """
        return Timeout(read=timeout, connect=timeout)

    def clone(self):
        """Create a copy of the timeout object

        Timeout properties are stored per-pool but each request needs a fresh
        Timeout object to ensure each one has its own start/stop configured.

        :return: a copy of the timeout object
        :rtype: :class:`Timeout`
        """
        return Timeout(connect=(self._connect), read=(self._read), total=(self.total))

    def start_connect(self):
        """Start the timeout clock, used during a connect() attempt

        :raises urllib3.exceptions.TimeoutStateError: if you attempt
            to start a timer that has been started already.
        """
        if self._start_connect is not None:
            raise TimeoutStateError('Timeout timer has already been started.')
        self._start_connect = current_time()
        return self._start_connect

    def get_connect_duration(self):
        """Gets the time elapsed since the call to :meth:`start_connect`.

        :return: Elapsed time in seconds.
        :rtype: float
        :raises urllib3.exceptions.TimeoutStateError: if you attempt
            to get duration for a timer that hasn't been started.
        """
        if self._start_connect is None:
            raise TimeoutStateError("Can't get connect duration for timer that has not started.")
        return current_time() - self._start_connect

    @property
    def connect_timeout(self):
        """Get the value to use when setting a connection timeout.

        This will be a positive float or integer, the value None
        (never timeout), or the default system timeout.

        :return: Connect timeout.
        :rtype: int, float, :attr:`Timeout.DEFAULT_TIMEOUT` or None
        """
        if self.total is None:
            return self._connect
        else:
            if self._connect is None or self._connect is self.DEFAULT_TIMEOUT:
                return self.total
            return min(self._connect, self.total)

    @property
    def read_timeout(self):
        """Get the value for the read timeout.

        This assumes some time has elapsed in the connection timeout and
        computes the read timeout appropriately.

        If self.total is set, the read timeout is dependent on the amount of
        time taken by the connect timeout. If the connection time has not been
        established, a :exc:`~urllib3.exceptions.TimeoutStateError` will be
        raised.

        :return: Value to use for the read timeout.
        :rtype: int, float, :attr:`Timeout.DEFAULT_TIMEOUT` or None
        :raises urllib3.exceptions.TimeoutStateError: If :meth:`start_connect`
            has not yet been called on this object.
        """
        if self.total is not None and self.total is not self.DEFAULT_TIMEOUT and self._read is not None and self._read is not self.DEFAULT_TIMEOUT:
            if self._start_connect is None:
                return self._read
            return max(0, min(self.total - self.get_connect_duration(), self._read))
        else:
            if self.total is not None:
                if self.total is not self.DEFAULT_TIMEOUT:
                    return max(0, self.total - self.get_connect_duration())
            return self._read