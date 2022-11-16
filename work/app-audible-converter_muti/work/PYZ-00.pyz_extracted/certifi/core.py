# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: certifi\core.py
"""
certifi.py
~~~~~~~~~~

This module returns the installation location of cacert.pem or its contents.
"""
import os
try:
    from importlib.resources import path as get_path, read_text
    _CACERT_CTX = None
    _CACERT_PATH = None

    def where():
        global _CACERT_CTX
        global _CACERT_PATH
        if _CACERT_PATH is None:
            _CACERT_CTX = get_path('certifi', 'cacert.pem')
            _CACERT_PATH = str(_CACERT_CTX.__enter__())
        return _CACERT_PATH


except ImportError:

    def read_text(_module, _path, encoding='ascii'):
        with open((where()), 'r', encoding=encoding) as (data):
            return data.read()


    def where():
        f = os.path.dirname(__file__)
        return os.path.join(f, 'cacert.pem')


def contents():
    return read_text('certifi', 'cacert.pem', encoding='ascii')