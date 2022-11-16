# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: win32com\client\dynamic.py
"""Support for dynamic COM client support.

Introduction
 Dynamic COM client support is the ability to use a COM server without
 prior knowledge of the server.  This can be used to talk to almost all
 COM servers, including much of MS Office.
 
 In general, you should not use this module directly - see below.
 
Example
 >>> import win32com.client
 >>> xl = win32com.client.Dispatch("Excel.Application")
 # The line above invokes the functionality of this class.
 # xl is now an object we can use to talk to Excel.
 >>> xl.Visible = 1 # The Excel window becomes visible.

"""
import sys, traceback, types, pythoncom, winerror
from . import build
from pywintypes import IIDType
import win32com.client
debugging = 0
debugging_attr = 0
LCID = 0
ERRORS_BAD_CONTEXT = [
 winerror.DISP_E_MEMBERNOTFOUND,
 winerror.DISP_E_BADPARAMCOUNT,
 winerror.DISP_E_PARAMNOTOPTIONAL,
 winerror.DISP_E_TYPEMISMATCH,
 winerror.E_INVALIDARG]
ALL_INVOKE_TYPES = [
 pythoncom.INVOKE_PROPERTYGET,
 pythoncom.INVOKE_PROPERTYPUT,
 pythoncom.INVOKE_PROPERTYPUTREF,
 pythoncom.INVOKE_FUNC]

def debug_print(*args):
    if debugging:
        for arg in args:
            print(arg, end=' ')

        print()


def debug_attr_print(*args):
    if debugging_attr:
        for arg in args:
            print(arg, end=' ')

        print()


py3k = sys.version_info > (3, 0)
if py3k:

    def MakeMethod(func, inst, cls):
        return types.MethodType(func, inst)


else:
    MakeMethod = types.MethodType
PyIDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]
PyIUnknownType = pythoncom.TypeIIDs[pythoncom.IID_IUnknown]
if py3k:
    _GoodDispatchTypes = (
     str, IIDType)
else:
    _GoodDispatchTypes = (
     str, IIDType, str)
_defaultDispatchItem = build.DispatchItem

def _GetGoodDispatch(IDispatch, clsctx=pythoncom.CLSCTX_SERVER):
    if isinstance(IDispatch, PyIDispatchType):
        return IDispatch
    else:
        if isinstance(IDispatch, _GoodDispatchTypes):
            try:
                IDispatch = pythoncom.connect(IDispatch)
            except pythoncom.ole_error:
                IDispatch = pythoncom.CoCreateInstance(IDispatch, None, clsctx, pythoncom.IID_IDispatch)

        else:
            IDispatch = getattr(IDispatch, '_oleobj_', IDispatch)
        return IDispatch


def _GetGoodDispatchAndUserName(IDispatch, userName, clsctx):
    if userName is None:
        if isinstance(IDispatch, str):
            userName = IDispatch
        elif not py3k:
            if isinstance(IDispatch, str):
                userName = IDispatch.encode('ascii', 'replace')
    elif not py3k:
        if isinstance(userName, str):
            userName = userName.encode('ascii', 'replace')
    else:
        userName = str(userName)
    return (
     _GetGoodDispatch(IDispatch, clsctx), userName)


def _GetDescInvokeType(entry, invoke_type):
    if not entry or not entry.desc:
        return invoke_type
    else:
        varkind = entry.desc[4]
        if varkind == pythoncom.VAR_DISPATCH:
            if invoke_type == pythoncom.INVOKE_PROPERTYGET:
                return pythoncom.INVOKE_FUNC | invoke_type
        return varkind


def Dispatch(IDispatch, userName=None, createClass=None, typeinfo=None, UnicodeToString=None, clsctx=pythoncom.CLSCTX_SERVER):
    if not UnicodeToString is None:
        raise AssertionError('this is deprecated and will go away')
    else:
        IDispatch, userName = _GetGoodDispatchAndUserName(IDispatch, userName, clsctx)
        if createClass is None:
            createClass = CDispatch
        lazydata = None
        try:
            if typeinfo is None:
                typeinfo = IDispatch.GetTypeInfo()
            if typeinfo is not None:
                try:
                    typecomp = typeinfo.GetTypeComp()
                    lazydata = (typeinfo, typecomp)
                except pythoncom.com_error:
                    pass

        except pythoncom.com_error:
            typeinfo = None

    olerepr = MakeOleRepr(IDispatch, typeinfo, lazydata)
    return createClass(IDispatch, olerepr, userName, lazydata=lazydata)


def MakeOleRepr(IDispatch, typeinfo, typecomp):
    olerepr = None
    if typeinfo is not None:
        try:
            attr = typeinfo.GetTypeAttr()
            if attr[5] == pythoncom.TKIND_INTERFACE:
                if attr[11] & pythoncom.TYPEFLAG_FDUAL:
                    href = typeinfo.GetRefTypeOfImplType(-1)
                    typeinfo = typeinfo.GetRefTypeInfo(href)
                    attr = typeinfo.GetTypeAttr()
            if typecomp is None:
                olerepr = build.DispatchItem(typeinfo, attr, None, 0)
            else:
                olerepr = build.LazyDispatchItem(attr, None)
        except pythoncom.ole_error:
            pass

    if olerepr is None:
        olerepr = build.DispatchItem()
    return olerepr


def DumbDispatch(IDispatch, userName=None, createClass=None, UnicodeToString=None, clsctx=pythoncom.CLSCTX_SERVER):
    """Dispatch with no type info"""
    assert UnicodeToString is None, 'this is deprecated and will go away'
    IDispatch, userName = _GetGoodDispatchAndUserName(IDispatch, userName, clsctx)
    if createClass is None:
        createClass = CDispatch
    return createClass(IDispatch, build.DispatchItem(), userName)


class CDispatch:

    def __init__(self, IDispatch, olerepr, userName=None, UnicodeToString=None, lazydata=None):
        assert UnicodeToString is None, 'this is deprecated and will go away'
        if userName is None:
            userName = '<unknown>'
        self.__dict__['_oleobj_'] = IDispatch
        self.__dict__['_username_'] = userName
        self.__dict__['_olerepr_'] = olerepr
        self.__dict__['_mapCachedItems_'] = {}
        self.__dict__['_builtMethods_'] = {}
        self.__dict__['_enum_'] = None
        self.__dict__['_unicode_to_string_'] = None
        self.__dict__['_lazydata_'] = lazydata

    def __call__(self, *args):
        """Provide 'default dispatch' COM functionality - allow instance to be called"""
        if self._olerepr_.defaultDispatchName:
            invkind, dispid = self._find_dispatch_type_(self._olerepr_.defaultDispatchName)
        else:
            invkind, dispid = pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET, pythoncom.DISPID_VALUE
        if invkind is not None:
            allArgs = (
             dispid, LCID, invkind, 1) + args
            return self._get_good_object_((self._oleobj_.Invoke)(*allArgs), self._olerepr_.defaultDispatchName, None)
        raise TypeError('This dispatch object does not define a default method')

    def __bool__(self):
        return True

    def __repr__(self):
        return '<COMObject %s>' % self._username_

    def __str__(self):
        try:
            return str(self.__call__())
        except pythoncom.com_error as details:
            if details.hresult not in ERRORS_BAD_CONTEXT:
                raise
            return self.__repr__()

    def __eq__(self, other):
        other = getattr(other, '_oleobj_', other)
        return self._oleobj_ == other

    def __ne__(self, other):
        other = getattr(other, '_oleobj_', other)
        return self._oleobj_ != other

    def __int__(self):
        return int(self.__call__())

    def __len__(self):
        invkind, dispid = self._find_dispatch_type_('Count')
        if invkind:
            return self._oleobj_.Invoke(dispid, LCID, invkind, 1)
        raise TypeError('This dispatch object does not define a Count method')

    def _NewEnum(self):
        try:
            invkind = pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET
            enum = self._oleobj_.InvokeTypes(pythoncom.DISPID_NEWENUM, LCID, invkind, (13,
                                                                                       10), ())
        except pythoncom.com_error:
            return
        else:
            from . import util
            return util.WrapEnum(enum, None)

    def __getitem__(self, index):
        if isinstance(index, int):
            if self.__dict__['_enum_'] is None:
                self.__dict__['_enum_'] = self._NewEnum()
            if self.__dict__['_enum_'] is not None:
                return self._get_good_object_(self._enum_.__getitem__(index))
        invkind, dispid = self._find_dispatch_type_('Item')
        if invkind is not None:
            return self._get_good_object_(self._oleobj_.Invoke(dispid, LCID, invkind, 1, index))
        raise TypeError('This object does not support enumeration')

    def __setitem__(self, index, *args):
        if self._olerepr_.defaultDispatchName:
            invkind, dispid = self._find_dispatch_type_(self._olerepr_.defaultDispatchName)
        else:
            invkind, dispid = pythoncom.DISPATCH_PROPERTYPUT | pythoncom.DISPATCH_PROPERTYPUTREF, pythoncom.DISPID_VALUE
        if invkind is not None:
            allArgs = (
             dispid, LCID, invkind, 0, index) + args
            return self._get_good_object_((self._oleobj_.Invoke)(*allArgs), self._olerepr_.defaultDispatchName, None)
        raise TypeError('This dispatch object does not define a default method')

    def _find_dispatch_type_(self, methodName):
        if methodName in self._olerepr_.mapFuncs:
            item = self._olerepr_.mapFuncs[methodName]
            return (
             item.desc[4], item.dispid)
        else:
            if methodName in self._olerepr_.propMapGet:
                item = self._olerepr_.propMapGet[methodName]
                return (item.desc[4], item.dispid)
            try:
                dispid = self._oleobj_.GetIDsOfNames(0, methodName)
            except:
                return (None, None)

            return (
             pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET, dispid)

    def _ApplyTypes_(self, dispid, wFlags, retType, argTypes, user, resultCLSID, *args):
        result = (self._oleobj_.InvokeTypes)(*(dispid, LCID, wFlags, retType, argTypes) + args)
        return self._get_good_object_(result, user, resultCLSID)

    def _wrap_dispatch_(self, ob, userName=None, returnCLSID=None, UnicodeToString=None):
        assert UnicodeToString is None, 'this is deprecated and will go away'
        return Dispatch(ob, userName)

    def _get_good_single_object_(self, ob, userName=None, ReturnCLSID=None):
        if isinstance(ob, PyIDispatchType):
            return self._wrap_dispatch_(ob, userName, ReturnCLSID)
        else:
            if isinstance(ob, PyIUnknownType):
                try:
                    ob = ob.QueryInterface(pythoncom.IID_IDispatch)
                except pythoncom.com_error:
                    return ob
                else:
                    return self._wrap_dispatch_(ob, userName, ReturnCLSID)
            return ob

    def _get_good_object_(self, ob, userName=None, ReturnCLSID=None):
        """Given an object (usually the retval from a method), make it a good object to return.
                   Basically checks if it is a COM object, and wraps it up.
                   Also handles the fact that a retval may be a tuple of retvals"""
        if ob is None:
            return
        else:
            if isinstance(ob, tuple):
                return tuple(map(lambda o, s=self, oun=userName, rc=ReturnCLSID: s._get_good_single_object_(o, oun, rc), ob))
            return self._get_good_single_object_(ob)

    def _make_method_(self, name):
        """Make a method object - Assumes in olerepr funcmap"""
        methodName = build.MakePublicAttributeName(name)
        methodCodeList = self._olerepr_.MakeFuncMethod(self._olerepr_.mapFuncs[name], methodName, 0)
        methodCode = '\n'.join(methodCodeList)
        try:
            codeObject = compile(methodCode, '<COMObject %s>' % self._username_, 'exec')
            tempNameSpace = {}
            globNameSpace = globals().copy()
            globNameSpace['Dispatch'] = win32com.client.Dispatch
            exec(codeObject, globNameSpace, tempNameSpace)
            name = methodName
            fn = self._builtMethods_[name] = tempNameSpace[name]
            newMeth = MakeMethod(fn, self, self.__class__)
            return newMeth
        except:
            debug_print('Error building OLE definition for code ', methodCode)
            traceback.print_exc()

    def _Release_(self):
        """Cleanup object - like a close - to force cleanup when you dont 
                   want to rely on Python's reference counting."""
        for childCont in self._mapCachedItems_.values():
            childCont._Release_()

        self._mapCachedItems_ = {}
        if self._oleobj_:
            self._oleobj_.Release()
            self.__dict__['_oleobj_'] = None
        if self._olerepr_:
            self.__dict__['_olerepr_'] = None
        self._enum_ = None

    def _proc_(self, name, *args):
        """Call the named method as a procedure, rather than function.
                   Mainly used by Word.Basic, which whinges about such things."""
        try:
            item = self._olerepr_.mapFuncs[name]
            dispId = item.dispid
            return self._get_good_object_((self._oleobj_.Invoke)(*(dispId, LCID, item.desc[4], 0) + args))
        except KeyError:
            raise AttributeError(name)

    def _print_details_(self):
        """Debug routine - dumps what it knows about an object."""
        print('AxDispatch container', self._username_)
        try:
            print('Methods:')
            for method in self._olerepr_.mapFuncs.keys():
                print('\t', method)

            print('Props:')
            for prop, entry in self._olerepr_.propMap.items():
                print('\t%s = 0x%x - %s' % (prop, entry.dispid, repr(entry)))

            print('Get Props:')
            for prop, entry in self._olerepr_.propMapGet.items():
                print('\t%s = 0x%x - %s' % (prop, entry.dispid, repr(entry)))

            print('Put Props:')
            for prop, entry in self._olerepr_.propMapPut.items():
                print('\t%s = 0x%x - %s' % (prop, entry.dispid, repr(entry)))

        except:
            traceback.print_exc()

    def __LazyMap__(self, attr):
        try:
            if self._LazyAddAttr_(attr):
                debug_attr_print('%s.__LazyMap__(%s) added something' % (self._username_, attr))
                return 1
        except AttributeError:
            return 0

    def _LazyAddAttr_(self, attr):
        if self._lazydata_ is None:
            return 0
        else:
            res = 0
            typeinfo, typecomp = self._lazydata_
            olerepr = self._olerepr_
            for i in ALL_INVOKE_TYPES:
                try:
                    x, t = typecomp.Bind(attr, i)
                    if x == 0:
                        if attr[:3] in ('Set', 'Get'):
                            x, t = typecomp.Bind(attr[3:], i)
                    if x == 1:
                        r = olerepr._AddFunc_(typeinfo, t, 0)
                    else:
                        if x == 2:
                            r = olerepr._AddVar_(typeinfo, t, 0)
                        else:
                            r = None
                    if r is not None:
                        key, map = r[0], r[1]
                        item = map[key]
                        if map == olerepr.propMapPut:
                            olerepr._propMapPutCheck_(key, item)
                        elif map == olerepr.propMapGet:
                            olerepr._propMapGetCheck_(key, item)
                        res = 1
                except:
                    pass

            return res

    def _FlagAsMethod(self, *methodNames):
        """Flag these attribute names as being methods.
                Some objects do not correctly differentiate methods and
                properties, leading to problems when calling these methods.

                Specifically, trying to say: ob.SomeFunc()
                may yield an exception "None object is not callable"
                In this case, an attempt to fetch the *property*has worked
                and returned None, rather than indicating it is really a method.
                Calling: ob._FlagAsMethod("SomeFunc")
                should then allow this to work.
                """
        for name in methodNames:
            details = build.MapEntry(self.__AttrToID__(name), (name,))
            self._olerepr_.mapFuncs[name] = details

    def __AttrToID__(self, attr):
        debug_attr_print('Calling GetIDsOfNames for property %s in Dispatch container %s' % (attr, self._username_))
        return self._oleobj_.GetIDsOfNames(0, attr)

    def __getattr__(self, attr):
        if attr == '__iter__':
            try:
                invkind = pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET
                enum = self._oleobj_.InvokeTypes(pythoncom.DISPID_NEWENUM, LCID, invkind, (13,
                                                                                           10), ())
            except pythoncom.com_error:
                raise AttributeError('This object can not function as an iterator')

            class Factory:

                def __init__(self, ob):
                    self.ob = ob

                def __call__(self):
                    import win32com.client.util
                    return win32com.client.util.Iterator(self.ob)

            return Factory(enum)
        else:
            if attr.startswith('_'):
                if attr.endswith('_'):
                    raise AttributeError(attr)
                else:
                    try:
                        return MakeMethod(self._builtMethods_[attr], self, self.__class__)
                    except KeyError:
                        pass

                    if attr in self._olerepr_.mapFuncs:
                        return self._make_method_(attr)
                    retEntry = None
                    if self._olerepr_ and self._oleobj_:
                        retEntry = self._olerepr_.propMap.get(attr)
                        if retEntry is None:
                            retEntry = self._olerepr_.propMapGet.get(attr)
                        if retEntry is None:
                            try:
                                if self.__LazyMap__(attr):
                                    if attr in self._olerepr_.mapFuncs:
                                        return self._make_method_(attr)
                                    retEntry = self._olerepr_.propMap.get(attr)
                                    if retEntry is None:
                                        retEntry = self._olerepr_.propMapGet.get(attr)
                                if retEntry is None:
                                    retEntry = build.MapEntry(self.__AttrToID__(attr), (attr,))
                            except pythoncom.ole_error:
                                pass

            else:
                if retEntry is not None:
                    try:
                        ret = self._mapCachedItems_[retEntry.dispid]
                        debug_attr_print('Cached items has attribute!', ret)
                        return ret
                    except (KeyError, AttributeError):
                        debug_attr_print('Attribute %s not in cache' % attr)

            if retEntry is not None:
                invoke_type = _GetDescInvokeType(retEntry, pythoncom.INVOKE_PROPERTYGET)
                debug_attr_print('Getting property Id 0x%x from OLE object' % retEntry.dispid)
                try:
                    ret = self._oleobj_.Invoke(retEntry.dispid, 0, invoke_type, 1)
                except pythoncom.com_error as details:
                    if details.hresult in ERRORS_BAD_CONTEXT:
                        self._olerepr_.mapFuncs[attr] = retEntry
                        return self._make_method_(attr)
                    raise

                debug_attr_print('OLE returned ', ret)
                return self._get_good_object_(ret)
        raise AttributeError('%s.%s' % (self._username_, attr))

    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            self.__dict__[attr] = value
            return
        else:
            debug_attr_print('SetAttr called for %s.%s=%s on DispatchContainer' % (self._username_, attr, repr(value)))
            if self._olerepr_:
                if attr in self._olerepr_.propMap:
                    entry = self._olerepr_.propMap[attr]
                    invoke_type = _GetDescInvokeType(entry, pythoncom.INVOKE_PROPERTYPUT)
                    self._oleobj_.Invoke(entry.dispid, 0, invoke_type, 0, value)
                    return
                if attr in self._olerepr_.propMapPut:
                    entry = self._olerepr_.propMapPut[attr]
                    invoke_type = _GetDescInvokeType(entry, pythoncom.INVOKE_PROPERTYPUT)
                    self._oleobj_.Invoke(entry.dispid, 0, invoke_type, 0, value)
                    return
            if self._oleobj_:
                if self.__LazyMap__(attr):
                    if attr in self._olerepr_.propMap:
                        entry = self._olerepr_.propMap[attr]
                        invoke_type = _GetDescInvokeType(entry, pythoncom.INVOKE_PROPERTYPUT)
                        self._oleobj_.Invoke(entry.dispid, 0, invoke_type, 0, value)
                        return
                    if attr in self._olerepr_.propMapPut:
                        entry = self._olerepr_.propMapPut[attr]
                        invoke_type = _GetDescInvokeType(entry, pythoncom.INVOKE_PROPERTYPUT)
                        self._oleobj_.Invoke(entry.dispid, 0, invoke_type, 0, value)
                        return
                try:
                    entry = build.MapEntry(self.__AttrToID__(attr), (attr,))
                except pythoncom.com_error:
                    entry = None

                if entry is not None:
                    try:
                        invoke_type = _GetDescInvokeType(entry, pythoncom.INVOKE_PROPERTYPUT)
                        self._oleobj_.Invoke(entry.dispid, 0, invoke_type, 0, value)
                        self._olerepr_.propMap[attr] = entry
                        debug_attr_print('__setattr__ property %s (id=0x%x) in Dispatch container %s' % (attr, entry.dispid, self._username_))
                        return
                    except pythoncom.com_error:
                        pass

        raise AttributeError("Property '%s.%s' can not be set." % (self._username_, attr))