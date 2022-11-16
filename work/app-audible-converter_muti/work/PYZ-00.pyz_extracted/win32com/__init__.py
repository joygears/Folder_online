# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: win32com\__init__.py
import win32api, sys, os, pythoncom
_frozen = getattr(sys, 'frozen', 1 == 0)
if _frozen:
    if not getattr(pythoncom, 'frozen', 0):
        pythoncom.frozen = sys.frozen
__gen_path__ = ''
__build_path__ = None

def SetupEnvironment():
    global __build_path__
    global __gen_path__
    HKEY_LOCAL_MACHINE = -2147483646
    KEY_QUERY_VALUE = 1
    try:
        keyName = 'SOFTWARE\\Python\\PythonCore\\%s\\PythonPath\\win32com' % sys.winver
        key = win32api.RegOpenKey(HKEY_LOCAL_MACHINE, keyName, 0, KEY_QUERY_VALUE)
    except (win32api.error, AttributeError):
        key = None

    try:
        found = 0
        if key is not None:
            try:
                __path__.append(win32api.RegQueryValue(key, 'Extensions'))
                found = 1
            except win32api.error:
                pass

        if not found:
            try:
                __path__.append(win32api.GetFullPathName(__path__[0] + '\\..\\win32comext'))
            except win32api.error:
                pass

        try:
            if key is not None:
                __build_path__ = win32api.RegQueryValue(key, 'BuildPath')
                __path__.append(__build_path__)
        except win32api.error:
            pass

        if key is not None:
            try:
                __gen_path__ = win32api.RegQueryValue(key, 'GenPath')
            except win32api.error:
                pass

    finally:
        if key is not None:
            key.Close()


def __PackageSupportBuildPath__(package_path):
    if not _frozen:
        if __build_path__:
            package_path.append(__build_path__)


if not _frozen:
    SetupEnvironment()
if not __gen_path__:
    try:
        import win32com.gen_py
        __gen_path__ = next(iter(sys.modules['win32com.gen_py'].__path__))
    except ImportError:
        __gen_path__ = os.path.abspath(os.path.join(__path__[0], 'gen_py'))
        if not os.path.isdir(__gen_path__):
            __gen_path__ = os.path.join(win32api.GetTempPath(), 'gen_py', '%d.%d' % (sys.version_info[0], sys.version_info[1]))

if 'win32com.gen_py' not in sys.modules:
    import imp
    gen_py = imp.new_module('win32com.gen_py')
    gen_py.__path__ = [__gen_path__]
    sys.modules[gen_py.__name__] = gen_py
    del imp
gen_py = sys.modules['win32com.gen_py']
del os
del sys
del win32api
del pythoncom