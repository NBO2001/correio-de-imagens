import os
import socket
from os.path import abspath

import pyqrcode
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

from model import insert, insert_plan, mapping, querry, create_table
from utils import count_folders, create_folder, padronizador, trate_date, trim

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/api/addinfobox', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def addboxifo():
    if request.method == 'POST':
        try:

            index = padronizador(
                request.form['index'], request.form['cliente']
            )
            setor = request.form['setor']
            descricao = request.form['descricao']
            key_one = request.form['key_one']
            key_two = request.form['key_two']
            data = trate_date(request.form['data'])

            if insert_plan(
                index, setor, descricao, key_one, key_two, data[0], data[1]
            ):
                return jsonify(
                    {'Error': False, 'msg': 'Adicionado com sucesso'}
                )

            else:
                return jsonify({'Error': True, 'msg': 'Ocorreu um erro'})
        except Exception as e:
            print(e)

            return jsonify({'Error': True, 'msg': 'Ocorreu um erro'})


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
            mapping()
            return jsonify(
                {
                    'Error': False,
                    'msg': 'Foi salvo com sucesso',
                    'boxs': length_boxs,
                    'endboxs': end_box,
                }
            )
        except Exception as e:
            print(e)

            return jsonify({'Error': True, 'msg': 'Ocorreu um erro'})

    elif request.method == 'GET':
        try:
            length_boxs, end_box = count_folders()
            return jsonify(
                {'Error': False, 'boxs': length_boxs, 'endboxs': end_box}
            )
        except:
            return jsonify({'Error': True, 'msg': 'Ocorreu um erro'})


@app.route('/api/table', methods=['GET'])
@cross_origin(supports_credentials=True)
def table_genaration():

    if request.method == 'GET':
        if create_table():
            return jsonify({'Error': False, 'msg': 'Planilha gerada com sucesso'})
        else:
            return jsonify({'Error': True, 'msg': 'Ocorreu um erro'})

@app.route('/api/imginfo/<int:imge>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_sum_imgs(imge):

    data = querry(imge)
    return jsonify(
        {
            'Error': False,
            'box': data['box'],
        }
    )


@app.route('/api/imgs/<int:imge>', methods=['GET'])
@cross_origin(supports_credentials=True)
def getImage(imge: int):

    data = querry(imge)

    if request.method == 'GET':
        return send_file(
            f'{abspath("./")}/{data["box"]}/{data["imgs"]}',
            mimetype='image/jpg',
        )


if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))

    ip = s.getsockname()[0]

    url = pyqrcode.create(f'http://{ip}:3000')

    print(url.terminal(quiet_zone=2))
    print(f'IP: http://{ip}:3000')

    app.run(host='0.0.0.0', port=port)
