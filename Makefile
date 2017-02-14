PYTHON = python3
SETUP = $(PYTHON) setup.py
LINT = $(PYTHON) -m flake8


all: build

build:
	$(SETUP) build

devel:
	$(SETUP) develop

clean:
	rm -rf build html *.egg-info _trial_temp
	find . -type d -name __pycache__ | xargs rm -rf

test:
	tox

lint:
	@$(LINT) setup.py toolrack

html:
	sphinx-build -b html docs html

.PHONY: build html
