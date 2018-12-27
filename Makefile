SOURCE = src/routed-gothic-stroke-source.sfd

TTF_FONTS = \
	dist/routed-gothic.ttf \
	dist/routed-gothic-Half-Italic.ttf \
	dist/routed-gothic-Italic.ttf \
	dist/routed-gothic-Narrow.ttf \
	dist/routed-gothic-Narrow-Half-Italic.ttf \
	dist/routed-gothic-Narrow-Italic.ttf \
	dist/routed-gothic-Wide.ttf \
	dist/routed-gothic-Wide-Half-Italic.ttf \
	dist/routed-gothic-Wide-Italic.ttf

EOT_FONTS = \
	dist/routed-gothic.ttf2eot.eot \
	dist/routed-gothic.mkeot.eot \
	dist/routed-gothic-Half-Italic.ttf2eot.eot \
	dist/routed-gothic-Half-Italic.mkeot.eot \
	dist/routed-gothic-Italic.ttf2eot.eot \
	dist/routed-gothic-Italic.mkeot.eot \
	dist/routed-gothic-Narrow.ttf2eot.eot \
	dist/routed-gothic-Narrow.mkeot.eot \
	dist/routed-gothic-Narrow-Half-Italic.ttf2eot.eot \
	dist/routed-gothic-Narrow-Half-Italic.mkeot.eot \
	dist/routed-gothic-Narrow-Italic.ttf2eot.eot \
	dist/routed-gothic-Narrow-Italic.mkeot.eot \
	dist/routed-gothic-Wide.ttf2eot.eot \
	dist/routed-gothic-Wide.mkeot.eot \
	dist/routed-gothic-Wide-Half-Italic.ttf2eot.eot \
	dist/routed-gothic-Wide-Half-Italic.mkeot.eot \
	dist/routed-gothic-Wide-Italic.ttf2eot.eot \
	dist/routed-gothic-Wide-Italic.mkeot.eot

FONTS = $(TTF_FONTS)

.PHONY: default
default:
	make ttf-fonts
	make eot-fonts
	make stage charlist

.PHONY: publish
publish:
	make ttf-fonts
	make eot-fonts
	svn commit -m ""
	make stage charlist publish-after-stage

.PHONY: fonts
fonts:
	make $(FONTS)

.PHONY: ttf-fonts
ttf-fonts:
	make $(TTF_FONTS)

.PHONY: eot-fonts
eot-fonts:
	make $(EOT_FONTS)

###############################################################################

$(TTF_FONTS): $(SOURCE) bin/generate-fonts.py
	bin/generate-fonts.py

%.ttf2eot.eot: %.ttf
	ttf2eot "$<" >"$@.tmp.eot"
	mv "$@.tmp.eot" "$@"

%.mkeot.eot: %.ttf
	mkeot "$<" >"$@.tmp.eot"
	mv "$@.tmp.eot" "$@"
