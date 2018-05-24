#
# notepaper class, includes calendar code
#
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

import time

class notepaper:
    def __init__(self):
        self.name = ""                  # default name
        self.font = "Helvetica"        # default font
        self.buf = "%!\nletter\n"
	self.lang = ""
    def line(self,x1,y1,x2,y2):
        self.buf += "%g %g moveto %g %g lineto stroke \n" % (x1,y1,x2,y2)

    def make_lines(self,x1,y1,x2,y2,skip):
        self.buf += "0.5 setgray "
        self.buf += "0.1 setlinewidth "

        # Horizontal lines
        y = y1
        while(y<y2):
            self.line(x1,y,x2,y)
            y += skip
            self.buf += "stroke\n"

        # Vertical Lines
        self.buf += "0 setgray\n"
        self.buf += "1 setlinewidth "
        self.line(x1,0,x1,72*11)
        self.line(x1+2,0,x1+2,72*11)
            
    def make_hole(self,x,y):
        self.buf += "%g %g %g 0 360 arc fill\n" % (x,y,.125*72)

    def done(self):
        self.buf += "showpage\n"

    def setfont(self,font,size):
        self.buf += "/%s findfont %g scalefont setfont " % (font,size)

    def stroke(self,gray):
        self.buf += "%f setgray stroke\n" % (gray)

    def do_text(self,x,y,text):
        self.buf += "%g %g moveto (%s) show\n" % (x,y,text)

    def do_textRight(self,x,y,text):
        self.buf += "%g " % (x)             # X
        self.buf += "(%s) stringwidth pop " % (text) # puts width of string on stack
        self.buf += "sub "            # stack is now x-stringwidth(text)
        self.buf += "%g " % (y)       # puts Y on stack
        self.buf += "moveto (%s) show\n" % (text)

    def fill(self,gray):
        self.buf += "%f setgray fill\n" % (gray)

    def do_textCenter(self,x,y,text):
        self.buf += "%g " % (x)             # X
        self.buf += "(%s) stringwidth pop " % (text) # puts width of string on stack
        self.buf += " 2 div "
        self.buf += "sub "            # stack is now x-stringwidth(text)/2
        self.buf += "%g " % (y)       # puts Y on stack
        self.buf += "moveto (%s) show\n" % (text)

    def do_name(self,font,name,y,lang):
	if (lang):
		page = "Hoja _____"
		subject = "Asunto: ____________________"
	else:
		page = "Page _____"
                subject	= "Subject: ____________________"
        self.setfont(font,8)
        self.do_text(1*72+4,y,name)
        self.do_text(1*72+4,y-8,"Please return if found")
        self.setfont(font,16)
        self.do_text(6.5*72,y-16,page)
        self.do_text(1*72+4,10.4*72,subject)    
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
        
    def do_calendar(self,font,x,y,size,width,year,month,lang):
	if(lang):
		days   = ("L","M","X","J","V","S","D")
		week_start = 0
		months = ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre")
	else:
		days   = ("S","M","Tu","W","Th","F","S")
		week_start = 1
		months = ("January","February","March","April","May","June","July","August","September","October","November","December")
        import time;
                
	if(month<1 or month>12):
            raise InvalidMonth
        self.setfont(font,size)

        self.buf += "0.8 setgray %g %g %g %g rectfill 0 setgray " \
                    % (x,y-(size+1),width*7+4,size-1)


        t   = time.mktime((year,month,1,0,0,0,0,0,0))
        tm  = time.localtime(t)
        today = time.localtime(time.time())
        self.do_textCenter(x+width*4,y,"%s %d" % (months[month-1],year))
        y -= size

        for i in range(0,7):
            self.do_textRight(x+(i+1)*width,y,days[i])
        y -= size                       # down a line

        if(tm < today): self.buf += "0.5 setgray "    # stuff in the past is in gray
        while(tm.tm_mon == month):
            day = (tm.tm_wday+week_start) % 7    # tm_wday==0 for Monday

            if(tm.tm_mon == today.tm_mon and (tm.tm_mday == today.tm_mday)):
                self.buf += "0 setgray " # today and on is black

            self.do_textRight(x+(1+day)*width,y,"%d" % tm.tm_mday)
            if(day==6):
                y -= size               # We were Saturday; go to next line
            t += 60*60*24;
            tm = time.localtime(t)      # get the day
        
    def do_notepaper(self,do_summary,do_holes):
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

        self.do_name(self.font,self.name,72-8,self.lang)
        self.do_calendar(self.font,5.4*72,10.7*72,8,12,tm.tm_year,tm.tm_mon,self.lang)

        next_month = tm.tm_mon+1
        next_year  = tm.tm_year
        if(next_month>12):
            next_month  = 1
            next_year  += 1

        self.do_calendar(self.font,6.8*72,10.7*72,8,12,next_year,next_month,self.lang)
        self.done()
        return self.buf