# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\__init__.py
"""
Python HTTP library with thread-safe connection pooling, file post support, user friendly, and more
"""
from __future__ import absolute_import
import logging, warnings
from logging import NullHandler
from . import exceptions
from ._version import __version__
from .connectionpool import HTTPConnectionPool, HTTPSConnectionPool, connection_from_url
from .filepost import encode_multipart_formdata
from .poolmanager import PoolManager, ProxyManager, proxy_from_url
from .response import HTTPResponse
from .util.request import make_headers
from .util.retry import Retry
from .util.timeout import Timeout
from .util.url import get_host
__author__ = 'Andrey Petrov (andrey.petrov@shazow.net)'
__license__ = 'MIT'
__version__ = __version__
__all__ = ('HTTPConnectionPool', 'HTTPSConnectionPool', 'PoolManager', 'ProxyManager',
           'HTTPResponse', 'Retry', 'Timeout', 'add_stderr_logger', 'connection_from_url',
           'disable_warnings', 'encode_multipart_formdata', 'get_host', 'make_headers',
           'proxy_from_url')
logging.getLogger(__name__).addHandler(NullHandler())

def add_stderr_logger(level=logging.DEBUG):
    """
    Helper for quickly adding a StreamHandler to the logger. Useful for
    debugging.

    Returns the handler after adding it.
    """
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.debug('Added a stderr logging handler to logger: %s', __name__)
    return handler


del NullHandler
warnings.simplefilter('always', (exceptions.SecurityWarning), append=True)
warnings.simplefilter('default', (exceptions.SubjectAltNameWarning), append=True)
warnings.simplefilter('default', (exceptions.InsecurePlatformWarning), append=True)
warnings.simplefilter('default', (exceptions.SNIMissingWarning), append=True)

def disable_warnings(category=exceptions.HTTPWarning):
    """
    Helper for quickly disabling all urllib3 warnings.
    """
    warnings.simplefilter('ignore', category)