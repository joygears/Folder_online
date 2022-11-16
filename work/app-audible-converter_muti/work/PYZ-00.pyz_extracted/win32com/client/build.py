# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: win32com\client\build.py
"""Contains knowledge to build a COM object definition.

This module is used by both the @dynamic@ and @makepy@ modules to build
all knowledge of a COM object.

This module contains classes which contain the actual knowledge of the object.
This include parameter and return type information, the COM dispid and CLSID, etc.

Other modules may use this information to generate .py files, use the information
dynamically, or possibly even generate .html documentation for objects.
"""
import sys, string
from keyword import iskeyword
import pythoncom
from pywintypes import TimeType
import winerror, datetime

def _makeDocString(s):
    if sys.version_info < (3, ):
        s = s.encode('mbcs')
    return repr(s)


error = 'PythonCOM.Client.Build error'

class NotSupportedException(Exception):
    pass


DropIndirection = 'DropIndirection'
NoTranslateTypes = [
 pythoncom.VT_BOOL, pythoncom.VT_CLSID, pythoncom.VT_CY,
 pythoncom.VT_DATE, pythoncom.VT_DECIMAL, pythoncom.VT_EMPTY,
 pythoncom.VT_ERROR, pythoncom.VT_FILETIME, pythoncom.VT_HRESULT,
 pythoncom.VT_I1, pythoncom.VT_I2, pythoncom.VT_I4,
 pythoncom.VT_I8, pythoncom.VT_INT, pythoncom.VT_NULL,
 pythoncom.VT_R4, pythoncom.VT_R8, pythoncom.VT_NULL,
 pythoncom.VT_STREAM,
 pythoncom.VT_UI1, pythoncom.VT_UI2, pythoncom.VT_UI4,
 pythoncom.VT_UI8, pythoncom.VT_UINT, pythoncom.VT_VOID]
NoTranslateMap = {}
for v in NoTranslateTypes:
    NoTranslateMap[v] = None

class MapEntry:
    __doc__ = 'Simple holder for named attibutes - items in a map.'

    def __init__(self, desc_or_id, names=None, doc=None, resultCLSID=pythoncom.IID_NULL, resultDoc=None, hidden=0):
        if type(desc_or_id) == type(0):
            self.dispid = desc_or_id
            self.desc = None
        else:
            self.dispid = desc_or_id[0]
            self.desc = desc_or_id
        self.names = names
        self.doc = doc
        self.resultCLSID = resultCLSID
        self.resultDocumentation = resultDoc
        self.wasProperty = 0
        self.hidden = hidden

    def GetResultCLSID(self):
        rc = self.resultCLSID
        if rc == pythoncom.IID_NULL:
            return
        else:
            return rc

    def GetResultCLSIDStr(self):
        rc = self.GetResultCLSID()
        if rc is None:
            return 'None'
        else:
            return repr(str(rc))

    def GetResultName(self):
        if self.resultDocumentation is None:
            return
        else:
            return self.resultDocumentation[0]


class OleItem:
    typename = 'OleItem'

    def __init__(self, doc=None):
        self.doc = doc
        if self.doc:
            self.python_name = MakePublicAttributeName(self.doc[0])
        else:
            self.python_name = None
        self.bWritten = 0
        self.bIsDispatch = 0
        self.bIsSink = 0
        self.clsid = None
        self.co_class = None


class DispatchItem(OleItem):
    typename = 'DispatchItem'

    def __init__(self, typeinfo=None, attr=None, doc=None, bForUser=1):
        OleItem.__init__(self, doc)
        self.propMap = {}
        self.propMapGet = {}
        self.propMapPut = {}
        self.mapFuncs = {}
        self.defaultDispatchName = None
        self.hidden = 0
        if typeinfo:
            self.Build(typeinfo, attr, bForUser)

    def _propMapPutCheck_(self, key, item):
        ins, outs, opts = self.CountInOutOptArgs(item.desc[2])
        if ins > 1:
            if opts + 1 == ins or ins == item.desc[6] + 1:
                newKey = 'Set' + key
                deleteExisting = 0
            else:
                deleteExisting = 1
                if key in self.mapFuncs or key in self.propMapGet:
                    newKey = 'Set' + key
                else:
                    newKey = key
                item.wasProperty = 1
                self.mapFuncs[newKey] = item
                if deleteExisting:
                    del self.propMapPut[key]

    def _propMapGetCheck_(self, key, item):
        ins, outs, opts = self.CountInOutOptArgs(item.desc[2])
        if ins > 0:
            if item.desc[6] == ins or ins == opts:
                newKey = 'Get' + key
                deleteExisting = 0
            else:
                deleteExisting = 1
                if key in self.mapFuncs:
                    newKey = 'Get' + key
                else:
                    newKey = key
                item.wasProperty = 1
                self.mapFuncs[newKey] = item
                if deleteExisting:
                    del self.propMapGet[key]

    def _AddFunc_(self, typeinfo, fdesc, bForUser):
        id = fdesc.memid
        funcflags = fdesc.wFuncFlags
        try:
            names = typeinfo.GetNames(id)
            name = names[0]
        except pythoncom.ole_error:
            name = ''
            names = None

        doc = None
        try:
            if bForUser:
                doc = typeinfo.GetDocumentation(id)
        except pythoncom.ole_error:
            pass

        if id == 0:
            if name:
                self.defaultDispatchName = name
        else:
            invkind = fdesc.invkind
            typerepr, flag, defval = fdesc.rettype
            typerepr, resultCLSID, resultDoc = _ResolveType(typerepr, typeinfo)
            fdesc.rettype = (
             typerepr, flag, defval, resultCLSID)
            argList = []
            for argDesc in fdesc.args:
                typerepr, flag, defval = argDesc
                arg_type, arg_clsid, arg_doc = _ResolveType(typerepr, typeinfo)
                argDesc = (arg_type, flag, defval, arg_clsid)
                argList.append(argDesc)

            fdesc.args = tuple(argList)
            hidden = funcflags & pythoncom.FUNCFLAG_FHIDDEN != 0
            if invkind == pythoncom.INVOKE_PROPERTYGET:
                map = self.propMapGet
            else:
                if invkind in (pythoncom.INVOKE_PROPERTYPUT, pythoncom.INVOKE_PROPERTYPUTREF):
                    existing = self.propMapPut.get(name, None)
                    if existing is not None:
                        if existing.desc[4] == pythoncom.INVOKE_PROPERTYPUT:
                            map = self.mapFuncs
                            name = 'Set' + name
                        else:
                            existing.wasProperty = 1
                            self.mapFuncs['Set' + name] = existing
                            map = self.propMapPut
                    else:
                        map = self.propMapPut
                else:
                    if invkind == pythoncom.INVOKE_FUNC:
                        map = self.mapFuncs
                    else:
                        map = None
        if map is not None:
            map[name] = MapEntry(tuple(fdesc), names, doc, resultCLSID, resultDoc, hidden)
            if fdesc.funckind != pythoncom.FUNC_DISPATCH:
                return
            else:
                return (
                 name, map)

    def _AddVar_(self, typeinfo, fdesc, bForUser):
        if fdesc.varkind == pythoncom.VAR_DISPATCH:
            id = fdesc.memid
            names = typeinfo.GetNames(id)
            typerepr, flags, defval = fdesc.elemdescVar
            typerepr, resultCLSID, resultDoc = _ResolveType(typerepr, typeinfo)
            fdesc.elemdescVar = (typerepr, flags, defval)
            doc = None
            try:
                if bForUser:
                    doc = typeinfo.GetDocumentation(id)
            except pythoncom.ole_error:
                pass

            map = self.propMap
            hidden = 0
            if hasattr(fdesc, 'wVarFlags'):
                hidden = fdesc.wVarFlags & 64 != 0
            map[names[0]] = MapEntry(tuple(fdesc), names, doc, resultCLSID, resultDoc, hidden)
            return (
             names[0], map)
        else:
            return

    def Build(self, typeinfo, attr, bForUser=1):
        self.clsid = attr[0]
        self.bIsDispatch = attr.wTypeFlags & pythoncom.TYPEFLAG_FDISPATCHABLE != 0
        if typeinfo is None:
            return
        for j in range(attr[6]):
            fdesc = typeinfo.GetFuncDesc(j)
            self._AddFunc_(typeinfo, fdesc, bForUser)

        for j in range(attr[7]):
            fdesc = typeinfo.GetVarDesc(j)
            self._AddVar_(typeinfo, fdesc, bForUser)

        for key, item in list(self.propMapGet.items()):
            self._propMapGetCheck_(key, item)

        for key, item in list(self.propMapPut.items()):
            self._propMapPutCheck_(key, item)

    def CountInOutOptArgs(self, argTuple):
        """Return tuple counting in/outs/OPTS.  Sum of result may not be len(argTuple), as some args may be in/out."""
        ins = out = opts = 0
        for argCheck in argTuple:
            inOut = argCheck[1]
            if inOut == 0:
                ins = ins + 1
                out = out + 1
            else:
                if inOut & pythoncom.PARAMFLAG_FIN:
                    ins = ins + 1
                if inOut & pythoncom.PARAMFLAG_FOPT:
                    opts = opts + 1
                if inOut & pythoncom.PARAMFLAG_FOUT:
                    out = out + 1

        return (
         ins, out, opts)

    def MakeFuncMethod(self, entry, name, bMakeClass=1):
        if entry.desc is not None:
            if len(entry.desc) < 6 or entry.desc[6] != -1:
                return self.MakeDispatchFuncMethod(entry, name, bMakeClass)
        return self.MakeVarArgsFuncMethod(entry, name, bMakeClass)

    def MakeDispatchFuncMethod(self, entry, name, bMakeClass=1):
        fdesc = entry.desc
        doc = entry.doc
        names = entry.names
        ret = []
        if bMakeClass:
            linePrefix = '\t'
            defNamedOptArg = 'defaultNamedOptArg'
            defNamedNotOptArg = 'defaultNamedNotOptArg'
            defUnnamedArg = 'defaultUnnamedArg'
        else:
            linePrefix = ''
            defNamedOptArg = 'pythoncom.Missing'
            defNamedNotOptArg = 'pythoncom.Missing'
            defUnnamedArg = 'pythoncom.Missing'
        defOutArg = 'pythoncom.Missing'
        id = fdesc[0]
        s = linePrefix + 'def ' + name + '(self' + BuildCallList(fdesc, names, defNamedOptArg, defNamedNotOptArg, defUnnamedArg, defOutArg) + '):'
        ret.append(s)
        if doc:
            if doc[1]:
                ret.append(linePrefix + '\t' + _makeDocString(doc[1]))
        else:
            resclsid = entry.GetResultCLSID()
            if resclsid:
                resclsid = "'%s'" % resclsid
            else:
                resclsid = 'None'
        retDesc = fdesc[8][:2]
        argsDesc = tuple([what[:2] for what in fdesc[2]])
        param_flags = [what[1] for what in fdesc[2]]
        bad_params = [flag for flag in param_flags if flag & (pythoncom.PARAMFLAG_FOUT | pythoncom.PARAMFLAG_FRETVAL) != 0]
        s = None
        if len(bad_params) == 0:
            if len(retDesc) == 2:
                if retDesc[1] == 0:
                    rd = retDesc[0]
                    if rd in NoTranslateMap:
                        s = '%s\treturn self._oleobj_.InvokeTypes(%d, LCID, %s, %s, %s%s)' % (linePrefix, id, fdesc[4], retDesc, argsDesc, _BuildArgList(fdesc, names))
                    else:
                        if rd in [pythoncom.VT_DISPATCH, pythoncom.VT_UNKNOWN]:
                            s = '%s\tret = self._oleobj_.InvokeTypes(%d, LCID, %s, %s, %s%s)\n' % (linePrefix, id, fdesc[4], retDesc, repr(argsDesc), _BuildArgList(fdesc, names))
                            s = s + '%s\tif ret is not None:\n' % (linePrefix,)
                            if rd == pythoncom.VT_UNKNOWN:
                                s = s + '%s\t\t# See if this IUnknown is really an IDispatch\n' % (linePrefix,)
                                s = s + '%s\t\ttry:\n' % (linePrefix,)
                                s = s + '%s\t\t\tret = ret.QueryInterface(pythoncom.IID_IDispatch)\n' % (linePrefix,)
                                s = s + '%s\t\texcept pythoncom.error:\n' % (linePrefix,)
                                s = s + '%s\t\t\treturn ret\n' % (linePrefix,)
                            s = s + '%s\t\tret = Dispatch(ret, %s, %s)\n' % (linePrefix, repr(name), resclsid)
                            s = s + '%s\treturn ret' % linePrefix
                        elif rd == pythoncom.VT_BSTR:
                            s = '%s\t# Result is a Unicode object\n' % (linePrefix,)
                            s = s + '%s\treturn self._oleobj_.InvokeTypes(%d, LCID, %s, %s, %s%s)' % (linePrefix, id, fdesc[4], retDesc, repr(argsDesc), _BuildArgList(fdesc, names))
        if s is None:
            s = '%s\treturn self._ApplyTypes_(%d, %s, %s, %s, %s, %s%s)' % (linePrefix, id, fdesc[4], retDesc, argsDesc, repr(name), resclsid, _BuildArgList(fdesc, names))
        ret.append(s)
        ret.append('')
        return ret

    def MakeVarArgsFuncMethod(self, entry, name, bMakeClass=1):
        fdesc = entry.desc
        names = entry.names
        doc = entry.doc
        ret = []
        argPrefix = 'self'
        if bMakeClass:
            linePrefix = '\t'
        else:
            linePrefix = ''
        ret.append(linePrefix + 'def ' + name + '(' + argPrefix + ', *args):')
        if doc:
            if doc[1]:
                ret.append(linePrefix + '\t' + _makeDocString(doc[1]))
        else:
            if fdesc:
                invoketype = fdesc[4]
            else:
                invoketype = pythoncom.DISPATCH_METHOD
        s = linePrefix + '\treturn self._get_good_object_(self._oleobj_.Invoke(*(('
        ret.append(s + str(entry.dispid) + ",0,%d,1)+args)),'%s')" % (invoketype, names[0]))
        ret.append('')
        return ret


class VTableItem(DispatchItem):

    def Build(self, typeinfo, attr, bForUser=1):
        DispatchItem.Build(self, typeinfo, attr, bForUser)
        assert typeinfo is not None, 'Cant build vtables without type info!'
        meth_list = list(self.mapFuncs.values()) + list(self.propMapGet.values()) + list(self.propMapPut.values())
        meth_list.sort(key=(lambda m: m.desc[7]))
        self.vtableFuncs = []
        for entry in meth_list:
            self.vtableFuncs.append((entry.names, entry.dispid, entry.desc))


class LazyDispatchItem(DispatchItem):
    typename = 'LazyDispatchItem'

    def __init__(self, attr, doc):
        self.clsid = attr[0]
        DispatchItem.__init__(self, None, attr, doc, 0)


typeSubstMap = {pythoncom.VT_INT: pythoncom.VT_I4, 
 pythoncom.VT_UINT: pythoncom.VT_UI4, 
 pythoncom.VT_HRESULT: pythoncom.VT_I4}

def _ResolveType(typerepr, itypeinfo):
    if type(typerepr) == tuple:
        indir_vt, subrepr = typerepr
        if indir_vt == pythoncom.VT_PTR:
            was_user = type(subrepr) == tuple and subrepr[0] == pythoncom.VT_USERDEFINED
            subrepr, sub_clsid, sub_doc = _ResolveType(subrepr, itypeinfo)
            if was_user:
                if subrepr in [pythoncom.VT_DISPATCH, pythoncom.VT_UNKNOWN, pythoncom.VT_RECORD]:
                    return (
                     subrepr, sub_clsid, sub_doc)
            return (
             subrepr | pythoncom.VT_BYREF, sub_clsid, sub_doc)
        if indir_vt == pythoncom.VT_SAFEARRAY:
            subrepr, sub_clsid, sub_doc = _ResolveType(subrepr, itypeinfo)
            return (pythoncom.VT_ARRAY | subrepr, sub_clsid, sub_doc)
        if indir_vt == pythoncom.VT_CARRAY:
            return (
             pythoncom.VT_CARRAY, None, None)
        if indir_vt == pythoncom.VT_USERDEFINED:
            try:
                resultTypeInfo = itypeinfo.GetRefTypeInfo(subrepr)
            except pythoncom.com_error as details:
                if details.hresult in [winerror.TYPE_E_CANTLOADLIBRARY, winerror.TYPE_E_LIBNOTREGISTERED]:
                    return (pythoncom.VT_UNKNOWN, None, None)
                raise

            resultAttr = resultTypeInfo.GetTypeAttr()
            typeKind = resultAttr.typekind
            if typeKind == pythoncom.TKIND_ALIAS:
                tdesc = resultAttr.tdescAlias
                return _ResolveType(tdesc, resultTypeInfo)
            if typeKind in [pythoncom.TKIND_ENUM, pythoncom.TKIND_MODULE]:
                return (pythoncom.VT_I4, None, None)
            if typeKind == pythoncom.TKIND_DISPATCH:
                clsid = resultTypeInfo.GetTypeAttr()[0]
                retdoc = resultTypeInfo.GetDocumentation(-1)
                return (pythoncom.VT_DISPATCH, clsid, retdoc)
            if typeKind in [pythoncom.TKIND_INTERFACE,
             pythoncom.TKIND_COCLASS]:
                clsid = resultTypeInfo.GetTypeAttr()[0]
                retdoc = resultTypeInfo.GetDocumentation(-1)
                return (pythoncom.VT_UNKNOWN, clsid, retdoc)
            if typeKind == pythoncom.TKIND_RECORD:
                return (
                 pythoncom.VT_RECORD, None, None)
            raise NotSupportedException('Can not resolve alias or user-defined type')
    return (
     typeSubstMap.get(typerepr, typerepr), None, None)


def _BuildArgList(fdesc, names):
    """Builds list of args to the underlying Invoke method."""
    numArgs = max(fdesc[6], len(fdesc[2]))
    names = list(names)
    while None in names:
        i = names.index(None)
        names[i] = 'arg%d' % (i,)

    names = list(map(MakePublicAttributeName, names[1:numArgs + 1]))
    name_num = 0
    while len(names) < numArgs:
        names.append('arg%d' % (len(names),))

    for i in range(0, len(names), 5):
        names[i] = names[i] + '\n\t\t\t'

    return ',' + ', '.join(names)


valid_identifier_chars = string.ascii_letters + string.digits + '_'

def demunge_leading_underscores(className):
    i = 0
    while className[i] == '_':
        i += 1

    assert i >= 2, "Should only be here with names starting with '__'"
    return className[i - 1:] + className[:i - 1]


def MakePublicAttributeName(className, is_global=False):
    if className[:2] == '__':
        return demunge_leading_underscores(className)
    else:
        if className == 'None':
            className = 'NONE'
        else:
            if iskeyword(className):
                ret = className.capitalize()
                if ret == className:
                    ret = ret.upper()
                return ret
        if is_global:
            if hasattr(__builtins__, className):
                ret = className.capitalize()
                if ret == className:
                    ret = ret.upper()
                return ret
        return ''.join([char for char in className if char in valid_identifier_chars])


def MakeDefaultArgRepr(defArgVal):
    try:
        inOut = defArgVal[1]
    except IndexError:
        inOut = pythoncom.PARAMFLAG_FIN

    if inOut & pythoncom.PARAMFLAG_FHASDEFAULT:
        val = defArgVal[2]
        if isinstance(val, datetime.datetime):
            return repr(tuple(val.utctimetuple()))
        else:
            if type(val) is TimeType:
                year = val.year
                month = val.month
                day = val.day
                hour = val.hour
                minute = val.minute
                second = val.second
                msec = val.msec
                return 'pywintypes.Time((%(year)d, %(month)d, %(day)d, %(hour)d, %(minute)d, %(second)d,0,0,0,%(msec)d))' % locals()
            return repr(val)


def BuildCallList(fdesc, names, defNamedOptArg, defNamedNotOptArg, defUnnamedArg, defOutArg, is_comment=False):
    """Builds a Python declaration for a method."""
    numArgs = len(fdesc[2])
    numOptArgs = fdesc[6]
    strval = ''
    if numOptArgs == -1:
        firstOptArg = numArgs
        numArgs = numArgs - 1
    else:
        firstOptArg = numArgs - numOptArgs
    for arg in range(numArgs):
        try:
            argName = names[(arg + 1)]
            namedArg = argName is not None
        except IndexError:
            namedArg = 0

        if not namedArg:
            argName = 'arg%d' % arg
        thisdesc = fdesc[2][arg]
        defArgVal = MakeDefaultArgRepr(thisdesc)
        if defArgVal is None:
            if thisdesc[1] & (pythoncom.PARAMFLAG_FOUT | pythoncom.PARAMFLAG_FIN) == pythoncom.PARAMFLAG_FOUT:
                defArgVal = defOutArg
            else:
                if namedArg:
                    if arg >= firstOptArg:
                        defArgVal = defNamedOptArg
                    else:
                        defArgVal = defNamedNotOptArg
                else:
                    defArgVal = defUnnamedArg
            argName = MakePublicAttributeName(argName)
            if (arg + 1) % 5 == 0:
                strval = strval + '\n'
                if is_comment:
                    strval = strval + '#'
                strval = strval + '\t\t\t'
            strval = strval + ', ' + argName
            if defArgVal:
                strval = strval + '=' + defArgVal

    if numOptArgs == -1:
        strval = strval + ', *' + names[(-1)]
    return strval


if __name__ == '__main__':
    print("Use 'makepy.py' to generate Python code - this module is just a helper")