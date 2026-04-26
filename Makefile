PYTHON ?= .venv/bin/python
PIP ?= $(PYTHON) -m pip
UVICORN ?= $(PYTHON) -m uvicorn
PYTEST ?= $(PYTHON) -m pytest
HOST ?= 127.0.0.1
PORT ?= 8000

.PHONY: install run test

install:
	$(PIP) install -r requirements.txt

run:
	$(UVICORN) app.main:app --host $(HOST) --port $(PORT) --reload

test:
	$(PYTEST)
