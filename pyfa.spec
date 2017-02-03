# -*- mode: python -*-

# Command line to build:
# c:\Python27\Scripts\pyinstaller.exe --noconsole --clean --noconfirm --onefile pyfa.spec

block_cipher = None

added_files = [
             ( 'imgs/gui/*.png', 'imgs/gui' ),
             ( 'imgs/gui/*.gif', 'imgs/gui' ),
             ( 'imgs/icons/*.png', 'imgs/icons' ),
             ( 'imgs/renders/*.png', 'imgs/renders' ),
             ( 'dist_assets/mac/*.icns', 'dist_assets/mac' ),
             ( 'dist_assets/win/*.ico', 'dist_assets/win' ),
             ( 'eve.db', '.' ),
             ( 'README.md', '.' ),
             ( 'LICENSE', '.' ),
             ]

a = Analysis(
             ['pyfa.py'],
             pathex=['C:\\Users\\Ebag333\\Documents\\GitHub\\Ebag333\\Pyfa'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
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
          name='pyfa',
          debug=True,
          strip=False,
          upx=True,
          console=True,
          )
coll = COLLECT(
               exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               debug=False,
               console=False,
               strip=False,
               upx=True,
               name='pyfa',
               icon='\\dist_assets\\win\\pyfa.ico',
               )
