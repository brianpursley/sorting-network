#!/bin/bash

pushd "$(dirname "$0")" > /dev/null || exit 1
pushd ../tests > /dev/null || exit 1

if command -v pypy3 &> /dev/null; then
  echo "Running unit tests with pypy3..."
  PYTHON=pypy3
elif command -v pypy &> /dev/null; then
  echo "Running unit tests with pypy..."
  PYTHON=pypy
elif command -v python3 &> /dev/null; then
  echo "Running unit tests with python3..."
  PYTHON=python3
else
  echo "Running unit tests with python..."
  PYTHON=python
fi

PYTHONPATH=.. $PYTHON -m unittest ./*_test.py -v

popd > /dev/null || exit 1
popd > /dev/null || exit 1
