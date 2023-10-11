#!/usr/bin/env bash

# Activate your conda environment
source activate /Users/tadeasfort/.pyenv/versions/anaconda3-2023.07-2/envs/pyfa

# Check if PYFA_VERSION is set
if [ -z "$PYFA_VERSION" ]; then
  echo "PYFA_VERSION is not set. Exiting."
  exit 1
fi

# Check if version.yml exists
if [ ! -f "version.yml" ]; then
  echo "version.yml not found. Exiting."
  exit 1
fi

echo "Pyfa version (ENV): $PYFA_VERSION"
echo "Pyfa version (YAML):"
cat version.yml

# Build the application
echo "Building distributive..."
python -m PyInstaller -y --clean dist_assets/mac/pyfa.spec

# Check if dist directory exists
if [ ! -d "dist" ]; then
  echo "dist directory not found. Exiting."
  exit 1
fi

echo "Compressing distributive..."
cd dist
/usr/libexec/PlistBuddy -c "Add :CFBundleVersion string $PYFA_VERSION" "pyfa.app/Contents/Info.plist"
/usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString $PYFA_VERSION" "pyfa.app/Contents/Info.plist"
zip -r "pyfa-$PYFA_VERSION-mac.zip" pyfa.app
md5 -r "pyfa-$PYFA_VERSION-mac.zip"
