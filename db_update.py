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


import functools
import itertools
import json
import os
import sqlite3
import sys


ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT_DIR, 'eve.db')
JSON_DIR = os.path.join(ROOT_DIR, 'staticdata')
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
GAMEDATA_SCHEMA_VERSION = 1


def db_needs_update():
    """True if needs, false if it does not, none if we cannot check it."""
    try:
        with open(os.path.join(JSON_DIR, 'phobos', 'metadata.json')) as f:
            data_version = next((r['field_value'] for r in json.load(f) if r['field_name'] == 'client_build'))
    except KeyboardInterrupt:
        raise
    # If we have no source data - return None; should not update in this case
    except:
        return None
    if not os.path.isfile(DB_PATH):
        print('Gamedata DB not found')
        return True
    db_data_version = None
    db_schema_version = None
    try:
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        cursor.execute('SELECT field_value FROM metadata WHERE field_name = \'client_build\'')
        for row in cursor:
            db_data_version = int(row[0])
        cursor.execute('SELECT field_value FROM metadata WHERE field_name = \'schema_version\'')
        for row in cursor:
            db_schema_version = int(row[0])
        cursor.close()
        db.close()
    except KeyboardInterrupt:
        raise
    except:
        print('Error when fetching gamedata DB metadata')
        return True
    if data_version != db_data_version:
        print('Gamedata DB data version mismatch: needed {}, DB has {}'.format(data_version, db_data_version))
        return True
    if GAMEDATA_SCHEMA_VERSION != db_schema_version:
        print('Gamedata DB schema version mismatch: needed {}, DB has {}'.format(GAMEDATA_SCHEMA_VERSION, db_schema_version))
        return True
    return False


def update_db():

    print('Building gamedata DB...')

    if os.path.isfile(DB_PATH):
        os.remove(DB_PATH)

    import eos.db
    import eos.gamedata

    # Create the database tables
    eos.db.gamedata_meta.create_all()

    # Config dict
    tables = {
        'clonegrades': ('fsd_lite', eos.gamedata.AlphaCloneSkill),
        'dogmaattributes': ('bulkdata', eos.gamedata.AttributeInfo),
        'dogmaeffects': ('bulkdata', eos.gamedata.Effect),
        'dogmatypeattributes': ('bulkdata', eos.gamedata.Attribute),
        'dogmatypeeffects': ('bulkdata', eos.gamedata.ItemEffect),
        'dogmaunits': ('bulkdata', eos.gamedata.Unit),
        'evecategories': ('fsd_lite', eos.gamedata.Category),
        'evegroups': ('fsd_lite', eos.gamedata.Group),
        'metagroups': ('fsd_binary', eos.gamedata.MetaGroup),
        'evetypes': ('fsd_lite', eos.gamedata.Item),
        'traits': ('phobos', eos.gamedata.Traits),
        'metadata': ('phobos', eos.gamedata.MetaData),
        'marketgroups': ('fsd_binary', eos.gamedata.MarketGroup)}

    fieldMapping = {
        'marketgroups': {
            'id': 'marketGroupID',
            'name': 'marketGroupName'},
        'metagroups': {
            'id': 'metaGroupID'}}

    rowsInValues = (
        'evetypes',
        'evegroups',
        'evecategories',
        'marketgroups',
        'metagroups')

    def convertIcons(data):
        new = []
        for k, v in list(data.items()):
            v['iconID'] = k
            new.append(v)
        return new

    def convertClones(data):
        newData = []

        # December, 2017 - CCP decided to use only one set of skill levels for alpha clones. However, this is still
        # represented in the data as a skillset per race. To ensure that all skills are the same, we store them in a way
        # that we can check to make sure all races have the same skills, as well as skill levels

        check = {}

        for ID in data:
            for skill in data[ID]['skills']:
                newData.append({
                    'alphaCloneID': int(ID),
                    'alphaCloneName': 'Alpha Clone',
                    'typeID': skill['typeID'],
                    'level': skill['level']})
                if ID not in check:
                    check[ID] = {}
                check[ID][int(skill['typeID'])] = int(skill['level'])

        if not functools.reduce(lambda a, b: a if a == b else False, [v for _, v in check.items()]):
            raise Exception('Alpha Clones not all equal')

        newData = [x for x in newData if x['alphaCloneID'] == 1]

        if len(newData) == 0:
            raise Exception('Alpha Clone processing failed')

        return newData

    def convertTraits(data):

        def convertSection(sectionData):
            sectionLines = []
            headerText = '<b>{}</b>'.format(sectionData['header'])
            sectionLines.append(headerText)
            for bonusData in sectionData['bonuses']:
                prefix = '{} '.format(bonusData['number']) if 'number' in bonusData else ''
                bonusText = '{}{}'.format(prefix, bonusData['text'].replace('\u00B7', '\u2022 '))
                sectionLines.append(bonusText)
            sectionLine = '<br />\n'.join(sectionLines)
            return sectionLine

        newData = []
        for row in data:
            typeLines = []
            typeId = row['typeID']
            traitData = row['traits']
            for skillData in sorted(traitData.get('skills', ()), key=lambda i: i['header']):
                typeLines.append(convertSection(skillData))
            if 'role' in traitData:
                typeLines.append(convertSection(traitData['role']))
            if 'misc' in traitData:
                typeLines.append(convertSection(traitData['misc']))
            traitLine = '<br />\n<br />\n'.join(typeLines)
            newRow = {'typeID': typeId, 'traitText': traitLine}
            newData.append(newRow)
        return newData

    def fillReplacements(tables):

        def compareAttrs(attrs1, attrs2):
            # Consider items as different if they have no attrs
            if len(attrs1) == 0 and len(attrs2) == 0:
                return False
            if set(attrs1) != set(attrs2):
                return False
            if all(attrs1[aid] == attrs2[aid] for aid in attrs1):
                return True
            return False

        print('finding replacements')
        skillReqAttribs = {
            182: 277,
            183: 278,
            184: 279,
            1285: 1286,
            1289: 1287,
            1290: 1288}
        skillReqAttribsFlat = set(skillReqAttribs.keys()).union(skillReqAttribs.values())
        # Get data on type groups
        # Format: {type ID: group ID}
        typesGroups = {}
        for row in tables['evetypes']:
            typesGroups[row['typeID']] = row['groupID']
        # Get data on item effects
        # Format: {type ID: set(effect, IDs)}
        typesEffects = {}
        for row in tables['dogmatypeeffects']:
            typesEffects.setdefault(row['typeID'], set()).add(row['effectID'])
        # Get data on type attributes
        # Format: {type ID: {attribute ID: attribute value}}
        typesNormalAttribs = {}
        typesSkillAttribs = {}
        for row in tables['dogmatypeattributes']:
            attributeID = row['attributeID']
            if attributeID in skillReqAttribsFlat:
                typeSkillAttribs = typesSkillAttribs.setdefault(row['typeID'], {})
                typeSkillAttribs[row['attributeID']] = row['value']
            # Ignore these attributes for comparison purposes
            elif attributeID in (
                # We do not need mass as it affects final ship stats only when carried by ship itself
                # (and we're not going to replace ships), but it's wildly inconsistent for other items,
                # which otherwise would be the same
                4,  # mass
                124,  # mainColor
                162,  # radius
                422,  # techLevel
                633,  # metaLevel
                1692,  # metaGroupID
                1768  # typeColorScheme
            ):
                continue
            else:
                typeNormalAttribs = typesNormalAttribs.setdefault(row['typeID'], {})
                typeNormalAttribs[row['attributeID']] = row['value']
        # Get data on skill requirements
        # Format: {type ID: {skill type ID: skill level}}
        typesSkillReqs = {}
        for typeID, typeAttribs in typesSkillAttribs.items():
            typeSkillAttribs = typesSkillAttribs.get(typeID, {})
            if not typeSkillAttribs:
                continue
            typeSkillReqs = typesSkillReqs.setdefault(typeID, {})
            for skillreqTypeAttr, skillreqLevelAttr in skillReqAttribs.items():
                try:
                    skillType = int(typeSkillAttribs[skillreqTypeAttr])
                    skillLevel = int(typeSkillAttribs[skillreqLevelAttr])
                except (KeyError, ValueError):
                    continue
                typeSkillReqs[skillType] = skillLevel
        # Format: {group ID: category ID}
        groupCategories = {}
        for row in tables['evegroups']:
            groupCategories[row['groupID']] = row['categoryID']
        # As EVE affects various types mostly depending on their group or skill requirements,
        # we're going to group various types up this way
        # Format: {(group ID, frozenset(skillreq, type, IDs), frozenset(type, effect, IDs): [type ID, {attribute ID: attribute value}]}
        groupedData = {}
        for row in tables['evetypes']:
            typeID = row['typeID']
            # Ignore items outside of categories we need
            if groupCategories[typesGroups[typeID]] not in (
                6,  # Ship
                7,  # Module
                8,  # Charge
                18,  # Drone
                20,  # Implant
                22,  # Deployable
                23,  # Starbase
                32,  # Subsystem
                35,  # Decryptors
                65,  # Structure
                66,  # Structure Module
                87,  # Fighter
            ):
                continue
            typeAttribs = typesNormalAttribs.get(typeID, {})
            # Ignore items w/o attributes
            if not typeAttribs:
                continue
            # We need only skill types, not levels for keys
            typeSkillreqs = frozenset(typesSkillReqs.get(typeID, {}))
            typeGroup = typesGroups[typeID]
            typeEffects = frozenset(typesEffects.get(typeID, ()))
            groupData = groupedData.setdefault((typeGroup, typeSkillreqs, typeEffects), [])
            groupData.append((typeID, typeAttribs))
        # Format: {type ID: set(type IDs)}
        replacements = {}
        # Now, go through composed groups and for every item within it
        # find items which are the same
        for groupData in groupedData.values():
            for type1, type2 in itertools.combinations(groupData, 2):
                if compareAttrs(type1[1], type2[1]):
                    replacements.setdefault(type1[0], set()).add(type2[0])
                    replacements.setdefault(type2[0], set()).add(type1[0])
        # Put this data into types table so that normal process hooks it up
        for row in tables['evetypes']:
            row['replacements'] = ','.join('{}'.format(tid) for tid in sorted(replacements.get(row['typeID'], ())))

    data = {}

    # Dump all data to memory so we can easely cross check ignored rows
    for jsonName, (minerName, cls) in tables.items():
        with open(os.path.join(JSON_DIR, minerName, '{}.json'.format(jsonName)), encoding='utf-8') as f:
            tableData = json.load(f)
        if jsonName in rowsInValues:
            newTableData = []
            for k, v in tableData.items():
                row = {}
                row.update(v)
                if 'id' not in row:
                    row['id'] = int(k)
                newTableData.append(row)
            tableData = newTableData
        if jsonName == 'icons':
            tableData = convertIcons(tableData)
        if jsonName == 'traits':
            tableData = convertTraits(tableData)
        if jsonName == 'clonegrades':
            tableData = convertClones(tableData)
        data[jsonName] = tableData

    fillReplacements(data)

    # Set with typeIDs which we will have in our database
    # Sometimes CCP unpublishes some items we want to have published, we
    # can do it here - just add them to initial set
    eveTypes = set()
    for row in data['evetypes']:
        if (
            row['published'] or
            row['typeName'] == 'Capsule' or
            # group Ship Modifiers, for items like tactical t3 ship modes
            row['groupID'] == 1306 or
            # Civilian weapons
            (row['typeName'].startswith('Civilian') and "Shuttle" not in row['typeName']) or
            # Micro Bombs (Fighters)
            row['typeID'] in (41549, 41548, 41551, 41550) or
            # Abyssal weather (environment)
            row['groupID'] in (
                1882,
                1975,
                1971,
                # the "container" for the abyssal environments
                1983) or
            # Dark Blood Tracking Disruptor (drops, but rarely)
            row['typeID'] == 32416
        ):
            eveTypes.add(row['typeID'])

    # ignore checker
    def isIgnored(file, row):
        if file in ('evetypes', 'dogmatypeeffects', 'dogmatypeattributes') and row['typeID'] not in eveTypes:
            return True
        return False

    # Loop through each json file and write it away, checking ignored rows
    for jsonName, table in data.items():
        fieldMap = fieldMapping.get(jsonName, {})
        tmp = []

        print('processing {}'.format(jsonName))

        for row in table:
            # We don't care about some kind of rows, filter it out if so
            if not isIgnored(jsonName, row):
                if (
                    jsonName == 'evetypes' and (
                        # Apparently people really want Civilian modules available
                        (row['typeName'].startswith('Civilian') and "Shuttle" not in row['typeName']) or
                        row['typeName'] in ('Capsule', 'Dark Blood Tracking Disruptor'))
                ):
                    row['published'] = True

                instance = tables[jsonName][1]()
                # fix for issue 80
                if jsonName is 'icons' and 'res:/ui/texture/icons/' in str(row['iconFile']).lower():
                    row['iconFile'] = row['iconFile'].lower().replace('res:/ui/texture/icons/', '').replace('.png', '')
                    # with res:/ui... references, it points to the actual icon file (including it's size variation of #_size_#)
                    # strip this info out and get the identifying info
                    split = row['iconFile'].split('_')
                    if len(split) == 3:
                        row['iconFile'] = '{}_{}'.format(split[0], split[2])
                if jsonName is 'icons' and 'modules/' in str(row['iconFile']).lower():
                    row['iconFile'] = row['iconFile'].lower().replace('modules/', '').replace('.png', '')

                if jsonName is 'clonegrades':
                    if row['alphaCloneID'] not in tmp:
                        cloneParent = eos.gamedata.AlphaClone()
                        setattr(cloneParent, 'alphaCloneID', row['alphaCloneID'])
                        setattr(cloneParent, 'alphaCloneName', row['alphaCloneName'])
                        eos.db.gamedata_session.add(cloneParent)
                        tmp.append(row['alphaCloneID'])

                for k, v in row.items():
                    if isinstance(v, str):
                        v = v.strip()
                    setattr(instance, fieldMap.get(k, k), v)

                eos.db.gamedata_session.add(instance)

    # quick and dirty hack to get this data in
    with open(os.path.join(JSON_DIR, 'fsd_binary', 'dynamicitemattributes.json'), encoding='utf-8') as f:
        bulkdata = json.load(f)
        for mutaID, data in bulkdata.items():
            muta = eos.gamedata.DynamicItem()
            muta.typeID = mutaID
            muta.resultingTypeID = data['inputOutputMapping'][0]['resultingType']
            eos.db.gamedata_session.add(muta)

            for x in data['inputOutputMapping'][0]['applicableTypes']:
                item = eos.gamedata.DynamicItemItem()
                item.typeID = mutaID
                item.applicableTypeID = x
                eos.db.gamedata_session.add(item)

            for attrID, attrData in data['attributeIDs'].items():
                attr = eos.gamedata.DynamicItemAttribute()
                attr.typeID = mutaID
                attr.attributeID = attrID
                attr.min = attrData['min']
                attr.max = attrData['max']
                eos.db.gamedata_session.add(attr)

    metadata_schema_version = eos.gamedata.MetaData()
    metadata_schema_version.field_name = 'schema_version'
    metadata_schema_version.field_value = GAMEDATA_SCHEMA_VERSION
    eos.db.gamedata_session.add(metadata_schema_version)

    eos.db.gamedata_session.commit()

    # CCP still has 5 subsystems assigned to T3Cs, even though only 4 are available / usable. They probably have some
    # old legacy requirement or assumption that makes it difficult for them to change this value in the data. But for
    # pyfa, we can do it here as a post-processing step
    eos.db.gamedata_engine.execute('UPDATE dgmtypeattribs SET value = 4.0 WHERE attributeID = ?', (1367,))

    eos.db.gamedata_engine.execute('UPDATE invtypes SET published = 0 WHERE typeName LIKE \'%abyssal%\'')


    print()
    for x in [
        30  # Apparel
    ]:
        cat = eos.db.gamedata_session.query(eos.gamedata.Category).filter(eos.gamedata.Category.ID == x).first()
        print ('Removing Category: {}'.format(cat.name))
        eos.db.gamedata_session.delete(cat)

    eos.db.gamedata_session.commit()
    eos.db.gamedata_engine.execute('VACUUM')

    print('done')


if __name__ == '__main__':
    update_db()
