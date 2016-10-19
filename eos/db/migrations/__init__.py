"""
The migration module includes migration logic to update database scheme and/or
data for the user database.

To create a migration, simply create a file upgrade<migration number>.py and
define an upgrade() function with the logic. Please note that there must be as
many upgrade files as there are database versions (version 5 would include
upgrade files 1-5)
"""

import pkgutil
import re

updates = {}
appVersion = 0

prefix = __name__ + "."
for importer, modname, ispkg in pkgutil.iter_modules(__path__, prefix):
    # loop through python files, extracting update number and function, and
    # adding it to a list
    modname_tail = modname.rsplit('.', 1)[-1]
    module = __import__(modname, fromlist=True)
    m = re.match("^upgrade(?P<index>\d+)$", modname_tail)
    if not m:
        continue
    index = int(m.group("index"))
    appVersion = max(appVersion, index)
    upgrade = getattr(module, "upgrade", False)
    if upgrade:
        updates[index] = upgrade
