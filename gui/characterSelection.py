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

import wx
import service
from gui import characterEditor as ce
from gui import bitmapLoader
import gui.globalEvents as GE
import gui.mainFrame

class CharacterSelection(wx.Panel):
    def __init__(self, parent):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(mainSizer)

        mainSizer.Add(wx.StaticText(self, wx.ID_ANY, "Character: "), 0, wx.CENTER | wx.TOP | wx.RIGHT | wx.LEFT, 3)

        self.charChoice = wx.Choice(self)
        mainSizer.Add(self.charChoice, 1, wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.RIGHT | wx.LEFT, 3)

        self.refreshCharacterList()

        self.skillReqsStaticBitmap = wx.StaticBitmap(self)
        mainSizer.Add(self.skillReqsStaticBitmap, 0, wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.RIGHT | wx.LEFT, 3)

        self.cleanSkills = bitmapLoader.getBitmap("skill_big", "icons")
        self.redSkills   = bitmapLoader.getBitmap("skillRed_big", "icons")
        self.greenSkills = bitmapLoader.getBitmap("skillGreen_big", "icons")
        self.refresh     = bitmapLoader.getBitmap("refresh", "icons")

        self.skillReqsStaticBitmap.SetBitmap(self.cleanSkills)

        self.btnRefresh = wx.BitmapButton(self, wx.ID_ANY, self.refresh)
        size = self.btnRefresh.GetSize()

        self.btnRefresh.SetMinSize(size)
        self.btnRefresh.SetMaxSize(size)
        self.btnRefresh.SetToolTipString("Refresh API")

        self.btnRefresh.Bind(wx.EVT_BUTTON, self.refreshApi)
        self.btnRefresh.Enable(False)
        mainSizer.Add(self.btnRefresh, 0, wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        
        self.Bind(wx.EVT_CHOICE, self.charChanged)
        self.mainFrame.Bind(GE.CHAR_LIST_UPDATED, self.refreshCharacterList)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)

#        panelSize = wx.Size(-1,30)
#        self.SetMinSize(panelSize)

        self.charChoice.Enable(False)

    def getActiveCharacter(self):
        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection is not -1 else None

    def refreshCharacterList(self, event=None):
        choice = self.charChoice
        cChar = service.Character.getInstance()
        activeChar = self.getActiveCharacter()

        choice.Clear()
        charList = cChar.getCharacterList()
        cChar.getCharacterList()
        picked = False

        for id, name, active in charList:
            currId = choice.Append(name, id)
            if id == activeChar:
                choice.SetSelection(currId)
                self.charChanged(None)
                picked = True

        if not picked:
            charID = cChar.all5ID()
            self.selectChar(charID)
            fitID = self.mainFrame.getActiveFit()
            cFit = service.Fit.getInstance()
            cFit.changeChar(fitID, charID)

        if event is not None:
            event.Skip()

    def refreshApi(self, event):
        cChar = service.Character.getInstance()
        ID, key, charName, chars = cChar.getApiDetails(self.getActiveCharacter())
        if charName:
            try:
                cChar.apiFetch(self.getActiveCharacter(), charName)
            except:
                # can we do a popup, notifying user of API error?
                pass
        self.refreshCharacterList()
        
    def charChanged(self, event):
        fitID = self.mainFrame.getActiveFit()
        charID = self.getActiveCharacter()
        cChar = service.Character.getInstance()

        if cChar.getCharName(charID) not in ("All 0", "All 5") and cChar.apiEnabled(charID):
            self.btnRefresh.Enable(True)
        else:
            self.btnRefresh.Enable(False)

        cFit = service.Fit.getInstance()
        cFit.changeChar(fitID, charID)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def selectChar(self, charID):
        choice = self.charChoice
        numItems = len(choice.GetItems())
        for i in xrange(numItems):
            id = choice.GetClientData(i)
            if id == charID:
                choice.SetSelection(i)
                return True

        return False

    def fitChanged(self, event):
        self.charChoice.Enable(event.fitID != None)
        choice = self.charChoice
        cFit = service.Fit.getInstance()
        currCharID = choice.GetClientData(choice.GetCurrentSelection())
        fit = cFit.getFit(event.fitID)
        newCharID = fit.character.ID if fit is not None else None
        if event.fitID is None:
            self.skillReqsStaticBitmap.SetBitmap(self.cleanSkills)
            self.skillReqsStaticBitmap.SetToolTipString("No active fit")
        else:
            sCharacter = service.Character.getInstance()
            reqs = sCharacter.checkRequirements(fit)
            sCharacter.skillReqsDict = {'charname':fit.character.name, 'skills':[]}
            if len(reqs) == 0:
                tip = "All skill prerequisites have been met"
                self.skillReqsStaticBitmap.SetBitmap(self.greenSkills)
            else:
                tip  = "Skills required:\n"
                tip += self._buildSkillsTooltip(reqs)
                self.skillReqsStaticBitmap.SetBitmap(self.redSkills)
            self.skillReqsStaticBitmap.SetToolTipString(tip.strip())

        if newCharID == None:
            cChar = service.Character.getInstance()
            self.selectChar(cChar.all5ID())
            
        elif currCharID != newCharID:
            self.selectChar(newCharID)
            self.charChanged(None)

        
        event.Skip()

    def _buildSkillsTooltip(self, reqs, currItem = "", tabulationLevel = 0):
        tip = ""
        sCharacter = service.Character.getInstance()
        if tabulationLevel == 0:
            for item, subReqs in reqs.iteritems():
                tip += " %s:\n" % item.name
                tip += self._buildSkillsTooltip(subReqs, item.name, 1)
        else:
            for name, info in reqs.iteritems():
                level, ID, more = info
                sCharacter.skillReqsDict['skills'].append({
                    'item' : currItem,
                    'skillID' : ID,
                    'skill' : name,
                    'level' : level,
                    'indent' : tabulationLevel
                })
                tip += "  %s%s: %d\n" % ("  " * tabulationLevel, name, level)
                tip += self._buildSkillsTooltip(more, currItem, tabulationLevel + 1)

        return tip
