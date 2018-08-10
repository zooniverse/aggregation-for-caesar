#!/bin/bash
cd docs
if [ -d build ]; then
  rm -r build
fi
make html
cd ..
