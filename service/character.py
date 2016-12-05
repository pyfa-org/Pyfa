# =============================================================================
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
# =============================================================================

import copy
import gzip
import itertools
import json
import logging
import threading
from codecs import open
from xml.dom import minidom
from xml.etree import ElementTree

import wx

import config
import eos.db
from eos.db.saveddata import queries as eds_queries
from eos.saveddata.character import Character as es_Character, getCharacter
from eos.saveddata.fighter import Fighter as es_Fighter
from eos.saveddata.implant import Implant as es_Implant
from eos.saveddata.module import Slot as es_Slot, Module as es_Module
from service.eveapi import EVEAPIConnection, ParseXML

logger = logging.getLogger(__name__)


class CharacterImportThread(threading.Thread):
    def __init__(self, paths, callback):
        threading.Thread.__init__(self)
        self.paths = paths
        self.callback = callback

    def run(self):
        paths = self.paths
        sCharacter = Character.getInstance()
        for path in paths:
            try:
                # we try to parse api XML data first
                with open(path, mode='r') as charFile:
                    sheet = ParseXML(charFile)
                    char = sCharacter.new(sheet.name + " (imported)")
                    sCharacter.apiUpdateCharSheet(char.ID, sheet.skills)
            except:
                # if it's not api XML data, try this
                # this is a horrible logic flow, but whatever
                try:
                    charFile = open(path, mode='r').read()
                    doc = minidom.parseString(charFile)
                    if doc.documentElement.tagName not in ("SerializableCCPCharacter", "SerializableUriCharacter"):
                        raise RuntimeError("Incorrect EVEMon XML sheet")
                    name = doc.getElementsByTagName("name")[0].firstChild.nodeValue
                    skill_els = doc.getElementsByTagName("skill")
                    skills = []
                    for skill in skill_els:
                        skills.append({
                            "typeID": int(skill.getAttribute("typeID")),
                            "level": int(skill.getAttribute("level")),
                        })
                    char = sCharacter.new(name + " (EVEMon)")
                    sCharacter.apiUpdateCharSheet(char.ID, skills)
                except Exception as e:
                    print(e.message)
                    continue

        wx.CallAfter(self.callback)


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

        backupData = ""
        if self.saveFmt == "xml" or self.saveFmt == "emp":
            backupData = sCharacter.exportXml()
        else:
            backupData = sCharacter.exportText()

        if self.saveFmt == "emp":
            with gzip.open(path, mode='wb') as backupFile:
                backupFile.write(backupData)
        else:
            with open(path, mode='w', encoding='utf-8') as backupFile:
                backupFile.write(backupData)

        wx.CallAfter(self.callback)


class Character(object):
    instance = None
    skillReqsDict = {}

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Character()

        return cls.instance

    def __init__(self):
        # Simply initializes default characters in case they aren't in the database yet
        self.all0()
        self.all5()

    def exportText(self):
        data = "Pyfa exported plan for \"" + self.skillReqsDict['charname'] + "\"\n"
        data += "=" * 79 + "\n"
        data += "\n"
        item = ""
        for s in self.skillReqsDict['skills']:
            if item == "" or not item == s["item"]:
                item = s["item"]
                data += "-" * 79 + "\n"
                data += "Skills required for {}:\n".format(item)
            data += "{}{}: {}\n".format("    " * s["indent"], s["skill"], int(s["level"]))
        data += "-" * 79 + "\n"

        return data

    def exportXml(self):
        root = ElementTree.Element("plan")
        root.attrib["name"] = "Pyfa exported plan for " + self.skillReqsDict['charname']
        root.attrib["revision"] = config.evemonMinVersion

        sorts = ElementTree.SubElement(root, "sorting")
        sorts.attrib["criteria"] = "None"
        sorts.attrib["order"] = "None"
        sorts.attrib["groupByPriority"] = "false"

        skillsSeen = set()

        for s in self.skillReqsDict['skills']:
            skillKey = str(s["skillID"]) + "::" + s["skill"] + "::" + str(int(s["level"]))
            if skillKey in skillsSeen:
                pass   # Duplicate skills confuse EVEMon
            else:
                skillsSeen.add(skillKey)
                entry = ElementTree.SubElement(root, "entry")
                entry.attrib["skillID"] = str(s["skillID"])
                entry.attrib["skill"] = s["skill"]
                entry.attrib["level"] = str(int(s["level"]))
                entry.attrib["priority"] = "3"
                entry.attrib["type"] = "Prerequisite"
                notes = ElementTree.SubElement(entry, "notes")
                notes.text = entry.attrib["skill"]

        # tree = ElementTree.ElementTree(root)
        data = ElementTree.tostring(root, 'utf-8')
        prettydata = minidom.parseString(data).toprettyxml(indent="  ")

        return prettydata

    def backupSkills(self, path, saveFmt, activeFit, callback):
        thread = SkillBackupThread(path, saveFmt, activeFit, callback)
        thread.start()

    def importCharacter(self, path, callback):
        thread = CharacterImportThread(path, callback)
        thread.start()

    def all0(self):
        return es_Character.getAll0()

    def all0ID(self):
        return self.all0().ID

    def all5(self):
        return es_Character.getAll5()

    def all5ID(self):
        return self.all5().ID

    def saveCharacter(self, charID):
        """Save edited skills"""
        if charID == self.all5ID() or charID == self.all0ID():
            return
        char = getCharacter(charID)
        char.saveLevels()

    def saveCharacterAs(self, charID, newName):
        """Save edited skills as a new character"""
        char = getCharacter(charID)
        newChar = copy.deepcopy(char)
        newChar.name = newName
        eds_queries.save(newChar)

        # revert old char
        char.revertLevels()

    def revertCharacter(self, charID):
        """Rollback edited skills"""
        char = getCharacter(charID)
        char.revertLevels()

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
            if skill.published is True:
                skills.append((skill.ID, skill.name))
        return skills

    def getSkillDescription(self, itemID):
        return eds_queries.getItem(itemID).description

    def getGroupDescription(self, groupID):
        return eos.db.getMarketGroup(groupID).description

    def getSkillLevel(self, charID, skillID):
        skill = getCharacter(charID).getSkill(skillID)
        return (skill.level if skill.learned else "Not learned", skill.isDirty)

    def getDirtySkills(self, charID):
        return getCharacter(charID).dirtySkills

    def getCharName(self, charID):
        return getCharacter(charID).name

    def new(self, name="New Character"):
        char = es_Character(name)
        eds_queries.save(char)
        return char

    def rename(self, char, newName):
        char.name = newName
        eds_queries.commit()

    def copy(self, char):
        newChar = copy.deepcopy(char)
        eds_queries.save(newChar)
        return newChar

    def delete(self, char):
        eos.db.remove(char)

    def getApiDetails(self, charID):
        char = getCharacter(charID)
        if char.chars is not None:
            chars = json.loads(char.chars)
        else:
            chars = None
        return (char.apiID or "", char.apiKey or "", char.defaultChar or "", chars or [])

    def apiEnabled(self, charID):
        id, key, default, _ = self.getApiDetails(charID)
        return id is not "" and key is not "" and default is not ""

    def apiCharList(self, charID, userID, apiKey):
        char = getCharacter(charID)

        char.apiID = userID
        char.apiKey = apiKey

        api = EVEAPIConnection()
        auth = api.auth(keyID=userID, vCode=apiKey)
        apiResult = auth.account.Characters()
        charList = map(lambda c: unicode(c.name), apiResult.characters)

        char.chars = json.dumps(charList)
        return charList

    def apiFetch(self, charID, charName):
        dbChar = getCharacter(charID)
        dbChar.defaultChar = charName

        api = EVEAPIConnection()
        auth = api.auth(keyID=dbChar.apiID, vCode=dbChar.apiKey)
        apiResult = auth.account.Characters()
        charID = None
        for char in apiResult.characters:
            if char.name == charName:
                charID = char.characterID

        if charID is None:
            return

        sheet = auth.character(charID).CharacterSheet()

        dbChar.apiUpdateCharSheet(sheet.skills)
        eds_queries.commit()

    def apiUpdateCharSheet(self, charID, skills):
        char = getCharacter(charID)
        char.apiUpdateCharSheet(skills)
        eds_queries.commit()

    def changeLevel(self, charID, skillID, level, persist=False):
        char = getCharacter(charID)
        skill = char.getSkill(skillID)
        if isinstance(level, basestring) or level > 5 or level < 0:
            skill.level = None
        else:
            skill.level = level

        if persist:
            skill.saveLevel()

        eds_queries.commit()

    def revertLevel(self, charID, skillID):
        char = getCharacter(charID)
        skill = char.getSkill(skillID)
        skill.revert()

    def saveSkill(self, charID, skillID):
        char = getCharacter(charID)
        skill = char.getSkill(skillID)
        skill.saveLevel()

    def addImplant(self, charID, itemID):
        char = getCharacter(charID)
        if char.ro:
            logger.error("Trying to add implant to read-only character")
            return

        implant = es_Implant(eds_queries.getItem(itemID))
        char.implants.append(implant)
        eds_queries.commit()

    def removeImplant(self, charID, implant):
        char = getCharacter(charID)
        char.implants.remove(implant)
        eds_queries.commit()

    def getImplants(self, charID):
        char = getCharacter(charID)
        return char.implants

    def checkRequirements(self, fit):
        # toCheck = []
        reqs = {}
        for thing in itertools.chain(fit.modules, fit.drones, fit.fighters, (fit.ship,)):
            if isinstance(thing, es_Module) and thing.slot == es_Slot.RIG:
                continue
            for attr in ("item", "charge"):
                if attr == "charge" and isinstance(thing, es_Fighter):
                    # Fighter Bombers are automatically charged with micro bombs.
                    # These have skill requirements attached, but aren't used in EVE.
                    continue
                subThing = getattr(thing, attr, None)
                subReqs = {}
                if subThing is not None:
                    if isinstance(thing, es_Fighter) and attr == "charge":
                        continue
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
