# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: decimal.py
try:
    from _decimal import *
    from _decimal import __doc__
    from _decimal import __version__
    from _decimal import __libmpdec_version__
except ImportError:
    from _pydecimal import *
    from _pydecimal import __doc__
    from _pydecimal import __version__
    from _pydecimal import __libmpdec_version__