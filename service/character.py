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

import os.path
import locale
import threading
import wx
from codecs import open

from xml.etree import ElementTree
from xml.dom import minidom

EVEMON_COMPATIBLE_VERSION = "4081"

class SkillBackupThread(threading.Thread):
    def __init__(self, path, saveFmt, activeFit, callback):
        threading.Thread.__init__(self)
        self.path = path
        self.saveFmt = saveFmt
        self.activeFit = activeFit
        self.callback = callback

    def run(self):
        path = self.path
        sCharacter = Character.getInstance()
        sFit = service.Fit.getInstance()
        fit = sFit.getFit(self.activeFit)
        backupFile = open(path, "w", encoding="utf-8")
        backupData = "";
        if self.saveFmt == "xml":
            backupData = sCharacter.exportXml()
        elif self.saveFmt == "txt":
            backupData = sCharacter.exportText()
        else:
            backupData = sCharacter.exportText()
        backupFile.write(backupData)
        backupFile.close()
        wx.CallAfter(self.callback)

class Character():
    instance = None
    skillReqsDict = {}

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Character()

        return cls.instance

    def exportText(self):
        data = ""

        mySkills = repr(self.skillReqsDict)
        data += "-" * 79
        data += '\n'
        data += repr(self.skillReqsDict)
        data += '\n'
        data += "-" * 79
        data += '\n'

        return data

    def exportXml(self):
        root = ElementTree.Element("plan")
        root.attrib["name"] = "Pyfa exported plan for "+self.skillReqsDict['charname']
        root.attrib["revision"] = EVEMON_COMPATIBLE_VERSION
        
        sorts = ElementTree.SubElement(root, "sorting")
        sorts.attrib["criteria"] = "None"
        sorts.attrib["order"] = "None"
        sorts.attrib["groupByPriority"] = "false"
       
        for s in self.skillReqsDict['skills']:
            entry = ElementTree.SubElement(root, "entry")
            entry.attrib["skillID"] = str(s["skillID"])
            entry.attrib["skill"] = s["skill"]
            entry.attrib["level"] = str(s["level"])
            entry.attrib["priority"] = "3"
            entry.attrib["type"] = "Prerequisite"
            notes = ElementTree.SubElement(entry, "notes")
            notes.text = entry.attrib["skill"]
        
        tree = ElementTree.ElementTree(root)
        data = ElementTree.tostring(root, 'utf-8')
        prettydata = minidom.parseString(data).toprettyxml(indent="  ")

        return prettydata

    def backupSkills(self, path, saveFmt, activeFit, callback):
        thread = SkillBackupThread(path, saveFmt, activeFit, callback)
        thread.start()

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

    def charList(self, charID, userID, apiKey):
        char = eos.db.getCharacter(charID)
        try:
            char.apiID = userID
            char.apiKey = apiKey
            return char.apiCharList(proxy = service.settings.ProxySettings.getInstance().getProxySettings())
        except:
            return None

    def apiFetch(self, charID, charName):
        char = eos.db.getCharacter(charID)
        char.apiFetch(charName, proxy = service.settings.ProxySettings.getInstance().getProxySettings())
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
            ID = req.ID
            info = reqs.get(name)
            currLevel, subs = info if info is not None else 0, {}
            if level > currLevel and (char is None or char.getSkill(req).level < level):
                reqs[name] = (level, ID, subs)
                self._checkRequirements(fit, char, req, subs)

        return reqs
