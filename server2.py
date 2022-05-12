from http.client import INSUFFICIENT_STORAGE, HTTPException
import io
import flask
import win32print
import json
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from base64 import b64decode
from glob import glob
import win32ui
from PIL import Image, ImageWin
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/getAllPrinters', methods=['GET'])
@cross_origin()
def getAllPrinters():
    lista_impressoras = [printer[2] for printer in win32print.EnumPrinters(2)]
    return json.dumps(lista_impressoras)

@app.route('/imprimirteste', methods=['GET','POST'])
@cross_origin()
def receiveFile():
    if request.method == 'POST':
        if not request.form.get('printer'):
            return Response("Impressora não informada!", status="400", mimetype='application/json')
        else:
            if request.form.get('printer') not in getPrinters():
                return Response("Impressora não encontrada!", status="400", mimetype='application/json')
            else:
                pdf_64 = request.form.get("pdf_64")
                bytes = b64decode(pdf_64, validate=True)
                callPrinterService('Microsoft Print to PDF', bytes)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

def getPrinters():
    return [printer[2] for printer in win32print.EnumPrinters(2)]

def callPrinterService(printer, bytes):
    file_name = "teste.png"
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer)
    buf = io.BytesIO(bytes)
    bmp = Image.open (buf)
    hDC.StartDoc (file_name)
    hDC.StartPage ()
    dib = ImageWin.Dib (bmp)
   
    x1 = 50
    y1 = 50
    x2 = 2000 + bmp.size[0]
    y2 = 3000 + bmp.size[1]
    dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

    hDC.EndPage ()
    hDC.EndDoc ()
    hDC.DeleteDC ()

if __name__ == '__main__':
    app.run()