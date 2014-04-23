#!/usr/bin/env python3
#======================================================================
# Copyright (C) 2012 Diego Duclos
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

import os
import sys

# Add eos root path to sys.path so we can import ourselves
path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))
sys.path.append(os.path.realpath(os.path.join(path, "..", "..", "..")))

import sqlite3
import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This scripts dumps effects from an sqlite cache dump to mongo")
    parser.add_argument("-d", "--db", required=True, type=str, help="The sqlalchemy connectionstring, example: sqlite:///c:/tq.db")
    parser.add_argument("-j", "--json", required=True, type=str, help="The path to the json dum")
    args = parser.parse_args()

    jsonPath = os.path.expanduser(args.json)

    # Import eos.config first and change it
    import eos.config
    eos.config.gamedata_connectionstring = args.db
    eos.config.debug = False

    # Now thats done, we can import the eos modules using the config
    import eos.db
    import eos.gamedata

    # Create the database tables
    eos.db.gamedata_meta.create_all()

    # Config dict
    tables = {"dgmattribs": eos.gamedata.AttributeInfo,
              "dgmeffects": eos.gamedata.EffectInfo,
              "dgmtypeattribs": eos.gamedata.Attribute,
              "dgmtypeeffects": eos.gamedata.Effect,
              "dgmunits": eos.gamedata.Unit,
              "icons": eos.gamedata.Icon,
              "invcategories": eos.gamedata.Category,
              "invgroups": eos.gamedata.Group,
              "invmetagroups": eos.gamedata.MetaGroup,
              "invmetatypes": eos.gamedata.MetaType,
              "invtypes": eos.gamedata.Item,
              "phobostraits": eos.gamedata.Traits,
              "marketProxy()_GetMarketGroups()": eos.gamedata.MarketGroup}

    fieldMapping = {"icons": {"id": "iconID"}}
    data = {}

    # Dump all data to memory so we can easely cross check ignored rows
    for jsonName, cls in tables.iteritems():
        f = open(os.path.join(jsonPath, "{}.json".format(jsonName)))
        data[jsonName] = json.load(f, encoding='cp1252')

    # Do some preprocessing to make our job easier
    invTypes = set()
    for row in data["invtypes"]:
        if row["published"]:
            invTypes.add(row["typeID"])

    # ignore checker
    def isIgnored(file, row):
        if file == "invtypes" and not row["published"]:
            return True
        elif file == "dgmtypeeffects" and not row["typeID"] in invTypes:
            return True
        elif file == "dgmtypeattribs" and not row["typeID"] in invTypes:
            return True
        elif file == "invmetatypes" and not row["typeID"] in invTypes:
            return True

        return False

    # Loop through each json file and write it away, checking ignored rows
    for jsonName, table in data.iteritems():
        fieldMap = fieldMapping.get(jsonName, {})
        print "processing {}".format(jsonName)
        for row in table:
            # We don't care about some kind of rows, filter it out if so
            if not isIgnored(jsonName, row):
                instance = tables[jsonName]()
                # fix for issue 80
                if jsonName is "icons" and "res:/UI/Texture/Icons/" in str(row['iconFile']):
                    row['iconFile'] = row['iconFile'].replace('res:/UI/Texture/Icons/','')
                    row['iconFile'] = row['iconFile'].replace('.png','')
                for k, v in row.iteritems():
                    setattr(instance, fieldMap.get(k, k), v)

                eos.db.gamedata_session.add(instance)

        eos.db.gamedata_session.commit()

    print("done")
