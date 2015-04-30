

import sys
from itertools import chain

from cx_Freeze import setup, Executable


packages = ['eos', 'gui', 'service', 'utils']
include_files = ['icons', 'staticdata']
includes = []
excludes = []


def dict_union(a, b):
    """Values from b have priority"""
    return dict(i for i in chain(a.items(), b.items()))
    

build_options_generic = {
    'packages': packages,
    'include_files': include_files,
    'includes': includes,
    'excludes': excludes,
    'build_exe': 'dist',
    'compressed': True,
    'optimize': 2
}

build_options_winexe = dict_union(build_options_generic, {
    'build_exe': 'dist_winexe',
})

build_options_winmsi = dict_union(build_options_generic, {
    'build_exe': 'dist_winmsi',
})

executable_options = {
    'script': 'pyfa.py',
    'base': 'Win32GUI' if sys.platform=='win32' else None,
    'icon': 'pyfa.ico',
}

setup(
    name='pyfa',
    version='0.0.0',
    description='TODO',
    options = {
        'build_exe': build_options_winexe,
        'bdist_msi': build_options_winmsi
    },
    executables=[Executable(**executable_options)]
)
