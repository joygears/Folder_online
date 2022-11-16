# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pywin\mfc\thread.py
from . import object
import win32ui

class WinThread(object.CmdTarget):

    def __init__(self, initObj=None):
        if initObj is None:
            initObj = win32ui.CreateThread()
        object.CmdTarget.__init__(self, initObj)

    def InitInstance(self):
        pass

    def ExitInstance(self):
        pass


class WinApp(WinThread):

    def __init__(self, initApp=None):
        if initApp is None:
            initApp = win32ui.GetApp()
        WinThread.__init__(self, initApp)