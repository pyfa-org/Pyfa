#!/usr/bin/env bash
wget "https://www.python.org/ftp/python/${PYTHON}/python-${PYTHON}-macosx10.6.pkg"
sudo installer -pkg python-${PYTHON}-macosx10.6.pkg -target /
sudo python3 -m ensurepip
# A manual check that the correct version of Python is running.
python3 --version
pip3 install -r requirements.txt
