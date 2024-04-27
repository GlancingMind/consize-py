.Phony = tests

repl:
	python -i src/main.py

test:
	python -m unittest tests/*.py
