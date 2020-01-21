"""
This module contains a list of item conversions that need to be done for pyfa.

Each file in this module must contain a dictionary named CONVERSIONS in the
format of convertFrom: convertTo, with both key and value being a string of the
item's name. The name of the file is usually arbitrary unless it's used in logic
elsewhere (in which case can be accessed with packs[name])
"""


from eos.utils.pyinst_support import iterNamespace


# init parent dict
all = {}
# init container to store the separate conversion packs in case we need them
packs = {}

for modName in iterNamespace(__name__, __path__):
    conversionPack = __import__(modName, fromlist="dummy")
    all.update(conversionPack.CONVERSIONS)
    modname_tail = modName.rsplit('.', 1)[-1]
    packs[modname_tail] = conversionPack.CONVERSIONS
