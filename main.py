from PyQt5.QtWidgets import QApplication
from utils import create_qr
import datetime
from Interface import main, app, admin_panel,settings
from threading import Thread
import requests
import os
import sys
from flask import Flask, request, render_template, make_response, session
from flask_restful import Api
import qr_api
from PyQt5.QtGui import QScreen, QPixmap, QFont, QIcon
from PyQt5.QtCore import QTimer





if 'picture.png' in os.listdir():
    os.remove('picture.png')




admin_panel.show()
web_app = Flask(__name__)

api = Api(web_app)
web_app.config['SECRET_KEY'] = 'Econica'
web_app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365)
web_app.register_blueprint(qr_api.blueprint)

kwargs = {'port': main.port, 'host': '127.0.0.1'}

flaskThread = Thread(target=web_app.run, daemon=True, kwargs=kwargs).start()

app.exec_()
