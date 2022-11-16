# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ui\tables.py
import sys, os, threading, shutil, subprocess, webbrowser
from queue import Queue
from PyQt5.QtCore import QObject, Qt, pyqtSignal, QAbstractTableModel, QSize, QEvent, QModelIndex, QThread
from PyQt5.QtWidgets import QStackedWidget, QMessageBox, QStyledItemDelegate, QStyle, QStyleOptionToolButton, QApplication, QToolTip, QHeaderView, QMenu, QAction, QTableView
from PyQt5.QtGui import QColor, QPixmap, QIcon, QPalette, QCursor, QMovie
from PyQt5.Qt import QRect, QMouseEvent
from settings.settings import res, tr, apps, STYLE_SCROLLBAR, isblind
from settings.functions import explorer_select_files, os_sep
from ui.dlgOption import DlgOption, AudibleMeta
from ui.dlgTrial import DlgTrial
from module.logger import logger
from settings.audible import AudibleConvert
NOT_CONVERT = 0
CONVERTING = 1
CONVERT_OK = 2
CONVERT_FAILED = 3

class ItemTable:

    def __init__(self, filepath='', filetype='', audibleMeta=None):
        self.filepath = filepath
        self.filetype = filetype
        self.audibleMeta = audibleMeta
        self.isconverting = False
        self.covLog = ''
        self.outfilepath = ''
        self.covStatus = NOT_CONVERT
        self.rate = 0
        self.splitMethod = 0
        self.splitMinutes = 1
        self.splitFiles = 1
        self.convertParam = (0, None)


class StackRight(QStackedWidget):
    signalDragFiles = pyqtSignal(object)

    def __init__(self, parent=None):
        QStackedWidget.__init__(self, parent)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
            files = []
            for i in event.mimeData().urls():
                url = os.path.abspath(i.toLocalFile())
                if i.toString().startswith('file:///.file/id='):
                    args = ['osascript', '-e']
                    f = 'get posix path of my posix file "%s" -- kthx. bai' % i.toString()
                    args.append(f)
                    result = subprocess.Popen(args=args, stdout=(subprocess.PIPE))
                    r = result.stdout.read().decode()
                    src = r.replace('\n', '')
                    files.append(src)
                else:
                    files.append(url)

            self.signalDragFiles.emit(files)
        else:
            event.ignore()


def repaint_widget(widget):
    widget.resize(widget.size() + QSize(1, 0))
    widget.resize(widget.size() + QSize(-1, 0))


class TableDelegate(QStyledItemDelegate):
    signalOption = pyqtSignal(object)
    signalDel = pyqtSignal(object)
    signalStatus = pyqtSignal(object)

    def __init__(self, items=[], parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self.items = items
        self.parent = parent
        self.optionState = self.delState = self.statusState = QStyle.State_Enabled
        self.optionRect = [45, 20, -50, -35]
        self.delRect = [85, 20, -50, -35]
        self.statusRect = [20, 45, 0, -10]
        self.signalOption.connect(self.parent.slotOption)
        self.signalDel.connect(self.parent.slotDel)
        self.signalStatus.connect(self.parent.slotStatus)

    def getRect(self, orgRect):
        x = orgRect.x()
        y = orgRect.y()
        width = orgRect.width()
        height = orgRect.height()
        icon_size = 20
        optionRect = QRect(x + (width - icon_size * 2) / 3 + 12, y + height / 2 - icon_size, icon_size, icon_size)
        delRect = QRect(x + (width - icon_size * 2) / 3 * 2 + 6, y + height / 2 - icon_size, icon_size, icon_size)
        statusRect = QRect(x + (width - icon_size * 2) / 3 - 32, y + height / 2 - 2 - 4, width - 10, height / 2 + 4)
        return (optionRect, delRect, statusRect)

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, index)
        rect = option.rect
        x = rect.x()
        y = rect.y()
        width = rect.width()
        height = rect.height()
        painter.setPen(QColor('#D7D7D7'))
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        optionRect, delRect, statusRect = self.getRect(rect)
        item = self.items[index.row()]
        if index.column() == 0:
            w = 38
            h = 50
            coverRect = QRect(x + (width - w) / 2, y + (height - h) / 2, w, h)
            painter.drawPixmap(coverRect, QPixmap(item.audibleMeta.cover))
        else:
            if index.column() == 1:
                pass
            else:
                if index.column() == 2:
                    if item.audibleMeta.duration:
                        btnDuration = QStyleOptionToolButton()
                        btnDuration.rect = QRect(rect.x(), rect.y(), rect.width(), rect.height() / 4 * 3)
                        btnDuration.iconSize = QSize(16, 16)
                        btnDuration.icon = QIcon(QPixmap(':imgs/clock.png'))
                        btnDuration.state = self.statusState | QStyle.State_Enabled
                        duration = item.audibleMeta.duration
                        tPos = duration.find('.')
                        if tPos > 0:
                            duration = duration[:tPos]
                        btnDuration.text = duration
                        btnDuration.toolButtonStyle = Qt.ToolButtonTextBesideIcon
                        QApplication.style().drawControl(QStyle.CE_ToolButtonLabel, btnDuration, painter)
                elif index.column() == 3:
                    icon_size = 20
                    btnOption = QStyleOptionToolButton()
                    btnOption.rect = optionRect
                    btnOption.iconSize = QSize(icon_size, icon_size)
                    btnOption.icon = QIcon(QPixmap(':imgs/edit.png'))
                    btnOption.state = self.optionState | QStyle.State_Enabled
                    QApplication.style().drawControl(QStyle.CE_ToolButtonLabel, btnOption, painter)
                    btnDel = QStyleOptionToolButton()
                    btnDel.rect = delRect
                    btnDel.iconSize = QSize(icon_size, icon_size)
                    btnDel.icon = QIcon(QPixmap(':imgs/del.png'))
                    btnDel.state = self.delState | QStyle.State_Enabled
                    QApplication.style().drawControl(QStyle.CE_ToolButtonLabel, btnDel, painter)
                    covStatus = item.covStatus
                    if covStatus == NOT_CONVERT:
                        return
                    btnStatus = QStyleOptionToolButton()
                    btnStatus.rect = statusRect
                    btnStatus.state = self.statusState | QStyle.State_Enabled
                    color = ''
                    if covStatus == CONVERTING:
                        rate = item.rate
                        x = statusRect.x() + 10
                        y = statusRect.y()
                        width = statusRect.width() - 20
                        height = statusRect.height()
                        rate_width = int(width * rate / 100)
                        painter.fillRect(x, y + height - 10, rate_width, 5, QColor('#1E78BA'))
                        painter.fillRect(x + rate_width, y + height - 10, width - rate_width, 5, QColor('#404040'))
                        btnStatus.text = str(item.rate) + '%'
                        color = '#F40'
                    else:
                        if covStatus == CONVERT_OK:
                            btnStatus.text = tr('Succeeded')
                            color = '#000000'
                        else:
                            if covStatus == CONVERT_FAILED:
                                btnStatus.text = tr('Failed')
                                color = '#FF0000'
                            palette = QPalette()
                            palette.setColor(QPalette.ButtonText, QColor(color))
                            btnStatus.palette = palette
                            QApplication.style().drawControl(QStyle.CE_ToolButtonLabel, btnStatus, painter)

    def editorEvent(self, event, model, option, index):
        if index.column() == 3 and isinstance(event, QMouseEvent):
            optionRect, delRect, statusRect = self.getRect(option.rect)
            if optionRect.contains(event.pos()):
                if event.type() == QEvent.MouseMove:
                    self.optionState = QStyle.State_MouseOver
                    QToolTip.showText(QCursor.pos(), tr('Option'))
                    return True
                else:
                    if event.type() == QEvent.MouseButtonPress:
                        self.optionState = QStyle.State_Sunken
                        return True
                    if event.type() == QEvent.MouseButtonRelease:
                        self.optionState = QStyle.State_MouseOver
                        self.signalOption.emit(index.row())
                        return True
            else:
                if delRect.contains(event.pos()):
                    if event.type() == QEvent.MouseMove:
                        self.delState = QStyle.State_MouseOver
                        QToolTip.showText(QCursor.pos(), tr('Delete item'))
                        return True
                    if event.type() == QEvent.MouseButtonPress:
                        self.delState = QStyle.State_Sunken
                        return True
                    if event.type() == QEvent.MouseButtonRelease:
                        self.delState = QStyle.State_MouseOver
                        self.signalDel.emit(index.row())
                        return True
                elif statusRect.contains(event.pos()):
                    if event.type() == QEvent.MouseMove:
                        self.statusState = QStyle.State_MouseOver
                        return True
                    if event.type() == QEvent.MouseButtonPress:
                        self.statusState = QStyle.State_Sunken
                        return True
                    if event.type() == QEvent.MouseButtonRelease:
                        self.statusState = QStyle.State_MouseOver
                        self.signalStatus.emit(self.items[index.row()])
                        return True
        return False


class TableModel(QAbstractTableModel):

    def __init__(self, items=[], parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.items = items
        self.parent = parent

    def rowCount(self, index):
        return len(self.items)

    def columnCount(self, index):
        return 4

    def data(self, index, role):
        item = self.items[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 1:
                return item.audibleMeta.title + '\n\n' + item.audibleMeta.artist
        elif role == Qt.BackgroundRole:
            if item.isconverting:
                return QColor('#BCDCF4')
            return QColor('#FFFFFF')

    def removeRows(self, row, count, index):
        self.beginRemoveRows(index, row, row + count - 1)
        self.endRemoveRows()
        return True

    def insertRows(self, row, count, index):
        self.beginInsertRows(index, row, row + count - 1)
        self.endInsertRows()
        return True


class TableBook(QTableView):
    signalKeyDel = pyqtSignal()

    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.parent = parent
        self.parentMainWindow = None

    def setParentMainWindow(self, mainWindow):
        self.parentMainWindow = mainWindow

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.signalKeyDel.emit()
        else:
            if event.key() == Qt.Key_Tab:
                try:
                    self.parentMainWindow.setFocus(Qt.OtherFocusReason)
                except Exception as e:
                    print('******tab', e)

        QTableView.keyPressEvent(self, event)


class Tables(QObject):
    signalConverting = pyqtSignal(object)
    signalRate = pyqtSignal(object)
    signalCovFinished = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.parent = parent
        self.itemTables = []
        self.itemTablesLeftCount = 0
        self.isCoverting = False
        self.tableBook = self.parent.tableBook
        self.tableBook.setMouseTracking(True)
        s = self.tableBook.style()
        self.tableBook.setStyle(res.styled)
        self.tableBook.verticalHeader().setStyle(s)
        self.tableBook.setStyleSheet('#tableBook {selection-background-color: #E7E6E6; selection-color: #000000;}')
        self.tableBook.verticalScrollBar().setStyleSheet(STYLE_SCROLLBAR)
        self.tableModel = TableModel(self.itemTables, self)
        self.tableDelegate = TableDelegate(self.itemTables, self)
        self.tableBook.setModel(self.tableModel)
        self.tableBook.setItemDelegate(self.tableDelegate)
        self.tableBook.setColumnWidth(0, 80)
        self.tableBook.setColumnWidth(2, 100)
        self.tableBook.setColumnWidth(3, 150)
        self.tableBook.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableBook.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableBook.verticalHeader().setDefaultSectionSize(70)
        self.tableBook.setParentMainWindow(self.parent)
        self.parent.labCovNum.setVisible(False)
        self.parent.labCovGif.setVisible(False)
        m = QMovie(':imgs/working.gif')
        m.setSpeed(50)
        m.setScaledSize(QSize(20, 20))
        self.parent.labCovGif.setMovie(m)
        m.start()
        self.audible = AudibleConvert(res.usrpath)
        self.signalConverting.connect(self.slotConverting)
        self.signalRate.connect(self.slotRate)
        self.signalCovFinished.connect(self.slotCovFinished)
        self.tableBook.customContextMenuRequested.connect(self.slotTableContextMenu)
        self.tableBook.signalKeyDel.connect(self.slotActionRemoveItems)

    def getIndex(self, file):
        for i, item in enumerate(self.itemTables):
            if file == item.filepath:
                return i

        return -1

    def addFiles(self, files):
        if self.isCoverting:
            return
        else:
            txtWarning = ''
            txtAaxc = ''
            for file in files:
                file = os_sep(file)
                if os.path.isfile(file) and self.getIndex(file) < 0:
                    filetype = self.audible.check_type(file)
                    if filetype:
                        meta = self.audible.getMeta(file)
                        if meta:
                            itemTable = ItemTable(filepath=file, filetype=filetype, audibleMeta=meta)
                            self.itemTables.append(itemTable)
                            index = len(self.itemTables)
                            self.tableModel.insertRow(index - 1, QModelIndex())
                        else:
                            txtWarning += file + '<br/>'
                    else:
                        if self.audible.is_aaxc(file):
                            txtAaxc += file + '<br/>'
                        else:
                            txtWarning += file + '<br/>'

            if txtWarning or txtAaxc:
                url = res.copyright + 'how-to-listen-and-download-audible-books-on-computer.html' + '?utm_medium=soft&utm_source=help&utm_campaign=help&utm_content=' + res.title.replace(' ', '') + '_' + res.product_id + '#P2'
                msg_unsupport = '<html><body>' + tr('Unsupported format:') + '<br/>' + txtWarning + tr('Please &nbsp;') + '<b>' + tr('Add') + " <a href='" + url + "'>" + 'AA/AAX' + '</a> ' + tr('Format Audible Books') + '</b></body></html>'
                msg_aaxc = '<html><body>' + tr('Unsupported format:') + '<br/>' + txtAaxc + tr('Please &nbsp;') + '<b>' + tr('download') + " <a href='" + url + "'> " + tr('Audible books') + '</a> ' + tr('on Windows/Mac') + '.</b></body></html>'
                message = ''
                if txtWarning:
                    if txtAaxc:
                        message = msg_unsupport + '<br/>' + msg_aaxc
                if txtWarning:
                    if not txtAaxc:
                        message = msg_unsupport
                if not txtWarning:
                    if txtAaxc:
                        message = msg_aaxc
                print('message', type(message), message)
                QMessageBox.warning(self.parent, res.titleMsg, message)
            if not self.itemTables:
                return
        self.parent.stackRight.setCurrentWidget(self.parent.pageTable)
        self.tableBook.scrollToBottom()

    def slotOption(self, row):
        if self.isCoverting:
            return
        else:
            if res.regInfo.isRegister:
                dlgOption = DlgOption(self.itemTables[row])
                dlgOption.exec_()
                item = dlgOption.book
                if dlgOption.applyToAll:
                    for i in range(len(self.itemTables)):
                        self.itemTables[i].convertParam = item.convertParam
                        self.itemTables[i].splitMethod = item.splitMethod
                        self.itemTables[i].splitMinutes = item.splitMinutes
                        self.itemTables[i].splitFiles = item.splitFiles

                else:
                    self.itemTables[row].convertParam = item.convertParam
                    self.itemTables[row].splitMethod = item.splitMethod
                    self.itemTables[row].splitMinutes = item.splitMinutes
                    self.itemTables[row].splitFiles = item.splitFiles
            else:
                dlgTrial = DlgTrial(self.parent)
                dlgTrial.exec_()

    def slotDel(self, row):
        if self.isCoverting:
            return
        self.tableModel.removeRow(row, QModelIndex())
        self.itemTables.pop(row)
        if not self.itemTables:
            self.parent.stackRight.setCurrentWidget(self.parent.pageBackground)

    def slotStatus(self, item):
        covStatus = item.covStatus
        if covStatus == NOT_CONVERT:
            return
        if covStatus == CONVERTING:
            return
        if covStatus == CONVERT_OK:
            explorer_select_files([item.outfilepath])

    def convert(self, ext, chapters=False):
        if not self.itemTables:
            return
        q = Queue()
        for item in self.itemTables:
            item.isconverting = False
            item.covLog = ''
            item.outfilepath = ''
            item.rate = 0
            item.covStatus = NOT_CONVERT
            if isblind:
                if chapters:
                    item.convertParam = (3, None)
                else:
                    item.convertParam = (0, None)
            q.put(item)

        self.itemTablesLeftCount = q.qsize()
        if self.itemTablesLeftCount <= 0:
            return
        self.covLeft()
        self.parent.labCovNum.setVisible(True)
        self.parent.labCovGif.setVisible(True)
        tCount = 1
        self.covUIEnable(iscoverting=True)
        self.audible.setSettings(apps['outputpath'], res.regInfo.isRegister)
        for i in range(tCount):
            cov = ThreadCov(ext=ext, q=q, parent=self)
            cov.start()

    def slotConverting(self, item):
        index = self.getIndex(item.filepath)
        self.tableBook.selectRow(index)
        self.tableBook.clearSelection()

    def slotRate(self, item):
        index = self.getIndex(item.filepath)
        self.itemTables[index].rate = item.rate
        repaint_widget(self.tableBook)

    def slotCovFinished(self):
        self.itemTablesLeftCount -= 1
        self.covLeft()
        if self.itemTablesLeftCount <= 0:
            self.parent.labCovNum.setText('')
            self.parent.labCovNum.setVisible(False)
            self.parent.labCovGif.setVisible(False)
            files = []
            for i in self.itemTables:
                if os.path.exists(i.outfilepath):
                    files.append(i.outfilepath)

            explorer_select_files(files)
            self.covUIEnable(iscoverting=False)

    def covLeft(self):
        msg = tr('files') if self.itemTablesLeftCount > 1 else tr('file')
        self.parent.labCovNum.setText('<b style="color:#4283D4">' + tr('Converting') + '&nbsp;<span style="color:red">%d</span>&nbsp;' % self.itemTablesLeftCount + msg + '</b>')

    def slotTableContextMenu(self):

        def hideAction(cov):
            indexes = self.tableBook.selectionModel().selectedRows()
            for i in indexes:
                if os.path.exists(self.itemTables[i.row()].outfilepath):
                    cov.setVisible(True)

        if self.isCoverting:
            return
        if self.tableBook.selectionModel().selectedRows():
            menu = QMenu()
            actionSrcFile = QAction(QIcon(':/imgs/open.png'), tr('Explore source file'), self.tableBook)
            actionCovFile = QAction(QIcon(':/imgs/open.png'), tr('Explore converted file'), self.tableBook)
            actionRemoveItems = QAction(QIcon(':/imgs/del.png'), tr('Remove selected item(s)'), self.tableBook)
            actionRemoveAll = QAction(QIcon(':/imgs/empty.png'), tr('Remove all items'), self.tableBook)
            menu.addAction(actionSrcFile)
            menu.addAction(actionCovFile)
            menu.addAction(actionRemoveItems)
            menu.addAction(actionRemoveAll)
            actionSrcFile.triggered.connect(self.slotActionSrcFile)
            actionCovFile.triggered.connect(self.slotActionCovFile)
            actionRemoveItems.triggered.connect(self.slotActionRemoveItems)
            actionRemoveAll.triggered.connect(self.slotActionRemoveAll)
            menu.move(QCursor.pos())
            actionCovFile.setVisible(False)
            hideAction(actionCovFile)
            menu.exec_()

    def slotActionSrcFile(self):
        indexes = self.tableBook.selectionModel().selectedRows()
        for i in indexes:
            explorer_select_files([self.itemTables[i.row()].filepath])
            return

    def slotActionCovFile(self):
        indexes = self.tableBook.selectionModel().selectedRows()
        files = []
        for i in indexes:
            files.append(self.itemTables[i.row()].outfilepath)

        explorer_select_files(files)

    def slotActionRemoveItems(self):

        def getrow():
            indexes = self.tableBook.selectionModel().selectedRows()
            for i in indexes:
                return i.row()

            return -1

        while True:
            row = getrow()
            if row < 0:
                break
            self.slotDel(row)

    def slotActionRemoveAll(self):
        self.tableModel.removeRows(0, len(self.itemTables), QModelIndex())
        self.itemTables.clear()
        self.parent.stackRight.setCurrentWidget(self.parent.pageBackground)

    def covUIEnable(self, iscoverting=False):
        self.isCoverting = iscoverting
        tEnabled = not iscoverting
        self.parent.btnAdd.setEnabled(tEnabled)
        self.parent.btnCov.setEnabled(tEnabled)
        self.parent.btnFormat.setEnabled(tEnabled)
        if not res.regInfo.isRegister:
            self.parent.btnReg.setEnabled(tEnabled)
        self.parent.btnSettings.setEnabled(tEnabled)


class ThreadCov(QThread):

    def __init__(self, ext='', q=None, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
        self.ext = ext
        self.q = q
        self.process = self.parent.audible.process

    def run(self):
        while True:
            item = self.q.get()
            item.isconverting = True
            item.covStatus = CONVERTING
            self.parent.signalConverting.emit(item)
            dst, error = self.cov(item)
            if dst:
                item.covStatus = CONVERT_OK
                item.outfilepath = dst
            else:
                item.covStatus = CONVERT_FAILED
                item.outfilepath = ''
                item.covLog = tr('Failed with converting Audible File') + ': ' + error
            item.isconverting = False
            self.parent.signalConverting.emit(item)

    def cov(self, item):
        try:
            try:
                logger.debug('Start convert audible file.')
                dst = self.process(item, self.ext, self.parent.signalRate)
                error = ''
            except Exception as e:
                logger.error('Failed with converting Audible File:' + str(e))
                dst = ''
                error = repr(e)

        finally:
            self.parent.signalCovFinished.emit()

        return (dst, error)