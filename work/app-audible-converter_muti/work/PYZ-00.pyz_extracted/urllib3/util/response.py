# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\util\response.py
from __future__ import absolute_import
from email.errors import MultipartInvariantViolationDefect, StartBoundaryNotFoundDefect
from ..exceptions import HeaderParsingError
from ..packages.six.moves import http_client as httplib

def is_fp_closed(obj):
    """
    Checks whether a given file-like object is closed.

    :param obj:
        The file-like object to check.
    """
    try:
        return obj.isclosed()
    except AttributeError:
        pass

    try:
        return obj.closed
    except AttributeError:
        pass

    try:
        return obj.fp is None
    except AttributeError:
        pass

    raise ValueError('Unable to determine whether fp is closed.')


def assert_header_parsing(headers):
    """
    Asserts whether all headers have been successfully parsed.
    Extracts encountered errors from the result of parsing headers.

    Only works on Python 3.

    :param http.client.HTTPMessage headers: Headers to verify.

    :raises urllib3.exceptions.HeaderParsingError:
        If parsing errors are found.
    """
    if not isinstance(headers, httplib.HTTPMessage):
        raise TypeError('expected httplib.Message, got {0}.'.format(type(headers)))
    else:
        defects = getattr(headers, 'defects', None)
        get_payload = getattr(headers, 'get_payload', None)
        unparsed_data = None
        if get_payload:
            if not headers.is_multipart():
                payload = get_payload()
                if isinstance(payload, (bytes, str)):
                    unparsed_data = payload
        if defects:
            defects = [defect for defect in defects if not isinstance(defect, (StartBoundaryNotFoundDefect, MultipartInvariantViolationDefect))]
        if defects or unparsed_data:
            raise HeaderParsingError(defects=defects, unparsed_data=unparsed_data)


def is_response_to_head(response):
    """
    Checks whether the request of a response has been a HEAD-request.
    Handles the quirks of AppEngine.

    :param http.client.HTTPResponse response:
        Response to check if the originating request
        used 'HEAD' as a method.
    """
    method = response._method
    if isinstance(method, int):
        return method == 3
    else:
        return method.upper() == 'HEAD'