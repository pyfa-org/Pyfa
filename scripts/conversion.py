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
conversion_phrase = " converted to "

text = """
    Micro Electrochemical Capacitor Booster I renamed to 'Seed' Micro Capacitor Booster I
    Small Electrochemical Capacitor Booster I renamed to Small F-RX Compact Capacitor Booster
    Medium Electrochemical Capacitor Booster I renamed to Medium F-RX Compact Capacitor Booster
    Heavy Electrochemical Capacitor Booster I renamed to Heavy F-RX Compact Capacitor Booster
    Micro Brief Capacitor Overcharge I converted to 'Seed' Micro Capacitor Booster I
    Micro Tapered Capacitor Infusion I converted to 'Seed' Micro Capacitor Booster I
    Micro F-RX Prototype Capacitor Boost converted to 'Seed' Micro Capacitor Booster I
    Micro Capacitor Booster I converted to 'Seed' Micro Capacitor Booster I
    Micro Capacitor Booster II converted to 'Seed' Micro Capacitor Booster I
    Ammatar Navy Micro Capacitor Booster converted to 'Seed' Micro Capacitor Booster I
    Dark Blood Micro Capacitor Booster converted to 'Seed' Micro Capacitor Booster I
    True Sansha Micro Capacitor Booster converted to 'Seed' Micro Capacitor Booster I
    Imperial Navy Micro Capacitor Booster converted to 'Seed' Micro Capacitor Booster I
    Small Brief Capacitor Overcharge I converted to Small F-RX Compact Capacitor Booster
    Small Tapered Capacitor Infusion I converted to Small F-RX Compact Capacitor Booster
    Small F-RX Prototype Capacitor Boost converted to Small F-RX Compact Capacitor Booster
    Medium Brief Capacitor Overcharge I converted to Medium F-RX Compact Capacitor Booster
    Medium Tapered Capacitor Infusion I converted to Medium F-RX Compact Capacitor Booster
    Medium F-RX Prototype Capacitor Boost converted to Medium F-RX Compact Capacitor Booster
    Heavy Brief Capacitor Overcharge I converted to Heavy F-RX Compact Capacitor Booster
    Heavy Tapered Capacitor Infusion I converted to Heavy F-RX Compact Capacitor Booster
    Heavy F-RX Prototype Capacitor Boost converted to Heavy F-RX Compact Capacitor Booster
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
