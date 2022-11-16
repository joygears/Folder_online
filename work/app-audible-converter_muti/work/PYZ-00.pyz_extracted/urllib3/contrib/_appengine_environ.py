# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\contrib\_appengine_environ.py
"""
This module provides means to detect the App Engine environment.
"""
import os

def is_appengine():
    return is_local_appengine() or is_prod_appengine()


def is_appengine_sandbox():
    """Reports if the app is running in the first generation sandbox.

    The second generation runtimes are technically still in a sandbox, but it
    is much less restrictive, so generally you shouldn't need to check for it.
    see https://cloud.google.com/appengine/docs/standard/runtimes
    """
    return is_appengine() and os.environ['APPENGINE_RUNTIME'] == 'python27'


def is_local_appengine():
    return 'APPENGINE_RUNTIME' in os.environ and os.environ.get('SERVER_SOFTWARE', '').startswith('Development/')


def is_prod_appengine():
    return 'APPENGINE_RUNTIME' in os.environ and os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine/')


def is_prod_appengine_mvms():
    """Deprecated."""
    return False