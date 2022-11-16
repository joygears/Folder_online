# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ui\ui_dlgWaiting.py
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgWaiting(object):

    def setupUi(self, dlgWaiting):
        dlgWaiting.setObjectName('dlgWaiting')
        dlgWaiting.resize(481, 107)
        self.horizontalLayout = QtWidgets.QHBoxLayout(dlgWaiting)
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.labGif = QtWidgets.QLabel(dlgWaiting)
        self.labGif.setText('')
        self.labGif.setObjectName('labGif')
        self.horizontalLayout.addWidget(self.labGif)
        self.labMessage = QtWidgets.QLabel(dlgWaiting)
        self.labMessage.setText('')
        self.labMessage.setWordWrap(True)
        self.labMessage.setObjectName('labMessage')
        self.horizontalLayout.addWidget(self.labMessage)
        self.retranslateUi(dlgWaiting)
        QtCore.QMetaObject.connectSlotsByName(dlgWaiting)

    def retranslateUi(self, dlgWaiting):
        from settings.settings import tr_ui
        _translate = tr_ui
        dlgWaiting.setWindowTitle(_translate('dlgWaiting', 'Information'))