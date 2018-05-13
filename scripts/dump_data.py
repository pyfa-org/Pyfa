#!/usr/bin/env python
"""
This script bootstraps Phobos from a supplied path and feeds it
information regarding EVE data paths and where to dump data. It then imports
some other scripts and uses them to convert the json data into a SQLite
database and then compare the new database to the existing one, producing a
diff which can then be used to assist in the updating.
"""

import sys
import os

# Phobos location
phb_path = os.path.expanduser("path/to/phobos")

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--eve", dest="eve_path", help="Location of EVE directory", required=True)
parser.add_argument("-c", "--cache", dest="cache_path", help="Location of EVE cache directory. If not specified, an attempt will be make to automatically determine path.")
parser.add_argument("-r", "--res", dest="res_path", help="Location of EVE shared resource cache. If not specified, an attempt will be make to automatically determine path.")
parser.add_argument("-d", "--dump", dest="dump_path", help="Location of Phobos JSON dump directory", required=True)
parser.add_argument("-p", "--phobos", dest="phb_path", help="Location of Phobos, defaults to path noted in script", default=phb_path)
parser.add_argument("-s", "--singularity", action="store_true", help="Singularity build")

args = parser.parse_args()
eve_path = os.path.expanduser(args.eve_path)
cache_path = os.path.expanduser(args.cache_path) if args.cache_path else None
res_path = os.path.expanduser(args.res_path) if args.res_path else None
dump_path = os.path.expanduser(args.dump_path)
script_path = os.path.dirname(__file__)

### Append Phobos to path
sys.path.append(os.path.expanduser(args.phb_path))

def header(text, subtext=None):
    print()
    print("* "*30)
    print(text.center(60))
    if subtext:
        print(subtext.center(60))
    print("* "*30)
    print()

header("Dumping Phobos Data", dump_path)

import reverence
from flow import FlowManager
from miner import *
from translator import Translator
from writer import *

rvr = reverence.blue.EVE(eve_path, cachepath=args.cache_path, sharedcachepath=res_path, server="singularity" if args.singularity else "tranquility")
print("EVE Directory: {}".format(rvr.paths.root))
print("Cache Directory: {}".format(rvr.paths.cache))
print("Shared Resource Directory: {}".format(rvr.paths.sharedcache))

pickle_miner = ResourcePickleMiner(rvr)
trans = Translator(pickle_miner)
bulkdata_miner = BulkdataMiner(rvr, trans)
staticcache_miner = ResourceStaticCacheMiner(rvr, trans)
miners = (
    MetadataMiner(eve_path),
    bulkdata_miner,
    staticcache_miner,
    TraitMiner(staticcache_miner, bulkdata_miner, trans),
    SqliteMiner(rvr.paths.root, trans),
    CachedCallsMiner(rvr, trans),
    pickle_miner
)

writers = (
    JsonWriter(dump_path, indent=2),
)

list = "dgmexpressions,dgmattribs,dgmeffects,dgmtypeattribs,dgmtypeeffects,"\
       "dgmunits,invcategories,invgroups,invmetagroups,invmetatypes,"\
       "invtypes,mapbulk_marketGroups,phbmetadata,phbtraits,fsdTypeOverrides,"\
       "evegroups,evetypes,evecategories,mapbulk_marketGroups,clonegrades"

FlowManager(miners, writers).run(list, "en-us")
