#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys;
import os;
import time, getopt, sys
import notepaper

sys.path.append( os.path.join(os.path.dirname(__file__), ".."))   # get bottle in path

import bottle

"""This is the WSGI driver for notepaper.
"""

def do_cgi():
    form = cgi.FieldStorage()
    if "post" in form and False:
        pdf = make_pdf(form.getfirst("name",""),
                     form.getfirst("font","Helvectica"),
                     form.getfirst("do_summary",0),
                     form.getfirst("do_holes",0),
		     form.getfirst("lang",0))

        print("Content-Type: application/pdf")
        print()
        print(pdf)
    do_form()


def notepaper_app():
    return bottle.static_file( "notepaper_form.html", root=os.path.dirname(__file__), )

