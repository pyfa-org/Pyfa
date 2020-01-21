#!/usr/bin/env bash
wget "https://www.python.org/ftp/python/${PYTHON}/python-${PYTHON}-macosx10.6.pkg"
sudo installer -pkg python-${PYTHON}-macosx10.6.pkg -target /
sudo python3 -m ensurepip --upgrade
# A manual check that the correct version of Python is running.
python3 --version
python3 -m pip install -r requirements.txt
python3 -m pip install PyInstaller==3.3
