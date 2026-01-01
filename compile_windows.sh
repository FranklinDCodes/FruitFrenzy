#! /bin/bash

# run this from the base FruitFrenzy dir

version=$1

pyinstaller --onefile --windowed --add-data "assets;assets" --name "FruitFrenzy${version}" main.py
rm "FruitFrenzy${version}.spec"
rm -r "build/FruitFrenzy${version}/"
