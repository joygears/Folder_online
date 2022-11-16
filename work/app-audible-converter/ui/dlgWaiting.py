# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ui\dlgWaiting.py
from PyQt5.Qt import QDialog, Qt, QMovie, QSize
from ui.ui_dlgWaiting import Ui_dlgWaiting

class DlgWaiting(QDialog, Ui_dlgWaiting):

    def __init__(self, parent=None, message=''):
        super(DlgWaiting, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.resize(400, 80)
        self.labGif.setFixedSize(30, 30)
        movie = QMovie(':/imgs/pro.gif')
        movie.setScaledSize(QSize(25, 25))
        movie.start()
        self.labGif.setMovie(movie)
        self.labMessage.setText(message)