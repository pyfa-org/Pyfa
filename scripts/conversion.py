# Developed for module tiericide, this script will quickly print out a market
# conversion map based on patch notes, as well as database conversion mapping.

import argparse
import os.path
import sqlite3
import sys

# Add eos root path to sys.path so we can import ourselves
path = os.path.dirname(__file__)
sys.path.append(os.path.realpath(os.path.join(path, "..")))

# change to correct conversion

rename_phrase = " renamed to "
conversion_phrase = " -> "

text = """
Veldspar Mining Crystal I -> Simple Asteroid Mining Crystal Type A I
Scordite Mining Crystal I -> Simple Asteroid Mining Crystal Type A I
Pyroxeres Mining Crystal I -> Simple Asteroid Mining Crystal Type A I
Plagioclase Mining Crystal I -> Simple Asteroid Mining Crystal Type A I
Veldspar Mining Crystal II -> Simple Asteroid Mining Crystal Type A II
Scordite Mining Crystal II -> Simple Asteroid Mining Crystal Type A II
Pyroxeres Mining Crystal II -> Simple Asteroid Mining Crystal Type A II
Plagioclase Mining Crystal II -> Simple Asteroid Mining Crystal Type A II
Omber Mining Crystal I -> Coherent Asteroid Mining Crystal Type A I
Kernite Mining Crystal I -> Coherent Asteroid Mining Crystal Type A I
Jaspet Mining Crystal I -> Coherent Asteroid Mining Crystal Type A I
Hemorphite Mining Crystal I -> Coherent Asteroid Mining Crystal Type A I
Hedbergite Mining Crystal I -> Coherent Asteroid Mining Crystal Type A I
Omber Mining Crystal II -> Coherent Asteroid Mining Crystal Type A II
Jaspet Mining Crystal II -> Coherent Asteroid Mining Crystal Type A II
Kernite Mining Crystal II -> Coherent Asteroid Mining Crystal Type A II
Hedbergite Mining Crystal II -> Coherent Asteroid Mining Crystal Type A II
Hemorphite Mining Crystal II -> Coherent Asteroid Mining Crystal Type A II
Gneiss Mining Crystal I -> Variegated Asteroid Mining Crystal Type A I
Dark Ochre Mining Crystal I -> Variegated Asteroid Mining Crystal Type A I
Crokite Mining Crystal I -> Variegated Asteroid Mining Crystal Type A I
Gneiss Mining Crystal II -> Variegated Asteroid Mining Crystal Type A II
Dark Ochre Mining Crystal II -> Variegated Asteroid Mining Crystal Type A II
Crokite Mining Crystal II -> Variegated Asteroid Mining Crystal Type A II
Bistot Mining Crystal I -> Complex Asteroid Mining Crystal Type A I
Arkonor Mining Crystal I -> Complex Asteroid Mining Crystal Type A I
Spodumain Mining Crystal I -> Complex Asteroid Mining Crystal Type A I
Bistot Mining Crystal II -> Complex Asteroid Mining Crystal Type A II
Arkonor Mining Crystal II -> Complex Asteroid Mining Crystal Type A II
Spodumain Mining Crystal II -> Complex Asteroid Mining Crystal Type A II
    """

def main(old, new):
    # Open both databases and get their cursors
    old_db = sqlite3.connect(os.path.expanduser(old))
    old_cursor = old_db.cursor()
    new_db = sqlite3.connect(os.path.expanduser(new))
    new_cursor = new_db.cursor()

    renames = {}
    conversions = {}

    for x in text.splitlines():
        x = x.strip()
        if not x:
            continue
        if conversion_phrase in x:
            c = x.split(conversion_phrase)
            container = conversions
        elif rename_phrase in x:
            c = x.split(rename_phrase)
            container = renames
        else:
            print("Unknown format: {}".format(x))
            sys.exit()

        old_name, new_name = c[0], c[1]
        old_item, new_item = None, None

        if "Blueprint" in old_name or "Blueprint" in new_name:
            print("Blueprint: Skipping this line: %s"%x)
            continue

        # gather item info
        new_cursor.execute('SELECT "typeID" FROM "invtypes" WHERE "typeName" = ?', (new_name,))
        for row in new_cursor:
            new_item = row[0]
            break

        old_cursor.execute('SELECT "typeID" FROM "invtypes" WHERE "typeName" = ?', (old_name,))
        for row in old_cursor:
            old_item = row[0]
            break

        if not old_item:
            print("Error finding old item in {} -> {}".format(old_name, new_name))
        if not new_item:
            print("Error finding new item in {} -> {}".format(old_name, new_name))

        if not container.get((new_item,new_name), None):
            container[(new_item,new_name)] = []


        container[(new_item,new_name)].append((old_item, old_name))

    print("    # Renamed items")

    for new, old in renames.items():
        if len(old) != 1:
            print("Incorrect length, key: {}, value: {}".format(new, old))
            sys.exit()
        old = old[0]

        print("    \"{}\": \"{}\",".format(old[1], new[1]))

    # Convert modules
    print("\n    # Converted items")

    for new, olds in conversions.items():
        for old in olds:
            print("    \"{}\": \"{}\",".format(old[1], new[1]))

    print()
    print()

    for new, old in conversions.items():
        print("    {}: (  # {}".format(new[0], new[1]))
        for item in old:
            print("        {},  # {}".format(item[0], item[1]))
        print("    ),")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", type=str)
    parser.add_argument("-n", "--new", type=str)
    args = parser.parse_args()

    main(args.old, args.new)
