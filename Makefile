.Phony = tests

consize:
	python src/main.py -i -v consize.ruleset load-rules

test:
	python -m unittest tests/*.py
