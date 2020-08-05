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
    Basic Energized EM Membrane renamed to 'Basic' EM Energized Membrane
    Energized EM Membrane I renamed to EM Energized Membrane I
    Energized EM Membrane II renamed to EM Energized Membrane II
    Basic Energized Explosive Membrane renamed to 'Basic' Explosive Energized Membrane
    Energized Explosive Membrane I renamed to Explosive Energized Membrane I
    Energized Explosive Membrane II renamed to Explosive Energized Membrane II
    Basic Energized Armor Layering Membrane renamed to 'Basic' Layered Energized Membrane
    Energized Armor Layering Membrane I renamed to Layered Energized Membrane I
    Energized Armor Layering Membrane II renamed to Layered Energized Membrane II
    Basic Energized Kinetic Membrane renamed to 'Basic' Kinetic Energized Membrane
    Energized Kinetic Membrane I renamed to Kinetic Energized Membrane I
    Energized Kinetic Membrane II renamed to Kinetic Energized Membrane II
    Basic Energized Thermal Membrane renamed to 'Basic' Thermal Energized Membrane
    Energized Thermal Membrane I renamed to Thermal Energized Membrane I
    Energized Thermal Membrane II renamed to Thermal Energized Membrane II
    Basic Energized Adaptive Nano Membrane renamed to 'Basic' Multispectrum Energized Membrane
    Energized Adaptive Nano Membrane I renamed to Multispectrum Energized Membrane I
    Energized Adaptive Nano Membrane II renamed to Multispectrum Energized Membrane II
    Dark Blood Energized Adaptive Nano Membrane renamed to Dark Blood Multispectrum Energized Membrane
    True Sansha Energized Adaptive Nano Membrane renamed to True Sansha Multispectrum Energized Membrane
    Shadow Serpentis Energized Adaptive Nano Membrane renamed to Shadow Serpentis Multispectrum Energized Membrane
    Dark Blood Energized Kinetic Membrane renamed to Dark Blood Kinetic Energized Membrane
    True Sansha Energized Kinetic Membrane renamed to True Sansha Kinetic Energized Membrane
    Shadow Serpentis Energized Kinetic Membrane renamed to Shadow Serpentis Kinetic Energized Membrane
    Dark Blood Energized Explosive Membrane renamed to Dark Blood Explosive Energized Membrane
    True Sansha Energized Explosive Membrane renamed to True Sansha Explosive Energized Membrane
    Shadow Serpentis Energized Explosive Membrane renamed to Shadow Serpentis Explosive Energized Membrane
    Dark Blood Energized EM Membrane renamed to Dark Blood EM Energized Membrane
    True Sansha Energized EM Membrane renamed to True Sansha EM Energized Membrane
    Shadow Serpentis Energized EM Membrane renamed to Shadow Serpentis EM Energized Membrane
    Dark Blood Energized Thermal Membrane renamed to Dark Blood Thermal Energized Membrane
    True Sansha Energized Thermal Membrane renamed to True Sansha Thermal Energized Membrane
    Shadow Serpentis Energized Thermal Membrane renamed to Shadow Serpentis Thermal Energized Membrane
    Brokara's Modified Energized Adaptive Nano Membrane renamed to Brokara's Modified Multispectrum Energized Membrane
    Tairei's Modified Energized Adaptive Nano Membrane renamed to Tairei's Modified Multispectrum Energized Membrane
    Selynne's Modified Energized Adaptive Nano Membrane renamed to Selynne's Modified Multispectrum Energized Membrane
    Raysere's Modified Energized Adaptive Nano Membrane renamed to Raysere's Modified Multispectrum Energized Membrane
    Vizan's Modified Energized Adaptive Nano Membrane renamed to Vizan's Modified Multispectrum Energized Membrane
    Ahremen's Modified Energized Adaptive Nano Membrane renamed to Ahremen's Modified Multispectrum Energized Membrane
    Chelm's Modified Energized Adaptive Nano Membrane renamed to Chelm's Modified Multispectrum Energized Membrane
    Draclira's Modified Energized Adaptive Nano Membrane renamed to Draclira's Modified Multispectrum Energized Membrane
    Brokara's Modified Energized Thermal Membrane renamed to Brokara's Modified Thermal Energized Membrane
    Tairei's Modified Energized Thermal Membrane renamed to Tairei's Modified Thermal Energized Membrane
    Selynne's Modified Energized Thermal Membrane renamed to Selynne's Modified Thermal Energized Membrane
    Raysere's Modified Energized Thermal Membrane renamed to Raysere's Modified Thermal Energized Membrane
    Vizan's Modified Energized Thermal Membrane renamed to Vizan's Modified Thermal Energized Membrane
    Ahremen's Modified Energized Thermal Membrane renamed to Ahremen's Modified Thermal Energized Membrane
    Chelm's Modified Energized Thermal Membrane renamed to Chelm's Modified Thermal Energized Membrane
    Draclira's Modified Energized Thermal Membrane renamed to Draclira's Modified Thermal Energized Membrane
    Brokara's Modified Energized EM Membrane renamed to Brokara's Modified EM Energized Membrane
    Tairei's Modified Energized EM Membrane renamed to Tairei's Modified EM Energized Membrane
    Selynne's Modified Energized EM Membrane renamed to Selynne's Modified EM Energized Membrane
    Raysere's Modified Energized EM Membrane renamed to Raysere's Modified EM Energized Membrane
    Vizan's Modified Energized EM Membrane renamed to Vizan's Modified EM Energized Membrane
    Ahremen's Modified Energized EM Membrane renamed to Ahremen's Modified EM Energized Membrane
    Chelm's Modified Energized EM Membrane renamed to Chelm's Modified EM Energized Membrane
    Draclira's Modified Energized EM Membrane renamed to Draclira's Modified EM Energized Membrane
    Brokara's Modified Energized Explosive Membrane renamed to Brokara's Modified Explosive Energized Membrane
    Tairei's Modified Energized Explosive Membrane renamed to Tairei's Modified Explosive Energized Membrane
    Selynne's Modified Energized Explosive Membrane renamed to Selynne's Modified Explosive Energized Membrane
    Raysere's Modified Energized Explosive Membrane renamed to Raysere's Modified Explosive Energized Membrane
    Vizan's Modified Energized Explosive Membrane renamed to Vizan's Modified Explosive Energized Membrane
    Ahremen's Modified Energized Explosive Membrane renamed to Ahremen's Modified Explosive Energized Membrane
    Chelm's Modified Energized Explosive Membrane renamed to Chelm's Modified Explosive Energized Membrane
    Draclira's Modified Energized Explosive Membrane renamed to Draclira's Modified Explosive Energized Membrane
    Brokara's Modified Energized Kinetic Membrane renamed to Brokara's Modified Kinetic Energized Membrane
    Tairei's Modified Energized Kinetic Membrane renamed to Tairei's Modified Kinetic Energized Membrane
    Selynne's Modified Energized Kinetic Membrane renamed to Selynne's Modified Kinetic Energized Membrane
    Raysere's Modified Energized Kinetic Membrane renamed to Raysere's Modified Kinetic Energized Membrane
    Vizan's Modified Energized Kinetic Membrane renamed to Vizan's Modified Kinetic Energized Membrane
    Ahremen's Modified Energized Kinetic Membrane renamed to Ahremen's Modified Kinetic Energized Membrane
    Chelm's Modified Energized Kinetic Membrane renamed to Chelm's Modified Kinetic Energized Membrane
    Draclira's Modified Energized Kinetic Membrane renamed to Draclira's Modified Kinetic Energized Membrane
    Brynn's Modified Energized Adaptive Nano Membrane renamed to Brynn's Modified Multispectrum Energized Membrane
    Tuvan's Modified Energized Adaptive Nano Membrane renamed to Tuvan's Modified Multispectrum Energized Membrane
    Setele's Modified Energized Adaptive Nano Membrane renamed to Setele's Modified Multispectrum Energized Membrane
    Cormack's Modified Energized Adaptive Nano Membrane renamed to Cormack's Modified Multispectrum Energized Membrane
    Brynn's Modified Energized Thermal Membrane renamed to Brynn's Modified Thermal Energized Membrane
    Tuvan's Modified Energized Thermal Membrane renamed to Tuvan's Modified Thermal Energized Membrane
    Setele's Modified Energized Thermal Membrane renamed to Setele's Modified Thermal Energized Membrane
    Cormack's Modified Energized Thermal Membrane renamed to Cormack's Modified Thermal Energized Membrane
    Brynn's Modified Energized EM Membrane renamed to Brynn's Modified EM Energized Membrane
    Tuvan's Modified Energized EM Membrane renamed to Tuvan's Modified EM Energized Membrane
    Setele's Modified Energized EM Membrane renamed to Setele's Modified EM Energized Membrane
    Cormack's Modified Energized EM Membrane renamed to Cormack's Modified EM Energized Membrane
    Brynn's Modified Energized Explosive Membrane renamed to Brynn's Modified Explosive Energized Membrane
    Tuvan's Modified Energized Explosive Membrane renamed to Tuvan's Modified Explosive Energized Membrane
    Setele's Modified Energized Explosive Membrane renamed to Setele's Modified Explosive Energized Membrane
    Cormack's Modified Energized Explosive Membrane renamed to Cormack's Modified Explosive Energized Membrane
    Brynn's Modified Energized Kinetic Membrane renamed to Brynn's Modified Kinetic Energized Membrane
    Tuvan's Modified Energized Kinetic Membrane renamed to Tuvan's Modified Kinetic Energized Membrane
    Setele's Modified Energized Kinetic Membrane renamed to Setele's Modified Kinetic Energized Membrane
    Cormack's Modified Energized Kinetic Membrane renamed to Cormack's Modified Kinetic Energized Membrane
    Imperial Navy Energized Thermal Membrane renamed to Imperial Navy Thermal Energized Membrane
    Imperial Navy Energized EM Membrane renamed to Imperial Navy EM Energized Membrane
    Imperial Navy Energized Explosive Membrane renamed to Imperial Navy Explosive Energized Membrane
    Imperial Navy Energized Kinetic Membrane renamed to Imperial Navy Kinetic Energized Membrane
    Imperial Navy Energized Adaptive Nano Membrane renamed to Imperial Navy Multispectrum Energized Membrane
    Federation Navy Energized Thermal Membrane renamed to Federation Navy Thermal Energized Membrane
    Federation Navy Energized EM Membrane renamed to Federation Navy EM Energized Membrane
    Federation Navy Energized Explosive Membrane renamed to Federation Navy Explosive Energized Membrane
    Federation Navy Energized Kinetic Membrane renamed to Federation Navy Kinetic Energized Membrane
    Federation Navy Energized Adaptive Nano Membrane renamed to Federation Navy Multispectrum Energized Membrane
    Prototype Energized Adaptive Nano Membrane I renamed to Compact Multispectrum Energized Membrane
    Prototype Energized Kinetic Membrane I renamed to Compact Kinetic Energized Membrane
    Prototype Energized Explosive Membrane I renamed to Compact Explosive Energized Membrane
    Prototype Energized EM Membrane I renamed to Compact EM Energized Membrane
    Prototype Energized Armor Layering Membrane I renamed to Compact Layered Energized Membrane
    Prototype Energized Thermal Membrane I renamed to Compact Thermal Energized Membrane
    Ammatar Navy Energized Adaptive Nano Membrane renamed to Ammatar Navy Multispectrum Energized Membrane
    Ammatar Navy Energized Kinetic Membrane renamed to Ammatar Navy Kinetic Energized Membrane
    Ammatar Navy Energized Explosive Membrane renamed to Ammatar Navy Explosive Energized Membrane
    Ammatar Navy Energized EM Membrane renamed to Ammatar Navy EM Energized Membrane
    Ammatar Navy Energized Thermal Membrane renamed to Ammatar Navy Thermal Energized Membrane
    Corelum C-Type Energized Adaptive Nano Membrane renamed to Corelum C-Type Multispectrum Energized Membrane
    Corelum C-Type Energized Kinetic Membrane renamed to Corelum C-Type Kinetic Energized Membrane
    Corelum C-Type Energized Explosive Membrane renamed to Corelum C-Type Explosive Energized Membrane
    Corelum C-Type Energized EM Membrane renamed to Corelum C-Type EM Energized Membrane
    Corelum C-Type Energized Thermal Membrane renamed to Corelum C-Type Thermal Energized Membrane
    Corelum B-Type Energized Adaptive Nano Membrane renamed to Corelum B-Type Multispectrum Energized Membrane
    Corelum B-Type Energized Kinetic Membrane renamed to Corelum B-Type Kinetic Energized Membrane
    Corelum B-Type Energized Explosive Membrane renamed to Corelum B-Type Explosive Energized Membrane
    Corelum B-Type Energized EM Membrane renamed to Corelum B-Type EM Energized Membrane
    Corelum B-Type Energized Thermal Membrane renamed to Corelum B-Type Thermal Energized Membrane
    Corelum A-Type Energized Adaptive Nano Membrane renamed to Corelum A-Type Multispectrum Energized Membrane
    Corelum A-Type Energized Kinetic Membrane renamed to Corelum A-Type Kinetic Energized Membrane
    Corelum A-Type Energized Explosive Membrane renamed to Corelum A-Type Explosive Energized Membrane
    Corelum A-Type Energized EM Membrane renamed to Corelum A-Type EM Energized Membrane
    Corelum A-Type Energized Thermal Membrane renamed to Corelum A-Type Thermal Energized Membrane
    Corpum C-Type Energized Adaptive Nano Membrane renamed to Corpum C-Type Multispectrum Energized Membrane
    Centum C-Type Energized Adaptive Nano Membrane renamed to Centum C-Type Multispectrum Energized Membrane
    Corpum C-Type Energized Kinetic Membrane renamed to Corpum C-Type Kinetic Energized Membrane
    Centum C-Type Energized Kinetic Membrane renamed to Centum C-Type Kinetic Energized Membrane
    Corpum C-Type Energized Explosive Membrane renamed to Corpum C-Type Explosive Energized Membrane
    Centum C-Type Energized Explosive Membrane renamed to Centum C-Type Explosive Energized Membrane
    Corpum C-Type Energized EM Membrane renamed to Corpum C-Type EM Energized Membrane
    Centum C-Type Energized EM Membrane renamed to Centum C-Type EM Energized Membrane
    Corpum C-Type Energized Thermal Membrane renamed to Corpum C-Type Thermal Energized Membrane
    Centum C-Type Energized Thermal Membrane renamed to Centum C-Type Thermal Energized Membrane
    Corpum B-Type Energized Adaptive Nano Membrane renamed to Corpum B-Type Multispectrum Energized Membrane
    Centum B-Type Energized Adaptive Nano Membrane renamed to Centum B-Type Multispectrum Energized Membrane
    Corpum B-Type Energized Kinetic Membrane renamed to Corpum B-Type Kinetic Energized Membrane
    Centum B-Type Energized Kinetic Membrane renamed to Centum B-Type Kinetic Energized Membrane
    Corpum B-Type Energized Explosive Membrane renamed to Corpum B-Type Explosive Energized Membrane
    Centum B-Type Energized Explosive Membrane renamed to Centum B-Type Explosive Energized Membrane
    Corpum B-Type Energized Thermal Membrane renamed to Corpum B-Type Thermal Energized Membrane
    Centum B-Type Energized Thermal Membrane renamed to Centum B-Type Thermal Energized Membrane
    Corpum A-Type Energized Thermal Membrane renamed to Corpum A-Type Thermal Energized Membrane
    Centum A-Type Energized Thermal Membrane renamed to Centum A-Type Thermal Energized Membrane
    Corpum A-Type Energized EM Membrane renamed to Corpum A-Type EM Energized Membrane
    Centum A-Type Energized EM Membrane renamed to Centum A-Type EM Energized Membrane
    Corpum A-Type Energized Explosive Membrane renamed to Corpum A-Type Explosive Energized Membrane
    Centum A-Type Energized Explosive Membrane renamed to Centum A-Type Explosive Energized Membrane
    Corpum A-Type Energized Kinetic Membrane renamed to Corpum A-Type Kinetic Energized Membrane
    Centum A-Type Energized Kinetic Membrane renamed to Centum A-Type Kinetic Energized Membrane
    Corpum A-Type Energized Adaptive Nano Membrane renamed to Corpum A-Type Multispectrum Energized Membrane
    Centum A-Type Energized Adaptive Nano Membrane renamed to Centum A-Type Multispectrum Energized Membrane
    Corpum B-Type Energized EM Membrane renamed to Corpum B-Type EM Energized Membrane
    Centum B-Type Energized EM Membrane renamed to Centum B-Type EM Energized Membrane
    'Pilfer' Energized Adaptive Nano Membrane I renamed to 'Pilfer' Multispectrum Energized Membrane
    'Moonshine' Energized Thermal Membrane I renamed to 'Moonshine' Thermal Energized Membrane
    'Mafia' Energized Kinetic Membrane I renamed to 'Mafia' Kinetic Energized Membrane
    Khanid Navy Energized Adaptive Nano Membrane renamed to Khanid Navy Multispectrum Energized Membrane
    Khanid Navy Energized Kinetic Membrane renamed to Khanid Navy Kinetic Energized Membrane
    Khanid Navy Energized Explosive Membrane renamed to Khanid Navy Explosive Energized Membrane
    Khanid Navy Energized EM Membrane renamed to Khanid Navy EM Energized Membrane
    Khanid Navy Energized Thermal Membrane renamed to Khanid Navy Thermal Energized Membrane
    Large Compact Vorton projector renamed to Large Compact Vorton Projector
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
