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
import controller
from gui import characterEditor as ce
from gui import shipBrowser as sb
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
        mainSizer.Add(self.charChoice, 1, wx.EXPAND)

        self.refreshCharacterList()

        self.Bind(wx.EVT_CHOICE, self.charChanged)
        self.mainFrame.Bind(ce.CHAR_LIST_UPDATED, self.refreshCharacterList)
        self.mainFrame.Bind(fv.FIT_CHANGED, self.fitChanged)

        panelSize = self.GetSize()
        panelSize.height += 5
        self.SetMinSize(panelSize)

        self.Enable(False)

    def getActiveCharacter(self):
        selection = self.charChoice.GetCurrentSelection()
        return self.charChoice.GetClientData(selection) if selection is not -1 else None

    def refreshCharacterList(self, event=None):
        choice = self.charChoice
        cChar = controller.Character.getInstance()
        activeChar = self.getActiveCharacter()

        choice.Clear()
        for id, name in cChar.getCharacterList():
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

        cFit = controller.Fit.getInstance()
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
        cFit = controller.Fit.getInstance()
        currCharID = choice.GetClientData(choice.GetCurrentSelection())
        fit = cFit.getFit(event.fitID)
        newCharID = fit.character.ID if fit is not None else None

        if newCharID == None:
            cChar = controller.Character.getInstance()
            self.selectChar(cChar.all0ID())
        elif currCharID != newCharID:
            self.selectChar(newCharID)

        event.Skip()
