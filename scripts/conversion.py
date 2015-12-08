# Developed for module tiericide, this script will quickly print out a market
# conversion map based on patch notes, as well as database conversion mapping.

import argparse
import os.path
import sqlite3
import sys

# Add eos root path to sys.path so we can import ourselves
path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))
sys.path.append(os.path.realpath(os.path.join(path, "..")))

# change to correct conversion

rename_phrase = " is now known as "
conversion_phrase = " has been converted into "

text = """F-392 Baker Nunn Tracking Disruptor I is now known as Baker Nunn Enduring Tracking Disruptor I
Balmer Series Tracking Disruptor I is now known as Balmer Series Compact Tracking Disruptor I
'Abandon' Tracking Disruptor I is now known as C-IR Compact Guidance Disruptor I
DDO Photometry Tracking Disruptor I is now known as DDO Scoped Tracking Disruptor I
'Distributor' Tracking Disruptor I is now known as 'Distributor' Guidance Disruptor I
5W Infectious Power System Malfunction is now known as Small Infectious Scoped Energy Neutralizer
Small 'Gremlin' Power Core Disruptor I is now known as Small Gremlin Compact Energy Neutralizer
Medium 'Gremlin' Power Core Disruptor I is now known as Medium Gremlin Compact Energy Neutralizer
50W Infectious Power System Malfunction is now known as Medium Infectious Scoped Energy Neutralizer
Heavy 'Gremlin' Power Core Disruptor I is now known as Heavy Gremlin Compact Energy Neutralizer
500W Infectious Power System Malfunction is now known as Heavy Infectious Scoped Energy Neutralizer
'Caltrop' Small Energy Neutralizer I is now known as Small 'Caltrop' Energy Neutralizer
'Ditch' Medium Energy Neutralizer I is now known as Medium 'Ditch' Energy Neutralizer
'Moat' Heavy Energy Neutralizer I is now known as Heavy 'Moat' Energy Neutralizer
Small 'Knave' Energy Drain is now known as Small Knave Scoped Energy Nosferatu
Small 'Ghoul' Energy Siphon I is now known as Small Ghoul Compact Energy Nosferatu
Heavy 'Ghoul' Energy Siphon I is now known as Heavy Ghoul Compact Energy Nosferatu
Heavy 'Knave' Energy Drain is now known as Heavy Knave Scoped Energy Nosferatu
Medium 'Ghoul' Energy Siphon I is now known as Medium Ghoul Compact Energy Nosferatu
Medium 'Knave' Energy Drain is now known as Medium Knave Scoped Energy Nosferatu
'Upir' Small Nosferatu I is now known as Small 'Upir' Energy Nosferatu
'Strigoi' Medium Nosferatu I is now known as Medium 'Strigoi' Energy Nosferatu
'Vrykolakas' Heavy Nosferatu I is now known as Heavy 'Vrykolakas' Energy Nosferatu
M51 Iterative Shield Regenerator is now known as M51 Benefactor Compact Shield Recharger
Basic Shield Power Relay is now known as 'Basic' Shield Power Relay
Type-D Power Core Modification: Shield Power Relay is now known as Type-D Restrained Shield Power Relay
Mark I Generator Refitting: Shield Power Relay is now known as Mark I Compact Shield Power Relay
Basic Shield Flux Coil is now known as 'Basic' Shield Flux Coil
Type-D Power Core Modification: Shield Flux is now known as Type-D Restrained Shield Flux Coil
Mark I Generator Refitting: Shield Flux is now known as Mark I Compact Shield Flux Coil
Micro Remote Shield Booster I is now known as 'Micro' Remote Shield Booster
Capital Murky Remote Shield Booster is now known as CONCORD Capital Remote Shield Booster
Small Murky Remote Shield Booster is now known as Small Murky Compact Remote Shield Booster
Small Asymmetric Remote Shield Booster is now known as Small Asymmetric Enduring Remote Shield Booster
Small S95a Remote Shield Booster is now known as Small S95a Scoped Remote Shield Booster
Medium Murky Remote Shield Booster is now known as Medium Murky Compact Remote Shield Booster
Medium Asymmetric Remote Shield Booster is now known as Medium Asymmetric Enduring Remote Shield Booster
Medium S95a Remote Shield Booster is now known as Medium S95a Scoped Remote Shield Booster
Large Murky Remote Shield Booster is now known as Large Murky Compact Remote Shield Booster
Large Asymmetric Remote Shield Booster is now known as Large Asymmetric Enduring Remote Shield Booster
Large S95a Remote Shield Booster is now known as Large S95a Scoped Remote Shield Booster
Capital Coaxial Remote Armor Repairer is now known as CONCORD Capital Remote Armor Repairer
Small I-ax Remote Armor Repairer is now known as Small I-ax Enduring Remote Armor Repairer
Small Coaxial Remote Armor Repairer is now known as Small Coaxial Compact Remote Armor Repairer
Small 'Solace' Remote Armor Repairer is now known as Small Solace Scoped Remote Armor Repairer
Medium I-ax Remote Armor Repairer is now known as Medium I-ax Enduring Remote Armor Repairer
Medium Coaxial Remote Armor Repairer is now known as Medium Coaxial Compact Remote Armor Repairer
Medium 'Solace' Remote Armor Repairer is now known as Medium Solace Scoped Remote Armor Repairer
Large I-ax Remote Armor Repairer is now known as Large I-ax Enduring Remote Armor Repairer
Large Coaxial Remote Armor Repairer is now known as Large Coaxial Compact Remote Armor Repairer
Large 'Solace' Remote Armor Repairer is now known as Large Solace Scoped Remote Armor Repairer
Small 'Arup' Remote Armor Repairer has been converted into Small Solace Scoped Remote Armor Repairer
'Brotherhood' Small Remote Armor Repairer has been converted into 'Beatnik' Small Remote Armor Repairer
Medium 'Arup' Remote Armor Repairer has been converted into Medium Solace Scoped Remote Armor Repairer
Large 'Arup' Remote Armor Repairer has been converted into Large Solace Scoped Remote Armor Repairer
'Pacifier' Large Remote Armor Repairer has been converted into 'Peace' Large Remote Armor Repairer
Micro Asymmetric Remote Shield Booster has been converted into 'Micro' Remote Shield Booster
Micro Murky Remote Shield Booster has been converted into 'Micro' Remote Shield Booster
Micro 'Atonement' Remote Shield Booster has been converted into 'Micro' Remote Shield Booster
Micro S95a Remote Shield Booster has been converted into 'Micro' Remote Shield Booster
Small 'Atonement' Remote Shield Booster has been converted into Small Murky Compact Remote Shield Booster
Medium 'Atonement' Remote Shield Booster has been converted into Medium Murky Compact Remote Shield Booster
Large 'Atonement' Remote Shield Booster has been converted into Large Murky Compact Remote Shield Booster
E5 Prototype Energy Vampire has been converted into Small Knave Scoped Energy Nosferatu
Small Diminishing Power System Drain I has been converted into Small Ghoul Compact Energy Nosferatu
E50 Prototype Energy Vampire has been converted into Medium Knave Scoped Energy Nosferatu
Medium Diminishing Power System Drain I has been converted into Medium Ghoul Compact Energy Nosferatu
E500 Prototype Energy Vampire has been converted into Heavy Knave Scoped Energy Nosferatu
Heavy Diminishing Power System Drain I has been converted into Heavy Ghoul Compact Energy Nosferatu
Small Rudimentary Energy Destabilizer I has been converted into Small Infectious Scoped Energy Neutralizer
Small Unstable Power Fluctuator I has been converted into Small Gremlin Compact Energy Neutralizer
Medium Rudimentary Energy Destabilizer I has been converted into Medium Infectious Scoped Energy Neutralizer
Medium Unstable Power Fluctuator I has been converted into Medium Gremlin Compact Energy Neutralizer
Heavy Rudimentary Energy Destabilizer I has been converted into Heavy Infectious Scoped Energy Neutralizer
Heavy Unstable Power Fluctuator I has been converted into Heavy Gremlin Compact Energy Neutralizer
Passive Barrier Compensator I has been converted into M51 Benefactor Compact Shield Recharger
'Benefactor' Ward Reconstructor has been converted into M51 Benefactor Compact Shield Recharger
Supplemental Screen Generator I has been converted into M51 Benefactor Compact Shield Recharger
Alpha Reactor Shield Power Relay has been converted into 'Basic' Shield Power Relay
Marked Generator Refitting: Shield Power Relay has been converted into 'Basic' Shield Power Relay
Partial Power Plant Manager: Shield Power Relay has been converted into 'Basic' Shield Power Relay
Type-E Power Core Modification: Shield Power Relay has been converted into 'Basic' Shield Power Relay
Beta Reactor Control: Shield Power Relay I has been converted into Type-D Restrained Shield Power Relay
Local Power Plant Manager: Reaction Shield Power Relay I has been converted into Mark I Compact Shield Power Relay
Alpha Reactor Shield Flux has been converted into 'Basic' Shield Flux Coil
Marked Generator Refitting: Shield Flux has been converted into 'Basic' Shield Flux Coil
Partial Power Plant Manager: Shield Flux has been converted into 'Basic' Shield Flux Coil
Type-E Power Core Modification: Shield Flux has been converted into 'Basic' Shield Flux Coil
Beta Reactor Control: Shield Flux I has been converted into Type-D Restrained Shield Flux Coil
Local Power Plant Manager: Reaction Shield Flux I has been converted into Mark I Compact Shield Flux Coil"""

def main(old, new):
    # Open both databases and get their cursors
    old_db = sqlite3.connect(os.path.expanduser(old))
    old_cursor = old_db.cursor()
    new_db = sqlite3.connect(os.path.expanduser(new))
    new_cursor = new_db.cursor()

    renames = {}
    conversions = {}

    for x in text.splitlines():
        if conversion_phrase in x:
            c = x.split(conversion_phrase)
            container = conversions
        elif rename_phrase in x:
            c = x.split(rename_phrase)
            container = renames
        else:
            print "Unknown format: {}".format(x)
            sys.exit()

        old_name, new_name = c[0], c[1]
        old_item, new_item = None, None

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
            print "Error finding old item in {} -> {}".format(old_name, new_name)
        if not new_item:
            print "Error finding new item in {} -> {}".format(old_name, new_name)

        if not container.get((new_item,new_name), None):
            container[(new_item,new_name)] = []


        container[(new_item,new_name)].append((old_item, old_name))

    print "    # Renamed items"

    for new, old in renames.iteritems():
        if len(old) != 1:
            print "Incorrect length, key: {}, value: {}".format(new, old)
            sys.exit()
        old = old[0]

        print "    \"{}\": \"{}\",".format(old[1], new[1])

    # Convert modules
    print "\n    # Converted items"

    for new, olds in conversions.iteritems():
        for old in olds:
            print "    \"{}\": \"{}\",".format(old[1], new[1])

    print
    print

    for new, old in conversions.iteritems():
        print "    {}: (  # {}".format(new[0], new[1])
        for item in old:
            print "        {},  # {}".format(item[0], item[1])
        print "    ),"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", type=str)
    parser.add_argument("-n", "--new", type=str)
    args = parser.parse_args()

    main(args.old, args.new)
