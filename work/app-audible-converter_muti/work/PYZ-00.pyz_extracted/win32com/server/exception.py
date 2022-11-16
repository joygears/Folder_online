# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: win32com\server\exception.py
"""Exception Handling

 Exceptions

         To better support COM exceptions, the framework allows for an instance to be
         raised.  This instance may have a certain number of known attributes, which are
         translated into COM exception details.
        
         This means, for example, that Python could raise a COM exception that includes details
         on a Help file and location, and a description for the user.
        
         This module provides a class which provides the necessary attributes.

"""
import sys, pythoncom

class COMException(pythoncom.com_error):
    __doc__ = 'An Exception object that is understood by the framework.\n\t\n\tIf the framework is presented with an exception of type class,\n\tit looks for certain known attributes on this class to provide rich\n\terror information to the caller.\n\n\tIt should be noted that the framework supports providing this error\n\tinformation via COM Exceptions, or via the ISupportErrorInfo interface.\n\n\tBy using this class, you automatically provide rich error information to the\n\tserver.\n\t'

    def __init__(self, description=None, scode=None, source=None, helpfile=None, helpContext=None, desc=None, hresult=None):
        """Initialize an exception
                **Params**

                description -- A string description for the exception.
                scode -- An integer scode to be returned to the server, if necessary.
                The pythoncom framework defaults this to be DISP_E_EXCEPTION if not specified otherwise.
                source -- A string which identifies the source of the error.
                helpfile -- A string which points to a help file which contains details on the error.
                helpContext -- An integer context in the help file.
                desc -- A short-cut for description.
                hresult -- A short-cut for scode.
                """
        scode = scode or hresult
        if scode:
            if scode != 1:
                if scode >= -32768:
                    if scode < 32768:
                        scode = -2147024896 | scode & 65535
        self.scode = scode
        self.description = description or desc
        if scode == 1:
            if not self.description:
                self.description = 'S_FALSE'
        if scode:
            if not self.description:
                self.description = pythoncom.GetScodeString(scode)
        self.source = source
        self.helpfile = helpfile
        self.helpcontext = helpContext
        pythoncom.com_error.__init__(self, scode, self.description, None, -1)

    def __repr__(self):
        return '<COM Exception - scode=%s, desc=%s>' % (self.scode, self.description)


Exception = COMException

def IsCOMException(t=None):
    if t is None:
        t = sys.exc_info()[0]
    try:
        return issubclass(t, pythoncom.com_error)
    except TypeError:
        return t is pythoncon.com_error


def IsCOMServerException(t=None):
    if t is None:
        t = sys.exc_info()[0]
    try:
        return issubclass(t, COMException)
    except TypeError:
        return 0