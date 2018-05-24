<<<<<<< Makefile
out.pdf: out.ps
	gs -dNOPAUSE -SOutputFile=out.pdf -sDEVICE=pdfwrite -dBATCH out.ps
=======
mp:
	python makepaper.py -o test.ps
>>>>>>> 1.3

out.ps: makepaper.py
	python makepaper.py out.ps 

