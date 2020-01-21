#
# notepaper class, includes calendar code
#
"""
Copyright (c) 2006,2019 Simson L. Garfinkel

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Changelog:
2019-01-20 Changes from PostScript to FPDF to get UTF8 support.
"""

import time
import datetime
import gettext
import subprocess
import os
import locale
import tempfile
import logging
from pyfpdf.fpdf import FPDF

class Notepaper:
    def __init__(self):
        self.name = ""                  # default name
        self.font = "Helvetica"        # default font
        self.pdf  = FPDF('P', 'pt', 'Letter')
        self.pdf.add_page()
        self.pdf.set_auto_page_break(False, margin=0)
        self.pdf.set_margins(0,0,0)

    def make_lines(self,x1,y1,x2,y2,skip):
        self.pdf.set_draw_color(128)
        self.pdf.set_line_width(0.1)

        # Horizontal lines
        y = y1
        while(y<y2):
            self.pdf.line(x1,y,x2,y)
            y += skip

        # Vertical Lines
        self.pdf.set_draw_color(0)
        self.pdf.set_line_width(1)
        self.pdf.line(x1,0,x1,72*11)
        self.pdf.line(x1+2,0,x1+2,72*11)
            
    def make_hole(self,x,y):
        self.pdf.ellipse(x, y, .125*72, .125*72, 'F')

    def stroke(self,gray):
        self.buf += "%f setgray stroke\n" % (gray)

    def do_text(self,x,y,text):
        self.pdf.set_xy(x, y)
        self.pdf.cell(0, 0, text)

    def do_textRight(self,x,y,text):
        self.pdf.set_xy(x, y)
        self.pdf.cell(0, 0, text, align='R')

    def fill(self,gray):
        self.buf += "%f setgray fill\n" % (gray)

    def do_textCenter(self,x,y,text):
        self.pdf.set_xy(x, y)
        self.pdf.cell(0, 0, text, align='C')

    #
    # round box needs to be drawn counter-clockwise
    def do_roundbox(self,x,y,width,height):
        r = 24                  # in points
        # Note: degrees: 0 is to the right, and degrees increase counter-clockwise

        self.buf += "2 setlinewidth "

        # left side
        self.buf += "%g %g moveto %g %g lineto \n" % (x,y+height-r,x,y+r)

        # lower-left corner
        self.buf += "%g %g %g 180 270 arc \n" % (x+r,y+r,r)

        # bottom line
        self.buf += "%g %g lineto \n" % (x+width-r,y)

        # lower-right corner

        self.buf += "%g %g %g 270 360 arc \n" % (x+width-r,y+r,r) 

        # right side
        self.buf += "%g %g lineto  \n" % (x+width,y+height-r)

        # top right corner
        self.buf += "%g %g %g 0 90 arc  \n" % (x+width-r,y+height-r,r)        

        # top
        self.buf += "%g %g lineto \n" % (x+r,y+height)
        
        # top left corner
        self.buf += "%g %g %g 90 180 arc \n" % (x+r,y+height-r,r)        
        
    def do_calendar(self,x,y,size,width,year,month):
        week_start = 1
        days   = [datetime.date(2000,1,d).strftime("%a") for d in range(2,9)]
        months = [datetime.date(2000,m,1).strftime("%B") for m in range(1,13)]
                
        if(month<1 or month>12):
            raise InvalidMonth
        self.set_font(family=font, size=size)

        self.buf += "0.8 setgray %g %g %g %g rectfill 0 setgray " \
                    % (x,y-(size+1),width*7+4,size-1)


        t   = time.mktime((year,month,1,0,0,0,0,0,0))
        tm  = time.localtime(t)
        today = time.localtime(time.time())
        self.do_textCenter(x+width*4,y,"%s %d" % (months[month-1],year))
        y -= size

        for i in range(0,7):
            self.do_textRight(x+(i+1)*width,y,days[i][0])
        y -= size                       # down a line

        if tm < today:
            self.buf += "0.5 setgray "    # stuff in the past is in gray
        while(tm.tm_mon == month):
            day = (tm.tm_wday+week_start) % 7    # tm_wday==0 for Monday

            if(tm.tm_mon == today.tm_mon and (tm.tm_mday == today.tm_mday)):
                self.buf += "0 setgray " # today and on is black

            self.do_textRight(x+(1+day)*width,y,"%d" % tm.tm_mday)
            if day==6:
                y -= size               # We were Saturday; go to next line
            t += 60*60*24;
            tm = time.localtime(t)      # get the day
        
    def do_notepaper(self, do_summary, do_holes):
        localdir = os.path.join( os.path.dirname(__file__), 'locales')
        _ = gettext.translation('base',localdir,fallback=True).gettext

        tm = time.localtime(time.time())
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

        self.pdf.set_font(family=self.font, style='', size=8)
        self.do_text(1*72+4, 10*72,  self.name)
        self.do_text(1*72+4, 10*72+8, _("Please return if found"))

        self.pdf.set_font(family=self.font, style='', size=16)
        self.do_text(6.5*72, 10*72, _("Page") + ": _____")
        self.do_text(1*72+4, 36, _("Subject") + ":____________________")

        # Do this month calendar
        #self.do_calendar(self.5.4*72,10.7*72,8,12,tm.tm_year,tm.tm_mon)
        next_month = tm.tm_mon+1
        if next_month<13 :
            next_year = tm.tm_year
        else:
            next_month  = 1
            next_year   = tm.tm_year+1
        #self.do_calendar(6.8*72,10.7*72,8,12,next_year,next_month)


def make_pdf(name,font,do_summary,do_holes,lang):
    if lang=='en':
        lcl = "en_US.UTF-8"
    else:
        lcl = f"{lang}_{lang.upper()}.UTF-8"
    os.environ['LANGUAGE']=lcl
    print("lcl:",lcl)
    try:
        locale.setlocale(locale.LC_ALL, lcl)
    except locale.Error:
        logging.error("Invalid locale: %s",lcl)
    paper      = Notepaper()
    paper.name = name
    paper.font = font
    paper.do_notepaper(do_summary,do_holes)
    return paper.pdf.output(dest='S')


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--debug",action="store_true",help="write results to STDOUT")
    parser.add_argument("--lang", help="Specify language (for testing)", default='en')
    parser.add_argument("filename", help="Specify output file")
    parser.add_argument("--summary", action='store_true')
    parser.add_argument("--holes", action='store_true')
    args = parser.parse_args()
    open(args.filename,"wb").write(
        make_pdf("No Name", "Helvetica", args.summary, args.holes, lang=args.lang))
