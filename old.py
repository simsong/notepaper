#!/usr/bin/python

import cgitb; cgitb.enable()
import sys;
import os;
import cgi;
import time, getopt, sys

cgiform = """
<html>
<head>
<title>Notepaper Generator</title>
<link rel="stylesheet" href="/blog/styles-site.css" type="text/css">
</head>
<body>
<h1>Notepaper Generator</h1>
<p></p>
<form action="index.cgi" method=post>
<input type=hidden name="post" value="value">
Name: <input type=text size=50 length=50 name="name" value="Simson L. Garfinkel <simsong@acm.org>"> <br>
Font: <input type=text length=30 name="font" value="Helvectica"> <br>
Display Summary Box: <input type=checkbox name="do_summary"><br>
Display Punch Holes: <input type=checkbox name="do_holes"><br>
<input type=submit value="download paper">
</form>
<hr>
<a href="makepaper.py">Download the source</a>
</body>
</html>
"""
    

def do_form():
    print "Content-Type: text/html\r\n\r\n"     # HTML is following
    print                               # blank line, end of headers
    print cgiform
    sys.exit(0)
    

def do_cgi():
    do_form();

    import tempfile
    form = cgi.FieldStorage()
    if not (form.has_key("post")): do_form()

    paper = Paper()

    paper.name = form.getfirst("name")
    paper.font = form.getfirst("font","Helvectica")

    ps  = tempfile.NamedTemporaryFile("w+")
    pdf = tempfile.NamedTemporaryFile("w+")

    ps = open("/tmp/out","w")

    paper.do_notepaper(ps,
                       form.getfirst("do_summary",0),
                       form.getfirst("do_holes",0))


    ps_name = "/tmp/out"

    cmd = gs_path + " -q -dNOPAUSE -SOutputFile=" + pdf.name + " -sDEVICE=pdfwrite -dBATCH " + ps_name
    sys.stderr.write(cmd+"\n")
    os.system(cmd);

    pdf.seek(0);

    print "Content-Type: application/pdf"
    print
    print pdf.read()


if __name__ == "__main__":
    do_cgi();

    # If we are called from the CGI...
    if(os.getenv("REQUEST_METHOD")!=None):
        do_cgi();
        sys.exit(0)
        
    # If we are called from the command-line
    fname = "out.ps"

    try:
	opts, args = getopt.getopt(sys.argv[1:], "hn:f:o:", ["name=","font="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for o,a in opts:
        if o in ("-n", "--name"):
            name = a
        if o in ("-f", "--font"):
            font = a
        if o in ("-o"):
            fname = a
            
    out = open(fname,"w")
    paper = Paper()
    paper.name = "Simson L. Garfinkel <simsong@acm.org>"
    paper.font = "Chalkboard"
    paper.do_notepaper(out, True, True)

    
