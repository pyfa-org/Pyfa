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
from gui import fittingView as fv
import gui.mainFrame

class CharacterSelection(wx.Panel):
    def __init__(self, parent):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(mainSizer)

        mainSizer.Add(wx.StaticText(self, wx.ID_ANY, "Character: "), 0, wx.CENTER)

        self.charChoice = wx.Choice(self)
        mainSizer.Add(self.charChoice, 1, wx.ALIGN_CENTER_VERTICAL)

        self.refreshCharacterList()

        self.skillReqsStaticBitmap = wx.StaticBitmap(self)
        mainSizer.Add(self.skillReqsStaticBitmap, 0, wx.ALIGN_CENTER_VERTICAL)

        self.cleanSkills = bitmapLoader.getBitmap("skill_big", "icons")
        self.redSkills = bitmapLoader.getBitmap("skillRed_big", "icons")
        self.greenSkills = bitmapLoader.getBitmap("skillGreen_big", "icons")

        self.skillReqsStaticBitmap.SetBitmap(self.cleanSkills)
        self.Bind(wx.EVT_CHOICE, self.charChanged)
        self.mainFrame.Bind(ce.CHAR_LIST_UPDATED, self.refreshCharacterList)
        self.mainFrame.Bind(fv.FIT_CHANGED, self.fitChanged)

        panelSize = wx.Size(-1,30)
        self.SetMinSize(panelSize)

        self.Enable(False)

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
        for id, name, active in charList:
            currId = choice.Append(name, id)
            if id == activeChar:
                choice.SetSelection(currId)
            elif activeChar is None and name == "All 0":
                all0 = currId

        if activeChar is None:
            choice.SetSelection(all0)

        if event is not None:
            event.Skip()

    def charChanged(self, event):
        fitID = self.mainFrame.fitMultiSwitch.getActiveFit()
        charID = self.getActiveCharacter()

        cFit = service.Fit.getInstance()
        cFit.changeChar(fitID, charID)

        wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=fitID))

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
        self.Enable(event.fitID != None)

        choice = self.charChoice
        cFit = service.Fit.getInstance()
        currCharID = choice.GetClientData(choice.GetCurrentSelection())
        fit = cFit.getFit(event.fitID)
        newCharID = fit.character.ID if fit is not None else None
        if event.fitID is None:
            self.skillReqsStaticBitmap.SetBitmap(self.cleanSkills)
        else:
            sCharacter = service.Character.getInstance()
            reqs = sCharacter.checkRequirements(fit)
            if len(reqs) == 0:
                self.skillReqsStaticBitmap.SetBitmap(self.greenSkills)
                self.skillReqsStaticBitmap.SetToolTip(None)
            else:
                tip = self._buildSkillsTooltip(reqs)
                self.skillReqsStaticBitmap.SetBitmap(self.redSkills)
                self.skillReqsStaticBitmap.SetToolTipString(tip.strip())

        if newCharID == None:
            cChar = service.Character.getInstance()
            self.selectChar(cChar.all0ID())
        elif currCharID != newCharID:
            self.selectChar(newCharID)

        event.Skip()

    def _buildSkillsTooltip(self, reqs, tabulationLevel = 0):
        tip = ""
        for name, info in reqs.iteritems():
            level, more = info
            tip += "%s%s: %d\n" % ("  " * tabulationLevel, name, level)
            tip += self._buildSkillsTooltip(more, tabulationLevel + 1)

        return tip
