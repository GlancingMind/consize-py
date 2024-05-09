.Phony = tests

repl:
	python -i src/main.py

consize:
	python src/main.py "\ src/prelude.txt run say-hi"

test:
	#python -m unittest tests/*.py
	python src/main.py "\ src/prelude.txt run \ src/prelude-test.txt run"
