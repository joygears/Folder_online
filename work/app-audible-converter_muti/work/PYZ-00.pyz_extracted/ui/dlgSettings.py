# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ui\dlgSettings.py
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QDialog, QButtonGroup, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from ui.ui_dlgSettings import Ui_dlgSettings
from settings.settings import tr, res, apps, homepath, MultiLanguage
from settings.functions import restart, os_sep

class DlgSettings(QDialog, Ui_dlgSettings):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(res.title)
        self.parent = parent
        self.labTitleIcon.setPixmap(QPixmap(res.icon))
        tTitle = res.title
        if res.regInfo.isRegister:
            tTitle += '      ' + tr('Licensed to') + ': ' + res.regInfo.email
        else:
            self.labTitle.setText(tTitle)
            self.stackRoot.setCurrentWidget(self.pageSettings)
            self.btnSettings.setChecked(True)
            self.grpRoot = QButtonGroup(self)
            self.grpRoot.addButton(self.btnSettings)
            self.grpRoot.addButton(self.btnHelp)
            self.slotGrpRoot(self.btnSettings)
            self.grpSettings = QButtonGroup(self)
            self.grpSettings.addButton(self.btnLang)
            self.grpSettings.addButton(self.btnOutput)
            self.slotGrpSettings(self.btnLang)
            self.grpHelp = QButtonGroup(self)
            if res.regInfo.isRegister:
                txtDereg = '<b>' + tr('Note') + ':&nbsp;&nbsp;</b>' + tr('De-register software will make you unable to use this software.') + '<br/><br/>' + tr('Please make sure you have a new license code, or do not de-register the') + '<br/><br/>' + tr('software') + '.'
                self.labelDeregisterInfo.setText(txtDereg)
                self.grpHelp.addButton(self.btnLicenseManager)
                self.btnDeRegister.clicked.connect(self.slotBtnDeRegister)
            else:
                self.btnLicenseManager.setVisible(False)
                self.cline5.setVisible(False)
                tRect = self.btnHelpHelp.geometry()
                self.btnHelpHelp.setGeometry(QRect(tRect.x(), tRect.y() - 33, tRect.width(), tRect.height()))
                tRect = self.btnAbout.geometry()
                self.btnAbout.setGeometry(QRect(tRect.x(), tRect.y() - 33, tRect.width(), tRect.height()))
        self.grpHelp.addButton(self.btnHelpHelp)
        self.grpHelp.addButton(self.btnAbout)
        self.slotGrpHelp(self.btnHelpHelp)
        self.grpRoot.buttonClicked.connect(self.slotGrpRoot)
        self.grpSettings.buttonClicked.connect(self.slotGrpSettings)
        self.grpHelp.buttonClicked.connect(self.slotGrpHelp)
        self.btnOutPath.clicked.connect(self.slotbtnOutPath)
        self.btnOutOK.clicked.connect(self.slotBtnOutOK)
        self.btnOutDefault.clicked.connect(self.slotBtnOutDefault)
        self.btnLangOK.clicked.connect(self.slotBtnLangOK)

    def slotGrpRoot(self, button):
        for i in self.grpRoot.buttons():
            if i is button:
                i.setStyleSheet('QToolButton{background-color: #4283DE; color: #FFFFFF; border: 0;}')
            else:
                i.setStyleSheet('QToolButton{background-color: #676767; color: #FFFFFF; border: 0;}QToolButton::hover{background-color: #4283DE;}')

        if button is self.btnSettings:
            self.stackRoot.setCurrentWidget(self.pageSettings)
        elif button is self.btnHelp:
            self.stackRoot.setCurrentWidget(self.pageHelp)

    def slotGrpSettings(self, button):
        for i in self.grpSettings.buttons():
            if i is button:
                i.setStyleSheet('QPushButton{text-align: right; background-color: #4283DE; color: #FFFFFF; border: 0;}')
            else:
                i.setStyleSheet('QPushButton{text-align: right;background-color: #FFFFFF; color: #000000; border: 0;}QPushButton::hover{background-color: #4283DE;color: #FFFFFF;}')

        if button is self.btnLang:
            self.stackSettings.setCurrentWidget(self.pageLang)
            index = 0
            self.cboxLang.clear()
            for key, value in MultiLanguage.items():
                self.cboxLang.addItem(value)
                if apps['app_language'] == key:
                    self.cboxLang.setCurrentIndex(index)
                index += 1

        elif button is self.btnOutput:
            self.stackSettings.setCurrentWidget(self.pageOutput)
            self.txtOutPath.setText(apps['outputpath'])

    def slotGrpHelp(self, button):
        for i in self.grpHelp.buttons():
            if i is button:
                i.setStyleSheet('QPushButton{text-align: right; background-color: #4283DE; color: #FFFFFF; border: 0;}')
            else:
                i.setStyleSheet('QPushButton{text-align: right;background-color: #FFFFFF; color: #000000; border: 0;}QPushButton::hover{background-color: #4283DE;color: #FFFFFF;}')

        if button is self.btnHelpHelp:
            self.stackHelp.setCurrentWidget(self.pageHelpHelp)
            if res.isEpubor:
                html = '<table width="100%" height="100%" border="0" cellpadding="0" cellspacing="0"><tr><td width="110" align="right">{0}: </td><td width="310" align="left"><a href="{1}">{2}</a></td><tr/><tr><td width="110" align="right">{3}: </td><td width="310" align="left"><a href="{4}">{5}</a></td><tr/><tr><td width="110" align="right">{6}: </td><td width="310" align="left"><a href="{7}">{8}</a></td><tr/><tr><td width="110" align="right">{9}: </td><td width="310" align="left"><a href="{10}">{11}</a></td><tr/><tr><td width="110" align="right">{12}: </td><td width="310" align="left"><a href="{13}">{14}</a></td></tr></table>'.format(tr('Tutorial'), res.guideLink + '?utm_medium=soft&utm_source=about&utm_campaign=about&utm_content=' + res.title.replace(' ', '') + '_' + res.product_id, res.guideText, tr('FAQ'), 'https://www.epubor.com/faq.html?utm_medium=soft&utm_source=help&utm_campaign=help&utm_content=' + res.title.replace(' ', '') + '_' + res.product_id, 'https://www.epubor.com/faq.html', tr('Live Chat'), 'http://chat.epubor.com/Chat/Live.aspx?sitename=epubor.com', 'http://chat.epubor.com/', tr('Ticket'), 'http://ticket.epubor.com/?utm_medium=soft&utm_source=help&utm_campaign=help&utm_content=' + res.title.replace(' ', '') + '_' + res.product_id, res.ticket, tr('Email'), 'mailto:' + res.author, res.author)
            else:
                html = '<table width="100%" height="100%" border="0" cellpadding="0" cellspacing="0"><tr><td width="110" align="right">{0}: </td><td width="310" align="left"><a href="{1}">{2}</a></td><tr/><tr><td width="110" align="right">{3}: </td><td width="310" align="left"><a href="{4}">{5}</a></td><tr/><tr><td width="110" align="right">{6}: </td><td width="310" align="left"><a href="{7}">{8}</a></td></tr></table>'.format(tr('Tutorial'), res.help + '?utm_medium=soft&utm_source=about&utm_campaign=about&utm_content=' + res.title.replace(' ', '') + '_' + res.product_id, res.help, tr('Ticket'), res.ticket + '/?utm_medium=soft&utm_source=help&utm_campaign=help&utm_content=' + res.title.replace(' ', '') + '_' + res.product_id, res.ticket, tr('Email'), 'mailto:' + res.author, res.author)
            self.labHelp.setText(html)
        else:
            if button is self.btnAbout:
                self.stackHelp.setCurrentWidget(self.pageAbout)
                if res.regInfo.isRegister:
                    txtLicense = res.regInfo.email
                else:
                    txtLicense = tr('Free Trial')
                txtHelp = txtCopyright = res.help + '?utm_medium=soft&utm_source=about&utm_campaign=about&utm_content=' + res.title.replace(' ', '') + '_' + res.product_id
                html = '<table width="100%" height="100%" border="0" cellpadding="0" cellspacing="0"><tr><td width="110" align="right">{0}: </td><td width="310" align="left"><b>{1}</b></td><tr/><tr><td width="110" align="right">{2}: </td><td width="310" align="left"><a href="{3}">{4}</a></td><tr/><tr><td width="110" align="right">{5}: </td><td width="310" align="left"><a href=mailto:"{6}">{7}</a></td><tr/><tr><td width="110" align="right">{8}: </td><td width="310" align="left"><a href="{9}">{10}</a></td><tr/><tr><td width="110" align="right">{11}: </td><td width="310" align="left"><a href="file:{12}">{13}</a></td></tr></table>'.format(tr('Licensed to'), txtLicense, tr('Copyright'), txtCopyright, res.copyright, tr('Support'), res.author, res.author, tr('Help'), txtHelp, res.help, tr('Output Path'), apps['outputpath'], apps['outputpath'])
                self.labAbout.setText(html)
            elif button is self.btnLicenseManager:
                self.stackHelp.setCurrentWidget(self.pageLicenseManager)

    def directory(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, tr('Set Path'), homepath, options)
        return os_sep(directory)

    def slotbtnOutPath(self):
        d = self.directory()
        if d:
            self.txtOutPath.setText(d)

    def slotBtnOutOK(self):
        apps['outputpath'] = self.txtOutPath.text()
        self.close()

    def slotBtnOutDefault(self):
        self.txtOutPath.setText(res.outputpath)

    def slotBtnLangOK(self):
        for key, value in MultiLanguage.items():
            if self.cboxLang.currentText() == value:
                QMessageBox.information(self, res.titleMsg, tr('Language change will take effect when you restart the application.'), QMessageBox.Ok)
                apps['app_language'] = key
                restart()
                break

    def slotBtnDeRegister(self):
        try:
            from settings.register import Register, RegAction_DeRegister
            email, licenseCode, retcode = self.parent.register.Register(res.regInfo.email, RegAction_DeRegister)
            if retcode == '0':
                res.regInfo.isRegister = False
                res.regInfo.email = apps['email'] = ''
                self.parent.btnReg.setVisible(True)
                self.close()
        except Exception as e:
            print(e)