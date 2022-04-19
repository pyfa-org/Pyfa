#!/usr/bin/env bash
echo "Pyfa version (ENV):"
echo "${PYFA_VERSION}"
echo "Pyfa version (YAML):"
cat version.yml
echo "Building distributive..."
python3 -m PyInstaller -y --clean --windowed dist_assets/mac/pyfa.spec
echo "Compressing distributive..."
cd dist
/usr/libexec/PlistBuddy -c "Add :CFBundleVersion string ${PYFA_VERSION}" "pyfa.app/Contents/Info.plist" # Add missing
/usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString ${PYFA_VERSION}" "pyfa.app/Contents/Info.plist" # Modify existing
zip -r "pyfa-$PYFA_VERSION-mac.zip" pyfa.app
md5 -r "pyfa-$PYFA_VERSION-mac.zip"
