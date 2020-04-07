#!/usr/bin/env bash
echo "Python version:"
python3 --version
echo "Upgrading pip..."
python3 -m pip install --upgrade pip
echo "Installing hardcoded app requirements for debugging..."
python3 -m pip install matplotlib==3.2.0 SQLAlchemy==1.3.14 cryptography==2.8 PyYAML==5.3 six==1.13.0 Pillow==7.0.0 pyparsing==2.4.6 kiwisolver==1.1.0 certifi==2019.11.28 setuptools==42.0.2
echo "Installing app requirements..."
python3 -m pip install -r requirements.txt
echo "Installing packaging tools..."
python3 -m pip install PyInstaller==3.6
