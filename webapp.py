import os
import logging
from StringIO import StringIO

from flask import Flask, request, redirect #, url_for
from werkzeug import secure_filename

from reader import MusicXMLReader

UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = set(['xml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 256 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filename)

            buff = StringIO()
            rootLogger = logging.getLogger()
            logHandler = logging.StreamHandler(buff)
            rootLogger.addHandler(logHandler)
            rootLogger.setLevel(logging.INFO)

            MusicXMLReader(filename)

            rootLogger.removeHandler(logHandler)
            logHandler.flush()
            buff.flush()
            # print(buff.read())
            return "<pre>%s</pre>" % buff.getvalue()
        else:
            return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form action="" method=post enctype=multipart/form-data>
              <p><input type=file name=file>
                 <input type=submit value=Upload>
            </form>
            '''