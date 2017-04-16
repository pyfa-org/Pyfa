# -*- mode: python -*-

# Note: This script is provided AS-IS for those that may be interested.
# pyfa does not currently support pyInstaller (or any other build process) 100% at the moment

# Command line to build:
# (Run from directory where pyfa.py and pyfa.spec lives.)
# c:\Python27\scripts\pyinstaller.exe --clean --noconfirm --windowed --upx-dir=.\scripts\upx.exe pyfa.spec

# Don't forget to change the path to where your pyfa.py and pyfa.spec lives
#  pathex=['C:\\Users\\Ebag333\\Documents\\GitHub\\Ebag333\\Pyfa'],

import os

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
             ]

import_these = []

# Walk eos.effects and add all effects so we can import them properly
for root, folders, files in os.walk("eos/effects"):
    for file_ in files:
        if file_.endswith(".py") and not file_.startswith("_"):
            mod_name = "{}.{}".format(
                root.replace("/", "."),
                file_.split(".py")[0],
            )
            import_these.append(mod_name)

a = Analysis(
             ['pyfa.py'],
             pathex=['C:\\projects\\pyfa\\'],
             binaries=[],
             datas=added_files,
             hiddenimports=import_these,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             )

pyz = PYZ(
          a.pure,
          a.zipped_data,
          cipher=block_cipher,
          )

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          debug=False,
          console=False,
          strip=False,
          upx=True,
          name='pyfa',
          icon='dist_assets/win/pyfa.ico',
          onefile=False,
          )

coll = COLLECT(
               exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               onefile=False,
               name='pyfa',
               icon='dist_assets/win/pyfa.ico',
               )
