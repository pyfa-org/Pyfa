#!/usr/bin/env bash
echo "Python version:"
python3 --version
echo "Upgrading pip..."
python3 -m pip install --upgrade pip
# See issue #2156
echo "Upgrading setuptools..."
python3 -m pip install --upgrade setuptools
echo "Installing app requirements..."
python3 -m pip install -r requirements.txt
echo "Installing packaging tools..."
python3 -m pip install PyInstaller==3.6
