#!/usr/bin/env python3

import copy
import os.path
import re
import sqlite3

script_dir = os.path.dirname(str(__file__, sys.getfilesystemencoding()))

# Connect to database and set up cursor
db = sqlite3.connect(os.path.join(script_dir, "..", "eve.db"))
cursor = db.cursor()

# Queries to get raw data
QUERY_ALLEFFECTS = 'SELECT effectID, effectName FROM dgmeffects'
# Limit categories to
# \Modules (7), Charges (8), Drones (18),
# Implants (20), Subsystems (32)
QUERY_PUBLISHEDTYPEIDS = 'SELECT it.typeID FROM invtypes AS it INNER JOIN \
invgroups AS ig ON it.groupID = ig.groupID INNER JOIN invcategories AS ic ON \
ig.categoryID = ic.categoryID WHERE it.published = 1 AND ic.categoryID IN \
(7, 8, 18, 20, 32)'
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
QUERY_TYPEID_ATTRIBS = 'SELECT da.attributeName, dta.value FROM dgmattribs AS \
da INNER JOIN dgmtypeattribs AS dta ON dta.attributeID = da.attributeID WHERE \
dta.typeID = ?'
QUERY_TYPEID_BASEATTRIBS = 'SELECT volume, mass, capacity FROM invtypes WHERE \
typeID = ?'
QUERY_TYPEID_METAGROUPID = 'SELECT metaGroupID FROM invmetatypes WHERE typeID = ?'
QUERY_METAGROUPNAME_METAGROUPID = 'SELECT metaGroupName FROM invmetagroups WHERE metaGroupID = ?'

# Compose list of effects w/o symbols which eos doesn't take into
# consideration, we'll use it to find proper effect IDs from file
# names
globalmap_effectnameeos_effectid = {}
STRIPSPEC = "[^A-Za-z0-9]"
cursor.execute(QUERY_ALLEFFECTS)
for row in cursor:
    effectid = row[0]
    effectnamedb = row[1]
    effectnameeos = re.sub(STRIPSPEC, "", effectnamedb)
    # There may be different effects with the same name, so form
    # sets of IDs
    if not effectnameeos in globalmap_effectnameeos_effectid:
        globalmap_effectnameeos_effectid[effectnameeos] = set()
    globalmap_effectnameeos_effectid[effectnameeos].add(effectid)

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


nonmarket = set()
for typeid in publishedtypes:
    if not typeid in globalmap_typeidwithvariations_marketgroupid:
        nonmarket.add(typeid)

def getItemAttrs(typeid):
    attrs = {}
    cursor.execute(QUERY_TYPEID_ATTRIBS, (typeid,))
    for row in cursor:
        attrs[row[0]] = row[1]
    cursor.execute(QUERY_TYPEID_BASEATTRIBS, (typeid,))
    for row in cursor:
        if row[0] is not None:
            attrs["volume"] = row[0]
        if row[1] is not None:
            attrs["mass"] = row[1]
        if row[2] is not None:
            attrs["capacity"] = row[2]
    return attrs

def suggestMktGrp(typeid, mode="grp"):
    typecat = globalmap_typeid_categoryid[typeid]
    catname = ""
    cursor.execute(QUERY_CATEGORYID_CATEGORYNAME, (typecat,))
    for row in cursor:
        catname = row[0]
    typename = ""
    cursor.execute(QUERY_TYPEID_TYPENAME, (typeid,))
    for row in cursor:
        typename = row[0]
    if catname.lower() == "module" and "civilian" in typename.lower():
        return 760
    attrs = getItemAttrs(typeid)
    implantness = None
    boosterness = None
    cpu = None
    power = None
    droneBandwidthUsed = None
    volume = None
    if "implantness" in attrs:
        implantness = attrs["implantness"]
    if "boosterness" in attrs:
        boosterness = attrs["boosterness"]
    if "cpu" in attrs:
        cpu = attrs["cpu"]
    if "power" in attrs:
        power = attrs["power"]
    if "droneBandwidthUsed" in attrs:
        droneBandwidthUsed = attrs["droneBandwidthUsed"]
    if "volume" in attrs:
        volume = attrs["volume"]
    if mode == "grp":
        grp = globalmap_typeid_groupid[typeid]
        comrades = globalmap_groupid_typeid[grp]
    elif mode == "cat":
        cat = globalmap_typeid_categoryid[typeid]
        comrades = globalmap_categoryid_typeid[cat]
    mktgrps_w_cos = {}
    for co in comrades:
        marketgroupid = 0
        cursor.execute(QUERY_TYPEID_MARKETGROUPID, (co,))
        for row in cursor:
            marketgroupid = row[0]
        if not marketgroupid:
            continue
        if not marketgroupid in mktgrps_w_cos:
            mktgrps_w_cos[marketgroupid] = 0.0
        similarity_factor = 1.0
        metagrp = 0
        cursor.execute(QUERY_TYPEID_METAGROUPID, (co,))
        for row in cursor:
            metagrp = row[0]
        if not metagrp in (0,1,2,14):
            similarity_factor *= 0.01
        if implantness or boosterness or cpu or power or droneBandwidthUsed or volume:
            cgrpattrs = getItemAttrs(co)
        if implantness:
            if "implantness" in cgrpattrs:
                if cgrpattrs["implantness"] != implantness:
                    similarity_factor *= 0.1
            else:
                similarity_factor *= 0.01
        if boosterness:
            if "boosterness" in cgrpattrs:
                if cgrpattrs["boosterness"] != boosterness:
                    similarity_factor *= 0.1
            else:
                similarity_factor *= 0.01
        if cpu:
            if "cpu" in cgrpattrs and cgrpattrs["cpu"]:
                    fct = cpu / cgrpattrs["cpu"]
                    if fct > 1:
                        fct = 1 / fct
                    similarity_factor *= fct
            else:
                similarity_factor *= 0.01
        if power:
            if "power" in cgrpattrs and cgrpattrs["power"]:
                fct = power / cgrpattrs["power"]
                if fct > 1:
                    fct = 1 / fct
                similarity_factor *= fct
            else:
                similarity_factor *= 0.01
        if droneBandwidthUsed:
            if "droneBandwidthUsed" in cgrpattrs:
                fct = droneBandwidthUsed / cgrpattrs["droneBandwidthUsed"]
                if fct > 1:
                    fct = 1 / fct
                similarity_factor *= fct
            else:
                similarity_factor *= 0.01
        if volume:
            if "volume" in cgrpattrs:
                fct = volume / cgrpattrs["volume"]
                if fct > 1:
                    fct = 1 / fct
                similarity_factor *= fct
            else:
                similarity_factor *= 0.01
        mktgrps_w_cos[marketgroupid] += similarity_factor
    if mktgrps_w_cos:
        winner = max(list(mktgrps_w_cos.keys()), key=lambda k: mktgrps_w_cos[k])
    else:
        winner = None
    return winner

def suggestMetaGrp(typeid):
    typename = ""
    cursor.execute(QUERY_TYPEID_TYPENAME, (typeid,))
    for row in cursor:
        typename = row[0]
    faction_affixes = ("Arch Angel", "Domination", "Blood", "Guristas", "Sansha", "Sanshas", "Shadow", "Guardian", "Serpentis",
                       "Caldari", "Imperial", "Gallente", "Federation", "Republic",
                       "Ammatar", "Khanid", "Thukker", "Syndicate", "Sisters", "Legion", "ORE",
                       "Nugoehuvi")
    deadspace_affixes = ("Gistii", "Gistum", "Gist",
                         "Corpii", "Corpum", "Corpus",
                         "Pithi", "Pithum", "Pith",
                         "Centii", "Centum", "Centus",
                         "Coreli", "Corelum", "Core")
    storyline_names = {"Akemon", "Michi", "Ogdin", "Pashan", "Shaqil", "Whelan Machorin", "Numon"}
    officer_names = ("Ahremen", "Brokara", "Brynn", "Chelm", "Cormack", "Draclira", "Estamel", "Gotan", "Hakim",
                     "Kaikka", "Mizuro", "Raysere", "Selynne", "Setele", "Tairei", "Thon", "Tuvan", "Vizan")
    storyline_pattern_general = "'[A-Za-z ]+'"
    storyline_pattern_names = "|".join("{0}".format(name) for name in storyline_names)
    faction_pattern = "({0}) ".format("|".join(faction_affixes))
    deadspace_pattern = "({0}) ".format("|".join(deadspace_affixes))
    officer_pattern = "({0}) ".format("|".join("{0}'s".format(name) for name in officer_names))

    attrs = getItemAttrs(typeid)
    if attrs.get("metaLevel") is not None:
        mlvl = attrs["metaLevel"]
        if mlvl in (0, 1, 2, 3, 4):
            meta = 1
        elif mlvl == 5:
            meta = 2
        elif mlvl in (6, 7):
            meta = 3
        elif mlvl in (8, 9):
            meta = 4
        elif mlvl in (11, 12, 13, 14):
            if re.search(deadspace_pattern, typename):
                meta = 6
            else:
                meta = 5
        else:
            meta = 1
    elif re.search(officer_pattern, typename):
        meta = 5
    elif re.search(deadspace_pattern, typename):
        meta = 6
    elif re.search(faction_pattern, typename):
        meta = 4
    elif re.search(storyline_pattern_names, typename):
        meta = 3
    elif re.search(storyline_pattern_general, typename) and not "Hardwiring" in typename:
        meta = 3
    else:
        meta = 1

    return meta


map_typeid_stuff = {}
map_typeid_stuff2 = {}

for typeid in nonmarket:
    typename = ""
    cursor.execute(QUERY_TYPEID_TYPENAME, (typeid,))
    for row in cursor:
        typename = row[0]
    grpname = ""
    cursor.execute(QUERY_GROUPID_GROUPNAME, (globalmap_typeid_groupid[typeid],))
    for row in cursor:
        grpname = row[0]
    mkt = suggestMktGrp(typeid)
    if mkt is None:
        mkt = suggestMktGrp(typeid, mode="cat")
    meta = suggestMetaGrp(typeid)
    attrs = getItemAttrs(typeid)
    if mkt:
        map_typeid_stuff[typeid] = (mkt, meta)
        marketgroupname = ""
        cursor.execute(QUERY_MARKETGROUPID_MARKETGROUPNAME,
                       (mkt,))
        for row in cursor:
            marketgroupname = row[0]
        # Prepend market group name with its parents names
        prependparentid = mkt
        # Limit depth to avoid looping, as usual
        for depth in range(20):
            cursor_parentmarket = db.cursor()
            cursor_parentmarket.execute(QUERY_MARKETGROUPID_PARENTGROUPID,
                                        (prependparentid,))
            for row in cursor_parentmarket:
                prependparentid = row[0]
            if prependparentid:
                cursor_parentmarket2 = db.cursor()
                cursor_parentmarket2.execute(QUERY_MARKETGROUPID_MARKETGROUPNAME,
                               (prependparentid,))
                for row in cursor_parentmarket2:
                    marketgroupname = "{0} > {1}".format(row[0],
                                                         marketgroupname)
            else:
                break
    else:
        marketgroupname = "None"

    map_typeid_stuff2[typename] = (mkt, marketgroupname)


    metagroupname = ""
    cursor.execute(QUERY_METAGROUPNAME_METAGROUPID,
                   (meta,))
    for row in cursor:
        metagroupname = row[0]

    #print("---\nItem: {0}\nGroup: {1}\nSuggested market group: {2} ({3})\nMeta group: {4}".format(typename, grpname, marketgroupname, mkt, metagroupname))

#print("\n\nmap = {{ {0} }}".format(", ".join("{0}: ({1}, {2})".format(key, map_typeid_stuff[key][0], map_typeid_stuff[key][1]) for key in sorted(map_typeid_stuff))))
print(("---\n{0}".format("\n".join("\"{0}\": {1}, # {2}".format(key, map_typeid_stuff2[key][0], map_typeid_stuff2[key][1]) for key in sorted(map_typeid_stuff2)))))
