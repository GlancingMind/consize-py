[![Pattern Matching Tests](https://github.com/GlancingMind/consize-py/actions/workflows/docker-image.yml/badge.svg?branch=pattern-matching)](https://github.com/GlancingMind/consize-py/actions/workflows/docker-image.yml)

# How to run - The Interpreter?

You can use the provided docker container:

```bash
# to build the container image
docker build -t consize-py .
# to run the container
docker run -i -t consize-py
```

This will start the interpreter in verbose and interactive mode and with the consize.ruleset preloaded.

Or by invoking python directly:

```bash
python src/main.py -i -v consize.ruleset load-rules
```

Or just use make :-)

```bash
make consize
```

Note, it is recommended to always load the consize.ruleset, otherwise the interpreter will not provide any operations worth mentioning, unless you really want to start from scratch and enter every single rule live in the REPL. Also the `-i` stand for interactive mode. If `-i` is missing, the Interpreter will start running and only stop, when everything is done. With the interactive mode, you can step trough each operation. `-v` will command the interpreter to print the current stacks and therefore the *chain of reasoning*.

# And how to run - The Tests?

```bash
docker run -i -t consize-py "\ prelude/prelude.txt run \ prelude/prelude-test.txt run"
```

Or by invoking python directly:

```bash
python -m unittest tests/*.py
```

Or again, just use make :-)

```bash
make test
```
