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
import flask.json

sys.path.append( dirname( abspath( __file__ )))
from app import app                       # needed for app routing

# from . import APP_DIR, BIN_DIR, LIB_DIR, ROOT_DIR, STATIC_DIR, HOME

################################################################
## background

@app.route('/favicon.ico')
def icon():
    return redirect("static/favicon.ico.png")

@app.route('/ver')
def ver():
    return f"Python version {sys.version}"

@app.route('/error')
def error():
    raise RuntimeError("Demonstration Error")

@app.route('/heic', methods=['GET','POST'])
def do_heic():
    import heic_app
    return heic_app.heic_app()
