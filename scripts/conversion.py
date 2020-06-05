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
    Supplemental EM Ward Amplifier converted to 'Basic' EM Shield Amplifier
    Supplemental Explosive Deflection Amplifier converted to 'Basic' Explosive Shield Amplifier
    Supplemental Kinetic Deflection Amplifier converted to 'Basic' Kinetic Shield Amplifier
    Supplemental Thermal Dissipation Amplifier converted to 'Basic' Thermal Shield Amplifier
    Basic EM Ward Amplifier renamed to 'Basic' EM Shield Amplifier
    Basic Thermal Dissipation Amplifier renamed to 'Basic' Thermal Shield Amplifier
    Basic Kinetic Deflection Amplifier renamed to 'Basic' Kinetic Shield Amplifier
    Basic Explosive Deflection Amplifier renamed to 'Basic' Explosive Shield Amplifier
    EM Ward Amplifier I renamed to EM Shield Amplifier I
    Explosive Deflection Amplifier I renamed to Explosive Shield Amplifier I
    Explosive Deflection Amplifier II renamed to Explosive Shield Amplifier II
    Thermal Dissipation Amplifier I renamed to Thermal Shield Amplifier I
    Thermal Dissipation Amplifier II renamed to Thermal Shield Amplifier II
    Kinetic Deflection Amplifier I renamed to Kinetic Shield Amplifier I
    Kinetic Deflection Amplifier II renamed to Kinetic Shield Amplifier II
    EM Ward Amplifier II renamed to EM Shield Amplifier II
    Upgraded Explosive Deflection Amplifier I renamed to Compact Explosive Shield Amplifier
    Upgraded Thermal Dissipation Amplifier I renamed to Compact Thermal Shield Amplifier
    Upgraded EM Ward Amplifier I renamed to Compact EM Shield Amplifier
    Upgraded Kinetic Deflection Amplifier I renamed to Compact Kinetic Shield Amplifier
    Domination Explosive Deflection Amplifier renamed to Domination Explosive Shield Amplifier
    Dread Guristas Explosive Deflection Amplifier renamed to Dread Guristas Explosive Shield Amplifier
    Domination Thermal Dissipation Amplifier renamed to Domination Thermal Shield Amplifier
    Dread Guristas Thermal Dissipation Amplifier renamed to Dread Guristas Thermal Shield Amplifier
    Domination Kinetic Deflection Amplifier renamed to Domination Kinetic Shield Amplifier
    Dread Guristas Kinetic Deflection Amplifier renamed to Dread Guristas Kinetic Shield Amplifier
    Domination EM Ward Amplifier renamed to Domination EM Shield Amplifier
    Dread Guristas EM Ward Amplifier renamed to Dread Guristas EM Shield Amplifier
    Hakim's Modified Explosive Deflection Amplifier renamed to Hakim's Modified Explosive Shield Amplifier
    Tobias' Modified Explosive Deflection Amplifier renamed to Tobias' Modified Explosive Shield Amplifier
    Hakim's Modified Thermal Dissipation Amplifier renamed to Hakim's Modified Thermal Shield Amplifier
    Tobias' Modified Thermal Dissipation Amplifier renamed to Tobias' Modified Thermal Shield Amplifier
    Hakim's Modified Kinetic Deflection Amplifier renamed to Hakim's Modified Kinetic Shield Amplifier
    Tobias' Modified Kinetic Deflection Amplifier renamed to Tobias' Modified Kinetic Shield Amplifier
    Hakim's Modified EM Ward Amplifier renamed to Hakim's Modified EM Shield Amplifier
    Tobias' Modified EM Ward Amplifier renamed to Tobias' Modified EM Shield Amplifier
    Kaikka's Modified Explosive Deflection Amplifier renamed to Kaikka's Modified Explosive Shield Amplifier
    Thon's Modified Explosive Deflection Amplifier renamed to Thon's Modified Explosive Shield Amplifier
    Vepas' Modified Explosive Deflection Amplifier renamed to Vepas' Modified Explosive Shield Amplifier
    Estamel's Modified Explosive Deflection Amplifier renamed to Estamel's Modified Explosive Shield Amplifier
    Kaikka's Modified Thermal Dissipation Amplifier renamed to Kaikka's Modified Thermal Shield Amplifier
    Thon's Modified Thermal Dissipation Amplifier renamed to Thon's Modified Thermal Shield Amplifier
    Vepas' Modified Thermal Dissipation Amplifier renamed to Vepas' Modified Thermal Shield Amplifier
    Estamel's Modified Thermal Dissipation Amplifier renamed to Estamel's Modified Thermal Shield Amplifier
    Kaikka's Modified Kinetic Deflection Amplifier renamed to Kaikka's Modified Kinetic Shield Amplifier
    Thon's Modified Kinetic Deflection Amplifier renamed to Thon's Modified Kinetic Shield Amplifier
    Vepas' Modified Kinetic Deflection Amplifier renamed to Vepas' Modified Kinetic Shield Amplifier
    Estamel's Modified Kinetic Deflection Amplifier renamed to Estamel's Modified Kinetic Shield Amplifier
    Kaikka's Modified EM Ward Amplifier renamed to Kaikka's Modified EM Shield Amplifier
    Thon's Modified EM Ward Amplifier renamed to Thon's Modified EM Shield Amplifier
    Vepas' Modified EM Ward Amplifier renamed to Vepas' Modified EM Shield Amplifier
    Estamel's Modified EM Ward Amplifier renamed to Estamel's Modified EM Shield Amplifier
    Caldari Navy EM Ward Amplifier renamed to Caldari Navy EM Shield Amplifier
    Caldari Navy Kinetic Deflection Amplifier renamed to Caldari Navy Kinetic Shield Amplifier
    Caldari Navy Thermal Dissipation Amplifier renamed to Caldari Navy Thermal Shield Amplifier
    Caldari Navy Explosive Deflection Amplifier renamed to Caldari Navy Explosive Shield Amplifier
    Republic Fleet EM Ward Amplifier renamed to Republic Fleet EM Shield Amplifier
    Republic Fleet Kinetic Deflection Amplifier renamed to Republic Fleet Kinetic Shield Amplifier
    Republic Fleet Thermal Dissipation Amplifier renamed to Republic Fleet Thermal Shield Amplifier
    Republic Fleet Explosive Deflection Amplifier renamed to Republic Fleet Explosive Shield Amplifier
    Pithum C-Type Explosive Deflection Amplifier renamed to Pithum C-Type Explosive Shield Amplifier
    Pithum C-Type Thermal Dissipation Amplifier renamed to Pithum C-Type Thermal Shield Amplifier
    Pithum C-Type Kinetic Deflection Amplifier renamed to Pithum C-Type Kinetic Shield Amplifier
    Pithum C-Type EM Ward Amplifier renamed to Pithum C-Type EM Shield Amplifier
    Pithum B-Type Explosive Deflection Amplifier renamed to Pithum B-Type Explosive Shield Amplifier
    Pithum B-Type Thermal Dissipation Amplifier renamed to Pithum B-Type Thermal Shield Amplifier
    Pithum B-Type Kinetic Deflection Amplifier renamed to Pithum B-Type Kinetic Shield Amplifier
    Pithum B-Type EM Ward Amplifier renamed to Pithum B-Type EM Shield Amplifier
    Pithum A-Type Explosive Deflection Amplifier renamed to Pithum A-Type Explosive Shield Amplifier
    Pithum A-Type Thermal Dissipation Amplifier renamed to Pithum A-Type Thermal Shield Amplifier
    Pithum A-Type Kinetic Deflection Amplifier renamed to Pithum A-Type Kinetic Shield Amplifier
    Pithum A-Type EM Ward Amplifier renamed to Pithum A-Type EM Shield Amplifier
    Gistum C-Type Explosive Deflection Amplifier renamed to Gistum C-Type Explosive Shield Amplifier
    Gistum B-Type Explosive Deflection Amplifier renamed to Gistum B-Type Explosive Shield Amplifier
    Gistum C-Type Thermal Dissipation Amplifier renamed to Gistum C-Type Thermal Shield Amplifier
    Gistum B-Type Thermal Dissipation Amplifier renamed to Gistum B-Type Thermal Shield Amplifier
    Gistum C-Type Kinetic Deflection Amplifier renamed to Gistum C-Type Kinetic Shield Amplifier
    Gistum B-Type Kinetic Deflection Amplifier renamed to Gistum B-Type Kinetic Shield Amplifier
    Gistum C-Type EM Ward Amplifier renamed to Gistum C-Type EM Shield Amplifier
    Gistum B-Type EM Ward Amplifier renamed to Gistum B-Type EM Shield Amplifier
    Gistum A-Type Explosive Deflection Amplifier renamed to Gistum A-Type Explosive Shield Amplifier
    Gistum A-Type Thermal Dissipation Amplifier renamed to Gistum A-Type Thermal Shield Amplifier
    Gistum A-Type Kinetic Deflection Amplifier renamed to Gistum A-Type Kinetic Shield Amplifier
    Gistum A-Type EM Ward Amplifier renamed to Gistum A-Type EM Shield Amplifier
    'Whiskey' Explosive Deflection Amplifier renamed to 'Whiskey' Explosive Shield Amplifier
    'High Noon' Thermal Dissipation Amplifier renamed to 'High Noon' Thermal Shield Amplifier
    'Cactus' Modified Kinetic Deflection Amplifier renamed to 'Cactus' Modified Kinetic Shield Amplifier
    'Prospector' EM Ward Amplifier renamed to 'Prospector' EM Shield Amplifier
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
