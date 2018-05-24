#!/usr/bin/python

import cgitb; cgitb.enable()
import sys;
import os;
import cgi;
import time, getopt, sys

gs_path = '/usr/bin/gs'

class Paper:
    def setFile(self,f_):
        self.f = f_

    def line(self,x1,y1,x2,y2):
        self.f.write("%g %g moveto %g %g lineto stroke \n" % (x1,y1,x2,y2))

    def make_lines(self,x1,y1,x2,y2,skip):
        self.f.write("0.5 setgray\n");
        self.f.write("0.1 setlinewidth ")

        # Horizontal lines
        y = y1
        while(y<y2):
            self.line(x1,y,x2,y)
            y += skip
            self.f.write("stroke\n")

        # Vertical Lines
        self.f.write("0 setgray\n")
        self.f.write("1 setlinewidth ")
        self.line(x1,0,x1,72*11)
        self.line(x1+2,0,x1+2,72*11)
            
    def make_hole(self,x,y):
        self.f.write("%g %g %g 0 360 arc fill\n" % (x,y,.125*72))

    def start(self):
        self.f.write("%!\n")

    def done(self):
        self.f.write("showpage\n")

    def setfont(self,font,size):
        self.f.write("/%s findfont %g scalefont setfont " % (font,size))

    def stroke(self,gray):
        self.f.write("%f setgray stroke\n" % (gray))

    def do_text(self,x,y,text):
        self.f.write("%g %g moveto (%s) show\n" % (x,y,text))

    def do_textRight(self,x,y,text):
        self.f.write("%g " % (x))             # X
        self.f.write("(%s) stringwidth pop " % (text)) # puts width of string on stack
        self.f.write("sub ")            # stack is now x-stringwidth(text)
        self.f.write("%g " % (y))       # puts Y on stack
        self.f.write("moveto (%s) show\n" % (text))

    def fill(self,gray):
        self.f.write("%f setgray fill\n" % (gray))

    def do_textCenter(self,x,y,text):
        self.f.write("%g " % (x))             # X
        self.f.write("(%s) stringwidth pop " % (text)) # puts width of string on stack
        self.f.write(" 2 div ")
        self.f.write("sub ")            # stack is now x-stringwidth(text)/2
        self.f.write("%g " % (y))       # puts Y on stack
        self.f.write("moveto (%s) show\n" % (text))

    def do_name(self,font,name,y):
        self.setfont(font,8)
        self.do_text(1*72+4,y,name)
        self.do_text(1*72+4,y-8,"Please return if found")
        self.setfont(font,16)
        self.do_text(6.5*72,y-16,"Page _____")
        self.do_text(1*72+4,10.4*72,"Subject: ____________________")
        
    #
    # round box needs to be drawn counter-clockwise
    def do_roundbox(self,x,y,width,height):
        r = 24                  # in points
        # Note: degrees: 0 is to the right, and degrees increase counter-clockwise

        self.f.write("2 setlinewidth ")

        # left side
        self.f.write("%g %g moveto %g %g lineto \n" %
                     (x,y+height-r,x,y+r))

        # lower-left corner
        self.f.write("%g %g %g 180 270 arc \n" % (x+r,y+r,r))

        # bottom line
        self.f.write("%g %g lineto \n" %
                     (x+width-r,y))

        # lower-right corner

        self.f.write("%g %g %g 270 360 arc \n" % (x+width-r,y+r,r)) 

        # right side
        self.f.write("%g %g lineto  \n" %
                     (x+width,y+height-r))

        # top right corner
        self.f.write("%g %g %g 0 90 arc  \n" %
                     (x+width-r,y+height-r,r))        

        # top
        self.f.write("%g %g lineto \n" %
                     (x+r,y+height))
        
        # top left corner
        self.f.write("%g %g %g 90 180 arc \n" %
                     (x+r,y+height-r,r))        
        
    def do_calendar(self,font,x,y,size,width,year,month):
        import time;
        months = ("January","February","March","April","May","June","July",
                  "August","September","October","November","December")
        days   = ("S","M","Tu","W","Th","F","S")
        if(month<1 or month>12):
            raise InvalidMonth
        self.setfont(font,size)

        self.f.write("0.8 setgray %g %g %g %g rectfill 0 setgray "
                     % (x,y-(size+1),width*7+4,size-1))


        t   = time.mktime((year,month,1,0,0,0,0,0,0))
        tm  = time.localtime(t)
        today = time.localtime(time.time())
        self.do_textCenter(x+width*4,y,"%s %d" % (months[month-1],year))
        y -= size

        for i in range(0,7):
            self.do_textRight(x+(i+1)*width,y,days[i])
        y -= size                       # down a line

        if(tm < today):
            self.f.write("0.5 setgray ")    # stuff in the past is in gray
        while(tm.tm_mon == month):
            day = (tm.tm_wday+1) % 7    # tm_wday==0 for Monday

            if(tm.tm_mon == today.tm_mon and (tm.tm_mday == today.tm_mday)):
                self.f.write("0 setgray ") # today and on is black

            self.do_textRight(x+(1+day)*width,y,"%d" % tm.tm_mday)
            if(day==6):
                y -= size               # We were Saturday; go to next line
            t += 60*60*24;
            tm = time.localtime(t)      # get the day
        
    def do_notepaper(self,out,do_summary,do_holes):
        self.setFile(out)

        tm = time.localtime(time.time())
        self.start()
        self.make_lines(1*72,1*72,8.5*72,9.76*72,14)

        if(do_summary):
            self.do_roundbox(5*72,6*72,4*72,5*72)
            self.fill(1)
            self.do_roundbox(5*72,6*72,3*72,3.75*72)
            self.stroke(0)

        if(do_holes):
            self.make_hole(0.35 * 72, 1.25*72)
            self.make_hole(0.35 * 72, 5.5*72)
            self.make_hole(0.35 * 72, 9.75*72)

        self.do_name(self.font,self.name,72-8)
        self.do_calendar(self.font,6.8*72,10.7*72,8,12,tm.tm_year,tm.tm_mon)
        self.done()
        out.flush()


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
    

def do_cgi():
    import tempfile
    form = cgi.FieldStorage()
    if not (form.has_key("post")):
        print "Content-Type: text/html\r\n\r\n"     # HTML is following
        print                               # blank line, end of headers
        print cgiform
        return

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

    
