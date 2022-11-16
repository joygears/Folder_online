# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ui\dlgMain.py
import os, threading
from PyQt5.Qt import Qt, QPoint, QMainWindow, QFileDialog, QMenu, QActionGroup, QAction, QIcon, pyqtSignal, QPixmap
from settings.settings import res, tr, apps, iswindows, isosx, isblind, MP3_CHAPTER
from ui.ui_dlgMain import Ui_dlgMain
from ui.tables import Tables
from ui.dlgSettings import DlgSettings
from module.logger import logger
from settings.register import Register, RegAction_Check

class dlgMain(QMainWindow, Ui_dlgMain):
    if isblind:
        format = [('MP3 - MPEG-1,2 Audio Layer III', '.mp3'),
         ('MP3 with chapters - MPEG-1,2 Audio Layer III', '.mp3'),
         ('M4B - MPEG-4 Audio', '.m4b'),
         ('M4B with chapters - MPEG-4 Audio', '.m4b')]
    else:
        format = [('MP3 - MPEG-1,2 Audio Layer III', '.mp3'),
         ('M4B - MPEG-4 Audio', '.m4b')]
    signalUpdateVersion = pyqtSignal(object)

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(res.title)
        self.setWindowIcon(QIcon(res.icon))
        self.labelUpdate.setVisible(False)
        self.labelUpdateVer.setVisible(False)
        self.chapters = False
        threading.Thread(target=(self.getNewVersion), daemon=True).start()
        if isosx:
            style = '#btnReg,#btnSettings,#btnAdd, #btnOut{border: 1px solid #EEEEEE} #btnReg::hover,#btnSettings::hover,#btnAdd::hover,#btnOut::hover{background-color: #D6E4F0} #btnReg::pressed,#btnSettings::pressed,#btnAdd::pressed,#btnOut::pressed{background-color: #BEDAF1}'
            self.btnReg.setStyleSheet(style)
            self.btnSettings.setStyleSheet(style)
            self.btnAdd.setStyleSheet(style)
            self.btnOut.setStyleSheet(style)
        self.btnOut.setFixedSize(36, 36)
        self.btnOut.clicked.connect(self.slotBtnOut)
        self.stackRight.setCurrentWidget(self.pageBackground)
        if apps['is_max_size']:
            self.setWindowState(Qt.WindowMaximized)
        else:
            uisize = apps['ui_size']
        if uisize:
            self.resize(uisize[0], uisize[1])
        tOutputFormat = apps['output_formated'][1:]
        if tOutputFormat not in ('mp3', 'm4b'):
            tOutputFormat = 'mp3'
            apps['output_formated'] = '.mp3'
        pix = QPixmap(':/imgs/cover.png')
        if not os.path.exists(res.defaultcover):
            pix.save(res.defaultcover, 'PNG')
        self.btnCov.setText(tr('Convert to') + ' ' + tOutputFormat.upper())
        self.btnCov.setToolTip(tr('Convert to') + ' ' + tOutputFormat.upper())
        if isblind:
            if MP3_CHAPTER:
                apps['output_formated'] = '.mp3'
                self.chapters = True
                self.btnFormat.setVisible(False)
                self.btnCov.setText(tr('Convert to') + ' MP3 with chapters')
                self.btnCov.setToolTip(tr('Convert to') + ' MP3 with chapters')
        self.tables = Tables(self)
        self.register = Register(apps['id'], self)
        if apps['email']:
            email, licenseCode, retcode = self.register.Register(apps['email'], RegAction_Check)
            if retcode == '0':
                res.regInfo.isRegister = True
                res.regInfo.email = apps['email'] = email.lower()
                if licenseCode:
                    apps['email'] += ';' + licenseCode
                self.btnReg.setVisible(False)
            else:
                res.regInfo.isRegister = False
                res.regInfo.email = ''
        self.menu = QMenu()
        self.menu.setMinimumWidth(240)
        self.menu.setMaximumWidth(240 if iswindows else 300)
        self.menu.setStyleSheet('\n            QMenu {\n                background-color: #EFF6FB;\n                margin: 2px;\n            }\n            QMenu::item:selected {\n                color: #FFFFFF;\n                background: #63B1FC;\n            }\n            ')
        actiongrp = QActionGroup(self)
        for item in self.format:
            action = QAction(item[0], self)
            action.setData(item[1])
            actiongrp.addAction(action)
            self.menu.addAction(action)

        actiongrp.triggered.connect(self.slotFormatGroup)
        self.btnCov.clicked.connect(self.slotBtnCov)
        self.btnAdd.clicked.connect(self.slotBtnAdd)
        self.stackRight.signalDragFiles.connect(self.addFiles)
        self.btnReg.clicked.connect(self.slotBtnReg)
        self.btnSettings.clicked.connect(self.slotBtnSettings)
        self.btnFormat.clicked.connect(self.slotBtnFormat)
        self.signalUpdateVersion.connect(self.slotUpdateVersion)
        logger.debug('The main ui has started.')

    def getNewVersion(self):
        self.signalUpdateVersion.emit(res.newVersion)

    def slotUpdateVersion(self, newVersion):
        if not isblind:
            if newVersion:
                self.labelUpdateVer.setText('v' + newVersion)
                self.labelUpdateVer.clicked.connect(self.slotUpdate)
                self.labelUpdateVer.setVisible(True)
                self.labelUpdate.setVisible(True)
            else:
                self.labelUpdate.setVisible(False)
                self.labelUpdateVer.setVisible(False)

    def slotUpdate(self):
        import webbrowser, platform
        if iswindows:
            webbrowser.open('https://www.epubor.com/audible-converter-download.htm#os_Win')
        elif isosx:
            webbrowser.open('https://www.epubor.com/audible-converter-download.htm#os_Mac')

    def slotFormatGroup(self, action):
        apps['output_formated'] = action.data()
        if action.text() == 'MP3 with chapters - MPEG-1,2 Audio Layer III' or action.text() == 'M4B with chapters - MPEG-4 Audio':
            self.chapters = True
            self.btnCov.setText(tr('Convert to') + ' ' + apps['output_formated'][1:].upper() + ' Chapters')
            self.btnCov.setToolTip(tr('Convert to') + ' ' + apps['output_formated'][1:].upper() + ' Chapters')
        else:
            self.btnCov.setText(tr('Convert to') + ' ' + apps['output_formated'][1:].upper())
            self.btnCov.setToolTip(tr('Convert to') + ' ' + apps['output_formated'][1:].upper())
            self.chapters = False

    def slotBtnCov(self):
        self.tables.convert((apps['output_formated']), chapters=(self.chapters))

    def slotBtnAdd(self):
        logger.debug('Add audible files.')
        files = QFileDialog.getOpenFileNames(self, tr('Add Audible Books'), apps['downloadpath'], res.filter_add)[0]
        if files:
            apps['downloadpath'] = os.path.dirname(files[0])
            self.addFiles(files)

    def addFiles(self, files):
        self.tables.addFiles(files)

    def slotBtnReg(self):
        logger.debug('Click register button.')
        from ui.dlgReg import DlgReg
        r = DlgReg(self)
        r.exec_()

    def slotBtnSettings(self):
        logger.debug('Click settings button.')
        w = DlgSettings(self)
        w.exec_()

    def closeEvent(self, event):
        logger.debug('Close the program.')
        if self.isMaximized():
            apps['is_max_size'] = True
        else:
            apps['is_max_size'] = False
            apps['ui_size'] = [self.width(), self.height()]
        from settings.functions import kill_conv
        kill_conv()
        import sys
        sys.exit(0)

    def slotBtnFormat(self):
        if iswindows:
            width = 125
            height = 100
        else:
            if isosx:
                width = 135
                height = 90
        pos = QPoint(self.width() / 2 - width, self.height() - height)
        self.menu.move(self.mapToGlobal(pos))
        self.menu.exec_()

    def slotBtnOut(self):
        logger.debug('Open the output button.')
        import webbrowser
        webbrowser.open('file:///' + apps['outputpath'])