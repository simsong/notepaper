FORM="""
<html>
<head>
<title>HEIC Converter</title>
</head>
<body>
<h1>HEIC Converter</h1>
    <h1>Upload HEIC file to convert</h1>
<p>Max image size: 16MB.</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file/><br/>
      <input type=submit value=Upload>
    </form>

<p>Privacy policy: images are processed on server with a Python program but are never written to disk. </p>

</body>
</html>
"""

import sys
import os
import json
import tempfile
import urllib.parse
import io
import re
from os.path import basename,dirname,abspath

from flask import Flask, redirect, request, render_template
from flask import Flask, send_from_directory
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import flask.json

from PIL import Image
import pillow_heif

UPLOAD_FOLDER = '/home/simsong/upload'

def heic_app():
    if request.method=='POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            f = io.BytesIO()
            file.save(f)
            f.seek(0)
            h = pillow_heif.read_heif(f)
            image = Image.frombytes(h.mode, h.size, h.data, 'raw')
            out = io.BytesIO()
            image.save(out, format='jpeg')
            out.seek(0)
            return out, 200, {'Content-Type':'image/jpeg'}
            return open("/home/simsong/IMG_2305.JPG","rb").read(), 200, {'Content-Type':'image/jpeg'}
            

    return FORM
