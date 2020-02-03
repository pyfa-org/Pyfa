#!/usr/bin/env bash
echo "Upgrading pip"
sudo python3 -m ensurepip --upgrade
echo "Checking python version"
python3 --version
echo "Installing app requirements"
python3 -m pip install -r requirements.txt
echo "Installing packaging tools"
python3 -m pip install PyInstaller==3.6
