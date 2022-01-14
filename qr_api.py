import datetime
import flask
from flask import request, Flask
from flask_restful import Api

from utils import create_qr
import os

blueprint = flask.Blueprint(
    'users_api',
    __name__
)



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
                return 'showing QR'
            else:
                if 'TextMessage' in request.json:
                    if request.json['TextMessage'] != '':
                        main.takePayment(request.json['TextMessage'])
                        return 'Showing message'
                    return 'send info'
                return 'send info'
        else:
            main.standbyMode()
        return 'Turning to wait mode'
    return 'try to put some right info into request'


web_app = Flask(__name__)

api = Api(web_app)
web_app.config['SECRET_KEY'] = 'Econica'
web_app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365)
web_app.register_blueprint(blueprint)
kwargs = {'port': 5001, 'host': '127.0.0.1'}
web_app.run(debug=True, port=5001)
