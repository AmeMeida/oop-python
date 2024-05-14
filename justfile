set shell := ["fish", "-c"]

venv:
    uv venv

run:
    python3 src/passagem.py

test:
    just run < entrada.in | diff -y - expected.out
