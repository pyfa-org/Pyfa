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
import re
import sqlite3
import sys


ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT_DIR, 'eve.db')
JSON_DIR = os.path.join(ROOT_DIR, 'staticdata')
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
GAMEDATA_SCHEMA_VERSION = 3


def db_needs_update():
    """True if needs, false if it does not, none if we cannot check it."""
    try:
        with open(os.path.join(JSON_DIR, 'phobos', 'metadata.json')) as f:
            data_version = next((r['field_value'] for r in json.load(f) if r['field_name'] == 'client_build'))
    except (KeyboardInterrupt, SystemExit):
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
    except (KeyboardInterrupt, SystemExit):
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

    def _readData(minerName, jsonName, keyIdName=None):
        with open(os.path.join(JSON_DIR, minerName, '{}.json'.format(jsonName)), encoding='utf-8') as f:
            rawData = json.load(f)
        if not keyIdName:
            return rawData
        # IDs in keys, rows in values
        data = []
        for k, v in rawData.items():
            row = {}
            row.update(v)
            if keyIdName not in row:
                row[keyIdName] = int(k)
            data.append(row)
        return data

    def _addRows(data, cls, fieldMap=None):
        if fieldMap is None:
            fieldMap = {}
        for row in data:
            instance = cls()
            for k, v in row.items():
                if isinstance(v, str):
                    v = v.strip()
                setattr(instance, fieldMap.get(k, k), v)
            eos.db.gamedata_session.add(instance)

    def processEveTypes():
        print('processing evetypes')
        data = _readData('fsd_lite', 'evetypes', keyIdName='typeID')
        for row in data:
            if (
                # Apparently people really want Civilian modules available
                (row['typeName'].startswith('Civilian') and "Shuttle" not in row['typeName']) or
                row['typeName'] in ('Capsule', 'Dark Blood Tracking Disruptor')
            ):
                row['published'] = True
            elif row['typeName'].startswith('Limited Synth '):
                row['published'] = False

        newData = []
        for row in data:
            if (
                row['published'] or
                # group Ship Modifiers, for items like tactical t3 ship modes
                row['groupID'] == 1306 or
                # Micro Bombs (Fighters)
                row['typeID'] in (41549, 41548, 41551, 41550) or
                # Abyssal weather (environment)
                row['groupID'] in (
                1882,
                1975,
                1971,
                # the "container" for the abyssal environments
                1983)
            ):
                newData.append(row)

        _addRows(newData, eos.gamedata.Item)
        return newData

    def processEveGroups():
        print('processing evegroups')
        data = _readData('fsd_lite', 'evegroups', keyIdName='groupID')
        _addRows(data, eos.gamedata.Group)
        return data

    def processEveCategories():
        print('processing evecategories')
        data = _readData('fsd_lite', 'evecategories', keyIdName='categoryID')
        _addRows(data, eos.gamedata.Category)

    def processDogmaAttributes():
        print('processing dogmaattributes')
        data = _readData('fsd_binary', 'dogmaattributes', keyIdName='attributeID')
        _addRows(data, eos.gamedata.AttributeInfo)

    def processDogmaTypeAttributes(eveTypesData):
        print('processing dogmatypeattributes')
        data = _readData('fsd_binary', 'typedogma', keyIdName='typeID')
        eveTypeIds = set(r['typeID'] for r in eveTypesData)
        newData = []
        seenKeys = set()

        def checkKey(key):
            if key in seenKeys:
                return False
            seenKeys.add(key)
            return True

        for typeData in data:
            if typeData['typeID'] not in eveTypeIds:
                continue
            for row in typeData.get('dogmaAttributes', ()):
                row['typeID'] = typeData['typeID']
                if checkKey((row['typeID'], row['attributeID'])):
                    newData.append(row)
        for row in eveTypesData:
            for attrId, attrName in {4: 'mass', 38: 'capacity', 161: 'volume', 162: 'radius'}.items():
                if attrName in row and checkKey((row['typeID'], attrId)):
                    newData.append({'typeID': row['typeID'], 'attributeID': attrId, 'value': row[attrName]})

        _addRows(newData, eos.gamedata.Attribute)
        return newData

    def processDynamicItemAttributes():
        print('processing dynamicitemattributes')
        data = _readData('fsd_binary', 'dynamicitemattributes')
        for mutaID, mutaData in data.items():
            muta = eos.gamedata.DynamicItem()
            muta.typeID = mutaID
            muta.resultingTypeID = mutaData['inputOutputMapping'][0]['resultingType']
            eos.db.gamedata_session.add(muta)

            for x in mutaData['inputOutputMapping'][0]['applicableTypes']:
                item = eos.gamedata.DynamicItemItem()
                item.typeID = mutaID
                item.applicableTypeID = x
                eos.db.gamedata_session.add(item)

            for attrID, attrData in mutaData['attributeIDs'].items():
                attr = eos.gamedata.DynamicItemAttribute()
                attr.typeID = mutaID
                attr.attributeID = attrID
                attr.min = attrData['min']
                attr.max = attrData['max']
                eos.db.gamedata_session.add(attr)

    def processDogmaEffects():
        print('processing dogmaeffects')
        data = _readData('fsd_binary', 'dogmaeffects', keyIdName='effectID')
        _addRows(data, eos.gamedata.Effect, fieldMap={'resistanceAttributeID': 'resistanceID'})

    def processDogmaTypeEffects(eveTypesData):
        print('processing dogmatypeeffects')
        data = _readData('fsd_binary', 'typedogma', keyIdName='typeID')
        eveTypeIds = set(r['typeID'] for r in eveTypesData)
        newData = []
        for typeData in data:
            if typeData['typeID'] not in eveTypeIds:
                continue
            for row in typeData.get('dogmaEffects', ()):
                row['typeID'] = typeData['typeID']
                newData.append(row)
        _addRows(newData, eos.gamedata.ItemEffect)
        return newData

    def processDogmaUnits():
        print('processing dogmaunits')
        data = _readData('fsd_binary', 'dogmaunits', keyIdName='unitID')
        _addRows(data, eos.gamedata.Unit, fieldMap={'name': 'unitName'})

    def processMarketGroups():
        print('processing marketgroups')
        data = _readData('fsd_binary', 'marketgroups', keyIdName='marketGroupID')
        _addRows(data, eos.gamedata.MarketGroup, fieldMap={'name': 'marketGroupName'})

    def processMetaGroups():
        print('processing metagroups')
        data = _readData('fsd_binary', 'metagroups', keyIdName='metaGroupID')
        _addRows(data, eos.gamedata.MetaGroup)

    def processCloneGrades():
        print('processing clonegrades')
        data = _readData('fsd_lite', 'clonegrades')

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

        tmp = []
        for row in newData:
            if row['alphaCloneID'] not in tmp:
                cloneParent = eos.gamedata.AlphaClone()
                setattr(cloneParent, 'alphaCloneID', row['alphaCloneID'])
                setattr(cloneParent, 'alphaCloneName', row['alphaCloneName'])
                eos.db.gamedata_session.add(cloneParent)
                tmp.append(row['alphaCloneID'])
        _addRows(newData, eos.gamedata.AlphaCloneSkill)

    def processTraits():
        print('processing traits')
        data = _readData('phobos', 'traits')

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

        _addRows(newData, eos.gamedata.Traits)

    def processMetadata():
        print('processing metadata')
        data = _readData('phobos', 'metadata')
        _addRows(data, eos.gamedata.MetaData)

    def processReqSkills(eveTypesData):
        print('processing requiredskillsfortypes')

        def composeReqSkills(raw):
            reqSkills = {}
            for skillTypeID, skillLevel in raw.items():
                reqSkills[int(skillTypeID)] = skillLevel
            return reqSkills

        eveTypeIds = set(r['typeID'] for r in eveTypesData)
        data = _readData('fsd_binary', 'requiredskillsfortypes')
        reqsByItem = {}
        itemsByReq = {}
        for typeID, skillreqData in data.items():
            typeID = int(typeID)
            if typeID not in eveTypeIds:
                continue
            for skillTypeID, skillLevel in composeReqSkills(skillreqData).items():
                reqsByItem.setdefault(typeID, {})[skillTypeID] = skillLevel
                itemsByReq.setdefault(skillTypeID, {})[typeID] = skillLevel
        for item in eos.db.gamedata_session.query(eos.gamedata.Item).all():
            if item.typeID in reqsByItem:
                item.reqskills = json.dumps(reqsByItem[item.typeID])
            if item.typeID in itemsByReq:
                item.requiredfor = json.dumps(itemsByReq[item.typeID])

    def processReplacements(eveTypesData, eveGroupsData, dogmaTypeAttributesData, dogmaTypeEffectsData):
        print('finding item replacements')

        def compareAttrs(attrs1, attrs2):
            # Consider items as different if they have no attrs
            if len(attrs1) == 0 and len(attrs2) == 0:
                return False
            if set(attrs1) != set(attrs2):
                return False
            if all(attrs1[aid] == attrs2[aid] for aid in attrs1):
                return True
            return False

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
        for row in eveTypesData:
            typesGroups[row['typeID']] = row['groupID']
        # Get data on item effects
        # Format: {type ID: set(effect, IDs)}
        typesEffects = {}
        for row in dogmaTypeEffectsData:
            typesEffects.setdefault(row['typeID'], set()).add(row['effectID'])
        # Get data on type attributes
        # Format: {type ID: {attribute ID: attribute value}}
        typesNormalAttribs = {}
        typesSkillAttribs = {}
        for row in dogmaTypeAttributesData:
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
        for row in eveGroupsData:
            groupCategories[row['groupID']] = row['categoryID']
        # As EVE affects various types mostly depending on their group or skill requirements,
        # we're going to group various types up this way
        # Format: {(group ID, frozenset(skillreq, type, IDs), frozenset(type, effect, IDs): [type ID, {attribute ID: attribute value}]}
        groupedData = {}
        for row in eveTypesData:
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
        # Update DB session with data we generated
        for item in eos.db.gamedata_session.query(eos.gamedata.Item).all():
            itemReplacements = replacements.get(item.typeID)
            if itemReplacements is not None:
                item.replacements = ','.join('{}'.format(tid) for tid in sorted(itemReplacements))

    def processImplantSets(eveTypesData):
        print('composing implant sets')
        # Includes only implants which can be considered part of sets, not all implants
        implant_groups = (300, 1730)
        specials = {'Genolution': ('Genolution Core Augmentation', r'CA-\d+')}
        implantSets = {}
        for row in eveTypesData:
            if not row.get('published'):
                continue
            if row.get('groupID') not in implant_groups:
                continue
            typeName = row.get('typeName', '')
            # Regular sets matching
            m = re.match('(?P<grade>(High|Mid|Low)-grade) (?P<set>\w+) (?P<implant>(Alpha|Beta|Gamma|Delta|Epsilon|Omega))', typeName, re.IGNORECASE)
            if m:
                implantSets.setdefault((m.group('grade'), m.group('set')), set()).add(row['typeID'])
            # Special set matching
            for setHandle, (setName, implantPattern) in specials.items():
                pattern = '(?P<set>{}) (?P<implant>{})'.format(setName, implantPattern)
                m = re.match(pattern, typeName)
                if m:
                    implantSets.setdefault((None, setHandle), set()).add(row['typeID'])
                    break
        data = []
        for (gradeName, setName), implants in implantSets.items():
            if len(implants) < 2:
                continue
            implants = ','.join('{}'.format(tid) for tid in sorted(implants))
            row = {'setName': setName, 'gradeName': gradeName, 'implants': implants}
            data.append(row)
        _addRows(data, eos.gamedata.ImplantSet)

    eveTypesData = processEveTypes()
    eveGroupsData = processEveGroups()
    processEveCategories()
    processDogmaAttributes()
    dogmaTypeAttributesData = processDogmaTypeAttributes(eveTypesData)
    processDynamicItemAttributes()
    processDogmaEffects()
    dogmaTypeEffectsData = processDogmaTypeEffects(eveTypesData)
    processDogmaUnits()
    processMarketGroups()
    processMetaGroups()
    processCloneGrades()
    processTraits()
    processMetadata()

    eos.db.gamedata_session.flush()
    processReqSkills(eveTypesData)
    processReplacements(eveTypesData, eveGroupsData, dogmaTypeAttributesData, dogmaTypeEffectsData)
    processImplantSets(eveTypesData)

    # Add schema version to prevent further updates
    metadata_schema_version = eos.gamedata.MetaData()
    metadata_schema_version.field_name = 'schema_version'
    metadata_schema_version.field_value = GAMEDATA_SCHEMA_VERSION
    eos.db.gamedata_session.add(metadata_schema_version)

    eos.db.gamedata_session.flush()

    # CCP still has 5 subsystems assigned to T3Cs, even though only 4 are available / usable. They probably have some
    # old legacy requirement or assumption that makes it difficult for them to change this value in the data. But for
    # pyfa, we can do it here as a post-processing step
    for attr in eos.db.gamedata_session.query(eos.gamedata.Attribute).filter(eos.gamedata.Attribute.ID == 1367).all():
        attr.value = 4.0
    for item in eos.db.gamedata_session.query(eos.gamedata.Item).filter(eos.gamedata.Item.name.like('%abyssal%')).all():
        item.published = False

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
