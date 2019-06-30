.DEFAULT_GOAL := all

.PHONY: all
all :build install 

.PHONY: build
build:
	python setup.py sdist


.PHONY: install
install:
	pip install dist/$$(ls -s -c dist | grep -v total  | cut -d ' ' -f 2 | head -n 1 )


.PHONE: coverage
coverage:
	coverage3 erase
	coverage3 run pytest
	coverage3 report -m


