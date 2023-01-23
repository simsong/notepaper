import bottle
import sys
import json
import os

"""
tail protocol:

tail(file,loc):
  file = file being tailed
  loc  = loc of last tail

reply:
  buf  = data at end of tail
  next = end of file
"""

LOGFILE='/home/simsong/logs/simson.net/https/access.log'

import subprocess

INITIAL_READ=4096
MAX_READ=65536

@bottle.route('/tail/')
def chat():
    return bottle.static_file('tail.html', root='static')

@bottle.route('/tail/tail.css')
def chat():
    return bottle.static_file('tail.css', root='static')

@bottle.route('/tail/tail.js')
def chat():
    return bottle.static_file('tail.js', root='static')

@bottle.route('/tail/api', method=['GET','POST'])
def tail():
    if not bottle.request.params.loc:
        end = os.path.getsize(LOGFILE)
        with open(LOGFILE,'rb') as f:
            f.seek(end-INITIAL_READ)
            data = f.read(INITIAL_READ).decode('utf-8',errors='ignore')
        start = data.find('\n')
        buf  = data[start:]
    else:
        with open(LOGFILE,'rb') as f:
            start = int(bottle.request.params.loc) 
            f.seek(start)
            buf = f.read(MAX_READ)
            end = start+len(buf)
            buf = buf.decode('utf-8',errors='ignore')

    return json.dumps({'buf':buf, 'next':end})

    
