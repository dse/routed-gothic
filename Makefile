SOURCE = src/routed-gothic-stroke-source.sfd

TTF_FONTS = \
	dist/ttf/routed-gothic.ttf \
	dist/ttf/routed-gothic-half-italic.ttf \
	dist/ttf/routed-gothic-italic.ttf \
	dist/ttf/routed-gothic-narrow.ttf \
	dist/ttf/routed-gothic-narrow-half-italic.ttf \
	dist/ttf/routed-gothic-narrow-italic.ttf \
	dist/ttf/routed-gothic-wide.ttf \
	dist/ttf/routed-gothic-wide-half-italic.ttf \
	dist/ttf/routed-gothic-wide-italic.ttf

EOT_FONTS = \
	dist/eot/routed-gothic.ttf2eot.eot \
	dist/eot/routed-gothic.mkeot.eot \
	dist/eot/routed-gothic-half-italic.ttf2eot.eot \
	dist/eot/routed-gothic-half-italic.mkeot.eot \
	dist/eot/routed-gothic-italic.ttf2eot.eot \
	dist/eot/routed-gothic-italic.mkeot.eot \
	dist/eot/routed-gothic-narrow.ttf2eot.eot \
	dist/eot/routed-gothic-narrow.mkeot.eot \
	dist/eot/routed-gothic-narrow-half-italic.ttf2eot.eot \
	dist/eot/routed-gothic-narrow-half-italic.mkeot.eot \
	dist/eot/routed-gothic-narrow-italic.ttf2eot.eot \
	dist/eot/routed-gothic-narrow-italic.mkeot.eot \
	dist/eot/routed-gothic-wide.ttf2eot.eot \
	dist/eot/routed-gothic-wide.mkeot.eot \
	dist/eot/routed-gothic-wide-half-italic.ttf2eot.eot \
	dist/eot/routed-gothic-wide-half-italic.mkeot.eot \
	dist/eot/routed-gothic-wide-italic.ttf2eot.eot \
	dist/eot/routed-gothic-wide-italic.mkeot.eot

FONTS = $(TTF_FONTS)

.PHONY: default
default: ttf-fonts eot-fonts

.PHONY: ttf-fonts
ttf-fonts: $(firstword $(TTF_FONTS))

.PHONY: eot-fonts
eot-fonts: $(EOT_FONTS)

###############################################################################

$(TTF_FONTS): $(SOURCE) Makefile bin/generate-fonts.py
	bin/generate-fonts.py

dist/eot/%.ttf2eot.eot: dist/ttf/%.ttf Makefile
	mkdir -p "$$(dirname "$@")"
	ttf2eot "$<" >"$@.tmp.eot"
	mv "$@.tmp.eot" "$@"

dist/eot/%.mkeot.eot: dist/ttf/%.ttf Makefile
	mkdir -p "$$(dirname "$@")"
	mkeot "$<" >"$@.tmp.eot"
	mv "$@.tmp.eot" "$@"

clean:
	find . -type f -name '*.tmp' -o -name '*.tmp.*' -exec rm {} +

superclean:
	find dist -type f -exec rm {} +
