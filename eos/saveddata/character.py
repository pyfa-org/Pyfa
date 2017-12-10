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

import time

from logbook import Logger
from itertools import chain

from sqlalchemy.orm import validates, reconstructor

import eos
import eos.db
import eos.config
from eos.effectHandlerHelpers import HandledItem, HandledImplantBoosterList

pyfalog = Logger(__name__)


class Character(object):
    __itemList = None
    __itemIDMap = None
    __itemNameMap = None

    def __init__(self, name, defaultLevel=None, initSkills=True):
        self.savedName = name
        self.__owner = None
        self.defaultLevel = defaultLevel
        self.__skills = []
        self.__skillIdMap = {}
        self.dirtySkills = set()
        self.alphaClone = None
        self.__secStatus = 0.0

        if initSkills:
            for item in self.getSkillList():
                self.addSkill(Skill(self, item.ID, self.defaultLevel))

        self.__implants = HandledImplantBoosterList()
        self.apiKey = None

    @reconstructor
    def init(self):

        self.__skillIdMap = {}
        for skill in self.__skills:
            self.__skillIdMap[skill.itemID] = skill
        self.dirtySkills = set()

        self.alphaClone = None

        if self.alphaCloneID:
            self.alphaClone = eos.db.getAlphaClone(self.alphaCloneID)

    @classmethod
    def getSkillList(cls):
        if cls.__itemList is None:
            cls.__itemList = eos.db.getItemsByCategory("Skill")

        return cls.__itemList

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

    def apiUpdateCharSheet(self, skills, secStatus=0):
        del self.__skills[:]
        self.__skillIdMap.clear()
        for skillRow in skills:
            self.addSkill(Skill(self, skillRow["typeID"], skillRow["level"]))
        self.secStatus = secStatus

    @property
    def ro(self):
        return self == self.getAll0() or self == self.getAll5()

    @property
    def secStatus(self):
        if self.name == "All 5":
            self.__secStatus = 5.00
        elif self.name == "All 0":
            self.__secStatus = 0.00
        return self.__secStatus

    @secStatus.setter
    def secStatus(self, sec):
        self.__secStatus = sec

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, owner):
        self.__owner = owner

    @property
    def name(self):
        name = self.savedName

        if self.isDirty:
            name += " *"

        if self.alphaCloneID:
            name += u' (\u03B1)'

        return name

    @name.setter
    def name(self, name):
        self.savedName = name

    @property
    def alphaCloneID(self):
        return self.__alphaCloneID

    @alphaCloneID.setter
    def alphaCloneID(self, cloneID):
        self.__alphaCloneID = cloneID
        self.alphaClone = eos.db.getAlphaClone(cloneID) if cloneID is not None else None

    @property
    def skills(self):
        return self.__skills

    def addSkill(self, skill):
        if skill.itemID in self.__skillIdMap:
            oldSkill = self.__skillIdMap[skill.itemID]
            if skill.level > oldSkill.level:
                # if new skill is higher, remove old skill (new skill will still append)
                self.__skills.remove(oldSkill)
            else:
                return

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
            skill = Skill(self, item, self.defaultLevel, False, True)
            self.addSkill(skill)

        return skill

    @property
    def implants(self):
        return self.__implants

    @property
    def isDirty(self):
        return len(self.dirtySkills) > 0

    def saveLevels(self):
        if self.ro:
            raise ReadOnlyException("This character is read-only")

        for skill in self.dirtySkills.copy():
            skill.saveLevel()

        self.dirtySkills = set()
        eos.db.commit()

    def revertLevels(self):
        for skill in self.dirtySkills.copy():
            skill.revert()

        self.dirtySkills = set()

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

    def calculateModifiedAttributes(self, fit, runTime, forceProjected=False):
        if forceProjected:
            return
        for skill in self.skills:
            fit.register(skill)
            skill.calculateModifiedAttributes(fit, runTime)

    def clear(self):
        c = chain(
                self.skills,
                self.implants
        )
        for stuff in c:
            if stuff is not None and stuff != self:
                stuff.clear()

    def __deepcopy__(self, memo):
        copy = Character("%s copy" % self.name, initSkills=False)
        copy.apiKey = self.apiKey
        copy.apiID = self.apiID

        for skill in self.skills:
            copy.addSkill(Skill(copy, skill.itemID, skill.level, False, skill.learned))

        return copy

    @validates("ID", "name", "apiKey", "ownerID")
    def validator(self, key, val):
        map = {
            "ID"     : lambda _val: isinstance(_val, int),
            "name"   : lambda _val: True,
            "apiKey" : lambda _val: _val is None or (isinstance(_val, basestring) and len(_val) > 0),
            "ownerID": lambda _val: isinstance(_val, int) or _val is None
        }

        if not map[key](val):
            raise ValueError(str(val) + " is not a valid value for " + key)
        else:
            return val

    def __repr__(self):
        return "Character(ID={}, name={}) at {}".format(
                self.ID, self.name, hex(id(self))
        )


class Skill(HandledItem):
    def __init__(self, character, item, level=0, ro=False, learned=True):
        self.character = character
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

    def saveLevel(self):
        self.__level = self.activeLevel

        if self in self.character.dirtySkills:
            self.character.dirtySkills.remove(self)

    def revert(self):
        self.activeLevel = self.__level

    @property
    def isDirty(self):
        return self.__level != self.activeLevel

    @property
    def learned(self):
        return self.activeLevel is not None

    @property
    def level(self):
        # @todo: there is a phantom bug that keep popping up about skills not having a character... See #1234
        # Remove this at some point when the cause can be determined.
        if self.character:
            # Ensure that All 5/0 character have proper skill levels (in case database gets corrupted)
            if self.character.name == "All 5":
                self.activeLevel = self.__level = 5
            elif self.character.name == "All 0":
                self.activeLevel = self.__level = 0
            elif self.character.alphaClone:
                return min(self.activeLevel, self.character.alphaClone.getSkillLevel(self)) or 0

        return self.activeLevel or 0

    def setLevel(self, level, persist=False, ignoreRestrict=False):

        if (level < 0 or level > 5) and level is not None:
            raise ValueError(str(level) + " is not a valid value for level")

        if hasattr(self, "_Skill__ro") and self.__ro is True:
            raise ReadOnlyException()

        self.activeLevel = level

        # todo: have a way to do bulk skill level editing. Currently, everytime a single skill is changed, this runs,
        # which affects performance. Should have a checkSkillLevels() or something that is more efficient for bulk.
        if not ignoreRestrict and eos.config.settings['strictSkillLevels']:
            start = time.time()
            for item, rlevel in self.item.requiredFor.iteritems():
                if item.group.category.ID == 16:  # Skill category
                    if level < rlevel:
                        skill = self.character.getSkill(item.ID)
                        # print "Removing skill: {}, Dependant level: {}, Required level: {}".format(skill, level, rlevel)
                        skill.setLevel(None, persist)
            pyfalog.debug("Strict Skill levels enabled, time to process {}: {}".format(self.item.ID, time.time() - start))

        if persist:
            self.saveLevel()
        else:
            self.character.dirtySkills.add(self)

            if self.activeLevel == self.__level and self in self.character.dirtySkills:
                self.character.dirtySkills.remove(self)

    @property
    def item(self):
        if self.__item is None:
            self.__item = item = Character.getSkillIDMap().get(self.itemID)
            if item is None:
                # This skill is no longer in the database and thus invalid it, get rid of it.
                self.character.removeSkill(self)

        return self.__item

    def getModifiedItemAttr(self, key):
        if key in self.item.attributes:
            return self.item.attributes[key].value
        else:
            return None

    def calculateModifiedAttributes(self, fit, runTime):
        if self.__suppressed:  # or not self.learned - removed for GH issue 101
            return

        item = self.item
        if item is None:
            return

        for effect in item.effects.itervalues():
            if effect.runTime == runTime and \
                    effect.isType("passive") and \
                    (not fit.isStructure or effect.isType("structure")) and \
                    effect.activeByDefault:
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
        if hasattr(self, "_Skill__ro") and self.__ro is True and key != "characterID":
            raise ReadOnlyException()

        map = {
            "characterID": lambda _val: isinstance(_val, int),
            "skillID"    : lambda _val: isinstance(_val, int)
        }

        if not map[key](val):
            raise ValueError(str(val) + " is not a valid value for " + key)
        else:
            return val

    def __deepcopy__(self, memo):
        copy = Skill(self.character, self.item, self.level, self.__ro)
        return copy

    def __repr__(self):
        return "Skill(ID={}, name={}) at {}".format(
                self.item.ID, self.item.name, hex(id(self))
        )


class ReadOnlyException(Exception):
    pass
