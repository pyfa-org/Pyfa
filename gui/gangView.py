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

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from service.fit import Fit
from service.fleet import Fleet
from service.character import Character
from service.market import Market

import gui.mainFrame
import gui.shipBrowser
import gui.globalEvents as GE


class GangView(ScrolledPanel):
    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(100, 20), style=wx.TAB_TRAVERSAL | wx.HSCROLL | wx.VSCROLL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.draggedFitID = None

        help_msg = '''Set fit as booster to display in dropdown, or drag fitting from\nship browser to this window, or right click fit and select booster role.'''
        helpSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.helpText = wx.StaticText(self, wx.ID_ANY, help_msg, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        helpSizer.Add(self.helpText, 1, wx.ALL, 5)

        self.options = ["Fleet", "Wing", "Squad"]

        self.fleet = {}
        for id_, option in enumerate(self.options):

            # set content for each commander
            self.fleet[id_] = {}
            self.fleet[id_]['stLabel'] = wx.StaticText(self, wx.ID_ANY, self.options[id_] + ':', wx.DefaultPosition, wx.DefaultSize, 0)
            self.fleet[id_]['stText'] = wx.StaticText(self, wx.ID_ANY, 'None', wx.DefaultPosition, wx.DefaultSize, 0)
            self.fleet[id_]['chFit'] = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [])
            self.fleet[id_]['chChar'] = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [])
            self.fleet[id_]['fitSizer'] = wx.BoxSizer(wx.VERTICAL)

        self.FitDNDPopupMenu = self.buildBoostermenu()

        contentFGSizer = wx.FlexGridSizer(5, 3, 0, 0)
        contentFGSizer.AddGrowableCol(1)
        contentFGSizer.SetFlexibleDirection(wx.BOTH)
        contentFGSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Header
        self.stBooster = wx.StaticText(self, wx.ID_ANY, u"Booster", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stBooster.Wrap(-1)
        self.stBooster.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        contentFGSizer.Add(self.stBooster, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.stFits = wx.StaticText(self, wx.ID_ANY, u"Fits", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stFits.Wrap(-1)
        self.stFits.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        contentFGSizer.Add(self.stFits, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.stCharacters = wx.StaticText(self, wx.ID_ANY, u"Characters", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stCharacters.Wrap(-1)
        self.stCharacters.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        contentFGSizer.Add(self.stCharacters, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        contentFGSizer.Add(self.m_staticline2, 0, wx.EXPAND, 5)

        self.m_staticline3 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        contentFGSizer.Add(self.m_staticline3, 0, wx.EXPAND, 5)

        self.m_staticline4 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        contentFGSizer.Add(self.m_staticline4, 0, wx.EXPAND, 5)

        # Content
        for id_ in self.fleet:
            # set various properties
            self.fleet[id_]['stLabel'].Wrap(-1)
            self.fleet[id_]['stLabel'].SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
            self.fleet[id_]['stText'].Wrap(-1)

            # bind text and choice events
            self.fleet[id_]['stText'].Bind(wx.EVT_LEFT_DCLICK, self.RemoveBooster)
            self.fleet[id_]['stText'].Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
            self.fleet[id_]['stText'].Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
            self.fleet[id_]['stText'].SetToolTip(wx.ToolTip("Double click to remove booster"))
            self.fleet[id_]['chChar'].Bind(wx.EVT_CHOICE, self.CharChanged)
            self.fleet[id_]['chFit'].Bind(wx.EVT_CHOICE, self.OnFitChoiceSelected)

            # add fit text and choice to the fit sizer
            self.fleet[id_]['fitSizer'].Add(self.fleet[id_]['stText'], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.fleet[id_]['fitSizer'].Add(self.fleet[id_]['chFit'], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 1)

            # add everything to the content sizer
            contentFGSizer.Add(self.fleet[id_]['stLabel'], 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            contentFGSizer.Add(self.fleet[id_]['fitSizer'], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 5)
            contentFGSizer.Add(self.fleet[id_]['chChar'], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        mainSizer.Add(contentFGSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(helpSizer, 0, wx.EXPAND, 0)

        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)
        self.SetupScrolling()

        self.mainFrame.Bind(GE.CHAR_LIST_UPDATED, self.RefreshCharacterList)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitSelected)
        self.mainFrame.Bind(gui.shipBrowser.EVT_FIT_RENAMED, self.fitRenamed)
        self.mainFrame.Bind(gui.shipBrowser.BOOSTER_LIST_UPDATED, self.RefreshBoosterFits)

        self.RefreshBoosterFits()
        self.RefreshCharacterList()

    def buildBoostermenu(self):
        menu = wx.Menu()

        for option in self.options:
            item = menu.Append(-1, option)
            # We bind it to the mainFrame because it may be called from either this class or from FitItem via shipBrowser
            self.mainFrame.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
        return menu

    def OnEnterWindow(self, event):
        obj = event.GetEventObject()
        obj.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWindow(self, event):
        obj = event.GetEventObject()
        obj.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
        event.Skip()

    def CharChanged(self, event):
        ''' Change booster character '''
        chBooster = event.GetEventObject()

        type_ = -1
        for id_ in self.fleet:
            if chBooster == self.fleet[id_]['chChar']:
                type_ = id_

        if type_ == -1:
            event.Skip()
            return

        sFit = Fit.getInstance()

        fleetSrv = Fleet.getInstance()

        activeFitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(activeFitID)

        # sChar = Character.getInstance()
        # charList = sChar.getCharacterList()

        if activeFitID:
            commanders = fleetSrv.loadLinearFleet(fit)
            if commanders is None:
                fleetCom, wingCom, squadCom = (None, None, None)
            else:
                fleetCom, wingCom, squadCom = commanders

            if type_ == 0:
                if fleetCom:
                    charID = chBooster.GetClientData(chBooster.GetSelection())
                    sFit.changeChar(fleetCom.ID, charID)
                else:
                    chBooster.SetSelection(0)

            if type_ == 1:
                if wingCom:
                    charID = chBooster.GetClientData(chBooster.GetSelection())
                    sFit.changeChar(wingCom.ID, charID)
                else:
                    chBooster.SetSelection(0)

            if type_ == 2:
                if squadCom:
                    charID = chBooster.GetClientData(chBooster.GetSelection())
                    sFit.changeChar(squadCom.ID, charID)
                else:
                    chBooster.SetSelection(0)

            sFit.recalc(fit, withBoosters=True)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=activeFitID))

        else:
            chBooster.SetSelection(0)

    def RemoveBooster(self, event):
        activeFitID = self.mainFrame.getActiveFit()
        if not activeFitID:
            return

        location = event.GetEventObject()

        for id_ in self.fleet:
            if location == self.fleet[id_]['stText']:
                type_ = id_

        sFit = Fit.getInstance()
        boostee = sFit.getFit(activeFitID)
        booster = None

        fleetSrv = Fleet.getInstance()

        if type_ == 0:
            fleetSrv.setLinearFleetCom(boostee, booster)
        elif type_ == 1:
            fleetSrv.setLinearWingCom(boostee, booster)
        elif type_ == 2:
            fleetSrv.setLinearSquadCom(boostee, booster)

        # Hide stText and, default fit selection, and enable it
        location.Hide()
        choice = self.fleet[type_]['chFit']
        choice.SetSelection(0)
        choice.Show()

        sFit.recalc(boostee, withBoosters=True)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=activeFitID))

    def fitRenamed(self, event):
        # fleetSrv = Fleet.getInstance()
        activeFitID = self.mainFrame.getActiveFit()

        if activeFitID:
            ev = event
            ev.fitID = activeFitID
            self.fitSelected(ev)

    def fitSelected(self, event):
        ''' Fires when active fit is selected and when booster is saved to fit. Update the UI to reflect changes '''
        fleetSrv = Fleet.getInstance()

        activeFitID = self.mainFrame.getActiveFit()
        sFit = Fit.getInstance()
        fit = sFit.getFit(event.fitID or activeFitID)

        self.Parent.Parent.DisablePage(self, not fit or fit.isStructure)

        commanders = (None, None, None)

        if activeFitID:
            commanders = fleetSrv.loadLinearFleet(fit)

        for id_ in self.fleet:
            # try...except here as we're trying 2 different criteria and want to fall back on the same code
            try:
                commander = commanders[id_]

                if not activeFitID or commander is None:
                    raise Exception()

                self.fleet[id_]['stText'].SetLabel(commander.ship.item.name + ": " + commander.name)
                self.fleet[id_]['chChar'].SetStringSelection(commander.character.name if commander.character is not None else "All 0")
                self.fleet[id_]['chChar'].Enable()
                self.fleet[id_]['chFit'].Hide()
                self.fleet[id_]['stText'].Show()
            except:
                # set defaults, disable char selection, and enable fit selection
                self.fleet[id_]['stText'].SetLabel("None")
                self.fleet[id_]['chChar'].SetStringSelection("All 0")
                self.fleet[id_]['chChar'].Disable()
                self.fleet[id_]['chFit'].SetSelection(0)
                self.fleet[id_]['chFit'].Show()
                self.fleet[id_]['stText'].Hide()

        if activeFitID:
            self.Enable()
        else:
            self.Disable()

        self.Layout()
        self.SendSizeEvent()

    def AddCommander(self, fitID, type=None):
        ''' Adds booster to a fit, then recalculates active fit '''
        if type is None:
            return

        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID:
            sFit = Fit.getInstance()

            boostee = sFit.getFit(activeFitID)
            booster = sFit.getFit(fitID)

            fleetSrv = Fleet.getInstance()

            if type == 0:
                fleetSrv.setLinearFleetCom(boostee, booster)
            elif type == 1:
                fleetSrv.setLinearWingCom(boostee, booster)
            elif type == 2:
                fleetSrv.setLinearSquadCom(boostee, booster)

            sFit.recalc(boostee)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=activeFitID))

    def RefreshBoosterFits(self, event=None):
        sFit = Fit.getInstance()
        sMkt = Market.getInstance()
        fitList = sFit.getBoosterFits()

        for id_ in self.fleet:
            choice = self.fleet[id_]['chFit']
            chCurrSelection = choice.GetSelection()
            chCurrData = -1
            if chCurrSelection != -1:
                chCurrData = choice.GetClientData(chCurrSelection)
                chCurrSelString = choice.GetString(chCurrSelection)
            choice.Clear()
            currSelFound = False
            choice.Append("None", -1)
            for fit in fitList:
                fit_id, name, type_ = fit
                ship = sMkt.getItem(type_)
                choice.Append(ship.name + ': ' + name, fit_id)
                if chCurrData == fit_id:
                    currSelFound = True

            if chCurrSelection == -1:
                choice.SetSelection(0)
            else:
                if currSelFound:
                    choice.SetStringSelection(chCurrSelString)
                else:
                    choice.SetSelection(0)

    def RefreshCharacterList(self, event=None):
        sChar = Character.getInstance()
        charList = sChar.getCharacterList()
        for id_ in self.fleet:
            choice = self.fleet[id_]['chChar']
            chCurrSelection = choice.GetSelection()
            chCurrData = -1
            if chCurrSelection != -1:
                chCurrData = choice.GetClientData(chCurrSelection)
                chCurrSelString = choice.GetString(chCurrSelection)
            choice.Clear()
            currSelFound = False
            for char in charList:
                choice.Append(char.name, char.ID)
                if chCurrData == char.ID:
                    currSelFound = True

            if chCurrSelection == -1:
                choice.SetSelection(1)
            else:
                if currSelFound:
                    choice.SetStringSelection(chCurrSelString)
                else:
                    choice.SetSelection(1)

    def handleDrag(self, type, fitID):
        ''' Handle dragging of fit to fleet interface '''
        # Those are drags coming from pyfa sources, NOT builtin wx drags
        self.draggedFitID = None
        if type == "fit":
            sFit = Fit.getInstance()
            fit = sFit.getFit(self.mainFrame.getActiveFit())

            if fit and not fit.isStructure:
                self.draggedFitID = fitID

                pos = wx.GetMousePosition()
                pos = self.ScreenToClient(pos)

                self.PopupMenu(self.FitDNDPopupMenu, pos)

    def OnPopupItemSelected(self, event):
        ''' Fired when booster popup item is selected '''
        # Get menu selection ID via self.options
        menuItem = event.EventObject.FindItemById(event.GetId())
        type_ = self.options.index(menuItem.GetText())

        if self.draggedFitID:
            sFit = Fit.getInstance()
            draggedFit = sFit.getFit(self.draggedFitID)

            self.AddCommander(draggedFit.ID, type_)
            self.mainFrame.additionsPane.select("Fleet")

    def OnFitChoiceSelected(self, event):
        ''' Fired when booster choice is selected '''
        sFit = Fit.getInstance()

        # set type via choice box used
        chFit = event.GetEventObject()
        fitID = chFit.GetClientData(chFit.GetSelection())

        type_ = -1
        for id_ in self.fleet:
            if chFit == self.fleet[id_]['chFit']:
                type_ = id_

        if type_ == -1 or fitID == -1:
            event.Skip()
            return

        fit = sFit.getFit(fitID)

        self.AddCommander(fit.ID, type_)
        self.mainFrame.additionsPane.select("Fleet")
