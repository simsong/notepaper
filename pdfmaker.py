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
    LINE_HEIGHT = 10
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

    def fill(self,gray):
        self.buf += "%f setgray fill\n" % (gray)

    def text(self, x, y, width, txt, *, border=0, align='L'):
        """@param (x,y) - upper-left corner of the box.
        width - width of the box; if 0, goes to the right margin.
        txt   - the text.
        align - L,R,C within the box.
        """
        self.pdf.set_xy(x, y)
        self.pdf.cell( width, self.LINE_HEIGHT, txt, border=border, align=align)

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
        
    def do_calendar(self, x, y, when):
        """
        @param x,y - upper-left corner of the calendear in points
        @param when - calender for which we are making
        """
        WIDTH  = 1.3 * 72
        LINES  = 7              # 0 - month year | 1 - SMTWTFS | 2, 3, 4 5, 6 = weeks
        HEIGHT = self.LINE_HEIGHT * 6
        COLS   = 7
        COL_MARGIN = 6          # between columns, and between columns and edge
        COL_WIDTH  = (WIDTH-(COL_MARGIN*(COLS+1)))/COLS
        import holidays.holidays
        us_holidays = holidays.holidays.US()

        def liney(n):
            return y+self.LINE_HEIGHT*n
        def col_start(n):
            assert 0 <= n <= 6
            return x + COL_MARGIN + n*(COL_WIDTH+COL_MARGIN)
        def day_name(d):
            return datetime.date(2000,1,d).strftime("%a")
        
        self.pdf.set_font(family=self.font, style='', size=8 )

        # First draw the month name
        line = 0
        self.text( x, liney(line), WIDTH, when.strftime("%B %Y"), align='C' )
        line += 1

        # Now the grey bar with the day names
        self.pdf.set_fill_color(100,255,255)
        self.pdf.set_draw_color(100,255,255)
        self.pdf.rect(x, liney(line), WIDTH, self.LINE_HEIGHT, style='F')
        for i in range(0,7):
            self.text( col_start(i), liney(line), COL_WIDTH, day_name(i+2)[0], align='R' )
        
        line  += 1               # start on the second line
        day   = datetime.date(year=when.year, month=when.month, day=1) # iterator
        today = datetime.date.today() # today
        while day.month == when.month:
            weekday = day.weekday()
            col = ( weekday + 1 ) % 7
            if (day in us_holidays):
                self.pdf.set_fill_color(200,200,255)
                self.pdf.rect( col_start( col ) - COL_WIDTH, liney(line), COL_WIDTH*1.5, self.LINE_HEIGHT, style='F')
            if day < today:
                self.pdf.set_text_color(128,128,128)
            elif day == today:
                self.pdf.set_text_color(255,0,0)
            else:
                self.pdf.set_text_color(0,0,0)
            self.text( col_start( col ), liney(line), COL_WIDTH, str(day.day), align='R')
            if day.weekday()==5: # if sat, go to next line
                line += 1
            day += datetime.timedelta(days=1)

    def do_notepaper(self, do_summary, do_holes):
        localdir = os.path.join( os.path.dirname(__file__), 'locales')
        _ = gettext.translation('base',localdir,fallback=True).gettext

        self.make_lines(1*72,1*72,8.5*72,9.76*72,16)

        if do_summary:
            self.do_roundbox(5*72,6*72,4*72,5*72)
            self.fill(1)
            self.do_roundbox(5*72,6*72,3*72,3.75*72)
            self.stroke(0)

        if do_holes:
            self.make_hole(0.35 * 72, 1.25*72)
            self.make_hole(0.35 * 72, 5.5*72)
            self.make_hole(0.35 * 72, 9.75*72)

        self.pdf.set_font(family=self.font, style='', size=8)
        self.text(1*72+4, 10*72,  0, self.name)
        self.text(1*72+4, 10*72+8, 0, _("Please return if found"))

        self.pdf.set_font(family=self.font, style='', size=16)
        self.text(6.5*72, 10*72, 0, _("Page") + ": _____")
        self.text(1*72+4, 36, 0, _("Subject") + ":____________________")

        # Do this month calendar
        today = datetime.date.today()
        self.do_calendar( 5*72, 0, today)
        this_month = today.month
        while today.month==this_month:
            today = today + datetime.timedelta(days=1)
        self.do_calendar( 6.5*72, 0, today)


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
