from fileinput import filename
from flask import (Flask, Response, redirect, request, send_file, url_for)
import os
import pyqrcode
from werkzeug.utils import secure_filename
import socket
from flask_cors import CORS, cross_origin


app = Flask(__name__)

@app.route("/")
@cross_origin(supports_credentials=True)
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/home", methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def red_home():
    return redirect(f'/home/1.1')

@app.route("/home/<box>", methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def login(box):
    error = None
    if request.method == 'POST':
        print(request.get_json())
        return request.form['username']
    else:
        print(box)
        return (
            '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PreInvt</title>
</head>
<body style="height: 95vh;width: 95vw;align-items: center;">
    <form style="height: 90vh;width: 90vw;" enctype="multipart/form-data" action='/upimg' method="POST">

        <div style="margin: 2px; padding: 5px;height: 100%;width: 100%;display: flex;flex-direction: column;justify-content: center;">
           <div>

              <button style="margin: 0.5rem; padding: 0.5rem;height: 4rem;width: 4rem;"  type="button" onclick={subst()}>( - )</button>
               
'''
    +
              f' <input style="margin: 0.5rem; padding: 0.5rem;height: 4rem;width: 8rem;"  type="text" name="box" id="box" value={box}>'
    +   

'''
                <button style="margin: 0.5rem; padding: 0.5rem;height: 4rem;width: 4rem;"  type="button" onclick={add()}>( + )</button>
           </div>
            <input style="margin: 1rem; padding: 4rem;background-color: aqua;"  type="file" name="boxs" accept="image/*" capture="camera" />
            <br>
            <input style="margin: 1rem; padding: 4rem;height: 5rem;"  type="submit" value="Submit">
        </div>

        
    </form>
<script>
    const subst = () => {
        const inputValue = document.querySelector("[id='box']")
        const values_spli = (inputValue.value).split('.')
        if(values_spli.length == 2){
            
            if (values_spli[1] > 1){
                
                const nextBox = parseInt(values_spli[1]) - 1
                inputValue.value = `${values_spli[0]}.${nextBox}`
            } 
            else if(values_spli[1] <= 1){

                const nextUep = parseInt(values_spli[0]) - 1
                inputValue.value = `${nextUep}.3`
            }
        }
    }
    const add = () => {
        const inputValue = document.querySelector("[id='box']")

        const values_spli = (inputValue.value).split('.')

        if(values_spli.length == 2){
            
            if(values_spli[1] >= 3){

                const nextUep = parseInt(values_spli[0]) + 1
                inputValue.value = `${nextUep}.1`
            }
            
            else if (values_spli[1] < 3){
                
                const nextBox = parseInt(values_spli[1]) + 1
                inputValue.value = `${values_spli[0]}.${nextBox}`
            }
        }

    }
</script>
</body>
</html>
'''

        )


@app.route("/upimg", methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def procimg():
    if request.method == 'POST':
        
        arq = request.files['boxs']
        box = request.form['box']
        try:
            
            fileName = arq.filename.split('.')

            extesion = fileName[-1]
            
            if(not extesion):
                return '''
                <div>Error</div>
                '''

            
            newFileName = f'{box}.{extesion}'
            
            arq.save(f'./{secure_filename(newFileName)}')
        except:
            return '''
            <div>Error</div>
            '''
        else:
            return redirect(f'/home/{box}')

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    ip = s.getsockname()[0]

    url = pyqrcode.create(f'http://{ip}:5000/home')
    
    print(url.terminal(quiet_zone=2))

    app.run(host='0.0.0.0', port=port)