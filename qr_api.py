import flask
from flask import jsonify, request
from utils import create_qr
import os

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
    from Interface import main
    if 'ShowMessage' in request.json:
        if request.json['ShowMessage']:
            if 'picture.png' in os.listdir():
                os.remove('picture.png')
            if 'QR' in request.json:
                create_qr(request.json['QR'])
                if 'TextMessage' in request.json:
                    if request.json['TextMessage'] != '':
                        main.takePayment(request.json['TextMessage'])
                    else:
                        main.takePayment()
                else:
                    main.takePayment()
                return jsonify({'success': 'QR created, showing window'})
            else:
                if 'TextMessage' in request.json:
                    if request.json['TextMessage'] != '':
                        main.takePayment(request.json['TextMessage'])
                        return jsonify({'success': 'Showing message'})
                    return jsonify({'no info to show': 'send info'})
                return jsonify({'no info to show': 'send info'})
        else:
            main.standbyMode()
        return jsonify({'success': 'Turning to wait mode'})
    return jsonify({'empty request': 'try to put some right info into request'})


