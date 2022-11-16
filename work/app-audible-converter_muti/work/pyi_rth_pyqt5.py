# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: PyInstaller\hooks\rthooks\pyi_rth_pyqt5.py
import os, sys
pyqt_path = os.path.join(sys._MEIPASS, 'PyQt5', 'Qt')
os.environ['QT_PLUGIN_PATH'] = os.path.join(pyqt_path, 'plugins')
os.environ['QML2_IMPORT_PATH'] = os.path.join(pyqt_path, 'qml')
if 'PATH' in os.environ:
    os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']