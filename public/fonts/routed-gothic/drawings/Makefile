%.pdf: %.svg Makefile
	inkscape -o "$@.tmp.pdf" "$<"
	mv "$@.tmp.pdf" "$@"
%-96dpi.png: %.svg Makefile
	inkscape -o "$@.tmp.png" "$<"
	mv "$@.tmp.png" "$@"
%-300dpi.png: %.svg Makefile
	inkscape -o "$@.tmp.png" -d 300 -b white "$<"
	mv "$@.tmp.png" "$@"
