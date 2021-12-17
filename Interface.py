import sys
import os
from PIL import Image
from PyQt5 import uic, QtWidgets
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel, QFileDialog
from PyQt5.QtGui import QScreen, QPixmap, QFont, QIcon
from PyQt5.QtCore import QTimer, Qt

main = ''
admin_panel = ''


class ShowWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('monitor.ico'))
        f = open('config.cfg', encoding='utf-8').readlines()
        picpath = f[0].replace('\n', '')
        os.chdir(picpath)
        self.port = int(f[1])
        self.font = QFont()
        self.mode = 's'
        self.interval = int(f[2]) * 1000
        self.font.setPointSize(int(f[4]))
        self.pictures = os.listdir()
        self.setGeometry(QDesktopWidget().screenGeometry(int(f[3]) - 1))
        self.setWindowTitle('Показатор')
        self.label = QLabel(self)
        self.label.setFont(self.font)
        self.count = 0
        self.label.move(200, 100)
        self.current = self.pictures[0]
        self.a = ImageQt(self.current)
        self.image = QLabel(self)
        self.pixmap = QPixmap.fromImage(self.a)
        self.pixmap = self.pixmap.scaled(self.screen().size().height(), self.screen().size().height(),
                                         Qt.KeepAspectRatio)
        self.image.resize(self.pixmap.size())
        self.image.move(self.screen().size().width() // 2 - self.pixmap.size().width() // 2,
                        self.screen().size().height() // 2 - self.pixmap.size().height() // 2)
        self.image.setPixmap(self.pixmap)

    def takePayment(self, text):
        self.mode = 'p'
        self.label.setText(text)
        self.label.adjustSize()
        if self.showQR():
            self.label.move(self.screen().size().width() // 2 - self.label.width() // 2, 5)
        else:
            self.label.move(self.screen().size().width() // 2 - self.label.width() // 2,
                            self.screen().size().height() // 2)
            self.image.setVisible(False)

    def changePicture(self):
        self.count = (self.count + 1) % len(self.pictures)
        self.current = self.pictures[self.count]
        self.a = ImageQt(self.current)
        self.pixmap = QPixmap.fromImage(self.a)
        self.pixmap = self.pixmap.scaled(self.screen().size().height(), self.screen().size().height(),
                                         Qt.KeepAspectRatio)
        self.image.resize(self.pixmap.size())
        self.image.move(self.screen().size().width() // 2 - self.pixmap.size().width() // 2,
                        self.screen().size().height() // 2 - self.pixmap.size().height() // 2)
        self.image.setPixmap(self.pixmap)

    def showQR(self):
        if 'picture.png' in os.listdir():
            self.current = 'picture.png'
            self.a = ImageQt(self.current)
            self.pixmap = QPixmap.fromImage(self.a)
            self.pixmap = self.pixmap.scaled(self.screen().size().height() - self.label.rect().height() - 10,
                                             self.screen().size().height() - self.label.rect().height() - 10,
                                             Qt.KeepAspectRatio)
            self.image.resize(self.pixmap.size())
            self.image.move(self.screen().size().width() // 2 - self.pixmap.size().width() // 2,
                            self.label.height() + 10)
            self.image.setPixmap(self.pixmap)
            return True
        return False

    def standbyMode(self):
        self.image.setVisible(True)
        self.mode = 's'
        if 'picture.png' in os.listdir():
            os.remove('picture.png')
        self.label.setText('')
        self.changePicture()


class SettingsWindow(QMainWindow):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        uic.loadUi('SettingsWindow.ui', self)
        self.fileButton.clicked.connect(self.choseFile)
        self.Monitor_spinBox.setMaximum(QDesktopWidget().screenCount())
        self.pushButton.clicked.connect(self.start)
        try:
            file = open('config.cfg', encoding='utf-8')
            f = file.readlines()
            if f != []:
                try:
                    self.lineEdit.setText(f[0].replace('\n', ''))
                    self.Timing_spinBox.setValue(int(f[2]))
                    self.Monitor_spinBox.setValue(int(f[3]))
                    self.Port_spinBox.setValue(int(f[1]))
                    self.Font_spinBox.setValue(int(f[4]))
                except IndexError:
                    pass
            file.close()
        except FileNotFoundError:
            f = open('config.cfg', encoding='utf-8', mode='w')
            f.close()

    def start(self):
        data = [self.lineEdit.text(), self.Port_spinBox.value(), self.Timing_spinBox.value(),
                self.Monitor_spinBox.value(), self.Font_spinBox.value()]
        if all(data):
            f = open('config.cfg', encoding='utf-8', mode='w')
            f.writelines(map(lambda x: str(x) + '\n', data))
            f.close()
            start_main()
            self.close()
        else:
            self.label_6.setText('Заполните все поля.')

    def choseFile(self):
        fname = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.lineEdit.setText(fname)


def start_main():
    global main, admin_panel
    main = ShowWindow()


class AdminPanelWindow(QMainWindow):
    def __init__(self):
        super(AdminPanelWindow, self).__init__()
        uic.loadUi('AdminPanel.ui', self)


app = QApplication(sys.argv)

admin_panel = AdminPanelWindow()
admin_panel.show()
app.exec_()
