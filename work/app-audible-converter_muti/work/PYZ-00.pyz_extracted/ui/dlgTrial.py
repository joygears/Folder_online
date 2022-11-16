# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ui\dlgTrial.py
import webbrowser
from PyQt5.Qt import QDialog, QFontMetrics, Qt
from ui.ui_dlgTrial import Ui_dlgTrial
from settings.settings import res

class DlgTrial(QDialog, Ui_dlgTrial):

    def __init__(self, parent):
        super(DlgTrial, self).__init__(parent)
        self.setupUi(self)
        self.resize(480, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        mcs_trial = QFontMetrics(self.btnTrial.font())
        self.btnTrial.setMinimumSize(mcs_trial.width(self.btnTrial.text()) + 20, mcs_trial.height() + 15)
        mcs_upgrade = QFontMetrics(self.btnUpgrade.font())
        self.btnUpgrade.setMinimumSize(mcs_upgrade.width(self.btnUpgrade.text()) + 20, mcs_upgrade.height() + 15)
        self.btnTrial.clicked.connect(self.close)
        self.btnUpgrade.clicked.connect(self.slotBtnUpgrade)

    def slotBtnUpgrade(self):
        link = res.help.replace('.html', '-order.htm') + '?utm_medium=' + res.tag_utm_medium + '&utm_source=upgrade&utm_campaign=' + res.tag_utm_campaign + '&utm_content=' + res.title.replace(' ', '') + '_' + res.product_id + res.tag_utm_affiliate + res.ordertag
        webbrowser.open(link)