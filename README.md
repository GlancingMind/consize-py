# How to run - The REPL?

You can use the provided docker container:

```bash
docker build -t consize-py . # to build the container image
docker run -i -t consize-py  # to run the container
```

Or by invoking python directly:

```bash
python src/main.py "\ prelude/prelude.txt run say-hi"
```

Or just use make :-)

```bash
make consize
```

# And how to run - The Prelude Tests?

```bash
docker run -i -t consize-py "\ prelude/prelude.txt run \ prelude/prelude-test.txt run"
```

Or by invoking python directly:

```bash
python src/main.py "\ prelude/prelude.txt run \ prelude/prelude-test.txt run"
```

Or again, just use make :-)

```bash
make prelude-test
```

# Required Dependencies

- Python
- requests
- and requests-file
