#!/bin/bash
cp README.md docs/source/README.md
cp Scripts.md docs/source/Scripts.md
cp GUI.md docs/source/GUI.md
cp Contributing.md docs/source/Contributing.md
cp CODE_OF_CONDUCT.md docs/source/CODE_OF_CONDUCT.md
cp _static/*.png docs/source/_static/
cd docs
if [ -d build ]; then
  rm -r build
fi
make html
cd ..
