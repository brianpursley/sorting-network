#!/bin/bash

pushd "$(dirname "$0")" > /dev/null || exit 1

../sortingnetwork.py -i ../examples/3-input.cn svg ../examples/3-input.svg
../sortingnetwork.py -i ../examples/3-input.cn svg | rsvg-convert > ../examples/3-input.png

../sortingnetwork.py -i ../examples/4-input.cn svg ../examples/4-input.svg
../sortingnetwork.py -i ../examples/4-input.cn svg | rsvg-convert > ../examples/4-input.png

../sortingnetwork.py -i ../examples/5-input.cn svg ../examples/5-input.svg
../sortingnetwork.py -i ../examples/5-input.cn svg | rsvg-convert > ../examples/5-input.png

../sortingnetwork.py -i ../examples/6-input.cn svg ../examples/6-input.svg
../sortingnetwork.py -i ../examples/6-input.cn svg | rsvg-convert > ../examples/6-input.png

../sortingnetwork.py -i ../examples/7-input.cn svg ../examples/7-input.svg
../sortingnetwork.py -i ../examples/7-input.cn svg | rsvg-convert > ../examples/7-input.png

../sortingnetwork.py -i ../examples/8-input.cn svg ../examples/8-input.svg
../sortingnetwork.py -i ../examples/8-input.cn svg | rsvg-convert > ../examples/8-input.png

../sortingnetwork.py -i ../examples/8-input-bitonic.cn svg ../examples/8-input-bitonic.svg
../sortingnetwork.py -i ../examples/8-input-bitonic.cn svg | rsvg-convert > ../examples/8-input-bitonic.png

../sortingnetwork.py -i ../examples/9-input.cn svg ../examples/9-input.svg
../sortingnetwork.py -i ../examples/9-input.cn svg | rsvg-convert > ../examples/9-input.png

../sortingnetwork.py -i ../examples/10-input.cn svg ../examples/10-input.svg
../sortingnetwork.py -i ../examples/10-input.cn svg | rsvg-convert > ../examples/10-input.png

../sortingnetwork.py -i ../examples/11-input.cn svg ../examples/11-input.svg
../sortingnetwork.py -i ../examples/11-input.cn svg | rsvg-convert > ../examples/11-input.png

../sortingnetwork.py -i ../examples/12-input.cn svg ../examples/12-input.svg
../sortingnetwork.py -i ../examples/12-input.cn svg | rsvg-convert > ../examples/12-input.png

../sortingnetwork.py -i ../examples/16-input.cn svg ../examples/16-input.svg
../sortingnetwork.py -i ../examples/16-input.cn svg | rsvg-convert > ../examples/16-input.png

popd > /dev/null || exit 1
