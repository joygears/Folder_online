# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ui\ui_dlgTrial.py
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgTrial(object):

    def setupUi(self, dlgTrial):
        dlgTrial.setObjectName('dlgTrial')
        dlgTrial.resize(481, 218)
        dlgTrial.setStyleSheet('#dlgTrial {\n    background: #FDFDFD;\n}\n\n#btnTrial {\n    background-color: #4283DE;\n    color: #FFFFFF;\n    border: 1px solid #4283DE;\n    border-radius: 2px;\n}\n\n#btnTrial::hover {\n    background-color: #5891E1;\n}\n\n#btnTrial::pressed {\n    background-color: #3478D8;\n}\n\n#btnUpgrade {\n    color: #FFFFFF;\n    background: #c34e2e;\n    border: 0;\n    border-radius: 2px;\n}\n\n#btnUpgrade::hover {\n    background: #c45d41;\n}\n\n#btnUpgrade::pressed {\n    background: #BB401E;\n}')
        self.verticalLayout = QtWidgets.QVBoxLayout(dlgTrial)
        self.verticalLayout.setContentsMargins(20, 30, 30, 30)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName('verticalLayout')
        self.label = QtWidgets.QLabel(dlgTrial)
        self.label.setWordWrap(True)
        self.label.setObjectName('label')
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 61, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName('horizontalLayout')
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnTrial = QtWidgets.QPushButton(dlgTrial)
        self.btnTrial.setObjectName('btnTrial')
        self.horizontalLayout.addWidget(self.btnTrial)
        self.btnUpgrade = QtWidgets.QPushButton(dlgTrial)
        self.btnUpgrade.setObjectName('btnUpgrade')
        self.horizontalLayout.addWidget(self.btnUpgrade)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(dlgTrial)
        QtCore.QMetaObject.connectSlotsByName(dlgTrial)

    def retranslateUi(self, dlgTrial):
        from settings.settings import tr_ui
        _translate = tr_ui
        dlgTrial.setWindowTitle(_translate('dlgTrial', 'Trial limit'))
        self.label.setText(_translate('dlgTrial', 'Splitting Audible into chapters is not available for the trial version. Please upgrade to the full version to unlock it.'))
        self.btnTrial.setText(_translate('dlgTrial', 'Continue Trial'))
        self.btnUpgrade.setText(_translate('dlgTrial', 'Upgrade Now'))