.DEFAULT_GOAL := all

PYTHON = python3
COV = coverage
PYSRC = ham
PYTST = ham/tests
VIRTUALENVWRAPPER_SCRIPT = source ~\pe38\bin\activate

all :build install 


build:
	python setup.py sdist


check:
	$(PYTHON) -m pylint -E            $(PYSRC)
	$(PYTHON) -m black --check --diff $(PYSRC)
	#shellcheck -x scripts/*

format:
	$(PYTHON) -m black $(PYSRC)


test:
	$(PYTHON) -m pytest $(PYTST)

coverage:
	pytest --cov=$(PYSRC)


install:
	pip install dist/$$(ls -asl dist | tail  -n 1 | perl -lane \'print $F[9]\')
	#pip install dist/$$(ls -s -c dist | grep -v total  | cut -d ' ' -f 2 | head -n 1 )

.DEFAULT_GOAL := fullcheck
#Check all is formatted
#Passes tests
fullcheck:
	$(MAKE) check
	$(MAKE) test

