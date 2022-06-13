.PHONY: default

# Generate PDF
default:
	latexmk -pdf main.tex

# Generate PNG from pdf
preview: default
	convert -density 150 main.pdf -quality 90 main.png

# Prepare archive to be used on overleaf
archive:
	rm -rf build
	mkdir build

	cp report-UTC.cls main.tex LICENSE README.md .gitignore .latexmkrc Makefile build/
	cp -r src Graphismes-UTC build/

	cd build &&	zip -r ../latex-rapport-UTC.zip *

# Prepare folder to be use as the content of gitlab pages
prepare_deploy: preview archive
	rm -rf deploy
	mkdir deploy

	cp main.pdf latex-rapport-UTC.zip main-0.png main-1.png deploy/

# Remove all temporary files
clean:
	latexmk -C
	rm -rf build deploy *.png *.zip
