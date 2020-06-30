# ===============================================================================
# Copyright (C) 2010 Diego Duclos
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
# ===============================================================================

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import aliased, exc, join
from sqlalchemy.sql import and_, or_, select

import eos.config
from eos.db import get_gamedata_session
from eos.db.gamedata.item import items_table
from eos.db.gamedata.group import groups_table
from eos.db.util import processEager, processWhere
from eos.gamedata import AlphaClone, Attribute, AttributeInfo, Category, DynamicItem, Group, Item, MarketGroup, MetaData, MetaGroup, ImplantSet

cache = {}
configVal = getattr(eos.config, "gamedataCache", None)
if configVal is True:
    def cachedQuery(amount, *keywords):
        def deco(function):
            def checkAndReturn(*args, **kwargs):
                useCache = kwargs.pop("useCache", True)
                cacheKey = []
                cacheKey.extend(args)
                for keyword in keywords:
                    cacheKey.append(kwargs.get(keyword))

                cacheKey = tuple(cacheKey)
                handler = cache.get(cacheKey)
                if handler is None or not useCache:
                    handler = cache[cacheKey] = function(*args, **kwargs)

                return handler

            return checkAndReturn

        return deco

elif callable(configVal):
    cachedQuery = eos.config.gamedataCache
else:
    def cachedQuery(amount, *keywords):
        def deco(function):
            def checkAndReturn(*args, **kwargs):
                return function(*args, **kwargs)

            return checkAndReturn

        return deco


def sqlizeNormalString(line):
    # Escape backslashes first, as they will be as escape symbol in queries
    # Then escape percent and underscore signs
    # Finally, replace generic wildcards with sql-style wildcards
    line = line.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_").replace("*", "%")
    return line


itemNameMap = {}


@cachedQuery(1, "lookfor")
def getItem(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            item = get_gamedata_session().query(Item).get(lookfor)
        else:
            item = get_gamedata_session().query(Item).options(*processEager(eager)).filter(Item.ID == lookfor).first()
    elif isinstance(lookfor, str):
        if lookfor in itemNameMap:
            id = itemNameMap[lookfor]
            if eager is None:
                item = get_gamedata_session().query(Item).get(id)
            else:
                item = get_gamedata_session().query(Item).options(*processEager(eager)).filter(Item.ID == id).first()
        else:
            # Item names are unique, so we can use first() instead of one()
            item = get_gamedata_session().query(Item).options(*processEager(eager)).filter(Item.typeName == lookfor).first()
            if item is not None:
                itemNameMap[lookfor] = item.ID
    else:
        raise TypeError("Need integer or string as argument")
    return item

@cachedQuery(1, "itemIDs")
def getItems(itemIDs, eager=None):
    if not isinstance(itemIDs, (tuple, list, set)) or not all(isinstance(t, int) for t in itemIDs):
        raise TypeError("Need iterable of integers as argument")
    if eager is None:
        items = get_gamedata_session().query(Item).filter(Item.ID.in_(itemIDs)).all()
    else:
        items = get_gamedata_session().query(Item).options(*processEager(eager)).filter(Item.ID.in_(itemIDs)).all()
    return items


def getMutaplasmid(lookfor, eager=None):
    if isinstance(lookfor, int):
        item = get_gamedata_session().query(DynamicItem).filter(DynamicItem.ID == lookfor).first()
    else:
        raise TypeError("Need integer as argument")
    return item


def getItemWithBaseItemAttribute(lookfor, baseItemID, eager=None):
    # A lot of this is described in more detail in #1597
    item = get_gamedata_session().query(Item).get(lookfor)
    base = getItem(baseItemID)

    # we have to load all attributes for this object, otherwise we'll lose access to them when we expunge.
    # todo: figure out a way to eagerly load all these via the query...
    for x in [*inspect(Item).relationships.keys(), 'description']:
        getattr(item, x)

    # Copy over the attributes from the base, but ise the items attributes when there's an overlap
    # WARNING: the attribute object still has the old typeID. I don't believe we access this typeID anywhere in the code,
    # but should keep this in mind for now.
    item._Item__attributes = {**base.attributes, **item.attributes}

    # Expunge the item form the session. This is required to have different Abyssal / Base combinations loaded in memory.
    # Without expunging it, once one Abyssal Web is created, SQLAlchmey will use it for all others. We don't want this,
    # we want to generate a completely new object to work with
    get_gamedata_session().expunge(item)
    return item


@cachedQuery(1, "lookfor")
def getItems(lookfor, eager=None):
    """
    Gets a list of items. Does a bit of cache hackery to get working properly -- cache
    is usually based on function calls with the parameters, needed to extract data directly.
    Works well enough. Not currently used, but it's here for possible future inclusion
    """

    toGet = []
    results = []

    for id in lookfor:
        if (id, None) in cache:
            results.append(cache.get((id, None)))
        else:
            toGet.append(id)

    if len(toGet) > 0:
        # Get items that aren't currently cached, and store them in the cache
        items = get_gamedata_session().query(Item).filter(Item.ID.in_(toGet)).all()
        for item in items:
            cache[(item.ID, None)] = item
        results += items

    # sort the results based on the original indexing
    results.sort(key=lambda x: lookfor.index(x.ID))
    return results


@cachedQuery(1, "lookfor")
def getAlphaClone(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            item = get_gamedata_session().query(AlphaClone).get(lookfor)
        else:
            item = get_gamedata_session().query(AlphaClone).options(*processEager(eager)).filter(AlphaClone.ID == lookfor).first()
    else:
        raise TypeError("Need integer as argument")
    return item


def getAlphaCloneList(eager=None):
    eager = processEager(eager)
    clones = get_gamedata_session().query(AlphaClone).options(*eager).all()
    return clones


groupNameMap = {}


@cachedQuery(1, "lookfor")
def getGroup(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            group = get_gamedata_session().query(Group).get(lookfor)
        else:
            group = get_gamedata_session().query(Group).options(*processEager(eager)).filter(Group.ID == lookfor).first()
    elif isinstance(lookfor, str):
        if lookfor in groupNameMap:
            id = groupNameMap[lookfor]
            if eager is None:
                group = get_gamedata_session().query(Group).get(id)
            else:
                group = get_gamedata_session().query(Group).options(*processEager(eager)).filter(Group.ID == id).first()
        else:
            # Group names are unique, so we can use first() instead of one()
            group = get_gamedata_session().query(Group).options(*processEager(eager)).filter(Group.name == lookfor).first()
            if group is not None:
                groupNameMap[lookfor] = group.ID
    else:
        raise TypeError("Need integer or string as argument")
    return group


categoryNameMap = {}


@cachedQuery(1, "lookfor")
def getCategory(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            category = get_gamedata_session().query(Category).get(lookfor)
        else:
            category = get_gamedata_session().query(Category).options(*processEager(eager)).filter(
                    Category.ID == lookfor).first()
    elif isinstance(lookfor, str):
        if lookfor in categoryNameMap:
            id = categoryNameMap[lookfor]
            if eager is None:
                category = get_gamedata_session().query(Category).get(id)
            else:
                category = get_gamedata_session().query(Category).options(*processEager(eager)).filter(
                        Category.ID == id).first()
        else:
            # Category names are unique, so we can use first() instead of one()
            category = get_gamedata_session().query(Category).options(*processEager(eager)).filter(
                    Category.name == lookfor).first()
            if category is not None:
                categoryNameMap[lookfor] = category.ID
    else:
        raise TypeError("Need integer or string as argument")
    return category


metaGroupNameMap = {}


@cachedQuery(1, "lookfor")
def getMetaGroup(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            metaGroup = get_gamedata_session().query(MetaGroup).get(lookfor)
        else:
            metaGroup = get_gamedata_session().query(MetaGroup).options(*processEager(eager)).filter(
                    MetaGroup.ID == lookfor).first()
    elif isinstance(lookfor, str):
        if lookfor in metaGroupNameMap:
            id = metaGroupNameMap[lookfor]
            if eager is None:
                metaGroup = get_gamedata_session().query(MetaGroup).get(id)
            else:
                metaGroup = get_gamedata_session().query(MetaGroup).options(*processEager(eager)).filter(
                        MetaGroup.ID == id).first()
        else:
            # MetaGroup names are unique, so we can use first() instead of one()
            metaGroup = get_gamedata_session().query(MetaGroup).options(*processEager(eager)).filter(
                    MetaGroup.metaGroupName == lookfor).first()
            if metaGroup is not None:
                metaGroupNameMap[lookfor] = metaGroup.ID
    else:
        raise TypeError("Need integer or string as argument")
    return metaGroup


def getMetaGroups():
    return get_gamedata_session().query(MetaGroup).all()


@cachedQuery(1, "lookfor")
def getMarketGroup(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            marketGroup = get_gamedata_session().query(MarketGroup).get(lookfor)
        else:
            marketGroup = get_gamedata_session().query(MarketGroup).options(*processEager(eager)).filter(
                    MarketGroup.ID == lookfor).first()
    else:
        raise TypeError("Need integer as argument")
    return marketGroup


def getMarketTreeNodeIds(rootNodeIds):
    allIds = set()
    addedIds = set(rootNodeIds)
    while addedIds:
        allIds.update(addedIds)
        addedIds = {mg.ID for mg in get_gamedata_session().query(MarketGroup).filter(MarketGroup.parentGroupID.in_(addedIds))}
    return allIds


@cachedQuery(2, "where", "filter")
def getItemsByCategory(filter, where=None, eager=None):
    if isinstance(filter, int):
        filter = Category.ID == filter
    elif isinstance(filter, str):
        filter = Category.name == filter
    else:
        raise TypeError("Need integer or string as argument")

    filter = processWhere(filter, where)
    return get_gamedata_session().query(Item).options(*processEager(eager)).join(Item.group, Group.category).filter(
            filter).all()


@cachedQuery(3, "where", "nameLike", "join")
def searchItems(nameLike, where=None, join=None, eager=None):
    if not isinstance(nameLike, str):
        raise TypeError("Need string as argument")

    if join is None:
        join = tuple()

    if not hasattr(join, "__iter__"):
        join = (join,)

    items = get_gamedata_session().query(Item).options(*processEager(eager)).join(*join)
    for token in nameLike.split(' '):
        token_safe = "%{0}%".format(sqlizeNormalString(token))
        if where is not None:
            items = items.filter(and_(Item.name.like(token_safe, escape="\\"), where))
        else:
            items = items.filter(Item.name.like(token_safe, escape="\\"))
    items = items.limit(100).all()
    return items


@cachedQuery(3, "tokens", "where", "join")
def searchItemsRegex(tokens, where=None, join=None, eager=None):
    if not isinstance(tokens, (tuple, list)) or not all(isinstance(t, str) for t in tokens):
        raise TypeError("Need tuple or list of strings as argument")

    if join is None:
        join = tuple()

    if not hasattr(join, "__iter__"):
        join = (join,)

    items = get_gamedata_session().query(Item).options(*processEager(eager)).join(*join)
    for token in tokens:
        if where is not None:
            items = items.filter(and_(Item.name.op('regexp')(token), where))
        else:
            items = items.filter(Item.name.op('regexp')(token))
    items = items.limit(100).all()
    return items


@cachedQuery(3, "where", "nameLike", "join")
def searchSkills(nameLike, where=None, eager=None):
    if not isinstance(nameLike, str):
        raise TypeError("Need string as argument")

    items = get_gamedata_session().query(Item).options(*processEager(eager)).join(Item.group, Group.category)
    for token in nameLike.split(' '):
        token_safe = "%{0}%".format(sqlizeNormalString(token))
        if where is not None:
            items = items.filter(and_(Item.name.like(token_safe, escape="\\"), Category.ID == 16, where))
        else:
            items = items.filter(and_(Item.name.like(token_safe, escape="\\"), Category.ID == 16))
    items = items.limit(100).all()
    return items


@cachedQuery(2, "where", "itemids")
def getVariations(itemids, groupIDs=None, where=None, eager=None):
    for itemid in itemids:
        if not isinstance(itemid, int):
            raise TypeError("All passed item IDs must be integers")
    # Get out if list of provided IDs is empty
    if len(itemids) == 0:
        return []

    itemfilter = or_(*(items_table.c.variationParentTypeID == itemid for itemid in itemids))
    filter = processWhere(itemfilter, where)
    vars = get_gamedata_session().query(Item).options(*processEager(eager)).filter(filter).all()

    if vars:
        return vars
    elif groupIDs:
        itemfilter = or_(*(groups_table.c.groupID == groupID for groupID in groupIDs))
        filter = processWhere(itemfilter, where)
        joinon = items_table.c.groupID == groups_table.c.groupID
        vars = get_gamedata_session().query(Item).options(*processEager(eager)).join((groups_table, joinon)).filter(
                filter).all()

    return vars


@cachedQuery(1, "attr")
def getAttributeInfo(attr, eager=None):
    if isinstance(attr, str):
        filter = AttributeInfo.name == attr
    elif isinstance(attr, int):
        filter = AttributeInfo.ID == attr
    else:
        raise TypeError("Need integer or string as argument")
    try:
        result = get_gamedata_session().query(AttributeInfo).options(*processEager(eager)).filter(filter).one()
    except exc.NoResultFound:
        result = None
    return result


@cachedQuery(1, "field")
def getMetaData(field):
    if isinstance(field, str):
        data = get_gamedata_session().query(MetaData).get(field)
    else:
        raise TypeError("Need string as argument")
    return data


@cachedQuery(2, "itemIDs", "attributeID")
def directAttributeRequest(itemIDs, attrIDs):
    for itemID in itemIDs:
        if not isinstance(itemID, int):
            raise TypeError("All attrIDs must be integer")
    for itemID in itemIDs:
        if not isinstance(itemID, int):
            raise TypeError("All itemIDs must be integer")

    q = select((Item.typeID, Attribute.attributeID, Attribute.value),
               and_(Attribute.attributeID.in_(attrIDs), Item.typeID.in_(itemIDs)),
               from_obj=[join(Attribute, Item)])

    result = get_gamedata_session().execute(q).fetchall()
    return result


def getAbyssalTypes():
    return set([r.resultingTypeID for r in get_gamedata_session().query(DynamicItem.resultingTypeID).distinct()])


@cachedQuery(1, "itemID")
def getDynamicItem(itemID, eager=None):
    try:
        if isinstance(itemID, int):
            if eager is None:
                result = get_gamedata_session().query(DynamicItem).filter(DynamicItem.ID == itemID).one()
            else:
                result = get_gamedata_session().query(DynamicItem).options(*processEager(eager)).filter(DynamicItem.ID == itemID).one()
        else:
            raise TypeError("Need integer as argument")
    except exc.NoResultFound:
        result = None
    return result


@cachedQuery(1, "lookfor")
def getAllImplantSets():
    implantSets = get_gamedata_session().query(ImplantSet).all()
    return implantSets
