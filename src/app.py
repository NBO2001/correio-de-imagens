import os
import socket

import pyqrcode
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

from utils import count_folders, create_folder, trim

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/api/upimg', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def upload_imagens():
    if request.method == 'POST':

        try:
            arq = request.files['File']
            path = request.form['Path']

            fileName = arq.filename

            create_folder(trim(path))

            arq.save(f'./{trim(path)}/{secure_filename(fileName)}')
            length_boxs, end_box = count_folders()

            return jsonify(
                {
                    'Error': False,
                    'msg': 'Salvo com sucesso',
                    'boxs': length_boxs,
                    'endboxs': end_box,
                }
            )
        except:
            return jsonify({'Error': True, 'msg': 'Ocorreu um erro'})
    elif request.method == 'GET':
        try:
            length_boxs, end_box = count_folders()
            return jsonify(
                {'Error': False, 'boxs': length_boxs, 'endboxs': end_box}
            )
        except:
            return jsonify({'Error': True, 'msg': 'Ocorreu um erro'})


if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))

    ip = s.getsockname()[0]

    url = pyqrcode.create(f'http://{ip}:5000/home')

    print(url.terminal(quiet_zone=2))

    app.run(host='0.0.0.0', port=port)
