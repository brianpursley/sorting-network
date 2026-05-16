#!/bin/bash

set -e

pushd "$(dirname "$0")" > /dev/null || exit 1

printf "Running benchmarks...\n\n"

echo -n "check 16-input ... "
time ../sortingnetwork.py -i ../examples/16-input.cn check
echo

echo -n "check 24-input ... "
time ../sortingnetwork.py -i ../examples/24-input.cn check
echo

echo -n "check 28-input ... "
time ../sortingnetwork.py -i ../examples/28-input.cn check
echo

echo -n "check 32-input ... "
time ../sortingnetwork.py -i ../examples/32-input.cn check
echo

popd > /dev/null || exit 1
