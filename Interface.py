import sys
import os
import datetime
from threading import Thread

from PyQt5 import uic, QtWidgets
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel, QFileDialog
from PyQt5.QtGui import QScreen, QPixmap, QFont, QIcon
from PyQt5.QtCore import QTimer, Qt
from flask import Flask
from flask_restful import Api

settingsUI = os.path.abspath('SettingsWindow.ui')
admin_panelUI = os.path.abspath('AdminPanel.ui')
config = os.path.abspath('config.cfg')
icon = os.path.abspath('monitor.ico')

main = ''
admin_panel = ''
settings = ''
flaskThread = ''


def startFlaskThread():
    import qr_api
    global flaskThread, main
    web_app = Flask(__name__)

    api = Api(web_app)
    web_app.config['SECRET_KEY'] = 'Econica'
    web_app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
        days=365)
    web_app.register_blueprint(qr_api.blueprint)

    kwargs = {'port': main.port, 'host': '127.0.0.1'}

    flaskThread = Thread(target=web_app.run, daemon=True, kwargs=kwargs).start()


class ShowWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(icon))
        f = open(config, encoding='utf-8').readlines()
        picpath = f[0].replace('\n', '')
        os.chdir(picpath)
        if 'picture.png' in os.listdir():
            os.remove('picture.png')
        self.port = int(f[1])
        self.font = QFont()
        self.mode = 'standBy'
        self.interval = int(f[2]) * 1000
        self.font.setPointSize(int(f[4]))
        self.pictures = os.listdir()
        self.setMaximumSize(QDesktopWidget().availableGeometry(int(f[3]) - 1).width(), QDesktopWidget().availableGeometry(int(f[3]) - 1).height())
        self.setMinimumSize(QDesktopWidget().availableGeometry(int(f[3]) - 1).width(), QDesktopWidget().availableGeometry(int(f[3]) - 1).height())
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
        self.timer = QTimer()
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.changePicture)
        self.timer.start()

    def takePayment(self, text):
        global admin_panel
        self.mode = 'takePayment'
        self.label.setText(text)
        self.label.adjustSize()
        if self.showQR():
            self.label.move(self.screen().size().width() // 2 - self.label.width() // 2, 5)
            admin_panel.changeText('Демонстарция QR кода')
        else:
            self.label.move(self.screen().size().width() // 2 - self.label.width() // 2,
                            self.screen().size().height() // 2)
            admin_panel.changeText('Демонстарция сообщения')
            self.image.setVisible(False)

    def changePicture(self):
        if self.mode == 'standBy':
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
        self.mode = 'standBy'
        admin_panel.changeText('Ожидание запроса')
        if 'picture.png' in os.listdir():
            os.remove('picture.png')
        self.label.setText('')
        self.changePicture()


class SettingsWindow(QMainWindow):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        uic.loadUi(settingsUI, self)
        self.fileButton.clicked.connect(self.choseFile)
        self.Monitor_spinBox.setMaximum(QDesktopWidget().screenCount())
        self.pushButton.clicked.connect(self.start)
        try:
            file = open(config, encoding='utf-8')
            f = file.readlines()
            if f:
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
            f = open(config, encoding='utf-8', mode='w')
            f.close()

    def start(self):
        data = [self.lineEdit.text(), self.Port_spinBox.value(), self.Timing_spinBox.value(),
                self.Monitor_spinBox.value(), self.Font_spinBox.value()]
        if all(data):
            f = open(config, encoding='utf-8', mode='w')
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
    admin_panel = AdminPanelWindow()
    main = ShowWindow()
    startFlaskThread()
    main.show()
    admin_panel.show()


class AdminPanelWindow(QMainWindow):
    def __init__(self):
        super(AdminPanelWindow, self).__init__()
        uic.loadUi(admin_panelUI, self)
        self.setWindowTitle('Окно администратора')
        self.pushButton.clicked.connect(self.returnToSettings)
        self.closeButton.clicked.connect(self.closeAll)
        self.changeText('Ожидание запроса')

    def returnToSettings(self):
        global main, settings
        main.close()
        settings = SettingsWindow()
        settings.show()
        self.close()

    def closeAll(self):
        sys.exit(0)

    def changeText(self, text):
        self.label_2.setText(text)


app = QApplication(sys.argv)
settings = SettingsWindow()
settings.show()
