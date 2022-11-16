# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pywin\mfc\window.py
from . import object
import win32ui, win32con

class Wnd(object.CmdTarget):

    def __init__(self, initobj=None):
        object.CmdTarget.__init__(self, initobj)
        if self._obj_:
            self._obj_.HookMessage(self.OnDestroy, win32con.WM_DESTROY)

    def OnDestroy(self, msg):
        pass


class FrameWnd(Wnd):

    def __init__(self, wnd):
        Wnd.__init__(self, wnd)


class MDIChildWnd(FrameWnd):

    def __init__(self, wnd=None):
        if wnd is None:
            wnd = win32ui.CreateMDIChild()
        FrameWnd.__init__(self, wnd)

    def OnCreateClient(self, cp, context):
        if context is not None:
            if context.template is not None:
                context.template.CreateView(self, context)


class MDIFrameWnd(FrameWnd):

    def __init__(self, wnd=None):
        if wnd is None:
            wnd = win32ui.CreateMDIFrame()
        FrameWnd.__init__(self, wnd)