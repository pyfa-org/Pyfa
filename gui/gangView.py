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
from wx.lib.scrolledpanel import ScrolledPanel

import service
import gui.mainFrame
import gui.shipBrowser
import gui.globalEvents as GE

from gui import characterEditor as CharEditor


class GangView ( ScrolledPanel ):

    def __init__( self, parent ):
        ScrolledPanel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 100,20 ), style = wx.TAB_TRAVERSAL | wx.HSCROLL | wx.VSCROLL )
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.draggedFitID = None

        self.FitDNDPopupMenu = wx.Menu()

        self.options = ["Fleet booster", "Wing booster", "Squad booster"]

        for option in self.options:
            item = self.FitDNDPopupMenu.Append(-1, option)
            # We bind it to the mainFrame because it may be called from either this class or from FitItem via shipBrowser
            self.mainFrame.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)

        contentFGSizer = wx.FlexGridSizer( 5, 3, 0, 0 )
        contentFGSizer.AddGrowableCol( 1 )
        contentFGSizer.SetFlexibleDirection( wx.BOTH )
        contentFGSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.oneonePlaceholder = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.oneonePlaceholder.Wrap( -1 )
        contentFGSizer.Add( self.oneonePlaceholder, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        fleetFitsSizer = wx.BoxSizer( wx.VERTICAL )
        wingFitsSizer = wx.BoxSizer( wx.VERTICAL )
        squadFitsSizer = wx.BoxSizer( wx.VERTICAL )

        self.stFits = wx.StaticText( self, wx.ID_ANY, u"Fits", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stFits.Wrap( -1 )
        self.stFits.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        contentFGSizer.Add( self.stFits, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.stCharacters = wx.StaticText( self, wx.ID_ANY, u"Characters", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stCharacters.Wrap( -1 )
        self.stCharacters.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        contentFGSizer.Add( self.stCharacters, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        contentFGSizer.Add( self.m_staticline2, 0, wx.EXPAND, 5 )

        self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        contentFGSizer.Add( self.m_staticline3, 0, wx.EXPAND, 5 )

        self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        contentFGSizer.Add( self.m_staticline4, 0, wx.EXPAND, 5 )

        self.stFleet = wx.StaticText( self, wx.ID_ANY, u"Fleet booster:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stFleet.Wrap( -1 )
        self.stFleet.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        contentFGSizer.Add( self.stFleet, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.stFleetFit = wx.StaticText( self, wx.ID_ANY, u"None", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stFleetFit.Wrap( -1 )
        self.stFleetFit.Hide()
        
        cFleetFitChoices = []
        self.cFleetFit = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cFleetFitChoices, 0 )

        fleetFitsSizer.Add( self.stFleetFit, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        fleetFitsSizer.Add( self.cFleetFit, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        contentFGSizer.Add( fleetFitsSizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        chFleetCharChoices = []
        self.chFleetChar = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chFleetCharChoices, 0 )
        self.chFleetChar.SetSelection( 0 )

        contentFGSizer.Add( self.chFleetChar, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )

        self.stWing = wx.StaticText( self, wx.ID_ANY, u"Wing booster:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stWing.Wrap( -1 )
        self.stWing.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        contentFGSizer.Add( self.stWing, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.stWingFit = wx.StaticText( self, wx.ID_ANY, u"None", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stWingFit.Wrap( -1 )
        self.stWingFit.Hide()
        
        cWingFitChoices = []
        self.cWingFit = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cWingFitChoices, 0 )
        
        wingFitsSizer.Add( self.stWingFit, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        wingFitsSizer.Add( self.cWingFit, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        contentFGSizer.Add( wingFitsSizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        chWingCharChoices = []
        self.chWingChar = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chWingCharChoices, 0 )
        self.chWingChar.SetSelection( 0 )

        contentFGSizer.Add( self.chWingChar, 0, wx.ALL| wx.ALIGN_CENTER_VERTICAL, 5 )

        self.stSquad = wx.StaticText( self, wx.ID_ANY, u"Squad booster:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stSquad.Wrap( -1 )
        self.stSquad.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        contentFGSizer.Add( self.stSquad, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.stSquadFit = wx.StaticText( self, wx.ID_ANY, u"None", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stSquadFit.Wrap( -1 )
        self.stSquadFit.Hide()
        
        cSquadFitChoices = []
        self.cSquadFit = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cSquadFitChoices, 0 )

        squadFitsSizer.Add( self.stSquadFit, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        squadFitsSizer.Add( self.cSquadFit, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        contentFGSizer.Add( squadFitsSizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        
        chSquadCharChoices = []
        self.chSquadChar = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chSquadCharChoices, 0 )
        self.chSquadChar.SetSelection( 0 )

        contentFGSizer.Add( self.chSquadChar, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )

        mainSizer.Add( contentFGSizer, 1, wx.EXPAND, 0 )

        self.stBoosters = []
        self.stBoosters.append(self.stFleetFit)
        self.stBoosters.append(self.stWingFit)
        self.stBoosters.append(self.stSquadFit)


        self.chCharacters = []
        self.chCharacters.append(self.chFleetChar)
        self.chCharacters.append(self.chWingChar)
        self.chCharacters.append(self.chSquadChar)

        self.chFits = []
        self.chFits.append(self.cFleetFit)
        self.chFits.append(self.cWingFit)
        self.chFits.append(self.cSquadFit)
        
        self.SetSizer( mainSizer )
        self.SetAutoLayout(True)
        self.SetupScrolling()
        self.Disable()

        self.mainFrame.Bind(GE.CHAR_LIST_UPDATED, self.RefreshCharacterList)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitSelected)
        self.mainFrame.Bind(gui.shipBrowser.EVT_FIT_RENAMED, self.fitRenamed)
        self.mainFrame.Bind(gui.shipBrowser.BOOSTER_LIST_UPDATED, self.RefreshBoosterFits)

        for stBooster in self.stBoosters:
            stBooster.Bind(wx.EVT_LEFT_DCLICK, self.RemoveBooster)
            stBooster.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
            stBooster.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
            stBooster.SetToolTip(wx.ToolTip("Double click to remove booster"))

        for chCharacter in self.chCharacters:
            chCharacter.Bind(wx.EVT_CHOICE, self.CharChanged)

        for chFits in self.chFits:
            chFits.Bind(wx.EVT_CHOICE, self.BoosterChanged)

        self.RefreshBoosterFits()
        self.RefreshCharacterList()

    def BoosterChanged(self, event):
        ''' Fired when booster choice is selected ''' 
        chFit = event.GetEventObject()
        
        type = -1
        if chFit == self.cFleetFit:
            type = 0
        if chFit == self.cWingFit:
            type = 1
        if chFit == self.cSquadFit:
            type = 2

        if type == -1:
            event.Skip()
            return
        
        id = chFit.GetClientData(chFit.GetSelection())

        sFit = service.Fit.getInstance()
        fit = sFit.getFit(id)
        
        chFit.Hide()
        text = self.stBoosters[type]
        text.Show()
        self.AddCommander(fit.ID, type)
        self.mainFrame.additionsPane.select("Fleet")


    def OnEnterWindow(self, event):
        obj = event.GetEventObject()
        obj.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWindow(self, event):
        obj = event.GetEventObject()
        obj.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
        event.Skip()


    def CharChanged(self, event):
        chBooster = event.GetEventObject()
        type = -1
        if chBooster == self.chFleetChar:
            type = 0
        if chBooster == self.chWingChar:
            type = 1
        if chBooster == self.chSquadChar:
            type = 2

        if type == -1:
            event.Skip()
            return

        cFit = service.Fit.getInstance()

        fleetSrv = service.Fleet.getInstance()

        activeFitID = self.mainFrame.getActiveFit()
        fit = cFit.getFit(activeFitID)

        cChar = service.Character.getInstance()
        charList = cChar.getCharacterList()

        if activeFitID:
            commanders = fleetSrv.loadLinearFleet(fit)
            if commanders is None:
                fleetCom, wingCom, squadCom = (None, None, None)
            else:
                fleetCom, wingCom, squadCom = commanders

            if type == 0:
                if fleetCom:
                    charID = chBooster.GetClientData(chBooster.GetSelection())
                    cFit.changeChar(fleetCom.ID, charID)
                else:
                    chBooster.SetSelection(0)

            if type == 1:
                if wingCom:
                    charID = chBooster.GetClientData(chBooster.GetSelection())
                    cFit.changeChar(wingCom.ID, charID)
                else:
                    chBooster.SetSelection(0)

            if type == 2:
                if squadCom:
                    charID = chBooster.GetClientData(chBooster.GetSelection())
                    cFit.changeChar(squadCom.ID, charID)
                else:
                    chBooster.SetSelection(0)

            cFit.recalc(fit, withBoosters=True)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=activeFitID))

        else:
            chBooster.SetSelection(0)

    def RemoveBooster(self, event):
        activeFitID = self.mainFrame.getActiveFit()
        if  not activeFitID:
            return

        location = event.GetEventObject()

        if location == self.stFleetFit:
            type = 0
        if location == self.stWingFit:
            type = 1
        if location == self.stSquadFit:
            type = 2

        sFit = service.Fit.getInstance()
        boostee = sFit.getFit(activeFitID)
        booster = None

        fleetSrv = service.Fleet.getInstance()

        if type == 0:
            fleetSrv.setLinearFleetCom(boostee, booster)
        elif type == 1:
            fleetSrv.setLinearWingCom(boostee, booster)
        elif type == 2:
            fleetSrv.setLinearSquadCom(boostee, booster)

        location.Hide()
        choice = self.chFits[type]
        choice.Show()
        
        sFit.recalc(boostee, withBoosters=True)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=activeFitID))

    def fitRenamed(self, event):
        fleetSrv = service.Fleet.getInstance()
        activeFitID = self.mainFrame.getActiveFit()

        if activeFitID:
            ev = event
            ev.fitID = activeFitID
            self.fitSelected(ev)

    def fitSelected(self, event):
        fleetSrv = service.Fleet.getInstance()

        activeFitID = self.mainFrame.getActiveFit()
        cFit = service.Fit.getInstance()
        fit = cFit.getFit(event.fitID or activeFitID)

        if activeFitID:
            commanders = fleetSrv.loadLinearFleet(fit)
            if commanders is None:
                fleetCom, wingCom, squadCom = (None, None, None)
            else:
                fleetCom, wingCom, squadCom = commanders

            if fleetCom:
                fleetComName = fleetCom.ship.item.name + ": " + fleetCom.name
                fleetComCharName = fleetCom.character.name if fleetCom.character is not None else "All 0"
            else:
                fleetComName = "None"
                fleetComCharName = "All 0"

            if wingCom:
                wingComName = wingCom.ship.item.name + ": " + wingCom.name
                wingComCharName = wingCom.character.name if wingCom.character is not None else "All 0"
            else:
                wingComName = "None"
                wingComCharName = "All 0"

            if squadCom:
                squadComName = squadCom.ship.item.name + ": " + squadCom.name
                squadComCharName = squadCom.character.name if squadCom.character is not None else "All 0"
            else:
                squadComName = "None"
                squadComCharName = "All 0"

            self.UpdateFleetFitsUI( fleetComName, wingComName, squadComName, fleetComCharName, wingComCharName, squadComCharName )
            self.Enable()

        else:
            fleetComName = "None"
            fleetComCharName = "All 0"
            wingComName = "None"
            wingComCharName = "All 0"
            squadComName = "None"
            squadComCharName = "All 0"

            self.UpdateFleetFitsUI( fleetComName, wingComName, squadComName, fleetComCharName, wingComCharName, squadComCharName )
            self.Disable()

    def UpdateFleetFitsUI(self, fleet, wing, squad, fleetChar, wingChar, squadChar):
        self.stFleetFit.SetLabel(fleet)
        self.stWingFit.SetLabel(wing)
        self.stSquadFit.SetLabel(squad)

        self.chFleetChar.SetStringSelection(fleetChar)
        self.chWingChar.SetStringSelection(wingChar)
        self.chSquadChar.SetStringSelection(squadChar)


        self.Layout()
        self.SendSizeEvent()



    def AddCommander(self, fitID, type = None):
        if type is None:
            return

        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID:
            sFit = service.Fit.getInstance()

            boostee = sFit.getFit(activeFitID)
            booster = sFit.getFit(fitID)

            fleetSrv = service.Fleet.getInstance()

            if type == 0:
                fleetSrv.setLinearFleetCom(boostee, booster)
            elif type == 1:
                fleetSrv.setLinearWingCom(boostee, booster)
            elif type == 2:
                fleetSrv.setLinearSquadCom(boostee, booster)
            sFit.recalc(boostee, withBoosters=True)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=activeFitID))

    def RefreshBoosterFits(self, event = None):
        sFit = service.Fit.getInstance()
        sMarket = service.Market.getInstance()
        fitList = sFit.getBoosterFits()
        
        for choice in self.chFits:
            chCurrSelection = choice.GetSelection()
            chCurrData = -1
            if chCurrSelection != -1:
                chCurrData = choice.GetClientData(chCurrSelection)
                chCurrSelString = choice.GetString(chCurrSelection)
            choice.Clear()
            currSelFound = False
            for fit in fitList:
                id,name,type = fit
                ship = sMarket.getItem(type)
                choice.Append(str(id)+': '+ship.name+' - '+name, id)
                if chCurrData == id:
                    currSelFound = True

            if chCurrSelection == -1:
                choice.SetSelection(1)
            else:
                if currSelFound:
                    choice.SetStringSelection(chCurrSelString)
                else:
                    choice.SetSelection(1)

    def RefreshCharacterList(self, event = None):
        cChar = service.Character.getInstance()
        charList = cChar.getCharacterList()

        for choice in self.chCharacters:
            chCurrSelection = choice.GetSelection()
            chCurrData = -1
            if chCurrSelection != -1:
                chCurrData = choice.GetClientData(chCurrSelection)
                chCurrSelString = choice.GetString(chCurrSelection)
            choice.Clear()
            currSelFound = False
            for char in charList:
                id,name,_ = char
                choice.Append(name, id)
                if chCurrData == id:
                    currSelFound = True

            if chCurrSelection == -1:
                choice.SetSelection(1)
            else:
                if currSelFound:
                    choice.SetStringSelection(chCurrSelString)
                else:
                    choice.SetSelection(1)

    def handleDrag(self, type, fitID):
        ''' Handle dragging of fit to fleet interface. This is also fired when right-clicking fit if there's an active one '''
        #Those are drags coming from pyfa sources, NOT builtin wx drags
        self.draggedFitID = None
        if type == "fit":
            activeFit = self.mainFrame.getActiveFit()
            if activeFit:
                self.draggedFitID = fitID

                pos = wx.GetMousePosition()
                pos = self.ScreenToClient(pos)

                self.PopupMenu(self.FitDNDPopupMenu, pos)

#                sFit.project(activeFit,draggedFit)
#                wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=activeFit))

    def OnPopupItemSelected(self, event):
        ''' Fired when booster popup item is selected ''' 
        item = self.FitDNDPopupMenu.FindItemById(event.GetId())
        text = item.GetText()
        booster = self.options.index(text)
        if self.draggedFitID:
            sFit = service.Fit.getInstance()
            draggedFit = sFit.getFit(self.draggedFitID)

#            self.stBoosters[booster].SetLabel(draggedFit.name)
#            self.Layout()

            self.AddCommander(draggedFit.ID, booster)
            self.mainFrame.additionsPane.select("Fleet")

