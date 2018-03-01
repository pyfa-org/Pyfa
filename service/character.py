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

import sys
import copy
import itertools
import json

from logbook import Logger
import threading
from codecs import open
from xml.etree import ElementTree
from xml.dom import minidom
import gzip

# noinspection PyPackageRequirements
import wx

import config
import eos.db
from service.eveapi import EVEAPIConnection, ParseXML

from eos.saveddata.implant import Implant as es_Implant
from eos.saveddata.character import Character as es_Character
from eos.saveddata.module import Slot as es_Slot, Module as es_Module
from eos.saveddata.fighter import Fighter as es_Fighter

pyfalog = Logger(__name__)


class CharacterImportThread(threading.Thread):
    def __init__(self, paths, callback):
        threading.Thread.__init__(self)
        self.name = "CharacterImport"
        self.paths = paths
        self.callback = callback

    def run(self):
        paths = self.paths
        sCharacter = Character.getInstance()
        all5_character = es_Character("All 5", 5)
        all_skill_ids = []
        for skill in all5_character.skills:
            # Parse out the skill item IDs to make searching it easier later on
            all_skill_ids.append(skill.itemID)

        for path in paths:
            try:
                # we try to parse api XML data first
                with open(path, mode='r') as charFile:
                    sheet = ParseXML(charFile)
                    char = sCharacter.new(sheet.name + " (imported)")
                    sCharacter.apiUpdateCharSheet(char.ID, sheet.skills, 0)
            except:
                # if it's not api XML data, try this
                # this is a horrible logic flow, but whatever
                try:
                    charFile = open(path, mode='r').read()
                    doc = minidom.parseString(charFile)
                    if doc.documentElement.tagName not in ("SerializableCCPCharacter", "SerializableUriCharacter"):
                        pyfalog.error("Incorrect EVEMon XML sheet")
                        raise RuntimeError("Incorrect EVEMon XML sheet")
                    name = doc.getElementsByTagName("name")[0].firstChild.nodeValue
                    securitystatus = float(doc.getElementsByTagName("securityStatus")[0].firstChild.nodeValue) or 0.0
                    skill_els = doc.getElementsByTagName("skill")
                    skills = []
                    for skill in skill_els:
                        if int(skill.getAttribute("typeID")) in all_skill_ids and (0 <= int(skill.getAttribute("level")) <= 5):
                            skills.append({
                                "typeID": int(skill.getAttribute("typeID")),
                                "level": int(skill.getAttribute("level")),
                            })
                        else:
                            pyfalog.error(
                                    "Attempted to import unknown skill {0} (ID: {1}) (Level: {2})",
                                    skill.getAttribute("name"),
                                    skill.getAttribute("typeID"),
                                    skill.getAttribute("level"),
                            )
                    char = sCharacter.new(name + " (EVEMon)")
                    sCharacter.apiUpdateCharSheet(char.ID, skills, securitystatus)
                except Exception, e:
                    pyfalog.error("Exception on character import:")
                    pyfalog.error(e)
                    continue

        wx.CallAfter(self.callback)


class SkillBackupThread(threading.Thread):
    def __init__(self, path, saveFmt, activeFit, callback):
        threading.Thread.__init__(self)
        self.name = "SkillBackup"
        self.path = path
        self.saveFmt = saveFmt
        self.activeFit = activeFit
        self.callback = callback

    def run(self):
        path = self.path
        sCharacter = Character.getInstance()
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
        data = u"Pyfa exported plan for \"" + self.skillReqsDict['charname'] + "\"\n"
        data += u"=" * 79 + u"\n"
        data += u"\n"
        item = u""
        try:
            for s in self.skillReqsDict['skills']:
                if item == "" or not item == s["item"]:
                    item = s["item"]
                    data += u"-" * 79 + "\n"
                    data += u"Skills required for {}:\n".format(item)
                data += u"{}{}: {}\n".format("    " * s["indent"], s["skill"], int(s["level"]))
            data += u"-" * 79 + "\n"
        except Exception:
            pass

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
                pass  # Duplicate skills confuse EVEMon
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

    @staticmethod
    def backupSkills(path, saveFmt, activeFit, callback):
        thread = SkillBackupThread(path, saveFmt, activeFit, callback)
        pyfalog.debug("Starting backup skills thread.")
        thread.start()

    @staticmethod
    def importCharacter(path, callback):
        thread = CharacterImportThread(path, callback)
        pyfalog.debug("Starting import character thread.")
        thread.start()

    @staticmethod
    def all0():
        return es_Character.getAll0()

    def all0ID(self):
        return self.all0().ID

    @staticmethod
    def all5():
        return es_Character.getAll5()

    def all5ID(self):
        return self.all5().ID

    @staticmethod
    def getAlphaCloneList():
        return eos.db.getAlphaCloneList()

    @staticmethod
    def getCharacterList():
        return eos.db.getCharacterList()

    @staticmethod
    def getCharacter(charID):
        char = eos.db.getCharacter(charID)
        return char

    def saveCharacter(self, charID):
        """Save edited skills"""
        if charID == self.all5ID() or charID == self.all0ID():
            return
        char = eos.db.getCharacter(charID)
        char.saveLevels()

    @staticmethod
    def saveCharacterAs(charID, newName):
        """Save edited skills as a new character"""
        char = eos.db.getCharacter(charID)
        newChar = copy.deepcopy(char)
        newChar.name = newName
        eos.db.save(newChar)

        # revert old char
        char.revertLevels()
        return newChar.ID

    @staticmethod
    def revertCharacter(charID):
        """Rollback edited skills"""
        char = eos.db.getCharacter(charID)
        char.revertLevels()

    @staticmethod
    def getSkillGroups():
        cat = eos.db.getCategory(16)
        groups = []
        for grp in cat.groups:
            if grp.published:
                groups.append((grp.ID, grp.name))
        return groups

    @staticmethod
    def getSkills(groupID):
        group = eos.db.getGroup(groupID)
        skills = []
        for skill in group.items:
            if skill.published is True:
                skills.append((skill.ID, skill.name))
        return skills

    @staticmethod
    def getSkillsByName(text):
        items = eos.db.searchSkills(text)
        skills = []
        for skill in items:
            if skill.published is True:
                skills.append((skill.ID, skill.name))
        return skills

    @staticmethod
    def setAlphaClone(char, cloneID):
        char.alphaCloneID = cloneID
        eos.db.commit()

    @staticmethod
    def setSecStatus(char, secStatus):
        char.secStatus = secStatus
        eos.db.commit()

    @staticmethod
    def getSkillDescription(itemID):
        return eos.db.getItem(itemID).description

    @staticmethod
    def getGroupDescription(groupID):
        return eos.db.getMarketGroup(groupID).description

    @staticmethod
    def getSkillLevel(charID, skillID):
        skill = eos.db.getCharacter(charID).getSkill(skillID)
        return float(skill.level) if skill.learned else "Not learned", skill.isDirty

    @staticmethod
    def getDirtySkills(charID):
        return eos.db.getCharacter(charID).dirtySkills

    @staticmethod
    def getCharName(charID):
        return eos.db.getCharacter(charID).name

    @staticmethod
    def new(name="New Character"):
        char = es_Character(name)
        eos.db.save(char)
        return char

    @staticmethod
    def rename(char, newName):
        if char.name in ("All 0", "All 5"):
            pyfalog.info("Cannot rename built in characters.")
        else:
            char.name = newName
            eos.db.commit()

    @staticmethod
    def copy(char):
        newChar = copy.deepcopy(char)
        eos.db.save(newChar)
        return newChar

    @staticmethod
    def delete(char):
        eos.db.remove(char)

    @staticmethod
    def getApiDetails(charID):
        char = eos.db.getCharacter(charID)
        if char.chars is not None:
            chars = json.loads(char.chars)
        else:
            chars = None
        return char.apiID or "", char.apiKey or "", char.defaultChar or "", chars or []

    def apiEnabled(self, charID):
        id_, key, default, _ = self.getApiDetails(charID)
        return id_ is not "" and key is not "" and default is not ""

    @staticmethod
    def apiCharList(charID, userID, apiKey):
        char = eos.db.getCharacter(charID)

        char.apiID = userID
        char.apiKey = apiKey

        api = EVEAPIConnection()
        auth = api.auth(keyID=userID, vCode=apiKey)
        apiResult = auth.account.Characters()
        charList = map(lambda c: unicode(c.name), apiResult.characters)

        char.chars = json.dumps(charList)
        return charList

    def apiFetch(self, charID, charName, callback):
        thread = UpdateAPIThread(charID, charName, (self.apiFetchCallback, callback))
        thread.start()

    def apiFetchCallback(self, guiCallback, e=None):
        eos.db.commit()
        wx.CallAfter(guiCallback, e)

    @staticmethod
    def apiUpdateCharSheet(charID, skills, securitystatus):
        char = eos.db.getCharacter(charID)
        char.apiUpdateCharSheet(skills, securitystatus)
        eos.db.commit()

    @staticmethod
    def changeLevel(charID, skillID, level, persist=False, ifHigher=False):
        char = eos.db.getCharacter(charID)
        skill = char.getSkill(skillID)

        if ifHigher and level < skill.level:
            return

        if isinstance(level, basestring) or level > 5 or level < 0:
            skill.setLevel(None, persist)
        else:
            skill.setLevel(level, persist)

        eos.db.commit()

    @staticmethod
    def revertLevel(charID, skillID):
        char = eos.db.getCharacter(charID)
        skill = char.getSkill(skillID)
        skill.revert()

    @staticmethod
    def saveSkill(charID, skillID):
        char = eos.db.getCharacter(charID)
        skill = char.getSkill(skillID)
        skill.saveLevel()

    @staticmethod
    def addImplant(charID, itemID):
        char = eos.db.getCharacter(charID)
        if char.ro:
            pyfalog.error("Trying to add implant to read-only character")
            return

        implant = es_Implant(eos.db.getItem(itemID))
        char.implants.append(implant)
        eos.db.commit()

    @staticmethod
    def removeImplant(charID, implant):
        char = eos.db.getCharacter(charID)
        char.implants.remove(implant)
        eos.db.commit()

    @staticmethod
    def getImplants(charID):
        char = eos.db.getCharacter(charID)
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


class UpdateAPIThread(threading.Thread):
    def __init__(self, charID, charName, callback):
        threading.Thread.__init__(self)

        self.name = "CheckUpdate"
        self.callback = callback
        self.charID = charID
        self.charName = charName

    def run(self):
        try:
            dbChar = eos.db.getCharacter(self.charID)
            dbChar.defaultChar = self.charName

            api = EVEAPIConnection()
            auth = api.auth(keyID=dbChar.apiID, vCode=dbChar.apiKey)
            apiResult = auth.account.Characters()
            charID = None
            for char in apiResult.characters:
                if char.name == self.charName:
                    charID = char.characterID
                    break

            if charID is None:
                return

            sheet = auth.character(charID).CharacterSheet()
            charInfo = api.eve.CharacterInfo(characterID=charID)

            dbChar.apiUpdateCharSheet(sheet.skills, charInfo.securityStatus)
            self.callback[0](self.callback[1])
        except Exception:
            self.callback[0](self.callback[1], sys.exc_info())
