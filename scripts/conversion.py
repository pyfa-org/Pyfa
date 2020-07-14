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
    Limited Layered Plating I converted to Upgraded Layered Coating I
    'Scarab' Layered Plating I converted to Upgraded Layered Coating I
    'Grail' Layered Plating I converted to Upgraded Layered Coating I
    Limited Adaptive Nano Plating I converted to Upgraded Multispectrum Coating I
    'Collateral' Adaptive Nano Plating I converted to Upgraded Multispectrum Coating I
    'Refuge' Adaptive Nano Plating I converted to Upgraded Multispectrum Coating I
    Limited EM Plating I converted to Upgraded EM Coating I
    'Contour' EM Plating I converted to Upgraded EM Coating I
    'Spiegel' EM Plating I converted to Upgraded EM Coating I
    Limited Explosive Plating I converted to Upgraded Explosive Coating I
    Experimental Explosive Plating I converted to Upgraded Explosive Coating I
    'Aegis' Explosive Plating I converted to Upgraded Explosive Coating I
    Limited Kinetic Plating I converted to Upgraded Kinetic Coating I
    Experimental Kinetic Plating I converted to Upgraded Kinetic Coating I
    'Element' Kinetic Plating I converted to Upgraded Kinetic Coating I
    Limited Thermal Plating I converted to Upgraded Thermal Coating I
    Experimental Thermal Plating I converted to Upgraded Thermal Coating I
    Prototype Thermal Plating I converted to Upgraded Thermal Coating I
    Basic EM Plating renamed to 'Basic' EM Coating
    EM Plating I renamed to EM Coating I
    EM Plating II renamed to EM Coating II
    Basic Explosive Plating renamed to 'Basic' Explosive Coating
    Explosive Plating I renamed to Explosive Coating I
    Explosive Plating II renamed to Explosive Coating II
    Basic Layered Plating renamed to 'Basic' Layered Coating
    Layered Plating I renamed to Layered Coating I
    Layered Plating II renamed to Layered Coating II
    Basic Kinetic Plating renamed to 'Basic' Kinetic Coating
    Kinetic Plating I renamed to Kinetic Coating I
    Kinetic Plating II renamed to Kinetic Coating II
    Basic Thermal Plating renamed to 'Basic' Thermal Coating
    Thermal Plating I renamed to Thermal Coating I
    Thermal Plating II renamed to Thermal Coating II
    Basic Adaptive Nano Plating renamed to 'Basic' Multispectrum Coating
    Adaptive Nano Plating I renamed to Multispectrum Coating I
    Adaptive Nano Plating II renamed to Multispectrum Coating II
    Domination Adaptive Nano Plating renamed to Domination Multispectrum Coating
    True Sansha Adaptive Nano Plating renamed to True Sansha Multispectrum Coating
    Dark Blood Adaptive Nano Plating renamed to Dark Blood Multispectrum Coating
    Domination Kinetic Plating renamed to Domination Kinetic Coating
    True Sansha Kinetic Plating renamed to True Sansha Kinetic Coating
    Dark Blood Kinetic Plating renamed to Dark Blood Kinetic Coating
    Domination Explosive Plating renamed to Domination Explosive Coating
    True Sansha Explosive Plating renamed to True Sansha Explosive Coating
    Dark Blood Explosive Plating renamed to Dark Blood Explosive Coating
    Domination EM Plating renamed to Domination EM Coating
    True Sansha EM Plating renamed to True Sansha EM Coating
    Dark Blood EM Plating renamed to Dark Blood EM Coating
    Domination Thermal Plating renamed to Domination Thermal Coating
    True Sansha Thermal Plating renamed to True Sansha Thermal Coating
    Dark Blood Thermal Plating renamed to Dark Blood Thermal Coating
    Shadow Serpentis Adaptive Nano Plating renamed to Shadow Serpentis Multispectrum Coating
    Shadow Serpentis Kinetic Plating renamed to Shadow Serpentis Kinetic Coating
    Shadow Serpentis Explosive Plating renamed to Shadow Serpentis Explosive Coating
    Shadow Serpentis EM Plating renamed to Shadow Serpentis EM Coating
    Shadow Serpentis Thermal Plating renamed to Shadow Serpentis Thermal Coating
    Mizuro's Modified Adaptive Nano Plating renamed to Mizuro's Modified Multispectrum Coating
    Gotan's Modified Adaptive Nano Plating renamed to Gotan's Modified Multispectrum Coating
    Mizuro's Modified Kinetic Plating renamed to Mizuro's Modified Kinetic Coating
    Gotan's Modified Kinetic Plating renamed to Gotan's Modified Kinetic Coating
    Mizuro's Modified Explosive Plating renamed to Mizuro's Modified Explosive Coating
    Gotan's Modified Explosive Plating renamed to Gotan's Modified Explosive Coating
    Mizuro's Modified EM Plating renamed to Mizuro's Modified EM Coating
    Gotan's Modified EM Plating renamed to Gotan's Modified EM Coating
    Mizuro's Modified Thermal Plating renamed to Mizuro's Modified Thermal Coating
    Gotan's Modified Thermal Plating renamed to Gotan's Modified Thermal Coating
    Brokara's Modified Adaptive Nano Plating renamed to Brokara's Modified Multispectrum Coating
    Tairei's Modified Adaptive Nano Plating renamed to Tairei's Modified Multispectrum Coating
    Selynne's Modified Adaptive Nano Plating renamed to Selynne's Modified Multispectrum Coating
    Raysere's Modified Adaptive Nano Plating renamed to Raysere's Modified Multispectrum Coating
    Vizan's Modified Adaptive Nano Plating renamed to Vizan's Modified Multispectrum Coating
    Ahremen's Modified Adaptive Nano Plating renamed to Ahremen's Modified Multispectrum Coating
    Chelm's Modified Adaptive Nano Plating renamed to Chelm's Modified Multispectrum Coating
    Draclira's Modified Adaptive Nano Plating renamed to Draclira's Modified Multispectrum Coating
    Brokara's Modified Kinetic Plating renamed to Brokara's Modified Kinetic Coating
    Tairei's Modified Kinetic Plating renamed to Tairei's Modified Kinetic Coating
    Selynne's Modified Kinetic Plating renamed to Selynne's Modified Kinetic Coating
    Raysere's Modified Kinetic Plating renamed to Raysere's Modified Kinetic Coating
    Vizan's Modified Kinetic Plating renamed to Vizan's Modified Kinetic Coating
    Ahremen's Modified Kinetic Plating renamed to Ahremen's Modified Kinetic Coating
    Chelm's Modified Kinetic Plating renamed to Chelm's Modified Kinetic Coating
    Draclira's Modified Kinetic Plating renamed to Draclira's Modified Kinetic Coating
    Brokara's Modified Explosive Plating renamed to Brokara's Modified Explosive Coating
    Tairei's Modified Explosive Plating renamed to Tairei's Modified Explosive Coating
    Selynne's Modified Explosive Plating renamed to Selynne's Modified Explosive Coating
    Raysere's Modified Explosive Plating renamed to Raysere's Modified Explosive Coating
    Vizan's Modified Explosive Plating renamed to Vizan's Modified Explosive Coating
    Ahremen's Modified Explosive Plating renamed to Ahremen's Modified Explosive Coating
    Chelm's Modified Explosive Plating renamed to Chelm's Modified Explosive Coating
    Draclira's Modified Explosive Plating renamed to Draclira's Modified Explosive Coating
    Brokara's Modified EM Plating renamed to Brokara's Modified EM Coating
    Tairei's Modified EM Plating renamed to Tairei's Modified EM Coating
    Selynne's Modified EM Plating renamed to Selynne's Modified EM Coating
    Raysere's Modified EM Plating renamed to Raysere's Modified EM Coating
    Vizan's Modified EM Plating renamed to Vizan's Modified EM Coating
    Ahremen's Modified EM Plating renamed to Ahremen's Modified EM Coating
    Chelm's Modified EM Plating renamed to Chelm's Modified EM Coating
    Draclira's Modified EM Plating renamed to Draclira's Modified EM Coating
    Brokara's Modified Thermal Plating renamed to Brokara's Modified Thermal Coating
    Tairei's Modified Thermal Plating renamed to Tairei's Modified Thermal Coating
    Selynne's Modified Thermal Plating renamed to Selynne's Modified Thermal Coating
    Raysere's Modified Thermal Plating renamed to Raysere's Modified Thermal Coating
    Vizan's Modified Thermal Plating renamed to Vizan's Modified Thermal Coating
    Ahremen's Modified Thermal Plating renamed to Ahremen's Modified Thermal Coating
    Chelm's Modified Thermal Plating renamed to Chelm's Modified Thermal Coating
    Draclira's Modified Thermal Plating renamed to Draclira's Modified Thermal Coating
    Brynn's Modified Adaptive Nano Plating renamed to Brynn's Modified Multispectrum Coating
    Tuvan's Modified Adaptive Nano Plating renamed to Tuvan's Modified Multispectrum Coating
    Setele's Modified Adaptive Nano Plating renamed to Setele's Modified Multispectrum Coating
    Cormack's Modified Adaptive Nano Plating renamed to Cormack's Modified Multispectrum Coating
    Brynn's Modified Thermal Plating renamed to Brynn's Modified Thermal Coating
    Tuvan's Modified Thermal Plating renamed to Tuvan's Modified Thermal Coating
    Setele's Modified Thermal Plating renamed to Setele's Modified Thermal Coating
    Cormack's Modified Thermal Plating renamed to Cormack's Modified Thermal Coating
    Brynn's Modified EM Plating renamed to Brynn's Modified EM Coating
    Tuvan's Modified EM Plating renamed to Tuvan's Modified EM Coating
    Setele's Modified EM Plating renamed to Setele's Modified EM Coating
    Cormack's Modified EM Plating renamed to Cormack's Modified EM Coating
    Brynn's Modified Explosive Plating renamed to Brynn's Modified Explosive Coating
    Tuvan's Modified Explosive Plating renamed to Tuvan's Modified Explosive Coating
    Setele's Modified Explosive Plating renamed to Setele's Modified Explosive Coating
    Cormack's Modified Explosive Plating renamed to Cormack's Modified Explosive Coating
    Brynn's Modified Kinetic Plating renamed to Brynn's Modified Kinetic Coating
    Tuvan's Modified Kinetic Plating renamed to Tuvan's Modified Kinetic Coating
    Setele's Modified Kinetic Plating renamed to Setele's Modified Kinetic Coating
    Cormack's Modified Kinetic Plating renamed to Cormack's Modified Kinetic Coating
    Imperial Navy Thermal Plating renamed to Imperial Navy Thermal Coating
    Imperial Navy EM Plating renamed to Imperial Navy EM Coating
    Imperial Navy Explosive Plating renamed to Imperial Navy Explosive Coating
    Imperial Navy Kinetic Plating renamed to Imperial Navy Kinetic Coating
    Imperial Navy Adaptive Nano Plating renamed to Imperial Navy Multispectrum Coating
    Republic Fleet Thermal Plating renamed to Republic Fleet Thermal Coating
    Republic Fleet EM Plating renamed to Republic Fleet EM Coating
    Republic Fleet Explosive Plating renamed to Republic Fleet Explosive Coating
    Republic Fleet Kinetic Plating renamed to Republic Fleet Kinetic Coating
    Republic Fleet Adaptive Nano Plating renamed to Republic Fleet Multispectrum Coating
    Upgraded Adaptive Nano Plating I renamed to Upgraded Multispectrum Coating I
    Upgraded Kinetic Plating I renamed to Upgraded Kinetic Coating I
    Upgraded Explosive Plating I renamed to Upgraded Explosive Coating I
    Upgraded EM Plating I renamed to Upgraded EM Coating I
    Upgraded Thermal Plating I renamed to Upgraded Thermal Coating I
    Upgraded Layered Plating I renamed to Upgraded Layered Coating I
    Ammatar Navy Kinetic Plating renamed to Ammatar Navy Kinetic Coating
    Ammatar Navy Adaptive Nano Plating renamed to Ammatar Navy Multispectrum Coating
    Ammatar Navy Explosive Plating renamed to Ammatar Navy Explosive Coating
    Ammatar Navy EM Plating renamed to Ammatar Navy EM Coating
    Federation Navy Adaptive Nano Plating renamed to Federation Navy Multispectrum Coating
    Federation Navy Kinetic Plating renamed to Federation Navy Kinetic Coating
    Federation Navy Explosive Plating renamed to Federation Navy Explosive Coating
    Federation Navy EM Plating renamed to Federation Navy EM Coating
    Federation Navy Thermal Plating renamed to Federation Navy Thermal Coating
    Corpii C-Type Adaptive Nano Plating renamed to Corpii C-Type Multispectrum Coating
    Centii C-Type Adaptive Nano Plating renamed to Centii C-Type Multispectrum Coating
    Corpii B-Type Adaptive Nano Plating renamed to Corpii B-Type Multispectrum Coating
    Centii B-Type Adaptive Nano Plating renamed to Centii B-Type Multispectrum Coating
    Corpii A-Type Adaptive Nano Plating renamed to Corpii A-Type Multispectrum Coating
    Centii A-Type Adaptive Nano Plating renamed to Centii A-Type Multispectrum Coating
    Corpii C-Type Kinetic Plating renamed to Corpii C-Type Kinetic Coating
    Centii C-Type Kinetic Plating renamed to Centii C-Type Kinetic Coating
    Corpii C-Type Explosive Plating renamed to Corpii C-Type Explosive Coating
    Centii C-Type Explosive Plating renamed to Centii C-Type Explosive Coating
    Corpii C-Type EM Plating renamed to Corpii C-Type EM Coating
    Centii C-Type EM Plating renamed to Centii C-Type EM Coating
    Corpii C-Type Thermal Plating renamed to Corpii C-Type Thermal Coating
    Centii C-Type Thermal Plating renamed to Centii C-Type Thermal Coating
    Corpii B-Type Thermal Plating renamed to Corpii B-Type Thermal Coating
    Centii B-Type Thermal Plating renamed to Centii B-Type Thermal Coating
    Corpii B-Type Kinetic Plating renamed to Corpii B-Type Kinetic Coating
    Centii B-Type Kinetic Plating renamed to Centii B-Type Kinetic Coating
    Corpii B-Type Explosive Plating renamed to Corpii B-Type Explosive Coating
    Centii B-Type Explosive Plating renamed to Centii B-Type Explosive Coating
    Corpii B-Type EM Plating renamed to Corpii B-Type EM Coating
    Centii B-Type EM Plating renamed to Centii B-Type EM Coating
    Corpii A-Type Kinetic Plating renamed to Corpii A-Type Kinetic Coating
    Centii A-Type Kinetic Plating renamed to Centii A-Type Kinetic Coating
    Corpii A-Type Explosive Plating renamed to Corpii A-Type Explosive Coating
    Centii A-Type Explosive Plating renamed to Centii A-Type Explosive Coating
    Corpii A-Type EM Plating renamed to Corpii A-Type EM Coating
    Centii A-Type EM Plating renamed to Centii A-Type EM Coating
    Corpii A-Type Thermal Plating renamed to Corpii A-Type Thermal Coating
    Centii A-Type Thermal Plating renamed to Centii A-Type Thermal Coating
    Coreli C-Type Adaptive Nano Plating renamed to Coreli C-Type Multispectrum Coating
    Coreli C-Type Kinetic Plating renamed to Coreli C-Type Kinetic Coating
    Coreli C-Type Explosive Plating renamed to Coreli C-Type Explosive Coating
    Coreli C-Type EM Plating renamed to Coreli C-Type EM Coating
    Coreli C-Type Thermal Plating renamed to Coreli C-Type Thermal Coating
    Coreli B-Type Adaptive Nano Plating renamed to Coreli B-Type Multispectrum Coating
    Coreli B-Type Kinetic Plating renamed to Coreli B-Type Kinetic Coating
    Coreli B-Type Explosive Plating renamed to Coreli B-Type Explosive Coating
    Coreli B-Type EM Plating renamed to Coreli B-Type EM Coating
    Coreli B-Type Thermal Plating renamed to Coreli B-Type Thermal Coating
    Coreli A-Type Adaptive Nano Plating renamed to Coreli A-Type Multispectrum Coating
    Coreli A-Type Kinetic Plating renamed to Coreli A-Type Kinetic Coating
    Coreli A-Type Explosive Plating renamed to Coreli A-Type Explosive Coating
    Coreli A-Type EM Plating renamed to Coreli A-Type EM Coating
    Coreli A-Type Thermal Plating renamed to Coreli A-Type Thermal Coating
    Khanid Navy Adaptive Nano Plating renamed to Khanid Navy Multispectrum Coating
    Khanid Navy Kinetic Plating renamed to Khanid Navy Kinetic Coating
    Khanid Navy Explosive Plating renamed to Khanid Navy Explosive Coating
    Khanid Navy EM Plating renamed to Khanid Navy EM Coating
    Khanid Navy Thermal Plating renamed to Khanid Navy Thermal Coating
    Ammatar Navy Thermal Plating renamed to Ammatar Navy Thermal Coating
    Low-Grade Mimesis Alpha renamed to Low-grade Mimesis Alpha
    Low-Grade Mimesis Beta renamed to Low-grade Mimesis Beta
    Low-Grade Mimesis Gamma renamed to Low-grade Mimesis Gamma
    Low-Grade Mimesis Delta renamed to Low-grade Mimesis Delta
    Low-Grade Mimesis Epsilon renamed to Low-grade Mimesis Epsilon
    Low-Grade Mimesis Omega renamed to Low-grade Mimesis Omega
    Mid-Grade Mimesis Alpha renamed to Mid-grade Mimesis Alpha
    Mid-Grade Mimesis Beta renamed to Mid-grade Mimesis Beta
    Mid-Grade Mimesis Gamma renamed to Mid-grade Mimesis Gamma
    Mid-Grade Mimesis Delta renamed to Mid-grade Mimesis Delta
    Mid-Grade Mimesis Epsilon renamed to Mid-grade Mimesis Epsilon
    Mid-Grade Mimesis Omega renamed to Mid-grade Mimesis Omega
    High-Grade Mimesis Alpha renamed to High-grade Mimesis Alpha
    High-Grade Mimesis Beta renamed to High-grade Mimesis Beta
    High-Grade Mimesis Delta renamed to High-grade Mimesis Delta
    High-Grade Mimesis Epsilon renamed to High-grade Mimesis Epsilon
    High-Grade Mimesis Gamma renamed to High-grade Mimesis Gamma
    High-Grade Mimesis Omega renamed to High-grade Mimesis Omega
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
