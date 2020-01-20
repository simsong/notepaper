test:
	python3 notepaper.py out.pdf ; open out.pdf

test-de:
	python3 notepaper.py out.pdf --lang de_DE.UTF-8 ; open out.pdf

test-es:
	python3 notepaper.py out.pdf --lang es_ES.UTF-8 ; open out.pdf


loc:
	for fn in locales/*/LC_MESSAGES ; do cd $$fn ; python2 ../../../Tools/i18n/msgfmt.py -o base.mo base.po ; cd ../../.. ; done
