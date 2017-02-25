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

coverage:
	@coverage run -m unittest
	@coverage report --show-missing --skip-covered --fail-under=100 \
		--include=toolrack/\* --omit=**/test_\*.py

lint:
	@$(LINT) setup.py toolrack

html:
	sphinx-build -b html docs html

.PHONY: build html
