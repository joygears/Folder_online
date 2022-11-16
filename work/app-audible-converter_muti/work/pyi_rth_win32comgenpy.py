# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: PyInstaller\hooks\rthooks\pyi_rth_win32comgenpy.py
import atexit, os, shutil, tempfile
supportdir = tempfile.mkdtemp()
genpydir = os.path.join(supportdir, 'gen_py')
try:
    os.makedirs(genpydir)
    atexit.register((shutil.rmtree), supportdir, ignore_errors=True)
except OSError:
    pass

import win32com
win32com.__gen_path__ = genpydir
if hasattr(win32com, '__loader__'):
    del win32com.__loader__
import win32com.gen_py
win32com.gen_py.__path__.insert(0, genpydir)