#! /usr/bin/env bash

python3 -m ensurepip
python3 -m pip install -r ./requirements.txt
NO_SUDO=1 ./install.py
python3 ./src/main.py init
python3 ./src/main.py create wttr.in "curl -X GET wttr.in"
python3 ./src/main.py serve 6969 0.0.0.0
