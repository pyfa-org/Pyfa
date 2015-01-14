# Developed for module tiericide, this script will quickly print out a market
# conversion map based on database conversions / renamed modules between two
# eve databases. Correct database conversions must be implemented in upgrade
# script in eos.db.migrations

import argparse
import os.path
import sqlite3
import sys

# Add eos root path to sys.path so we can import ourselves
path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))
sys.path.append(os.path.realpath(os.path.join(path, "..")))

# change to correct conversion
from eos.db.migrations.upgrade4 import CONVERSIONS

def main(old, new):
    # Open both databases and get their cursors
    old_db = sqlite3.connect(os.path.expanduser(old))
    old_cursor = old_db.cursor()
    new_db = sqlite3.connect(os.path.expanduser(new))
    new_cursor = new_db.cursor()

    print "# Renamed items"

    # find renames (stolen from itemDiff)
    old_namedata = {}
    new_namedata = {}

    for cursor, dictionary in ((old_cursor, old_namedata), (new_cursor, new_namedata)):
        cursor.execute("SELECT typeID, typeName FROM invtypes")
        for row in cursor:
            id = row[0]
            name = row[1]
            dictionary[id] = name

    for id in set(old_namedata.keys()).intersection(new_namedata.keys()):
        oldname = old_namedata[id]
        newname = new_namedata[id]
        if oldname != newname:
            print '"%s": "%s",' % (oldname.encode('utf-8'), newname.encode('utf-8'))

    # Convert modules
    print "\n# Converted items"
    for replacement_item, list in CONVERSIONS.iteritems():
        new_cursor.execute('SELECT "typeName" FROM "invtypes" WHERE "typeID" = ?', (replacement_item,))
        for row in new_cursor:
            new_item = row[0]
            break

        for retired_item in list:
            old_cursor.execute('SELECT "typeName" FROM "invtypes" WHERE "typeID" = ?', (retired_item,))
            for row in old_cursor:
                old_item = row[0]
                break
            print '"%s": "%s",' % (old_item, new_item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", type=str)
    parser.add_argument("-n", "--new", type=str)
    args = parser.parse_args()

    main(args.old, args.new)
