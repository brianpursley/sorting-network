#!/bin/bash

pushd "$(dirname "$0")" > /dev/null || exit 1

for f in ../examples/*.cn; do
    ../sortingnetwork.py -i "$f" svg "${f%.cn}.svg"
    ../sortingnetwork.py -i "$f" svg | rsvg-convert > "${f%.cn}.png"
done

popd > /dev/null || exit 1
