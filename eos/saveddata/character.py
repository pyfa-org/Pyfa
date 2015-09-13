#===============================================================================
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
#===============================================================================


from sqlalchemy.orm import validates, reconstructor

from eos.effectHandlerHelpers import HandledItem
import eos.db
import eos

class Character(object):
    __itemList = None
    __itemIDMap = None
    __itemNameMap = None

    @classmethod
    def getSkillList(cls):
        if cls.__itemList is None:
            cls.__itemList = eos.db.getItemsByCategory("Skill")

        return cls.__itemList

    @classmethod
    def setSkillList(cls, list):
        cls.__itemList = list

    @classmethod
    def getSkillIDMap(cls):
        if cls.__itemIDMap is None:
            map = {}
            for skill in cls.getSkillList():
                map[skill.ID] = skill

            cls.__itemIDMap = map

        return cls.__itemIDMap

    @classmethod
    def getSkillNameMap(cls):
        if cls.__itemNameMap is None:
            map = {}
            for skill in cls.getSkillList():
                map[skill.name] = skill

            cls.__itemNameMap = map

        return cls.__itemNameMap

    @classmethod
    def getAll5(cls):
        all5 = eos.db.getCharacter("All 5")

        if all5 is None:
            # We do not have to be afraid of committing here and saving
            # edited character data. If this ever runs, it will be during the
            # get character list phase when pyfa first starts
            all5 = Character("All 5", 5)
            eos.db.save(all5)

        return all5

    @classmethod
    def getAll0(cls):
        all0 = eos.db.getCharacter("All 0")

        if all0 is None:
            all0 = Character("All 0")
            eos.db.save(all0)

        return all0

    def __init__(self, name, defaultLevel=None):
        self.name = name
        self.__owner = None
        self.defaultLevel = defaultLevel
        self.__skills = []
        self.__skillIdMap = {}

        for item in self.getSkillList():
            self.addSkill(Skill(item.ID, self.defaultLevel))

        self.__implants = eos.saveddata.fit.HandledImplantBoosterList()
        self.apiKey = None

    @reconstructor
    def init(self):
        self.__skillIdMap = {}
        for skill in self.__skills:
            self.__skillIdMap[skill.itemID] = skill

    def apiUpdateCharSheet(self, skills):
        del self.__skills[:]
        self.__skillIdMap.clear()
        for skillRow in skills:
            self.addSkill(Skill(skillRow["typeID"], skillRow["level"]))

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, owner):
        self.__owner = owner

    @property
    def skills(self):
        return self.__skills

    def addSkill(self, skill):
        self.__skills.append(skill)
        self.__skillIdMap[skill.itemID] = skill

    def removeSkill(self, skill):
        self.__skills.remove(skill)
        del self.__skillIdMap[skill.itemID]

    def getSkill(self, item):
        if isinstance(item, basestring):
            item = self.getSkillNameMap()[item]
        elif isinstance(item, int):
            item = self.getSkillIDMap()[item]

        skill = self.__skillIdMap.get(item.ID)

        if skill is None:
            skill = Skill(item, self.defaultLevel, False, True)
            self.addSkill(skill)

        return skill

    @property
    def implants(self):
        return self.__implants

    @property
    def isDirty(self):
        return getattr(self, "dirty", False)

    def saveLevels(self):
        for skill in self.skills:
            skill.__level = skill.level
        self.dirty = False
        eos.db.commit()

    def filteredSkillIncrease(self, filter, *args, **kwargs):
        for element in self.skills:
            if filter(element):
                element.increaseItemAttr(*args, **kwargs)

    def filteredSkillMultiply(self, filter, *args, **kwargs):
        for element in self.skills:
            if filter(element):
                element.multiplyItemAttr(*args, **kwargs)

    def filteredSkillBoost(self, filter, *args, **kwargs):
        for element in self.skills:
            if filter(element):
                element.boostItemAttr(*args, **kwargs)

    def calculateModifiedAttributes(self, fit, runTime, forceProjected = False):
        if forceProjected: return
        for skill in self.skills:
            fit.register(skill)
            skill.calculateModifiedAttributes(fit, runTime)

    def clear(self):
        for skill in self.skills:
            skill.clear()

    def __deepcopy__(self, memo):
        copy = Character("%s copy" % self.name)
        copy.apiKey = self.apiKey
        copy.apiID = self.apiID

        for skill in self.skills:
            copy.addSkill(Skill(skill.itemID, skill.level, False, skill.learned))

        return copy

    @validates("ID", "name", "apiKey", "ownerID")
    def validator(self, key, val):
        map = {"ID": lambda val: isinstance(val, int),
               "name" : lambda val: True,
               "apiKey" : lambda val: val is None or (isinstance(val, basestring) and len(val) > 0),
               "ownerID" : lambda val: isinstance(val, int) or val is None}

        if map[key](val) == False: raise ValueError(str(val) + " is not a valid value for " + key)
        else: return val

class Skill(HandledItem):
    def __init__(self, item, level=0, ro=False, learned=True):
        self.__item = item if not isinstance(item, int) else None
        self.itemID = item.ID if not isinstance(item, int) else item
        self.__level = level if learned else None
        self.commandBonus = 0
        self.build(ro)

    @reconstructor
    def init(self):
        self.build(False)
        self.__item = None

    def build(self, ro):
        self.__ro = ro
        self.__suppressed = False
        self.activeLevel = self.__level

    @property
    def learned(self):
        return self.__level is not None

    @property
    def level(self):
        return self.activeLevel or 0

    @level.setter
    def level(self, level):
        if (level < 0 or level > 5) and level is not None:
            raise ValueError(str(level) + " is not a valid value for level")

        if hasattr(self, "_Skill__ro") and self.__ro == True:
            raise ReadOnlyException()

        self.activeLevel = level
        self.character.dirty = True

    @property
    def item(self):
        if self.__item is None:
            self.__item = item = Character.getSkillIDMap().get(self.itemID)
            if item is None:
                #This skill is no longer in the database and thus invalid it, get rid of it.
                self.character.removeSkill(self)

        return self.__item

    def getModifiedItemAttr(self, key):
        return self.item.attributes[key].value

    def calculateModifiedAttributes(self, fit, runTime):
        if self.__suppressed: # or not self.learned - removed for GH issue 101
            return

        item = self.item
        if item is None:
            return

        for effect in item.effects.itervalues():
            if effect.runTime == runTime and effect.isType("passive"):
                try:
                    effect.handler(fit, self, ("skill",))
                except AttributeError:
                    continue

    def clear(self):
        self.__suppressed = False
        self.commandBonus = 0

    def suppress(self):
        self.__suppressed = True

    def isSuppressed(self):
        return self.__suppressed

    @validates("characterID", "skillID", "level")
    def validator(self, key, val):
        if hasattr(self, "_Skill__ro") and self.__ro == True and key != "characterID":
            raise ReadOnlyException()

        map = {"characterID": lambda val: isinstance(val, int),
               "skillID" : lambda val: isinstance(val, int)}

        if map[key](val) == False: raise ValueError(str(val) + " is not a valid value for " + key)
        else: return val

    def __deepcopy__(self, memo):
        copy = Skill(self.item, self.level, self.__ro)
        return copy

    def __repr__(self):
        return "Skill(ID={}, name={}) at {}".format(
            self.item.ID, self.item.name, hex(id(self))
        )

class ReadOnlyException(Exception):
    pass
