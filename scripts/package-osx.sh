#!/usr/bin/env bash

echo "${PYFA_VERSION}"

cat version.yml
python3 -m PyInstaller -y --clean --windowed dist_assets/mac/pyfa.spec
cd dist
zip -r "pyfa-$PYFA_VERSION-mac.zip" pyfa.app
curl --connect-timeout 30 --max-time 300 --upload-file "pyfa-$PYFA_VERSION-mac.zip" https://transfer.sh/ || echo 'upload to transfer.sh failed'
echo -e "\n"
md5 -r "pyfa-$PYFA_VERSION-mac.zip"
