# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ui\dlgOption.py
import os
from PyQt5.Qt import QDialog, Qt, QIcon, QFontMetrics, QFileDialog
from settings.settings import apps, tr, res, homepath
from ui.ui_dlgOption import Ui_dlgOption

class AudibleMeta:

    def __init__(self, title='', album='', artist='', copyright='', year='', genre='', comments='', cover=''):
        self.title = title
        self.album = album
        self.artist = artist
        self.copyright = copyright
        self.year = year
        self.genre = genre
        self.comments = comments
        self.duration = ''
        self.checksum = ''
        self._AudibleMeta__cover = cover

    @property
    def cover(self):
        if os.path.exists(self._AudibleMeta__cover):
            return self._AudibleMeta__cover
        else:
            return res.defaultcover

    @cover.setter
    def cover(self, cover):
        self._AudibleMeta__cover = cover


class DlgOption(QDialog, Ui_dlgOption):

    def __init__(self, book, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(res.icon))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(res.title)
        self.parent = parent
        self.book = book
        self.display_meta(self.book.audibleMeta)
        self.openPath = homepath
        self.applyToAll = False
        self.checkBoxApplyToAll.setChecked(False)
        self.radioBtns = [
         self.radioBtnNoSplit, self.radioBtnSplitMinutes, self.radioBtnSplitFiles, self.radioBtnSplitChapters]
        splitIndex = book.splitMethod
        mcs = QFontMetrics(self.btnOK.font())
        self.btnOK.setMinimumSize(mcs.width(self.btnOK.text()) + 40, mcs.height() + 10)
        self.tabOption.setCurrentWidget(self.pageSplit)
        for i, btn in enumerate(self.radioBtns):
            btn.setChecked(i == splitIndex)

        self.spinBoxMinutes.setValue(book.splitMinutes)
        self.spinBoxFiles.setValue(book.splitFiles)
        self.spinBoxMinutes.setEnabled(splitIndex == 1)
        self.spinBoxFiles.setEnabled(splitIndex == 2)
        for btn in self.radioBtns:
            btn.toggled.connect(self.slotRadioButtonToggled)

        self.btnOK.clicked.connect(self.slotBtnOK)
        self.btnCover.clicked.connect(self.slotBtnCover)
        width = 0
        txt = ''
        for index in range(self.tabOption.count()):
            t = self.tabOption.tabText(index)
            if len(t) > len(txt):
                txt = t

        fm = QFontMetrics(self.tabOption.font())
        width = fm.width(txt) + 50
        style_tab = '\n        QTabWidget::pane { /* The tab widget frame */\n            border-top: 1px solid #C2C7CB;\n            border-bottom: 1px solid #C2C7CB;\n          }\n\n        QTabWidget::tab-bar {\n            left: 5px;\n        }\n\n          /* Style the tab using the tab sub-control. Note that\n              it reads QTabBar _not_ QTabWidget */\n          QTabBar::tab {\n              background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n                                          stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n                                          stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n              border: 1px solid #C4C4C3;\n                border-bottom: none;\n              border-bottom-color: #C2C7CB; /* same as the pane color */\n              border-top-left-radius: 4px;\n              border-top-right-radius: 4px;\n              /*min-width: 8ex;*/\n              padding: 2px;\n              width: %spx;\n              height: 25px;\n          }\n\n          QTabBar::tab:selected, QTabBar::tab:hover {\n              background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n                                          stop: 0 #fafafa, stop: 0.4 #f4f4f4,\n                                          stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);\n          }\n\n          QTabBar::tab:selected {\n              border-color: #9B9B9B;\n              border-bottom-color: #C2C7CB; /* same as pane color */\n          }\n\n          QTabBar::tab:!selected {\n              margin-top: 2px; /* make non-selected tabs look smaller */\n          }\n          /*\n          QTabBar::tab:selected {\n              margin-left: -4px;\n              margin-right: -4px;\n          }\n\n          QTabBar::tab:first:selected {\n              margin-left: 0; \n          }\n\n          QTabBar::tab:last:selected {\n              margin-right: 0;\n          }\n\n          QTabBar::tab:only-one {\n              margin: 0;\n        */\n          }\n        ' % width
        self.tabOption.setStyleSheet(style_tab)

    def getSplitMethod(self):
        for i, btn in enumerate(self.radioBtns):
            if btn.isChecked():
                return i

    def slotRadioButtonToggled(self):
        index = self.getSplitMethod()
        self.spinBoxMinutes.setEnabled(index == 1)
        self.spinBoxFiles.setEnabled(index == 2)

    def slotBtnOK(self):
        splitMethod = self.getSplitMethod()
        self.book.splitMethod = splitMethod
        self.book.splitMinutes = self.spinBoxMinutes.value()
        self.book.splitFiles = self.spinBoxFiles.value()
        if splitMethod == 0:
            self.book.convertParam = (0, None)
        else:
            if splitMethod == 1:
                self.book.convertParam = (
                 1, self.book.splitMinutes)
            else:
                if splitMethod == 2:
                    self.book.convertParam = (
                     2, self.book.splitFiles)
                else:
                    if splitMethod == 3:
                        self.book.convertParam = (3, None)
        self.applyToAll = self.checkBoxApplyToAll.isChecked()
        self.set_meta()
        self.close()

    def set_meta(self):
        meta = self.book.audibleMeta
        meta.title = self.txtTitle.text().strip()
        meta.album = self.txtAlbum.text().strip()
        meta.artist = self.txtArtist.text().strip()
        meta.copyright = self.txtCopyright.text().strip()
        meta.year = self.txtYear.text().strip()
        meta.genre = self.comboxGenre.currentText()
        meta.comments = self.txtComments.toPlainText().strip()

    def display_meta(self, meta):
        self.txtTitle.setText(meta.title)
        self.txtAlbum.setText(meta.album)
        self.txtArtist.setText(meta.artist)
        self.txtCopyright.setText(meta.copyright)
        self.txtYear.setText(meta.year)
        self.txtComments.setPlainText(meta.comments)
        self.display_cover(meta.cover)
        items = [self.comboxGenre.itemText(i) for i in range(self.comboxGenre.count())]
        index = 0
        if meta.genre in items:
            index = items.index(meta.genre)
        self.comboxGenre.setCurrentIndex(index)
        self.txtTitle.setCursorPosition(0)
        self.txtAlbum.setCursorPosition(0)
        self.txtArtist.setCursorPosition(0)
        self.txtCopyright.setCursorPosition(0)
        self.txtYear.setCursorPosition(0)

    def display_cover(self, cover):
        style_cover = '\n        QPushButton {\n            border-image: url(%s);\n        }\n        ' % cover.replace('\\', '/')
        self.btnCover.setStyleSheet(style_cover)

    def slotBtnCover(self):
        coverpath = QFileDialog.getOpenFileName(self, tr('Choose Cover Image'), self.openPath, 'Images (*.png;*.jpg;*.jpeg)')
        if coverpath:
            if coverpath[0]:
                self.book.audibleMeta.cover = coverpath[0]
                self.display_cover(coverpath[0])