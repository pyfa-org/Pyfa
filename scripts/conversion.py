# Developed for module tiericide, this script will quickly print out a market
# conversion map based on patch notes, as well as database conversion mapping.

import argparse
import os.path
import sqlite3
import sys

# Add eos root path to sys.path so we can import ourselves
path = os.path.dirname(str(__file__, sys.getfilesystemencoding()))
sys.path.append(os.path.realpath(os.path.join(path, "..")))

# change to correct conversion

rename_phrase = " is now known as "
conversion_phrase = " is being converted to "

text = """Partial Weapon Navigation is being converted to Phased Scoped Target Painter
Indirect Scanning Dampening Unit I is being converted to Phased Muon Scoped Sensor Dampener
'Broker' Remote Sensor Dampener I is being converted to 'Executive' Remote Sensor Dampener
Initiated Ion Field ECM I is being converted to Hypnos Scoped Magnetometric ECM
FZ-3 Subversive Spatial Destabilizer ECM is being converted to BZ-5 Scoped Gravimetric ECM
'Penumbra' White Noise ECM is being converted to Umbra Scoped Radar ECM
Faint Phase Inversion ECM I is being converted to Enfeebling Scoped Ladar ECM
'Hypnos' Multispectral ECM I is being converted to Compulsive Scoped Multispectral ECM
1Z-3 Subversive ECM Eruption is being converted to Cetus Scoped Burst Jammer
'Prayer' Remote Tracking Computer is being converted to P-S Compact Remote Tracking Computer
'Tycoon' Remote Tracking Computer is being converted to 'Enterprise' Remote Tracking Computer
Monopulse Tracking Mechanism I is being converted to F-12 Enduring Tracking Computer
'Orion' Tracking CPU I is being converted to Optical Compact Tracking Computer
'Economist' Tracking Computer I is being converted to 'Marketeer' Tracking Computer
Beta-Nought Tracking Mode is being converted to 'Basic' Tracking Enhancer
Azimuth Descalloping Tracking Enhancer is being converted to 'Basic' Tracking Enhancer
F-AQ Delay-Line Scan Tracking Subroutines is being converted to 'Basic' Tracking Enhancer
Beam Parallax Tracking Program is being converted to 'Basic' Tracking Enhancer
Sigma-Nought Tracking Mode I is being converted to Fourier Compact Tracking Enhancer
Auto-Gain Control Tracking Enhancer I is being converted to Fourier Compact Tracking Enhancer
F-aQ Phase Code Tracking Subroutines is being converted to Fourier Compact Tracking Enhancer
Lateral Gyrostabilizer is being converted to 'Basic' Gyrostabilizer
F-M2 Weapon Inertial Suspensor is being converted to 'Basic' Gyrostabilizer
Hydraulic Stabilization Actuator is being converted to 'Basic' Gyrostabilizer
Stabilized Weapon Mounts is being converted to 'Basic' Gyrostabilizer
Cross-Lateral Gyrostabilizer I is being converted to Counterbalanced Compact Gyrostabilizer
F-M3 Munition Inertial Suspensor is being converted to Counterbalanced Compact Gyrostabilizer
Pneumatic Stabilization Actuator I is being converted to Counterbalanced Compact Gyrostabilizer
Monophonic Stabilization Actuator I is being converted to 'Kindred' Gyrostabilizer
Monophonic Stabilization Actuator I Blueprint is being converted to 'Kindred' Gyrostabilizer Blueprint
Heat Exhaust System is being converted to 'Basic' Heat Sink
C3S Convection Thermal Radiator is being converted to 'Basic' Heat Sink
'Boreas' Coolant System is being converted to 'Basic' Heat Sink
Stamped Heat Sink is being converted to 'Basic' Heat Sink
Thermal Exhaust System I is being converted to Extruded Compact Heat Sink
C4S Coiled Circuit Thermal Radiator is being converted to Extruded Compact Heat Sink
'Skadi' Coolant System I is being converted to Extruded Compact Heat Sink
'Mangonel' Heat Sink I is being converted to 'Trebuchet' Heat Sink I
'Mangonel' Heat Sink I Blueprint is being converted to 'Trebuchet' Heat Sink Blueprint
Insulated Stabilizer Array is being converted to 'Basic' Magnetic Field Stabilizer
Linear Flux Stabilizer is being converted to 'Basic' Magnetic Field Stabilizer
Gauss Field Balancer is being converted to 'Basic' Magnetic Field Stabilizer
Magnetic Vortex Stabilizer is being converted to 'Basic' Magnetic Field Stabilizer
Insulated Stabilizer Array I is being converted to Vortex Compact Magnetic Field Stabilizer
Linear Flux Stabilizer I is being converted to Vortex Compact Magnetic Field Stabilizer
Gauss Field Balancer I is being converted to Vortex Compact Magnetic Field Stabilizer
'Capitalist' Magnetic Field Stabilizer I is being converted to 'Monopoly' Magnetic Field Stabilizer
'Capitalist' Magnetic Field Stabilizer I Blueprint is being converted to 'Monopoly' Magnetic Field Stabilizer Blueprint
Muon Coil Bolt Array I is being converted to Crosslink Compact Ballistic Control System
Multiphasic Bolt Array I is being converted to Crosslink Compact Ballistic Control System
'Pandemonium' Ballistic Enhancement is being converted to Crosslink Compact Ballistic Control System
Ballistic 'Purge' Targeting System I is being converted to 'Full Duplex' Ballistic Control System
Ballistic 'Purge' Targeting System I Blueprint is being converted to 'Full Duplex' Ballistic Control System Blueprint
'Langour' Drive Disruptor I is being converted to X5 Enduring Stasis Webifier
Patterned Stasis Web I is being converted to Fleeting Compact Stasis Webifier
Fleeting Progressive Warp Scrambler I is being converted to Faint Epsilon Scoped Warp Scrambler
Fleeting Warp Disruptor I is being converted to Faint Scoped Warp Disruptor
GLFF Containment Field is being converted to 'Basic' Damage Control
Interior Force Field Array is being converted to 'Basic' Damage Control
F84 Local Damage System is being converted to 'Basic' Damage Control
Systematic Damage Control is being converted to 'Basic' Damage Control
'Gonzo' Damage Control I is being converted to 'Radical' Damage Control
'Gonzo' Damage Control I Blueprint is being converted to 'Radical' Damage Control Blueprint
Emergency Damage Control I is being converted to IFFA Compact Damage Control
F85 Peripheral Damage System I is being converted to IFFA Compact Damage Control
Pseudoelectron Containment Field I is being converted to IFFA Compact Damage Control
Micro Ld-Acid Capacitor Battery I is being converted to 'Micro' Cap Battery
Micro Ohm Capacitor Reserve I is being converted to 'Micro' Cap Battery
Micro F-4a Ld-Sulfate Capacitor Charge Unit is being converted to 'Micro' Cap Battery
Micro Peroxide Capacitor Power Cell is being converted to 'Micro' Cap Battery
Micro Capacitor Battery II is being converted to 'Micro' Cap Battery
Small Ohm Capacitor Reserve I is being converted to Small Compact Pb-Acid Cap Battery
Small F-4a Ld-Sulfate Capacitor Charge Unit is being converted to Small Compact Pb-Acid Cap Battery
Small Peroxide Capacitor Power Cell is being converted to Small Compact Pb-Acid Cap Battery
Medium Ohm Capacitor Reserve I is being converted to Medium Compact Pb-Acid Cap Battery
Medium F-4a Ld-Sulfate Capacitor Charge Unit is being converted to Medium Compact Pb-Acid Cap Battery
Medium Peroxide Capacitor Power Cell is being converted to Medium Compact Pb-Acid Cap Battery
Large Ohm Capacitor Reserve I is being converted to Large Compact Pb-Acid Cap Battery
Large F-4a Ld-Sulfate Capacitor Charge Unit is being converted to Large Compact Pb-Acid Cap Battery
Large Peroxide Capacitor Power Cell is being converted to Large Compact Pb-Acid Cap Battery
ECCM - Radar I is being converted to Sensor Booster I
ECCM - Ladar I is being converted to Sensor Booster I
ECCM - Magnetometric I is being converted to Sensor Booster I
ECCM - Gravimetric I is being converted to Sensor Booster I
ECCM - Omni I is being converted to Sensor Booster I
ECCM - Radar I Blueprint is being converted to Sensor Booster I Blueprint
ECCM - Ladar I Blueprint is being converted to Sensor Booster I Blueprint
ECCM - Magnetometric I Blueprint is being converted to Sensor Booster I Blueprint
ECCM - Gravimetric I Blueprint is being converted to Sensor Booster I Blueprint
ECCM - Omni I Blueprint is being converted to Sensor Booster I Blueprint
Alumel Radar ECCM Sensor Array I is being converted to Alumel-Wired Enduring Sensor Booster
Alumel Ladar ECCM Sensor Array I is being converted to Alumel-Wired Enduring Sensor Booster
Alumel Gravimetric ECCM Sensor Array I is being converted to Alumel-Wired Enduring Sensor Booster
Alumel Omni ECCM Sensor Array I is being converted to Alumel-Wired Enduring Sensor Booster
Alumel Magnetometric ECCM Sensor Array I is being converted to Alumel-Wired Enduring Sensor Booster
Supplemental Ladar ECCM Scanning Array I is being converted to Alumel-Wired Enduring Sensor Booster
Supplemental Gravimetric ECCM Scanning Array I is being converted to Alumel-Wired Enduring Sensor Booster
Supplemental Omni ECCM Scanning Array I is being converted to Alumel-Wired Enduring Sensor Booster
Supplemental Radar ECCM Scanning Array I is being converted to Alumel-Wired Enduring Sensor Booster
Supplemental Magnetometric ECCM Scanning Array I is being converted to Alumel-Wired Enduring Sensor Booster
Extra Radar ECCM Scanning Array I is being converted to F-90 Compact Sensor Booster
Extra Ladar ECCM Scanning Array I is being converted to F-90 Compact Sensor Booster
Extra Gravimetric ECCM Scanning Array I is being converted to F-90 Compact Sensor Booster
Extra Magnetometric ECCM Scanning Array I is being converted to F-90 Compact Sensor Booster
Gravimetric Positional ECCM Sensor System I is being converted to F-90 Compact Sensor Booster
Radar Positional ECCM Sensor System I is being converted to F-90 Compact Sensor Booster
Omni Positional ECCM Sensor System I is being converted to F-90 Compact Sensor Booster
Ladar Positional ECCM Sensor System I is being converted to F-90 Compact Sensor Booster
Magnetometric Positional ECCM Sensor System I is being converted to F-90 Compact Sensor Booster
Incremental Radar ECCM Scanning Array I is being converted to Alumel-Wired Enduring Sensor Booster
Incremental Ladar ECCM Scanning Array I is being converted to Alumel-Wired Enduring Sensor Booster
Incremental Gravimetric ECCM Scanning Array I is being converted to Alumel-Wired Enduring Sensor Booster
Incremental Magnetometric ECCM Scanning Array I is being converted to Alumel-Wired Enduring Sensor Booster
Prototype ECCM Radar Sensor Cluster is being converted to Alumel-Wired Enduring Sensor Booster
Prototype ECCM Ladar Sensor Cluster is being converted to Alumel-Wired Enduring Sensor Booster
Prototype ECCM Gravimetric Sensor Cluster is being converted to Alumel-Wired Enduring Sensor Booster
Prototype ECCM Omni Sensor Cluster is being converted to Alumel-Wired Enduring Sensor Booster
Prototype ECCM Magnetometric Sensor Cluster is being converted to Alumel-Wired Enduring Sensor Booster
Conjunctive Radar ECCM Scanning Array I is being converted to F-90 Compact Sensor Booster
Conjunctive Ladar ECCM Scanning Array I is being converted to F-90 Compact Sensor Booster
Conjunctive Gravimetric ECCM Scanning Array I is being converted to F-90 Compact Sensor Booster
Conjunctive Magnetometric ECCM Scanning Array I is being converted to F-90 Compact Sensor Booster
ECCM - Omni II is being converted to Sensor Booster II
ECCM - Gravimetric II is being converted to Sensor Booster II
ECCM - Ladar II is being converted to Sensor Booster II
ECCM - Magnetometric II is being converted to Sensor Booster II
ECCM - Radar II is being converted to Sensor Booster II
ECCM - Omni II Blueprint is being converted to Sensor Booster II Blueprint
ECCM - Gravimetric II Blueprint is being converted to Sensor Booster II Blueprint
ECCM - Ladar II Blueprint is being converted to Sensor Booster II Blueprint
ECCM - Magnetometric II Blueprint is being converted to Sensor Booster II Blueprint
ECCM - Radar II Blueprint is being converted to Sensor Booster II Blueprint
'Forger' ECCM - Magnetometric I is being converted to 'Shady' Sensor Booster
'Forger' ECCM - Magnetometric I Blueprint is being converted to 'Shady' Sensor Booster Blueprint
Basic RADAR Backup Array is being converted to 'Basic' Signal Amplifier
Basic Ladar Backup Array is being converted to 'Basic' Signal Amplifier
Basic Gravimetric Backup Array is being converted to 'Basic' Signal Amplifier
Basic Magnetometric Backup Array is being converted to 'Basic' Signal Amplifier
Basic Multi Sensor Backup Array is being converted to 'Basic' Signal Amplifier
Emergency Magnetometric Scanners is being converted to 'Basic' Signal Amplifier
Emergency Multi-Frequency Scanners is being converted to 'Basic' Signal Amplifier
Emergency RADAR Scanners is being converted to 'Basic' Signal Amplifier
Emergency Ladar Scanners is being converted to 'Basic' Signal Amplifier
Emergency Gravimetric Scanners is being converted to 'Basic' Signal Amplifier
Sealed RADAR Backup Cluster is being converted to 'Basic' Signal Amplifier
Sealed Magnetometric Backup Cluster is being converted to 'Basic' Signal Amplifier
Sealed Multi-Frequency Backup Cluster is being converted to 'Basic' Signal Amplifier
Sealed Ladar Backup Cluster is being converted to 'Basic' Signal Amplifier
Sealed Gravimetric Backup Cluster is being converted to 'Basic' Signal Amplifier
Surplus RADAR Reserve Array is being converted to 'Basic' Signal Amplifier
F-42 Reiterative RADAR Backup Sensors is being converted to 'Basic' Signal Amplifier
Surplus Magnetometric Reserve Array is being converted to 'Basic' Signal Amplifier
F-42 Reiterative Magnetometric Backup Sensors is being converted to 'Basic' Signal Amplifier
Surplus Multi-Frequency Reserve Array is being converted to 'Basic' Signal Amplifier
F-42 Reiterative Multi-Frequency Backup Sensors is being converted to 'Basic' Signal Amplifier
Surplus Ladar Reserve Array is being converted to 'Basic' Signal Amplifier
F-42 Reiterative Ladar Backup Sensors is being converted to 'Basic' Signal Amplifier
Surplus Gravimetric Reserve Array is being converted to 'Basic' Signal Amplifier
F-42 Reiterative Gravimetric Backup Sensors is being converted to 'Basic' Signal Amplifier
Gravimetric Backup Array I is being converted to Signal Amplifier I
Ladar Backup Array I is being converted to Signal Amplifier I
Magnetometric Backup Array I is being converted to Signal Amplifier I
Multi Sensor Backup Array I is being converted to Signal Amplifier I
RADAR Backup Array I is being converted to Signal Amplifier I
Gravimetric Backup Array I Blueprint is being converted to Signal Amplifier I Blueprint
Ladar Backup Array I Blueprint is being converted to Signal Amplifier I Blueprint
Magnetometric Backup Array I Blueprint is being converted to Signal Amplifier I Blueprint
Multi Sensor Backup Array I Blueprint is being converted to Signal Amplifier I Blueprint
RADAR Backup Array I Blueprint is being converted to Signal Amplifier I Blueprint
Protected Gravimetric Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Protected Ladar Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Protected Magnetometric Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Protected Multi-Frequency Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Protected RADAR Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Reserve Gravimetric Scanners is being converted to F-89 Compact Signal Amplifier
Reserve Ladar Scanners is being converted to F-89 Compact Signal Amplifier
Reserve Magnetometric Scanners is being converted to F-89 Compact Signal Amplifier
Reserve Multi-Frequency Scanners is being converted to F-89 Compact Signal Amplifier
Reserve RADAR Scanners is being converted to F-89 Compact Signal Amplifier
Secure Gravimetric Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Secure Ladar Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Secure Magnetometric Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Secure Radar Backup Cluster I is being converted to F-89 Compact Signal Amplifier
F-43 Repetitive Gravimetric Backup Sensors is being converted to F-89 Compact Signal Amplifier
F-43 Repetitive Ladar Backup Sensors is being converted to F-89 Compact Signal Amplifier
F-43 Repetitive Magnetometric Backup Sensors is being converted to F-89 Compact Signal Amplifier
F-43 Repetitive Multi-Frequency Backup Sensors is being converted to F-89 Compact Signal Amplifier
F-43 Repetitive RADAR Backup Sensors is being converted to F-89 Compact Signal Amplifier
Shielded Gravimetric Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Shielded Ladar Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Shielded Magnetometric Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Shielded Radar Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Surrogate Gravimetric Reserve Array I is being converted to F-89 Compact Signal Amplifier
Surrogate Ladar Reserve Array I is being converted to F-89 Compact Signal Amplifier
Surrogate Magnetometric Reserve Array I is being converted to F-89 Compact Signal Amplifier
Surrogate Multi-Frequency Reserve Array I is being converted to F-89 Compact Signal Amplifier
Surrogate RADAR Reserve Array I is being converted to F-89 Compact Signal Amplifier
Warded Gravimetric Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Warded Ladar Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Warded Magnetometric Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Warded Radar Backup Cluster I is being converted to F-89 Compact Signal Amplifier
Gravimetric Backup Array II is being converted to Signal Amplifier II
Ladar Backup Array II is being converted to Signal Amplifier II
Magnetometric Backup Array II is being converted to Signal Amplifier II
Multi Sensor Backup Array II is being converted to Signal Amplifier II
RADAR Backup Array II is being converted to Signal Amplifier II
Gravimetric Backup Array II Blueprint is being converted to Signal Amplifier II Blueprint
Ladar Backup Array II Blueprint is being converted to Signal Amplifier II Blueprint
Magnetometric Backup Array II Blueprint is being converted to Signal Amplifier II Blueprint
Multi Sensor Backup Array II Blueprint is being converted to Signal Amplifier II Blueprint
RADAR Backup Array II Blueprint is being converted to Signal Amplifier II Blueprint
Gravimetric Firewall is being converted to 'Firewall' Signal Amplifier
Ladar Firewall is being converted to 'Firewall' Signal Amplifier
Magnetometric Firewall is being converted to 'Firewall' Signal Amplifier
Multi Sensor Firewall is being converted to 'Firewall' Signal Amplifier
RADAR Firewall is being converted to 'Firewall' Signal Amplifier
ECCM Projector I is being converted to Remote Sensor Booster I
ECCM Projector I Blueprint is being converted to Remote Sensor Booster I Blueprint
Scattering ECCM Projector I is being converted to Linked Enduring Sensor Booster
Piercing ECCM Emitter I is being converted to Coadjunct Scoped Remote Sensor Booster
Spot Pulsing ECCM I is being converted to F-23 Compact Remote Sensor Booster
Phased Muon ECCM Caster I is being converted to F-23 Compact Remote Sensor Booster
ECCM Projector II is being converted to Remote Sensor Booster II
ECCM Projector II Blueprint is being converted to Remote Sensor Booster II Blueprint
Prototype Sensor Booster is being converted to Alumel-Wired Enduring Sensor Booster
Supplemental Scanning CPU I is being converted to F-90 Compact Sensor Booster
Amplitude Signal Enhancer is being converted to 'Basic' Signal Amplifier
'Acolyth' Signal Booster is being converted to 'Basic' Signal Amplifier
Type-E Discriminative Signal Augmentation is being converted to 'Basic' Signal Amplifier
F-90 Positional Signal Amplifier is being converted to 'Basic' Signal Amplifier
'Mendicant' Signal Booster I is being converted to F-89 Compact Signal Amplifier
Wavelength Signal Enhancer I is being converted to F-89 Compact Signal Amplifier
Type-D Attenuation Signal Augmentation is being converted to F-89 Compact Signal Amplifier
Connected Remote Sensor Booster is being converted to F-23 Compact Remote Sensor Booster
'Boss' Remote Sensor Booster is being converted to 'Bootleg' Remote Sensor Booster
'Entrepreneur' Remote Sensor Booster is being converted to 'Bootleg' Remote Sensor Booster
'Pacifier' Large Remote Armor Repairer is being converted to 'Peace' Large Remote Armor Repairer
'Pacifier' Large Remote Armor Repairer Blueprint is being converted to 'Peace' Large Remote Armor Repairer Blueprint
'Broker' Remote Sensor Dampener I Blueprint is being converted to 'Executive' Remote Sensor Dampener Blueprint
'Tycoon' Remote Tracking Computer Blueprint is being converted to 'Enterprise' Remote Tracking Computer Blueprint
'Economist' Tracking Computer I Blueprint is being converted to 'Marketeer' Tracking Computer Blueprint"""

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
