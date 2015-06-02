#!/usr/bin/env python
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
sys.path.append(os.path.realpath(os.path.join(path, "..")))

import json
import argparse

def main(db, json_path):

    jsonPath = os.path.expanduser(json_path)

    # Import eos.config first and change it
    import eos.config
    eos.config.gamedata_connectionstring = db
    eos.config.debug = False

    # Now thats done, we can import the eos modules using the config
    import eos.db
    import eos.gamedata

    # Create the database tables
    eos.db.gamedata_meta.create_all()

    # Config dict
    tables = {
        "dgmattribs": eos.gamedata.AttributeInfo,
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
        "phbtraits": eos.gamedata.Traits,
        "phbmetadata": eos.gamedata.MetaData,
        "mapbulk_marketGroups": eos.gamedata.MarketGroup
    }

    fieldMapping = {
        "dgmattribs": {
            "displayName_en-us": "displayName"
        },
        "dgmeffects": {
            "displayName_en-us": "displayName",
            "description_en-us": "description"
        },
        "dgmunits": {
            "displayName_en-us": "displayName"
        },
        #icons???
        "invcategories": {
            "categoryName_en-us": "categoryName"
        },
        "invgroups": {
            "groupName_en-us": "groupName"
        },
        "invmetagroups": {
            "metaGroupName_en-us": "metaGroupName"
        },
        "invtypes": {
            "typeName_en-us": "typeName",
            "description_en-us": "description"
        },
        #phbtraits???
        "mapbulk_marketGroups": {
            "marketGroupName_en-us": "marketGroupName",
            "description_en-us": "description"
        }

    }

    def convertIcons(data):
        new = []
        for k, v in data.items():
            v["iconID"] = k
            new.append(v)
        return new

    def convertTraits(data):

        def convertSection(sectionData):
            sectionLines = []
            headerText = u"<b>{}</b>".format(sectionData["header"])
            sectionLines.append(headerText)
            for bonusData in sectionData["bonuses"]:
                prefix = u"{} ".format(bonusData["number"]) if "number" in bonusData else ""
                bonusText = u"{}{}".format(prefix, bonusData["text"].replace(u"\u00B7", u"\u2022 "))
                sectionLines.append(bonusText)
            sectionLine = u"<br />\n".join(sectionLines)
            return sectionLine

        newData = []
        for row in data:
            typeLines = []
            typeId = row["typeID"]
            traitData = row["traits_en-us"]
            for skillData in sorted(traitData.get("skills", ()), key=lambda i: i["header"]):
                typeLines.append(convertSection(skillData))
            if "role" in traitData:
                typeLines.append(convertSection(traitData["role"]))
            if "misc" in traitData:
                typeLines.append(convertSection(traitData["misc"]))
            traitLine = u"<br />\n<br />\n".join(typeLines)
            newRow = {"typeID": typeId, "traitText": traitLine}
            newData.append(newRow)
        return newData

    def convertTypes(typesData):
        """
        Add factionID column to invtypes table.
        """
        factionMap = {}
        with open(os.path.join(jsonPath, "fsdTypeOverrides.json")) as f:
            overridesData = json.load(f)
        for typeID, typeData in overridesData.items():
            factionID = typeData.get("factionID")
            if factionID is not None:
                factionMap[int(typeID)] = factionID
        for row in typesData:
            row['factionID'] = factionMap.get(int(row['typeID']))
        return typesData

    data = {}

    # Dump all data to memory so we can easely cross check ignored rows
    for jsonName, cls in tables.iteritems():
        with open(os.path.join(jsonPath, "{}.json".format(jsonName))) as f:
            tableData = json.load(f)
        if jsonName == "icons":
            tableData = convertIcons(tableData)
        if jsonName == "phbtraits":
            tableData = convertTraits(tableData)
        if jsonName == "invtypes":
            tableData = convertTypes(tableData)
        data[jsonName] = tableData

    # Set with typeIDs which we will have in our database
    invTypes = {
    # Sometimes CCP unpublishes some items we want to have published, we
    # can do it here
        31906,  # Federation Navy 200mm Steel Plates
        31904,  # Imperial Navy 200mm Steel Plates
        28782,  # Syndicate 200mm Steel Plates
    }
    for row in data["invtypes"]:
        # 1306 - group Ship Modifiers, for items like tactical t3 ship modes
        if (row["published"] or row['groupID'] == 1306):
            invTypes.add(row["typeID"])

    # ignore checker
    def isIgnored(file, row):
        if file in ("invtypes", "dgmtypeeffects", "dgmtypeattribs", "invmetatypes") and row['typeID'] not in invTypes:
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
                if jsonName is "icons" and "res:/UI/Texture/Icons/" in str(row["iconFile"]):
                    row["iconFile"] = row["iconFile"].replace("res:/UI/Texture/Icons/","").replace(".png", "")
                for k, v in row.iteritems():
                    setattr(instance, fieldMap.get(k, k), v)

                eos.db.gamedata_session.add(instance)

    eos.db.gamedata_session.commit()

    print("done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This scripts dumps effects from an sqlite cache dump to mongo")
    parser.add_argument("-d", "--db", required=True, type=str, help="The sqlalchemy connectionstring, example: sqlite:///c:/tq.db")
    parser.add_argument("-j", "--json", required=True, type=str, help="The path to the json dump")
    args = parser.parse_args()

    main(args.db, args.json)
