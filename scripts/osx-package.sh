#!/usr/bin/env bash
echo "Pyfa version (ENV):"
echo "${PYFA_VERSION}"
echo "Pyfa version (YAML):"
cat version.yml
echo "Building distributive..."
python3 -m PyInstaller -y --clean --windowed dist_assets/mac/pyfa.spec
echo "Compressing distributive..."
cd dist
zip -r "pyfa-$PYFA_VERSION-mac.zip" pyfa.app
echo "Uploading distributive to transfer.sh..."
curl --connect-timeout 30 --max-time 300 --upload-file "pyfa-$PYFA_VERSION-mac.zip" https://transfer.sh/ || echo 'upload to transfer.sh failed'
echo -e "\n"
md5 -r "pyfa-$PYFA_VERSION-mac.zip"
