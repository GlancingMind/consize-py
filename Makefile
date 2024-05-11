.Phony = tests

consize:
	python src/main.py "\ prelude/prelude.txt run say-hi"

prelude-test:
	python src/main.py "\ prelude/prelude.txt run \ prelude/prelude-test.txt run"

test:
	python -m unittest tests/*.py
