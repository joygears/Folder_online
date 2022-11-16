# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: win32com\server\dispatcher.py
"""Dispatcher

Please see policy.py for a discussion on dispatchers and policies
"""
import pythoncom, traceback, win32api
from sys import exc_info
from win32com.server.exception import IsCOMServerException
from win32com.util import IIDToInterfaceName
import win32com

class DispatcherBase:
    __doc__ = ' The base class for all Dispatchers.  \n\n      This dispatcher supports wrapping all operations in exception handlers, \n      and all the necessary delegation to the policy.\n\n      This base class supports the printing of "unexpected" exceptions.  Note, however,\n      that exactly where the output of print goes may not be useful!  A derived class may\n      provide additional semantics for this.\n  '

    def __init__(self, policyClass, object):
        self.policy = policyClass(object)
        self.logger = getattr(win32com, 'logger', None)

    def _CreateInstance_(self, clsid, reqIID):
        try:
            self.policy._CreateInstance_(clsid, reqIID)
            return pythoncom.WrapObject(self, reqIID)
        except:
            return self._HandleException_()

    def _QueryInterface_(self, iid):
        try:
            return self.policy._QueryInterface_(iid)
        except:
            return self._HandleException_()

    def _Invoke_(self, dispid, lcid, wFlags, args):
        try:
            return self.policy._Invoke_(dispid, lcid, wFlags, args)
        except:
            return self._HandleException_()

    def _GetIDsOfNames_(self, names, lcid):
        try:
            return self.policy._GetIDsOfNames_(names, lcid)
        except:
            return self._HandleException_()

    def _GetTypeInfo_(self, index, lcid):
        try:
            return self.policy._GetTypeInfo_(index, lcid)
        except:
            return self._HandleException_()

    def _GetTypeInfoCount_(self):
        try:
            return self.policy._GetTypeInfoCount_()
        except:
            return self._HandleException_()

    def _GetDispID_(self, name, fdex):
        try:
            return self.policy._GetDispID_(name, fdex)
        except:
            return self._HandleException_()

    def _InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
        try:
            return self.policy._InvokeEx_(dispid, lcid, wFlags, args, kwargs, serviceProvider)
        except:
            return self._HandleException_()

    def _DeleteMemberByName_(self, name, fdex):
        try:
            return self.policy._DeleteMemberByName_(name, fdex)
        except:
            return self._HandleException_()

    def _DeleteMemberByDispID_(self, id):
        try:
            return self.policy._DeleteMemberByDispID_(id)
        except:
            return self._HandleException_()

    def _GetMemberProperties_(self, id, fdex):
        try:
            return self.policy._GetMemberProperties_(id, fdex)
        except:
            return self._HandleException_()

    def _GetMemberName_(self, dispid):
        try:
            return self.policy._GetMemberName_(dispid)
        except:
            return self._HandleException_()

    def _GetNextDispID_(self, fdex, flags):
        try:
            return self.policy._GetNextDispID_(fdex, flags)
        except:
            return self._HandleException_()

    def _GetNameSpaceParent_(self):
        try:
            return self.policy._GetNameSpaceParent_()
        except:
            return self._HandleException_()

    def _HandleException_(self):
        """Called whenever an exception is raised.
 
       Default behaviour is to print the exception.
    """
        if not IsCOMServerException():
            if self.logger is not None:
                self.logger.exception('pythoncom server error')
            else:
                traceback.print_exc()
            raise

    def _trace_(self, *args):
        if self.logger is not None:
            record = ' '.join(map(str, args))
            self.logger.debug(record)
        else:
            for arg in args[:-1]:
                print(arg, end=' ')

            print(args[(-1)])


class DispatcherTrace(DispatcherBase):
    __doc__ = "A dispatcher, which causes a 'print' line for each COM function called.\n  "

    def _QueryInterface_(self, iid):
        rc = DispatcherBase._QueryInterface_(self, iid)
        if not rc:
            self._trace_('in %s._QueryInterface_ with unsupported IID %s (%s)' % (repr(self.policy._obj_), IIDToInterfaceName(iid), iid))
        return rc

    def _GetIDsOfNames_(self, names, lcid):
        self._trace_("in _GetIDsOfNames_ with '%s' and '%d'\n" % (names, lcid))
        return DispatcherBase._GetIDsOfNames_(self, names, lcid)

    def _GetTypeInfo_(self, index, lcid):
        self._trace_('in _GetTypeInfo_ with index=%d, lcid=%d\n' % (index, lcid))
        return DispatcherBase._GetTypeInfo_(self, index, lcid)

    def _GetTypeInfoCount_(self):
        self._trace_('in _GetTypeInfoCount_\n')
        return DispatcherBase._GetTypeInfoCount_(self)

    def _Invoke_(self, dispid, lcid, wFlags, args):
        self._trace_('in _Invoke_ with', dispid, lcid, wFlags, args)
        return DispatcherBase._Invoke_(self, dispid, lcid, wFlags, args)

    def _GetDispID_(self, name, fdex):
        self._trace_('in _GetDispID_ with', name, fdex)
        return DispatcherBase._GetDispID_(self, name, fdex)

    def _InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
        self._trace_('in %r._InvokeEx_-%s%r [%x,%s,%r]' % (self.policy._obj_, dispid, args, wFlags, lcid, serviceProvider))
        return DispatcherBase._InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider)

    def _DeleteMemberByName_(self, name, fdex):
        self._trace_('in _DeleteMemberByName_ with', name, fdex)
        return DispatcherBase._DeleteMemberByName_(self, name, fdex)

    def _DeleteMemberByDispID_(self, id):
        self._trace_('in _DeleteMemberByDispID_ with', id)
        return DispatcherBase._DeleteMemberByDispID_(self, id)

    def _GetMemberProperties_(self, id, fdex):
        self._trace_('in _GetMemberProperties_ with', id, fdex)
        return DispatcherBase._GetMemberProperties_(self, id, fdex)

    def _GetMemberName_(self, dispid):
        self._trace_('in _GetMemberName_ with', dispid)
        return DispatcherBase._GetMemberName_(self, dispid)

    def _GetNextDispID_(self, fdex, flags):
        self._trace_('in _GetNextDispID_ with', fdex, flags)
        return DispatcherBase._GetNextDispID_(self, fdex, flags)

    def _GetNameSpaceParent_(self):
        self._trace_('in _GetNameSpaceParent_')
        return DispatcherBase._GetNameSpaceParent_(self)


class DispatcherWin32trace(DispatcherTrace):
    __doc__ = 'A tracing dispatcher that sends its output to the win32trace remote collector.\n  \n  '

    def __init__(self, policyClass, object):
        DispatcherTrace.__init__(self, policyClass, object)
        if self.logger is None:
            import win32traceutil
        self._trace_('Object with win32trace dispatcher created (object=%s)' % repr(object))


class DispatcherOutputDebugString(DispatcherTrace):
    __doc__ = 'A tracing dispatcher that sends its output to win32api.OutputDebugString\n  \n  '

    def _trace_(self, *args):
        for arg in args[:-1]:
            win32api.OutputDebugString(str(arg) + ' ')

        win32api.OutputDebugString(str(args[(-1)]) + '\n')


class DispatcherWin32dbg(DispatcherBase):
    __doc__ = 'A source-level debugger dispatcher\n\n  A dispatcher which invokes the debugger as an object is instantiated, or \n  when an unexpected exception occurs.\n\n  Requires Pythonwin.\n  '

    def __init__(self, policyClass, ob):
        pywin.debugger.brk()
        print('The DispatcherWin32dbg dispatcher is deprecated!')
        print('Please let me know if this is a problem.')
        print('Uncomment the relevant lines in dispatcher.py to re-enable')
        DispatcherBase.__init__(self, policyClass, ob)

    def _HandleException_(self):
        """ Invoke the debugger post mortem capability """
        typ, val, tb = exc_info()
        debug = 0
        try:
            raise typ(val)
        except Exception:
            debug = pywin.debugger.GetDebugger().get_option(pywin.debugger.dbgcon.OPT_STOP_EXCEPTIONS)
        except:
            debug = 1

        if debug:
            try:
                pywin.debugger.post_mortem(tb, typ, val)
            except:
                traceback.print_exc()

        del tb
        raise


try:
    import win32trace
    DefaultDebugDispatcher = DispatcherWin32trace
except ImportError:
    DefaultDebugDispatcher = DispatcherTrace