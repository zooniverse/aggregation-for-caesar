#!/bin/bash
cp README.md docs/source/README.md
cp Scripts.md docs/source/Scripts.md
cp Contributing.md docs/source/Contributing.md
cd docs
if [ -d build ]; then
  rm -r build
fi
make html
cd ..
