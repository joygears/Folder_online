# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: win32com\client\gencache.py
"""Manages the cache of generated Python code.

Description
  This file manages the cache of generated Python code.  When run from the 
  command line, it also provides a number of options for managing that cache.
  
Implementation
  Each typelib is generated into a filename of format "{guid}x{lcid}x{major}x{minor}.py"
  
  An external persistant dictionary maps from all known IIDs in all known type libraries
  to the type library itself.
  
  Thus, whenever Python code knows the IID of an object, it can find the IID, LCID and version of
  the type library which supports it.  Given this information, it can find the Python module
  with the support.
  
  If necessary, this support can be generated on the fly.
  
Hacks, to do, etc
  Currently just uses a pickled dictionary, but should used some sort of indexed file.
  Maybe an OLE2 compound file, or a bsddb file?
"""
import pywintypes, os, sys, pythoncom, win32com, win32com.client, glob, traceback
from . import CLSIDToClass
import operator
try:
    from imp import reload
except:
    pass

bForDemandDefault = 0
clsidToTypelib = {}
versionRedirectMap = {}
is_readonly = is_zip = hasattr(win32com, '__loader__') and hasattr(win32com.__loader__, 'archive')
demandGeneratedTypeLibraries = {}
import pickle

def __init__():
    try:
        _LoadDicts()
    except IOError:
        Rebuild()


pickleVersion = 1

def _SaveDicts():
    global clsidToTypelib
    if is_readonly:
        raise RuntimeError("Trying to write to a readonly gencache ('%s')!" % win32com.__gen_path__)
    f = open(os.path.join(GetGeneratePath(), 'dicts.dat'), 'wb')
    try:
        p = pickle.Pickler(f)
        p.dump(pickleVersion)
        p.dump(clsidToTypelib)
    finally:
        f.close()


def _LoadDicts():
    global clsidToTypelib
    if is_zip:
        import io
        loader = win32com.__loader__
        arc_path = loader.archive
        dicts_path = os.path.join(win32com.__gen_path__, 'dicts.dat')
        if dicts_path.startswith(arc_path):
            dicts_path = dicts_path[len(arc_path) + 1:]
        else:
            return
            try:
                data = loader.get_data(dicts_path)
            except AttributeError:
                return
            except IOError:
                return

        f = io.BytesIO(data)
    else:
        f = open(os.path.join(win32com.__gen_path__, 'dicts.dat'), 'rb')
    try:
        p = pickle.Unpickler(f)
        version = p.load()
        clsidToTypelib = p.load()
        versionRedirectMap.clear()
    finally:
        f.close()


def GetGeneratedFileName(clsid, lcid, major, minor):
    """Given the clsid, lcid, major and  minor for a type lib, return
        the file name (no extension) providing this support.
        """
    return str(clsid).upper()[1:-1] + 'x%sx%sx%s' % (lcid, major, minor)


def SplitGeneratedFileName(fname):
    """Reverse of GetGeneratedFileName()
        """
    return tuple(fname.split('x', 4))


def GetGeneratePath():
    """Returns the name of the path to generate to.
        Checks the directory is OK.
        """
    assert not is_readonly, 'Why do you want the genpath for a readonly store?'
    try:
        os.makedirs(win32com.__gen_path__)
    except os.error:
        pass

    try:
        fname = os.path.join(win32com.__gen_path__, '__init__.py')
        os.stat(fname)
    except os.error:
        f = open(fname, 'w')
        f.write('# Generated file - this directory may be deleted to reset the COM cache...\n')
        f.write('import win32com\n')
        f.write('if __path__[:-1] != win32com.__gen_path__: __path__.append(win32com.__gen_path__)\n')
        f.close()

    return win32com.__gen_path__


def GetClassForProgID(progid):
    """Get a Python class for a Program ID
        
        Given a Program ID, return a Python class which wraps the COM object
        
        Returns the Python class, or None if no module is available.
        
        Params
        progid -- A COM ProgramID or IID (eg, "Word.Application")
        """
    clsid = pywintypes.IID(progid)
    return GetClassForCLSID(clsid)


def GetClassForCLSID(clsid):
    """Get a Python class for a CLSID
        
        Given a CLSID, return a Python class which wraps the COM object
        
        Returns the Python class, or None if no module is available.
        
        Params
        clsid -- A COM CLSID (or string repr of one)
        """
    clsid = str(clsid)
    if CLSIDToClass.HasClass(clsid):
        return CLSIDToClass.GetClass(clsid)
    mod = GetModuleForCLSID(clsid)
    if mod is None:
        return
    try:
        return CLSIDToClass.GetClass(clsid)
    except KeyError:
        return


def GetModuleForProgID(progid):
    """Get a Python module for a Program ID
        
        Given a Program ID, return a Python module which contains the
        class which wraps the COM object.
        
        Returns the Python module, or None if no module is available.
        
        Params
        progid -- A COM ProgramID or IID (eg, "Word.Application")
        """
    try:
        iid = pywintypes.IID(progid)
    except pywintypes.com_error:
        return
    else:
        return GetModuleForCLSID(iid)


def GetModuleForCLSID(clsid):
    """Get a Python module for a CLSID
        
        Given a CLSID, return a Python module which contains the
        class which wraps the COM object.
        
        Returns the Python module, or None if no module is available.
        
        Params
        progid -- A COM CLSID (ie, not the description)
        """
    clsid_str = str(clsid)
    try:
        typelibCLSID, lcid, major, minor = clsidToTypelib[clsid_str]
    except KeyError:
        return
    else:
        try:
            mod = GetModuleForTypelib(typelibCLSID, lcid, major, minor)
        except ImportError:
            mod = None

        if mod is not None:
            sub_mod = mod.CLSIDToPackageMap.get(clsid_str)
            if sub_mod is None:
                sub_mod = mod.VTablesToPackageMap.get(clsid_str)
            if sub_mod is not None:
                sub_mod_name = mod.__name__ + '.' + sub_mod
                try:
                    __import__(sub_mod_name)
                except ImportError:
                    info = (
                     typelibCLSID, lcid, major, minor)
                    if info in demandGeneratedTypeLibraries:
                        info = demandGeneratedTypeLibraries[info]
                    from . import makepy
                    makepy.GenerateChildFromTypeLibSpec(sub_mod, info)

                mod = sys.modules[sub_mod_name]
        return mod


def GetModuleForTypelib(typelibCLSID, lcid, major, minor):
    """Get a Python module for a type library ID
        
        Given the CLSID of a typelibrary, return an imported Python module, 
        else None
        
        Params
        typelibCLSID -- IID of the type library.
        major -- Integer major version.
        minor -- Integer minor version
        lcid -- Integer LCID for the library.
        """
    modName = GetGeneratedFileName(typelibCLSID, lcid, major, minor)
    mod = _GetModule(modName)
    if '_in_gencache_' not in mod.__dict__:
        AddModuleToCache(typelibCLSID, lcid, major, minor)
        if not '_in_gencache_' in mod.__dict__:
            raise AssertionError
    return mod


def MakeModuleForTypelib(typelibCLSID, lcid, major, minor, progressInstance=None, bForDemand=bForDemandDefault, bBuildHidden=1):
    """Generate support for a type library.
        
        Given the IID, LCID and version information for a type library, generate
        and import the necessary support files.
        
        Returns the Python module.  No exceptions are caught.

        Params
        typelibCLSID -- IID of the type library.
        major -- Integer major version.
        minor -- Integer minor version.
        lcid -- Integer LCID for the library.
        progressInstance -- Instance to use as progress indicator, or None to
                            use the GUI progress bar.
        """
    from . import makepy
    makepy.GenerateFromTypeLibSpec((typelibCLSID, lcid, major, minor), progressInstance=progressInstance, bForDemand=bForDemand, bBuildHidden=bBuildHidden)
    return GetModuleForTypelib(typelibCLSID, lcid, major, minor)


def MakeModuleForTypelibInterface(typelib_ob, progressInstance=None, bForDemand=bForDemandDefault, bBuildHidden=1):
    """Generate support for a type library.
        
        Given a PyITypeLib interface generate and import the necessary support files.  This is useful
        for getting makepy support for a typelibrary that is not registered - the caller can locate
        and load the type library itself, rather than relying on COM to find it.
        
        Returns the Python module.

        Params
        typelib_ob -- The type library itself
        progressInstance -- Instance to use as progress indicator, or None to
                            use the GUI progress bar.
        """
    from . import makepy
    try:
        makepy.GenerateFromTypeLibSpec(typelib_ob, progressInstance=progressInstance, bForDemand=bForDemandDefault, bBuildHidden=bBuildHidden)
    except pywintypes.com_error:
        return
    else:
        tla = typelib_ob.GetLibAttr()
        guid = tla[0]
        lcid = tla[1]
        major = tla[3]
        minor = tla[4]
        return GetModuleForTypelib(guid, lcid, major, minor)


def EnsureModuleForTypelibInterface(typelib_ob, progressInstance=None, bForDemand=bForDemandDefault, bBuildHidden=1):
    """Check we have support for a type library, generating if not.
        
        Given a PyITypeLib interface generate and import the necessary
        support files if necessary. This is useful for getting makepy support
        for a typelibrary that is not registered - the caller can locate and
        load the type library itself, rather than relying on COM to find it.
        
        Returns the Python module.

        Params
        typelib_ob -- The type library itself
        progressInstance -- Instance to use as progress indicator, or None to
                            use the GUI progress bar.
        """
    tla = typelib_ob.GetLibAttr()
    guid = tla[0]
    lcid = tla[1]
    major = tla[3]
    minor = tla[4]
    if bForDemand:
        demandGeneratedTypeLibraries[(str(guid), lcid, major, minor)] = typelib_ob
    try:
        return GetModuleForTypelib(guid, lcid, major, minor)
    except ImportError:
        pass

    return MakeModuleForTypelibInterface(typelib_ob, progressInstance, bForDemand, bBuildHidden)


def ForgetAboutTypelibInterface(typelib_ob):
    """Drop any references to a typelib previously added with EnsureModuleForTypelibInterface and forDemand"""
    tla = typelib_ob.GetLibAttr()
    guid = tla[0]
    lcid = tla[1]
    major = tla[3]
    minor = tla[4]
    info = (str(guid), lcid, major, minor)
    try:
        del demandGeneratedTypeLibraries[info]
    except KeyError:
        print('ForgetAboutTypelibInterface:: Warning - type library with info %s is not being remembered!' % (info,))

    for key, val in list(versionRedirectMap.items()):
        if val == info:
            del versionRedirectMap[key]


def EnsureModule(typelibCLSID, lcid, major, minor, progressInstance=None, bValidateFile=not is_readonly, bForDemand=bForDemandDefault, bBuildHidden=1):
    """Ensure Python support is loaded for a type library, generating if necessary.
        
        Given the IID, LCID and version information for a type library, check and if
        necessary (re)generate, then import the necessary support files. If we regenerate the file, there
        is no way to totally snuff out all instances of the old module in Python, and thus we will regenerate the file more than necessary,
        unless makepy/genpy is modified accordingly.
        
        
        Returns the Python module.  No exceptions are caught during the generate process.

        Params
        typelibCLSID -- IID of the type library.
        major -- Integer major version.
        minor -- Integer minor version
        lcid -- Integer LCID for the library.
        progressInstance -- Instance to use as progress indicator, or None to
                            use the GUI progress bar.
        bValidateFile -- Whether or not to perform cache validation or not
        bForDemand -- Should a complete generation happen now, or on demand?
        bBuildHidden -- Should hidden members/attributes etc be generated?
        """
    bReloadNeeded = 0
    try:
        try:
            module = GetModuleForTypelib(typelibCLSID, lcid, major, minor)
        except ImportError:
            module = None
            try:
                tlbAttr = pythoncom.LoadRegTypeLib(typelibCLSID, major, minor, lcid).GetLibAttr()
                if tlbAttr[1] != lcid or tlbAttr[4] != minor:
                    try:
                        module = GetModuleForTypelib(typelibCLSID, tlbAttr[1], tlbAttr[3], tlbAttr[4])
                    except ImportError:
                        minor = tlbAttr[4]

            except pythoncom.com_error:
                pass

        if module is not None and bValidateFile:
            assert not is_readonly, "Can't validate in a read-only gencache"
            try:
                typLibPath = pythoncom.QueryPathOfRegTypeLib(typelibCLSID, major, minor, lcid)
                if typLibPath[(-1)] == '\x00':
                    typLibPath = typLibPath[:-1]
                suf = getattr(os.path, 'supports_unicode_filenames', 0)
                if not suf:
                    try:
                        typLibPath = typLibPath.encode(sys.getfilesystemencoding())
                    except AttributeError:
                        typLibPath = str(typLibPath)

                tlbAttributes = pythoncom.LoadRegTypeLib(typelibCLSID, major, minor, lcid).GetLibAttr()
            except pythoncom.com_error:
                bValidateFile = 0

        if module is not None:
            if bValidateFile:
                assert not is_readonly, "Can't validate in a read-only gencache"
                filePathPrefix = '%s\\%s' % (GetGeneratePath(), GetGeneratedFileName(typelibCLSID, lcid, major, minor))
                filePath = filePathPrefix + '.py'
                filePathPyc = filePathPrefix + '.py'
                filePathPyc = filePathPyc + 'c'
                from . import genpy
                if module.MinorVersion != tlbAttributes[4] or genpy.makepy_version != module.makepy_version:
                    try:
                        os.unlink(filePath)
                    except os.error:
                        pass

                    try:
                        os.unlink(filePathPyc)
                    except os.error:
                        pass

                    if os.path.isdir(filePathPrefix):
                        import shutil
                        shutil.rmtree(filePathPrefix)
                    minor = tlbAttributes[4]
                    module = None
                    bReloadNeeded = 1
                else:
                    minor = module.MinorVersion
                    filePathPrefix = '%s\\%s' % (GetGeneratePath(), GetGeneratedFileName(typelibCLSID, lcid, major, minor))
                    filePath = filePathPrefix + '.py'
                    filePathPyc = filePathPrefix + '.pyc'
                    fModTimeSet = 0
                    try:
                        pyModTime = os.stat(filePath)[8]
                        fModTimeSet = 1
                    except os.error as e:
                        try:
                            pyModTime = os.stat(filePathPyc)[8]
                            fModTimeSet = 1
                        except os.error as e:
                            pass

                    typLibModTime = os.stat(typLibPath)[8]
                    if fModTimeSet:
                        if typLibModTime > pyModTime:
                            bReloadNeeded = 1
                            module = None
    except (ImportError, os.error):
        module = None

    if module is None:
        if is_readonly:
            key = (
             str(typelibCLSID), lcid, major, minor)
            try:
                return versionRedirectMap[key]
            except KeyError:
                pass

            items = []
            for desc in GetGeneratedInfos():
                if key[0] == desc[0] and key[1] == desc[1] and key[2] == desc[2]:
                    items.append(desc)

            if items:
                items.sort()
                new_minor = items[(-1)][3]
                ret = GetModuleForTypelib(typelibCLSID, lcid, major, new_minor)
            else:
                ret = None
            versionRedirectMap[key] = ret
            return ret
        module = MakeModuleForTypelib(typelibCLSID, lcid, major, minor, progressInstance, bForDemand=bForDemand, bBuildHidden=bBuildHidden)
        if bReloadNeeded:
            module = reload(module)
            AddModuleToCache(typelibCLSID, lcid, major, minor)
    return module


def EnsureDispatch(prog_id, bForDemand=1):
    """Given a COM prog_id, return an object that is using makepy support, building if necessary"""
    disp = win32com.client.Dispatch(prog_id)
    if not disp.__dict__.get('CLSID'):
        try:
            ti = disp._oleobj_.GetTypeInfo()
            disp_clsid = ti.GetTypeAttr()[0]
            tlb, index = ti.GetContainingTypeLib()
            tla = tlb.GetLibAttr()
            mod = EnsureModule((tla[0]), (tla[1]), (tla[3]), (tla[4]), bForDemand=bForDemand)
            GetModuleForCLSID(disp_clsid)
            from . import CLSIDToClass
            disp_class = CLSIDToClass.GetClass(str(disp_clsid))
            disp = disp_class(disp._oleobj_)
        except pythoncom.com_error:
            raise TypeError('This COM object can not automate the makepy process - please run makepy manually for this object')

    return disp


def AddModuleToCache(typelibclsid, lcid, major, minor, verbose=1, bFlushNow=not is_readonly):
    """Add a newly generated file to the cache dictionary.
        """
    fname = GetGeneratedFileName(typelibclsid, lcid, major, minor)
    mod = _GetModule(fname)
    mod._in_gencache_ = 1
    dict = mod.CLSIDToClassMap
    info = (str(typelibclsid), lcid, major, minor)
    for clsid, cls in dict.items():
        clsidToTypelib[clsid] = info

    dict = mod.CLSIDToPackageMap
    for clsid, name in dict.items():
        clsidToTypelib[clsid] = info

    dict = mod.VTablesToClassMap
    for clsid, cls in dict.items():
        clsidToTypelib[clsid] = info

    dict = mod.VTablesToPackageMap
    for clsid, cls in dict.items():
        clsidToTypelib[clsid] = info

    if info in versionRedirectMap:
        del versionRedirectMap[info]
    if bFlushNow:
        _SaveDicts()


def GetGeneratedInfos():
    zip_pos = win32com.__gen_path__.find('.zip\\')
    if zip_pos >= 0:
        import zipfile
        zip_file = win32com.__gen_path__[:zip_pos + 4]
        zip_path = win32com.__gen_path__[zip_pos + 5:].replace('\\', '/')
        zf = zipfile.ZipFile(zip_file)
        infos = {}
        for n in zf.namelist():
            if not n.startswith(zip_path):
                pass
            else:
                base = n[len(zip_path) + 1:].split('/')[0]
                try:
                    iid, lcid, major, minor = base.split('x')
                    lcid = int(lcid)
                    major = int(major)
                    minor = int(minor)
                    iid = pywintypes.IID('{' + iid + '}')
                except ValueError:
                    continue
                except pywintypes.com_error:
                    continue

                infos[(iid, lcid, major, minor)] = 1

        zf.close()
        return list(infos.keys())
    else:
        files = glob.glob(win32com.__gen_path__ + '\\*')
        ret = []
        for file in files:
            if not os.path.isdir(file):
                if not os.path.splitext(file)[1] == '.py':
                    continue
            name = os.path.splitext(os.path.split(file)[1])[0]
            try:
                iid, lcid, major, minor = name.split('x')
                iid = pywintypes.IID('{' + iid + '}')
                lcid = int(lcid)
                major = int(major)
                minor = int(minor)
            except ValueError:
                continue
            except pywintypes.com_error:
                continue

            ret.append((iid, lcid, major, minor))

        return ret


def _GetModule(fname):
    """Given the name of a module in the gen_py directory, import and return it.
        """
    mod_name = 'win32com.gen_py.%s' % fname
    mod = __import__(mod_name)
    return sys.modules[mod_name]


def Rebuild(verbose=1):
    """Rebuild the cache indexes from the file system.
        """
    clsidToTypelib.clear()
    infos = GetGeneratedInfos()
    if verbose:
        if len(infos):
            print('Rebuilding cache of generated files for COM support...')
    for info in infos:
        iid, lcid, major, minor = info
        if verbose:
            print('Checking', GetGeneratedFileName(*info))
        try:
            AddModuleToCache(iid, lcid, major, minor, verbose, 0)
        except:
            print('Could not add module %s - %s: %s' % (info, sys.exc_info()[0], sys.exc_info()[1]))

    if verbose:
        if len(infos):
            print('Done.')
    _SaveDicts()


def _Dump():
    print('Cache is in directory', win32com.__gen_path__)
    d = {}
    for clsid, (typelibCLSID, lcid, major, minor) in clsidToTypelib.items():
        d[(typelibCLSID, lcid, major, minor)] = None

    for typelibCLSID, lcid, major, minor in d.keys():
        mod = GetModuleForTypelib(typelibCLSID, lcid, major, minor)
        print('%s - %s' % (mod.__doc__, typelibCLSID))


__init__()

def usage():
    usageString = '\t  Usage: gencache [-q] [-d] [-r]\n\t  \n\t\t\t -q         - Quiet\n\t\t\t -d         - Dump the cache (typelibrary description and filename).\n\t\t\t -r         - Rebuild the cache dictionary from the existing .py files\n\t'
    print(usageString)
    sys.exit(1)


if __name__ == '__main__':
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'qrd')
    except getopt.error as message:
        print(message)
        usage()

    if len(sys.argv) == 1 or args:
        print(usage())
    verbose = 1
    for opt, val in opts:
        if opt == '-d':
            _Dump()
        if opt == '-r':
            Rebuild(verbose)
        if opt == '-q':
            verbose = 0