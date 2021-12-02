import flask
from Interface import main
from flask import jsonify, request
from utils import create_qr

blueprint = flask.Blueprint(
    'users_api',
    __name__
)


def QRMode(object, text):
    object.takePayment(text)


def StandbyMode(object):
    object.standbyMode()


@blueprint.route('/', methods=['POST'])
def generate_qr():
    if request.json['ShowMessage']:
        if request.json['QR']:
            create_qr(request.json['QR'])
        main.takePayment(request.json['TextMessage'])
        return jsonify({'success': 'QR created, showing window'})
    else:
        main.standbyMode()
        return jsonify({'success': 'Turning to wait mode'})
