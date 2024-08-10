FROM python

WORKDIR /app

COPY . .

ENTRYPOINT ["python", "/app/src/main.py", "consize.ruleset", "load-rules"]
CMD ["-v", "-i"]
