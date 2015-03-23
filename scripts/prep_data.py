#!/usr/bin/env python

import sys
import os

# Phobos location
phb_path = os.path.expanduser("path/to/phobos")

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--eve", dest="eve_path", help="Location of EVE directory", required=True)
parser.add_argument("-c", "--cache", dest="cache_path", help="Location of EVE cache directory. If not specified, an attempt will be make to automatically determine path.")
parser.add_argument("-r", "--res", dest="res_path", help="Location of EVE shared resource cache", required=True)
parser.add_argument("-d", "--dump", dest="dump_path", help="Location of Phobos JSON dump directory", required=True)
parser.add_argument("-p", "--phobos", dest="phb_path", help="Location of Phobos, defaults to path noted in script", default=phb_path)
parser.add_argument("-s", "--singularity", action="store_true", help="Singularity build")
parser.add_argument("-j", "--nojson", dest="nojson", action="store_true", help="Skip Phobos JSON data dump.")

args = parser.parse_args()
eve_path = os.path.expanduser(unicode(args.eve_path, sys.getfilesystemencoding()))
cache_path = os.path.expanduser(unicode(args.cache_path, sys.getfilesystemencoding())) if args.cache_path else None
path_res = os.path.expanduser(unicode(args.res_path,  sys.getfilesystemencoding()))
dump_path = os.path.expanduser(unicode(args.dump_path, sys.getfilesystemencoding()))
script_path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))

### Append Phobos to path
sys.path.append(os.path.expanduser(unicode(args.phb_path, sys.getfilesystemencoding())))

def header(text, subtext=None):
    print
    print "* "*30
    print text.center(60)
    if subtext:
        print subtext.center(60)
    print "* "*30
    print

### Data dump
if not args.nojson:
    header("Dumping Phobos Data", dump_path)

    import reverence
    from flow import FlowManager
    from miner import *
    from translator import Translator
    from writer import *

    rvr = reverence.blue.EVE(eve_path, cachepath=args.cache_path, respath=path_res, server="singularity" if args.singularity else "tranquility")

    pickle_miner = ResourcePickleMiner(rvr)
    trans = Translator(pickle_miner)
    bulkdata_miner = BulkdataMiner(rvr, trans)

    miners = (
        MetadataMiner(eve_path),
        bulkdata_miner,
        TraitMiner(bulkdata_miner, trans),
        SqliteMiner(eve_path, trans),
        CachedCallsMiner(rvr, trans),
        pickle_miner
    )

    writers = (
        JsonWriter(dump_path, indent=2),
    )

    list = "dgmexpressions,dgmattribs,dgmeffects,dgmtypeattribs,dgmtypeeffects,"\
           "dgmunits,icons,invcategories,invgroups,invmetagroups,invmetatypes,"\
           "invtypes,mapbulk_marketGroups,phbmetadata,phbtraits,fsdTypeOverrides"

    FlowManager(miners, writers).run(list, "multi")

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
old_db = os.path.join(script_path, "..", "staticdata", "eve.db")

header("Generating DIFF", diff_file)
old_stdout = sys.stdout
sys.stdout = open(diff_file, 'w')
itemDiff.main(old=old_db, new=db_file)
sys.stdout = old_stdout

print "\nAll done."
