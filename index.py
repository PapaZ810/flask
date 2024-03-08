from flask import Flask, request, make_response, jsonify, redirect, url_for, flash, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
cors = CORS(app, resources=r'/api/*')
UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'raw', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <div><input type=file name=file><div/>
      <br>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/garbage")
def me_api():
    #code can go here to process data
    return {
        "username": "user.username",
        "theme": "user.theme",
    }


@app.route("/api/send", methods=["POST", "OPTIONS"])
def send():
    data = request.get_json()
    print(data)
    return make_response(jsonify(data), 201)

