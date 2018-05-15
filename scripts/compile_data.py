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

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dump", dest="dump_path", help="Location of Phobos JSON dump directory", required=True)

args = parser.parse_args()
dump_path = os.path.expanduser(args.dump_path)
script_path = os.path.dirname(__file__)

def header(text, subtext=None):
    print()
    print("* "*30)
    print(text.center(60))
    if subtext:
        print(subtext.center(60))
    print("* "*30)
    print()

### SQL Convert
import jsonToSql

db_file = os.path.join(dump_path, "eve.db")
header("Converting Data to SQL", db_file)

if os.path.isfile(db_file):
    os.remove(db_file)

jsonToSql.main("sqlite:///" + db_file, dump_path)

### Diff generation
import itemDiff

diff_file = os.path.join(dump_path, "diff.txt")
old_db = os.path.join(script_path, "..", "eve.db")

header("Generating DIFF", diff_file)
old_stdout = sys.stdout
sys.stdout = open(diff_file, 'w')
itemDiff.main(old=old_db, new=db_file)
sys.stdout = old_stdout

header("Commiting changes for ", diff_file)

from subprocess import call

os.chdir(dump_path)

call(["git.exe", "add", "."])
call(["git.exe", "commit", "-m", "Commit"])

print("\nAll done.")