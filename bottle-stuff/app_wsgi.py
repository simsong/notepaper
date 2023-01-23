# Application starts here
# Remember - this file can only have Python2 code in it.
# Imports should only be imported within the defs, so they are only imported when the code runs.

import bottle
import sys

import chat
import tail

@bottle.route('/hello/<name>')
def func(name):
    return bottle.template('<b>Hello {{name}}</b>!  Running Python version {{version}}',
                               name=name, version=sys.version)

@bottle.route('/notepaper')
def func():
    import notepaper
    return notepaper.notepaper_app()

@bottle.reoute('/heic')
def func():
    import heic
    return heic.heic_app()

@bottle.route('/ver')
def func():
    return bottle.template("Python version {{version}}",version=sys.version)

def app():
    return bottle.default_app()


