.DEFAULT_GOAL := all

PYTHON = python3
COV = coverage
PYSRC = ham
PYTST = ham/tests
VIRTUALENVWRAPPER_SCRIPT = source ~\pe38\bin\activate

all : check test build install 

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
	pip install $$(ls -tr dist/*.gz | tail -1 )

.DEFAULT_GOAL := all 
