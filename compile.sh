#! /bin/bash

# run this from the base FruitFrenzy dir

version=$1

pyinstaller --onefile --windowed --add-data "assets;assets" --name "FruitFrenzy$1" main.py
rm FruitFrenzy$1.spec
rm -r build/FruitFrenzy$1/
