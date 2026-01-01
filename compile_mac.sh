#!/usr/bin/env zsh

# run this from the base FruitFrenzy dir

version="$1"

pyinstaller --onefile --windowed \
  --add-data "assets:assets" \
  --name "FruitFrenzy${version}" \
  main.py

rm -f "FruitFrenzy${version}.spec"
rm -rf "build/FruitFrenzy${version}/"
