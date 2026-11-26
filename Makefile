PYTHON ?= python

all: test bench plots

test:
	$(PYTHON) -m pytest tests -q

bench:
	$(PYTHON) src/benchmark.py

plots:
	$(PYTHON) src/graficas.py
