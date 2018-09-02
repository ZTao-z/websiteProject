# -*- coding: utf-8 -*-

#system import
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory, jsonify

#user import
from pylib import photo

#PHOTO PATH
UPLOAD_PHOTO_FOLDER = 'photo'
DOWNLOAD_PHOTO_FOLDER = 'photo'

#BOOK PATH
UPLOAD_BOOK_FOLDER = 'ebook'
DOWNLOAD_BOOK_FOLDER = 'ebook'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# PHOTO PATH CONFIG
app.config['UPLOAD_PHOTO_FOLDER'] = UPLOAD_PHOTO_FOLDER
app.config['DOWNLOAD_PHOTO_FOLDER'] = DOWNLOAD_PHOTO_FOLDER

# BOOK PATH CONFIG
app.config['UPLOAD_BOOK_FOLDER'] = UPLOAD_BOOK_FOLDER
app.config['DOWNLOAD_BOOK_FOLDER'] = DOWNLOAD_BOOK_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 主页
@app.route('/')
def hello_world():
    return '''<a href="/uploadphoto"> 图片上传 </a>
              <a href="/uploadbook"> 文件上传 </a>
              <a href="/updateDoc"> 网站文档 </a>
           '''

# 图片部分
@app.route('/uploadphoto', methods=['GET', 'POST'])
def uploadPhoto():
    if request.method == 'POST':
        file = request.files['photo']
        file_dir = os.path.join(BASEDIR, app.config['UPLOAD_PHOTO_FOLDER'])
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
        else:
            return jsonify({
                    'status' : 404
                })
    return render_template('photoUpload.html')

@app.route('/downloadphoto/<path:filename>', methods=['GET'])
def download(filename):
    dirpath = os.path.join(BASEDIR, app.config['DOWNLOAD_PHOTO_FOLDER'])
    return send_from_directory(dirpath, filename, as_attachment=True)

# 电子书部分
@app.route('/uploadbook', methods=['GET','POST'])
def uploadBook():
    if request.method == 'POST':
        book = request.files['book']
        book_dir = os.path.join(BASEDIR, app.config['UPLOAD_BOOK_FOLDER'])
        if book and allowed_file(book.filename):
            if os.path.exists(book_dir):
                app.logger.debug('%s path exist' % book_dir)
                pass
            else:
                app.logger.debug('%s path not exist' % book_dir)
                os.makedirs(book_dir)
            book.save(os.path.join(book_dir, book.filename))
            return jsonify({
                    'status' : 200
                })
        else:
            return jsonify({
                    'status' : 404
                })
    return render_template('bookUpload.html')

def findAllBooks(book_dir, allBooks):
    for book in os.listdir(book_dir):
        book_path = os.path.join(book_dir, book)
        if os.path.isdir(book_path):
            findAllBooks(unicode(book_path, 'utf-8'), allBooks)
        else:
            allBooks.append(book)

@app.route('/bookshelf', methods=['GET'])
def bookshelf():
    allBooks = []
    book_dir = os.path.join(BASEDIR, app.config['UPLOAD_BOOK_FOLDER'])
    findAllBooks(unicode(book_dir, 'utf-8'), allBooks)
    return jsonify({
            'status' : 200,
            'data' : allBooks
        })

@app.route('/bookshelf/get/<book_name>')
def get_book( book_name ):
    url = url_for( DOWNLOAD_BOOK_FOLDER , filename=book_name+'.txt' )
    if url is None:
        return search_txt( book_name )
    else:
        download( book_name+'.txt' )

#帮助文档
@app.route('/updateDoc', methods=['GET'])
def showDoc():
    return render_template('websiteDocument.html')

if __name__ == '__main__':
    app.run(debug='true')
