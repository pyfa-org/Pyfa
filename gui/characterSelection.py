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

# noinspection PyPackageRequirements
import wx

from logbook import Logger

import gui.globalEvents as GE
import gui.mainFrame
from gui.bitmapLoader import BitmapLoader
from gui.utils.clipboard import toClipboard
from service.character import Character
from service.fit import Fit

pyfalog = Logger(__name__)


class CharacterSelection(wx.Panel):
    def __init__(self, parent):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(mainSizer)

        mainSizer.Add(wx.StaticText(self, wx.ID_ANY, "Character: "), 0, wx.CENTER | wx.RIGHT | wx.LEFT, 3)

        # cache current selection to fall back in case we choose to open char editor
        self.charCache = None

        self.charChoice = wx.Choice(self)
        mainSizer.Add(self.charChoice, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT, 3)

        self.refreshCharacterList()

        self.cleanSkills = BitmapLoader.getBitmap("skill_big", "gui")
        self.redSkills = BitmapLoader.getBitmap("skillRed_big", "gui")
        self.greenSkills = BitmapLoader.getBitmap("skillGreen_big", "gui")
        self.refresh = BitmapLoader.getBitmap("refresh", "gui")
        self.needsSkills = False

        self.btnRefresh = wx.BitmapButton(self, wx.ID_ANY, self.refresh)
        size = self.btnRefresh.GetSize()

        self.btnRefresh.SetMinSize(size)
        self.btnRefresh.SetMaxSize(size)
        self.btnRefresh.SetToolTipString("Refresh API")

        self.btnRefresh.Bind(wx.EVT_BUTTON, self.refreshApi)
        self.btnRefresh.Enable(False)

        mainSizer.Add(self.btnRefresh, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT, 2)

        self.skillReqsStaticBitmap = wx.StaticBitmap(self)
        self.skillReqsStaticBitmap.SetBitmap(self.cleanSkills)
        mainSizer.Add(self.skillReqsStaticBitmap, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT, 3)

        self.skillReqsStaticBitmap.Bind(wx.EVT_RIGHT_UP, self.OnContextMenu)

        self.Bind(wx.EVT_CHOICE, self.charChanged)
        self.mainFrame.Bind(GE.CHAR_LIST_UPDATED, self.refreshCharacterList)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)

        self.SetMinSize(wx.Size(25, -1))

        self.charChoice.Enable(False)

    def OnContextMenu(self, event):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.mainFrame.getActiveFit())

        if not fit or not self.needsSkills:
            return

        pos = wx.GetMousePosition()
        pos = self.ScreenToClient(pos)

        menu = wx.Menu()

        grantItem = menu.Append(wx.ID_ANY, "Grant Missing Skills")
        self.Bind(wx.EVT_MENU, self.grantMissingSkills, grantItem)

        exportItem = menu.Append(wx.ID_ANY, "Export Missing Skills")
        self.Bind(wx.EVT_MENU, self.exportSkills, exportItem)

        self.PopupMenu(menu, pos)

        event.Skip()

    def grantMissingSkills(self, evt):
        charID = self.getActiveCharacter()
        sChar = Character.getInstance()

        skillsMap = self._buildSkillsTooltipCondensed(self.reqs, skillsMap={})

        for index in skillsMap:
            sChar.changeLevel(charID, skillsMap[index][1], skillsMap[index][0], ifHigher=True)

        self.refreshCharacterList()

    def getActiveCharacter(self):
        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection is not -1 else None

    def refreshCharacterList(self, event=None):
        choice = self.charChoice
        sChar = Character.getInstance()
        activeChar = self.getActiveCharacter()

        choice.Clear()
        charList = sorted(sChar.getCharacterList(), key=lambda c: (not c.ro, c.name))
        picked = False

        for char in charList:
            currId = choice.Append(char.name, char.ID)
            if char.ID == activeChar:
                choice.SetSelection(currId)
                self.charChanged(None)
                picked = True

        if not picked:
            charID = sChar.all5ID()
            self.selectChar(charID)
            fitID = self.mainFrame.getActiveFit()
            sFit = Fit.getInstance()
            sFit.changeChar(fitID, charID)

        choice.Append(u"\u2015 Open Character Editor \u2015", -1)
        self.charCache = self.charChoice.GetCurrentSelection()

        if event is not None:
            event.Skip()

    def refreshApi(self, event):
        self.btnRefresh.Enable(False)
        sChar = Character.getInstance()
        ID, key, charName, chars = sChar.getApiDetails(self.getActiveCharacter())
        if charName:
            sChar.apiFetch(self.getActiveCharacter(), charName, self.refreshAPICallback)

    def refreshAPICallback(self, e=None):
        self.btnRefresh.Enable(True)
        if e is None:
            self.refreshCharacterList()
        else:
            exc_type, exc_obj, exc_trace = e
            pyfalog.warn("Error fetching API information for character")
            pyfalog.warn(exc_obj)

            wx.MessageBox(
                "Error fetching API information, please check your API details in the character editor and try again later",
                "Error", wx.ICON_ERROR | wx.STAY_ON_TOP)

    def charChanged(self, event):
        fitID = self.mainFrame.getActiveFit()
        charID = self.getActiveCharacter()
        sChar = Character.getInstance()

        if charID == -1:
            # revert to previous character
            self.charChoice.SetSelection(self.charCache)
            self.mainFrame.showCharacterEditor(event)
            return
        if sChar.getCharName(charID) not in ("All 0", "All 5") and sChar.apiEnabled(charID):
            self.btnRefresh.Enable(True)
        else:
            self.btnRefresh.Enable(False)

        sFit = Fit.getInstance()
        sFit.changeChar(fitID, charID)
        self.charCache = self.charChoice.GetCurrentSelection()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def selectChar(self, charID):
        choice = self.charChoice
        numItems = len(choice.GetItems())
        for i in range(numItems):
            id_ = choice.GetClientData(i)
            if id_ == charID:
                choice.SetSelection(i)
                return True

        return False

    def fitChanged(self, event):
        """
        When fit is changed, or new fit is selected
        """
        self.charChoice.Enable(event.fitID is not None)
        choice = self.charChoice
        sFit = Fit.getInstance()
        currCharID = choice.GetClientData(choice.GetCurrentSelection())
        fit = sFit.getFit(event.fitID)
        newCharID = fit.character.ID if fit is not None else None

        if event.fitID is None:
            self.skillReqsStaticBitmap.SetBitmap(self.cleanSkills)
            self.skillReqsStaticBitmap.SetToolTipString("No active fit")
        else:
            sCharacter = Character.getInstance()
            self.reqs = sCharacter.checkRequirements(fit)

            sCharacter.skillReqsDict = {'charname': fit.character.name, 'skills': []}
            if len(self.reqs) == 0:
                self.needsSkills = False
                tip = "All skill prerequisites have been met"
                self.skillReqsStaticBitmap.SetBitmap(self.greenSkills)
            else:
                self.needsSkills = True
                tip = "Skills required:\n"
                condensed = sFit.serviceFittingOptions["compactSkills"]
                if condensed:
                    dict_ = self._buildSkillsTooltipCondensed(self.reqs, skillsMap={})
                    for key in sorted(dict_):
                        tip += "%s: %d\n" % (key, dict_[key][0])
                else:
                    tip += self._buildSkillsTooltip(self.reqs)
                self.skillReqsStaticBitmap.SetBitmap(self.redSkills)
            self.skillReqsStaticBitmap.SetToolTipString(tip.strip())

        if newCharID is None:
            sChar = Character.getInstance()
            self.selectChar(sChar.all5ID())

        elif currCharID != newCharID:
            self.selectChar(newCharID)
            if not fit.calculated:
                self.charChanged(None)

        event.Skip()

    def exportSkills(self, evt):
        skillsMap = self._buildSkillsTooltipCondensed(self.reqs, skillsMap={})

        list = ""
        for key in sorted(skillsMap):
            list += "%s %d\n" % (key, skillsMap[key][0])

        toClipboard(list)

    def _buildSkillsTooltip(self, reqs, currItem="", tabulationLevel=0):
        tip = ""
        sCharacter = Character.getInstance()

        if tabulationLevel == 0:
            for item, subReqs in reqs.iteritems():
                tip += "%s:\n" % item.name
                tip += self._buildSkillsTooltip(subReqs, item.name, 1)
        else:
            for name, info in reqs.iteritems():
                level, ID, more = info
                sCharacter.skillReqsDict['skills'].append({
                    'item': currItem,
                    'skillID': ID,
                    'skill': name,
                    'level': level,
                    'indent': tabulationLevel,
                })

                tip += "%s%s: %d\n" % ("    " * tabulationLevel, name, level)
                tip += self._buildSkillsTooltip(more, currItem, tabulationLevel + 1)

        return tip

    def _buildSkillsTooltipCondensed(self, reqs, currItem="", tabulationLevel=0, skillsMap=None):
        if skillsMap is None:
            skillsMap = {}

        sCharacter = Character.getInstance()

        if tabulationLevel == 0:
            for item, subReqs in reqs.iteritems():
                skillsMap = self._buildSkillsTooltipCondensed(subReqs, item.name, 1, skillsMap)
            sorted(skillsMap, key=skillsMap.get)
        else:
            for name, info in reqs.iteritems():
                level, ID, more = info
                sCharacter.skillReqsDict['skills'].append({
                    'item': currItem,
                    'skillID': ID,
                    'skill': name,
                    'level': level,
                    'indent': tabulationLevel,
                })

                if name not in skillsMap:
                    skillsMap[name] = level, ID
                elif skillsMap[name][0] < level:
                    skillsMap[name] = level, ID

                skillsMap = self._buildSkillsTooltipCondensed(more, currItem, tabulationLevel + 1, skillsMap)

        return skillsMap
