from flask import Flask
from os.path import dirname,basename,abspath
import os
import sys

DEBUG=False

app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16*1000*1000
app.debug=DEBUG

# Now bring in the routing...
from app import routes
