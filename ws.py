# Muchammad Nachirul Ichsan/19090023
# Arwinda Laurisma/19090063

import os, random, string
from flask import Flask
from flask import request
from flask import jsonify
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bigpro.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

UPLOAD_FOLDER = 'upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer') 

class Users(db.Model):
    nama = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    email = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    nohp = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, unique=True,primary_key=True)
    tanggal = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    filename = db.Column(db.String(200))
    path = db.Column(db.String(200))

class Yay(db.Model):
    id = db.Column(db.Integer, unique=True,primary_key=True)
    tanggal = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    filename = db.Column(db.String(200))
    path = db.Column(db.String(200))
db.create_all()

@app.route("/api/v1/users/create", methods=["POST"])
def create():
  nama = request.json['nama']
  email = request.json['email']
  nohp = request.json['nohp']
  username = request.json['username']
  password = request.json['password']
  addUsers = Users(nama=nama, email=email, nohp=nohp, username=username, password=password)
  db.session.add(addUsers)
  db.session.commit() 
  return jsonify({
    'msg': 'Registrasi Sukses',
    'username': username,
    'password' : password,
    })

@app.route("/api/v1/users/login", methods=["POST"])
def login():
  username = request.json['username']
  password = request.json['password']
  user = Users.query.filter_by(username=username, password=password).first()

  if user:
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    Users.query.filter_by(username=username, password=password).update({'token': token})
    db.session.commit()
    return jsonify({
      'msg': 'Login Sukses',
      'username': username,
      'token': token,
      })
  else:
    return jsonify({'msg': 'Login Failed'})

@app.route('/api/v2/vehicle/upload', methods=['POST'])
def upload_image():
    token = request.form['token']
    token = Users.query.filter_by(token=token).first()
    if token:
        if 'image' not in request.files:
            resp = jsonify({'msg': "Tidak ada request"})
            resp.status_code = 501
            return resp
        image = request.files['image']
        
        if image.filename == '':
            resp = jsonify({'msg': "Tidak ada file yang terpilih"})
            resp.status_code = 404
            return resp
        error = {}
         
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            error[image.filename] = "File Tipe Tidak Diijinkan"
 
        if success and error:
            error['Message'] = "File Gagal Diupload"
            resp = jsonify(error)
            resp.status_code = 500
            return resp
        if success:
            try:
                filename = secure_filename(image.filename)
                urlpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                data = Vehicle(filename = filename, path = urlpath)
                db.session.add(data)
                db.session.commit()
                
                resp = jsonify({
                    'message' : 'File Berhasil Diunggah',
                    'file' : filename,
                    'url' : urlpath,
                })
                resp.status_code = 201
                return resp
            except Exception as e:
                resp = jsonify('errors')
                resp.status_code = 500
                return resp

if __name__ == '__main__':
   app.run(debug = True, port=7123)