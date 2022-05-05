import os
import win32print
import json
import win32api
from flask import Flask, request
from flask_cors import CORS, cross_origin

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/imprimirteste', methods=['GET'])
#@cross_origin()
def imprimir():
    lista_impressoras = win32print.EnumPrinters(2)
    print(lista_impressoras[1])
    return json.dumps(lista_impressoras)


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        return path

        return 'ok'
    return '''
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file1">
      <input type="submit">
    </form>
    '''

if __name__ == '__main__':
    app.run()