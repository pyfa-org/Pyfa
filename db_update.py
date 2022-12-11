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

import sqlalchemy.orm
from sqlalchemy import or_, and_


# todo: need to set the EOS language to en, becasuse this assumes it's being run within an English context
# Need to know what that would do if called from pyfa
ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT_DIR, 'eve.db')
JSON_DIR = os.path.join(ROOT_DIR, 'staticdata')
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
GAMEDATA_SCHEMA_VERSION = 4


def db_needs_update():
    """True if needs, false if it does not, none if we cannot check it."""
    try:
        with open(os.path.join(JSON_DIR, 'phobos', 'metadata.0.json')) as f:
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
    import eos.config

    # Create the database tables
    eos.db.gamedata_meta.create_all()

    def _readData(minerName, jsonName, keyIdName=None):
        compiled_data = None
        for i in itertools.count(0):
            try:
                with open(os.path.join(JSON_DIR, minerName, '{}.{}.json'.format(jsonName, i)), encoding='utf-8') as f:
                    rawData = json.load(f)
                    if i == 0:
                        compiled_data = {} if type(rawData) == dict else []
                    if type(rawData) == dict:
                        compiled_data.update(rawData)
                    else:
                        compiled_data.extend(rawData)
            except FileNotFoundError:
                break

        if not keyIdName:
            return compiled_data
        # IDs in keys, rows in values
        data = []
        for k, v in compiled_data.items():
            row = {}
            row.update(v)
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
        data = _readData('fsd_binary', 'types', keyIdName='typeID')
        for row in data:
            if (
                # Apparently people really want Civilian modules available
                (row['typeName_en-us'].startswith('Civilian') and "Shuttle" not in row['typeName_en-us'])
                or row['typeName_en-us'] == 'Capsule'
                or row['groupID'] == 4033  # destructible effect beacons
                or re.match('AIR .+Booster.*', row['typeName_en-us'])
            ):
                row['published'] = True
            # Nearly useless and clutter search results too much
            elif (
                row['typeName_en-us'].startswith('Limited Synth ')
                or row['typeName_en-us'].startswith('Expired ')
                or re.match('Mining Blitz .+ Booster Dose .+', row['typeName_en-us'])
                or row['typeName_en-us'].endswith(' Filament') and (
                    "'Needlejack'" not in row['typeName_en-us'] and
                    "'Devana'" not in row['typeName_en-us'] and
                    "'Pochven'" not in row['typeName_en-us'] and
                    "'Extraction'" not in row['typeName_en-us'] and
                    "'Krai Veles'" not in row['typeName_en-us'] and
                    "'Krai Perun'" not in row['typeName_en-us'] and
                    "'Krai Svarog'" not in row['typeName_en-us']
                )
            ):
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
                    1983)  # the "container" for the abyssal environments
            ):
                newData.append(row)
        map = {'typeName_en-us': 'typeName', 'description_en-us': '_description'}
        map.update({'description'+v: '_description'+v for (k, v) in eos.config.translation_mapping.items() if k != 'en'})
        _addRows(newData, eos.gamedata.Item, fieldMap=map)
        return newData

    def processEveGroups():
        print('processing evegroups')
        data = _readData('fsd_binary', 'groups', keyIdName='groupID')
        map = {'groupName_en-us': 'name'}
        map.update({'groupName'+v: 'name'+v for (k, v) in eos.config.translation_mapping.items() if k != 'en'})
        _addRows(data, eos.gamedata.Group, fieldMap=map)
        return data

    def processEveCategories():
        print('processing evecategories')
        data = _readData('fsd_binary', 'categories', keyIdName='categoryID')
        map = { 'categoryName_en-us': 'name' }
        map.update({'categoryName'+v: 'name'+v for (k, v) in eos.config.translation_mapping.items() if k != 'en'})
        _addRows(data, eos.gamedata.Category, fieldMap=map)

    def processDogmaAttributes():
        print('processing dogmaattributes')
        data = _readData('fsd_binary', 'dogmaattributes', keyIdName='attributeID')
        map = {
            'displayName_en-us': 'displayName',
            # 'tooltipDescription_en-us': 'tooltipDescription'
        }
        _addRows(data, eos.gamedata.AttributeInfo, fieldMap=map)

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
        _addRows(data, eos.gamedata.Unit, fieldMap={
            'name': 'unitName',
            'displayName_en-us': 'displayName'
        })

    def processMarketGroups():
        print('processing marketgroups')
        data = _readData('fsd_binary', 'marketgroups', keyIdName='marketGroupID')
        map = {
            'name_en-us': 'marketGroupName',
            'description_en-us': '_description',
        }
        map.update({'name'+v: 'marketGroupName'+v for (k, v) in eos.config.translation_mapping.items() if k != 'en'})
        map.update({'description' + v: '_description' + v for (k, v) in eos.config.translation_mapping.items() if k != 'en'})
        _addRows(data, eos.gamedata.MarketGroup, fieldMap=map)

    def processMetaGroups():
        print('processing metagroups')
        data = _readData('fsd_binary', 'metagroups', keyIdName='metaGroupID')
        map = {'name_en-us': 'metaGroupName'}
        map.update({'name' + v: 'metaGroupName' + v for (k, v) in eos.config.translation_mapping.items() if k != 'en'})
        _addRows(data, eos.gamedata.MetaGroup, fieldMap=map)

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
            try:
                newRow = {
                    'typeID': row['typeID'],
                }
                for (k, v) in eos.config.translation_mapping.items():
                    if v == '':
                        v = '_en-us'
                    typeLines = []
                    traitData = row['traits{}'.format(v)]
                    for skillData in sorted(traitData.get('skills', ()), key=lambda i: i['header']):
                        typeLines.append(convertSection(skillData))
                    if 'role' in traitData:
                        typeLines.append(convertSection(traitData['role']))
                    if 'misc' in traitData:
                        typeLines.append(convertSection(traitData['misc']))
                    traitLine = '<br />\n<br />\n'.join(typeLines)
                    newRow['traitText{}'.format(v)] = traitLine

                newData.append(newRow)
            except:
                pass
        _addRows(newData, eos.gamedata.Traits, fieldMap={'traitText_en-us': 'traitText'})

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
            typeName = row.get('typeName_en-us', '')
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
    for item in eos.db.gamedata_session.query(eos.gamedata.Item).filter(or_(
        eos.gamedata.Item.name.like('%abyssal%'),
        eos.gamedata.Item.name.like('%mutated%'),
        eos.gamedata.Item.name.like('%_PLACEHOLDER%'),
        # Drifter weapons are published for some reason
        eos.gamedata.Item.name.in_(('Lux Kontos', 'Lux Xiphos'))
    )).all():
        if 'Asteroid Mining Crystal' in item.name:
            continue
        if 'Mutated Drone Specialization' in item.name:
            continue
        item.published = False

    for x in [
        30  # Apparel
    ]:
        cat = eos.db.gamedata_session.query(eos.gamedata.Category).filter(eos.gamedata.Category.ID == x).first()
        print ('Removing Category: {}'.format(cat.name))
        eos.db.gamedata_session.delete(cat)

    # Unused normally, can be useful for customizing items
    def _hardcodeAttribs(typeID, attrMap):
        for attrName, value in attrMap.items():
            try:
                attr = eos.db.gamedata_session.query(eos.gamedata.Attribute).filter(and_(
                    eos.gamedata.Attribute.name == attrName, eos.gamedata.Attribute.typeID == typeID)).one()
            except sqlalchemy.orm.exc.NoResultFound:
                attrInfo = eos.db.gamedata_session.query(eos.gamedata.AttributeInfo).filter(eos.gamedata.AttributeInfo.name == attrName).one()
                attr = eos.gamedata.Attribute()
                attr.ID = attrInfo.ID
                attr.typeID = typeID
                attr.value = value
                eos.db.gamedata_session.add(attr)
            else:
                attr.value = value

    def _hardcodeEffects(typeID, effectMap):
        item = eos.db.gamedata_session.query(eos.gamedata.Item).filter(eos.gamedata.Item.ID == typeID).one()
        item.effects.clear()
        for effectID, effectName in effectMap.items():
            effect = eos.gamedata.Effect()
            effect.effectID = effectID
            effect.effectName = effectName
            item.effects[effectName] = effect

    def hardcodeGeri():
        attrMap = {
            # Fitting
            'powerOutput': 50,
            'cpuOutput': 200,
            'capacitorCapacity': 325,
            'rechargeRate': 130000,
            # Slots
            'hiSlots': 5,
            'medSlots': 4,
            'lowSlots': 4,
            'launcherSlotsLeft': 3,
            'turretSlotsLeft': 2,
            # Rigs
            'rigSlots': 2,
            'rigSize': 1,
            'upgradeCapacity': 400,
            # Shield
            'shieldCapacity': 1000,
            'shieldEmDamageResonance': 1 - 0.75,
            'shieldThermalDamageResonance': 1 - 0.6,
            'shieldKineticDamageResonance': 1 - 0.4,
            'shieldExplosiveDamageResonance': 1 - 0.5,
            # Armor
            'armorHP': 1000,
            'armorEmDamageResonance': 1 - 0.9,
            'armorThermalDamageResonance': 1 - 0.675,
            'armorKineticDamageResonance': 1 - 0.25,
            'armorExplosiveDamageResonance': 1 - 0.1,
            # Structure
            'hp': 700,
            'emDamageResonance': 1 - 0.33,
            'thermalDamageResonance': 1 - 0.33,
            'kineticDamageResonance': 1 - 0.33,
            'explosiveDamageResonance': 1 - 0.33,
            'mass': 1309000,
            'volume': 27289,
            'capacity': 260,
            # Navigation
            'maxVelocity': 440,
            'agility': 2.5,
            'warpSpeedMultiplier': 5.5,
            # Drones
            'droneCapacity': 50,
            'droneBandwidth': 10,
            # Targeting
            'maxTargetRange': 42000,
            'maxLockedTargets': 6,
            'scanRadarStrength': 0,
            'scanLadarStrength': 12,
            'scanMagnetometricStrength': 0,
            'scanGravimetricStrength': 0,
            'signatureRadius': 33,
            'scanResolution': 770}
        effectMap = {
            100100: 'pyfaCustomGeriAfExploVel',
            100101: 'pyfaCustomGeriAfRof',
            100102: 'pyfaCustomGeriMfDmg',
            100103: 'pyfaCustomGeriMfRep',
            100104: 'pyfaCustomGeriRoleWebDroneStr',
            100105: 'pyfaCustomGeriRoleWebDroneHP',
            100106: 'pyfaCustomGeriRoleWebDroneSpeed',
            100107: 'pyfaCustomGeriRoleMWDSigBloom'}
        _hardcodeAttribs(74141, attrMap)
        _hardcodeEffects(74141, effectMap)

    def hardcodeBestla():
        attrMap = {
            # Fitting
            'powerOutput': 1300,
            'cpuOutput': 500,
            'capacitorCapacity': 1500,
            'rechargeRate': 200000,
            'hiSlots': 6,
            'medSlots': 5,
            'lowSlots': 5,
            'launcherSlotsLeft': 4,
            'turretSlotsLeft': 2,
            # Rigs
            'rigSlots': 2,
            'rigSize': 2,
            'upgradeCapacity': 400,
            # Shield
            'shieldCapacity': 3000,
            'shieldEmDamageResonance': 1 - 0.75,
            'shieldThermalDamageResonance': 1 - 0.6,
            'shieldKineticDamageResonance': 1 - 0.4,
            'shieldExplosiveDamageResonance': 1 - 0.5,
            # Armor
            'armorHP': 3000,
            'armorEmDamageResonance': 1 - 0.9,
            'armorThermalDamageResonance': 1 - 0.675,
            'armorKineticDamageResonance': 1 - 0.25,
            'armorExplosiveDamageResonance': 1 - 0.1,
            # Structure
            'hp': 1600,
            'emDamageResonance': 1 - 0.33,
            'thermalDamageResonance': 1 - 0.33,
            'kineticDamageResonance': 1 - 0.33,
            'explosiveDamageResonance': 1 - 0.33,
            'mass': 11650000,
            'volume': 96000,
            'capacity': 660,
            # Navigation
            'maxVelocity': 300,
            'agility': 0.47,
            'warpSpeedMultiplier': 4.5,
            # Drones
            'droneCapacity': 125,
            'droneBandwidth': 20,
            # Targeting
            'maxTargetRange': 80000,
            'maxLockedTargets': 7,
            'scanRadarStrength': 0,
            'scanLadarStrength': 22,
            'scanMagnetometricStrength': 0,
            'scanGravimetricStrength': 0,
            'signatureRadius': 120,
            'scanResolution': 340}
        effectMap = {
            100200: 'pyfaCustomBestlaHacExploVel',
            100201: 'pyfaCustomBestlaHacRof',
            100202: 'pyfaCustomBestlaMcDmg',
            100203: 'pyfaCustomBestlaMcRep',
            100204: 'pyfaCustomBestlaRoleWebDroneStr',
            100205: 'pyfaCustomBestlaRoleWebDroneHP',
            100206: 'pyfaCustomBestlaRoleWebDroneSpeed'}
        _hardcodeAttribs(74316, attrMap)
        _hardcodeEffects(74316, effectMap)

    hardcodeGeri()
    hardcodeBestla()


    eos.db.gamedata_session.commit()
    eos.db.gamedata_engine.execute('VACUUM')

    print('done')


if __name__ == '__main__':
    update_db()
