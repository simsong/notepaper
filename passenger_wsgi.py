"""
passenger_wsgi.py script to switch to python3 and use Bottle

To reload:

$ touch tmp/restart.txt
(or)
$ make touch
"""

import sys
import os
import os.path

DESIRED_PYTHON_VERSION  = '3.9'
DESIRED_PYTHON          = 'python3.9'
DREAMHOST_PYTHON_BINDIR = os.path.join( os.getenv('HOME'), 'opt/python-3.9.2/bin')

debug=True

errfile = open( os.path.join( os.getenv('HOME'), 'apps.error.log'),'a')
os.close(sys.stderr.fileno())
os.dup2(errfile.fileno(), sys.stderr.fileno())

if DREAMHOST_PYTHON_BINDIR not in os.environ['PATH']:
    if debug:
        sys.stderr.write("Adding "+DREAMHOST_PYTHON_BINDIR+" to PATH\n")
    os.environ['PATH'] = DREAMHOST_PYTHON_BINDIR + ":" + os.environ['PATH']

if (DESIRED_PYTHON not in sys.executable) and ('RUNNING_PYTEST' not in os.environ):
    os.execlp(DESIRED_PYTHON, DESIRED_PYTHON, *sys.argv)
    
from app import app as application
