# =============================================================================
# Copyright (C) 2014 Ryan Holmes
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


import re

from eos.db.gamedata.queries import getAttributeInfo, getDynamicItem
from eos.utils.float import floatUnerr
from service.port.shared import fetchItem
from service.esiAccess import EsiAccess


def renderMutant(mutant, firstPrefix='', prefix=''):
    exportLines = []
    mutatedAttrs = {}
    for attrID, mutator in mutant.mutators.items():
        attrName = getAttributeInfo(attrID).name
        mutatedAttrs[attrName] = mutator.value
    exportLines.append('{}{}'.format(firstPrefix, mutant.baseItem.name))
    exportLines.append('{}{}'.format(prefix, mutant.mutaplasmid.item.name))
    customAttrsLine = ', '.join(
        '{} {}'.format(a, floatUnerr(mutatedAttrs[a]))
        for a in sorted(mutatedAttrs))
    exportLines.append('{}{}'.format(prefix, customAttrsLine))
    return '\n'.join(exportLines)


def parseMutant(lines):
    # Fetch base item type
    try:
        baseItemName = lines[0]
    except IndexError:
        return None
    baseItem = fetchItem(baseItemName.strip())
    if baseItem is None:
        return None, None, {}
    # Fetch mutaplasmid item type and actual item
    try:
        mutaplasmidName = lines[1]
    except IndexError:
        return baseItem, None, {}
    mutaplasmidItem = fetchItem(mutaplasmidName.strip())
    if mutaplasmidItem is None:
        return baseItem, None, {}
    mutaplasmidItem = getDynamicItem(mutaplasmidItem.ID)
    # Process mutated attribute values
    try:
        mutationsLine = lines[2]
    except IndexError:
        return baseItem, mutaplasmidItem, {}
    mutations = {}
    pairs = [p.strip() for p in mutationsLine.split(',')]
    for pair in pairs:
        try:
            attrName, value = pair.split(' ')
        except ValueError:
            continue
        try:
            value = float(value)
        except (ValueError, TypeError):
            continue
        attrInfo = getAttributeInfo(attrName.strip())
        if attrInfo is None:
            continue
        mutations[attrInfo.ID] = value
    return baseItem, mutaplasmidItem, mutations


def parseDynamicItemString(text):
    m = re.search(r'<url=showinfo:(?P<typeid>\d+)//(?P<itemid>\d+)>.+</url>', text)
    if m:
        typeID = int(m.group('typeid'))
        itemID = int(m.group('itemid'))
        return typeID, itemID
    return None


def fetchDynamicItem(dynamicItemData):
    typeID, itemID = dynamicItemData
    esiData = EsiAccess().getDynamicItem(typeID, itemID).json()
    baseItemID = esiData['source_type_id']
    mutaplasmidID = esiData['mutator_type_id']
    attrs = {i['attribute_id']: i['value'] for i in esiData['dogma_attributes']}
    baseItem = fetchItem(baseItemID)
    mutaplasmid = getDynamicItem(mutaplasmidID)
    return baseItem, mutaplasmid, attrs
