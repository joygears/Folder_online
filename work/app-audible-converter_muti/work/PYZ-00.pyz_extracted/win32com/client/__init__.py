# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: win32com\client\__init__.py
import pythoncom
from . import dynamic
from . import gencache
import sys, pywintypes
_PyIDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]

def __WrapDispatch(dispatch, userName=None, resultCLSID=None, typeinfo=None, UnicodeToString=None, clsctx=pythoncom.CLSCTX_SERVER, WrapperClass=None):
    """
    Helper function to return a makepy generated class for a CLSID if it exists,
    otherwise cope by using CDispatch.
  """
    if not UnicodeToString is None:
        raise AssertionError('this is deprecated and will go away')
    else:
        if resultCLSID is None:
            try:
                typeinfo = dispatch.GetTypeInfo()
                if typeinfo is not None:
                    resultCLSID = str(typeinfo.GetTypeAttr()[0])
            except (pythoncom.com_error, AttributeError):
                pass

        if resultCLSID is not None:
            from . import gencache
            klass = gencache.GetClassForCLSID(resultCLSID)
            if klass is not None:
                return klass(dispatch)
        if WrapperClass is None:
            WrapperClass = CDispatch
    return dynamic.Dispatch(dispatch, userName, WrapperClass, typeinfo, clsctx=clsctx)


def GetObject(Pathname=None, Class=None, clsctx=None):
    """
    Mimic VB's GetObject() function.

    ob = GetObject(Class = "ProgID") or GetObject(Class = clsid) will
    connect to an already running instance of the COM object.
    
    ob = GetObject(r"c:\x08lah\x08lah\x0coo.xls") (aka the COM moniker syntax)
    will return a ready to use Python wrapping of the required COM object.

    Note: You must specifiy one or the other of these arguments. I know
    this isn't pretty, but it is what VB does. Blech. If you don't
    I'll throw ValueError at you. :)
    
    This will most likely throw pythoncom.com_error if anything fails.
  """
    if clsctx is None:
        clsctx = pythoncom.CLSCTX_ALL
    if Pathname is None and Class is None or Pathname is not None and Class is not None:
        raise ValueError('You must specify a value for Pathname or Class, but not both.')
    if Class is not None:
        return GetActiveObject(Class, clsctx)
    else:
        return Moniker(Pathname, clsctx)


def GetActiveObject(Class, clsctx=pythoncom.CLSCTX_ALL):
    """
    Python friendly version of GetObject's ProgID/CLSID functionality.
  """
    resultCLSID = pywintypes.IID(Class)
    dispatch = pythoncom.GetActiveObject(resultCLSID)
    dispatch = dispatch.QueryInterface(pythoncom.IID_IDispatch)
    return __WrapDispatch(dispatch, Class, resultCLSID=resultCLSID, clsctx=clsctx)


def Moniker(Pathname, clsctx=pythoncom.CLSCTX_ALL):
    """
    Python friendly version of GetObject's moniker functionality.
  """
    moniker, i, bindCtx = pythoncom.MkParseDisplayName(Pathname)
    dispatch = moniker.BindToObject(bindCtx, None, pythoncom.IID_IDispatch)
    return __WrapDispatch(dispatch, Pathname, clsctx=clsctx)


def Dispatch(dispatch, userName=None, resultCLSID=None, typeinfo=None, UnicodeToString=None, clsctx=pythoncom.CLSCTX_SERVER):
    """Creates a Dispatch based COM object.
  """
    assert UnicodeToString is None, 'this is deprecated and will go away'
    dispatch, userName = dynamic._GetGoodDispatchAndUserName(dispatch, userName, clsctx)
    return __WrapDispatch(dispatch, userName, resultCLSID, typeinfo, clsctx=clsctx)


def DispatchEx(clsid, machine=None, userName=None, resultCLSID=None, typeinfo=None, UnicodeToString=None, clsctx=None):
    """Creates a Dispatch based COM object on a specific machine.
  """
    if not UnicodeToString is None:
        raise AssertionError('this is deprecated and will go away')
    else:
        if clsctx is None:
            clsctx = pythoncom.CLSCTX_SERVER
            if machine is not None:
                clsctx = clsctx & ~pythoncom.CLSCTX_INPROC
        else:
            if machine is None:
                serverInfo = None
            else:
                serverInfo = (
                 machine,)
        if userName is None:
            userName = clsid
    dispatch = pythoncom.CoCreateInstanceEx(clsid, None, clsctx, serverInfo, (pythoncom.IID_IDispatch,))[0]
    return Dispatch(dispatch, userName, resultCLSID, typeinfo, clsctx=clsctx)


class CDispatch(dynamic.CDispatch):
    __doc__ = '\n    The dynamic class used as a last resort.\n    The purpose of this overriding of dynamic.CDispatch is to perpetuate the policy\n    of using the makepy generated wrapper Python class instead of dynamic.CDispatch\n    if/when possible.\n  '

    def _wrap_dispatch_(self, ob, userName=None, returnCLSID=None, UnicodeToString=None):
        assert UnicodeToString is None, 'this is deprecated and will go away'
        return Dispatch(ob, userName, returnCLSID, None)


def CastTo(ob, target, typelib=None):
    """'Cast' a COM object to another interface"""
    mod = None
    if typelib is not None:
        mod = gencache.MakeModuleForTypelib(typelib.clsid, typelib.lcid, int(typelib.major, 16), int(typelib.minor, 16))
        if not hasattr(mod, target):
            raise ValueError("The interface name '%s' does not appear in the specified library %r" % (
             target, typelib.ver_desc))
    else:
        if hasattr(target, 'index'):
            if 'CLSID' not in ob.__class__.__dict__:
                ob = gencache.EnsureDispatch(ob)
            else:
                if 'CLSID' not in ob.__class__.__dict__:
                    raise ValueError('Must be a makepy-able object for this to work')
                clsid = ob.CLSID
                mod = gencache.GetModuleForCLSID(clsid)
                mod = gencache.GetModuleForTypelib(mod.CLSID, mod.LCID, mod.MajorVersion, mod.MinorVersion)
                target_clsid = mod.NamesToIIDMap.get(target)
                if target_clsid is None:
                    raise ValueError("The interface name '%s' does not appear in the same library as object '%r'" % (
                     target, ob))
            mod = gencache.GetModuleForCLSID(target_clsid)
    if mod is not None:
        target_class = getattr(mod, target)
        target_class = getattr(target_class, 'default_interface', target_class)
        return target_class(ob)
    raise ValueError


class Constants:
    __doc__ = 'A container for generated COM constants.\n  '

    def __init__(self):
        self.__dicts__ = []

    def __getattr__(self, a):
        for d in self.__dicts__:
            if a in d:
                return d[a]

        raise AttributeError(a)


constants = Constants()

def _event_setattr_(self, attr, val):
    try:
        self.__class__.__bases__[0].__setattr__(self, attr, val)
    except AttributeError:
        self.__dict__[attr] = val


class EventsProxy:

    def __init__(self, ob):
        self.__dict__['_obj_'] = ob

    def __del__(self):
        try:
            self._obj_.close()
        except pythoncom.com_error:
            pass

    def __getattr__(self, attr):
        return getattr(self._obj_, attr)

    def __setattr__(self, attr, val):
        setattr(self._obj_, attr, val)


def DispatchWithEvents(clsid, user_event_class):
    """Create a COM object that can fire events to a user defined class.
  clsid -- The ProgID or CLSID of the object to create.
  user_event_class -- A Python class object that responds to the events.

  This requires makepy support for the COM object being created.  If
  this support does not exist it will be automatically generated by
  this function.  If the object does not support makepy, a TypeError
  exception will be raised.

  The result is a class instance that both represents the COM object
  and handles events from the COM object.

  It is important to note that the returned instance is not a direct
  instance of the user_event_class, but an instance of a temporary
  class object that derives from three classes:
  * The makepy generated class for the COM object
  * The makepy generated class for the COM events
  * The user_event_class as passed to this function.

  If this is not suitable, see the getevents function for an alternative
  technique of handling events.

  Object Lifetimes:  Whenever the object returned from this function is
  cleaned-up by Python, the events will be disconnected from
  the COM object.  This is almost always what should happen,
  but see the documentation for getevents() for more details.

  Example:

  >>> class IEEvents:
  ...    def OnVisible(self, visible):
  ...       print "Visible changed:", visible
  ...
  >>> ie = DispatchWithEvents("InternetExplorer.Application", IEEvents)
  >>> ie.Visible = 1
  Visible changed: 1
  >>> 
  """
    disp = Dispatch(clsid)
    if not disp.__class__.__dict__.get('CLSID'):
        try:
            ti = disp._oleobj_.GetTypeInfo()
            disp_clsid = ti.GetTypeAttr()[0]
            tlb, index = ti.GetContainingTypeLib()
            tla = tlb.GetLibAttr()
            gencache.EnsureModule((tla[0]), (tla[1]), (tla[3]), (tla[4]), bValidateFile=0)
            disp_class = gencache.GetClassForProgID(str(disp_clsid))
        except pythoncom.com_error:
            raise TypeError('This COM object can not automate the makepy process - please run makepy manually for this object')

    else:
        disp_class = disp.__class__
    clsid = disp_class.CLSID
    try:
        from types import ClassType as new_type
    except ImportError:
        new_type = type

    events_class = getevents(clsid)
    if events_class is None:
        raise ValueError('This COM object does not support events.')
    result_class = new_type('COMEventClass', (disp_class, events_class, user_event_class), {'__setattr__': _event_setattr_})
    instance = result_class(disp._oleobj_)
    events_class.__init__(instance, instance)
    if hasattr(user_event_class, '__init__'):
        user_event_class.__init__(instance)
    return EventsProxy(instance)


def WithEvents(disp, user_event_class):
    """Similar to DispatchWithEvents - except that the returned
  object is *not* also usable as the original Dispatch object - that is
  the returned object is not dispatchable.

  The difference is best summarised by example.

  >>> class IEEvents:
  ...    def OnVisible(self, visible):
  ...       print "Visible changed:", visible
  ...
  >>> ie = Dispatch("InternetExplorer.Application")
  >>> ie_events = WithEvents(ie, IEEvents)
  >>> ie.Visible = 1
  Visible changed: 1

  Compare with the code sample for DispatchWithEvents, where you get a
  single object that is both the interface and the event handler.  Note that
  the event handler instance will *not* be able to use 'self.' to refer to
  IE's methods and properties.

  This is mainly useful where using DispatchWithEvents causes
  circular reference problems that the simple proxy doesn't deal with
  """
    disp = Dispatch(disp)
    if not disp.__class__.__dict__.get('CLSID'):
        try:
            ti = disp._oleobj_.GetTypeInfo()
            disp_clsid = ti.GetTypeAttr()[0]
            tlb, index = ti.GetContainingTypeLib()
            tla = tlb.GetLibAttr()
            gencache.EnsureModule((tla[0]), (tla[1]), (tla[3]), (tla[4]), bValidateFile=0)
            disp_class = gencache.GetClassForProgID(str(disp_clsid))
        except pythoncom.com_error:
            raise TypeError('This COM object can not automate the makepy process - please run makepy manually for this object')

    else:
        disp_class = disp.__class__
    clsid = disp_class.CLSID
    try:
        from types import ClassType as new_type
    except ImportError:
        new_type = type

    events_class = getevents(clsid)
    if events_class is None:
        raise ValueError('This COM object does not support events.')
    result_class = new_type('COMEventClass', (events_class, user_event_class), {})
    instance = result_class(disp)
    if hasattr(user_event_class, '__init__'):
        user_event_class.__init__(instance)
    return instance


def getevents(clsid):
    """Determine the default outgoing interface for a class, given
    either a clsid or progid. It returns a class - you can
    conveniently derive your own handler from this class and implement
    the appropriate methods.

    This method relies on the classes produced by makepy. You must use
    either makepy or the gencache module to ensure that the
    appropriate support classes have been generated for the com server
    that you will be handling events from.

    Beware of COM circular references.  When the Events class is connected
    to the COM object, the COM object itself keeps a reference to the Python
    events class.  Thus, neither the Events instance or the COM object will
    ever die by themselves.  The 'close' method on the events instance
    must be called to break this chain and allow standard Python collection
    rules to manage object lifetimes.  Note that DispatchWithEvents() does
    work around this problem by the use of a proxy object, but if you use
    the getevents() function yourself, you must make your own arrangements
    to manage this circular reference issue.

    Beware of creating Python circular references: this will happen if your
    handler has a reference to an object that has a reference back to
    the event source. Call the 'close' method to break the chain.
    
    Example:

    >>>win32com.client.gencache.EnsureModule('{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}',0,1,1)
    <module 'win32com.gen_py.....
    >>>
    >>> class InternetExplorerEvents(win32com.client.getevents("InternetExplorer.Application.1")):
    ...    def OnVisible(self, Visible):
    ...        print "Visibility changed: ", Visible
    ...
    >>>
    >>> ie=win32com.client.Dispatch("InternetExplorer.Application.1")
    >>> events=InternetExplorerEvents(ie) 
    >>> ie.Visible=1
    Visibility changed:  1
    >>>
    """
    clsid = str(pywintypes.IID(clsid))
    klass = gencache.GetClassForCLSID(clsid)
    try:
        return klass.default_source
    except AttributeError:
        try:
            return gencache.GetClassForCLSID(klass.coclass_clsid).default_source
        except AttributeError:
            return


def Record(name, object):
    """Creates a new record object, given the name of the record,
  and an object from the same type library.

  Example usage would be:
    app = win32com.client.Dispatch("Some.Application")
    point = win32com.client.Record("SomeAppPoint", app)
    point.x = 0
    point.y = 0
    app.MoveTo(point)
  """
    from . import gencache
    object = gencache.EnsureDispatch(object)
    module = sys.modules[object.__class__.__module__]
    package = gencache.GetModuleForTypelib(module.CLSID, module.LCID, module.MajorVersion, module.MinorVersion)
    try:
        struct_guid = package.RecordMap[name]
    except KeyError:
        raise ValueError("The structure '%s' is not defined in module '%s'" % (name, package))

    return pythoncom.GetRecordFromGuids(module.CLSID, module.MajorVersion, module.MinorVersion, module.LCID, struct_guid)


class DispatchBaseClass:

    def __init__(self, oobj=None):
        if oobj is None:
            oobj = pythoncom.new(self.CLSID)
        else:
            if isinstance(oobj, DispatchBaseClass):
                try:
                    oobj = oobj._oleobj_.QueryInterface(self.CLSID, pythoncom.IID_IDispatch)
                except pythoncom.com_error as details:
                    import winerror
                    if details.hresult != winerror.E_NOINTERFACE:
                        raise
                    oobj = oobj._oleobj_

        self.__dict__['_oleobj_'] = oobj

    def __repr__(self):
        try:
            mod_doc = sys.modules[self.__class__.__module__].__doc__
            if mod_doc:
                mod_name = 'win32com.gen_py.' + mod_doc
            else:
                mod_name = sys.modules[self.__class__.__module__].__name__
        except KeyError:
            mod_name = 'win32com.gen_py.unknown'

        return '<%s.%s instance at 0x%s>' % (mod_name, self.__class__.__name__, id(self))

    def __eq__(self, other):
        other = getattr(other, '_oleobj_', other)
        return self._oleobj_ == other

    def __ne__(self, other):
        other = getattr(other, '_oleobj_', other)
        return self._oleobj_ != other

    def _ApplyTypes_(self, dispid, wFlags, retType, argTypes, user, resultCLSID, *args):
        return self._get_good_object_((self._oleobj_.InvokeTypes)(dispid, 0, wFlags, retType, argTypes, *args), user, resultCLSID)

    def __getattr__(self, attr):
        args = self._prop_map_get_.get(attr)
        if args is None:
            raise AttributeError("'%s' object has no attribute '%s'" % (repr(self), attr))
        return (self._ApplyTypes_)(*args)

    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            self.__dict__[attr] = value
            return
        try:
            args, defArgs = self._prop_map_put_[attr]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" % (repr(self), attr))

        (self._oleobj_.Invoke)(*args + (value,) + defArgs)

    def _get_good_single_object_(self, obj, obUserName=None, resultCLSID=None):
        return _get_good_single_object_(obj, obUserName, resultCLSID)

    def _get_good_object_(self, obj, obUserName=None, resultCLSID=None):
        return _get_good_object_(obj, obUserName, resultCLSID)


def _get_good_single_object_(obj, obUserName=None, resultCLSID=None):
    if _PyIDispatchType == type(obj):
        return Dispatch(obj, obUserName, resultCLSID)
    else:
        return obj


def _get_good_object_(obj, obUserName=None, resultCLSID=None):
    if obj is None:
        return
    else:
        if isinstance(obj, tuple):
            obUserNameTuple = (
             obUserName,) * len(obj)
            resultCLSIDTuple = (resultCLSID,) * len(obj)
            return tuple(map(_get_good_object_, obj, obUserNameTuple, resultCLSIDTuple))
        return _get_good_single_object_(obj, obUserName, resultCLSID)


class CoClassBaseClass:

    def __init__(self, oobj=None):
        if oobj is None:
            oobj = pythoncom.new(self.CLSID)
        self.__dict__['_dispobj_'] = self.default_interface(oobj)

    def __repr__(self):
        return '<win32com.gen_py.%s.%s>' % (__doc__, self.__class__.__name__)

    def __getattr__(self, attr):
        d = self.__dict__['_dispobj_']
        if d is not None:
            return getattr(d, attr)
        raise AttributeError(attr)

    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            self.__dict__[attr] = value
            return
        try:
            d = self.__dict__['_dispobj_']
            if d is not None:
                d.__setattr__(attr, value)
                return
        except AttributeError:
            pass

        self.__dict__[attr] = value


class VARIANT(object):

    def __init__(self, vt, value):
        self.varianttype = vt
        self._value = value

    def _get_value(self):
        return self._value

    def _set_value(self, newval):
        self._value = _get_good_object_(newval)

    def _del_value(self):
        del self._value

    value = property(_get_value, _set_value, _del_value)

    def __repr__(self):
        return 'win32com.client.VARIANT(%r, %r)' % (self.varianttype, self._value)