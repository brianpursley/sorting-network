#!/bin/bash

pushd "$(dirname "$0")" > /dev/null || exit 1

../sortingnetwork.py --input ../examples/4-input.cn --svg > ../examples/4-input.svg
../sortingnetwork.py --input ../examples/4-input.cn --svg | rsvg-convert > ../examples/4-input.png

../sortingnetwork.py --input ../examples/5-input.cn --svg > ../examples/5-input.svg
../sortingnetwork.py --input ../examples/5-input.cn --svg | rsvg-convert > ../examples/5-input.png

../sortingnetwork.py --input ../examples/8-input-bitonic.cn --svg > ../examples/8-input-bitonic.svg
../sortingnetwork.py --input ../examples/8-input-bitonic.cn --svg | rsvg-convert > ../examples/8-input-bitonic.png

../sortingnetwork.py --input ../examples/16-input.cn --svg > ../examples/16-input.svg
../sortingnetwork.py --input ../examples/16-input.cn --svg | rsvg-convert > ../examples/16-input.png

popd > /dev/null || exit 1
