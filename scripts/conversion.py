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
    Upgraded Armor EM Hardener I converted to Experimental Enduring EM Armor Hardener I
    Upgraded Armor Explosive Hardener I converted to Experimental Enduring Explosive Armor Hardener I
    Upgraded Armor Kinetic Hardener I converted to Experimental Enduring Kinetic Armor Hardener I
    Upgraded Armor Thermal Hardener I converted to Experimental Enduring Thermal Armor Hardener I
    Limited Armor EM Hardener I converted to Prototype Compact EM Armor Hardener I
    Limited Armor Explosive Hardener I converted to Prototype Compact Explosive Armor Hardener I
    Limited Armor Kinetic Hardener I converted to Prototype Compact Kinetic Armor Hardener I
    Limited Armor Thermal Hardener I converted to Prototype Compact Thermal Armor Hardener I
    Adaptive Invulnerability Shield Hardener I renamed to Multispectrum Shield Hardener I
    Gistum C-Type Adaptive Invulnerability Shield Hardener renamed to Gistum C-Type Multispectrum Shield Hardener
    Adaptive Invulnerability Shield Hardener II renamed to Multispectrum Shield Hardener II
    Anti-Explosive Shield Hardener I renamed to Explosive Shield Hardener I
    Anti-Kinetic Shield Hardener I renamed to Kinetic Shield Hardener I
    Anti-EM Shield Hardener I renamed to EM Shield Hardener I
    Anti-Thermal Shield Hardener I renamed to Thermal Shield Hardener I
    Anti-Explosive Shield Hardener II renamed to Explosive Shield Hardener II
    Anti-Kinetic Shield Hardener II renamed to Kinetic Shield Hardener II
    Anti-EM Shield Hardener II renamed to EM Shield Hardener II
    Anti-Thermal Shield Hardener II renamed to Thermal Shield Hardener II
    Gistum B-Type Adaptive Invulnerability Shield Hardener renamed to Gistum B-Type Multispectrum Shield Hardener
    Gistum A-Type Adaptive Invulnerability Shield Hardener renamed to Gistum A-Type Multispectrum Shield Hardener
    Pithum A-Type Adaptive Invulnerability Shield Hardener renamed to Pithum A-Type Multispectrum Shield Hardener
    Pithum B-Type Adaptive Invulnerability Shield Hardener renamed to Pithum B-Type Multispectrum Shield Hardener
    Pithum C-Type Adaptive Invulnerability Shield Hardener renamed to Pithum C-Type Multispectrum Shield Hardener
    Compact Anti-Kinetic Shield Hardener renamed to Compact Kinetic Shield Hardener
    Compact Anti-EM Shield Hardener renamed to Compact EM Shield Hardener
    Compact Adaptive Invulnerability Shield Hardener renamed to Compact Multispectrum Shield Hardener
    Compact Anti-Explosive Shield Hardener renamed to Compact Explosive Shield Hardener
    Compact Anti-Thermal Shield Hardener renamed to Compact Thermal Shield Hardener
    Armor Thermal Hardener I renamed to Thermal Armor Hardener I
    Armor EM Hardener I renamed to EM Armor Hardener I
    Armor Explosive Hardener I renamed to Explosive Armor Hardener I
    Armor Kinetic Hardener I renamed to Kinetic Armor Hardener I
    Armor EM Hardener II renamed to EM Armor Hardener II
    Armor Kinetic Hardener II renamed to Kinetic Armor Hardener II
    Armor Explosive Hardener II renamed to Explosive Armor Hardener II
    Armor Thermal Hardener II renamed to Thermal Armor Hardener II
    Dread Guristas Anti-EM Shield Hardener renamed to Dread Guristas EM Shield Hardener
    Dread Guristas Anti-Thermal Shield Hardener renamed to Dread Guristas Thermal Shield Hardener
    Dread Guristas Anti-Explosive Shield Hardener renamed to Dread Guristas Explosive Shield Hardener
    Dread Guristas Anti-Kinetic Shield Hardener renamed to Dread Guristas Kinetic Shield Hardener
    Dread Guristas Adaptive Invulnerability Shield Hardener renamed to Dread Guristas Multispectrum Shield Hardener
    True Sansha Armor EM Hardener renamed to True Sansha EM Armor Hardener
    Dark Blood Armor EM Hardener renamed to Dark Blood EM Armor Hardener
    True Sansha Armor Explosive Hardener renamed to True Sansha Explosive Armor Hardener
    Dark Blood Armor Explosive Hardener renamed to Dark Blood Explosive Armor Hardener
    True Sansha Armor Kinetic Hardener renamed to True Sansha Kinetic Armor Hardener
    Dark Blood Armor Kinetic Hardener renamed to Dark Blood Kinetic Armor Hardener
    True Sansha Armor Thermal Hardener renamed to True Sansha Thermal Armor Hardener
    Dark Blood Armor Thermal Hardener renamed to Dark Blood Thermal Armor Hardener
    Domination Armor EM Hardener renamed to Domination EM Armor Hardener
    Domination Armor Explosive Hardener renamed to Domination Explosive Armor Hardener
    Domination Armor Kinetic Hardener renamed to Domination Kinetic Armor Hardener
    Domination Armor Thermal Hardener renamed to Domination Thermal Armor Hardener
    Domination Anti-EM Shield Hardener renamed to Domination EM Shield Hardener
    Domination Anti-Thermal Shield Hardener renamed to Domination Thermal Shield Hardener
    Domination Anti-Explosive Shield Hardener renamed to Domination Explosive Shield Hardener
    Domination Anti-Kinetic Shield Hardener renamed to Domination Kinetic Shield Hardener
    Domination Adaptive Invulnerability Shield Hardener renamed to Domination Multispectrum Shield Hardener
    Shadow Serpentis Armor EM Hardener renamed to Shadow Serpentis EM Armor Hardener
    Shadow Serpentis Armor Explosive Hardener renamed to Shadow Serpentis Explosive Armor Hardener
    Shadow Serpentis Armor Kinetic Hardener renamed to Shadow Serpentis Kinetic Armor Hardener
    Shadow Serpentis Armor Thermal Hardener renamed to Shadow Serpentis Thermal Armor Hardener
    Kaikka's Modified Anti-Kinetic Shield Hardener renamed to Kaikka's Modified Kinetic Shield Hardener
    Thon's Modified Anti-Kinetic Shield Hardener renamed to Thon's Modified Kinetic Shield Hardener
    Vepas's Modified Anti-Kinetic Shield Hardener renamed to Vepas's Modified Kinetic Shield Hardener
    Estamel's Modified Anti-Kinetic Shield Hardener renamed to Estamel's Modified Kinetic Shield Hardener
    Kaikka's Modified Anti-EM Shield Hardener renamed to Kaikka's Modified EM Shield Hardener
    Thon's Modified Anti-EM Shield Hardener renamed to Thon's Modified EM Shield Hardener
    Vepas's Modified Anti-EM Shield Hardener renamed to Vepas's Modified EM Shield Hardener
    Estamel's Modified Anti-EM Shield Hardener renamed to Estamel's Modified EM Shield Hardener
    Kaikka's Modified Anti-Explosive Shield Hardener renamed to Kaikka's Modified Explosive Shield Hardener
    Thon's Modified Anti-Explosive Shield Hardener renamed to Thon's Modified Explosive Shield Hardener
    Vepas's Modified Anti-Explosive Shield Hardener renamed to Vepas's Modified Explosive Shield Hardener
    Estamel's Modified Anti-Explosive Shield Hardener renamed to Estamel's Modified Explosive Shield Hardener
    Kaikka's Modified Anti-Thermal Shield Hardener renamed to Kaikka's Modified Thermal Shield Hardener
    Thon's Modified Anti-Thermal Shield Hardener renamed to Thon's Modified Thermal Shield Hardener
    Vepas's Modified Anti-Thermal Shield Hardener renamed to Vepas's Modified Thermal Shield Hardener
    Estamel's Modified Anti-Thermal Shield Hardener renamed to Estamel's Modified Thermal Shield Hardener
    Kaikka's Modified Adaptive Invulnerability Shield Hardener renamed to Kaikka's Modified Multispectrum Shield Hardener
    Thon's Modified Adaptive Invulnerability Shield Hardener renamed to Thon's Modified Multispectrum Shield Hardener
    Vepas's Modified Adaptive Invulnerability Shield Hardener renamed to Vepas's Modified Multispectrum Shield Hardener
    Estamel's Modified Adaptive Invulnerability Shield Hardener renamed to Estamel's Modified Multispectrum Shield Hardener
    Brokara's Modified Armor EM Hardener renamed to Brokara's Modified EM Armor Hardener
    Tairei's Modified Armor EM Hardener renamed to Tairei's Modified EM Armor Hardener
    Selynne's Modified Armor EM Hardener renamed to Selynne's Modified EM Armor Hardener
    Raysere's Modified Armor EM Hardener renamed to Raysere's Modified EM Armor Hardener
    Vizan's Modified Armor EM Hardener renamed to Vizan's Modified EM Armor Hardener
    Ahremen's Modified Armor EM Hardener renamed to Ahremen's Modified EM Armor Hardener
    Chelm's Modified Armor EM Hardener renamed to Chelm's Modified EM Armor Hardener
    Draclira's Modified Armor EM Hardener renamed to Draclira's Modified EM Armor Hardener
    Brokara's Modified Armor Thermal Hardener renamed to Brokara's Modified Thermal Armor Hardener
    Tairei's Modified Armor Thermal Hardener renamed to Tairei's Modified Thermal Armor Hardener
    Selynne's Modified Armor Thermal Hardener renamed to Selynne's Modified Thermal Armor Hardener
    Raysere's Modified Armor Thermal Hardener renamed to Raysere's Modified Thermal Armor Hardener
    Vizan's Modified Armor Thermal Hardener renamed to Vizan's Modified Thermal Armor Hardener
    Ahremen's Modified Armor Thermal Hardener renamed to Ahremen's Modified Thermal Armor Hardener
    Chelm's Modified Armor Thermal Hardener renamed to Chelm's Modified Thermal Armor Hardener
    Draclira's Modified Armor Thermal Hardener renamed to Draclira's Modified Thermal Armor Hardener
    Brokara's Modified Armor Kinetic Hardener renamed to Brokara's Modified Kinetic Armor Hardener
    Tairei's Modified Armor Kinetic Hardener renamed to Tairei's Modified Kinetic Armor Hardener
    Selynne's Modified Armor Kinetic Hardener renamed to Selynne's Modified Kinetic Armor Hardener
    Raysere's Modified Armor Kinetic Hardener renamed to Raysere's Modified Kinetic Armor Hardener
    Vizan's Modified Armor Kinetic Hardener renamed to Vizan's Modified Kinetic Armor Hardener
    Ahremen's Modified Armor Kinetic Hardener renamed to Ahremen's Modified Kinetic Armor Hardener
    Chelm's Modified Armor Kinetic Hardener renamed to Chelm's Modified Kinetic Armor Hardener
    Draclira's Modified Armor Kinetic Hardener renamed to Draclira's Modified Kinetic Armor Hardener
    Brokara's Modified Armor Explosive Hardener renamed to Brokara's Modified Explosive Armor Hardener
    Tairei's Modified Armor Explosive Hardener renamed to Tairei's Modified Explosive Armor Hardener
    Selynne's Modified Armor Explosive Hardener renamed to Selynne's Modified Explosive Armor Hardener
    Raysere's Modified Armor Explosive Hardener renamed to Raysere's Modified Explosive Armor Hardener
    Vizan's Modified Armor Explosive Hardener renamed to Vizan's Modified Explosive Armor Hardener
    Ahremen's Modified Armor Explosive Hardener renamed to Ahremen's Modified Explosive Armor Hardener
    Chelm's Modified Armor Explosive Hardener renamed to Chelm's Modified Explosive Armor Hardener
    Draclira's Modified Armor Explosive Hardener renamed to Draclira's Modified Explosive Armor Hardener
    Brynn's Modified Armor EM Hardener renamed to Brynn's Modified EM Armor Hardener
    Tuvan's Modified Armor EM Hardener renamed to Tuvan's Modified EM Armor Hardener
    Setele's Modified Armor EM Hardener renamed to Setele's Modified EM Armor Hardener
    Cormack's Modified Armor EM Hardener renamed to Cormack's Modified EM Armor Hardener
    Brynn's Modified Armor Thermal Hardener renamed to Brynn's Modified Thermal Armor Hardener
    Tuvan's Modified Armor Thermal Hardener renamed to Tuvan's Modified Thermal Armor Hardener
    Setele's Modified Armor Thermal Hardener renamed to Setele's Modified Thermal Armor Hardener
    Cormack's Modified Armor Thermal Hardener renamed to Cormack's Modified Thermal Armor Hardener
    Brynn's Modified Armor Kinetic Hardener renamed to Brynn's Modified Kinetic Armor Hardener
    Tuvan's Modified Armor Kinetic Hardener renamed to Tuvan's Modified Kinetic Armor Hardener
    Setele's Modified Armor Kinetic Hardener renamed to Setele's Modified Kinetic Armor Hardener
    Cormack's Modified Armor Kinetic Hardener renamed to Cormack's Modified Kinetic Armor Hardener
    Brynn's Modified Armor Explosive Hardener renamed to Brynn's Modified Explosive Armor Hardener
    Tuvan's Modified Armor Explosive Hardener renamed to Tuvan's Modified Explosive Armor Hardener
    Setele's Modified Armor Explosive Hardener renamed to Setele's Modified Explosive Armor Hardener
    Cormack's Modified Armor Explosive Hardener renamed to Cormack's Modified Explosive Armor Hardener
    Imperial Navy Armor Thermal Hardener renamed to Imperial Navy Thermal Armor Hardener
    Imperial Navy Armor Kinetic Hardener renamed to Imperial Navy Kinetic Armor Hardener
    Imperial Navy Armor Explosive Hardener renamed to Imperial Navy Explosive Armor Hardener
    Imperial Navy Armor EM Hardener renamed to Imperial Navy EM Armor Hardener
    Republic Fleet Armor Thermal Hardener renamed to Republic Fleet Thermal Armor Hardener
    Republic Fleet Armor Kinetic Hardener renamed to Republic Fleet Kinetic Armor Hardener
    Republic Fleet Armor Explosive Hardener renamed to Republic Fleet Explosive Armor Hardener
    Republic Fleet Armor EM Hardener renamed to Republic Fleet EM Armor Hardener
    Experimental Armor EM Hardener I renamed to Experimental Enduring EM Armor Hardener I
    Prototype Armor EM Hardener I renamed to Prototype Compact EM Armor Hardener I
    Experimental Armor Explosive Hardener I renamed to Experimental Enduring Explosive Armor Hardener I
    Prototype Armor Explosive Hardener I renamed to Prototype Compact Explosive Armor Hardener I
    Experimental Armor Kinetic Hardener I renamed to Experimental Enduring Kinetic Armor Hardener I
    Prototype Armor Kinetic Hardener I renamed to Prototype Compact Kinetic Armor Hardener I
    Experimental Armor Thermal Hardener I renamed to Experimental Enduring Thermal Armor Hardener I
    Prototype Armor Thermal Hardener I renamed to Prototype Compact Thermal Armor Hardener I
    Caldari Navy Anti-Kinetic Shield Hardener renamed to Caldari Navy Kinetic Shield Hardener
    Caldari Navy Anti-Explosive Shield Hardener renamed to Caldari Navy Explosive Shield Hardener
    Caldari Navy Anti-Thermal Shield Hardener renamed to Caldari Navy Thermal Shield Hardener
    Caldari Navy Adaptive Invulnerability Shield Hardener renamed to Caldari Navy Multispectrum Shield Hardener
    Caldari Navy Anti-EM Shield Hardener renamed to Caldari Navy EM Shield Hardener
    Ammatar Navy Armor EM Hardener renamed to Ammatar Navy EM Armor Hardener
    Ammatar Navy Armor Explosive Hardener renamed to Ammatar Navy Explosive Armor Hardener
    Ammatar Navy Armor Kinetic Hardener renamed to Ammatar Navy Kinetic Armor Hardener
    Ammatar Navy Armor Thermal Hardener renamed to Ammatar Navy Thermal Armor Hardener
    Federation Navy Armor EM Hardener renamed to Federation Navy EM Armor Hardener
    Federation Navy Armor Explosive Hardener renamed to Federation Navy Explosive Armor Hardener
    Federation Navy Armor Kinetic Hardener renamed to Federation Navy Kinetic Armor Hardener
    Federation Navy Armor Thermal Hardener renamed to Federation Navy Thermal Armor Hardener
    Corpus C-Type Armor EM Hardener renamed to Corpus C-Type EM Armor Hardener
    Centus C-Type Armor EM Hardener renamed to Centus C-Type EM Armor Hardener
    Corpus C-Type Armor Explosive Hardener renamed to Corpus C-Type Explosive Armor Hardener
    Centus C-Type Armor Explosive Hardener renamed to Centus C-Type Explosive Armor Hardener
    Corpus C-Type Armor Kinetic Hardener renamed to Corpus C-Type Kinetic Armor Hardener
    Centus C-Type Armor Kinetic Hardener renamed to Centus C-Type Kinetic Armor Hardener
    Corpus C-Type Armor Thermal Hardener renamed to Corpus C-Type Thermal Armor Hardener
    Centus C-Type Armor Thermal Hardener renamed to Centus C-Type Thermal Armor Hardener
    Corpus B-Type Armor EM Hardener renamed to Corpus B-Type EM Armor Hardener
    Centus B-Type Armor EM Hardener renamed to Centus B-Type EM Armor Hardener
    Corpus B-Type Armor Explosive Hardener renamed to Corpus B-Type Explosive Armor Hardener
    Centus B-Type Armor Explosive Hardener renamed to Centus B-Type Explosive Armor Hardener
    Corpus B-Type Armor Kinetic Hardener renamed to Corpus B-Type Kinetic Armor Hardener
    Centus B-Type Armor Kinetic Hardener renamed to Centus B-Type Kinetic Armor Hardener
    Corpus B-Type Armor Thermal Hardener renamed to Corpus B-Type Thermal Armor Hardener
    Centus B-Type Armor Thermal Hardener renamed to Centus B-Type Thermal Armor Hardener
    Corpus A-Type Armor Thermal Hardener renamed to Corpus A-Type Thermal Armor Hardener
    Centus A-Type Armor Thermal Hardener renamed to Centus A-Type Thermal Armor Hardener
    Corpus A-Type Armor Kinetic Hardener renamed to Corpus A-Type Kinetic Armor Hardener
    Centus A-Type Armor Kinetic Hardener renamed to Centus A-Type Kinetic Armor Hardener
    Corpus A-Type Armor Explosive Hardener renamed to Corpus A-Type Explosive Armor Hardener
    Centus A-Type Armor Explosive Hardener renamed to Centus A-Type Explosive Armor Hardener
    Corpus A-Type Armor EM Hardener renamed to Corpus A-Type EM Armor Hardener
    Centus A-Type Armor EM Hardener renamed to Centus A-Type EM Armor Hardener
    Corpus X-Type Armor EM Hardener renamed to Corpus X-Type EM Armor Hardener
    Centus X-Type Armor EM Hardener renamed to Centus X-Type EM Armor Hardener
    Corpus X-Type Armor Explosive Hardener renamed to Corpus X-Type Explosive Armor Hardener
    Centus X-Type Armor Explosive Hardener renamed to Centus X-Type Explosive Armor Hardener
    Corpus X-Type Armor Kinetic Hardener renamed to Corpus X-Type Kinetic Armor Hardener
    Centus X-Type Armor Kinetic Hardener renamed to Centus X-Type Kinetic Armor Hardener
    Corpus X-Type Armor Thermal Hardener renamed to Corpus X-Type Thermal Armor Hardener
    Centus X-Type Armor Thermal Hardener renamed to Centus X-Type Thermal Armor Hardener
    Core C-Type Armor EM Hardener renamed to Core C-Type EM Armor Hardener
    Core C-Type Armor Explosive Hardener renamed to Core C-Type Explosive Armor Hardener
    Core C-Type Armor Kinetic Hardener renamed to Core C-Type Kinetic Armor Hardener
    Core C-Type Armor Thermal Hardener renamed to Core C-Type Thermal Armor Hardener
    Core B-Type Armor EM Hardener renamed to Core B-Type EM Armor Hardener
    Core B-Type Armor Explosive Hardener renamed to Core B-Type Explosive Armor Hardener
    Core B-Type Armor Kinetic Hardener renamed to Core B-Type Kinetic Armor Hardener
    Core B-Type Armor Thermal Hardener renamed to Core B-Type Thermal Armor Hardener
    Core A-Type Armor EM Hardener renamed to Core A-Type EM Armor Hardener
    Core A-Type Armor Explosive Hardener renamed to Core A-Type Explosive Armor Hardener
    Core A-Type Armor Kinetic Hardener renamed to Core A-Type Kinetic Armor Hardener
    Core A-Type Armor Thermal Hardener renamed to Core A-Type Thermal Armor Hardener
    Core X-Type Armor EM Hardener renamed to Core X-Type EM Armor Hardener
    Core X-Type Armor Explosive Hardener renamed to Core X-Type Explosive Armor Hardener
    Core X-Type Armor Kinetic Hardener renamed to Core X-Type Kinetic Armor Hardener
    Core X-Type Armor Thermal Hardener renamed to Core X-Type Thermal Armor Hardener
    Gist C-Type Anti-Kinetic Shield Hardener renamed to Gist C-Type Kinetic Shield Hardener
    Pith C-Type Anti-Kinetic Shield Hardener renamed to Pith C-Type Kinetic Shield Hardener
    Gist C-Type Anti-Explosive Shield Hardener renamed to Gist C-Type Explosive Shield Hardener
    Pith C-Type Anti-Explosive Shield Hardener renamed to Pith C-Type Explosive Shield Hardener
    Gist C-Type Anti-Thermal Shield Hardener renamed to Gist C-Type Thermal Shield Hardener
    Pith C-Type Anti-Thermal Shield Hardener renamed to Pith C-Type Thermal Shield Hardener
    Gist C-Type Anti-EM Shield Hardener renamed to Gist C-Type EM Shield Hardener
    Pith C-Type Anti-EM Shield Hardener renamed to Pith C-Type EM Shield Hardener
    Gist B-Type Anti-EM Shield Hardener renamed to Gist B-Type EM Shield Hardener
    Pith B-Type Anti-EM Shield Hardener renamed to Pith B-Type EM Shield Hardener
    Gist B-Type Anti-Thermal Shield Hardener renamed to Gist B-Type Thermal Shield Hardener
    Pith B-Type Anti-Thermal Shield Hardener renamed to Pith B-Type Thermal Shield Hardener
    Gist B-Type Anti-Explosive Shield Hardener renamed to Gist B-Type Explosive Shield Hardener
    Pith B-Type Anti-Explosive Shield Hardener renamed to Pith B-Type Explosive Shield Hardener
    Gist B-Type Anti-Kinetic Shield Hardener renamed to Gist B-Type Kinetic Shield Hardener
    Pith B-Type Anti-Kinetic Shield Hardener renamed to Pith B-Type Kinetic Shield Hardener
    Gist A-Type Anti-Kinetic Shield Hardener renamed to Gist A-Type Kinetic Shield Hardener
    Pith A-Type Anti-Kinetic Shield Hardener renamed to Pith A-Type Kinetic Shield Hardener
    Gist A-Type Anti-Explosive Shield Hardener renamed to Gist A-Type Explosive Shield Hardener
    Pith A-Type Anti-Explosive Shield Hardener renamed to Pith A-Type Explosive Shield Hardener
    Gist A-Type Anti-Thermal Shield Hardener renamed to Gist A-Type Thermal Shield Hardener
    Pith A-Type Anti-Thermal Shield Hardener renamed to Pith A-Type Thermal Shield Hardener
    Gist A-Type Anti-EM Shield Hardener renamed to Gist A-Type EM Shield Hardener
    Pith A-Type Anti-EM Shield Hardener renamed to Pith A-Type EM Shield Hardener
    Gist X-Type Anti-EM Shield Hardener renamed to Gist X-Type EM Shield Hardener
    Pith X-Type Anti-EM Shield Hardener renamed to Pith X-Type EM Shield Hardener
    Gist X-Type Anti-Thermal Shield Hardener renamed to Gist X-Type Thermal Shield Hardener
    Pith X-Type Anti-Thermal Shield Hardener renamed to Pith X-Type Thermal Shield Hardener
    Gist X-Type Anti-Explosive Shield Hardener renamed to Gist X-Type Explosive Shield Hardener
    Pith X-Type Anti-Explosive Shield Hardener renamed to Pith X-Type Explosive Shield Hardener
    Gist X-Type Anti-Kinetic Shield Hardener renamed to Gist X-Type Kinetic Shield Hardener
    Pith X-Type Anti-Kinetic Shield Hardener renamed to Pith X-Type Kinetic Shield Hardener
    'Nugget' Anti-Kinetic Shield Hardener renamed to 'Nugget' Kinetic Shield Hardener
    'Desert Heat' Anti-Thermal Shield Hardener renamed to 'Desert Heat' Thermal Shield Hardener
    'Posse' Adaptive Invulnerability Shield Hardener renamed to 'Posse' Multispectrum Shield Hardener
    'Poacher' Anti-EM Shield Hardener renamed to 'Poacher' EM Shield Hardener
    'Snake Eyes' Anti-Explosive Shield Hardener renamed to 'Snake Eyes' Explosive Shield Hardener
    Large Anti-EM Pump I renamed to Large EM Armor Reinforcer I
    Large Anti-Explosive Pump I renamed to Large Explosive Armor Reinforcer I
    Large Anti-Kinetic Pump I renamed to Large Kinetic Armor Reinforcer I
    Large Anti-Thermal Pump I renamed to Large Thermal Armor Reinforcer I
    Large Anti-EM Screen Reinforcer I renamed to Large EM Shield Reinforcer I
    Large Anti-Explosive Screen Reinforcer I renamed to Large Explosive Shield Reinforcer I
    Large Anti-Kinetic Screen Reinforcer I renamed to Large Kinetic Shield Reinforcer I
    Large Anti-Thermal Screen Reinforcer I renamed to Large Thermal Shield Reinforcer I
    Large Anti-EM Pump II renamed to Large EM Armor Reinforcer II
    Large Anti-Explosive Pump II renamed to Large Explosive Armor Reinforcer II
    Large Anti-Kinetic Pump II renamed to Large Kinetic Armor Reinforcer II
    Large Anti-Thermal Pump II renamed to Large Thermal Armor Reinforcer II
    Large Anti-EM Screen Reinforcer II renamed to Large EM Shield Reinforcer II
    Large Anti-Explosive Screen Reinforcer II renamed to Large Explosive Shield Reinforcer II
    Large Anti-Kinetic Screen Reinforcer II renamed to Large Kinetic Shield Reinforcer II
    Large Anti-Thermal Screen Reinforcer II renamed to Large Thermal Shield Reinforcer II
    Khanid Navy Armor EM Hardener renamed to Khanid Navy EM Armor Hardener
    Khanid Navy Armor Explosive Hardener renamed to Khanid Navy Explosive Armor Hardener
    Khanid Navy Armor Kinetic Hardener renamed to Khanid Navy Kinetic Armor Hardener
    Khanid Navy Armor Thermal Hardener renamed to Khanid Navy Thermal Armor Hardener
    Civilian Anti-Thermal Shield Hardener renamed to Civilian Thermal Shield Hardener
    Civilian Anti-EM Shield Hardener renamed to Civilian EM Shield Hardener
    Civilian Anti-Explosive Shield Hardener renamed to Civilian Explosive Shield Hardener
    Civilian Anti-Kinetic Shield Hardener renamed to Civilian Kinetic Shield Hardener
    Small Anti-EM Pump I renamed to Small EM Armor Reinforcer I
    Medium Anti-EM Pump I renamed to Medium EM Armor Reinforcer I
    Capital Anti-EM Pump I renamed to Capital EM Armor Reinforcer I
    Small Anti-EM Pump II renamed to Small EM Armor Reinforcer II
    Medium Anti-EM Pump II renamed to Medium EM Armor Reinforcer II
    Capital Anti-EM Pump II renamed to Capital EM Armor Reinforcer II
    Small Anti-Explosive Pump I renamed to Small Explosive Armor Reinforcer I
    Medium Anti-Explosive Pump I renamed to Medium Explosive Armor Reinforcer I
    Capital Anti-Explosive Pump I renamed to Capital Explosive Armor Reinforcer I
    Small Anti-Explosive Pump II renamed to Small Explosive Armor Reinforcer II
    Medium Anti-Explosive Pump II renamed to Medium Explosive Armor Reinforcer II
    Capital Anti-Explosive Pump II renamed to Capital Explosive Armor Reinforcer II
    Small Anti-Kinetic Pump I renamed to Small Kinetic Armor Reinforcer I
    Medium Anti-Kinetic Pump I renamed to Medium Kinetic Armor Reinforcer I
    Capital Anti-Kinetic Pump I renamed to Capital Kinetic Armor Reinforcer I
    Small Anti-Kinetic Pump II renamed to Small Kinetic Armor Reinforcer II
    Medium Anti-Kinetic Pump II renamed to Medium Kinetic Armor Reinforcer II
    Capital Anti-Kinetic Pump II renamed to Capital Kinetic Armor Reinforcer II
    Small Anti-Thermal Pump I renamed to Small Thermal Armor Reinforcer I
    Medium Anti-Thermal Pump I renamed to Medium Thermal Armor Reinforcer I
    Capital Anti-Thermal Pump I renamed to Capital Thermal Armor Reinforcer I
    Small Anti-Thermal Pump II renamed to Small Thermal Armor Reinforcer II
    Medium Anti-Thermal Pump II renamed to Medium Thermal Armor Reinforcer II
    Capital Anti-Thermal Pump II renamed to Capital Thermal Armor Reinforcer II
    Small Anti-EM Screen Reinforcer I renamed to Small EM Shield Reinforcer I
    Medium Anti-EM Screen Reinforcer I renamed to Medium EM Shield Reinforcer I
    Capital Anti-EM Screen Reinforcer I renamed to Capital EM Shield Reinforcer I
    Small Anti-EM Screen Reinforcer II renamed to Small EM Shield Reinforcer II
    Medium Anti-EM Screen Reinforcer II renamed to Medium EM Shield Reinforcer II
    Capital Anti-EM Screen Reinforcer II renamed to Capital EM Shield Reinforcer II
    Small Anti-Explosive Screen Reinforcer I renamed to Small Explosive Shield Reinforcer I
    Medium Anti-Explosive Screen Reinforcer I renamed to Medium Explosive Shield Reinforcer I
    Capital Anti-Explosive Screen Reinforcer I renamed to Capital Explosive Shield Reinforcer I
    Small Anti-Explosive Screen Reinforcer II renamed to Small Explosive Shield Reinforcer II
    Medium Anti-Explosive Screen Reinforcer II renamed to Medium Explosive Shield Reinforcer II
    Capital Anti-Explosive Screen Reinforcer II renamed to Capital Explosive Shield Reinforcer II
    Small Anti-Kinetic Screen Reinforcer I renamed to Small Kinetic Shield Reinforcer I
    Medium Anti-Kinetic Screen Reinforcer I renamed to Medium Kinetic Shield Reinforcer I
    Capital Anti-Kinetic Screen Reinforcer I renamed to Capital Kinetic Shield Reinforcer I
    Small Anti-Kinetic Screen Reinforcer II renamed to Small Kinetic Shield Reinforcer II
    Medium Anti-Kinetic Screen Reinforcer II renamed to Medium Kinetic Shield Reinforcer II
    Capital Anti-Kinetic Screen Reinforcer II renamed to Capital Kinetic Shield Reinforcer II
    Small Anti-Thermal Screen Reinforcer I renamed to Small Thermal Shield Reinforcer I
    Medium Anti-Thermal Screen Reinforcer I renamed to Medium Thermal Shield Reinforcer I
    Capital Anti-Thermal Screen Reinforcer I renamed to Capital Thermal Shield Reinforcer I
    Small Anti-Thermal Screen Reinforcer II renamed to Small Thermal Shield Reinforcer II
    Medium Anti-Thermal Screen Reinforcer II renamed to Medium Thermal Shield Reinforcer II
    Capital Anti-Thermal Screen Reinforcer II renamed to Capital Thermal Shield Reinforcer II
    Enduring Adaptive Invulnerability Shield Hardener renamed to Enduring Multispectrum Shield Hardener
    Enduring Anti-EM Shield Hardener renamed to Enduring EM Shield Hardener
    Enduring Anti-Explosive Shield Hardener renamed to Enduring Explosive Shield Hardener
    Enduring Anti-Kinetic Shield Hardener renamed to Enduring Kinetic Shield Hardener
    Enduring Anti-Thermal Shield Hardener renamed to Enduring Thermal Shield Hardener
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
