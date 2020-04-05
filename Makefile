SOURCE =		src/routed-gothic-stroke-source.sfd
ZIP_FILE =		dist/routed-gothic-ttf.zip
TTF_FONTS =		dist/ttf/routed-gothic.ttf \
			dist/ttf/routed-gothic-half-italic.ttf \
			dist/ttf/routed-gothic-italic.ttf \
			dist/ttf/routed-gothic-narrow.ttf \
			dist/ttf/routed-gothic-narrow-half-italic.ttf \
			dist/ttf/routed-gothic-narrow-italic.ttf \
			dist/ttf/routed-gothic-wide.ttf \
			dist/ttf/routed-gothic-wide-half-italic.ttf \
			dist/ttf/routed-gothic-wide-italic.ttf
GLYPH_LIST =		includes/unicode-coverage.inc.html
GENERATE_SCRIPT =	bin/generate-fonts.py
GLYPH_LIST_SCRIPT =	bin/make-character-list

FONTS = $(TTF_FONTS)

.PHONY: default
default: ttf zip web

.PHONY: dist
dist: fonts zip

.PHONY: fonts
fonts: ttf

.PHONY: zip
zip: $(ZIP_FILE)

.PHONY: ttf
ttf: $(firstword $(TTF_FONTS))
# single command builds all fonts, only specify first one

###############################################################################

$(TTF_FONTS): $(SOURCE) Makefile $(GENERATE_SCRIPT)
	$(GENERATE_SCRIPT)

$(ZIP_FILE): $(TTF_FONTS) Makefile
	rm $@ || true
	cd dist && zip $(patsubst dist/%, %, $@) $(patsubst dist/%, %, $(TTF_FONTS))

.PHONY: clean
clean:
	find . -type f \( \
		-name '*.tmp' \
		-o -name '*.tmp.*' \
		-o -name '#*#' \
		-o -name '#~' \
	\) -exec rm {} +

.PHONY: superclean
superclean: clean
	find dist -type f -exec rm {} +

.PHONY: web
web: coverage sass

.PHONY: sass
sass:
	gulp sass

.PHONY: downloads
downloads:
	bin/make-downloads

publish:
	ssh dse@webonastick.com "bash -c 'cd /www/webonastick.com/htdocs/fonts/routed-gothic && git pull'"

.PHONY: coverage
coverage: $(GLYPH_LIST)
$(GLYPH_LIST): $(SOURCE) $(GLYPH_LIST_SCRIPT) Makefile
	$(GLYPH_LIST_SCRIPT) $< >$@.tmp
	mv $@.tmp $@
