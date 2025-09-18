.PHONY: default
default: ttf zip web

SRC_BASEFONT			= src/basefont
DIST_TTF			= dist/ttf
SUPPORT_BIN			= support/bin
DIST_ZIP			= dist/zip

FONT_PACKAGE_NAME		= RoutedGothic

VERSION				= 1.0.0
SFNT_REVISION			= 001.000
#				  XXX.YZZ, typically

VENDOR				= DARN
COPYRIGHT_OWNER			= Darren Embry
COPYRIGHT_EMAIL			= dsembry@gmail.com

SOURCE				= $(SRC_BASEFONT)/routed-gothic-stroke-source.sfd
ZIP_FILE			= $(DIST_ZIP)/routed-gothic-ttf.zip
TTF_FONTS			= $(DIST_TTF)/routed-gothic.ttf \
				  $(DIST_TTF)/routed-gothic-half-italic.ttf \
				  $(DIST_TTF)/routed-gothic-italic.ttf \
				  $(DIST_TTF)/routed-gothic-narrow.ttf \
				  $(DIST_TTF)/routed-gothic-narrow-half-italic.ttf \
				  $(DIST_TTF)/routed-gothic-narrow-italic.ttf \
				  $(DIST_TTF)/routed-gothic-wide.ttf \
				  $(DIST_TTF)/routed-gothic-wide-half-italic.ttf \
				  $(DIST_TTF)/routed-gothic-wide-italic.ttf
GLYPH_LIST			= includes/unicode-coverage.inc.html
GENERATE_SCRIPT			= $(SUPPORT_BIN)/generate-fonts.py
GLYPH_LIST_SCRIPT		= $(SUPPORT_BIN)/make-character-list

FONTS				= $(TTF_FONTS)

.PHONY: dist
dist: fonts zip

.PHONY: fonts
fonts: ttf

.PHONY: zip
zip: $(ZIP_FILE)

.PHONY: ttf
ttf: $(firstword $(TTF_FONTS))
# single command builds all fonts, only specify first font

###############################################################################

$(TTF_FONTS): $(SOURCE) Makefile $(GENERATE_SCRIPT)
	$(GENERATE_SCRIPT)

$(ZIP_FILE): $(TTF_FONTS) Makefile
	rm $@ || true
	mkdir -p $(DIST_ZIP)
	cd $(DIST_ZIP) && zip $(patsubst $(DIST_ZIP)/%, %, $@) $(patsubst $(DIST_ZIP)/%, %, $(TTF_FONTS))

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
	$(SUPPORT_BIN)/make-downloads

publish:
	ssh dse@webonastick.com "bash -c 'cd /www/webonastick.com/htdocs/fonts/routed-gothic && git pull'"

.PHONY: coverage
coverage: $(GLYPH_LIST)
$(GLYPH_LIST): $(SOURCE) $(GLYPH_LIST_SCRIPT) Makefile
	$(GLYPH_LIST_SCRIPT) $< >$@.tmp
	mv $@.tmp $@
