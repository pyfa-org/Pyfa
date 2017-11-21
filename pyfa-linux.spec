# -*- mode: python -*-

import os
from itertools import chain
import subprocess

label = subprocess.check_output([
    "git", "describe", "--tags"]).strip()

with open('gitversion', 'w+') as f:
    f.write(label.decode())

block_cipher = None


added_files = [
             ( 'imgs/gui/*.png', 'imgs/gui' ),
             ( 'imgs/gui/*.gif', 'imgs/gui' ),
             ( 'imgs/icons/*.png', 'imgs/icons' ),
             ( 'imgs/renders/*.png', 'imgs/renders' ),
             ( 'dist_assets/win/pyfa.ico', '.' ),
             ( 'dist_assets/cacert.pem', '.' ),
             ( 'eve.db', '.' ),
             ( 'README.md', '.' ),
             ( 'LICENSE', '.' ),
             ( 'gitversion', '.' ),
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


a = Analysis(['pyfa.py'],
             pathex=[],
             binaries=[],
             datas=added_files,
             hiddenimports=import_these,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='pyfa',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='pyfa')
