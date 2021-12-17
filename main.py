from Interface import app, main
import os
import datetime
from threading import Thread
from flask import Flask
from flask_restful import Api

flaskThread = ''




if 'picture.png' in os.listdir():
    os.remove('picture.png')

app.exec_()
