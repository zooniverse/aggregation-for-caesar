#!/bin/bash
cp README.md docs/source/README.md
cd docs
make clean
make html
cd ..
