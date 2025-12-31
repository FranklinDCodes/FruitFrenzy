#!/usr/bin/env zsh

SCRIPT_DIR="${0:A:h}"
cd "$SCRIPT_DIR" || exit 1

pip3 install -r requirements.txt

python3 main.py

