#!/bin/bash
cp README.md docs/source/README.md
cp Scripts.md docs/source/Scripts.md
cp Contributing.md docs/source/Contributing.md
cp CODE_OF_CONDUCT.md docs/source/CODE_OF_CONDUCT.md
cd docs
if [ -d build ]; then
  rm -r build
fi
make html
cd ..
