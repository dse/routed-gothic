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
	dist/eot/routed-gothic.eot \
	dist/eot/routed-gothic-half-italic.eot \
	dist/eot/routed-gothic-italic.eot \
	dist/eot/routed-gothic-narrow.eot \
	dist/eot/routed-gothic-narrow-half-italic.eot \
	dist/eot/routed-gothic-narrow-italic.eot \
	dist/eot/routed-gothic-wide.eot \
	dist/eot/routed-gothic-wide-half-italic.eot \
	dist/eot/routed-gothic-wide-italic.eot

FONTS = $(TTF_FONTS)

.PHONY: default
default: ttf eot web

.PHONY: ttf
ttf: $(firstword $(TTF_FONTS))

.PHONY: eot
eot: $(EOT_FONTS)

###############################################################################

$(TTF_FONTS): $(SOURCE) Makefile bin/generate-fonts.py
	bin/generate-fonts.py

# why I chose mkeot over ttf2eot:
# https://lists.w3.org/Archives/Public/www-font/2010JanMar/0015.html
dist/eot/%.eot: dist/ttf/%.ttf Makefile
	mkdir -p "$$(dirname "$@")"
	mkeot "$<" >"$@.tmp.eot"
	mv "$@.tmp.eot" "$@"

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

WEB_REMOTE_USER=dse@webonastick.com
WEB_REMOTE_ROOT=/www/webonastick.com/htdocs/fonts/routed-gothic

.PHONY: publish
publish: downloads
	rsync -avCc --delete --exclude=download --exclude=fonts _site/    $(WEB_REMOTE_USER):$(WEB_REMOTE_ROOT)/
	rsync -avCc --delete                                    download/ $(WEB_REMOTE_USER):$(WEB_REMOTE_ROOT)/download/
	rsync -avCc --delete                                    dist/ttf/ $(WEB_REMOTE_USER):$(WEB_REMOTE_ROOT)/fonts/

.PHONY: local
local: downloads
	rsync -avCc --delete download/ _site/download/
	rsync -avCc --delete dist/ttf/ _site/fonts/

.PHONY: downloads
downloads:
	bin/make-downloads

.PHONY: coverage
coverage: _site/includes/unicode-coverage.inc.html
_site/includes/unicode-coverage.inc.html: src/routed-gothic-stroke-source.sfd bin/make-character-list Makefile
	bin/make-character-list $< >$@.tmp
	mv $@.tmp $@
