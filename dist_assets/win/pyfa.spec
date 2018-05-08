# -*- mode: python -*-

import os
from itertools import chain
import subprocess
import requests.certs

label = subprocess.check_output([
    "git", "describe", "--tags"]).strip()

with open('.version', 'w+') as f:
    f.write(label.decode())

block_cipher = None

added_files = [
             ('../../imgs/gui/*.png', 'imgs/gui'),
             ('../../imgs/gui/*.gif', 'imgs/gui'),
             ('../../imgs/icons/*.png', 'imgs/icons'),
             ('../../imgs/renders/*.png', 'imgs/renders'),
             ('../../service/jargon/*.yaml', 'service/jargon'),
             ('../../dist_assets/win/pyfa.ico', '.'),
             (requests.certs.where(), '.'),  # is this needed anymore?
             ('../../eve.db', '.'),
             ('../../README.md', '.'),
             ('../../LICENSE', '.'),
             ('../../.version', '.'),
             ]

import_these = []

# Walk directories that do dynamic importing
paths = ('eos/effects', 'eos/db/migrations', 'service/conversions')
for root, folders, files in chain.from_iterable(os.walk(path) for path in paths):
    for file_ in files:
        if file_.endswith(".py") and not file_.startswith("_"):
            mod_name = "{}.{}".format(
                root.replace("/", "."),
                file_.split(".py")[0],
            )
            import_these.append(mod_name)

a = Analysis(['../../pyfa.py'],
             pathex=[
                 # Need this, see https://github.com/pyinstaller/pyinstaller/issues/1566
                 # To get this, download and install windows 10 SDK
                 # If not building on Windows 10, this might be optional
                 r'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x86'],
             binaries=[],
             datas=added_files,
             hiddenimports=import_these,
             hookspath=['dist_assets/pyinstaller_hooks'],
             runtime_hooks=[],
             excludes=['Tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          debug=False,
          console=False,
          strip=False,
          upx=True,
          name='pyfa',
          icon='dist_assets/win/pyfa.ico',
          )

coll = COLLECT(
               exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='pyfa',
               icon='dist_assets/win/pyfa.ico',
               )