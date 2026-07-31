#!/usr/bin/env bash
echo "Pyfa version (ENV):"
echo "${PYFA_VERSION}"
echo "Pyfa version (YAML):"
cat version.yml
echo "Building distributive..."
uv run --group packaging python -m PyInstaller -y --clean dist_assets/mac/pyfa.spec
echo "Compressing distributive..."
cd dist
zip -yr "pyfa-$PYFA_VERSION-mac.zip" pyfa.app
md5 -r "pyfa-$PYFA_VERSION-mac.zip"
