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

# Show debugging prints?
# 0 - Don't show debugging stuff and perform actual run
# 1 - Show only for first iteration
# 2 - Show for all iterations
DEBUG_LEVEL = options.debug

# Ways to control process:
# Adjust grouping type weights (more number - better chance to pick
# this grouping type)
GROUP_WEIGHT = 1.0
CATEGORY_WEIGHT = 1.0
BASETYPE_WEIGHT = 1.0
MARKETGROUPWITHVARS_WEIGHT = 0.3
TYPENAMECOMBS_WEIGHT = 1.0
# If score drops below this value, remaining items will be listed
# without any grouping
LOWEST_SCORE = 0.7

# Adjust scoring formulae
def calc_innerscore(affected_decribed, affected_undescribed, total,
                    pereffect_totalaffected, weight=1.0):
    """Inner score calculation formula"""
    # Percentage of items affected by effect out of total number of
    # items in this group
    coverage_total = (affected_decribed + affected_undescribed) / total
    # Same, but only described/undescribed items are taken
    coverage_described = affected_decribed / total
    coverage_undescribed = affected_undescribed / total
    # Already described items should have less weight
    coverage_additionalfactor = coverage_undescribed + coverage_described * 0
    # If group has just one item - it should have zero score
    affected_total_factor = affected_decribed + affected_undescribed - 1
    innerscore = (coverage_total ** 0.23) * coverage_additionalfactor * \
    affected_total_factor * weight
    return innerscore

def calc_outerscore(innerscore_dict, pereffect_totalaffected, weight):
    """Outer score calculation formula"""
    # Return just max of the inner scores, including weight factor
    if float(len(innerscore_dict)):
        outerscore = innerscore_dict[max(innerscore_dict, key=lambda a:
        innerscore_dict.get(a))] * weight
        return outerscore
    else: return 0.0

def validate_string(s):
    try:
        s.encode('ascii')
    except KeyboardInterrupt:
        raise
    except Exception:
        return False
    else:
        return True

# Connect to database and set up cursor
db = sqlite3.connect(os.path.expanduser(options.database))
cursor = db.cursor()

# Force some of the items to make them published
FORCEPUB_TYPES = ("Ibis", "Impairor", "Velator", "Reaper")
OVERRIDES_TYPEPUB = 'UPDATE invtypes SET published = 1 WHERE typeName = ?'
for typename in FORCEPUB_TYPES:
    cursor.execute(OVERRIDES_TYPEPUB, (typename,))
# Publish t3 Dessy Modes
cursor.execute("UPDATE invtypes SET published = 1 WHERE groupID = ?", (1306,))

# Queries to get raw data
QUERY_ALLEFFECTS = 'SELECT effectID, effectName FROM dgmeffects'
# Limit categories to Ships (6), Modules (7), Charges (8), Skills (16),
# Drones (18), Implants (20), Subsystems (32), and groups to
# Effect Beacons (920)
QUERY_PUBLISHEDTYPEIDS = 'SELECT it.typeID FROM invtypes AS it INNER JOIN \
invgroups AS ig ON it.groupID = ig.groupID INNER JOIN invcategories AS ic ON \
ig.categoryID = ic.categoryID WHERE it.published = 1 AND (ic.categoryID IN \
(6, 7, 8, 16, 18, 20, 32) OR ig.groupID = 920)'
QUERY_TYPEID_GROUPID = 'SELECT groupID FROM invtypes WHERE typeID = ? LIMIT 1'
QUERY_GROUPID_CATEGORYID = 'SELECT categoryID FROM invgroups WHERE \
groupID = ? LIMIT 1'
QUERY_TYPEID_PARENTTYPEID = 'SELECT parentTypeID FROM invmetatypes WHERE \
typeID = ? LIMIT 1'
QUERY_TYPEID_MARKETGROUPID = 'SELECT marketGroupID FROM invtypes WHERE \
typeID = ? LIMIT 1'
QUERY_TYPEID_TYPENAME = 'SELECT typeName FROM invtypes WHERE typeID = ? \
LIMIT 1'
QUERY_MARKETGROUPID_PARENTGROUPID = 'SELECT parentGroupID FROM \
invmarketgroups WHERE marketGroupID = ? LIMIT 1'
QUERY_EFFECTID_TYPEID = 'SELECT typeID FROM dgmtypeeffects WHERE effectID = ?'
# Queries for printing
QUERY_GROUPID_GROUPNAME = 'SELECT groupName FROM invgroups WHERE groupID = ? \
LIMIT 1'
QUERY_CATEGORYID_CATEGORYNAME = 'SELECT categoryName FROM invcategories \
WHERE categoryID = ? LIMIT 1'
QUERY_MARKETGROUPID_MARKETGROUPNAME = 'SELECT marketGroupName FROM \
invmarketgroups WHERE marketGroupID = ? LIMIT 1'

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
    # There may be different effects with the same name, so form
    # sets of IDs
    if not effectnameeos in globalmap_effectnameeos_effectid:
        globalmap_effectnameeos_effectid[effectnameeos] = set()
    globalmap_effectnameeos_effectid[effectnameeos].add(effectid)
    globalmap_effectnameeos_effectnamedb[effectnameeos] = effectnamedb
# Stage 1

# Published types set
publishedtypes = set()
cursor.execute(QUERY_PUBLISHEDTYPEIDS)
for row in cursor:
    publishedtypes.add(row[0])

# Compose group maps
# { groupid : set(typeid) }
globalmap_groupid_typeid = {}
# { typeid : groupid }
globalmap_typeid_groupid = {}
for typeid in publishedtypes:
    groupid = 0
    cursor.execute(QUERY_TYPEID_GROUPID, (typeid,))
    for row in cursor:
        groupid = row[0]
    if not groupid in globalmap_groupid_typeid:
        globalmap_groupid_typeid[groupid] = set()
    globalmap_groupid_typeid[groupid].add(typeid)
    globalmap_typeid_groupid[typeid] = groupid

# Category maps
# { categoryid : set(typeid) }
globalmap_categoryid_typeid =  {}
# { typeid : categoryid }
globalmap_typeid_categoryid =  {}
for typeid in publishedtypes:
    categoryid = 0
    cursor.execute(QUERY_GROUPID_CATEGORYID,
                   (globalmap_typeid_groupid[typeid],))
    for row in cursor:
        categoryid = row[0]
    if not categoryid in globalmap_categoryid_typeid:
        globalmap_categoryid_typeid[categoryid] = set()
    globalmap_categoryid_typeid[categoryid].add(typeid)
    globalmap_typeid_categoryid[typeid] = categoryid

# Base type maps
# { basetypeid : set(typeid) }
globalmap_basetypeid_typeid =  {}
# { typeid : basetypeid }
globalmap_typeid_basetypeid =  {}
for typeid in publishedtypes:
    # Not all typeIDs in the database have baseTypeID, so assign some
    # default value to it
    basetypeid = 0
    cursor.execute(QUERY_TYPEID_PARENTTYPEID, (typeid,))
    for row in cursor:
        basetypeid = row[0]
    # If base type is not published or is not set in database, consider
    # item as variation of self
    if basetypeid not in publishedtypes:
        basetypeid = typeid
    if not basetypeid in globalmap_basetypeid_typeid:
        globalmap_basetypeid_typeid[basetypeid] = set()
    globalmap_basetypeid_typeid[basetypeid].add(typeid)
    globalmap_typeid_basetypeid[typeid] = basetypeid

# Market group maps - we won't use these for further processing, but
# just as helper for composing other maps
# { marketgroupid : set(typeid) }
globalmap_marketgroupid_typeid =  {}
# { typeid : set(marketgroupid) }
globalmap_typeid_marketgroupid =  {}
for typeid in publishedtypes:
    marketgroupid = 0
    cursor.execute(QUERY_TYPEID_MARKETGROUPID, (typeid,))
    for row in cursor:
        marketgroupid = row[0]
    if not marketgroupid:
        continue
    if not marketgroupid in globalmap_marketgroupid_typeid:
        globalmap_marketgroupid_typeid[marketgroupid] = set()
    globalmap_marketgroupid_typeid[marketgroupid].add(typeid)
# Copy items to all parent market groups
INITIALMARKETGROUPIDS = tuple(globalmap_marketgroupid_typeid)
for marketgroupid in INITIALMARKETGROUPIDS:
    # Limit depths for case if database will refer to groups making
    # the loop
    cyclingmarketgroupid = marketgroupid
    for depth in range(20):
        cursor_parentmarket = db.cursor()
        cursor_parentmarket.execute(QUERY_MARKETGROUPID_PARENTGROUPID,
                                    (cyclingmarketgroupid,))
        for row in cursor_parentmarket:
            cyclingmarketgroupid = row[0]
        if cyclingmarketgroupid:
            if not cyclingmarketgroupid in globalmap_marketgroupid_typeid:
                globalmap_marketgroupid_typeid[cyclingmarketgroupid] = set()
            globalmap_marketgroupid_typeid[cyclingmarketgroupid].update\
            (globalmap_marketgroupid_typeid[marketgroupid])
        else: break
# Now, make a reverse map
for marketgroupid, typeidset in list(globalmap_marketgroupid_typeid.items()):
    for typeid in typeidset:
        if not typeid in globalmap_typeid_marketgroupid:
            globalmap_typeid_marketgroupid[typeid] = set()
        globalmap_typeid_marketgroupid[typeid].add(marketgroupid)

# Combine market groups and variations
# { marketgroupid : set(typeidwithvariations) }
globalmap_marketgroupid_typeidwithvariations = \
copy.deepcopy(globalmap_marketgroupid_typeid)
# { typeidwithvariations : set(marketgroupid) }
globalmap_typeidwithvariations_marketgroupid = {}
for marketgroupid in globalmap_marketgroupid_typeidwithvariations:
    typestoadd = set()
    for typeid in globalmap_marketgroupid_typeidwithvariations[marketgroupid]:
        if typeid in globalmap_basetypeid_typeid:
            for variationid in globalmap_basetypeid_typeid[typeid]:
                # Do not include items which have market group, even if
                # they're variation
                if not variationid in globalmap_typeid_marketgroupid:
                    typestoadd.add(variationid)
    globalmap_marketgroupid_typeidwithvariations[marketgroupid].update\
    (typestoadd)
# Make reverse map using simple way too
for marketgroupid, typeidwithvariationsset in \
list(globalmap_marketgroupid_typeidwithvariations.items()):
    for typeid in typeidwithvariationsset:
        if not typeid in globalmap_typeidwithvariations_marketgroupid:
            globalmap_typeidwithvariations_marketgroupid[typeid] = set()
        globalmap_typeidwithvariations_marketgroupid[typeid].add(marketgroupid)

# Item names map
# We need to include category ID to avoid combining items from different
# categories (e.g. skills and modules) and length of original name to
# assess word coverage of various type name combinations
# { ((typenamecomb), categoryid) : set(typeid) }
globalmap_typenamecombtuple_typeid =  {}
# { typeid : (set((typenamecomb)), len(typename)) }
globalmap_typeid_typenamecombtuple =  {}
for typeid in publishedtypes:
    typename = ""
    cursor.execute(QUERY_TYPEID_TYPENAME, (typeid,))
    for row in cursor:
        typename = row[0]
    # Split strings into separate words
    typenamesplitted = []
    # Start from the whole type name
    remainingstring = typename
    # We will pick word each iteration
    iterate = True
    while iterate:
        # This regexp helps to split into words with spaces and dashes
        # between them, for example: CX|-|1, Hardwiring| - |Inherent,
        # Zainou| |'Snapshot'
        separatingpattern_general = \
        "((?P<left_part>[^ -]+)(?P<separator>[ -]+)(?P<right_part>([^ -].*)))"
        # This will help to split names like those used in implants,
        # for example: ZET||500, EE||8
        separatingpattern_series = \
        "((?P<left_part>[A-Za-z]{2,4})(?P<right_part>[0-9]{1,4}.*))"
        # Check remainingstring using both criteria
        matchobject_general = re.match(separatingpattern_general,
                                       remainingstring)
        matchobject_series = re.match(separatingpattern_series,
                                      remainingstring)
        # Now, we need to find which criterion satisfies us
        usegeneral = False
        useseries = False
        # If remaining string meets both criteria
        if matchobject_general and matchobject_series:
            # We check which occurs first and pick it
            shift_general = len(matchobject_general.group("left_part"))
            shift_series = len(matchobject_series.group("left_part"))
            if shift_general <= shift_series:
                usegeneral = True
            else:
                useseries = True
        # If only one criterion is met, just pick it
        elif matchobject_general:
            usegeneral = True
        elif matchobject_series:
            useseries = True
        # Now, actually split string into word, separator and remaining
        # string and append word to list of words of current typename
        if usegeneral:
            newword = matchobject_general.group("left_part")
            separator = matchobject_general.group("separator")
            remainingstring = matchobject_general.group("right_part")
            typenamesplitted.append(newword)
        elif useseries:
            newword = matchobject_series.group("left_part")
            separator = ""
            remainingstring = matchobject_series.group("right_part")
            typenamesplitted.append(newword)
        # If we didn't match any regexp, then we see last word - append
        # it too and stop iterating
        else:
            typenamesplitted.append(remainingstring)
            iterate = False
    # Iterate through number of words which will be used to compose
    # combinations
    for wordnumindex in range(len(typenamesplitted)):
        # Iterate through all possible combinations
        for typenamecomb in itertools.combinations(typenamesplitted,
                                                   wordnumindex + 1):
            typenamecombtuple = (typenamecomb,
                                 globalmap_typeid_categoryid[typeid])
            if not typenamecombtuple in globalmap_typenamecombtuple_typeid:
                globalmap_typenamecombtuple_typeid[typenamecombtuple] = set()
            globalmap_typenamecombtuple_typeid[typenamecombtuple].add(typeid)
            if not typeid in globalmap_typeid_typenamecombtuple:
                globalmap_typeid_typenamecombtuple[typeid] = \
                (set(), len(typenamesplitted))
            globalmap_typeid_typenamecombtuple[typeid][0].add(typenamecomb)

if options.effects:
    effect_list = options.effects.split(",")
else:
    effect_list = []
    for effect_file in os.listdir(effects_path):
        if not effect_file.startswith('__'):
            file_name, file_extension = effect_file.rsplit('.', 1)
            # Ignore non-py files and exclude implementation-specific 'effects'
            if file_extension == "py" and not file_name in ("__init__"):
                effect_list.append(file_name)

# Stage 2

# Go through effect files one-by-one
for effect_name in effect_list:
    effect_file = "{0}.py".format(effect_name)
    # Stage 2.1
    # Set of items which are affected by current effect
    pereffectlist_usedbytypes = set()
    if effect_name in globalmap_effectnameeos_effectid:
        effectids = globalmap_effectnameeos_effectid[effect_name]
    else:
        if options.remove2:
            print(("Warning: effect file " + effect_name +
              " exists but is not in database, removing"))
            os.remove(os.path.join(effects_path, effect_file))
        else:
            print(("Warning: effect file " + effect_name +
              " exists but is not in database"))
        continue
    for effectid in effectids:
        cursor.execute(QUERY_EFFECTID_TYPEID, (effectid,))
        for row in cursor:
            typeid = row[0]
            if typeid in publishedtypes:
                pereffectlist_usedbytypes.add(typeid)
    # Number of items affected by current effect
    pereffect_totalaffected = len(pereffectlist_usedbytypes)

    # Compose per-group map of items which are affected by current
    # effect
    # { groupid : (set(typeid), describes) }
    effectmap_groupid_typeid = {}
    for typeid in pereffectlist_usedbytypes:
        groupid = globalmap_typeid_groupid[typeid]
        if not groupid in effectmap_groupid_typeid:
            effectmap_groupid_typeid[groupid] = [set(), False]
        effectmap_groupid_typeid[groupid][0].add(typeid)

    # Now, per-category map of items
    # { categoryid : (set(typeid), describes) }
    effectmap_categoryid_typeid = {}
    for typeid in pereffectlist_usedbytypes:
        categoryid = globalmap_typeid_categoryid[typeid]
        if not categoryid in effectmap_categoryid_typeid:
            effectmap_categoryid_typeid[categoryid] = [set(), False]
        effectmap_categoryid_typeid[categoryid][0].add(typeid)

    # Per-base type map of variations
    # { basetypeid : (set(typeid), describes) }
    effectmap_basetypeid_typeid = {}
    for typeid in pereffectlist_usedbytypes:
        basetypeid = globalmap_typeid_basetypeid[typeid]
        if not basetypeid in effectmap_basetypeid_typeid:
            effectmap_basetypeid_typeid[basetypeid] = [set(), False]
        effectmap_basetypeid_typeid[basetypeid][0].add(typeid)

    # Per-market group map with item variations
    # { marketgroupid : (set(typeidwithvariations), describes) }
    effectmap_marketgroupid_typeidwithvars = {}
    for typeid in pereffectlist_usedbytypes:
        if typeid in globalmap_typeid_marketgroupid:
            marketGroupIDs = globalmap_typeid_marketgroupid[typeid]
        else:
            marketGroupIDs = set()
        for marketgroupid in marketGroupIDs:
            if not marketgroupid in effectmap_marketgroupid_typeidwithvars:
                effectmap_marketgroupid_typeidwithvars[marketgroupid] = \
                [set(), False]
            effectmap_marketgroupid_typeidwithvars[marketgroupid][0].add\
            (typeid)

    # Per-type name combination map
    # { ((typenamecomb), categoryid) : (set(typeid), describes) }
    effectmap_typenamecombtuple_typeid = {}
    for typeid in pereffectlist_usedbytypes:
        typenamecombs = globalmap_typeid_typenamecombtuple[typeid][0]
        for typenamecomb in typenamecombs:
            typenamecombtuple = (typenamecomb,
                                 globalmap_typeid_categoryid[typeid])
            if not typenamecombtuple in effectmap_typenamecombtuple_typeid:
                effectmap_typenamecombtuple_typeid[typenamecombtuple] = \
                [set(), False]
            effectmap_typenamecombtuple_typeid[typenamecombtuple][0].add\
            (typeid)

    stopdebugprints = False
    if DEBUG_LEVEL >= 1:
        print(("\nEffect:", effect_name))
        print(("Total items affected: {0}".format(pereffect_totalaffected)))

    # Stage 2.2
    # This set holds all ids of already described items
    effect_describedtypes = set()
    # These lists contain ids of each grouping type which are used
    # to describe items from the set above
    describedbygroup = []
    describedbycategory = []
    describedbybasetype = []
    describedbymarketgroupwithvars = []
    describedbytypenamecomb = []

    # Each iteration some group is picked which will be used
    # to describe set of items
    iterate = True
    while iterate:
        # Stage 2.2.1
        # Stores scores for each group which describe set of items
        groupscore = {}
        for groupid in effectmap_groupid_typeid:
            # Skip groups which are already used for item
            # description (have 'describes' flag set to True)
            describesflag = effectmap_groupid_typeid[groupid][1]
            if not describesflag:
                # Items from current group affected by current
                # effect
                affectedset = effectmap_groupid_typeid[groupid][0]
                # Number of affected items from current group;
                # Already described
                affected_decribed = len(affectedset.intersection
                                        (effect_describedtypes))
                # Yet undescribed
                affected_undescribed =  len(affectedset.difference
                                            (effect_describedtypes))
                # Total number of items from this group (not
                # necessarily affected by current effect)
                total = len(globalmap_groupid_typeid[groupid])
                # Calculate inner score and push it into score
                # dictionary for current grouping type
                groupscore[groupid] = calc_innerscore\
                (affected_decribed, affected_undescribed, total,
                 pereffect_totalaffected)
                # Debug prints for inner data
                if DEBUG_LEVEL >= 1 and not stopdebugprints:
                    cursor.execute(QUERY_GROUPID_GROUPNAME, (groupid,))
                    for row in cursor:
                        groupName = row[0]
                    coverage = (affected_decribed +
                    affected_undescribed) / total * 100
                    # If debug level is 1, print results only for
                    # 1st iteration
                    if DEBUG_LEVEL == 1:
                        printstr = "Group: {0}: {1}/{2} ({3:.3}%, inner \
score: {4:.3})"
                        print((printstr.format(groupName,
                              affected_undescribed, total, coverage,
                              groupscore[groupid])))
                    # If it's 2, print results for each
                    # iteration, so we need to include number
                    # of already described items
                    if DEBUG_LEVEL == 2:
                        printstr = "Group: {0}: {1}+{2}/{3} ({4:.3}%, \
inner score: {5:.3})"
                        print((printstr.format(groupName,
                              affected_undescribed, affected_decribed,
                              total, coverage, groupscore[groupid])))
        # Calculate outer score for this grouping type
        groupouterscore = calc_outerscore(groupscore,
                                          pereffect_totalaffected,
                                          GROUP_WEIGHT)
        # Debug print for outer data
        if DEBUG_LEVEL >= 1 and not stopdebugprints:
            printstr = "Groups outer score: {0:.3}"
            print((printstr.format(groupouterscore)))

        categoryscore = {}
        for categoryid in effectmap_categoryid_typeid:
            describesflag = effectmap_categoryid_typeid[categoryid][1]
            if not describesflag:
                affectedset = effectmap_categoryid_typeid[categoryid][0]
                affected_decribed = len(affectedset.intersection
                                        (effect_describedtypes))
                affected_undescribed =  len(affectedset.difference
                                            (effect_describedtypes))
                total = len(globalmap_categoryid_typeid[categoryid])
                categoryscore[categoryid] = calc_innerscore\
                (affected_decribed, affected_undescribed, total,
                 pereffect_totalaffected)
                if DEBUG_LEVEL >= 1 and not stopdebugprints:
                    cursor.execute(QUERY_CATEGORYID_CATEGORYNAME,
                                   (categoryid,))
                    for row in cursor:
                        categoryname = row[0]
                    coverage = (affected_decribed +
                    affected_undescribed) / total * 100
                    if DEBUG_LEVEL == 1:
                        printstr = "Category: {0}: {1}/{2} ({3:.3}%, \
inner score: {4:.3})"
                        print((printstr.format(categoryname,
                              affected_undescribed, total, coverage,
                              categoryscore[categoryid])))
                    if DEBUG_LEVEL == 2:
                        printstr = "Category: {0}: {1}+{2}/{3} ({4:.3}%, \
inner score: {5:.3})"
                        print((printstr.format(categoryname,
                              affected_undescribed, affected_decribed,
                              total, coverage, categoryscore[categoryid])))
        categoryouterscore = calc_outerscore(categoryscore,
                                             pereffect_totalaffected,
                                             CATEGORY_WEIGHT)
        if DEBUG_LEVEL >= 1 and not stopdebugprints:
            printstr = "Category outer score: {0:.3}"
            print((printstr.format(categoryouterscore)))

        basetypescore = {}
        for basetypeid in effectmap_basetypeid_typeid:
            describesflag = effectmap_basetypeid_typeid[basetypeid][1]
            if not describesflag:
                affectedset = effectmap_basetypeid_typeid[basetypeid][0]
                affected_decribed = len(affectedset.intersection
                                        (effect_describedtypes))
                affected_undescribed =  len(affectedset.difference
                                            (effect_describedtypes))
                total = len(globalmap_basetypeid_typeid[basetypeid])
                basetypescore[basetypeid] = calc_innerscore\
                (affected_decribed, affected_undescribed, total,
                 pereffect_totalaffected)
                if DEBUG_LEVEL >= 1 and not stopdebugprints:
                    cursor.execute(QUERY_TYPEID_TYPENAME, (basetypeid,))
                    for row in cursor:
                        basetypename = row[0]
                    coverage = (affected_decribed +
                    affected_undescribed) / total * 100
                    if DEBUG_LEVEL == 1:
                        printstr = "Base item: {0}: {1}/{2} ({3:.3}%, \
inner score: {4:.3})"
                        print((printstr.format(basetypename,
                              affected_undescribed, total, coverage,
                              basetypescore[basetypeid])))
                    if DEBUG_LEVEL == 2:
                        printstr = "Base item: {0}: {1}+{2}/{3} ({4:.3}%, \
inner score: {5:.3})"
                        print((printstr.format(basetypename,
                              affected_undescribed, affected_decribed,
                              total, coverage, basetypescore[basetypeid])))
        basetypeouterscore = calc_outerscore(basetypescore,
                                             pereffect_totalaffected,
                                             BASETYPE_WEIGHT)
        #Print outer data
        if DEBUG_LEVEL >= 1 and not stopdebugprints:
            printstr = "Base item outer score: {0:.3}"
            print((printstr.format(basetypeouterscore)))

        marketgroupwithvarsscore = {}
        for marketgroupid in effectmap_marketgroupid_typeidwithvars:
            describesflag = effectmap_marketgroupid_typeidwithvars\
            [marketgroupid][1]
            if not describesflag:
                affectedset = effectmap_marketgroupid_typeidwithvars\
                [marketgroupid][0]
                affected_decribed = len(affectedset.intersection
                                        (effect_describedtypes))
                affected_undescribed =  len(affectedset.difference
                                            (effect_describedtypes))
                total = len(globalmap_marketgroupid_typeidwithvariations
                            [marketgroupid])
                marketgroupwithvarsscore[marketgroupid] = calc_innerscore\
                (affected_decribed, affected_undescribed, total,
                 pereffect_totalaffected)
                if DEBUG_LEVEL >= 1 and not stopdebugprints:
                    cursor.execute(QUERY_MARKETGROUPID_MARKETGROUPNAME,
                                   (marketgroupid,))
                    for row in cursor:
                        marketgroupname = row[0]
                    # Prepend market group name with its parents
                    # names
                    prependparentid = marketgroupid
                    #Limit depth in case if market groups form a loop
                    for depth in range(20):
                        cursor_parentmarket = db.cursor()
                        cursor_parentmarket.execute\
                        (QUERY_MARKETGROUPID_PARENTGROUPID,
                         (prependparentid,))
                        for row in cursor_parentmarket:
                            prependparentid = row[0]
                        if prependparentid:
                            cursor.execute\
                            (QUERY_MARKETGROUPID_MARKETGROUPNAME,
                             (prependparentid,))
                            for row in cursor:
                                marketgroupname = "{0} > {1}".format\
                                (row[0],marketgroupname)
                        else:
                            break
                    coverage = (affected_decribed +
                    affected_undescribed) / total * 100
                    if DEBUG_LEVEL == 1:
                        printstr = "Market group with variations: {0}: \
{1}/{2} ({3:.3}%, inner score: {4:.3})"
                        print((printstr.format(marketgroupname,
                              affected_undescribed, total, coverage,
                              marketgroupwithvarsscore[marketgroupid])))
                    if DEBUG_LEVEL == 2:
                        printstr = "Market group with variations: {0}: \
{1}+{2}/{3} ({4:.3}%, inner score: {5:.3})"
                        print((printstr.format(marketgroupname,
                              affected_undescribed,
                              affected_decribed, total, coverage,
                              marketgroupwithvarsscore[marketgroupid])))
        marketgroupwithvarsouterscore = calc_outerscore\
        (marketgroupwithvarsscore, pereffect_totalaffected,
         MARKETGROUPWITHVARS_WEIGHT)
        if DEBUG_LEVEL >= 1 and not stopdebugprints:
            printstr = "Market group outer score: {0:.3}"
            print((printstr.format(marketgroupwithvarsouterscore)))

        typenamecombscore = {}
        for typenamecombtuple in effectmap_typenamecombtuple_typeid:
            describesflag = effectmap_typenamecombtuple_typeid\
            [typenamecombtuple][1]
            if not describesflag:
                affectedset = effectmap_typenamecombtuple_typeid\
                [typenamecombtuple][0]
                affected_decribed = len(affectedset.intersection
                                        (effect_describedtypes))
                affected_undescribed =  len(affectedset.difference
                                            (effect_describedtypes))
                total = len(globalmap_typenamecombtuple_typeid
                            [typenamecombtuple])
                # Type names are special: wee also need to consider
                # how certain word combination covers full type
                # name
                averagecoverage = 0
                itemsnamedlikethis = effectmap_typenamecombtuple_typeid\
                [typenamecombtuple][0]
                for typeid in itemsnamedlikethis:
                    # Add number of words in combination divided by
                    # total number of words from any given item
                    averagecoverage += len(typenamecombtuple[0]) / \
                    globalmap_typeid_typenamecombtuple[typeid][1]
                # Then divide by number of items we checked, making
                # it real average
                averagecoverage = averagecoverage / len(itemsnamedlikethis)
                # Pass average coverage as additional balancing
                # factor with certain weight factor (80%)
                typenamecombscore[typenamecombtuple] = \
                calc_innerscore(affected_decribed, affected_undescribed,
                                total, pereffect_totalaffected,
                                0.2 + averagecoverage*0.8)
                if DEBUG_LEVEL >= 1 and not stopdebugprints:
                    typenamecombprintable = " ".join(typenamecombtuple[0])
                    coverage = (affected_decribed +
                                affected_undescribed) / total * 100
                    if DEBUG_LEVEL == 1:
                        printstr = "Type name combination: \"{0}\": \
{1}/{2} ({3:.3}%, inner score: {4:.3})"
                        print((printstr.format(typenamecombprintable,
                              affected_undescribed, total, coverage,
                              typenamecombscore[typenamecombtuple])))
                    if DEBUG_LEVEL == 2:
                        printstr = "Type name combination: \"{0}\": \
{1}+{2}/{3} ({4:.3}%, inner score: {5:.3})"
                        print((printstr.format(typenamecombprintable,
                              affected_undescribed, affected_decribed,
                              total, coverage,
                              typenamecombscore[typenamecombtuple])))
        typenamecombouterscore = calc_outerscore(typenamecombscore,
                                                 pereffect_totalaffected,
                                                 TYPENAMECOMBS_WEIGHT)
        if DEBUG_LEVEL >= 1 and not stopdebugprints:
            printstr = "Type name combination outer score: {0:.3}"
            print((printstr.format(typenamecombouterscore)))

        # Don't print anything after 1st iteration at 1st debugging
        # level
        if DEBUG_LEVEL == 1:
            stopdebugprints = True

        # Stage 2.2.2
        # Pick max score from outer scores of all grouping types
        maxouterscore = max(groupouterscore, categoryouterscore,
                            basetypeouterscore,
                            marketgroupwithvarsouterscore,
                            typenamecombouterscore)
        # Define lower limit for score, below which there will be
        # no winners
        if maxouterscore >= LOWEST_SCORE:
            # If scores are similar, priorities are:
            # category > group > name > market group > base type
            if maxouterscore == categoryouterscore:
                # Pick ID of category which has highest score among
                # other categories
                categorywinner = max(categoryscore, key=categoryscore.get)
                # Add it to the list of categories which describe
                # set of items
                describedbycategory.append(categorywinner)
                # Add all items described by winning category into
                # set of described items
                effect_describedtypes.update\
                (globalmap_categoryid_typeid[categorywinner])
                # Set 'describes' flag to avoid processing of this
                # category during following iterations
                effectmap_categoryid_typeid[categorywinner][1] = True
                if DEBUG_LEVEL >= 2:
                    printstr = "Category winner: {0}"
                    print((printstr.format(categorywinner)))
            elif maxouterscore == groupouterscore:
                groupwinner = max(groupscore, key=groupscore.get)
                describedbygroup.append(groupwinner)
                effect_describedtypes.update\
                (globalmap_groupid_typeid[groupwinner])
                effectmap_groupid_typeid[groupwinner][1] = True
                if DEBUG_LEVEL >= 2:
                    printstr = "Group winner: {0}"
                    print((printstr.format(groupwinner)))
            elif maxouterscore == typenamecombouterscore:
                typenamecombwinner = max(typenamecombscore,
                                         key=typenamecombscore.get)
                describedbytypenamecomb.append(typenamecombwinner)
                effect_describedtypes.update\
                (globalmap_typenamecombtuple_typeid[typenamecombwinner])
                effectmap_typenamecombtuple_typeid[typenamecombwinner]\
                [1] = True
                if DEBUG_LEVEL >= 2:
                    printstr = "Named like winner: {0}"
                    print((printstr.format(typenamecombwinner)))
            elif maxouterscore == marketgroupwithvarsouterscore:
                marketgroupwithvarswinner = max(marketgroupwithvarsscore,
                key=marketgroupwithvarsscore.get)
                describedbymarketgroupwithvars.append\
                (marketgroupwithvarswinner)
                effect_describedtypes.update\
                (globalmap_marketgroupid_typeidwithvariations
                 [marketgroupwithvarswinner])
                effectmap_marketgroupid_typeidwithvars\
                [marketgroupwithvarswinner][1] = True
                if DEBUG_LEVEL >= 2:
                    printstr = "Market group with variations winner: {0}"
                    print((printstr.format(marketgroupwithvarswinner)))
            elif maxouterscore == basetypeouterscore:
                basetypewinner = max(basetypescore, key=basetypescore.get)
                describedbybasetype.append(basetypewinner)
                effect_describedtypes.update\
                (globalmap_basetypeid_typeid[basetypewinner])
                effectmap_basetypeid_typeid[basetypewinner][1] = True
                if DEBUG_LEVEL >= 2:
                    printstr = "Base item winner: {0}"
                    print((printstr.format(basetypewinner)))
        # Stop if we have score less than some critical value,
        # all undescribed items will be provided as plain list
        else:
            iterate = False
            if DEBUG_LEVEL >= 2:
                print("No winners this iteration")
        # Also stop if we described all items
        if pereffectlist_usedbytypes.issubset(effect_describedtypes):
            iterate = False
        # Print separator for 2nd debugging level, to separate
        # debug data of one iteration from another
        if DEBUG_LEVEL >= 2:
            print("---")
    singleitems = set(pereffectlist_usedbytypes).difference\
    (effect_describedtypes)
    if DEBUG_LEVEL >= 1:
        print("Effect will be described by:")
        print(("Single item IDs:", singleitems))
        print(("Group IDs:", describedbygroup))
        print(("Category IDs:", describedbycategory))
        print(("Base item IDs:", describedbybasetype))
        print(("Market group with variations IDs:",
              describedbymarketgroupwithvars))
        print(("Type name combinations:", describedbytypenamecomb))

    # Stage 2.1
    # Read effect file and split it into lines
    effectfile = open(os.path.join(effects_path, effect_file), 'r')
    effectcontentssource = effectfile.read()
    effectfile.close()
    effectLines = effectcontentssource.split("\n")
    # Delete old comments from file contents
    numofcommentlines = 0
    for line in effectLines:
        if line:
            if line[0] == "#": numofcommentlines += 1
            else: break
        else: break
    for i in range(numofcommentlines):
        del effectLines[0]

    # These lists will contain IDs and some metadata in tuples
    printing_types = []
    printing_groups = []
    printing_categories = []
    printing_basetypes = []
    printing_marketgroupswithvars = []
    printing_typenamecombtuples = []

    # Gather data for printing in the form of tuples, each tuple has
    # grouping type ID, human-readable name and category name
    for typeid in singleitems:
        typename = ""
        cursor.execute(QUERY_TYPEID_TYPENAME, (typeid,))
        for row in cursor:
            typename = row[0]
        categoryname = ""
        cursor.execute(QUERY_CATEGORYID_CATEGORYNAME,
                       (globalmap_typeid_categoryid[typeid],))
        for row in cursor:
            categoryname = row[0]
        printing_types.append((typeid, typename, categoryname))
    for groupid in describedbygroup:
        groupName = ""
        cursor.execute(QUERY_GROUPID_GROUPNAME, (groupid,))
        for row in cursor:
            groupName = row[0]
        categoryid = 0
        cursor.execute(QUERY_GROUPID_CATEGORYID, (groupid,))
        for row in cursor:
            categoryid = row[0]
        categoryname = ""
        cursor.execute(QUERY_CATEGORYID_CATEGORYNAME, (categoryid,))
        for row in cursor:
            categoryname = row[0]
        printing_groups.append((groupid, groupName, categoryname))
    for categoryid in describedbycategory:
        categoryname = ""
        cursor.execute(QUERY_CATEGORYID_CATEGORYNAME, (categoryid,))
        for row in cursor:
            categoryname = row[0]
        printing_categories.append((categoryid, categoryname))
    for basetypeid in describedbybasetype:
        basetypename = ""
        cursor.execute(QUERY_TYPEID_TYPENAME, (basetypeid,))
        for row in cursor:
            basetypename = row[0]
        categoryname = ""
        cursor.execute(QUERY_CATEGORYID_CATEGORYNAME,
                       (globalmap_typeid_categoryid[basetypeid],))
        for row in cursor:
            categoryname = row[0]
        printing_basetypes.append((basetypeid, basetypename,
                                   categoryname))
    for marketgroupid in describedbymarketgroupwithvars:
        cursor.execute(QUERY_MARKETGROUPID_MARKETGROUPNAME,
                       (marketgroupid,))
        for row in cursor:
            marketgroupname = row[0]
        # Prepend market group name with its parents names
        prependparentid = marketgroupid
        # Limit depth to avoid looping, as usual
        for depth in range(20):
            cursor_parentmarket = db.cursor()
            cursor_parentmarket.execute(QUERY_MARKETGROUPID_PARENTGROUPID,
                                        (prependparentid,))
            for row in cursor_parentmarket:
                prependparentid = row[0]
            if prependparentid:
                cursor.execute(QUERY_MARKETGROUPID_MARKETGROUPNAME,
                               (prependparentid,))
                for row in cursor:
                    marketgroupname = "{0} > {1}".format(row[0],
                                                         marketgroupname)
            else:
                break
        printing_marketgroupswithvars.append((marketgroupid,
                                              marketgroupname))
    for typenamecombtuple in describedbytypenamecomb:
        typenamecombprint = " ".join(typenamecombtuple[0])
        categoryname = ""
        cursor.execute(QUERY_CATEGORYID_CATEGORYNAME,
                       (typenamecombtuple[1],))
        for row in cursor:
            categoryname = row[0]
        printing_typenamecombtuples.append((typenamecombtuple,
                                            typenamecombprint,
                                            categoryname))

    # Use separate list per grouping type to ease grouping type
    # sorting
    printing_typelines = []
    # Sort by item name first
    printing_types = sorted(printing_types, key=lambda tuple: tuple[1])
    # Then sort by category name
    printing_types = sorted(printing_types, key=lambda tuple: tuple[2])
    for type in printing_types:
        # Append line for printing to list
        catname = type[2]
        typename = type[1]
        printstr = "# {0}: {1}".format(catname, typename)
        if validate_string(printstr):
            printing_typelines.append(printstr)
    # Do the same for groups
    printing_grouplines = []
    printing_groups = sorted(printing_groups, key=lambda tuple: tuple[1])
    printing_groups = sorted(printing_groups, key=lambda tuple: tuple[2])
    for group in printing_groups:
        catname = group[2]
        groupname = group[1]
        described = len(effectmap_groupid_typeid[group[0]][0])
        total = len(globalmap_groupid_typeid[group[0]])
        printstr = "# {0}s from group: {1} ({2} of {3})".format(catname, groupname, described, total)
        if validate_string(printstr):
            printing_grouplines.append(printstr)
    # Process categories
    printing_categorylines = []
    printing_categories = sorted(printing_categories,
                                 key=lambda tuple: tuple[1])
    for category in printing_categories:
        catname = category[1]
        described = len(effectmap_categoryid_typeid[category[0]][0])
        total = len(globalmap_categoryid_typeid[category[0]])
        printstr = "# Items from category: {0} ({1} of {2})".format(catname, described, total)
        if validate_string(printstr):
            printing_categorylines.append(printstr)
    # Process variations
    printing_basetypelines = []
    printing_basetypes = sorted(printing_basetypes,
                                key=lambda tuple: tuple[1])
    printing_basetypes = sorted(printing_basetypes,
                                key=lambda tuple: tuple[2])
    for basetype in printing_basetypes:
        catname = basetype[2].lower()
        basename = basetype[1]
        described = len(effectmap_basetypeid_typeid[basetype[0]][0])
        total = len(globalmap_basetypeid_typeid[basetype[0]])
        printstr = "# Variations of {0}: {1} ({2} of {3})".format(catname, basename, described, total)
        if validate_string(printstr):
            printing_basetypelines.append(printstr)
    # Process market groups with variations
    printing_marketgroupwithvarslines = []
    printing_marketgroupswithvars = sorted(printing_marketgroupswithvars,
                                           key=lambda tuple: tuple[1])
    for marketgroup in printing_marketgroupswithvars:
        marketgroupname = marketgroup[1]
        described = len(effectmap_marketgroupid_typeidwithvars
                        [marketgroup[0]][0])
        total = len(globalmap_marketgroupid_typeidwithvariations
                    [marketgroup[0]])
        printstr = "# Items from market group: {0} ({1} of {2})".format(marketgroupname, described, total)
        if validate_string(printstr):
            printing_marketgroupwithvarslines.append(printstr)
    # Process type name combinations
    printing_typenamecombtuplelines = []
    printing_typenamecombtuples = sorted(printing_typenamecombtuples,
                                         key=lambda tuple: tuple[1])
    printing_typenamecombtuples = sorted(printing_typenamecombtuples,
                                         key=lambda tuple: tuple[2])
    for typenamecomb in printing_typenamecombtuples:
        catname = typenamecomb[2]
        namedlike = typenamecomb[1]
        described = len(effectmap_typenamecombtuple_typeid
                        [typenamecomb[0]][0])
        total = len(globalmap_typenamecombtuple_typeid[typenamecomb[0]])
        printstr = "# {0}s named like: {1} ({2} of {3})".format(catname, namedlike, described, total)
        if validate_string(printstr):
            printing_typenamecombtuplelines.append(printstr)

    # Compose single list of lines using custom sorting
    commentlines = printing_categorylines + printing_grouplines + \
    printing_typenamecombtuplelines + printing_marketgroupwithvarslines + \
    printing_basetypelines + printing_typelines
    # Prepend list with "used by"
    if commentlines:
        commentlines = ["# %s\n#\n# Used by:" % \
            globalmap_effectnameeos_effectnamedb[effect_name]]+commentlines
    # If effect isn't used, write it to file and to terminal
    else:
        commentlines = ["# Not used by any item"]
        if options.remove:
            print(("Warning: effect file " + effect_name +
              " is not used by any item, removing"))
            os.remove(os.path.join(effects_path, effect_file))
            continue
        else:
            print(("Warning: effect file " + effect_name +
              " is not used by any item"))
    # Combine "used by" comment lines and actual effect lines
    outputlines = commentlines + effectLines
    # Combine all lines into single string
    effectcontentsprocessed = "\n".join(outputlines)
    # If we're not debugging and contents actually changed - write
    # changes to the file
    if DEBUG_LEVEL == 0 and (effectcontentsprocessed !=
                             effectcontentssource):
        effectfile = open(os.path.join(effects_path, effect_file), 'w')
        effectfile.write(effectcontentsprocessed)
        effectfile.close()
    elif DEBUG_LEVEL >= 2:
        print("Comment to write to file:")
        print(("\n".join(commentlines)))
