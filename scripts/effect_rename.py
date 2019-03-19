#!/usr/bin/env python3
#======================================================================
# Copyright (C) 2010 Anton Vorobyov
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with eos.  If not, see <http://www.gnu.org/licenses/>.
#======================================================================
"""
Go through all effects and fill them with 'used by' comments.

There're several big stages:
Stage 1. Gather all required data into 'global' dictionaries. We have
2 dictionaries per grouping type, one which lists groups per typeid,
and another which lists typeIDs per group.
Stage 2. Cycle through each effect.
Stage 2.1. Compose similar set of dictionaries like in stage 1, but
this time we take into consideration typeIDs affected by effect picked
in stage 2.
Stage 2.2. Create several lists (1 per grouping type) which will keep
IDs of these groups which will describe set of the typeIDs, and start
iterating. Each iteration one ID will be appended to any of the lists.
Stage 2.2.1. Compose score dictionaries per grouping type, and
calculate total score for given grouping type.
Stage 2.2.2. Pick grouping type with highest score, find winner group
inside grouping type, append its ID to corresponding list created in
stage 2.2. If score is less than certain value, stop iterating. If some
items are not covered by set of winners from lists, they'll be
presented as single items.
Stage 2.3. Print results to file if anything has been changed.

Grouping types used are:
Groups (groupID of an item);
Categories (categoryID of groupID of an item);
Base types (variations, like they appear on eve's variation tab);
Market groups + variations (marketGroupID of an item, plus variations
of all items from given market group, excluding items with
marketGroupID).
Type names (various combinations of words taken from typeName of item).
"""

import copy
import itertools
import os.path
import re
import sqlite3
from optparse import OptionParser

script_dir = os.path.dirname(__file__)

# Form list of effects for processing
effects_path = os.path.join(script_dir, "..", "eos", "effects")

usage = "usage: %prog --database=DB [--debug=DEBUG]"
parser = OptionParser(usage=usage)
parser.add_option("-d", "--database", help="path to eve cache data dump in \
    sqlite format, default to eve database file included in pyfa (../eve.db)",
    type="string", default=os.path.join(script_dir, "..", "eve.db"))
parser.add_option("-e", "--effects", help="explicit comma-separated list of \
effects to process", type="string", default="")
parser.add_option("-r", "--remove", help="remove effect files that are not \
used by any items", action="store_true", dest="remove", default=False)
parser.add_option("-x", "--remove2", help="remove effect files that do not exist \
in database", action="store_true", dest="remove2", default=False)
parser.add_option("-u", "--debug", help="debug level, 0 by default",
                  type="int", default=0)
(options, args) = parser.parse_args()

# Connect to database and set up cursor
db = sqlite3.connect(os.path.expanduser(options.database))
cursor = db.cursor()

QUERY_ALLEFFECTS = 'SELECT effectID, effectName FROM dgmeffects'


# Compose list of effects w/o symbols which eos doesn't take into
# consideration, we'll use it to find proper effect IDs from file
# names
globalmap_effectnameeos_effectid = {}
globalmap_effectnameeos_effectnamedb = {}
STRIPSPEC = "[^A-Za-z0-9]"
cursor.execute(QUERY_ALLEFFECTS)
for row in cursor:
    effectid = row[0]
    effectnamedb = row[1]
    effectnameeos = re.sub(STRIPSPEC, "", effectnamedb).lower()
    if(os.path.isfile(os.path.join('..', 'eos','effects',effectnameeos+'.py'))):
        os.rename(os.path.join('..', 'eos','effects',effectnameeos+'.py'), os.path.join('..', 'eos','effects','effect{}.py'.format(effectid)))
    # There may be different effects with the same name, so form
