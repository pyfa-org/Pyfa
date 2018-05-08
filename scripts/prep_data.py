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
parser.add_argument("-j", "--nojson", dest="nojson", action="store_true", help="Skip Phobos JSON data dump.")

args = parser.parse_args()
eve_path = os.path.expanduser(str(args.eve_path, sys.getfilesystemencoding()))
cache_path = os.path.expanduser(str(args.cache_path, sys.getfilesystemencoding())) if args.cache_path else None
res_path = os.path.expanduser(str(args.res_path,  sys.getfilesystemencoding())) if args.res_path else None
dump_path = os.path.expanduser(str(args.dump_path, sys.getfilesystemencoding()))
script_path = os.path.dirname(str(__file__, sys.getfilesystemencoding()))

### Append Phobos to path
sys.path.append(os.path.expanduser(str(args.phb_path, sys.getfilesystemencoding())))

def header(text, subtext=None):
    print()
    print("* "*30)
    print(text.center(60))
    if subtext:
        print(subtext.center(60))
    print("* "*30)
    print()

### Data dump
if not args.nojson:
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
    print()

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

### SQL Convert
import jsonToSql

db_file = os.path.join(dump_path, "eve.db")
header("Converting Data to SQL", db_file)

if os.path.isfile(db_file):
    os.remove(db_file)

jsonToSql.main("sqlite:///"+db_file, dump_path)

### Diff generation
import itemDiff
diff_file = os.path.join(dump_path, "diff.txt")
old_db = os.path.join(script_path, "..", "eve.db")

header("Generating DIFF", diff_file)
old_stdout = sys.stdout
sys.stdout = open(diff_file, 'w')
itemDiff.main(old=old_db, new=db_file)
sys.stdout = old_stdout

print("\nAll done.")
