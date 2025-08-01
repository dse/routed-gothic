FONT_SRC		= src/basefont/routed-gothic-stroke-source.sfd
FONT_NAME		= RoutedGothic
SFNT_REVISION		= 001.000	# XXX.YZZ, typically
VERSION			= 0.9.2
TTF_FONTS		= 	dist/ttf/routed-gothic.ttf \
				dist/ttf/routed-gothic-half-italic.ttf \
				dist/ttf/routed-gothic-italic.ttf \
				dist/ttf/routed-gothic-narrow.ttf \
				dist/ttf/routed-gothic-narrow-half-italic.ttf \
				dist/ttf/routed-gothic-narrow-italic.ttf \
				dist/ttf/routed-gothic-wide.ttf \
				dist/ttf/routed-gothic-wide-half-italic.ttf \
				dist/ttf/routed-gothic-wide-italic.ttf

FIRST_TTF_FONT		= $(firstword $(TTF_FONTS))

GENERATE_SCRIPT		= bin/generate-fonts.py
# NOTE: hard-coded to put fonts into dist/ttf, dist/sfd, and dist/eot

FONTS			= $(TTF_FONTS)

default: fonts zip data

fonts: $(FONTS)

zip: $(ZIP_FILE)

###############################################################################
# JSON DATA
###############################################################################

data: FORCE src/data/font-data.json

src/data/font-data.json: Makefile $(FIRST_TTF_FONT)
	mkdir -p src/data
	fontdata "$(FIRST_TTF_FONT)" >"$@.tmp"
	mv "$@.tmp" "$@"

###############################################################################
# GENERATE FONTS
###############################################################################

ttf: FORCE $(FIRST_TTF_FONT)
# single command builds all fonts, only specify first one

$(TTF_FONTS): $(FONT_SRC) Makefile $(GENERATE_SCRIPT)
	$(GENERATE_SCRIPT)

###############################################################################
# ZIP FILE
###############################################################################

ZIP_FILE		= dist/zip/$(FONT_NAME).zip
VERSIONED_ZIP_FILE    	= dist/zip/$(FONT_NAME)-$(VERSION).zip

zip: FORCE $(VERSIONED_ZIP_FILE) $(ZIP_FILE)

$(VERSIONED_ZIP_FILE): FORCE
	mkdir -p dist/zip
	cd dist/zip && \
		bsdtar -c -f "$(FONT_NAME)-$(VERSION).zip" \
		--format zip \
		-s '#^\.\./ttf#$(FONT_NAME)-$(VERSION)#' \
		../ttf

$(ZIP_FILE): $(VERSIONED_ZIP_FILE) Makefile
	cp "$(VERSIONED_ZIP_FILE)" "$(ZIP_FILE)"

###############################################################################
# PUBLISH
###############################################################################

publish:
	ssh dse@webonastick.com "bash -c 'cd /www/webonastick.com/htdocs/fonts/routed-gothic && git pull'"

###############################################################################
# CLEAN
###############################################################################

.PHONY: clean
clean:
	find . -type f \( \
		-name '*.tmp' \
		-o -name '*.tmp.*' \
		-o -name '#*#' \
		-o -name '#~' \
	\) -exec rm {} +

###############################################################################
# BACKMATTER
###############################################################################

.PHONY: FORCE
