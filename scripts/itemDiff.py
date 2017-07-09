#!/usr/bin/env python3
#===============================================================================
# Copyright (C) 2010-2011 Anton Vorobyov
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================


'''
This script is used to compare two different database versions.
It shows removed/changed/new items with list of changed effects,
changed attributes and effects which were renamed
'''

import argparse
import os.path
import re
import sqlite3
import sys

script_dir = os.path.dirname(__file__)
default_old = os.path.join(script_dir, "..", "eve.db")

def main(old, new, groups=True, effects=True, attributes=True, renames=True):
    # Open both databases and get their cursors
    old_db = sqlite3.connect(os.path.expanduser(old))
    old_cursor = old_db.cursor()
    new_db = sqlite3.connect(os.path.expanduser(new))
    new_cursor = new_db.cursor()

    # Force some of the items to make them published
    FORCEPUB_TYPES = ("Ibis", "Impairor", "Velator", "Reaper",
    "Amarr Tactical Destroyer Propulsion Mode",
    "Amarr Tactical Destroyer Sharpshooter Mode",
    "Amarr Tactical Destroyer Defense Mode")
    OVERRIDES_TYPEPUB = 'UPDATE invtypes SET published = 1 WHERE typeName = ?'
    for typename in FORCEPUB_TYPES:
        old_cursor.execute(OVERRIDES_TYPEPUB, (typename,))
        new_cursor.execute(OVERRIDES_TYPEPUB, (typename,))

    # Initialization of few things used by both changed/renamed effects list
    script_dir = os.path.dirname(__file__)
    effectspath = os.path.join(script_dir, "..", "eos", "effects")
    implemented = set()

    for filename in os.listdir(effectspath):
        basename, extension = filename.rsplit('.', 1)
        # Ignore non-py files and exclude implementation-specific 'effect'
        if extension == "py" and basename not in ("__init__",):
            implemented.add(basename)

    # Effects' names are used w/o any special symbols by eos
    stripspec = "[^A-Za-z0-9]"

    # Method to get data if effect is implemented in eos or not
    def geteffst(effectname):
        eosname = re.sub(stripspec, "", effectname).lower()
        if eosname in implemented:
            impstate = True
        else:
            impstate = False
        return impstate

    def findrenames(ren_dict, query, strip=False):

        old_namedata = {}
        new_namedata = {}

        for cursor, dictionary in ((old_cursor, old_namedata), (new_cursor, new_namedata)):
            cursor.execute(query)
            for row in cursor:
                id = row[0]
                name = row[1]
                if strip is True:
                    name = re.sub(stripspec, "", name)
                dictionary[id] = name

        for id in set(old_namedata.keys()).intersection(new_namedata.keys()):
            oldname = old_namedata[id]
            newname = new_namedata[id]
            if oldname != newname:
                ren_dict[id] = (oldname, newname)
        return

    def printrenames(ren_dict, title, implementedtag=False):
        if len(ren_dict) > 0:
            print('\nRenamed ' + title + ':')
            for id in sorted(ren_dict):
                couple = ren_dict[id]
                if implementedtag:
                    print("\n[{0}] \"{1}\"\n[{2}] \"{3}\"".format(geteffst(couple[0]), couple[0], geteffst(couple[1]), couple[1]))
                else:
                    print("    \"{0}\": \"{1}\",".format(couple[0].encode('utf-8'), couple[1].encode('utf-8')))

    groupcats = {}
    def getgroupcat(grp):
        """Get group category from the new db"""
        if grp in groupcats:
            cat = groupcats[grp]
        else:
            query = 'SELECT categoryID FROM invgroups WHERE groupID = ?'
            new_cursor.execute(query, (grp,))
            cat = 0
            for row in new_cursor:
                cat = row[0]
            groupcats[grp] = cat
        return cat

    itemnames = {}
    def getitemname(item):
        """Get item name from the new db"""
        if item in itemnames:
            name = itemnames[item]
        else:
            query = 'SELECT typeName FROM invtypes WHERE typeID = ?'
            new_cursor.execute(query, (item,))
            name = ""
            for row in new_cursor:
                name = row[0]
            if not name:
                old_cursor.execute(query, (item,))
                for row in old_cursor:
                    name = row[0]
            itemnames[item] = name
        return name

    groupnames = {}
    def getgroupname(grp):
        """Get group name from the new db"""
        if grp in groupnames:
            name = groupnames[grp]
        else:
            query = 'SELECT groupName FROM invgroups WHERE groupID = ?'
            new_cursor.execute(query, (grp,))
            name = ""
            for row in new_cursor:
                name = row[0]
            if not name:
                old_cursor.execute(query, (grp,))
                for row in old_cursor:
                    name = row[0]
            groupnames[grp] = name
        return name

    effectnames = {}
    def geteffectname(effect):
        """Get effect name from the new db"""
        if effect in effectnames:
            name = effectnames[effect]
        else:
            query = 'SELECT effectName FROM dgmeffects WHERE effectID = ?'
            new_cursor.execute(query, (effect,))
            name = ""
            for row in new_cursor:
                name = row[0]
            if not name:
                old_cursor.execute(query, (effect,))
                for row in old_cursor:
                    name = row[0]
            effectnames[effect] = name
        return name

    attrnames = {}
    def getattrname(attr):
        """Get attribute name from the new db"""
        if attr in attrnames:
            name = attrnames[attr]
        else:
            query = 'SELECT attributeName FROM dgmattribs WHERE attributeID = ?'
            new_cursor.execute(query, (attr,))
            name = ""
            for row in new_cursor:
                name = row[0]
            if not name:
                old_cursor.execute(query, (attr,))
                for row in old_cursor:
                    name = row[0]
            attrnames[attr] = name
        return name

    # State table
    S = {"unchanged": 0,
         "removed": 1,
         "changed": 2,
         "added": 3 }

    if effects or attributes or groups:
        # Format:
        # Key: item id
        # Value: [groupID, set(effects), {attribute id : value}]
        old_itmdata = {}
        new_itmdata = {}

        for cursor, dictionary in ((old_cursor, old_itmdata), (new_cursor, new_itmdata)):
            # Compose list of items we're interested in, filtered by category
            query = 'SELECT it.typeID, it.groupID FROM invtypes AS it INNER JOIN invgroups AS ig ON it.groupID = ig.groupID INNER JOIN invcategories AS ic ON ig.categoryID = ic.categoryID WHERE it.published = 1 AND ic.categoryName IN ("Ship", "Module", "Charge", "Skill", "Drone", "Implant", "Subsystem")'
            cursor.execute(query)
            for row in cursor:
                itemid = row[0]
                groupID = row[1]
                # Initialize container for the data for each item with empty stuff besides groupID
                dictionary[itemid] = [groupID, set(), {}]
            # Add items filtered by group
            query = 'SELECT it.typeID, it.groupID FROM invtypes AS it INNER JOIN invgroups AS ig ON it.groupID = ig.groupID WHERE it.published = 1 AND ig.groupName IN ("Effect Beacon", "Ship Modifiers")'
            cursor.execute(query)
            for row in cursor:
                itemid = row[0]
                groupID = row[1]
                dictionary[itemid] = [groupID, set(), {}]

            if effects:
                # Pull all eff
                query = 'SELECT it.typeID, de.effectID FROM invtypes AS it INNER JOIN dgmtypeeffects AS dte ON dte.typeID = it.typeID INNER JOIN dgmeffects AS de ON de.effectID = dte.effectID WHERE it.published = 1'
                cursor.execute(query)
                for row in cursor:
                    itemid = row[0]
                    effectID = row[1]
                    # Process only items we need
                    if itemid in dictionary:
                        # Add effect to the set
                        effectSet = dictionary[itemid][1]
                        effectSet.add(effectID)

            if attributes:
                # Add base attributes to our data
                query = 'SELECT it.typeID, it.mass, it.capacity, it.volume FROM invtypes AS it'
                cursor.execute(query)
                for row in cursor:
                    itemid = row[0]
                    if itemid in dictionary:
                        attrdict = dictionary[itemid][2]
                        # Add base attributes: mass (4), capacity (38) and volume (161)
                        attrdict[4] = row[1]
                        attrdict[38] = row[2]
                        attrdict[161] = row[3]

                # Add attribute data for other attributes
                query = 'SELECT dta.typeID, dta.attributeID, dta.value FROM dgmtypeattribs AS dta'
                cursor.execute(query)
                for row in cursor:
                    itemid = row[0]
                    if itemid in dictionary:
                        attrid = row[1]
                        attrval = row[2]
                        attrdict = dictionary[itemid][2]
                        attrdict[attrid] = attrval

        # Get set of IDs from both dictionaries
        items_old = set(old_itmdata.keys())
        items_new = set(new_itmdata.keys())

        # Format:
        # Key: item state
        # Value: {item id: ((group state, old group, new group), {effect state: set(effects)}, {attribute state: {attributeID: (old value, new value)}})}
        global_itmdata = {}

        # Initialize it
        for state in S:
            global_itmdata[S[state]] = {}


        # Fill all the data for removed items
        for item in items_old.difference(items_new):
            # Set item state to removed
            state = S["removed"]
            # Set only old group for item
            oldgroup = old_itmdata[item][0]
            groupdata = (S["unchanged"], oldgroup, None)
            # Set old set of effects and mark all as unchanged
            effectsdata = {}
            effectsdata[S["unchanged"]] = set()
            if effects:
                oldeffects = old_itmdata[item][1]
                effectsdata[S["unchanged"]].update(oldeffects)
            # Set old set of attributes and mark all as unchanged
            attrdata = {}
            attrdata[S["unchanged"]] = {}
            if attributes:
                oldattrs = old_itmdata[item][2]
                for attr in oldattrs:
                    # NULL will mean there's no such attribute in db
                    attrdata[S["unchanged"]][attr] = (oldattrs[attr], "NULL")
            # Fill global dictionary with data we've got
            global_itmdata[state][item] = (groupdata, effectsdata, attrdata)


        # Now, for added items
        for item in items_new.difference(items_old):
            # Set item state to added
            state = S["added"]
            # Set only new group for item
            newgroup = new_itmdata[item][0]
            groupdata = (S["unchanged"], None, newgroup)
            # Set new set of effects and mark all as unchanged
            effectsdata = {}
            effectsdata[S["unchanged"]] = set()
            if effects:
                neweffects = new_itmdata[item][1]
                effectsdata[S["unchanged"]].update(neweffects)
            # Set new set of attributes and mark all as unchanged
            attrdata = {}
            attrdata[S["unchanged"]] = {}
            if attributes:
                newattrs = new_itmdata[item][2]
                for attr in newattrs:
                    # NULL will mean there's no such attribute in db
                    attrdata[S["unchanged"]][attr] = ("NULL", newattrs[attr])
            # Fill global dictionary with data we've got
            global_itmdata[state][item] = (groupdata, effectsdata, attrdata)

        # Now, check all the items which exist in both databases
        for item in items_old.intersection(items_new):
            # Set group data for an item
            oldgroup = old_itmdata[item][0]
            newgroup = new_itmdata[item][0]
            # If we're not asked to compare groups, mark them as unchanged anyway
            groupdata = (S["changed"] if oldgroup != newgroup and groups else S["unchanged"], oldgroup, newgroup)
            # Fill effects data into appropriate groups
            effectsdata = {}
            for state in S:
                # We do not have changed effects whatsoever
                if state != "changed":
                    effectsdata[S[state]] = set()
            if effects:
                oldeffects = old_itmdata[item][1]
                neweffects = new_itmdata[item][1]
                effectsdata[S["unchanged"]].update(oldeffects.intersection(neweffects))
                effectsdata[S["removed"]].update(oldeffects.difference(neweffects))
                effectsdata[S["added"]].update(neweffects.difference(oldeffects))
            # Go through all attributes, filling global data dictionary
            attrdata = {}
            for state in S:
                attrdata[S[state]] = {}
            if attributes:
                oldattrs = old_itmdata[item][2]
                newattrs = new_itmdata[item][2]
                for attr in set(oldattrs.keys()).union(newattrs.keys()):
                    # NULL will mean there's no such attribute in db
                    oldattr = oldattrs.get(attr, "NULL")
                    newattr = newattrs.get(attr, "NULL")
                    attrstate = S["unchanged"]
                    if oldattr == "NULL" and newattr != "NULL":
                        attrstate = S["added"]
                    elif oldattr != "NULL" and newattr == "NULL":
                        attrstate = S["removed"]
                    elif oldattr != newattr:
                        attrstate = S["changed"]
                    attrdata[attrstate][attr] = (oldattr, newattr)
            # Consider item as unchanged by default and set it to change when we see any changes in sub-items
            state = S["unchanged"]
            if state == S["unchanged"] and groupdata[0] != S["unchanged"]:
                state = S["changed"]
            if state == S["unchanged"] and (len(effectsdata[S["removed"]]) > 0 or len(effectsdata[S["added"]]) > 0):
                state = S["changed"]
            if state == S["unchanged"] and (len(attrdata[S["removed"]]) > 0 or len(attrdata[S["changed"]]) > 0 or len(attrdata[S["added"]]) > 0):
                state = S["changed"]
            # Fill global dictionary with data we've got
            global_itmdata[state][item] = (groupdata, effectsdata, attrdata)

    # As eos uses names as unique IDs in lot of places, we have to keep track of name changes
    if renames:
        ren_effects = {}
        query = 'SELECT effectID, effectName FROM dgmeffects'
        findrenames(ren_effects, query, strip = True)

        ren_attributes = {}
        query = 'SELECT attributeID, attributeName FROM dgmattribs'
        findrenames(ren_attributes, query)

        ren_categories = {}
        query = 'SELECT categoryID, categoryName FROM invcategories'
        findrenames(ren_categories, query)

        ren_groups = {}
        query = 'SELECT groupID, groupName FROM invgroups'
        findrenames(ren_groups, query)

        ren_marketgroups = {}
        query = 'SELECT marketGroupID, marketGroupName FROM invmarketgroups'
        findrenames(ren_marketgroups, query)

        ren_items = {}
        query = 'SELECT typeID, typeName FROM invtypes'
        findrenames(ren_items, query)

    try:
        # Get db metadata
        old_meta = {}
        new_meta = {}
        query = 'SELECT field_name, field_value FROM metadata WHERE field_name LIKE "client_build"'
        old_cursor.execute(query)
        for row in old_cursor:
            old_meta[row[0]] = row[1]
        new_cursor.execute(query)
        for row in new_cursor:
            new_meta[row[0]] = row[1]
    except:
        pass
    # Print jobs
    print("Comparing databases:\n{0} -> {1}\n".format(old_meta.get("client_build"), new_meta.get("client_build")))

    if renames:
        title = 'effects'
        printrenames(ren_effects, title, implementedtag=True)

        title = 'attributes'
        printrenames(ren_attributes, title)

        title = 'categories'
        printrenames(ren_categories, title)

        title = 'groups'
        printrenames(ren_groups, title)

        title = 'market groups'
        printrenames(ren_marketgroups, title)

        title = 'items'
        printrenames(ren_items, title)

    print
    print

    if effects or attributes or groups:
        # Print legend only when there're any interesting changes
        if len(global_itmdata[S["removed"]]) > 0 or len(global_itmdata[S["changed"]]) > 0 or len(global_itmdata[S["added"]]) > 0:
            genleg = "[+] - new item\n[-] - removed item\n[*] - changed item\n"
            grpleg = "(x => y) - group changes\n" if groups else ""
            attreffleg = "  [+] - effect or attribute has been added to item\n  [-] - effect or attribute has been removed from item\n" if attributes or effects else ""
            effleg = "  [y] - effect is implemented\n  [n] - effect is not implemented\n" if effects else ""
            print("{0}{1}{2}{3}\nItems:".format(genleg, grpleg, attreffleg, effleg))

            # Make sure our states are sorted
            stateorder = sorted(global_itmdata)

            TG = {S["unchanged"]: "+", S["changed"]: "*",
                  S["removed"]: "-",
                  S["added"]: "+"}

            # Cycle through states
            for itmstate in stateorder:
                # Skip unchanged items
                if itmstate == S["unchanged"]:
                    continue
                items = global_itmdata[itmstate]
                # Sort by name first
                itemorder = sorted(items, key=lambda item: getitemname(item))
                # Then by group id
                itemorder = sorted(itemorder, key=lambda item: items[item][0][2] or items[item][0][1])
                # Then by category id
                itemorder = sorted(itemorder, key=lambda item: getgroupcat(items[item][0][2] or items[item][0][1]))

                for item in itemorder:
                    groupdata = items[item][0]
                    groupstr = " ({0} => {1})".format(getgroupname(groupdata[1]), getgroupname(groupdata[2])) if groupdata[0] == S["changed"] else ""
                    print("\n[{0}] {1}{2}".format(TG[itmstate], getitemname(item).encode('utf-8'), groupstr))

                    effdata = items[item][1]
                    for effstate in stateorder:
                        # Skip unchanged effect sets, but always include them for added or removed ships
                        # Also, always skip empty data
                        if (effstate == S["unchanged"] and itmstate not in (S["removed"], S["added"])) or effstate not in effdata:
                            continue
                        effects = effdata[effstate]
                        efforder = sorted(effects, key=lambda eff: geteffectname(eff))
                        for eff in efforder:
                            # Take tag from item if item was added or removed
                            tag = TG[effstate] if itmstate not in (S["removed"], S["added"]) else TG[itmstate]
                            print("  [{0}|{1}] {2}".format(tag, "y" if geteffst(geteffectname(eff)) else "n", geteffectname(eff)))

                    attrdata = items[item][2]
                    for attrstate in stateorder:
                        # Skip unchanged and empty attribute sets, also skip attributes display for added and removed items
                        if (attrstate == S["unchanged"] and itmstate != S["added"]) or itmstate in (S["removed"], ) or attrstate not in attrdata:
                            continue
                        attrs = attrdata[attrstate]
                        attrorder = sorted(attrs, key=lambda attr: getattrname(attr))
                        for attr in attrorder:
                            valline = ""
                            if attrs[attr][0] == "NULL" or itmstate == S["added"]:
                                valline = "{0}".format(attrs[attr][1] or 0)
                            elif attrs[attr][1] == "NULL":
                                valline = "{0}".format(attrs[attr][0] or 0)
                            else:
                                valline = "{0} => {1}".format(attrs[attr][0] or 0, attrs[attr][1] or 0)
                            print("  [{0}] {1}: {2}".format(TG[attrstate], getattrname(attr), valline))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two databases generated from eve dump to find eos-related differences")
    parser.add_argument("-o", "--old", type=str, help="path to old cache data dump, defaults to current pyfa eve.db", default=default_old)
    parser.add_argument("-n", "--new", type=str, required=True, help="path to new cache data dump")
    parser.add_argument("-g", "--nogroups", action="store_false", default=True, dest="groups", help="don't show changed groups")
    parser.add_argument("-e", "--noeffects", action="store_false", default=True, dest="effects", help="don't show list of changed effects")
    parser.add_argument("-a", "--noattributes", action="store_false", default=True, dest="attributes", help="don't show list of changed attributes")
    parser.add_argument("-r", "--norenames", action="store_false", default=True, dest="renames", help="don't show list of renamed data")
    args = parser.parse_args()

    main(args.old, args.new, args.groups, args.effects, args.attributes, args.renames)
