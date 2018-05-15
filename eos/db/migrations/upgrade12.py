"""
Migration 12

- Converts modules based on March 2016 Module Tiericide
    Some modules have been unpublished (and unpublished module attributes are removed
    from database), which causes pyfa to crash. We therefore replace these
    modules with their new replacements
"""

CONVERSIONS = {
    16457: (  # Crosslink Compact Ballistic Control System
        16459,  # Muon Coil Bolt Array I
        16461,  # Multiphasic Bolt Array I
        16463,  # 'Pandemonium' Ballistic Enhancement
    ),
    5281 : (  # Coadjunct Scoped Remote Sensor Booster
        7218,  # Piercing ECCM Emitter I
    ),
    5365 : (  # Cetus Scoped Burst Jammer
        5359,  # 1Z-3 Subversive ECM Eruption
    ),
    1973 : (  # Sensor Booster I
        1947,  # ECCM - Radar I
        2002,  # ECCM - Ladar I
        2003,  # ECCM - Magnetometric I
        2004,  # ECCM - Gravimetric I
        2005,  # ECCM - Omni I
    ),
    1951 : (  # 'Basic' Tracking Enhancer
        6322,  # Beta-Nought Tracking Mode
        6323,  # Azimuth Descalloping Tracking Enhancer
        6324,  # F-AQ Delay-Line Scan Tracking Subroutines
        6321,  # Beam Parallax Tracking Program
    ),
    521  : (  # 'Basic' Damage Control
        5829,  # GLFF Containment Field
        5831,  # Interior Force Field Array
        5835,  # F84 Local Damage System
        5833,  # Systematic Damage Control
    ),
    22925: (  # 'Bootleg' Remote Sensor Booster
        22939,  # 'Boss' Remote Sensor Booster
        22941,  # 'Entrepreneur' Remote Sensor Booster
    ),
    5443 : (  # Faint Epsilon Scoped Warp Scrambler
        5441,  # Fleeting Progressive Warp Scrambler I
    ),
    1963 : (  # Remote Sensor Booster I
        1959,  # ECCM Projector I
    ),
    6325 : (  # Fourier Compact Tracking Enhancer
        6326,  # Sigma-Nought Tracking Mode I
        6327,  # Auto-Gain Control Tracking Enhancer I
        6328,  # F-aQ Phase Code Tracking Subroutines
    ),
    21486: (  # 'Kindred' Gyrostabilizer
        21488,  # Monophonic Stabilization Actuator I
    ),
    19927: (  # Hypnos Scoped Magnetometric ECM
        9518,  # Initiated Ion Field ECM I
    ),
    10188: (  # 'Basic' Magnetic Field Stabilizer
        11111,  # Insulated Stabilizer Array
        11109,  # Linear Flux Stabilizer
        11115,  # Gauss Field Balancer
        11113,  # Magnetic Vortex Stabilizer
    ),
    22919: (  # 'Monopoly' Magnetic Field Stabilizer
        22917,  # 'Capitalist' Magnetic Field Stabilizer I
    ),
    5839 : (  # IFFA Compact Damage Control
        5841,  # Emergency Damage Control I
        5843,  # F85 Peripheral Damage System I
        5837,  # Pseudoelectron Containment Field I
    ),
    522  : (  # 'Micro' Cap Battery
        4747,  # Micro Ld-Acid Capacitor Battery I
        4751,  # Micro Ohm Capacitor Reserve I
        4745,  # Micro F-4a Ld-Sulfate Capacitor Charge Unit
        4749,  # Micro Peroxide Capacitor Power Cell
        3480,  # Micro Capacitor Battery II
    ),
    518  : (  # 'Basic' Gyrostabilizer
        5915,  # Lateral Gyrostabilizer
        5919,  # F-M2 Weapon Inertial Suspensor
        5913,  # Hydraulic Stabilization Actuator
        5917,  # Stabilized Weapon Mounts
    ),
    19931: (  # Compulsive Scoped Multispectral ECM
        19933,  # 'Hypnos' Multispectral ECM I
    ),
    5403 : (  # Faint Scoped Warp Disruptor
        5401,  # Fleeting Warp Disruptor I
    ),
    23902: (  # 'Trebuchet' Heat Sink I
        23900,  # 'Mangonel' Heat Sink I
    ),
    1893 : (  # 'Basic' Heat Sink
        5845,  # Heat Exhaust System
        5856,  # C3S Convection Thermal Radiator
        5855,  # 'Boreas' Coolant System
        5854,  # Stamped Heat Sink
    ),
    6160 : (  # F-90 Compact Sensor Booster
        20214,  # Extra Radar ECCM Scanning Array I
        20220,  # Extra Ladar ECCM Scanning Array I
        20226,  # Extra Gravimetric ECCM Scanning Array I
        20232,  # Extra Magnetometric ECCM Scanning Array I
        7948,  # Gravimetric Positional ECCM Sensor System I
        7964,  # Radar Positional ECCM Sensor System I
        7965,  # Omni Positional ECCM Sensor System I
        7966,  # Ladar Positional ECCM Sensor System I
        7970,  # Magnetometric Positional ECCM Sensor System I
        20218,  # Conjunctive Radar ECCM Scanning Array I
        20224,  # Conjunctive Ladar ECCM Scanning Array I
        20230,  # Conjunctive Gravimetric ECCM Scanning Array I
        20236,  # Conjunctive Magnetometric ECCM Scanning Array I
        6157,  # Supplemental Scanning CPU I
    ),
    23418: (  # 'Radical' Damage Control
        22893,  # 'Gonzo' Damage Control I
    ),
    19952: (  # Umbra Scoped Radar ECM
        9520,  # 'Penumbra' White Noise ECM
    ),
    1952 : (  # Sensor Booster II
        2258,  # ECCM - Omni II
        2259,  # ECCM - Gravimetric II
        2260,  # ECCM - Ladar II
        2261,  # ECCM - Magnetometric II
        2262,  # ECCM - Radar II
    ),
    5282 : (  # Linked Enduring Sensor Booster
        7219,  # Scattering ECCM Projector I
    ),
    1986 : (  # Signal Amplifier I
        2579,  # Gravimetric Backup Array I
        2583,  # Ladar Backup Array I
        2587,  # Magnetometric Backup Array I
        2591,  # Multi Sensor Backup Array I
        4013,  # RADAR Backup Array I
    ),
    4871 : (  # Large Compact Pb-Acid Cap Battery
        4875,  # Large Ohm Capacitor Reserve I
        4869,  # Large F-4a Ld-Sulfate Capacitor Charge Unit
        4873,  # Large Peroxide Capacitor Power Cell
    ),
    1964 : (  # Remote Sensor Booster II
        1960,  # ECCM Projector II
    ),
    5933 : (  # Counterbalanced Compact Gyrostabilizer
        5931,  # Cross-Lateral Gyrostabilizer I
        5935,  # F-M3 Munition Inertial Suspensor
        5929,  # Pneumatic Stabilization Actuator I
    ),
    4025 : (  # X5 Enduring Stasis Webifier
        4029,  # 'Langour' Drive Disruptor I
    ),
    4027 : (  # Fleeting Compact Stasis Webifier
        4031,  # Patterned Stasis Web I
    ),
    22937: (  # 'Enterprise' Remote Tracking Computer
        22935,  # 'Tycoon' Remote Tracking Computer
    ),
    22929: (  # 'Marketeer' Tracking Computer
        22927,  # 'Economist' Tracking Computer I
    ),
    1987 : (  # Signal Amplifier II
        2580,  # Gravimetric Backup Array II
        2584,  # Ladar Backup Array II
        2588,  # Magnetometric Backup Array II
        2592,  # Multi Sensor Backup Array II
        4014,  # RADAR Backup Array II
    ),
    19939: (  # Enfeebling Scoped Ladar ECM
        9522,  # Faint Phase Inversion ECM I
    ),
    5340 : (  # P-S Compact Remote Tracking Computer
        5341,  # 'Prayer' Remote Tracking Computer
    ),
    19814: (  # Phased Scoped Target Painter
        19808,  # Partial Weapon Navigation
    ),
    1949 : (  # 'Basic' Signal Amplifier
        1946,  # Basic RADAR Backup Array
        1982,  # Basic Ladar Backup Array
        1983,  # Basic Gravimetric Backup Array
        1984,  # Basic Magnetometric Backup Array
        1985,  # Basic Multi Sensor Backup Array
        6193,  # Emergency Magnetometric Scanners
        6194,  # Emergency Multi-Frequency Scanners
        6202,  # Emergency RADAR Scanners
        6216,  # Emergency Ladar Scanners
        6217,  # Emergency Gravimetric Scanners
        6225,  # Sealed RADAR Backup Cluster
        6238,  # Sealed Magnetometric Backup Cluster
        6239,  # Sealed Multi-Frequency Backup Cluster
        6241,  # Sealed Ladar Backup Cluster
        6242,  # Sealed Gravimetric Backup Cluster
        6257,  # Surplus RADAR Reserve Array
        6258,  # F-42 Reiterative RADAR Backup Sensors
        6283,  # Surplus Magnetometric Reserve Array
        6284,  # F-42 Reiterative Magnetometric Backup Sensors
        6285,  # Surplus Multi-Frequency Reserve Array
        6286,  # F-42 Reiterative Multi-Frequency Backup Sensors
        6289,  # Surplus Ladar Reserve Array
        6290,  # F-42 Reiterative Ladar Backup Sensors
        6291,  # Surplus Gravimetric Reserve Array
        6292,  # F-42 Reiterative Gravimetric Backup Sensors
        6309,  # Amplitude Signal Enhancer
        6310,  # 'Acolyth' Signal Booster
        6311,  # Type-E Discriminative Signal Augmentation
        6312,  # F-90 Positional Signal Amplifier
    ),
    21527: (  # 'Firewall' Signal Amplifier
        21521,  # Gravimetric Firewall
        21523,  # Ladar Firewall
        21525,  # Magnetometric Firewall
        21527,  # Multi Sensor Firewall
        21529,  # RADAR Firewall
    ),
    23416: (  # 'Peace' Large Remote Armor Repairer
        None,  # 'Pacifier' Large Remote Armor Repairer
    ),
    6176 : (  # F-12 Enduring Tracking Computer
        6174,  # Monopulse Tracking Mechanism I
    ),
    6159 : (  # Alumel-Wired Enduring Sensor Booster
        7917,  # Alumel Radar ECCM Sensor Array I
        7918,  # Alumel Ladar ECCM Sensor Array I
        7922,  # Alumel Gravimetric ECCM Sensor Array I
        7926,  # Alumel Omni ECCM Sensor Array I
        7937,  # Alumel Magnetometric ECCM Sensor Array I
        7867,  # Supplemental Ladar ECCM Scanning Array I
        7869,  # Supplemental Gravimetric ECCM Scanning Array I
        7870,  # Supplemental Omni ECCM Scanning Array I
        7887,  # Supplemental Radar ECCM Scanning Array I
        7889,  # Supplemental Magnetometric ECCM Scanning Array I
        20216,  # Incremental Radar ECCM Scanning Array I
        20222,  # Incremental Ladar ECCM Scanning Array I
        20228,  # Incremental Gravimetric ECCM Scanning Array I
        20234,  # Incremental Magnetometric ECCM Scanning Array I
        7892,  # Prototype ECCM Radar Sensor Cluster
        7893,  # Prototype ECCM Ladar Sensor Cluster
        7895,  # Prototype ECCM Gravimetric Sensor Cluster
        7896,  # Prototype ECCM Omni Sensor Cluster
        7914,  # Prototype ECCM Magnetometric Sensor Cluster
        6158,  # Prototype Sensor Booster
    ),
    5849 : (  # Extruded Compact Heat Sink
        5846,  # Thermal Exhaust System I
        5858,  # C4S Coiled Circuit Thermal Radiator
        5857,  # 'Skadi' Coolant System I
    ),
    22895: (  # 'Shady' Sensor Booster
        22897,  # 'Forger' ECCM - Magnetometric I
    ),
    11105: (  # Vortex Compact Magnetic Field Stabilizer
        11103,  # Insulated Stabilizer Array I
        11101,  # Linear Flux Stabilizer I
        11107,  # Gauss Field Balancer I
    ),
    22945: (  # 'Executive' Remote Sensor Dampener
        22943,  # 'Broker' Remote Sensor Dampener I
    ),
    6173 : (  # Optical Compact Tracking Computer
        6175,  # 'Orion' Tracking CPU I
    ),
    5279 : (  # F-23 Compact Remote Sensor Booster
        7217,  # Spot Pulsing ECCM I
        7220,  # Phased Muon ECCM Caster I
        5280,  # Connected Remote Sensor Booster
    ),
    4787 : (  # Small Compact Pb-Acid Cap Battery
        4791,  # Small Ohm Capacitor Reserve I
        4785,  # Small F-4a Ld-Sulfate Capacitor Charge Unit
        4789,  # Small Peroxide Capacitor Power Cell
    ),
    19946: (  # BZ-5 Scoped Gravimetric ECM
        9519,  # FZ-3 Subversive Spatial Destabilizer ECM
    ),
    6073 : (  # Medium Compact Pb-Acid Cap Battery
        6097,  # Medium Ohm Capacitor Reserve I
        6111,  # Medium F-4a Ld-Sulfate Capacitor Charge Unit
        6083,  # Medium Peroxide Capacitor Power Cell
    ),
    21484: (  # 'Full Duplex' Ballistic Control System
        21482,  # Ballistic 'Purge' Targeting System I
    ),
    6296 : (  # F-89 Compact Signal Amplifier
        6218,  # Protected Gravimetric Backup Cluster I
        6222,  # Protected Ladar Backup Cluster I
        6226,  # Protected Magnetometric Backup Cluster I
        6230,  # Protected Multi-Frequency Backup Cluster I
        6234,  # Protected RADAR Backup Cluster I
        6195,  # Reserve Gravimetric Scanners
        6199,  # Reserve Ladar Scanners
        6203,  # Reserve Magnetometric Scanners
        6207,  # Reserve Multi-Frequency Scanners
        6212,  # Reserve RADAR Scanners
        20238,  # Secure Gravimetric Backup Cluster I
        20244,  # Secure Ladar Backup Cluster I
        20250,  # Secure Magnetometric Backup Cluster I
        20260,  # Secure Radar Backup Cluster I
        6244,  # F-43 Repetitive Gravimetric Backup Sensors
        6252,  # F-43 Repetitive Ladar Backup Sensors
        6260,  # F-43 Repetitive Magnetometric Backup Sensors
        6268,  # F-43 Repetitive Multi-Frequency Backup Sensors
        6276,  # F-43 Repetitive RADAR Backup Sensors
        20240,  # Shielded Gravimetric Backup Cluster I
        20246,  # Shielded Ladar Backup Cluster I
        20252,  # Shielded Magnetometric Backup Cluster I
        20262,  # Shielded Radar Backup Cluster I
        6243,  # Surrogate Gravimetric Reserve Array I
        6251,  # Surrogate Ladar Reserve Array I
        6259,  # Surrogate Magnetometric Reserve Array I
        6267,  # Surrogate Multi-Frequency Reserve Array I
        6275,  # Surrogate RADAR Reserve Array I
        20242,  # Warded Gravimetric Backup Cluster I
        20248,  # Warded Ladar Backup Cluster I
        20254,  # Warded Magnetometric Backup Cluster I
        20264,  # Warded Radar Backup Cluster I
        6294,  # 'Mendicant' Signal Booster I
        6293,  # Wavelength Signal Enhancer I
        6295,  # Type-D Attenuation Signal Augmentation
    ),
    5302 : (  # Phased Muon Scoped Sensor Dampener
        5300,  # Indirect Scanning Dampening Unit I
    ),
}


def upgrade(saveddata_engine):
    # Convert modules
    for replacement_item, list in CONVERSIONS.items():
        for retired_item in list:
            saveddata_engine.execute('UPDATE "modules" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
            saveddata_engine.execute('UPDATE "cargo" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
