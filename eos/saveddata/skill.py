from sqlalchemy.orm import validates, reconstructor, mapper

from eos.effectHandlerHelpers import HandledItem
from eos.gamedata import getItemsByCategory
from eos.db.saveddata.mapper import CharacterSkills as skills_table


class ReadOnlyException(Exception):
    pass


class Skill(HandledItem):
    __itemList = None
    __itemIDMap = None

    @classmethod
    def getSkillList(cls):
        if cls.__itemList is None:
            cls.__itemList = getItemsByCategory("Skill")

        return cls.__itemList

    @classmethod
    def getSkillIDMap(cls):
        if cls.__itemIDMap is None:
            map = {}
            for skill in cls.getSkillList():
                map[skill.ID] = skill

            cls.__itemIDMap = map

        return cls.__itemIDMap

    def __init__(self, item, level=0, ro=False, learned=True):
        self.__item = item if not isinstance(item, int) else None
        self.itemID = item.ID if not isinstance(item, int) else item
        self.__level = level if learned else None
        self.commandBonus = 0
        self.build(ro)

        mapper(Skill, skills_table)

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
        self.level = self.__level

    @property
    def isDirty(self):
        return self.__level != self.activeLevel

    @property
    def learned(self):
        return self.activeLevel is not None

    @property
    def level(self):
        return self.activeLevel or 0

    @level.setter
    def level(self, level):
        if (level < 0 or level > 5) and level is not None:
            raise ValueError(str(level) + " is not a valid value for level")

        if hasattr(self, "_Skill__ro") and self.__ro is True:
            raise ReadOnlyException()

        self.activeLevel = level
        self.character.dirtySkills.add(self)

        if self.activeLevel == self.__level and self in self.character.dirtySkills:
            self.character.dirtySkills.remove(self)

    @property
    def item(self):
        if self.__item is None:
            self.__item = item = Skill.getSkillIDMap().get(self.itemID)
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

        map = {"characterID": lambda val: isinstance(val, int),
               "skillID": lambda val: isinstance(val, int)}

        if not map[key](val):
            raise ValueError(str(val) + " is not a valid value for " + key)
        else:
            return val

    def __deepcopy__(self, memo):
        copy = Skill(self.item, self.level, self.__ro)
        return copy

    def __repr__(self):
        return "Skill(ID={}, name={}) at {}".format(
            self.item.ID, self.item.name, hex(id(self))
        )
