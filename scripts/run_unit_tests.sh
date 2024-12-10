#!/bin/bash

pushd "$(dirname "$0")" > /dev/null || exit 1
pushd ../tests > /dev/null || exit 1

PYTHONPATH=.. python -m unittest ./*_test.py -v

popd > /dev/null || exit 1
popd > /dev/null || exit 1
