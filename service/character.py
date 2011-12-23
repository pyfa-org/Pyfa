#===============================================================================
# Copyright (C) 2010 Diego Duclos
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
#===============================================================================

import eos.db
import eos.types
import copy
import service
import itertools

class Character():
    instance = None
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Character()

        return cls.instance

    def all0(self):
        all0 = eos.types.Character.getAll0()
        eos.db.commit()
        return all0

    def all0ID(self):
        return self.all0().ID

    def all5(self):
        all5 = eos.types.Character.getAll5()
        eos.db.commit()
        return all5

    def all5ID(self):
        return self.all5().ID

    def getCharacterList(self):
        baseChars = [eos.types.Character.getAll0(), eos.types.Character.getAll5()]
        # Flush incase all0 & all5 weren't in the db yet
        eos.db.commit()
        sFit = service.Fit.getInstance()
        return map(lambda c: (c.ID, c.name, c == sFit.character), eos.db.getCharacterList())

    def getCharacter(self, charID):
        char = eos.db.getCharacter(charID)
        return char

    def getSkillGroups(self):
        cat = eos.db.getCategory(16)
        groups = []
        for grp in cat.groups:
            if grp.published:
                groups.append((grp.ID, grp.name))
        return groups

    def getSkills(self, groupID):
        group = eos.db.getGroup(groupID)
        skills = []
        for skill in group.items:
            if skill.published == True:
                skills.append((skill.ID, skill.name))
        return skills

    def getSkillDescription(self, itemID):
        return eos.db.getItem(itemID).description

    def getGroupDescription(self, groupID):
        return eos.db.getMarketGroup(groupID).description

    def getSkillLevel(self, charID, skillID):
        skill = eos.db.getCharacter(charID).getSkill(skillID)
        return skill.level if skill.learned else "Not learned"

    def rename(self, charID, newName):
        char = eos.db.getCharacter(charID)
        char.name = newName
        eos.db.commit()

    def new(self):
        char = eos.types.Character("New Character")
        eos.db.save(char)
        return char.ID

    def getCharName(self, charID):
        return eos.db.getCharacter(charID).name

    def copy(self, charID):
        char = eos.db.getCharacter(charID)
        newChar = copy.deepcopy(char)
        eos.db.save(newChar)
        return newChar.ID

    def delete(self, charID):
        char = eos.db.getCharacter(charID)
        eos.db.commit()
        eos.db.remove(char)

    def getApiDetails(self, charID):
        char = eos.db.getCharacter(charID)
        return (char.apiID or "", char.apiKey or "")

    def getProxySettings(self):
        ps = service.settings.ProxySettings.getInstance()
        if ps.getMode() == 0:
            return None
        elif ps.getMode() == 1:
            return ps.autodetect()
        elif ps.getMode == 2:
            return ps.getAddress() + ps.getPort()


    def charList(self, charID, userID, apiKey):
        char = eos.db.getCharacter(charID)
        try:
            char.apiID = userID
            char.apiKey = apiKey
            return char.apiCharList(proxy = self.getProxySettings())
        except:
            return None

    def apiFetch(self, charID, charName):

        char = eos.db.getCharacter(charID, proxy = self.getProxySettings())
        char.apiFetch(charName)
        eos.db.commit()

    def changeLevel(self, charID, skillID, level):
        char = eos.db.getCharacter(charID)
        skill = char.getSkill(skillID)
        if isinstance(level, basestring):
            skill.learned = False
            skill.level = None
        else:
            skill.level = level

        eos.db.commit()

    def addImplant(self, charID, itemID):
        char = eos.db.getCharacter(charID)
        implant = eos.types.Implant(eos.db.getItem(itemID))
        char.implants.freeSlot(implant.slot)
        char.implants.append(implant)

    def removeImplant(self, charID, slot):
        char = eos.db.getCharacter(charID)
        char.implants.freeSlot(slot)

    def getImplants(self, charID):
        char = eos.db.getCharacter(charID)
        return char.implants

    def checkRequirements(self, fit):
        toCheck = []
        reqs = {}
        for thing in itertools.chain(fit.modules, fit.drones, (fit.ship,)):
            for attr in ("item", "charge"):
                subThing = getattr(thing, attr, None)
                subReqs = {}
                if subThing is not None:
                    self._checkRequirements(fit, fit.character, subThing, subReqs)
                    if subReqs:
                        reqs[subThing] = subReqs

        return reqs

    def _checkRequirements(self, fit, char, subThing, reqs):
        for req, level in subThing.requiredSkills.iteritems():
            name = req.name
            info = reqs.get(name)
            currLevel, subs = info if info is not None else 0, {}
            if level > currLevel and (char is None or char.getSkill(req).level < level):
                reqs[name] = (level, subs)
                self._checkRequirements(fit, char, req, subs)

        return reqs
