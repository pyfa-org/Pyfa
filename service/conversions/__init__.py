"""
This module contains a list of item conversions that need to be done for pyfa.

Each file in this module must contain a dictionary named CONVERSIONS in the
format of convertFrom: convertTo, with both key and value being a string of the
item's name. The name of the file is usually arbitrary unless it's used in logic
elsewhere (in which case can be accessed with CONVERSIONS_SEPARATE[name])
"""

import os

# init parent dict
all = {}

# init container to store the separate conversion packs in case we need them
packs = {}

for filename in os.listdir(os.path.dirname(__file__)):
    basename, extension = filename.rsplit('.', 1)

    if extension == "py" and basename not in ("__init__",):
        conversionPack = __import__("%s.%s"%(__name__, basename), fromlist=True)
        all.update(conversionPack.CONVERSIONS)
        packs[basename] = conversionPack.CONVERSIONS
