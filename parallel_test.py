from PyQt5.QtWidgets import QLabel, QVBoxLayout, QMainWindow, QApplication, QWidget
from flask import Flask, render_template

from threading import Thread
import sys

# You can copy and paste this code for test and run it

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Sorted Ware House")
        widget = QWidget()
        label = QLabel("Flask is running...")
        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

#   Creating instance of QApplication
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app_ = Flask(__name__)

#   setting our root
    @app_.route('/')
    def index():
        return 'LOL'

#   Preparing parameters for flask to be given in the thread
#   so that it doesn't collide with main thread
    kwargs = {'host': '127.0.0.1', 'port': 5000, 'threaded': True, 'use_reloader': False, 'debug': False}

#   running flask thread
    flaskThread = Thread(target=app_.run, daemon=True, kwargs=kwargs).start()

    app.exec_()
