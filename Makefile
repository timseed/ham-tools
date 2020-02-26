.DEFAULT_GOAL := all

PYSRC = ham
PYTEST = ham/tests


VENV_NAME?=pe38
VENV_ACTIVATE=. ~/$(VENV_NAME)/bin/activate
PYTHON=~/${VENV_NAME}/bin/python3
PIP = pip3
PYCOV = $(PYTHON) -m coverage
Package = ham-1.0.3.tar.gz



all : check test build install 

.phony build:
build:
	python setup.py sdist
	-$(PIP) install "./dist/$(Package)"

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
