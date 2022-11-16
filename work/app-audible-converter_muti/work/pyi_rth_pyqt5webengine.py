# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: PyInstaller\hooks\rthooks\pyi_rth_pyqt5webengine.py
import os, sys
if sys.platform == 'darwin':
    os.environ['QTWEBENGINEPROCESS_PATH'] = os.path.normpath(os.path.join(sys._MEIPASS, 'PyQt5', 'Qt', 'lib', 'QtWebEngineCore.framework', 'Helpers', 'QtWebEngineProcess.app', 'Contents', 'MacOS', 'QtWebEngineProcess'))