#!/usr/bin/env bash

echo "${PYFA_VERSION}"

cat version.yml
python3 -m PyInstaller -y --clean --windowed dist_assets/mac/pyfa.spec
cd dist
zip -r "pyfa-$PYFA_VERSION-mac.zip" pyfa.app
curl --upload-file "pyfa-$PYFA_VERSION-mac.zip" https://transfer.sh/
echo -e "\n"
md5 -r "pyfa-$PYFA_VERSION-mac.zip"