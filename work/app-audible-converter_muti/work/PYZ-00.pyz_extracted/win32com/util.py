# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: win32com\util.py
"""General utility functions common to client and server.

  This module contains a collection of general purpose utility functions.
"""
import pythoncom, win32api, win32con

def IIDToInterfaceName(iid):
    """Converts an IID to a string interface name.  
        
        Used primarily for debugging purposes, this allows a cryptic IID to
        be converted to a useful string name.  This will firstly look for interfaces
        known (ie, registered) by pythoncom.  If not known, it will look in the
        registry for a registered interface.

        iid -- An IID object.

        Result -- Always a string - either an interface name, or '<Unregistered interface>'
        """
    try:
        return pythoncom.ServerInterfaces[iid]
    except KeyError:
        try:
            try:
                return win32api.RegQueryValue(win32con.HKEY_CLASSES_ROOT, 'Interface\\%s' % iid)
            except win32api.error:
                pass

        except ImportError:
            pass

        return str(iid)