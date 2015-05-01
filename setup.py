"""
Distribution builder for pyfa.

Windows executable: python setup.py build
Windows executable + installer: python setup.py bdist_msi
"""

import sys
from itertools import chain

from cx_Freeze import setup, Executable


app_name = 'pyfa'
app_version = '0.0.0'
app_description = 'TODO'


packages = ['eos', 'gui', 'service', 'utils']
include_files = ['icons', 'staticdata', 'gpl.txt']
includes = []
excludes = ['Tkinter', 'setup']


def dict_union(a, b):
    """Values from b have priority"""
    return dict(i for i in chain(a.items(), b.items()))
    

build_options_generic = {
    'packages': packages,
    'include_files': include_files,
    'includes': includes,
    'excludes': excludes,
    'compressed': True,
    'optimize': 2
}

build_options_winexe = dict_union(build_options_generic, {
})

build_options_winmsi = {
    'upgrade_code': '{E80885AC-31BA-4D9A-A04F-9E5915608A6C}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\{}'.format(app_name),
}

executable_options = {
    'script': 'pyfa.py',
    'base': 'Win32GUI' if sys.platform=='win32' else None,
    'icon': 'pyfa.ico',
    'shortcutDir': 'DesktopFolder',
    'shortcutName': app_name,
}

setup(
    name=app_name,
    version=app_version,
    description=app_description,
    options = {
        'build_exe': build_options_winexe,
        'bdist_msi': build_options_winmsi
    },
    executables=[Executable(**executable_options)]
)
