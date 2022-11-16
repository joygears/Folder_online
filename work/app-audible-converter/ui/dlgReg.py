# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ui\dlgReg.py
import webbrowser, threading
from PyQt5.Qt import QDialog, QMessageBox, Qt, pyqtSignal
from settings.settings import apps, tr, res
from ui.ui_dlgReg import Ui_dlgReg
from ui.dlgWaiting import DlgWaiting
from settings.register import RegAction_Register

class DlgReg(QDialog, Ui_dlgReg):
    signalRegister = pyqtSignal(object, object, object)
    signalCloseWaiting = pyqtSignal()

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.parent = parent
        self.position = self.btnClose.pos()
        self.labTitle.setText(res.title)
        self.labInfo.setText(res.descryption)
        self.btnBuy.setText(tr('ONLY') + ' $' + str(res.price))
        txtUrl = '<a href="' + res.help + '?utm_medium=soft&utm_source=register&utm_campaign=register&utm_content=' + res.title.replace(' ', '') + '_' + res.product_id + '">' + res.help + '</a>'
        self.labUrl.setText(txtUrl)
        self.txtMail.setPlaceholderText(tr('Please input the licensed email'))
        self.txtMail.returnPressed.connect(self.slotBtnReg)
        self.btnTrial.clicked.connect(self.close)
        self.btnClose.clicked.connect(self.close)
        self.btnClose2.clicked.connect(self.close)
        self.btnBuy.clicked.connect(self.slotBtnBuy)
        self.btnReg.clicked.connect(self.slotBtnReg)
        self.signalRegister.connect(self.slotRegister)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if event.pos().y() < 50:
                self.move(event.globalPos() - self.position)
                event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def slotBtnBuy(self):
        webbrowser.open(res.help.replace('.html', '-order.htm') + '?utm_medium=soft&utm_source=register&utm_campaign=register&utm_content=' + res.title.replace(' ', '') + '_' + res.product_id + res.ordertag)

    def slotBtnReg(self):
        dlgWaiting = DlgWaiting(parent=self, message=(tr('Please wait for registration!')))
        self.signalCloseWaiting.connect(dlgWaiting.close)
        threading.Thread(target=(self.th_register), args=(self.txtMail.text().strip(), RegAction_Register), daemon=True).start()
        dlgWaiting.exec_()

    def th_register(self, email, action):
        email, licenseCode, retcode = self.parent.register.Register(email, action)
        self.signalCloseWaiting.emit()
        self.signalRegister.emit(email, licenseCode, retcode)

    def slotRegister(self, email, licenseCode, retcode):
        if retcode == '0':
            apps['email'] = email.lower()
            if licenseCode:
                apps['email'] += ';' + licenseCode
            res.regInfo.isRegister = True
            res.regInfo.email = email.lower()
            res.regInfo.licenseCode = licenseCode
            QMessageBox.information(self, res.titleMsg, tr('Successfully registered!') + '\n', QMessageBox.Ok, QMessageBox.Ok)
            self.parent.btnReg.setVisible(False)
            self.close()
        else:
            errMsg = ''
            if retcode != 'NoQMessageBox':
                errMsg = retcode + '\n\n' + tr("If you've puchased the software, please contact support@epubor.com.")
            else:
                errMsg = licenseCode
            QMessageBox.critical(self, res.titleMsg, errMsg, QMessageBox.Ok, QMessageBox.Ok)