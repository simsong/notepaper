#!/usr/bin/python

import cgitb; cgitb.enable()
import sys;
import os;
import cgi;
import time, getopt, sys
import notepaper

# Copyright (c) 2006, Simson L. Garfinkel
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

gs_path = '/usr/bin/gs'

cgiform = """
<html>
<head>
<title>Simson Garfinkel's Notepaper Generator</title>
<link rel="stylesheet" href="/blog/styles-site.css" type="text/css">
</head>
<body>
<h1>Simson Garfinkel's Notepaper Generator</h1>
<p></p>
<form action="index.cgi" method=post>
<input type=hidden name="post" value="value">
Name: <input type=text size=50 length=50 name="name" value="Simson L. Garfinkel <simsong@acm.org>"> <br>
Font: <input type=text length=30 name="font" value="Helvectica"> <br>
Display Summary Box: <input type=checkbox name="do_summary"><br>
Display Punch Holes: <input type=checkbox name="do_holes"><br>
Spanish: <input type=checkbox name="lang"><br>
<input type=submit value="download paper">
</form>
<hr>
Download the source:
<ul>
<li><a href="index.cgi?source=index.cgi">index.cgi</a>
<li><a href="index.cgi?source=notepaper.py">notepaper.py</a>
</ul>
<hr>
Copyright 2006, Simson L. Garfinkel<br>
</body>
</html>
"""

def print_source(fn):
    print "Content-type: text/text\r\n\r\n"
    for line in open(fn,"r"):
        sys.stdout.write(line)

def do_form():
    print "Content-Type: text/html\r\n\r\n"     # HTML is following
    print                               # blank line, end of headers
    print cgiform
    sys.exit(0)


def debug(info="looks ok"):
    print "Content-type: text/text\r\n\r\n"
    print info
    sys.exit(0)


def make_ps(name,font,do_summary,do_holes,lang):
    paper      = notepaper.notepaper()
    paper.name = name
    paper.font = font
    paper.lang = lang
    paper_ps   = paper.do_notepaper(do_summary,do_holes)
    return paper_ps

def make_pdf(name,font,do_summary,do_holes,lang):
    import tempfile
    ps_file  = tempfile.NamedTemporaryFile("w+")
    pdf_file = tempfile.NamedTemporaryFile("w+")
    ps_file.write(make_ps(name,font,do_summary,do_holes,lang))
    ps_file.flush()
    ps_file.seek(0)
    cmd = gs_path + " -q -dNOPAUSE -SOutputFile=" + pdf_file.name + \
          " -sDEVICE=pdfwrite -dBATCH " + ps_file.name
    os.system(cmd);
    pdf_file.seek(0);
    return pdf_file.read()


def do_cgi():
    import tempfile
    form = cgi.FieldStorage()
    if form.has_key("source"):
        print_source(form.getfirst("source"))
        sys.exit(0)

    if form.has_key("post"):
        pdf = make_pdf(form.getfirst("name",""),
                     form.getfirst("font","Helvectica"),
                     form.getfirst("do_summary",0),
                     form.getfirst("do_holes",0),
		     form.getfirst("lang",0))

        print "Content-Type: application/pdf"
        print
        print pdf


    do_form()


if __name__ == "__main__":
    # If we are called from the CGI...

    if(os.getenv("REQUEST_METHOD")!=None):
        do_cgi();
        sys.exit(0)