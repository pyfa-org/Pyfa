import wx
import copy
from gui import bitmapLoader
import gui.mainFrame
import service

from wx.lib.buttons import GenBitmapButton
from pickle import TRUE

FitRenamed, EVT_FIT_RENAMED = wx.lib.newevent.NewEvent()
FitSelected, EVT_FIT_SELECTED = wx.lib.newevent.NewEvent()
FitRemoved, EVT_FIT_REMOVED = wx.lib.newevent.NewEvent()

Stage1Selected, EVT_SB_STAGE1_SEL = wx.lib.newevent.NewEvent()
Stage2Selected, EVT_SB_STAGE2_SEL = wx.lib.newevent.NewEvent()
Stage3Selected, EVT_SB_STAGE3_SEL = wx.lib.newevent.NewEvent()
SearchSelected, EVT_SB_SEARCH_SEL = wx.lib.newevent.NewEvent()

class ShipBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent,style = 0 if 'wxGTK' in wx.PlatformInfo else wx.DOUBLE_BORDER)

        self._lastWidth = 0
        self._activeStage = 1
        self.browseHist = []
        self.lastStage = (0,0)

        self.stage2Cache = {}
        self.stage3Cache = {}

        self.categoryList=[]

        self._stage1Data = -1
        self._stage2Data = -1
        self._stage3Data = -1
        self._stage3ShipName = ""
        self.fitIDMustEditName = -1
        self.filterShipsWithNoFits = False

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.hpane = HeaderPane(self)
        mainSizer.Add(self.hpane, 0, wx.EXPAND)

        self.m_sl2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_sl2, 0, wx.EXPAND, 0 )

        self.lpane = ListPane(self)
        mainSizer.Add(self.lpane, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        self.Layout()
        self.Show()

        self.Bind(wx.EVT_SIZE, self.SizeRefreshList)
        self.Bind(EVT_SB_STAGE2_SEL, self.stage2)
        self.Bind(EVT_SB_STAGE1_SEL, self.stage1)
        self.Bind(EVT_SB_STAGE3_SEL, self.stage3)
        self.Bind(EVT_SB_SEARCH_SEL, self.searchStage)

        self.stage1(None)

    def SizeRefreshList(self, event):
        ewidth, eheight = event.GetSize()
##            if ewidth != self._lastWidth:
##                self._lastWidth = ewidth
        self.Layout()
        self.lpane.Layout()
        self.lpane.RefreshList(True)
        event.Skip()

    def __del__(self):
        pass
    def GetActiveStage(self):
        return self._activeStage
    def GetLastStage(self):
        return self._lastStage

    def GetStageData(self, stage):
        if stage == 1:
            return self._stage1Data
        if stage == 2:
            return self._stage2Data
        if stage == 3:
            return self._stage3Data
        return -1
    def GetStage3ShipName(self):
        return self._stage3ShipName

    def nameKey(self, info):
        return info[1]

    def stage1(self, event):

        self._activeStage = 1
        self.lastdata = 0
        self.hpane.ToggleNewFitSB(False)
        self.hpane.ToggleFitViewModeSB(False)
        sMarket = service.Market.getInstance()
        self.lpane.RemoveAllChildren()
        if len(self.categoryList) == 0:
            self.categoryList = sMarket.getShipRoot()
            self.categoryList.sort(key=self.nameKey)
        for ID, name in self.categoryList:
            self.lpane.AddWidget(CategoryItem(self.lpane, ID, (name, 0)))

        self.lpane.RefreshList()
        self.Show()

    RACE_ORDER = ["amarr", "caldari", "gallente", "minmatar", "ore", "serpentis", "angel", "blood", "sansha", "guristas", None]
    def raceNameKey(self, shipInfo):
        return self.RACE_ORDER.index(shipInfo[2]), shipInfo[1]


    def stage2(self, event):
        back = event.back
        if not back:
            self.browseHist.append( (1,0) )

        self._activeStage = 2
        categoryID = event.categoryID
        self.lastdata = categoryID

        self._stage2Data = categoryID
        self.hpane.ToggleNewFitSB(False)
        self.hpane.ToggleFitViewModeSB(True)
        sMarket = service.Market.getInstance()
        sFit = service.Fit.getInstance()
        self.lpane.RemoveAllChildren()
        content = self.stage2Cache.get(categoryID,None)
        if not content:
            content = []
            shipList = sMarket.getShipList(categoryID)
            shipList.sort(key=self.raceNameKey)
            for ID, name, race in shipList:
                fits = len(sFit.getFitsWithShip(ID))
                if self.filterShipsWithNoFits:
                    if fits>0:
                        self.lpane.AddWidget(ShipItem(self.lpane, ID, (name, fits), race))
                else:
                    self.lpane.AddWidget(ShipItem(self.lpane, ID, (name, fits), race))

                content.append((ID,name,fits,race))
            self.stage2Cache[categoryID]= content
        else:
            count = 0
            for ID,name,fits,race in content:
                dbfits = len(sFit.getFitsWithShip(ID))
                if dbfits != fits:
                    fits = dbfits
                    self.stage2Cache[categoryID][count]= (ID,name,fits,race)
                count += 1
                if self.filterShipsWithNoFits:
                    if fits >0:
                        self.lpane.AddWidget(ShipItem(self.lpane,ID, (name,fits),race))
                else:
                    self.lpane.AddWidget(ShipItem(self.lpane,ID, (name,fits),race))
        self.lpane.RefreshList()
        self.Show()

    def stage3(self, event):
        if event.back == 0:
            self.browseHist.append( (2,self._stage2Data) )
        elif event.back == -1:
            if len(self.hpane.recentSearches)>0:
                self.browseHist.append((4, self.hpane.lastSearch))

        shipID = event.shipID
        self.lastdata = shipID

        self._activeStage = 3

        sFit = service.Fit.getInstance()
        sMarket = service.Market.getInstance()
        self.lpane.RemoveAllChildren()
        fitList = sFit.getFitsWithShip(shipID)

        if len(fitList) == 0:
            stage,data = self.browseHist.pop()
            self.hpane.gotoStage(stage,data)
            return
        self.hpane.ToggleFitViewModeSB(False)
        self.hpane.ToggleNewFitSB(True)
        fitList.sort(key=self.nameKey)
        shipName = sMarket.getItem(shipID).name

        self._stage3ShipName = shipName
        self._stage3Data = shipID

        for ID, name in fitList:
            self.lpane.AddWidget(FitItem(self.lpane, ID, (shipName, name),shipID))

        self.lpane.RefreshList()
        self.Show()

    def searchStage(self, event):
        if not event.back:
            if self._activeStage !=4:
                if len(self.browseHist) >0:
                    self.browseHist.append( (self._activeStage, self.lastdata) )
                else:
                    self.browseHist.append((1,0))
            self._activeStage = 4

        sMarket = service.Market.getInstance()
        sFit = service.Fit.getInstance()
        query = event.text

        self.lpane.RemoveAllChildren()
        if query:
            shipList = sMarket.searchShips(query)
            fitList = sFit.searchFits(query)

            for ID, name, race in shipList:
                self.lpane.AddWidget(ShipItem(self.lpane, ID, (name, len(sFit.getFitsWithShip(ID))), race))

            for ID, name, shipID, shipName in fitList:
                self.lpane.AddWidget(FitItem(self.lpane, ID, (shipName, name), shipID))

            self.lpane.RefreshList()
        self.Show()

class PFGenBitmapButton(GenBitmapButton):
    def __init__(self, parent, id, bitmap, pos, size, style):
        GenBitmapButton.__init__(self, parent, id, bitmap, pos, size, style)
        self.bgcolor = wx.Brush(wx.WHITE)

    def SetBackgroundColour(self, color):
        self.bgcolor = wx.Brush(color)

    def GetBackgroundBrush(self, dc):
        return self.bgcolor

class HeaderPane (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 32), style=wx.TAB_TRAVERSAL)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.rewBmp = bitmapLoader.getBitmap("frewind_small","icons")
        self.forwBmp = bitmapLoader.getBitmap("fforward_small","icons")
        self.searchBmp = bitmapLoader.getBitmap("fsearch_small","icons")
        self.newBmp = bitmapLoader.getBitmap("fit_add_small","icons")
        self.resetBmp = bitmapLoader.getBitmap("freset_small","icons")
        self.switchBmp = bitmapLoader.getBitmap("fit_switch_view_mode_small","icons")

        img = self.newBmp.ConvertToImage()
        img.RotateHue(0.625)
        self.newBmp = wx.BitmapFromImage(img)

        img = self.switchBmp.ConvertToImage()
        img.RotateHue(0.625)
        self.switchSelBmp = wx.BitmapFromImage(img)


        self.shipBrowser = self.Parent

        self.toggleSearch = -1
        self.recentSearches = []
        self.lastSearch = ""
        self.menu = None
        self.inPopup = False
        self.inSearch = False

        bmpSize = (16,16)
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.sbReset = PFGenBitmapButton( self, wx.ID_ANY, self.resetBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
        mainSizer.Add(self.sbReset, 0, wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL , 5)
        self.sbReset.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
        self.sbReset.SetBitmapSelected(self.resetBmp)

        self.sbRewind = PFGenBitmapButton( self, wx.ID_ANY, self.rewBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
        mainSizer.Add(self.sbRewind, 0, wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL , 5)
        self.sbRewind.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
        self.sbRewind.SetBitmapSelected(self.rewBmp)

#        self.sbForward = PFGenBitmapButton( self, wx.ID_ANY, self.forwBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
#        mainSizer.Add(self.sbForward, 0, wx.LEFT | wx.TOP | wx.BOTTOM  | wx.ALIGN_CENTER_VERTICAL , 5)
#        self.sbForward.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        self.sl1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        mainSizer.Add( self.sl1, 0, wx.EXPAND |wx.LEFT, 5 )

        self.sbSearch = PFGenBitmapButton( self, wx.ID_ANY, self.searchBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
        mainSizer.Add(self.sbSearch, 0, wx.LEFT | wx.TOP | wx.BOTTOM  | wx.ALIGN_CENTER_VERTICAL , 5)
        self.sbSearch.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        self.sl2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        mainSizer.Add( self.sl2, 0, wx.EXPAND |wx.LEFT, 5 )

        self.sbNewFit = PFGenBitmapButton( self, wx.ID_ANY, self.newBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
        mainSizer.Add(self.sbNewFit, 0, wx.LEFT | wx.TOP | wx.BOTTOM  | wx.ALIGN_CENTER_VERTICAL , 5)
        self.sbNewFit.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        self.sbSwitchFitView = PFGenBitmapButton( self, wx.ID_ANY, self.switchBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
        mainSizer.Add(self.sbSwitchFitView, 0, wx.LEFT | wx.TOP | wx.BOTTOM  | wx.ALIGN_CENTER_VERTICAL , 5)
        self.sbSwitchFitView.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )


        self.stStatus = wx.StaticText( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stStatus.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
        self.stStatus.Wrap( -1 )
        mainSizer.Add(self.stStatus, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL , 5)

        self.spanel = wx.Panel(self)
        self.spanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        spsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.spanel.SetSizer(spsizer)

        self.search = wx.TextCtrl(self.spanel, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER )


        spsizer.Add(self.search,1, wx.ALIGN_CENTER_VERTICAL)
        mainSizer.Add(self.spanel,1,wx.EXPAND)

        self.SetSizer(mainSizer)

#        self.sbForward.Bind(wx.EVT_BUTTON,self.OnForward)
#        self.sbForward.Bind( wx.EVT_ENTER_WINDOW, self.OnEnterWForward )
#        self.sbForward.Bind( wx.EVT_LEAVE_WINDOW, self.OnLeaveWForward )

        self.sbReset.Bind(wx.EVT_BUTTON,self.OnReset)
        self.sbReset.Bind( wx.EVT_ENTER_WINDOW, self.OnEnterWReset )
        self.sbReset.Bind( wx.EVT_LEAVE_WINDOW, self.OnLeaveWReset )

        self.sbRewind.Bind(wx.EVT_BUTTON,self.OnBack)
        self.sbRewind.Bind( wx.EVT_ENTER_WINDOW, self.OnEnterWRewind )
        self.sbRewind.Bind( wx.EVT_LEAVE_WINDOW, self.OnLeaveWRewind )



        self.sbSearch.Bind(wx.EVT_BUTTON,self.OnSearch)
        self.sbSearch.Bind( wx.EVT_ENTER_WINDOW, self.OnEnterWSearch )
        self.sbSearch.Bind( wx.EVT_LEAVE_WINDOW, self.OnLeaveWSearch )

        self.sbNewFit.Bind(wx.EVT_BUTTON,self.OnNewFitting)
        self.sbNewFit.Bind( wx.EVT_ENTER_WINDOW, self.OnEnterWNewFit )
        self.sbNewFit.Bind( wx.EVT_LEAVE_WINDOW, self.OnLeaveWNewFit )

        self.sbSwitchFitView.Bind(wx.EVT_BUTTON,self.OnSwitch)
        self.sbSwitchFitView.Bind( wx.EVT_ENTER_WINDOW, self.OnEnterWSwitch )
        self.sbSwitchFitView.Bind( wx.EVT_LEAVE_WINDOW, self.OnLeaveWSwitch )

        self.search.Bind(wx.EVT_TEXT_ENTER, self.doSearch)
        self.search.Bind(wx.EVT_KILL_FOCUS, self.editLostFocus)
        self.search.Bind(wx.EVT_KEY_DOWN, self.editCheckEsc)
        self.search.Bind(wx.EVT_CONTEXT_MENU,self.OnMenu)
        self.search.Bind(wx.EVT_TEXT, self.scheduleSearch)

        self.sbSearch.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.sbSearch.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

        self.Layout()
        self.spanel.Hide()
        self.search.Hide()

    def OnLeftDown(self, event):
        self.inPopup = True
        event.Skip()

    def OnLeftUp(self, event):
        self.inPopup = False
        event.Skip()

    def scheduleSearch(self, event):
        if self.inPopup:
            return
        search = self.search.GetValue()
        if len(search) < 3 and len(search) > 0:
            if self.inSearch == True:
                self.inSearch = False
                if len(self.shipBrowser.browseHist) > 0:
                    stage,data = self.shipBrowser.browseHist.pop()
                    self.gotoStage(stage,data)
        else:
            if search:
                wx.PostEvent(self.shipBrowser,SearchSelected(text=search, back = False))
                self.inSearch = True
            else:
                self.inSearch = False

        event.Skip()

    def OnMenu(self, event):
        self.inPopup = True
        self.menu = self.MakeMenu()
        self.PopupMenu(self.menu)
        self.inPopup = False
        pass

    def OnMenuSelected(self, event):
        item = self.menu.FindItemById(event.GetId())
        text = item.GetText()

        if len(text)>2 :
            wx.PostEvent(self.shipBrowser,SearchSelected(text=text, back = False))
        self.editLostFocus()

    def MakeMenu(self):
        menu = wx.Menu()
        normalCMItems = ["Undo","_sep_", "Cut", "Copy","Paste","Delte","_sep_", "Select All"]
        item = menu.Append(-1, "Recent")
        item.Enable(False)

        if len(self.recentSearches) > 0:
            menu.AppendSeparator()
        for txt in self.recentSearches:
            if txt:
                item = menu.Append(-1, txt)
                menu.Bind(wx.EVT_MENU, self.OnMenuSelected, item)

        if 'wxMSW' in wx.PlatformInfo:
            menu.Break()
        else:
            menu.AppendSeparator()

        for txt in normalCMItems:
            if txt =="_sep_":
                menu.AppendSeparator()
            else:
                item = menu.Append(-1, txt)
                item.Enable(False)
                menu.Bind(wx.EVT_MENU, self.OnMenuSelected, item)
        return menu


    def editLostFocus(self, event = None):
        if self.inPopup:
            return
        if self.toggleSearch == 1:
            self.search.Show(False)
            self.spanel.Show(False)
            self.toggleSearch = -1

#        if self.menu:
#            self.menu.Destroy()

        stxt = self.search.GetValue()
        if stxt not in self.recentSearches:
            if stxt:
                self.recentSearches.append(stxt)
                self.lastSearch = stxt
        if len(self.recentSearches) >5:
            self.recentSearches.remove(self.recentSearches[0])
        self.search.SetValue("")

    def editCheckEsc(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.search.Show(False)
            self.spanel.Show(False)
            self.toggleSearch = -1
        else:
            event.Skip()
    def doSearch(self, event):
        stxt = self.search.GetValue()
        if len(stxt) > 2:
            self.editLostFocus()

    def ToggleNewFitSB(self, toggle):
        self.sbNewFit.Show(toggle)
        self.sl2.Show(toggle)
        self.Layout()

    def ToggleFitViewModeSB(self, toggle):
        self.sbSwitchFitView.Show(toggle)
        self.sl2.Show(toggle)
        self.Layout()

    def OnReset(self,event):
        if self.shipBrowser.browseHist:
            self.shipBrowser.browseHist = []
            self.gotoStage(1,0)
            self.stStatus.SetLabel("")
            self.Layout()
        event.Skip()

    def OnEnterWReset(self, event):
        if self.shipBrowser.browseHist:
            self.stStatus.Enable()
        else:
            self.stStatus.Disable()
        if self.toggleSearch != 1:
            self.stStatus.SetLabel("Reset history")
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWReset(self, event):
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()


    def OnEnterWForward(self, event):
        if self.toggleSearch != 1:
            self.stStatus.SetLabel("Forward")
        stage = self.Parent.GetActiveStage()

        if stage < 3:
            if self.Parent.GetStageData(stage+1) != -1:
                self.stStatus.Enable()
            else:
                self.stStatus.Disable()
        else:
            self.stStatus.Disable()

        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWForward(self, event):
        self.stStatus.Enable()
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()

    def OnEnterWRewind(self, event):
        if self.toggleSearch != 1:
            self.stStatus.SetLabel("Back")

        stage = self.Parent.GetActiveStage()

        if stage > 1:
            self.stStatus.Enable()
        else:
            self.stStatus.Disable()


        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWRewind(self, event):
        self.stStatus.Enable()
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()

    def OnEnterWSearch(self, event):
        if self.toggleSearch != 1:
            self.stStatus.SetLabel("Search fittings")
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWSearch(self, event):
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()

    def OnEnterWSwitch(self, event):
        if self.toggleSearch != 1:
            self.stStatus.SetLabel("Show empty ship groups" if self.shipBrowser.filterShipsWithNoFits else "Hide empty ship groups")
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWSwitch(self, event):
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()

    def OnEnterWNewFit(self, event):
        if self.toggleSearch != 1:
            self.stStatus.SetLabel("New fitting")
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def OnLeaveWNewFit(self, event):
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()

    def OnSearch(self, event):
        self.stStatus.SetLabel("")
        if self.toggleSearch == 2:
            self.toggleSearch = -1
            return
        if not self.search.IsShown():
            self.spanel.Show(True)
            self.search.Show(True)
            self.search.SetFocus()
            self.toggleSearch = 1
            self.Layout()
            self.spanel.Layout()

        else:
            self.search.Show(False)
            self.spanel.Show(False)
            self.toggleSearch = -1
            self.Layout()
        event.Skip()

    def OnSwitch(self, event):
        if self.shipBrowser.filterShipsWithNoFits:
            self.shipBrowser.filterShipsWithNoFits = False
            self.sbSwitchFitView.SetBitmapLabel(self.switchBmp,False)
        else:
            self.shipBrowser.filterShipsWithNoFits = True
            self.sbSwitchFitView.SetBitmapLabel(self.switchSelBmp,False)
        self.stStatus.SetLabel("Show empty ship groups" if self.shipBrowser.filterShipsWithNoFits else "Hide empty ship groups")
        stage = self.shipBrowser.GetActiveStage()
        if stage == 2:
            categoryID = self.shipBrowser.GetStageData(stage)
            wx.PostEvent(self.shipBrowser,Stage2Selected(categoryID=categoryID, back = True))
        event.Skip()

    def OnNewFitting(self, event):
        self.editLostFocus()
        stage = self.Parent.GetActiveStage()
        if stage == 3:
            shipID = self.Parent.GetStageData(stage)
            shipName = self.Parent.GetStage3ShipName()
            sFit = service.Fit.getInstance()
            fitID = sFit.newFit(shipID, "%s fit" %shipName)
            self.shipBrowser.fitIDMustEditName = fitID
            wx.PostEvent(self.Parent,Stage3Selected(shipID=shipID, back = True))
            wx.PostEvent(self.mainFrame, FitSelected(fitID=fitID))
        event.Skip()

    def OnForward(self,event):
        self.editLostFocus()
        stage = self.Parent.GetActiveStage()
        stage +=1
        if stage >3:
            stage = 3
            return
        self.gotoStage(stage)

        self.stStatus.Enable()
        self.stStatus.SetLabel("")

        event.Skip()

    def OnBack(self,event):

        self.stStatus.Enable()
        self.stStatus.SetLabel("")
        if len(self.shipBrowser.browseHist) > 0:
            stage,data = self.shipBrowser.browseHist.pop()
            self.gotoStage(stage,data)
        event.Skip()

    def gotoStage(self,stage, data = None):
        if stage == 1:
            wx.PostEvent(self.Parent,Stage1Selected())
        elif stage == 2:
            wx.PostEvent(self.Parent,Stage2Selected(categoryID=data, back = True))
        elif stage == 3:
            wx.PostEvent(self.Parent,Stage3Selected(shipID=data, back = 1))
        elif stage == 4:
            self.shipBrowser._activeStage = 4
            self.stStatus.SetLabel("Search: %s" % data.capitalize())
            self.Layout()
            wx.PostEvent(self.Parent,SearchSelected(text=data, back = True))
        else:
            wx.PostEvent(self.Parent,Stage1Selected())

class ListPane (wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1, 1), style=wx.TAB_TRAVERSAL)
        self._wList = []
        self._wCount = 0
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))


        self.SetVirtualSize((1, 1))
        self.SetScrollRate(0, 1)
        self.Bind(wx.EVT_SCROLLWIN_LINEUP, self.MScrollUp)
        self.Bind(wx.EVT_SCROLLWIN_LINEDOWN, self.MScrollDown)

    def MScrollUp(self, event):

        posy = self.GetScrollPos(wx.VERTICAL)
        posy -= 12
        self.Scroll(0, posy)
#        self.RefreshList()
        event.Skip()

    def MScrollDown(self, event):

        posy = self.GetScrollPos(wx.VERTICAL)
        posy += 12
        self.Scroll(0, posy)
#        self.RefreshList()
        event.Skip()


    def AddWidget(self, widget):
        widget.Reparent(self)
        self._wList.append(widget)
        self._wCount += 1

    def RefreshList(self, doRefresh = False):
        ypos = 0
        maxy = 0
        for i in xrange( len(self._wList) ):
            iwidth, iheight = self._wList[i].GetSize()
            xa, ya = self.CalcScrolledPosition((0, maxy))
            self._wList[i].SetPosition((xa, ya))
            maxy += iheight
        self.SetVirtualSize((1, maxy))
        cwidth, cheight = self.GetVirtualSize()

        clientW,clientH = self.GetSize()
        for i in xrange( len(self._wList) ):
            iwidth, iheight = self._wList[i].GetSize()
            itemX,itemY = self._wList[i].GetPosition()
            self._wList[i].SetSize((cwidth, iheight))
            if doRefresh == True:
                if itemY >=-iheight and itemY< clientH:
                    self._wList[i].Refresh()

    def RemoveWidget(self, child):
        child.Destroy()
        self._wList.remove(child)


    def RemoveAllChildren(self):
        for widget in self._wList:
            widget.Destroy()

        self._wList = []

class CategoryItem(wx.Window):
    def __init__(self, parent, categoryID, shipFittingInfo,
                 id=wx.ID_ANY, range=100, pos=wx.DefaultPosition,
                 size=(0,16), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

        if categoryID:
            self.shipBmp = bitmapLoader.getBitmap("ship_small","icons")
        else:
            self.shipBmp = wx.EmptyBitmap(16,16)

        self.categoryID = categoryID
        self.shipFittingInfo = shipFittingInfo
        self.shipName, dummy = shipFittingInfo
        self.width,self.height = size

        self.highlighted = 0
        self.editWasShown = 0

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_UP, self.checkPosition)
        self.Bind(wx.EVT_ENTER_WINDOW, self.enterW)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.leaveW)

        self.shipBrowser = self.Parent.Parent

    def checkPosition(self, event):

        pos = event.GetPosition()
        x,y = pos
        categoryID = self.categoryID
        wx.PostEvent(self.shipBrowser,Stage2Selected(categoryID=categoryID, back=False))

    def enterW(self,event):
        self.highlighted = 1
        self.Refresh()
        event.Skip()

    def leaveW(self,event):
        self.highlighted = 0
        self.Refresh()
        event.Skip()


    def OnEraseBackground(self, event):
        pass

    def OnPaint(self,event):
        rect = self.GetRect()

        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        r = copy.copy(rect)
        r.top = 0
        r.left = 0
        r.height = r.height / 2
        if self.highlighted:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)))
            mdc.Clear()
            mdc.SetTextForeground(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

            sr = 221
            sg = 221
            sb = 221

            startColor = (sr,sg,sb)

            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.SOUTH)
            r.top = r.height
            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.NORTH)
            mdc.SetTextForeground(wx.BLACK)

        else:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
            mdc.SetTextForeground(wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ))
            mdc.Clear()

        mdc.DrawBitmap(self.shipBmp,5+(rect.height-self.shipBmp.GetHeight())/2,(rect.height-self.shipBmp.GetWidth())/2,0)
        mdc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False))



        shipName, fittings = self.shipFittingInfo



        xpos = self.shipBmp.GetWidth() + 10

        xtext, ytext = mdc.GetTextExtent(shipName)
        ypos = (rect.height - ytext) / 2
        mdc.DrawText(shipName, xpos, ypos)
        xpos+=xtext+5

        mdc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False))

        if fittings <1:
            fformat = "No fits"
        else:
            if fittings == 1:
                fformat = "%d fit"
            else:
                fformat = "%d fits"

        if fittings>0:
            xtext, ytext = mdc.GetTextExtent(fformat % fittings)
            ypos = (rect.height - ytext)/2
        else:
            xtext, ytext = mdc.GetTextExtent(fformat)
            ypos = (rect.height - ytext)/2

        #seems that a scrolled window without scrollbars shown always HasScrollbar ><

        addX = 5

        fPosX = rect.width - addX - xtext
        fPosY = (rect.height -ytext)/2
#        if fittings > 0:
#            mdc.DrawText(fformat % fittings, fPosX, fPosY)
#        else:
#            mdc.DrawText(fformat, fPosX, fPosY)

        event.Skip()

class ShipItem(wx.Window):
    def __init__(self, parent, shipID=None, shipFittingInfo=("Test", 2), itemData=None,
                 id=wx.ID_ANY, range=100, pos=wx.DefaultPosition,
                 size=(0, 38), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self._itemData = itemData
        self.ignoreFurtherFitNameEdit = False

        self.shipRace = itemData

        self.shipID = shipID
        self.shipBmp = None
        if shipID:
            self.shipBmp = bitmapLoader.getBitmap(str(shipID),"ships")
        if not self.shipBmp:
            self.shipBmp = wx.EmptyBitmap(32, 32)
        self.shipFittingInfo = shipFittingInfo
        self.shipName, self.shipFits = shipFittingInfo

        self.newBmp = bitmapLoader.getBitmap("fit_add_small", "icons")
        self.acceptBmp = bitmapLoader.getBitmap("faccept_small", "icons")
        img = self.acceptBmp.ConvertToImage()
        img.RotateHue(0.625)
        self.acceptBmp = wx.BitmapFromImage(img)
        self.newToggleBmp = self.newBmp
        self.shipEffBk = bitmapLoader.getBitmap("fshipbk_big","icons")
        self.raceBmp = bitmapLoader.getBitmap("race_%s_small" % self.shipRace, "icons")
        self.raceMBmp = bitmapLoader.getBitmap("fit_delete_small","icons")

        if not self.raceBmp:
            self.raceBmp = self.raceMBmp

        self.shipBrowser = self.Parent.Parent

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.editPosX = 0
        self.editPosY = 0
        self.highlighted = 0
        self.editWasShown = 0
        self.btnsStatus = ""
        self.Refresh()
        self.tcFitName = wx.TextCtrl(self, wx.ID_ANY, "%s fit" % self.shipName, wx.DefaultPosition, (120,-1), wx.TE_PROCESS_ENTER)
        self.tcFitName.Show(False)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.Bind(wx.EVT_LEFT_UP, self.checkPosition)
        self.Bind(wx.EVT_MOTION, self.cursorCheck)

        self.Bind(wx.EVT_ENTER_WINDOW, self.enterW)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.leaveW)

        self.tcFitName.Bind(wx.EVT_TEXT_ENTER, self.createNewFit)
        self.tcFitName.Bind(wx.EVT_KILL_FOCUS, self.editLostFocus)
        self.tcFitName.Bind(wx.EVT_KEY_DOWN, self.editCheckEsc)

    def SetData(self, data):
        self._itemData = data

    def GetData(self):
        return self._itemData

    def editLostFocus(self, event):
        self.tcFitName.Show(False)
        if self.highlighted == 1:
            self.editWasShown = 1
        self.newToggleBmp = self.newBmp
        self.ignoreFurtherFitNameEdit = True
        self.Refresh()

    def editCheckEsc(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.tcFitName.Show(False)
            self.editWasShown = 0
        else:
            event.Skip()

    def cursorCheck(self, event):
        pos = event.GetPosition()
        if self.NHitTest((self.editPosX, self.editPosY), pos, (16, 16)):
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            if self.btnsStatus != "New fit":
                self.btnsStatus = "New fit"
                self.Refresh()
        else:
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            if self.btnsStatus != "":
                self.btnsStatus = ""
                self.Refresh()

    def checkPosition(self, event):

        pos = event.GetPosition()
        x, y = pos
        if self.NHitTest((self.editPosX, self.editPosY), pos, (16, 16)):
            if self.editWasShown == 1:
                self.ignoreFurtherFitNameEdit = True
                self.createNewFit()
                return
            else:
                fnEditSize = self.tcFitName.GetSize()
                wSize = self.GetSize()
                fnEditPosX = self.editPosX - fnEditSize.width - 5
                fnEditPosY = (wSize.height - fnEditSize.height) / 2
                self.tcFitName.SetPosition((fnEditPosX, fnEditPosY))
                self.tcFitName.Show(True)
                self.tcFitName.SetFocus()
                self.tcFitName.SelectAll()
                self.newToggleBmp = self.acceptBmp
                self.Refresh()
                return

        if (not self.NHitTest((self.editPosX, self.editPosY), pos, (16, 16))):
            if self.shipFits > 0:
                if self.editWasShown == 1:
                    self.editWasShown = 0
                else:
                    wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID, back = -1 if self.shipBrowser.GetActiveStage() == 4 else 0))
            else:
                if self.editWasShown == 0:
                    fnEditSize = self.tcFitName.GetSize()
                    wSize = self.GetSize()
                    fnEditPosX = self.editPosX - fnEditSize.width - 5
                    fnEditPosY = (wSize.height - fnEditSize.height) / 2
                    self.tcFitName.SetPosition((fnEditPosX, fnEditPosY))
                    self.tcFitName.Show(True)
                    self.tcFitName.SetFocus()
                    self.tcFitName.SelectAll()
                    self.newToggleBmp = self.acceptBmp
                    self.Refresh()
                else:
                    self.editWasShown = 0

        event.Skip()

    def createNewFit(self, event=None):
        sFit = service.Fit.getInstance()
        fitID = sFit.newFit(self.shipID, self.tcFitName.GetValue())
        self.tcFitName.Show(False)
        self.editWasShown = 0
        if not self.ignoreFurtherFitNameEdit:
            self.shipBrowser.fitIDMustEditName = fitID
        wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID, back=False))
        wx.PostEvent(self.mainFrame, FitSelected(fitID=fitID))

    def NHitTest(self, target, position, area):
        x, y = target
        px, py = position
        aX, aY = area
        if (px > x and px < x + aX) and (py > y and py < y + aY):
            return True
        return False
    def enterW(self, event):
        self.highlighted = 1
        self.Refresh()
        event.Skip()

    def leaveW(self, event):
        self.highlighted = 0
        self.Refresh()
        event.Skip()

    def OnEraseBackground(self, event):
        pass

    def OnPaint(self, event):
        rect = self.GetRect()

        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        r = copy.copy(rect)
        r.top = 0
        r.left = 0
        r.height = r.height / 2
        if self.highlighted:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)))
            mdc.Clear()
            mdc.SetTextForeground(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

            sr = 221
            sg = 221
            sb = 221

            startColor = (sr,sg,sb)

            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.SOUTH)
            r.top = r.height
            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.NORTH)
            mdc.SetTextForeground(wx.BLACK)

        else:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
            mdc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
            mdc.Clear()

        mdc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        mdc.DrawBitmap(self.shipEffBk, 5 + (rect.height - self.shipEffBk.GetWidth())/2, (rect.height - self.shipEffBk.GetHeight())/2, 0)
        mdc.DrawBitmap(self.shipBmp, 5 + (rect.height - 32) / 2, (rect.height - 32) / 2, 0)

#        tempdc = wx.MemoryDCFromDC(mdc)
#        tempdc.DrawBitmap(self.raceBmp,0,0,0)
#        mdc.Blit(5 + (rect.height - self.raceBmp.GetWidth()) / 2, (rect.height - self.raceBmp.GetHeight()) / 2,
#                 self.raceBmp.GetWidth(),self.raceBmp.GetHeight(), tempdc, 0, 0, rop = wx.XOR, useMask = True)
#        img = self.raceBmp.ConvertToImage()
#        img.AdjustChannels(1, 1, 1,0)
#        self.raceBmp = wx.BitmapFromImage(img)
#        mdc.DrawBitmap(self.raceBmp, 5 + (rect.height - self.raceBmp.GetWidth()) , (rect.height - self.raceBmp.GetHeight()) , 0)
#        mdc.DrawBitmap(self.raceBmp, 5 + (rect.height - self.shipBmp.GetWidth()) / 2, (rect.height - self.shipBmp.GetHeight()) / 2, 0)
#        tempdc.SelectObject(wx.NullBitmap)


        shipName, fittings = self.shipFittingInfo


        ypos = (rect.height - 32) / 2
        textStart = 48
        xtext, ytext = mdc.GetTextExtent(shipName)
        mdc.DrawBitmap(self.raceBmp,textStart, ypos + self.raceBmp.GetHeight()/2)
#        mdc.DrawText(shipName, textStart + self.raceBmp.GetWidth() + 4, ypos)
        textStart += self.raceBmp.GetWidth() + 4
        sposy = ypos

        ypos += ytext

        mdc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False))

        if fittings <1:
            fformat = "No fits"
        else:
            if fittings == 1:
                fformat = "%d fit"
            else:
                fformat = "%d fits"

        if fittings>0:
            xtext, ytext = mdc.GetTextExtent(fformat % fittings)
        else:
            xtext, ytext = mdc.GetTextExtent(fformat)

        mdc.DrawText(fformat %fittings if fittings >0 else fformat, textStart, ypos)

        self.editPosX = rect.width - self.newToggleBmp.GetWidth() -5
        self.editPosY = (rect.height - self.newToggleBmp.GetHeight()) / 2

        mdc.DrawBitmap(self.newToggleBmp, self.editPosX, self.editPosY, 0)
        mdc.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL, False))
        if self.btnsStatus != "":
            status = "%s" % self.btnsStatus
            xtext, ytext = mdc.GetTextExtent(status)
            ytext = (rect.height - ytext)/2
            mdc.DrawText(status, self.editPosX - xtext -5,ytext)
        else:
            xtext =0

        mdc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        fnwidths = mdc.GetPartialTextExtents(shipName)
        count = 0
        maxsize = self.editPosX -xtext - 15 - textStart
        for i in fnwidths:
            if i<= maxsize:
                count +=1
            else:
                break

        shipName = "%s%s" % (shipName[:count if count >5 else 5],"..." if len(shipName)>count else "")
        mdc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        mdc.DrawText(shipName, textStart, sposy)

        if self.tcFitName.IsShown():
            fnEditSize = self.tcFitName.GetSize()
            wSize = self.GetSize()
            fnEditPosX = self.editPosX - fnEditSize.width -5
            fnEditPosY = (wSize.height - fnEditSize.height)/2
            self.tcFitName.SetPosition((fnEditPosX,fnEditPosY))

        event.Skip()

class FitItem(wx.Window):
    def __init__(self, parent, fitID=None, shipFittingInfo=("Test", "cnc's avatar"), shipID = None, itemData=None,
                 id=wx.ID_ANY, range=100, pos=wx.DefaultPosition,
                 size=(0, 38), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self._itemData = itemData
        self.fitID = fitID
        self.shipID = shipID
        self.shipBrowser = self.Parent.Parent
        self.shipBmp = None
        if shipID:
            self.shipBmp = bitmapLoader.getBitmap(str(shipID),"ships")
        if not self.shipBmp:
            self.shipBmp = wx.EmptyBitmap(32, 32)

        self.shipFittingInfo = shipFittingInfo
        self.shipName, self.fitName= shipFittingInfo
        self.copyBmp = bitmapLoader.getBitmap("fit_add_small", "icons")
        self.renameBmp = bitmapLoader.getBitmap("fit_rename_small", "icons")
        self.deleteBmp = bitmapLoader.getBitmap("fit_delete_small","icons")
        self.shipEffBk = bitmapLoader.getBitmap("fshipbk_big","icons")

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.renamePosX = 0
        self.renamePosY = 0

        self.deletePosX = 0
        self.deletePosY = 0

        self.copyPosX = 0
        self.copyPosY = 0

        self.highlighted = 0
        self.editWasShown = 0

        self.btnsStatus = ""

        self.tcFitName = wx.TextCtrl(self, wx.ID_ANY, "%s" % self.fitName, wx.DefaultPosition, (150,-1), wx.TE_PROCESS_ENTER)
        if self.shipBrowser.fitIDMustEditName != self.fitID:
            self.tcFitName.Show(False)
        else:
            self.tcFitName.SetFocus()
            self.tcFitName.SelectAll()
            self.shipBrowser.fitIDMustEditName = -1

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.Bind(wx.EVT_LEFT_UP, self.checkPosition)
        self.Bind(wx.EVT_MOTION, self.cursorCheck)

        self.Bind(wx.EVT_ENTER_WINDOW, self.enterW)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.leaveW)

        self.tcFitName.Bind(wx.EVT_TEXT_ENTER, self.renameFit)
        self.tcFitName.Bind(wx.EVT_KILL_FOCUS, self.editLostFocus)
        self.tcFitName.Bind(wx.EVT_KEY_DOWN, self.editCheckEsc)

    def SetData(self, data):
        self._itemData = data

    def GetData(self):
        return self._itemData

    def editLostFocus(self, event):
        self.tcFitName.Show(False)
        if self.highlighted == 1:
            self.editWasShown = 1

    def editCheckEsc(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.tcFitName.Show(False)
            self.editWasShown = 0
        else:
            event.Skip()

    def cursorCheck(self, event):
        pos = event.GetPosition()
        if self.NHitTest((self.renamePosX, self.renamePosY), pos, (16, 16)):
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            if self.btnsStatus != "Rename":
                self.btnsStatus = "Rename"
                self.Refresh()
        elif self.NHitTest((self.deletePosX, self.deletePosY), pos, (16, 16)):
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            if self.btnsStatus != "Delete":
                self.btnsStatus = "Delete"
                self.Refresh()
        elif self.NHitTest((self.copyPosX, self.copyPosY), pos, (16, 16)):
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            if self.btnsStatus != "Copy":
                self.btnsStatus = "Copy"
                self.Refresh()
        else:
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            if self.btnsStatus != "":
                self.btnsStatus = ""
                self.Refresh()
    def checkPosition(self, event):

        pos = event.GetPosition()
        x, y = pos
        if self.NHitTest((self.renamePosX, self.renamePosY), pos, (16, 16)):
            if self.editWasShown == 1:
                self.renameFit()
                return
            else:
                self.Refresh()
                fnEditSize = self.tcFitName.GetSize()
                wSize = self.GetSize()
                fnrenamePosX = self.renamePosX - fnEditSize.width - 5
                fnrenamePosY = (wSize.height - fnEditSize.height) / 2
                self.tcFitName.SetPosition((fnrenamePosX, fnrenamePosY))
                self.tcFitName.Show(True)
                self.tcFitName.SetFocus()
                self.tcFitName.SelectAll()
                return
        if self.NHitTest((self.deletePosX,self.deletePosY), pos, (16,16)):
            if self.editWasShown != 1:
                self.deleteFit()
                return

        if self.NHitTest((self.copyPosX,self.copyPosY), pos, (16,16)):
            if self.editWasShown != 1:
                self.copyFit()
                return

        if self.editWasShown != 1:
            activeFitID = self.mainFrame.getActiveFit()
            if activeFitID != self.fitID:
                self.selectFit()
        else:
            self.editWasShown = 0
            self.Refresh()

        event.Skip()

    def renameFit(self, event=None):
        sFit = service.Fit.getInstance()
        self.tcFitName.Show(False)
        self.editWasShown = 0
        fitName = self.tcFitName.GetValue()
        if fitName:
            self.fitName = fitName
            sFit.renameFit(self.fitID, self.fitName)
            wx.PostEvent(self.mainFrame, FitRenamed(fitID=self.fitID))
            self.Refresh()
        else:
            self.tcFitName.SetValue(self.fitName)

    def copyFit(self, event=None):
        sFit = service.Fit.getInstance()
        fitID = sFit.copyFit(self.fitID)
        self.shipBrowser.fitIDMustEditName = fitID
        wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID, back=True))
        wx.PostEvent(self.mainFrame, FitSelected(fitID=fitID))

    def deleteFit(self, event=None):
        sFit = service.Fit.getInstance()
        sFit.deleteFit(self.fitID)
        if self.shipBrowser.GetActiveStage() == 4:
            wx.PostEvent(self.shipBrowser,SearchSelected(text=self.shipBrowser.hpane.lastSearch,back=True))
        else:
            wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID, back=True))

        wx.PostEvent(self.mainFrame, FitRemoved(fitID=self.fitID))

    def selectFit(self, event=None):
        wx.PostEvent(self.mainFrame, FitSelected(fitID=self.fitID))

    def NHitTest(self, target, position, area):
        x, y = target
        px, py = position
        aX, aY = area
        if (px > x and px < x + aX) and (py > y and py < y + aY):
            return True
        return False
    def enterW(self, event):
        self.highlighted = 1
        self.Refresh()
        event.Skip()

    def leaveW(self, event):
        self.highlighted = 0
        self.Refresh()
        event.Skip()

    def OnEraseBackground(self, event):
        pass

    def OnPaint(self, event):
        rect = self.GetRect()

        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        r = copy.copy(rect)
        r.top = 0
        r.left = 0
        r.height = r.height / 2
        if self.highlighted:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)))
            mdc.Clear()
            mdc.SetTextForeground(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

            sr = 221
            sg = 221
            sb = 221

            startColor = (sr,sg,sb)

            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.SOUTH)
            r.top = r.height
            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.NORTH)
            mdc.SetTextForeground(wx.BLACK)

        else:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
            mdc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
            mdc.Clear()
        mdc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))
#        mdc.DrawBitmap(self.effBmp,5+(rect.height-40)/2,(rect.height-40)/2,0)
        mdc.DrawBitmap(self.shipEffBk,5+(rect.height - self.shipEffBk.GetWidth())/2,(rect.height - self.shipEffBk.GetHeight())/2,0)
        mdc.DrawBitmap(self.shipBmp, 5 + (rect.height - 32) / 2, (rect.height - 32) / 2, 0)

        shipName = self.shipName
        fitName = self.fitName

        ypos = (rect.height - 32) / 2
        textStart = 48
        xtext, ytext = mdc.GetTextExtent(fitName)
        fposy = ypos
        ypos += ytext

        mdc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False))


        mdc.DrawText("%s" % shipName, textStart, ypos)
        mdc.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL, False))

        self.deletePosX = rect.width - self.deleteBmp.GetWidth() - 5
        self.renamePosX = self.deletePosX - self.renameBmp.GetWidth() - 5
        self.copyPosX = self.renamePosX - self.copyBmp.GetWidth() -5
        self.renamePosY = self.deletePosY = self.copyPosY = (rect.height - 16) / 2

        if self.btnsStatus != "":
            status = "%s" % self.btnsStatus
            xtext, ytext = mdc.GetTextExtent(status)
            ytext = (rect.height - ytext)/2
            mdc.DrawText(status, self.copyPosX - xtext -5,ytext)
        else:
            xtext = 0

        mdc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        fnwidths = mdc.GetPartialTextExtents(fitName)
        count = 0
        maxsize = self.copyPosX -xtext - 15 - textStart
        for i in fnwidths:
            if i <= maxsize:
                count +=1
            else:
                break

        fitName = "%s%s" % (fitName[:count if count >5 else 5],"..." if len(fitName)>count else "")

        mdc.DrawText(fitName, textStart, fposy)

        mdc.DrawBitmap(self.copyBmp, self.copyPosX, self.copyPosY, 0)
        mdc.DrawBitmap(self.renameBmp, self.renamePosX, self.renamePosY, 0)
        mdc.DrawBitmap(self.deleteBmp, self.deletePosX, self.deletePosY, 0)

        if self.tcFitName.IsShown():
            fnEditSize = self.tcFitName.GetSize()
            wSize = self.GetSize()
            fnEditPosX = self.copyPosX - fnEditSize.width -5
            fnEditPosY = (wSize.height - fnEditSize.height)/2
            self.tcFitName.SetPosition((fnEditPosX,fnEditPosY))
        event.Skip()
