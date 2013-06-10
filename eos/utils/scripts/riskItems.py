"""
This is ugly, tricky and unreadable script which helps to detect which items should be tested,
based on how its current effects work.
"""
import sqlite3
import os.path
import copy
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--database", help="path to eve cache data dump in \
sqlite format, default eos database path is used if none specified",
type="string", default=os.path.join("~", ".pyfa","eve.db"))
parser.add_option("-a", "--attr", help="find items with all of these attributes",
type="string", default="")
parser.add_option("-s", "--srq", help="find items with any of these skill requirements",
type="string", default="")
parser.add_option("-g", "--grp", help="find items from any of these groups",
type="string", default="")
parser.add_option("-z", "--nozero", action="store_true", help="ignore attributes with zero values",
default=False)
parser.add_option("-o", "--noone", action="store_true", help="ignore attributes with value equal to 1",
default=False)
parser.add_option("-t", "--tech12", action="store_true", help="show only t12 items (with exception for items with no t1 variations)",
default=False)
(options, args) = parser.parse_args()

if not options.attr:
    import sys

    sys.stderr.write("You need to specify an attribute name.\n")
    sys.exit()

# Connect to database and set up cursor
db = sqlite3.connect(os.path.expanduser(options.database))
cursor = db.cursor()

# As we don't rely on eos's overrides, we need to set them manually
OVERRIDES = '''
UPDATE invtypes SET published = '1' WHERE typeName = 'Freki';
UPDATE invtypes SET published = '1' WHERE typeName = 'Mimir';
UPDATE invtypes SET published = '1' WHERE typeName = 'Utu';
UPDATE invtypes SET published = '1' WHERE typeName = 'Adrestia';
'''
for statement in OVERRIDES.split(";\n"):
    cursor.execute(statement)

# Queries to get raw data
# Limit categories to Celestials (2, only for wormhole effects),
# Ships (6), Modules (7), Charges (8), Skills (16), Drones (18),
# Implants (20), Subsystems (32)
QUERY_PUBLISHEDTYPEIDS = 'SELECT it.typeID FROM invtypes AS it INNER JOIN \
invgroups AS ig ON it.groupID = ig.groupID INNER JOIN invcategories AS ic ON \
ig.categoryID = ic.categoryID WHERE it.published = 1 AND ic.categoryID IN \
(2, 6, 7, 8, 16, 18, 20, 32)'
QUERY_ATTRIBUTEID_TYPEID = "SELECT it.typeID, dta.value FROM invtypes AS it INNER JOIN \
dgmtypeattribs AS dta ON it.typeID = dta.typeID INNER JOIN dgmattribs AS da \
ON dta.attributeID = da.attributeID WHERE da.attributeID = ?"
QUERY_TYPEID_GROUPID = 'SELECT groupID FROM invtypes WHERE typeID = ? LIMIT 1'
QUERY_GROUPID_CATEGORYID = 'SELECT categoryID FROM invgroups WHERE \
groupID = ? LIMIT 1'
QUERY_TYPEID_PARENTTYPEID = 'SELECT parentTypeID FROM invmetatypes WHERE \
typeID = ? LIMIT 1'
QUERY_TYPEID_METAGROUPID = 'SELECT metaGroupID FROM invmetatypes WHERE \
typeID = ? LIMIT 1'
QUERY_TYPEID_SKILLRQ = 'SELECT dta.value FROM dgmtypeattribs AS dta INNER JOIN \
dgmattribs AS da ON da.attributeID = dta.attributeID WHERE (da.attributeName = \
"requiredSkill1" OR da.attributeName = "requiredSkill2" OR da.attributeName = \
"requiredSkill3") AND dta.typeID = ?'
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

QUERY_ATTRIBUTENAME_ATTRIBUTEID = 'SELECT attributeID FROM dgmattribs WHERE attributeName = ?'
QUERY_TYPENAME_TYPEID = 'SELECT typeID FROM invtypes WHERE typeName = ?'
QUERY_GROUPNAME_GROUPID = 'SELECT groupID FROM invgroups WHERE groupName = ?'

if options.srq:
    global_skillrqids = set()
    for srq in options.srq.split(","):
        srqid = 0
        cursor.execute(QUERY_TYPENAME_TYPEID, (srq,))
        for row in cursor:
            srqid = row[0]
        if not srqid:
            import sys
            sys.stderr.write("You need to specify proper skill requirement name.\n")
            sys.exit()
        else:
            global_skillrqids.add(srqid)

if options.grp:
    global_groupids = set()
    for grp in options.grp.split(","):
        grouplist = []
        cursor.execute(QUERY_GROUPNAME_GROUPID, (grp,))
        for row in cursor:
            grouplist.append(row[0])
        if len(grouplist) > 1:
            print("Warning: multiple groups found, using ID", grouplist[0])
        elif len(grouplist) == 0:
            import sys
            sys.stderr.write("You need to specify proper group name.\n")
            sys.exit()
        global_groupids.add(grouplist[0])

# Published types set
publishedtypes = set()
cursor.execute(QUERY_PUBLISHEDTYPEIDS)
for row in cursor:
    publishedtypes.add(row[0])

# We'll use list of items with given attributes as base for any operations
# Term item means item with given attribute
typeswithattr = set()
first = True
for attr in options.attr.split(","):
    tmp = set()
    cursor.execute(QUERY_ATTRIBUTENAME_ATTRIBUTEID, (attr,))
    noattr = True
    for row in cursor:
        noattr = False
        attrid = row[0]
    if noattr:
        import sys
        sys.stderr.write("No \"{0}\" attribute found.\n".format(attr))
        sys.exit()
    cursor.execute(QUERY_ATTRIBUTEID_TYPEID, (attrid,))
    for row in cursor:
        if options.nozero:
            if row[0] in publishedtypes and row[1] not in (None, 0, 0.0):
                tmp.add(row[0])
        elif options.noone:
            if row[0] in publishedtypes and row[1] != 1.0:
                tmp.add(row[0])
        else:
            if row[0] in publishedtypes:
                tmp.add(row[0])
    if first:
        first = False
        typeswithattr = copy.deepcopy(tmp)
    else:
        typeswithattr.intersection_update(tmp)
if len(typeswithattr) == 0:
        import sys
        sys.stderr.write("No items found with all of supplied attributes.\n")
        sys.exit()

# Base type maps
# { basetypeid : set(typeid) }
map_basetypeid_typeid =  {}
# { typeid : basetypeid }
map_typeid_basetypeid =  {}
for typeid in typeswithattr:
    # Not all typeIDs in the database have baseTypeID, so assign some
    # default value to it
    basetypeid = 0
    cursor.execute(QUERY_TYPEID_PARENTTYPEID, (typeid,))
    for row in cursor:
        basetypeid = row[0]
    # If base type is not published or is not set in database, consider
    # item as variation of self
    if basetypeid not in typeswithattr:
        basetypeid = typeid
    if not basetypeid in map_basetypeid_typeid:
        map_basetypeid_typeid[basetypeid] = set()
    map_basetypeid_typeid[basetypeid].add(typeid)
    map_typeid_basetypeid[typeid] = basetypeid

# Meta group maps
# { metagroupid : set(typeid) }
map_metagroupid_typeid =  {}
# { typeid : metagroupid }
map_typeid_metagroupid =  {}
for typeid in typeswithattr:
    # Assume items are tech 1 by default
    metagroupid = 1
    cursor.execute(QUERY_TYPEID_METAGROUPID, (typeid,))
    for row in cursor:
        metagroupid = row[0]
    if not metagroupid in map_metagroupid_typeid:
        map_metagroupid_typeid[metagroupid] = set()
    map_metagroupid_typeid[metagroupid].add(typeid)
    map_typeid_metagroupid[typeid] = metagroupid

# Filter out non-t1/t2 items if we're asked to do so
if options.tech12:
    toremove = set()
    for typeid in typeswithattr:
        if map_typeid_basetypeid[typeid] != typeid and map_typeid_metagroupid[typeid] != 2:
            toremove.add(typeid)
    for id in toremove:
        typeswithattr.remove(id)

print("Attributes:")
for attr in sorted(options.attr.split(",")):
    print(attr)
print("")

# Compose group maps
# { groupid : set(typeid) }
map_groupid_typeid = {}
# { typeid : groupid }
map_typeid_groupid = {}
for typeid in typeswithattr:
    groupid = 0
    cursor.execute(QUERY_TYPEID_GROUPID, (typeid,))
    for row in cursor:
        groupid = row[0]
    if not groupid in map_groupid_typeid:
        map_groupid_typeid[groupid] = set()
    map_groupid_typeid[groupid].add(typeid)
    map_typeid_groupid[typeid] = groupid

# Category maps
# { categoryid : set(typeid) }
map_categoryid_typeid =  {}
# { typeid : categoryid }
map_typeid_categoryid =  {}
for typeid in typeswithattr:
    categoryid = 0
    cursor.execute(QUERY_GROUPID_CATEGORYID,
                   (map_typeid_groupid[typeid],))
    for row in cursor:
        categoryid = row[0]
    if not categoryid in map_categoryid_typeid:
        map_categoryid_typeid[categoryid] = set()
    map_categoryid_typeid[categoryid].add(typeid)
    map_typeid_categoryid[typeid] = categoryid
# { categoryid : set(groupid) }
map_categoryid_groupid =  {}
# { groupid : categoryid }
map_groupid_categoryid =  {}
for groupid in map_groupid_typeid:
    categoryid = 0
    cursor.execute(QUERY_GROUPID_CATEGORYID,
                   (groupid,))
    for row in cursor:
        categoryid = row[0]
    if not categoryid in map_categoryid_groupid:
        map_categoryid_groupid[categoryid] = set()
    map_categoryid_groupid[categoryid].add(groupid)
    map_groupid_categoryid[groupid] = categoryid

# Skill required maps
# { skillid : set(typeid) }
map_skillrq_typeid =  {}
# { typeid : set(skillid) }
map_typeid_skillrq =  {}
# list of items without skill requirements
set_typeid_noskillrq = set()
for typeid in typeswithattr:
    map_typeid_skillrq[typeid] = set()
    cursor.execute(QUERY_TYPEID_SKILLRQ, (typeid,))
    no_rqs = True
    for row in cursor:
        no_rqs = False
        skillid = row[0]
        if not skillid in map_skillrq_typeid:
            map_skillrq_typeid[skillid] = set()
        map_skillrq_typeid[skillid].add(typeid)
        map_typeid_skillrq[typeid].add(skillid)
    if no_rqs:
        set_typeid_noskillrq.add(typeid)

def gettypename(typeid):
    typename = ""
    cursor.execute(QUERY_TYPEID_TYPENAME, (typeid,))
    for row in cursor:
        typename = row[0]
    return typename

def getgroupname(grpid):
    grpname = ""
    cursor.execute(QUERY_GROUPID_GROUPNAME, (grpid,))
    for row in cursor:
        grpname = row[0]
    return grpname

def getcatname(catid):
    catname = ""
    cursor.execute(QUERY_CATEGORYID_CATEGORYNAME, (catid,))
    for row in cursor:
        catname = row[0]
    return catname

if options.grp and options.srq:
    # Set of items which are supposed to be affected
    targetitems = set()
    for groupid in global_groupids:
        for srqid in global_skillrqids:
            if groupid in map_groupid_typeid and srqid in map_skillrq_typeid:
                targetitems.update(map_groupid_typeid[groupid].intersection(map_skillrq_typeid[srqid]))
    targetitems_noskillrqs = targetitems.intersection(set_typeid_noskillrq)
    # All skill requirements of items which are supposed to be affected
    targetitems_skillrqs = set()
    for itemid in targetitems:
        targetitems_skillrqs.update(map_typeid_skillrq[itemid])
    # Remove skill requirement supplied as argument to script
    # we can use that argument when needed manually, and it
    # covers all targetitems which we don't want to do with single skill
    for srqid in global_skillrqids:
        targetitems_skillrqs.remove(srqid)

    if targetitems:
        # Print items which are supposed to be affected
        print("Affected items:")
        for groupid in sorted(global_groupids, key=lambda grid: getgroupname(grid)):
            targetitems_grp = targetitems.intersection(map_groupid_typeid[groupid])
            print("    Items from {0} group:".format(getgroupname(groupid)))
            # Cycle through all required skills
            targetitems_skillrqs_withgiven = copy.deepcopy(targetitems_skillrqs)
            for srqid in global_skillrqids:
                targetitems_skillrqs_withgiven.add(srqid)
            for skillrq in sorted(targetitems_skillrqs_withgiven, key=lambda sk: gettypename(sk)):
                targetitems_grp_srq = targetitems_grp.intersection(map_skillrq_typeid[skillrq])
                if targetitems_grp_srq:
                    print("        Items requiring {0} skill:".format(gettypename(skillrq)))
                    for item in sorted(targetitems_grp_srq, key=lambda item: gettypename(item)):
                        # If item has 3rd skill requirement (besides supplied as argument and
                        # included into header of current section), mention it
                        if len(map_typeid_skillrq[item]) in (2, 3):
                            otherskillrq = copy.deepcopy(map_typeid_skillrq[item])
                            otherskillrq.discard(skillrq)
                            print("            {0} ({1})".format(gettypename(item), ", ".join(sorted(gettypename(id) for id in otherskillrq))))
                        # Just print item names if there's only 1 skill requirement
                        elif len(map_typeid_skillrq[item]) == 1:
                            print("            {0}".format(gettypename(item)))
                        else:
                            print("WARNING: Bad things happened, we never should get here")

    print("\nUnaffected items")


    items_in_groups = set()
    for groupid in global_groupids:
        items_in_groups.update(map_groupid_typeid[groupid])
    items_with_skillrqs = set()
    for srqid in global_skillrqids:
        items_with_skillrqs.update(map_skillrq_typeid[srqid])
    # List items which do not belong to given group, but have given skill requirement
    wskill = typeswithattr.intersection(items_with_skillrqs)
    wogroup = typeswithattr.difference(items_in_groups)
    nontarget_wskill_wogroup = wskill.intersection(wogroup)
    if nontarget_wskill_wogroup:
        print("    With {0} skill requirements, not belonging to {1} groups:".format(", ".join(sorted(gettypename(id) for id in global_skillrqids)), ", ".join(sorted(getgroupname(grid) for grid in global_groupids))))
    for item in sorted(nontarget_wskill_wogroup, key=lambda item: gettypename(item)):
        print("        {0}".format(gettypename(item)))

    # List items which belong to given group, but do not have given skill requirement
    woskill = typeswithattr.difference(items_with_skillrqs)
    wgroup = typeswithattr.intersection(items_in_groups)
    nontarget_woskill_wgroup = woskill.intersection(wgroup)
    if nontarget_woskill_wgroup:
        print("    Without {0} skill requirement, belonging to {1} group:".format(", ".join(sorted(gettypename(id) for id in global_skillrqids)), ", ".join(sorted(getgroupname(grid) for grid in global_groupids))))
    for item in sorted(nontarget_woskill_wgroup, key=lambda item: gettypename(item)):
        print("        {0}".format(gettypename(item)))

    # If any of the above lists is missing, list all unaffected items
    if not nontarget_wskill_wogroup or not nontarget_woskill_wgroup:
        nontarget = typeswithattr.difference(items_in_groups)
        for srqid in global_skillrqids:
            nontarget.difference_update(map_skillrq_typeid[srqid])
        if nontarget_wskill_wogroup:
            nontarget.difference_update(nontarget_wskill_wogroup)
        if nontarget_woskill_wgroup:
            nontarget.difference_update(nontarget_woskill_wgroup)
        nontarget_groups = set()
        nontarget_cats = set()
        print("    Plain list:")
        for item in sorted(nontarget, key=lambda item: gettypename(item)):
            nontarget_groups.add(map_typeid_groupid[item])
            print("        {0} ({1})".format(gettypename(item), getgroupname(map_typeid_groupid[item])))
        #print("  Groups:")
        #for group in sorted(nontarget_groups, key=lambda grp: getgroupname(grp)):
        #    nontarget_cats.add(map_groupid_categoryid[group])
        #    print("    {0} ({1})".format(getgroupname(group), getcatname(map_groupid_categoryid[group])))
        #print("  Categories:")
        #for cat in sorted(nontarget_cats, key=lambda cat: getcatname(cat)):
        #    print("    {0}".format(getcatname(cat)))

elif options.grp:
    # Set of items which are supposed to be affected
    targetitems = set()
    for groupid in global_groupids:
        if groupid in map_groupid_typeid:
            targetitems.update(map_groupid_typeid[groupid])
    # All skill requirements of items which are supposed to be affected
    targetitems_skillrqs = set()
    for itemid in targetitems:
        targetitems_skillrqs.update(map_typeid_skillrq[itemid])
    targetitems_noskillrqs = targetitems.intersection(set_typeid_noskillrq)
    if targetitems:
        # Print items which are supposed to be affected
        print("Affected items:")
        for groupid in sorted(global_groupids, key=lambda grid: getgroupname(grid)):
            print("    From {0} group:".format(getgroupname(groupid)))
            targetitems_grp = targetitems.intersection(map_groupid_typeid[groupid])
            targetitems_noskillrqs_grp = targetitems_noskillrqs.intersection(map_groupid_typeid[groupid])
            # Cycle through all required skills
            for skillrq in sorted(targetitems_skillrqs, key=lambda sk: gettypename(sk)):
                items_grpsrq = targetitems_grp.intersection(map_skillrq_typeid[skillrq])
                if items_grpsrq:
                    print("        Requiring {0} skill:".format(gettypename(skillrq)))
                    for item in sorted(items_grpsrq, key=lambda item: gettypename(item)):
                        # If item has other skill requirements, print them
                        if len(map_typeid_skillrq[item]) == 3 or len(map_typeid_skillrq[item]) == 2:
                            otherskillrq = copy.deepcopy(map_typeid_skillrq[item])
                            otherskillrq.discard(skillrq)
                            print("            {0} ({1})".format(gettypename(item), ", ".join(sorted(gettypename(id) for id in otherskillrq))))
                        # Just print item names if there're only 2 skill requirements
                        elif len(map_typeid_skillrq[item]) == 1:
                            print("            {0}".format(gettypename(item)))
                        else:
                            print("WARNING: Bad things happened, we never should get here")
            if targetitems_noskillrqs:
                print("        Requiring no skills:")
                for item in sorted(targetitems_noskillrqs_grp, key=lambda item: gettypename(item)):
                    print("            {0}".format(gettypename(item)))

    print("\nUnaffected items")

    # List items which are supposed to be unaffected
    nontarget = typeswithattr.difference(targetitems)
    nontarget_groups = set()
    nontarget_cats = set()
    print("    Not belonging to groups {0}:".format(", ".join(getgroupname(id) for id in global_groupids)))

    removeitms = set()
    # Check 1 unaffected item with each skill requirement, if some items with it were affected
    for skillrq in sorted(targetitems_skillrqs, key=lambda srq: gettypename(srq)):
        if nontarget.intersection(map_skillrq_typeid[skillrq]):
            print("        With {0} skill requirement:".format(gettypename(skillrq)))
        for item in sorted(nontarget.intersection(map_skillrq_typeid[skillrq]), key=lambda item: gettypename(item)):
            print("            {0}".format(gettypename(item)))
        removeitms.update(map_skillrq_typeid[skillrq])
    nontarget.difference_update(removeitms)
    print("        With other or no skill requirements:")
    for item in sorted(nontarget, key=lambda item: gettypename(item)):
        nontarget_groups.add(map_typeid_groupid[item])
        print("            {0} ({1})".format(gettypename(item), getgroupname(map_typeid_groupid[item])))

    #print("    Groups:")
    #for group in sorted(nontarget_groups, key=lambda grp: getgroupname(grp)):
    #    nontarget_cats.add(map_groupid_categoryid[group])
    #    print("      {0} ({1})".format(getgroupname(group), getcatname(map_groupid_categoryid[group])))
    #print("    Categories:")
    #for cat in sorted(nontarget_cats, key=lambda cat: getcatname(cat)):
    #    print("      {0}".format(getcatname(cat)))

elif options.srq:
    # Set of items which are supposed to be affected
    targetitems = set()
    for srqid in global_skillrqids:
        if srqid in map_skillrq_typeid:
            targetitems.update(map_skillrq_typeid[srqid])

    # All groups of items which are supposed to be affected
    targetitems_groups = set()
    targetitems_srqs = set()
    targetitems_cats = set()
    for itemid in targetitems:
        targetitems_groups.add(map_typeid_groupid[itemid])
        targetitems_srqs.update(map_typeid_skillrq[itemid])
        targetitems_cats.add(map_typeid_categoryid[itemid])
    if targetitems:
        # Print items which are supposed to be affected
        print("Affected items:")
        for srqid in sorted(global_skillrqids, key=lambda itm: gettypename(itm)):
            print("    With {0} skill requirements:".format(gettypename(srqid)))
            targetitems_srq = targetitems.intersection(map_skillrq_typeid[srqid])
            targetitems_srq_groups = set()
            targetitems_srq_cats = set()
            for itemid in targetitems_srq:
                targetitems_srq_groups.add(map_typeid_groupid[itemid])
                targetitems_srq_cats.add(map_typeid_categoryid[itemid])
            # Cycle through groups
            for groupid in sorted(targetitems_srq_groups, key=lambda grp: getgroupname(grp)):
                print("        From {0} group:".format(getgroupname(groupid)))
                for item in sorted(targetitems_srq.intersection(map_groupid_typeid[groupid]), key=lambda item: gettypename(item)):
                    print("            {0} ({1})".format(gettypename(item), ", ".join(sorted(gettypename(itm) for itm in map_typeid_skillrq[item].difference(global_skillrqids))) or "None"))

    print("\nUnaffected items")

    # List items which are supposed to be unaffected
    nontarget = typeswithattr.difference(targetitems)
    nontarget_groups = set()
    nontarget_cats = set()
    print("    Without {0} skills requirement:".format(", ".join(gettypename(id) for id in global_skillrqids)))
    removeitms = set()
    # Check 1 unaffected item from each group where some items were affected
    for groupid in sorted(targetitems_groups, key=lambda grp: getgroupname(grp)):
        if nontarget.intersection(map_groupid_typeid[groupid]):
            print("        From {0} group:".format(getgroupname(groupid)))
            for skillrqid in sorted(targetitems_srqs.difference(global_skillrqids), key=lambda srq: gettypename(srq)):
                itmset = nontarget.intersection(map_groupid_typeid[groupid]).intersection(map_skillrq_typeid[skillrqid])
                if itmset:
                    print("            Items with {0} skill requirement:".format(gettypename(skillrqid)))
                    for item in sorted(itmset, key=lambda itm: gettypename(itm)):
                        otherskrqs = map_typeid_skillrq[item].difference(global_skillrqids)
                        otherskrqs.remove(skillrqid)
                        print("                {0} ({1})".format(gettypename(item), ", ".join(sorted(gettypename(itm) for itm in otherskrqs)) or "None"))
                    removeitms.update(itmset)
            nontarget.difference_update(removeitms)
            otsk = nontarget.intersection(map_groupid_typeid[groupid]).difference(set_typeid_noskillrq)
            if otsk:
                print("            Items with other skill requirements:")
                for item in sorted(otsk, key=lambda itm: gettypename(itm)):
                    print("                {0} (None)".format(gettypename(item)))
            removeitms.update(otsk)
            nosk = nontarget.intersection(map_groupid_typeid[groupid]).intersection(set_typeid_noskillrq)
            if nosk:
                print("            Items with no skill requirement:")
                for item in sorted(nosk, key=lambda itm: gettypename(itm)):
                    print("                {0} (None)".format(gettypename(item)))
            removeitms.update(nosk)
    nontarget.difference_update(removeitms)
    for catid in sorted(targetitems_cats, key=lambda cat: getcatname(cat)):
        if nontarget.intersection(map_categoryid_typeid[catid]):
            print("        From {0} category:".format(getcatname(catid)))
        for item in sorted(nontarget.intersection(map_categoryid_typeid[catid]), key=lambda item: gettypename(item)):
            print("            {0}".format(gettypename(item)))
        removeitms.update(map_categoryid_typeid[catid])
    nontarget.difference_update(removeitms)
    if nontarget:
        # Check any other unaffected item
        print("        Remaining items:")
        for item in sorted(nontarget, key=lambda item: gettypename(item)):
            nontarget_groups.add(map_typeid_groupid[item])
            print("            {0} ({1})".format(gettypename(item), getgroupname(map_typeid_groupid[item])))
    #print("    Groups:")
    #for group in sorted(nontarget_groups, key=lambda grp: getgroupname(grp)):
    #    nontarget_cats.add(map_groupid_categoryid[group])
    #    print("      {0} ({1})".format(getgroupname(group), getcatname(map_groupid_categoryid[group])))
    #print("    Categories:")
    #for cat in sorted(nontarget_cats, key=lambda cat: getcatname(cat)):
    #    print("      {0}".format(getcatname(cat)))

else:
    print("Affected items")
    targetitems = typeswithattr
    targetitems_groups = set()
    targetitems_cats = set()
    print("    Assumed set of items:")
    for item in sorted(targetitems, key=lambda item: gettypename(item)):
        targetitems_groups.add(map_typeid_groupid[item])
        print("        {0} ({1})".format(gettypename(item), getgroupname(map_typeid_groupid[item])))
    print("    Groups:")
    for group in sorted(targetitems_groups, key=lambda grp: getgroupname(grp)):
        targetitems_cats.add(map_groupid_categoryid[group])
        print("        {0} ({1})".format(getgroupname(group), getcatname(map_groupid_categoryid[group])))
    print("    Categories:")
    for cat in sorted(targetitems_cats, key=lambda cat: getcatname(cat)):
        print("        {0}".format(getcatname(cat)))
