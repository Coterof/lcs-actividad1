all: test bench plots

test:
	python -m pytest tests -q

bench:
	python src/benchmark.py

plots:
	python src/graficas.py
