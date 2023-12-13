# -*- mode: python -*-

import os
from itertools import chain
import subprocess
import requests.certs
import platform

os_name = platform.system()
block_cipher = None

added_files = [
     ('imgs/gui/*.png', 'imgs/gui'),
     ('imgs/gui/*.gif', 'imgs/gui'),
     ('imgs/icons/*.png', 'imgs/icons'),
     ('imgs/renders/*.png', 'imgs/renders'),
     ('service/jargon/*.yaml', 'service/jargon'),
     ('locale', 'locale'),
     (requests.certs.where(), '.'),  # is this needed anymore?
     ('eve.db', '.'),
     ('README.md', '.'),
     ('LICENSE', '.'),
     ('version.yml', '.'),
]

icon = None
pathex = []
upx = True
debug = False

if os_name == 'Windows':
    added_files.extend([
        ('dist_assets/win/pyfa.ico', '.'),
        ('dist_assets/win/pyfa.exe.manifest', '.'),
    ])

    icon = 'dist_assets/win/pyfa.ico'

    pathex.extend([
         # Need this, see https://github.com/pyinstaller/pyinstaller/issues/1566
         # To get this, download and install windows 10 SDK
         # If not building on Windows 10, this might be optional
         r'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x86'
    ])

if os_name == 'Darwin':
    added_files.extend([
        ('dist_assets/win/pyfa.ico', '.'),  # osx only
    ])
    pathex.extend([r'build/py'])
    icon = 'dist_assets/mac/pyfa.icns'

import_these = [
    'numpy.core._dtype_ctypes',  # https://github.com/pyinstaller/pyinstaller/issues/3982
    'sqlalchemy.ext.baked',  # windows build doesn't launch without if when using sqlalchemy 1.3.x
    'pkg_resources.py2_warn'  # issue 2156
]

# Walk directories that do dynamic importing
paths = ('eos/db/migrations', 'service/conversions')
for root, folders, files in chain.from_iterable(os.walk(path) for path in paths):
    for file_ in files:
        if file_.endswith(".py") and not file_.startswith("_"):
            mod_name = "{}.{}".format(
                root.replace("/", "."),
                file_.split(".py")[0],
            )
            import_these.append(mod_name)

a = Analysis(['pyfa.py'],
             pathex= pathex,
             binaries=[],
             datas=added_files,
             hiddenimports=import_these,
             hookspath=['dist_assets/pyinstaller_hooks'],
             runtime_hooks=[],
             excludes=['Tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)


exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='pyfa',
    debug=debug,
    strip=False,
    upx=upx,
    icon= icon,
    # version='win-version-info.txt',
    console=False,
    contents_directory='app',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=upx,
    name='pyfa',
)

if platform.system() == 'Darwin':
    info_plist = {
        'NSHighResolutionCapable': 'True',
        'NSPrincipalClass': 'NSApplication',
        'CFBundleName': 'pyfa',
        'CFBundleDisplayName': 'pyfa',
        'CFBundleIdentifier': 'org.pyfaorg.pyfa',
        'CFBundleVersion': '1.2.3',
        'CFBundleShortVersionString': '1.2.3',
    }
    app = BUNDLE(exe,
        name='pyfa.app',
        icon=icon,
        bundle_identifier=None,
        info_plist=info_plist
    )
