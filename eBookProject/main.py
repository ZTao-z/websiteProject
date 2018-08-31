# -*- coding: utf-8 -*-

#system import
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory

#user import
from pylib import photo


UPLOAD_FOLDER = 'photo'
DOWNLOAD_FOLDER = 'photo'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return '<a href="/uploadphoto"> 文件上传 </a> <a href="/updateDoc"> 网站文档 </a>'

@app.route('/uploadphoto', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['photo']
        file_dir= os.path.join(basedir,app.config['UPLOAD_FOLDER'])
        if file and allowed_file(file.filename):
            if os.path.exists(file_dir):
                app.logger.debug('%s path exist' % file_dir)
                pass
            else:
                app.logger.debug('%s path not exist' % file_dir)
                os.makedirs(file_dir)
            file.save(os.path.join(file_dir, file.filename))
            photo.getNonWaterImage(os.path.join(file_dir, file.filename), os.path.join(file_dir, 'temp.png'))
            return redirect('/downloadphoto/temp.png')
    return render_template('photoUpload.html')

@app.route('/downloadphoto/<path:filename>', methods=['GET'])
def download(filename):
    dirpath = os.path.join(basedir, app.config['DOWNLOAD_FOLDER'])
    return send_from_directory(dirpath, filename, as_attachment=True)

@app.route('/updateDoc', methods=['GET'])
def showDoc():
    return render_template('websiteDocument.html')

if __name__ == '__main__':
    app.run(debug='true')