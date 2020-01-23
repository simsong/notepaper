test-mac:
	python3 pdfmaker.py out.pdf --lang en --holes --summary
	open out.pdf

test-es:
	python3 notepaper.py out.pdf --lang es_ES.UTF-8 ; open out.pdf


loc:
	for fn in locales/*/LC_MESSAGES ; do cd $$fn ; python2 ../../../Tools/i18n/msgfmt.py -o base.mo base.po ; cd ../../.. ; done
