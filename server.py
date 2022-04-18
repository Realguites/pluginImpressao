from flask import Flask
from flask import send_file
from flask import jsonify 
from flask import request
import os

import _json
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

empDB=[
 {
 'id':'101',
 'name':'Saravanan S',
 'title':'Technical Leader'
 },
 {
 'id':'201',
 'name':'Rajkumar P',
 'title':'Sr Software Engineer'
 }
 ]

@app.route("/teste")
def getMessage():
    return "ola"

@app.route('/imprimir',methods=['GET'])
def createEmp(): 
    #dat = {
    #'id':request.json['id'],
    #'name':request.json['name'],
    #'title':request.json['title']
    #}
    #empDB.append(dat)
    #return jsonify(dat)
    imagefile = request.files.get('imagefile', '')
    return imagefile
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'



@app.route('/empdb/employee/<testeId>',methods=['GET'])
def getAllEmp(testeId):
    usr = [ emp for emp in empDB if (emp['id'] == testeId) ] 
    return testeId

if __name__ == "__main__":
    app.run()

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST'])
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
