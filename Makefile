.Phony = tests

repl:
	python -i src/main.py

consize:
	python src/main.py "\ src/prelude.txt run say-hi"

test:
	python -m unittest tests/*.py
