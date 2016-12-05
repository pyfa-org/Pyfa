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

import re
import traceback

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Table
from sqlalchemy import Float
from sqlalchemy import Unicode
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import reconstructor, exc, join
from sqlalchemy.orm import relation, mapper, synonym, deferred
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql import and_, or_, select

from eos.db import gamedata_meta
from eos.db import gamedata_session
from eos.db import saveddata_session
from eos.db.gamedata.cache import cachedQuery
from eos.db.saveddata import queries as eds_queries
from eos.db.util import processEager, processWhere, sqlizeString
from eos.eqBase import EqBase

try:
    from collections import OrderedDict
except ImportError:
    from utils.compat import OrderedDict


class Effect(EqBase):
    """
    The effect handling class, it is used to proxy and load effect handler code,
    as well as a container for extra information regarding effects coming
    from the gamedata db.

    @ivar ID: the ID of this effect
    @ivar name: The name of this effect
    @ivar description: The description of this effect, this is usualy pretty useless
    @ivar published: Wether this effect is published or not, unpublished effects are typicaly unused.
    """
    # Filter to change names of effects to valid python method names
    nameFilter = re.compile("[^A-Za-z0-9]")

    @reconstructor
    def init(self):
        """
        Reconstructor, composes the object as we grab it from the database
        """
        self.__generated = False
        self.__effectModule = None
        self.handlerName = re.sub(self.nameFilter, "", self.name).lower()

    @property
    def handler(self):
        """
        The handler for the effect,
        It is automaticly fetched from effects/<effectName>.py if the file exists
        the first time this property is accessed.
        """
        if not self.__generated:
            self.__generateHandler()

        return self.__handler

    @property
    def runTime(self):
        """
        The runTime that this effect should be run at.
        This property is also automaticly fetched from effects/<effectName>.py if the file exists.
        the possible values are:
        None, "early", "normal", "late"
        None and "normal" are equivalent, and are also the default.

        effects with an early runTime will be ran first when things are calculated,
        followed by effects with a normal runTime and as last effects with a late runTime are ran.
        """
        if not self.__generated:
            self.__generateHandler()

        return self.__runTime

    @property
    def activeByDefault(self):
        """
        The state that this effect should be be in.
        This property is also automaticly fetched from effects/<effectName>.py if the file exists.
        the possible values are:
        None, True, False

        If this is not set:
        We simply assume that missing/none = True, and set it accordingly
        (much as we set runTime to Normalif not otherwise set).
        Nearly all effect files will fall under this category.

        If this is set to True:
        We would enable it anyway, but hey, it's double enabled.
        No effect files are currently configured this way (and probably will never be).

        If this is set to False:
        Basically we simply skip adding the effect to the effect handler when the effect is called,
        much as if the run time didn't match or other criteria failed.
        """
        if not self.__generated:
            self.__generateHandler()

        return self.__activeByDefault

    @activeByDefault.setter
    def activeByDefault(self, value):
        """
        Just assign the input values to the activeByDefault attribute.
        You *could* do something more interesting here if you wanted.
        """
        self.__activeByDefault = value

    @property
    def type(self):
        """
        The type of the effect, automaticly fetched from effects/<effectName>.py if the file exists.

        Valid values are:
        "passive", "active", "projected", "gang", "structure"

        Each gives valuable information to eos about what type the module having
        the effect is. passive vs active gives eos clues about wether to module
        is activatable or not (duh!) and projected and gang each tell eos that the
        module can be projected onto other fits, or used as a gang booster module respectivly
        """
        if not self.__generated:
            self.__generateHandler()

        return self.__type

    @property
    def isImplemented(self):
        """
        Wether this effect is implemented in code or not,
        unimplemented effects simply do nothing at all when run
        """
        return self.handler != effectDummy

    def isType(self, type):
        """
        Check if this effect is of the passed type
        """
        return self.type is not None and type in self.type

    def __generateHandler(self):
        """
        Grab the handler, type and runTime from the effect code if it exists,
        if it doesn't, set dummy values and add a dummy handler
        """
        try:
            self.__effectModule = effectModule = __import__('eos.effects.' + self.handlerName, fromlist=True)
            try:
                self.__handler = getattr(effectModule, "handler")
            except AttributeError:
                print("effect {} exists, but no handler".format(self.handlerName))
                raise

            try:
                self.__runTime = getattr(effectModule, "runTime") or "normal"
            except AttributeError:
                self.__runTime = "normal"

            try:
                self.__activeByDefault = getattr(effectModule, "activeByDefault")
            except AttributeError:
                self.__activeByDefault = True

            try:
                t = getattr(effectModule, "type")
            except AttributeError:
                t = None

            t = t if isinstance(t, tuple) or t is None else (t,)
            self.__type = t
        except (ImportError, AttributeError) as e:
            self.__handler = effectDummy
            self.__runTime = "normal"
            self.__activeByDefault = True
            self.__type = None
        except Exception as e:
            traceback.print_exc(e)

        self.__generated = True

    def getattr(self, key):
        if not self.__generated:
            self.__generateHandler()

        return getattr(self.__effectModule, key, None)


def effectDummy(*args, **kwargs):
    pass


class Item(EqBase):
    MOVE_ATTRS = (4,  # Mass
                  38,  # Capacity
                  161)  # Volume

    MOVE_ATTR_INFO = None

    @classmethod
    def getMoveAttrInfo(cls):
        info = getattr(cls, "MOVE_ATTR_INFO", None)
        if info is None:
            cls.MOVE_ATTR_INFO = info = []
            for id in cls.MOVE_ATTRS:
                info.append(getAttributeInfo(id))

        return info

    def moveAttrs(self):
        self.__moved = True
        for info in self.getMoveAttrInfo():
            val = getattr(self, info.name, 0)
            if val != 0:
                attr = Attribute()
                attr.info = info
                attr.value = val
                self.__attributes[info.name] = attr

    @reconstructor
    def init(self):
        self.__race = None
        self.__requiredSkills = None
        self.__moved = False
        self.__offensive = None
        self.__assistive = None
        self.__overrides = None

    @property
    def attributes(self):
        if not self.__moved:
            self.moveAttrs()

        return self.__attributes

    def getAttribute(self, key):
        if key in self.attributes:
            return self.attributes[key].value

    def isType(self, type):
        for effect in self.effects.itervalues():
            if effect.isType(type):
                return True

        return False

    @property
    def overrides(self):
        if self.__overrides is None:
            self.__overrides = {}
            overrides = eds_queries.getOverrides(self.ID)
            for x in overrides:
                if x.attr.name in self.__attributes:
                    self.__overrides[x.attr.name] = x

        return self.__overrides

    def setOverride(self, attr, value):
        from eos.saveddata.override import Override
        if attr.name in self.__overrides:
            override = self.__overrides.get(attr.name)
            override.value = value
        else:
            override = Override(self, attr, value)
            self.__overrides[attr.name] = override
        eds_queries.save(override)

    def deleteOverride(self, attr):
        override = self.__overrides.pop(attr.name, None)
        saveddata_session.delete(override)
        eds_queries.commit()

    @property
    def requiredSkills(self):
        if self.__requiredSkills is None:
            # This import should be here to make sure it's fully initialized
            from eos.db.gamedata import queries as edg_queries
            requiredSkills = OrderedDict()
            self.__requiredSkills = requiredSkills
            # Map containing attribute IDs we may need for required skills
            # { requiredSkillX : requiredSkillXLevel }
            srqIDMap = {182: 277, 183: 278, 184: 279, 1285: 1286, 1289: 1287, 1290: 1288}
            combinedAttrIDs = set(srqIDMap.iterkeys()).union(set(srqIDMap.itervalues()))
            # Map containing result of the request
            # { attributeID : attributeValue }
            skillAttrs = {}
            # Get relevant attribute values from db (required skill IDs and levels) for our item
            for attrInfo in edg_queries.directAttributeRequest((self.ID,), tuple(combinedAttrIDs)):
                attrID = attrInfo[1]
                attrVal = attrInfo[2]
                skillAttrs[attrID] = attrVal
            # Go through all attributeID pairs
            for srqIDAtrr, srqLvlAttr in srqIDMap.iteritems():
                # Check if we have both in returned result
                if srqIDAtrr in skillAttrs and srqLvlAttr in skillAttrs:
                    skillID = int(skillAttrs[srqIDAtrr])
                    skillLvl = skillAttrs[srqLvlAttr]
                    # Fetch item from database and fill map
                    item = edg_queries.getItem(skillID)
                    requiredSkills[item] = skillLvl
        return self.__requiredSkills

    factionMap = {
        500001: "caldari",
        500002: "minmatar",
        500003: "amarr",
        500004: "gallente",
        500005: "jove",
        500010: "guristas",
        500011: "angel",
        500012: "blood",
        500014: "ore",
        500016: "sisters",
        500018: "mordu",
        500019: "sansha",
        500020: "serpentis"
    }

    @property
    def race(self):
        if self.__race is None:

            try:
                if self.category.categoryName == 'Structure':
                    self.__race = "upwell"
                else:
                    self.__race = self.factionMap[self.factionID]
            # Some ships (like few limited issue ships) do not have factionID set,
            # thus keep old mechanism for now
            except KeyError:
                # Define race map
                map = {1: "caldari",
                       2: "minmatar",
                       4: "amarr",
                       5: "sansha",  # Caldari + Amarr
                       6: "blood",  # Minmatar + Amarr
                       8: "gallente",
                       9: "guristas",  # Caldari + Gallente
                       10: "angelserp",  # Minmatar + Gallente, final race depends on the order of skills
                       12: "sisters",  # Amarr + Gallente
                       16: "jove",
                       32: "sansha",  # Incrusion Sansha
                       128: "ore"}
                # Race is None by default
                race = None
                # Check primary and secondary required skills' races
                if race is None:
                    skillRaces = tuple(filter(lambda rid: rid, (s.raceID for s in tuple(self.requiredSkills.keys()))))
                    if sum(skillRaces) in map:
                        race = map[sum(skillRaces)]
                        if race == "angelserp":
                            if skillRaces == (2, 8):
                                race = "angel"
                            else:
                                race = "serpentis"
                # Rely on item's own raceID as last resort
                if race is None:
                    race = map.get(self.raceID, None)
                # Store our final value
                self.__race = race
        return self.__race

    @property
    def assistive(self):
        """Detects if item can be used as assistance"""
        # Make sure we cache results
        if self.__assistive is None:
            assistive = False
            # Go through all effects and find first assistive
            for effect in self.effects.itervalues():
                if effect.info.isAssistance is True:
                    # If we find one, stop and mark item as assistive
                    assistive = True
                    break
            self.__assistive = assistive
        return self.__assistive

    @property
    def offensive(self):
        """Detects if item can be used as something offensive"""
        # Make sure we cache results
        if self.__offensive is None:
            offensive = False
            # Go through all effects and find first offensive
            for effect in self.effects.itervalues():
                if effect.info.isOffensive is True:
                    # If we find one, stop and mark item as offensive
                    offensive = True
                    break
            self.__offensive = offensive
        return self.__offensive

    def requiresSkill(self, skill, level=None):
        for s, l in self.requiredSkills.iteritems():
            if isinstance(skill, basestring):
                if s.name == skill and (level is None or l == level):
                    return True

            elif isinstance(skill, int) and (level is None or l == level):
                if s.ID == skill:
                    return True

            elif skill == s and (level is None or l == level):
                return True

            elif hasattr(skill, "item") and skill.item == s and (level is None or l == level):
                return True

        return False

    def __repr__(self):
        return "Item(ID={}, name={}) at {}".format(
            self.ID, self.name, hex(id(self))
        )


class MetaData(EqBase):
    pass


class EffectInfo(EqBase):
    pass


class AttributeInfo(EqBase):
    pass


class Attribute(EqBase):
    pass


class Category(EqBase):
    pass


class Group(EqBase):
    pass


class Icon(EqBase):
    pass


class MarketGroup(EqBase):
    def __repr__(self):
        return u"MarketGroup(ID={}, name={}, parent={}) at {}".format(
            self.ID, self.name, getattr(self.parent, "name", None), self.name, hex(id(self))
        ).encode('utf8')


class MetaGroup(EqBase):
    pass


class MetaType(EqBase):
    pass


class Unit(EqBase):
    pass


class Traits(EqBase):
    pass


itemNameMap = {}


@cachedQuery(1, "lookfor")
def getItem(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            item = gamedata_session.query(Item).get(lookfor)
        else:
            item = gamedata_session.query(Item).options(*processEager(eager)).filter(Item.ID == lookfor).first()
    elif isinstance(lookfor, basestring):
        if lookfor in itemNameMap:
            id = itemNameMap[lookfor]
            if eager is None:
                item = gamedata_session.query(Item).get(id)
            else:
                item = gamedata_session.query(Item).options(*processEager(eager)).filter(Item.ID == id).first()
        else:
            # Item names are unique, so we can use first() instead of one()
            item = gamedata_session.query(Item).options(*processEager(eager)).filter(Item.name == lookfor).first()
            itemNameMap[lookfor] = item.ID
    else:
        raise TypeError("Need integer or string as argument")
    return item


groupNameMap = {}


@cachedQuery(1, "lookfor")
def getGroup(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            group = gamedata_session.query(Group).get(lookfor)
        else:
            group = gamedata_session.query(Group).options(*processEager(eager)).filter(Group.ID == lookfor).first()
    elif isinstance(lookfor, basestring):
        if lookfor in groupNameMap:
            id = groupNameMap[lookfor]
            if eager is None:
                group = gamedata_session.query(Group).get(id)
            else:
                group = gamedata_session.query(Group).options(*processEager(eager)).filter(Group.ID == id).first()
        else:
            # Group names are unique, so we can use first() instead of one()
            group = gamedata_session.query(Group).options(*processEager(eager)).filter(Group.name == lookfor).first()
            groupNameMap[lookfor] = group.ID
    else:
        raise TypeError("Need integer or string as argument")
    return group


categoryNameMap = {}


@cachedQuery(1, "lookfor")
def getCategory(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            category = gamedata_session.query(Category).get(lookfor)
        else:
            category = gamedata_session.query(Category).options(*processEager(eager)).filter(
                Category.ID == lookfor).first()
    elif isinstance(lookfor, basestring):
        if lookfor in categoryNameMap:
            id = categoryNameMap[lookfor]
            if eager is None:
                category = gamedata_session.query(Category).get(id)
            else:
                category = gamedata_session.query(Category).options(*processEager(eager)).filter(
                    Category.ID == id).first()
        else:
            # Category names are unique, so we can use first() instead of one()
            category = gamedata_session.query(Category).options(*processEager(eager)).filter(
                Category.name == lookfor).first()
            categoryNameMap[lookfor] = category.ID
    else:
        raise TypeError("Need integer or string as argument")
    return category


metaGroupNameMap = {}


@cachedQuery(1, "lookfor")
def getMetaGroup(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            metaGroup = gamedata_session.query(MetaGroup).get(lookfor)
        else:
            metaGroup = gamedata_session.query(MetaGroup).options(*processEager(eager)).filter(
                MetaGroup.ID == lookfor).first()
    elif isinstance(lookfor, basestring):
        if lookfor in metaGroupNameMap:
            id = metaGroupNameMap[lookfor]
            if eager is None:
                metaGroup = gamedata_session.query(MetaGroup).get(id)
            else:
                metaGroup = gamedata_session.query(MetaGroup).options(*processEager(eager)).filter(
                    MetaGroup.ID == id).first()
        else:
            # MetaGroup names are unique, so we can use first() instead of one()
            metaGroup = gamedata_session.query(MetaGroup).options(*processEager(eager)).filter(
                MetaGroup.name == lookfor).first()
            metaGroupNameMap[lookfor] = metaGroup.ID
    else:
        raise TypeError("Need integer or string as argument")
    return metaGroup


@cachedQuery(1, "lookfor")
def getMarketGroup(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            marketGroup = gamedata_session.query(MarketGroup).get(lookfor)
        else:
            marketGroup = gamedata_session.query(MarketGroup).options(*processEager(eager)).filter(
                MarketGroup.ID == lookfor).first()
    else:
        raise TypeError("Need integer as argument")
    return marketGroup


@cachedQuery(2, "where", "filter")
def getItemsByCategory(filter, where=None, eager=None):
    if isinstance(filter, int):
        filter = Category.ID == filter
    elif isinstance(filter, basestring):
        filter = Category.name == filter
    else:
        raise TypeError("Need integer or string as argument")

    filter = processWhere(filter, where)
    return gamedata_session.query(Item).options(*processEager(eager)).join(Item.group, Group.category).filter(
        filter).all()


@cachedQuery(3, "where", "nameLike", "join")
def searchItems(nameLike, where=None, join=None, eager=None):
    if not isinstance(nameLike, basestring):
        raise TypeError("Need string as argument")

    if join is None:
        join = tuple()

    if not hasattr(join, "__iter__"):
        join = (join,)

    items = gamedata_session.query(Item).options(*processEager(eager)).join(*join)
    for token in nameLike.split(' '):
        token_safe = u"%{0}%".format(sqlizeString(token))
        if where is not None:
            items = items.filter(and_(Item.name.like(token_safe, escape="\\"), where))
        else:
            items = items.filter(Item.name.like(token_safe, escape="\\"))
    items = items.limit(100).all()
    return items


@cachedQuery(2, "where", "itemids")
def getVariations(itemids, where=None, eager=None):
    for itemid in itemids:
        if not isinstance(itemid, int):
            raise TypeError("All passed item IDs must be integers")
    # Get out if list of provided IDs is empty
    if len(itemids) == 0:
        return []

    itemfilter = or_(*(Mapper.metatypes_table.c.parentTypeID == itemid for itemid in itemids))
    filter = processWhere(itemfilter, where)
    joinon = Mapper.items_table.c.typeID == Mapper.metatypes_table.c.typeID
    vars = gamedata_session.query(Item).options(*processEager(eager)).join((Mapper.metatypes_table, joinon)).filter(
        filter).all()
    return vars


@cachedQuery(1, "attr")
def getAttributeInfo(attr, eager=None):
    if isinstance(attr, basestring):
        filter_ = AttributeInfo.name == attr
    elif isinstance(attr, int):
        filter_ = AttributeInfo.ID == attr
    else:
        raise TypeError("Need integer or string as argument")
    try:
        result = gamedata_session.query(AttributeInfo).options(*processEager(eager)).filter(filter_).one()
    except exc.NoResultFound:
        result = None
    return result


@cachedQuery(1, "field")
def getMetaData(field):
    if isinstance(field, basestring):
        data = gamedata_session.query(MetaData).get(field)
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

    result = gamedata_session.execute(q).fetchall()
    return result


class Mapper:
    Effect.name = association_proxy("info", "name")
    Effect.description = association_proxy("info", "description")
    Effect.published = association_proxy("info", "published")

    class Attributes:
        typeattributes_table = Table("dgmtypeattribs", gamedata_meta,
                                     Column("value", Float),
                                     Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True, index=True),
                                     Column("attributeID", ForeignKey("dgmattribs.attributeID"), primary_key=True))

        attributes_table = Table("dgmattribs", gamedata_meta,
                                 Column("attributeID", Integer, primary_key=True),
                                 Column("attributeName", String),
                                 Column("defaultValue", Float),
                                 Column("maxAttributeID", Integer, ForeignKey("dgmattribs.attributeID")),
                                 Column("description", Unicode),
                                 Column("published", Boolean),
                                 Column("displayName", String),
                                 Column("highIsGood", Boolean),
                                 Column("iconID", Integer, ForeignKey("icons.iconID")),
                                 Column("unitID", Integer, ForeignKey("dgmunits.unitID")))

        mapper(Attribute, typeattributes_table,
               properties={"info": relation(AttributeInfo, lazy=False)})

        mapper(AttributeInfo, attributes_table,
               properties={"icon": relation(Icon),
                           "unit": relation(Unit),
                           "ID": synonym("attributeID"),
                           "name": synonym("attributeName"),
                           "description": deferred(attributes_table.c.description)})

        Attribute.ID = association_proxy("info", "attributeID")
        Attribute.name = association_proxy("info", "attributeName")
        Attribute.description = association_proxy("info", "description")
        Attribute.published = association_proxy("info", "published")
        Attribute.displayName = association_proxy("info", "displayName")
        Attribute.highIsGood = association_proxy("info", "highIsGood")
        Attribute.iconID = association_proxy("info", "iconID")
        Attribute.icon = association_proxy("info", "icon")
        Attribute.unit = association_proxy("info", "unit")

    class Categories:
        categories_table = Table("invcategories", gamedata_meta,
                                 Column("categoryID", Integer, primary_key=True),
                                 Column("categoryName", String),
                                 Column("description", String),
                                 Column("published", Boolean),
                                 Column("iconID", Integer, ForeignKey("icons.iconID")))

        mapper(Category, categories_table,
               properties={"icon": relation(Icon),
                           "ID": synonym("categoryID"),
                           "name": synonym("categoryName"),
                           "description": deferred(categories_table.c.description)})

    class Effects:
        typeeffects_table = Table("dgmtypeeffects", gamedata_meta,
                                  Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True, index=True),
                                  Column("effectID", Integer, ForeignKey("dgmeffects.effectID"), primary_key=True))

        effects_table = Table("dgmeffects", gamedata_meta,
                              Column("effectID", Integer, primary_key=True),
                              Column("effectName", String),
                              Column("description", String),
                              Column("published", Boolean),
                              Column("isAssistance", Boolean),
                              Column("isOffensive", Boolean))

        mapper(EffectInfo, effects_table,
               properties={"ID": synonym("effectID"),
                           "name": synonym("effectName"),
                           "description": deferred(effects_table.c.description)})

        mapper(Effect, typeeffects_table,
               properties={"ID": synonym("effectID"),
                           "info": relation(EffectInfo, lazy=False)})

    class Groups:
        groups_table = Table("invgroups", gamedata_meta,
                             Column("groupID", Integer, primary_key=True),
                             Column("groupName", String),
                             Column("description", String),
                             Column("published", Boolean),
                             Column("categoryID", Integer, ForeignKey("invcategories.categoryID")),
                             Column("iconID", Integer, ForeignKey("icons.iconID")))

        mapper(Group, groups_table,
               properties={"category": relation(Category, backref="groups"),
                           "icon": relation(Icon),
                           "ID": synonym("groupID"),
                           "name": synonym("groupName"),
                           "description": deferred(groups_table.c.description)})

    class Units:
        units_table = Table("dgmunits", gamedata_meta,
                            Column("unitID", Integer, primary_key=True),
                            Column("unitName", String),
                            Column("displayName", String))

        mapper(Unit, units_table,
               properties={"ID": synonym("unitID"),
                           "name": synonym("unitName")})

    class Icons:
        icons_table = Table("icons", gamedata_meta,
                            Column("iconID", Integer, primary_key=True),
                            Column("description", String),
                            Column("iconFile", String))

        mapper(Icon, icons_table,
               properties={"ID": synonym("iconID"),
                           "description": deferred(icons_table.c.description)})

    class Items:
        metagroups_table = Table("invmetagroups", gamedata_meta,
                                 Column("metaGroupID", Integer, primary_key=True),
                                 Column("metaGroupName", String))

        metatypes_table = Table("invmetatypes", gamedata_meta,
                                Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True),
                                Column("parentTypeID", Integer, ForeignKey("invtypes.typeID")),
                                Column("metaGroupID", Integer, ForeignKey("invmetagroups.metaGroupID")))

        traits_table = Table("invtraits", gamedata_meta,
                             Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True),
                             Column("traitText", String))

        mapper(Traits, traits_table)

        items_table = Table("invtypes", gamedata_meta,
                            Column("typeID", Integer, primary_key=True),
                            Column("typeName", String, index=True),
                            Column("description", String),
                            Column("raceID", Integer),
                            Column("factionID", Integer),
                            Column("volume", Float),
                            Column("mass", Float),
                            Column("capacity", Float),
                            Column("published", Boolean),
                            Column("marketGroupID", Integer, ForeignKey("invmarketgroups.marketGroupID")),
                            Column("iconID", Integer, ForeignKey("icons.iconID")),
                            Column("groupID", Integer, ForeignKey("invgroups.groupID"), index=True))

        mapper(Item, items_table,
               properties={"group": relation(Group, backref="items"),
                           "icon": relation(Icon),
                           "_Item__attributes": relation(Attribute, collection_class=attribute_mapped_collection('name')),
                           "effects": relation(Effect, collection_class=attribute_mapped_collection('name')),
                           "metaGroup": relation(MetaType,
                                                 primaryjoin=metatypes_table.c.typeID == items_table.c.typeID,
                                                 uselist=False),
                           "ID": synonym("typeID"),
                           "name": synonym("typeName"),
                           "description": deferred(items_table.c.description),
                           "traits": relation(Traits,
                                              primaryjoin=traits_table.c.typeID == items_table.c.typeID,
                                              uselist=False)
                           })

        Item.category = association_proxy("group", "category")

        mapper(MetaGroup, metagroups_table,
               properties={"ID": synonym("metaGroupID"),
                           "name": synonym("metaGroupName")})

        mapper(MetaType, metatypes_table,
               properties={"ID": synonym("metaGroupID"),
                           "parent": relation(Item, primaryjoin=metatypes_table.c.parentTypeID == items_table.c.typeID),
                           "items": relation(Item, primaryjoin=metatypes_table.c.typeID == items_table.c.typeID),
                           "info": relation(MetaGroup, lazy=False)})

        MetaType.name = association_proxy("info", "name")

    class MarketGroups:
        marketgroups_table = Table("invmarketgroups", gamedata_meta,
                                   Column("marketGroupID", Integer, primary_key=True),
                                   Column("marketGroupName", String),
                                   Column("description", String),
                                   Column("hasTypes", Boolean),
                                   Column("parentGroupID", Integer,
                                          ForeignKey("invmarketgroups.marketGroupID", initially="DEFERRED",
                                                     deferrable=True)),
                                   Column("iconID", Integer, ForeignKey("icons.iconID")))

        mapper(MarketGroup, marketgroups_table,
               properties={"items": relation(Item, backref="marketGroup"),
                           "parent": relation(MarketGroup, backref="children",
                                              remote_side=[marketgroups_table.c.marketGroupID]),
                           "icon": relation(Icon),
                           "ID": synonym("marketGroupID"),
                           "name": synonym("marketGroupName"),
                           "description": deferred(marketgroups_table.c.description)})

    class Metadata:
        metadata_table = Table("metadata", gamedata_meta,
                               Column("field_name", String, primary_key=True),
                               Column("field_value", String))

        mapper(MetaData, metadata_table)
