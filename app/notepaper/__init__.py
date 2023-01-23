#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys;
import os;
import time, getopt, sys

sys.path.append( os.path.join(os.path.dirname(__file__), "."))   # get bottle in path
sys.path.append( os.path.join(os.path.dirname(__file__), ".."))   # get bottle in path

import notepaper.pdfmaker as pdfmaker
import bottle

"""This is the WSGI driver for notepaper.
"""

def notepaper_app():
    if bottle.request.params.get('lang',None) is None:
        return bottle.static_file( "notepaper_form.html", root=os.path.dirname(__file__), )
    bottle.response.content_type = 'application/pdf'
    return pdfmaker.make_pdf(
        bottle.request.params.get("name",''),
        bottle.request.params.get('font',"Helvectica"),
        bottle.request.params.get("do_summary",False),
        bottle.request.params.get("do_holes",False),
        int(bottle.request.params.get("lpi",6)),
        bottle.request.params.get("lang","en"))

