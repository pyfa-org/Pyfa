"""
This module contains a list of item conversions that need to be done for pyfa.

Each file in this module must contain a dictionary named CONVERSIONS in the
format of convertFrom: convertTo, with both key and value being a string of the
item's name. The name of the file is usually arbitrary unless it's used in logic
elsewhere (in which case can be accessed with packs[name])
"""

import pkgutil

# init parent dict
all = {}

# init container to store the separate conversion packs in case we need them
packs = {}

prefix = __name__ + "."

# load modules to work based with and without pyinstaller
# from: https://github.com/webcomics/dosage/blob/master/dosagelib/loader.py
# see: https://github.com/pyinstaller/pyinstaller/issues/1905

# load modules using iter_modules()
# (should find all filters in normal build, but not pyinstaller)
module_names = [m[1] for m in pkgutil.iter_modules(__path__, prefix)]

# special handling for PyInstaller
importers = map(pkgutil.get_importer, __path__)
toc = set()
for i in importers:
    if hasattr(i, 'toc'):
        toc |= i.toc

for elm in toc:
    if elm.startswith(prefix):
        module_names.append(elm)

for modname in module_names:
    conversionPack = __import__(modname, fromlist="dummy")
    all.update(conversionPack.CONVERSIONS)
    modname_tail = modname.rsplit('.', 1)[-1]
    packs[modname_tail] = conversionPack.CONVERSIONS
