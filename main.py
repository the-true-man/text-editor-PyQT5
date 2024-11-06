import datetime
import webbrowser
from PyQt5 import QtCore, QtWidgets, Qt, QtGui
from PyQt5.QtWidgets import QFileDialog, QFontDialog, QFrame, QInputDialog, QMessageBox
from PyQt5.QtPrintSupport import QPageSetupDialog
from PyQt5.QtCore import QSettings, QUrl
from PyQt5.QtGui import QFont, QDesktopServices, QIntValidator
import os


class dialogGoWindow(QtWidgets.QMainWindow):
    def __init__(self, mainText: QtWidgets.QPlainTextEdit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Переход на строку')
        self.setFixedSize(500, 120)
        self.mainText = mainText
        self.main_layout = QtWidgets.QGridLayout()
        self.vbox_1 = QtWidgets.QHBoxLayout()
        self.vbox_2 = QtWidgets.QVBoxLayout()

        self.row1_layout = QtWidgets.QHBoxLayout()
        self.labelThat = QtWidgets.QLabel("Номер строки:")
        self.text = QtWidgets.QLineEdit()
        self.text.setValidator(QIntValidator())
        self.text.setStyleSheet("font-size: 15px")
        self.labelThat.setStyleSheet("font-size: 15px")
        self.row1_layout.addWidget(self.labelThat)
        self.row1_layout.addWidget(self.text)
        self.vbox_1.addLayout(self.row1_layout)

        self.row3_layout = QtWidgets.QHBoxLayout()
        self.button_search = QtWidgets.QPushButton("Переход")
        self.button_search.clicked.connect(lambda: self.findLine())
        self.button_cancel = QtWidgets.QPushButton("Отмена")
        self.button_cancel.clicked.connect(lambda: self.close())
        self.row3_layout.addWidget(self.button_search)
        self.row3_layout.addWidget(self.button_cancel)
        self.vbox_2.addLayout(self.row3_layout)
        self.vbox_2.setContentsMargins(10, 37, 0, 10)
        self.main_layout.addLayout(self.vbox_1, 0, 0)
        self.main_layout.addLayout(self.vbox_2, 1, 0)

        self.central = QtWidgets.QWidget()
        self.central.setLayout(self.main_layout)
        self.setCentralWidget(self.central)

    def findLine(self):
        if not self.text.text():
            return
        line_number = int(''.join(self.text.text().split()))
        if line_number > self.mainText.document().blockCount():
            QtWidgets.QMessageBox.information(self, "Блокнот - Переход на строку",
                                              "Номер строки превышает общее число строк")
            return
        cursor = self.mainText.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        for i in range(line_number - 1):
            cursor.movePosition(QtGui.QTextCursor.Down)
        self.mainText.setTextCursor(cursor)
        self.close()


class dialogFindWindow(QtWidgets.QMainWindow):
    def __init__(self, text, mainText, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Найти')
        self.setFixedSize(500, 120)
        self.text = text
        self.mainText = mainText
        self.main_layout = QtWidgets.QGridLayout()
        self.vbox_1 = QtWidgets.QVBoxLayout()
        self.vbox_2 = QtWidgets.QVBoxLayout()

        self.row1_layout = QtWidgets.QHBoxLayout()
        self.labelThat = QtWidgets.QLabel("Что:")
        self.textThat = QtWidgets.QLineEdit()
        self.textThat.setStyleSheet("font-size: 15px")
        self.labelThat.setStyleSheet("font-size: 15px")
        self.row1_layout.addWidget(self.labelThat)
        self.row1_layout.addWidget(self.textThat)
        self.vbox_1.addLayout(self.row1_layout)

        self.row3_layout = QtWidgets.QVBoxLayout()
        self.button_search = QtWidgets.QPushButton("Найти далее")
        self.button_search.clicked.connect(lambda: self.search())
        self.button_cancel = QtWidgets.QPushButton("Отмена")
        self.button_cancel.clicked.connect(lambda: self.close())
        self.row3_layout.addWidget(self.button_search)
        self.row3_layout.addWidget(self.button_cancel)
        self.vbox_2.addLayout(self.row3_layout)
        self.vbox_2.setContentsMargins(10, 37, 0, 10)
        self.main_layout.addLayout(self.vbox_1, 0, 0)
        self.main_layout.addLayout(self.vbox_2, 0, 1)

        self.central = QtWidgets.QWidget()
        self.central.setLayout(self.main_layout)
        self.setCentralWidget(self.central)

    def search(self):
        text = self.mainText.toPlainText()
        cursor_position = self.mainText.textCursor().position()
        index = text.find(self.textThat.text(), cursor_position)
        if index != -1:
            cursor = self.mainText.textCursor()
            cursor.setPosition(index)
            cursor.setPosition(index + len(self.textThat.text()), Qt.QTextCursor.KeepAnchor)
            self.mainText.setTextCursor(cursor)
        else:
            QMessageBox.information(self, "Блокнот", f'Не удается найти "{self.textThat.text()}"')


class dialogReplaceWindow(QtWidgets.QMainWindow):
    def __init__(self, text, mainText, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Заменить')
        self.setFixedSize(500, 165)
        self.text = text
        self.mainText = mainText
        self.main_layout = QtWidgets.QGridLayout()
        self.vbox_1 = QtWidgets.QVBoxLayout()
        self.vbox_2 = QtWidgets.QVBoxLayout()

        self.row1_layout = QtWidgets.QHBoxLayout()
        self.labelThat = QtWidgets.QLabel("Что:")
        self.textThat = QtWidgets.QLineEdit()
        self.textThat.setStyleSheet("font-size: 15px")
        self.labelThat.setStyleSheet("font-size: 15px")
        self.row1_layout.addWidget(self.labelThat)
        self.row1_layout.addWidget(self.textThat)
        self.vbox_1.addLayout(self.row1_layout)

        self.row2_layout = QtWidgets.QHBoxLayout()
        self.labelThen = QtWidgets.QLabel("Чем:")
        self.textThen = QtWidgets.QLineEdit()
        self.labelThen.setStyleSheet("font-size: 15px")
        self.textThen.setStyleSheet("font-size: 15px")
        self.row2_layout.addWidget(self.labelThen)
        self.row2_layout.addWidget(self.textThen)
        self.vbox_1.addLayout(self.row2_layout)
        self.vbox_1.setContentsMargins(10, 0, 0, 60)

        self.row3_layout = QtWidgets.QVBoxLayout()
        self.button_search = QtWidgets.QPushButton("Найти далее")
        self.button_search.clicked.connect(lambda: self.search())
        self.button_replace = QtWidgets.QPushButton("Заменить")
        self.button_replace.clicked.connect(lambda: self.replace())
        self.button_replace_all = QtWidgets.QPushButton("Заменить все")
        self.button_replace_all.clicked.connect(lambda: self.replace_all())
        self.button_cancel = QtWidgets.QPushButton("Отмена")
        self.button_cancel.clicked.connect(lambda: self.close())
        self.row3_layout.addWidget(self.button_search)
        self.row3_layout.addWidget(self.button_replace)
        self.row3_layout.addWidget(self.button_replace_all)
        self.row3_layout.addWidget(self.button_cancel)
        self.vbox_2.addLayout(self.row3_layout)
        self.vbox_2.setContentsMargins(10, 0, 0, 10)
        self.main_layout.addLayout(self.vbox_1, 0, 0)
        self.main_layout.addLayout(self.vbox_2, 0, 1)

        self.central = QtWidgets.QWidget()
        self.central.setLayout(self.main_layout)
        self.setCentralWidget(self.central)

    def search(self):
        text = self.mainText.toPlainText()
        cursor_position = self.mainText.textCursor().position()
        index = text.find(self.textThat.text(), cursor_position)
        if index != -1:
            cursor = self.mainText.textCursor()
            cursor.setPosition(index)
            cursor.setPosition(index + len(self.textThat.text()), Qt.QTextCursor.KeepAnchor)
            self.mainText.setTextCursor(cursor)
        else:
            QMessageBox.information(self, "Блокнот", f'Не удается найти "{self.textThat.text()}"')

    def replace_all(self):
        text = self.mainText.toPlainText()
        self.mainText.setPlainText(str(text).replace(self.textThat.text(), self.textThen.text()))

    def replace(self):
        self.search()
        cursor = self.mainText.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.textThen.text())


class NotePad(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_file = "Безымяный"
        self.file_path = None
        self.scale = 100

        self.back = True
        self.saveOrNot = True
        self.settings = QSettings("app1", "qew", self);
        self.textBox = QtWidgets.QPlainTextEdit()
        self.statusBar = QtWidgets.QStatusBar()
        self.label = QtWidgets.QLabel("Стр 1, стлб 1" + " " * 20)
        self.label2 = QtWidgets.QLabel("100%" + " " * 6)
        self.label3 = QtWidgets.QLabel("Windows (CRLF)" + " " * 9)
        self.label4 = QtWidgets.QLabel("UTF-8" + " " * 26)
        self.statusbar_widgets()
        self.loadSettings()
        self.update_name(self.name_file)
        self.resize(750, 500)
        self.menu_bar = QtWidgets.QMenuBar()
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.file_menu = QtWidgets.QMenu("&Файл")
        self.file_menu.addAction("&Создать", self.create_new_tipa_clear_file, shortcut='CTRL+N')
        self.file_menu.addAction("&Новое окно", self.new_window, shortcut='CTRL+SHIFT+N')
        self.file_menu.addAction("&Открыть...", self.open_file, shortcut='CTRL+O')
        self.file_menu.addAction("&Сохранить", self.save, shortcut='CTRL+S')
        self.file_menu.addAction("&Сохранить как", self.save_as, shortcut='CTRL+SHIFT+S')
        self.file_menu.addSeparator()
        self.file_menu.addAction("&Параметры страницы", self.paramtri_stranici)
        self.file_menu.addAction("&Печать...", self.printer_window, shortcut="CTRL+P")
        self.file_menu.addSeparator()
        self.file_menu.addAction("&Выход", self.exit)
        self.pravka_menu = QtWidgets.QMenu("&Правка")
        self.pravka_menu.addAction("Отменить", self.undoRedo, shortcut=Qt.QKeySequence('CTRL+Z'))
        self.pravka_menu.addSeparator()

        self.cutAction = QtWidgets.QAction("&Вырезать", self)
        self.cutAction.setShortcut('Ctrl+X')
        self.cutAction.triggered.connect(self.cut_text)
        self.cutAction.setEnabled(False)

        self.copyTextAction = QtWidgets.QAction("&Скопировать", self)
        self.copyTextAction.triggered.connect(self.copy_text)
        self.copyTextAction.setShortcut('CTRL+C')
        self.copyTextAction.setEnabled(False)

        self.delTextAction = QtWidgets.QAction("&Удалить", self)
        self.delTextAction.triggered.connect(lambda: self.textBox.textCursor().removeSelectedText())
        self.delTextAction.setShortcut('DEL')
        self.delTextAction.setEnabled(False)

        self.searchBingAction = QtWidgets.QAction("&Поиск с помощью Bing...", self)
        self.searchBingAction.triggered.connect(lambda: webbrowser.open(f"https:/www.bing.com/search?q={self.textBox.textCursor().selectedText()}"))
        self.searchBingAction.setShortcut('CTRL+E')
        self.searchBingAction.setEnabled(False)


        self.searchAction = QtWidgets.QAction("&Найти...", self)
        self.searchAction.triggered.connect(self.findWords)
        self.searchAction.setShortcut('CTRL+F')

        self.replaceAction = QtWidgets.QAction("&Заменить...", self)
        self.replaceAction.triggered.connect(self.replaceWords)
        self.replaceAction.setShortcut('CTRL+H')

        self.goAction = QtWidgets.QAction("&Перейти...", self)
        self.goAction.triggered.connect(self.goStroke)
        self.goAction.setShortcut('CTRL+G')
        self.goAction.setEnabled(False)

        self.pravka_menu.addAction(self.cutAction)
        self.pravka_menu.addAction(self.copyTextAction)
        self.pravka_menu.addAction(self.delTextAction)

        self.pravka_menu.addAction("&Вставить", lambda: self.textBox.textCursor().insertText(self.clipboard.text()),
                                   shortcut='CTRL+V')
        self.pravka_menu.addSeparator()
        self.pravka_menu.addAction(self.searchBingAction)
        self.pravka_menu.addAction(self.searchAction)
        self.pravka_menu.addAction(self.replaceAction)
        self.pravka_menu.addAction(self.goAction)
        self.pravka_menu.addSeparator()
        self.pravka_menu.addAction("&Выделить все", self.selectAll, shortcut='CTRL+A')
        self.pravka_menu.addAction("&Время и дата", self.dateAndTime, shortcut='F5')

        self.lineBreaks_checkbox = QtWidgets.QAction("Перенос по словам", self)
        self.lineBreaks_checkbox.setCheckable(True)
        self.lineBreaks_checkbox.setChecked(True)
        self.lineBreaks_checkbox.triggered.connect(self.lineBreaks)
        self.format_menu = QtWidgets.QMenu("Фор&мат")
        self.format_menu.addAction(self.lineBreaks_checkbox)
        self.format_menu.addAction("&Шрифт...", self.font_set)

        self.view_menu = QtWidgets.QMenu("&Вид")
        self.mastab = QtWidgets.QMenu("Масштаб")
        self.mastab.addAction("Увеличить", self.scalePlus, shortcut="CTRL+=")
        self.mastab.addAction("Уменьшить", self.scaleMinus, shortcut="CTRL+-")
        self.mastab.addAction("Установить масштаб по умолчанию", self.defaultScale, shortcut="CTRL+0")
        self.view_menu.addMenu(self.mastab)
        self.statusBar_checkbox = QtWidgets.QAction("Строка состояния", self)
        self.statusBar_checkbox.setCheckable(True)
        self.statusBar_checkbox.setChecked(True)
        self.statusBar_checkbox.triggered.connect(self.hideStatusBarOrNot)
        self.view_menu.addAction(self.statusBar_checkbox)

        self.spravka_menu = QtWidgets.QMenu("&Справка")
        self.spravka_menu.addAction("&Просмотреть справку", lambda: webbrowser.open(
            f"https://www.bing.com/search?q=справка+по+использованию+блокнота+в+windows%c2%a010&filters=guid:%224466414-ru-dia%22%20lang:%22ru%22&form=T00032&ocid=HelpPane-BingIA"))
        self.spravka_menu.addAction("&Отправить отзыв", lambda: QDesktopServices.openUrl(QUrl("feedback-hub:")))
        self.spravka_menu.addSeparator()
        self.spravka_menu.addAction("&О программе", self.about)

        self.textBox.textChanged.connect(self.textChange)

        self.textBox.cursorPositionChanged.connect(self.update_cursor_label)
        self.textBox.selectionChanged.connect(self.unlockAction)
        self.textBox.setStyleSheet(("""
            QPlainTextEdit  {
                selection-background-color: #649aff; 
                selection-color: #FFFFFF;
            }
            QTextEdit:inactive {
                selection-background-color: #649aff; 
                selection-color: #FFFFFF;
            }
        """))

        self.textBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.pravka_menu)
        self.menu_bar.addMenu(self.format_menu)
        self.menu_bar.addMenu(self.view_menu)
        self.menu_bar.addMenu(self.spravka_menu)
        self.setMenuBar(self.menu_bar)

        main_vbox_layout = QtWidgets.QVBoxLayout()
        main_vbox_layout.setContentsMargins(0, 0, 0, 0)
        main_vbox_layout.addWidget(self.textBox)
        main_widget = QtWidgets.QWidget(self)
        main_widget.setLayout(main_vbox_layout)

        self.setCentralWidget(main_widget)

    def statusbar_widgets(self):
        self.statusBar.addPermanentWidget(self.label)
        self.statusBar.addPermanentWidget(self.label2)
        self.statusBar.addPermanentWidget(self.label3)
        self.statusBar.addPermanentWidget(self.label4)
        self.setStatusBar(self.statusBar)

    def unlockAction(self):
        if self.textBox.textCursor().selectedText():
            self.cutAction.setEnabled(True)
            self.copyTextAction.setEnabled(True)
            self.delTextAction.setEnabled(True)
            self.searchBingAction.setEnabled(True)
        else:
            self.cutAction.setEnabled(False)
            self.copyTextAction.setEnabled(False)
            self.delTextAction.setEnabled(False)
            self.searchBingAction.setEnabled(False)

    def update_cursor_label(self):
        self.label.setText(
            f"Стр {self.textBox.textCursor().blockNumber() + 1}, стлб {self.textBox.textCursor().columnNumber() + 1}" + " " * 20)

    def hideStatusBarOrNot(self):

        if self.statusBar_checkbox.isChecked():
            self.statusBar.show()
        else:
            self.statusBar.hide()

    def goStroke(self):
        goWindow = dialogGoWindow(self.textBox)
        goWindow.show()

    def closeEvent(self, a0):
        if self.textBox.toPlainText():
            if self.saveOrNot is False:
                temp = self.displayMessageBox()
                if temp is False:
                    a0.ignore()
                elif temp is None:
                    self.saveSettings()
                    self.close()


    def undoRedo(self):
        if self.back:
            self.back = False
            self.textBox.undo()
        else:
            self.back = True
            self.textBox.redo()

    def defaultScale(self):

        font = self.textBox.font()
        font.setPointSize(font.pointSize() - (self.scale - 100) // 10)
        self.textBox.setFont(font)
        self.scale = 100
        self.label2.setText(str(self.scale) + "%" + " " * 6)

    def replaceWords(self):
        replaceWindow = dialogReplaceWindow(self.textBox.toPlainText(), self.textBox)
        replaceWindow.show()

    def findWords(self):
        findWindow = dialogFindWindow(self.textBox.toPlainText(), self.textBox)
        findWindow.show()

    def loadSettings(self):
        self.font_dialog = QFontDialog()
        self.textBox.setFont(self.settings.value("fontText"))
        self.printer = Qt.QPrinter()
        self.printer1 = Qt.QPrinter()
        self.pageSettings = QPageSetupDialog(self.printer1)
        self.pageSettings.printer().setOrientation(self.settings.value("orient"))

        self.print_dialog = Qt.QPrintDialog(self.printer)
        self.printer.setPrinterName(self.settings.value("printName"))
        self.printer.setCopyCount(self.settings.value("copyCount"))


    def displayMessageBox(self):
        msg = QMessageBox.question(self, "Заголовок", "Вы хотите сохранить изменения в файле " + self.name_file + "?",
                                   QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)
        if msg == QMessageBox.Save:
            if self.save() is False:
                return False

            return True
        if msg == QMessageBox.No:
            # self.close()
            return None
        else:
            return False

    def exit(self):
        self.close()

    def wheelEvent(self, a0):
        key = QtWidgets.QApplication.keyboardModifiers()
        delta = a0.angleDelta().y()
        if delta > 0 and key == QtCore.Qt.ControlModifier and self.scale < 500:
            self.scale += 10;
            self.textBox.zoomIn(1)
        elif delta < 0 and key == QtCore.Qt.ControlModifier and self.scale > 10:
            self.scale -= 10;
            self.textBox.zoomOut(1)
        self.label2.setText(str(self.scale) + "%" + " " * 6)

    def saveSettings(self):
        self.defaultScale()
        self.settings.setValue("fontText", self.textBox.font())
        self.settings.setValue("orient", self.pageSettings.printer().orientation())
        self.settings.setValue("printName", self.printer.printerName())
        self.settings.setValue("copyCount", self.printer.copyCount())

    def cut_text(self):
        self.clipboard.setText(self.textBox.textCursor().selectedText())
        self.textBox.textCursor().removeSelectedText()

    def copy_text(self):
        self.clipboard.setText(self.textBox.textCursor().selectedText())

    def lineBreaks(self):
        if self.lineBreaks_checkbox.isChecked():
            self.goAction.setEnabled(False)
            self.textBox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.textBox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.textBox.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        else:
            self.goAction.setEnabled(True)
            self.textBox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.textBox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.textBox.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)

    def update_name(self, filename):
        self.setWindowTitle(filename + " - Блокнот")

    def textChange(self):
        if self.saveOrNot is True:
            self.setWindowTitle(self.name_file + " - Блокнот")
        else:
            self.setWindowTitle("*"+self.name_file + " - Блокнот")
        self.saveOrNot = False


    def selectAll(self):
        self.textBox.selectAll()

    def dateAndTime(self):
        self.textBox.textCursor().insertText(str(datetime.datetime.now().strftime("%H:%M %Y.%m.%d")))

    def paramtri_stranici(self):
        self.pageSettings.show()

    def scalePlus(self):
        if self.scale<500:
            self.textBox.zoomIn(1)
            self.scale += 10
            self.label2.setText(str(self.scale) + "%" + " " * 6)

    def scaleMinus(self):
        if self.scale>10:
            self.textBox.zoomOut(1)
            self.scale -= 10
            self.label2.setText(str(self.scale) + "%" + " " * 6)

    def save_as(self):
        filename, _ = QFileDialog.getSaveFileName(None, "Сохранение", self.name_file,
                                                  "Text Files (*.txt);;All Files (*)")

        if filename == "":
            return False
        else:
            self.name_file = filename.split("/")[-1]
            self.saveOrNot = True
            self.file_path = filename
            self.setWindowTitle(self.name_file + " - Блокнот")
            with open(filename, "w", encoding="UTF-8") as file:
                file.write(self.textBox.toPlainText())

    def save(self):
        if self.file_path is None:
            filename, _ = QFileDialog.getSaveFileName(None, "Сохранение", self.name_file,
                                                      "Text Files (*.txt);;All Files (*)")
            if filename == "":
                return False
            else:
                self.name_file = filename.split("/")[-1]
                self.file_path = filename
                with open(filename, "w", encoding="UTF-8") as file:
                    file.write(self.textBox.toPlainText())
                self.saveOrNot = True
                self.setWindowTitle(self.name_file + " - Блокнот")
        else:
            with open(self.file_path, "w", encoding="UTF-8") as file:
                file.write(self.textBox.toPlainText())
            self.saveOrNot = True
            self.setWindowTitle(self.name_file + " - Блокнот")

    def new_window(self):
        self.window1 = None
        if self.window1 is None:
            self.window1 = NotePad(self)
        self.window1.show()

    def printer_window(self):

        self.print_dialog = Qt.QPrintDialog(self.printer)
        self.print_dialog.printer().setOrientation(self.pageSettings.printer().orientation())
        self.printer.setPageSize(self.pageSettings.printer().pageSize())
        if self.print_dialog.exec() == Qt.QDialog.Accepted:
            self.textBox.print(self.printer)

    def open_file(self):
        if self.textBox.toPlainText() and self.saveOrNot is False:
            temp = self.displayMessageBox()
            if temp is False:
                return
        filename_path, _ = QFileDialog.getOpenFileName(None, "Open File", ".", "Text Files (*.txt);;All Files (*)")
        if filename_path == "":
            return
        self.file_path = filename_path
        with open(filename_path, "r", encoding="UTF-8") as file:
            lines = file.read()
        self.textBox.setPlainText(lines)
        self.name_file = filename_path.split("/")[-1]
        self.update_name(self.name_file)
        self.saveOrNot = True

    def create_new_tipa_clear_file(self):
        if self.textBox.toPlainText() and self.saveOrNot is False :
            temp = self.displayMessageBox()
            if temp is False:
                return
        self.saveOrNot = True
        self.file_path = None
        self.name_file = "Безымяный"
        self.textBox.setPlainText("")

    def font_set(self):
        tempFontSize =  ((self.scale-100)//10)
        oldFont = self.textBox.font()
        oldSizeFont = oldFont.pointSize()
        newSize = oldSizeFont - tempFontSize
        newFont =oldFont
        newFont.setPointSize(newSize)
        self.font_dialog, ok = QFontDialog().getFont(newFont)
        if ok:
            oldFont = self.font_dialog
            oldSizeFont = oldFont.pointSize()
            newSize = oldSizeFont + tempFontSize
            newFont = oldFont
            newFont.setPointSize(newSize)
            self.textBox.setFont(newFont)

    def about(self):
        str_about = """Приложение создано исключительно в познавательных целях
        И ниразу в жизни не сплагиачено"""
        msgBox_about = Qt.QMessageBox()
        msgBox_about.resize(200, 200)
        msgBox_about.setWindowTitle("Блокнот: сведения")
        msgBox_about.setText(str_about)
        msgBox_about.setWindowIcon(Qt.QIcon(""))
        msgBox_about.setStandardButtons(Qt.QMessageBox.Ok)
        msgBox_about.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = NotePad()
    window.show()
    app.exec()

