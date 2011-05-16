import wx
import copy
from gui import bitmapLoader
import gui.mainFrame
import gui.globalEvents as GE
import time
from gui.PFListPane import PFListPane
import service

from wx.lib.buttons import GenBitmapButton

import gui.utils.colorUtils as colorUtils
import gui.utils.drawUtils as drawUtils
import gui.utils.animUtils as animUtils
import gui.utils.animEffects as animEffects

import gui.sfBrowserItem as SFItem

FitRenamed, EVT_FIT_RENAMED = wx.lib.newevent.NewEvent()
FitSelected, EVT_FIT_SELECTED = wx.lib.newevent.NewEvent()
FitRemoved, EVT_FIT_REMOVED = wx.lib.newevent.NewEvent()

Stage1Selected, EVT_SB_STAGE1_SEL = wx.lib.newevent.NewEvent()
Stage2Selected, EVT_SB_STAGE2_SEL = wx.lib.newevent.NewEvent()
Stage3Selected, EVT_SB_STAGE3_SEL = wx.lib.newevent.NewEvent()
SearchSelected, EVT_SB_SEARCH_SEL = wx.lib.newevent.NewEvent()

class PFWidgetsContainer(PFListPane):
    def __init__(self,parent):
        PFListPane.__init__(self,parent)

        self.anim = animUtils.LoadAnimation(self,label = "", size=(100,12))
        self.anim.Stop()
        self.anim.Show(False)

    def ShowLoading(self, mode = True):
        if mode:
            aweight,aheight = self.anim.GetSize()
            cweight,cheight = self.GetSize()
            ax = (cweight - aweight)/2
            ay = (cheight - aheight)/2
            self.anim.SetPosition((ax,ay))
            self.anim.Show()
            self.anim.Play()
        else:
            self.anim.Stop()
            self.anim.Show(False)

    def IsWidgetSelectedByContext(self, widget):
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        stage = self.Parent.GetActiveStage()
        fit = mainFrame.getActiveFit()
        if stage == 3 or stage == 4:
            if self._wList[widget].GetType() == 3:
                if fit == self._wList[widget].fitID:
                    return True
        return False


class RaceSelector(wx.Window):
    def __init__ (self, parent, id = wx.ID_ANY, label = "", pos = wx.DefaultPosition, size = wx.Size(5,-1), style = 0):
        wx.Window.__init__(self, parent, id, pos = pos, size = size, style = style)
        self.SetSize(wx.Size(5,-1))
        self.SetMinSize(wx.Size(5,-1))

        self.animTimerID = wx.NewId()
        self.animTimer = wx.Timer(self, self.animTimerID)
        self.animPeriod = 25
        self.animDuration = 250
        self.animStep = 0
        self.minWidth = 5
        self.maxWidth = 24
        self.direction = 0

        self.checkTimerID = wx.NewId()
        self.checkTimer = wx.Timer(self, self.checkTimerID)
        self.checkPeriod = 250
        self.checkMaximize = True

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnWindowEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

    def OnTimer(self,event):
        if event.GetId() == self.animTimerID:
            start = 0
            end = self.maxWidth - self.minWidth

            step = animEffects.OUT_CIRC(self.animStep, start, end, self.animDuration)
            self.animStep += self.animPeriod * self.direction

            self.AdjustSize(self.minWidth + step)

            if self.animStep > self.animDuration or self.animStep < 0:
                self.animTimer.Stop()
                self.animStep = self.animDuration if self.direction == 1 else 0
                self.Parent.GetBrowserContainer().RefreshList(True)

        if event.GetId() == self.checkTimerID:
            if self.checkMaximize:
                self.direction = 1
            else:
                self.direction = -1

            if not self.animTimer.IsRunning():
                self.animTimer.Start(self.animPeriod)

    def AdjustSize(self, width):
        self.SetMinSize(wx.Size(width,-1))
        self.Parent.Layout()

    def OnWindowEnter(self, event):
        if not self.checkTimer.IsRunning():
            self.checkTimer.Start(self.checkPeriod, wx.TIMER_ONE_SHOT)
        self.checkMaximize = True

        event.Skip()

    def OnWindowLeave(self, event):
        if not self.checkTimer.IsRunning():
            self.checkTimer.Start(self.checkPeriod, wx.TIMER_ONE_SHOT)
        self.checkMaximize = False

        event.Skip()

class ShipBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent,style = 0)

        self._lastWidth = 0
        self._activeStage = 1
        self._lastStage = 0
        self.browseHist = []
        self.lastStage = (0,0)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

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

        self.lpane = PFWidgetsContainer(self)
#        self.raceselect = RaceSelector(self)
        container = wx.BoxSizer(wx.HORIZONTAL)

#        container.Add(self.raceselect,0,wx.EXPAND)
        container.Add(self.lpane,1,wx.EXPAND)
        mainSizer.Add(container, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        self.Layout()
        self.Show()

        self.Bind(wx.EVT_SIZE, self.SizeRefreshList)
        self.Bind(EVT_SB_STAGE2_SEL, self.stage2)
        self.Bind(EVT_SB_STAGE1_SEL, self.stage1)
        self.Bind(EVT_SB_STAGE3_SEL, self.stage3)
        self.Bind(EVT_SB_SEARCH_SEL, self.searchStage)

        self.mainFrame.Bind(GE.FIT_CHANGED, self.RefreshList)

        self.stage1(None)

    def GetBrowserContainer(self):
        return self.lpane

    def RefreshContent(self):
        stage = self.GetActiveStage()
        if stage == 1:
            return
        stageData = self.GetStageData(stage)
        self.hpane.gotoStage(stage, stageData)

    def RefreshList(self, event):
        stage = self.GetActiveStage()
        if stage == 3 or stage == 4:
            self.lpane.RefreshList(True)
        event.Skip()

    def SizeRefreshList(self, event):
        ewidth, eheight = event.GetSize()
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

    def stage1(self, event):
        self._lastStage = self._activeStage
        self._activeStage = 1
        self.lastdata = 0
        self.hpane.ToggleNewFitSB(False)
        self.hpane.ToggleFitViewModeSB(False)
        sMarket = service.Market.getInstance()

        self.lpane.ShowLoading(False)

        self.lpane.Freeze()
        self.lpane.RemoveAllChildren()
        if len(self.categoryList) == 0:
            self.categoryList = list(sMarket.getShipRoot())
            self.categoryList.sort(key=lambda ship: ship.name)
        for ship in self.categoryList:
            self.lpane.AddWidget(CategoryItem(self.lpane, ship.ID, (ship.name, 0)))

        self.lpane.RefreshList()
        self.lpane.Thaw()

    RACE_ORDER = ["amarr", "caldari", "gallente", "minmatar", "ore", "serpentis", "angel", "blood", "sansha", "guristas", None]
    def raceNameKey(self, ship):
        return self.RACE_ORDER.index(ship.race), ship.name

    def stage2Callback(self, data):
        if self.GetActiveStage() != 2:
            return
        ships = list(data[1])
        sFit = service.Fit.getInstance()

        ships.sort(key=self.raceNameKey)
        for ship in ships:
            fits = sFit.countFitsWithShip(ship.ID)
            if self.filterShipsWithNoFits:
                if fits>0:
                    self.lpane.AddWidget(ShipItem(self.lpane, ship.ID, (ship.name, fits), ship.race))
            else:
                self.lpane.AddWidget(ShipItem(self.lpane, ship.ID, (ship.name, fits), ship.race))

        self.lpane.ShowLoading(False)

        self.lpane.RefreshList()

    def stage2(self, event):
        back = event.back
        if not back:
            self.browseHist.append( (1,0) )
        self._lastStage = self._activeStage
        self._activeStage = 2
        categoryID = event.categoryID
        self.lastdata = categoryID

        self.lpane.ShowLoading()

        self.lpane.RemoveAllChildren()


        sMarket = service.Market.getInstance()
        sMarket.getShipListDelayed(self.stage2Callback, categoryID)

        self._stage2Data = categoryID
        self.hpane.ToggleNewFitSB(False)
        self.hpane.ToggleFitViewModeSB(True)

    def nameKey(self, info):
        return info[1]

    def stage3(self, event):

        self.lpane.ShowLoading(False)

        if event.back == 0:
            self.browseHist.append( (2,self._stage2Data) )
        elif event.back == -1:
            if len(self.hpane.recentSearches)>0:
                self.browseHist.append((4, self.hpane.lastSearch))

        shipID = event.shipID
        self.lastdata = shipID
        self._lastStage = self._activeStage
        self._activeStage = 3

        sFit = service.Fit.getInstance()
        sMarket = service.Market.getInstance()

        self.lpane.Freeze()
        self.lpane.RemoveAllChildren()
        fitList = sFit.getFitsWithShip(shipID)

        if len(fitList) == 0:
            stage,data = self.browseHist.pop()
            self.lpane.Thaw()
            self.hpane.gotoStage(stage,data)
            return
        self.hpane.ToggleFitViewModeSB(False)
        self.hpane.ToggleNewFitSB(True)
        fitList.sort(key=self.nameKey)
        shipName = sMarket.getItem(shipID).name

        self._stage3ShipName = shipName
        self._stage3Data = shipID

        for ID, name, timestamp in fitList:
            self.lpane.AddWidget(FitItem(self.lpane, ID, (shipName, name, timestamp),shipID))

        self.lpane.RefreshList()
        self.lpane.Thaw()

    def searchStage(self, event):

        self.lpane.ShowLoading(False)

        if not event.back:
            if self._activeStage !=4:
                if len(self.browseHist) >0:
                    self.browseHist.append( (self._activeStage, self.lastdata) )
                else:
                    self.browseHist.append((1,0))
            self._lastStage = self._activeStage
            self._activeStage = 4

        sMarket = service.Market.getInstance()
        sFit = service.Fit.getInstance()
        query = event.text

        self.lpane.Freeze()

        self.lpane.RemoveAllChildren()
        if query:
            ships = sMarket.searchShips(query)
            fitList = sFit.searchFits(query)

            for ship in ships:
                self.lpane.AddWidget(ShipItem(self.lpane, ship.ID, (ship.name, len(sFit.getFitsWithShip(ship.ID))), ship.race))

            for ID, name, shipID, shipName,timestamp in fitList:
                self.lpane.AddWidget(FitItem(self.lpane, ID, (shipName, name,timestamp), shipID))
            if len(ships) == 0 and len(fitList) == 0 :
                self.lpane.AddWidget(PFStaticText(self.lpane, label = "No matching results."))
            self.lpane.RefreshList(doFocus = False)
        self.lpane.Thaw()

class PFStaticText(wx.StaticText):
    def _init__(self,parent, label = wx.EmptyString):
        wx.StaticText(self,parent,label)

    def GetType(self):
        return -1

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

        img = self.switchBmp.ConvertToImage()
        img.RotateHue(0.500)
        self.switchHoverBmp = wx.BitmapFromImage(img)

        img = self.rewBmp.ConvertToImage()
        img.RotateHue(0.625)
        self.rewHoverBmp = wx.BitmapFromImage(img)

        img = self.resetBmp.ConvertToImage()
        img.RotateHue(-1)
        self.resetHoverBmp = wx.BitmapFromImage(img)

        img = self.searchBmp.ConvertToImage()
        img.RotateHue(0.625)
        self.searchHoverBmp = wx.BitmapFromImage(img)

        img = self.newBmp.ConvertToImage()
        img.RotateHue(0.350)
        self.newHoverBmp = wx.BitmapFromImage(img)


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

        if 'wxMac' in wx.PlatformInfo:
            bgcolour = wx.Colour(0, 0, 0, 0)
        else:
            bgcolour = wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE )

        self.sbReset = PFGenBitmapButton( self, wx.ID_ANY, self.resetBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
        mainSizer.Add(self.sbReset, 0, wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL , 5)
        self.sbReset.SetBackgroundColour( bgcolour )
        self.sbReset.SetBitmapSelected(self.resetBmp)

        self.sbRewind = PFGenBitmapButton( self, wx.ID_ANY, self.rewBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
        mainSizer.Add(self.sbRewind, 0, wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL , 5)
        self.sbRewind.SetBackgroundColour( bgcolour )
        self.sbRewind.SetBitmapSelected(self.rewBmp)

        self.sl1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        mainSizer.Add( self.sl1, 0, wx.EXPAND |wx.LEFT, 5 )

        self.sbNewFit = PFGenBitmapButton( self, wx.ID_ANY, self.newBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
        mainSizer.Add(self.sbNewFit, 0, wx.LEFT | wx.TOP | wx.BOTTOM  | wx.ALIGN_CENTER_VERTICAL , 5)
        self.sbNewFit.SetBackgroundColour( bgcolour )

        self.sbSwitchFitView = PFGenBitmapButton( self, wx.ID_ANY, self.switchBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
        mainSizer.Add(self.sbSwitchFitView, 0, wx.LEFT | wx.TOP | wx.BOTTOM  | wx.ALIGN_CENTER_VERTICAL , 5)
        self.sbSwitchFitView.SetBackgroundColour( bgcolour )


        self.stStatus = wx.StaticText( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stStatus.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
        self.stStatus.Wrap( -1 )
        mainSizer.Add(self.stStatus, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL , 5)

        self.spanel = wx.Panel(self)
        self.spanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        spsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.spanel.SetSizer(spsizer)

        self.search = wx.TextCtrl(self.spanel, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER )


        spsizer.Add(self.search,1, wx.ALIGN_CENTER_VERTICAL)
        mainSizer.Add(self.spanel,1000,wx.EXPAND | wx.LEFT, 5)

        self.sbSearch = PFGenBitmapButton( self, wx.ID_ANY, self.searchBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
        mainSizer.Add(self.sbSearch, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL , 5)
        self.sbSearch.SetBackgroundColour( bgcolour )

        self.SetSizer(mainSizer)

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

        return menu


    def editLostFocus(self, event = None):
        if self.inPopup:
            return
        if self.toggleSearch == 1:
            self.search.Show(False)
            self.spanel.Show(False)
            self.toggleSearch = -1

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
        self.Layout()

    def ToggleFitViewModeSB(self, toggle):
        self.sbSwitchFitView.Show(toggle)
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
            self.stStatus.SetLabel("Ship Groups")
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.sbReset.SetBitmapLabel(self.resetHoverBmp, False)
        self.sbReset.Refresh()
        event.Skip()

    def OnLeaveWReset(self, event):
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.sbReset.SetBitmapLabel(self.resetBmp, False)
        self.sbReset.Refresh()
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
        self.sbSearch.SetBitmapLabel(self.searchHoverBmp, False)
        self.Refresh()
        event.Skip()

    def OnLeaveWSearch(self, event):
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.sbSearch.SetBitmapLabel(self.searchBmp, False)
        self.Refresh()
        event.Skip()

    def OnEnterWSwitch(self, event):
        if self.toggleSearch != 1:
            self.stStatus.SetLabel("Show empty ship groups" if self.shipBrowser.filterShipsWithNoFits else "Hide empty ship groups")
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.sbSwitchFitView.SetBitmapLabel(self.switchHoverBmp, False)
        self.Refresh()
        event.Skip()

    def OnLeaveWSwitch(self, event):
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.sbSwitchFitView.SetBitmapLabel(self.switchBmp if not self.shipBrowser.filterShipsWithNoFits else self.switchSelBmp, False)
        self.Refresh()
        event.Skip()

    def OnEnterWNewFit(self, event):
        if self.toggleSearch != 1:
            self.stStatus.SetLabel("New fitting")
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.sbNewFit.SetBitmapLabel(self.newHoverBmp, False)
        self.Refresh()
        event.Skip()

    def OnLeaveWNewFit(self, event):
        self.stStatus.SetLabel("")
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.sbNewFit.SetBitmapLabel(self.newBmp, False)
        self.Refresh()
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


class CategoryItem(SFItem.SFBrowserItem):
    def __init__(self,parent, categoryID, fittingInfo, size = (0,16)):
        SFItem.SFBrowserItem.__init__(self,parent,size = size)

        if categoryID:
            self.shipBmp = bitmapLoader.getBitmap("ship_small","icons")
        else:
            self.shipBmp = wx.EmptyBitmap(16,16)

        self.categoryID = categoryID
        self.fittingInfo = fittingInfo
        self.shipBrowser = self.Parent.Parent

        self.padding = 4

        self.fontBig = wx.FontFromPixelSize((0,15),wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.animTimerId = wx.NewId()

        self.animTimer = wx.Timer(self, self.animTimerId)
        self.animStep = 0
        self.animPeriod = 10
        self.animDuration = 100

        self.Bind(wx.EVT_TIMER, self.OnTimer)

        #=======================================================================
        # Disabled - it will be added as an option to Preferences
        self.animCount = 0
        # self.animTimer.Start(self.animPeriod)
        #=======================================================================


    def OnTimer(self, event):
        step = self.OUT_QUAD(self.animStep, 0, 10, self.animDuration)
        self.animCount = 10 - step
        self.animStep += self.animPeriod
        if self.animStep > self.animDuration or self.animCount < 0 :
            self.animCount = 0
            self.animTimer.Stop()
        self.Refresh()

    def OUT_QUAD (self, t, b, c, d):
        t=float(t)
        b=float(b)
        c=float(c)
        d=float(d)

        t/=d

        return -c *(t)*(t-2) + b

    def GetType(self):
        return 1

    def MouseLeftUp(self, event):

        categoryID = self.categoryID
        wx.PostEvent(self.shipBrowser,Stage2Selected(categoryID=categoryID, back=False))

    def UpdateElementsPos(self, mdc):
        rect = self.GetRect()
        self.shipBmpx = self.padding
        self.shipBmpy = (rect.height-self.shipBmp.GetWidth())/2

        self.shipBmpx -= self.animCount

        mdc.SetFont(self.fontBig)
        categoryName, fittings = self.fittingInfo
        wtext, htext = mdc.GetTextExtent(categoryName)


        self.catx = self.shipBmpx + self.shipBmp.GetWidth() + self.padding
        self.caty = (rect.height - htext) / 2

    def DrawItem(self, mdc):
        rect = self.GetRect()

        self.UpdateElementsPos(mdc)

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        textColor = colorUtils.GetSuitableColor(windowColor, 1)

        mdc.SetTextForeground(textColor)

        mdc.DrawBitmap(self.shipBmp,self.shipBmpx,self.shipBmpy,0)

        mdc.SetFont(self.fontBig)

        categoryName, fittings = self.fittingInfo

        mdc.DrawText(categoryName, self.catx, self.caty)

#===============================================================================
#        Waiting for total #fits impl in eos/service
#
#        mdc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False))
#
#        if fittings <1:
#            fformat = "No fits"
#        else:
#            if fittings == 1:
#                fformat = "%d fit"
#            else:
#                fformat = "%d fits"
#
#        if fittings>0:
#            xtext, ytext = mdc.GetTextExtent(fformat % fittings)
#            ypos = (rect.height - ytext)/2
#        else:
#            xtext, ytext = mdc.GetTextExtent(fformat)
#            ypos = (rect.height - ytext)/2
#===============================================================================


class ShipItem(SFItem.SFBrowserItem):
    def __init__(self, parent, shipID=None, shipFittingInfo=("Test", 2), itemData=None,
                 id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=(0, 40), style=0):
        SFItem.SFBrowserItem.__init__(self, parent, size = size)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self._itemData = itemData

        self.shipRace = itemData

        self.shipID = shipID

        self.fontBig = wx.FontFromPixelSize((0,15),wx.SWISS, wx.NORMAL, wx.BOLD, False)
        self.fontNormal = wx.FontFromPixelSize((0,14),wx.SWISS, wx.NORMAL, wx.NORMAL, False)
        self.fontSmall = wx.FontFromPixelSize((0,12),wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.shipBmp = None
        if shipID:
            self.shipBmp = bitmapLoader.getBitmap(str(shipID),"ships")
        if not self.shipBmp:
            self.shipBmp = bitmapLoader.getBitmap("ship_no_image_big","icons")

        self.shipFittingInfo = shipFittingInfo
        self.shipName, self.shipFits = shipFittingInfo

        self.newBmp = bitmapLoader.getBitmap("fit_add_small", "icons")
        self.acceptBmp = bitmapLoader.getBitmap("faccept_small", "icons")

        self.shipEffBk = bitmapLoader.getBitmap("fshipbk_big","icons")

        img = wx.ImageFromBitmap(self.shipEffBk)
        img = img.Mirror(False)
        self.shipEffBkMirrored = wx.BitmapFromImage(img)

        self.raceBmp = bitmapLoader.getBitmap("race_%s_small" % self.shipRace, "icons")

        if self.shipName == "Apotheosis":
            self.raceMBmp = bitmapLoader.getBitmap("race_jove_small","icons")
        else:
            self.raceMBmp = bitmapLoader.getBitmap("fit_delete_small","icons")

        if not self.raceBmp:
            self.raceBmp = self.raceMBmp

        self.shipBrowser = self.Parent.Parent

        self.editWidth = 150
        self.padding = 4

        self.tcFitName = wx.TextCtrl(self, wx.ID_ANY, "%s fit" % self.shipName, wx.DefaultPosition, (120,-1), wx.TE_PROCESS_ENTER)
        self.tcFitName.Show(False)


        self.newBtn = self.toolbar.AddButton(self.newBmp,"New", self.newBtnCB)

        self.tcFitName.Bind(wx.EVT_TEXT_ENTER, self.createNewFit)
        self.tcFitName.Bind(wx.EVT_KILL_FOCUS, self.editLostFocus)
        self.tcFitName.Bind(wx.EVT_KEY_DOWN, self.editCheckEsc)

        self.animTimerId = wx.NewId()

        self.animTimer = wx.Timer(self, self.animTimerId)
        self.animStep = 0
        self.animPeriod = 10
        self.animDuration = 100
        #=======================================================================\
        # DISABLED - it will be added as an option in PREFERENCES

        self.animCount = 0

        # if self.shipBrowser.GetActiveStage() != 4 and self.shipBrowser.GetLastStage() !=2:
        #    self.Bind(wx.EVT_TIMER, self.OnTimer)
        #    self.animTimer.Start(self.animPeriod)
        # else:
        #    self.animCount = 0
        #=======================================================================

    def OnTimer(self, event):
        step = self.OUT_QUAD(self.animStep, 0, 10, self.animDuration)
        self.animCount = 10 - step
        self.animStep += self.animPeriod
        if self.animStep > self.animDuration or self.animCount < 0 :
            self.animCount = 0
            self.animTimer.Stop()
        self.Refresh()

    def OUT_QUAD (self, t, b, c, d):
        t=float(t)
        b=float(b)
        c=float(c)
        d=float(d)

        t/=d

        return -c *(t)*(t-2) + b

    def GetType(self):
        return 2

    def MouseLeftUp(self, event):
        if self.tcFitName.IsShown():
            self.tcFitName.Show(False)
            self.newBtn.SetBitmap(self.newBmp)
            self.Refresh()
        else:
            shipName, fittings = self.shipFittingInfo
            if fittings > 0:
                wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID, back = -1 if self.shipBrowser.GetActiveStage() == 4 else 0))
            else:
                self.newBtnCB()

    def newBtnCB(self):
        if self.tcFitName.IsShown():
            self.tcFitName.Show(False)
            self.createNewFit()
        else:
            self.tcFitName.SetValue("%s fit" % self.shipName)
            self.tcFitName.Show()

            self.tcFitName.SetFocus()
            self.tcFitName.SelectAll()

            self.newBtn.SetBitmap(self.acceptBmp)

            self.Refresh()

    def editLostFocus(self, event):
        self.tcFitName.Show(False)
        self.newBtn.SetBitmap(self.newBmp)
        self.Refresh()

    def editCheckEsc(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.tcFitName.Show(False)
        else:
            event.Skip()

    def createNewFit(self, event=None):
        self.tcFitName.Show(False)

        sFit = service.Fit.getInstance()
        fitID = sFit.newFit(self.shipID, self.tcFitName.GetValue())

        wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID, back=False))
        wx.PostEvent(self.mainFrame, FitSelected(fitID=fitID))

    def UpdateElementsPos(self, mdc):
        rect = self.GetRect()

        self.toolbarx = rect.width - self.toolbar.GetWidth() - self.padding
        self.toolbary = (rect.height - self.toolbar.GetHeight()) / 2

        self.toolbarx = self.toolbarx + self.animCount

        self.shipEffx = self.padding + (rect.height - self.shipEffBk.GetWidth())/2
        self.shipEffy = (rect.height - self.shipEffBk.GetHeight())/2

        self.shipEffx = self.shipEffx - self.animCount

        self.shipBmpx = self.padding + (rect.height - self.shipBmp.GetWidth()) / 2
        self.shipBmpy = (rect.height - self.shipBmp.GetHeight()) / 2

        self.shipBmpx= self.shipBmpx - self.animCount

        self.raceBmpx = self.shipEffx + self.shipEffBk.GetWidth() + self.padding
        self.raceBmpy = (rect.height - self.raceBmp.GetHeight())/2

        self.textStartx = self.raceBmpx + self.raceBmp.GetWidth() + self.padding

        self.shipNamey = (rect.height - self.shipBmp.GetHeight()) / 2

        shipName, fittings = self.shipFittingInfo

        mdc.SetFont(self.fontBig)
        wtext, htext = mdc.GetTextExtent(shipName)

        self.fittingsy = self.shipNamey + htext

        mdc.SetFont(self.fontSmall)

        wlabel,hlabel = mdc.GetTextExtent(self.toolbar.hoverLabel)

        self.thoverx = self.toolbarx - self.padding - wlabel
        self.thovery = (rect.height - hlabel)/2
        self.thoverw = wlabel

    def DrawItem(self, mdc):
        rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        textColor = colorUtils.GetSuitableColor(windowColor, 1)

        mdc.SetTextForeground(textColor)

        self.UpdateElementsPos(mdc)

        self.toolbar.SetPosition((self.toolbarx, self.toolbary))

        if self.GetState() & SFItem.SB_ITEM_HIGHLIGHTED:
            shipEffBk = self.shipEffBkMirrored
        else:
            shipEffBk = self.shipEffBk

        mdc.DrawBitmap(shipEffBk, self.shipEffx, self.shipEffy, 0)

        mdc.DrawBitmap(self.shipBmp, self.shipBmpx, self.shipBmpy, 0)

        mdc.DrawBitmap(self.raceBmp,self.raceBmpx, self.raceBmpy)

        shipName, fittings = self.shipFittingInfo

        if fittings <1:
            fformat = "No fits"
        else:
            if fittings == 1:
                fformat = "%d fit"
            else:
                fformat = "%d fits"

        mdc.SetFont(self.fontNormal)
        mdc.DrawText(fformat %fittings if fittings >0 else fformat, self.textStartx, self.fittingsy)

        mdc.SetFont(self.fontSmall)
        mdc.DrawText(self.toolbar.hoverLabel, self.thoverx, self.thovery)

        mdc.SetFont(self.fontBig)

        psname = drawUtils.GetPartialText(mdc, shipName, self.toolbarx - self.textStartx - self.padding * 2 - self.thoverw)

        mdc.DrawText(psname, self.textStartx, self.shipNamey)

        if self.tcFitName.IsShown():
            self.AdjustControlSizePos(self.tcFitName, self.textStartx, self.toolbarx - self.editWidth - self.padding)

    def AdjustControlSizePos(self, editCtl, start, end):
        fnEditSize = editCtl.GetSize()
        wSize = self.GetSize()
        fnEditPosX = end
        fnEditPosY = (wSize.height - fnEditSize.height)/2
        if fnEditPosX < start:
            editCtl.SetSize((self.editWidth + fnEditPosX - start,-1))
            editCtl.SetPosition((start,fnEditPosY))
        else:
            editCtl.SetSize((self.editWidth,-1))
            editCtl.SetPosition((fnEditPosX,fnEditPosY))

class PFBitmapFrame(wx.Frame):
    def __init__ (self,parent, pos, bitmap):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = pos, size = wx.DefaultSize, style =
                                                               wx.NO_BORDER
                                                             | wx.FRAME_NO_TASKBAR
                                                             | wx.STAY_ON_TOP)
        img = bitmap.ConvertToImage()
        img = img.ConvertToGreyscale()
        bitmap = wx.BitmapFromImage(img)
        self.bitmap = bitmap
        self.SetSize((bitmap.GetWidth(), bitmap.GetHeight()))
        self.Bind(wx.EVT_PAINT,self.OnWindowPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnWindowEraseBk)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.timer = wx.Timer(self,wx.ID_ANY)
        self.direction = 1
        self.transp = 0
        self.SetSize((bitmap.GetWidth(),bitmap.GetHeight()))

        self.SetTransparent(0)
        self.Refresh()

    def OnTimer(self, event):
        self.transp += 20*self.direction
        if self.transp > 200:
            self.transp = 200
            self.timer.Stop()
        if self.transp < 0:
            self.transp = 0
            self.timer.Stop()
            wx.Frame.Show(self,False)
            self.Destroy()
            return
        self.SetTransparent(self.transp)

    def Show(self, showWnd = True):
        if showWnd:
            wx.Frame.Show(self, showWnd)
            self.Parent.SetFocus()
            self.direction = 1
            self.timer.Start(5)
        else:
            self.direction = -1
            self.timer.Start(5)

    def OnWindowEraseBk(self,event):
        pass

    def OnWindowPaint(self,event):
        rect = self.GetRect()
        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        mdc.DrawBitmap(self.bitmap, 0, 0)
        mdc.SetPen( wx.Pen("#000000", width = 1 ) )
        mdc.SetBrush( wx.TRANSPARENT_BRUSH )
        mdc.DrawRectangle( 0,0,rect.width,rect.height)


class FitItem(SFItem.SFBrowserItem):
    def __init__(self, parent, fitID=None, shipFittingInfo=("Test", "cnc's avatar", 0 ), shipID = None, itemData=None,
                 id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=(0, 40), style=0):

        #===============================================================================
        # animCount should be 10 if we enable animation in Preferences
        #===============================================================================

        self.animCount = 0
        self.selectedDelta = 0

        SFItem.SFBrowserItem.__init__(self,parent,size = size)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self._itemData = itemData

        self.fitID = fitID

        self.shipID = shipID

        self.shipBrowser = self.Parent.Parent

        self.shipBmp = None

        self.deleted = False

        if shipID:
            self.shipBmp = bitmapLoader.getBitmap(str(shipID),"ships")

        if not self.shipBmp:
            self.shipBmp = bitmapLoader.getBitmap("ship_no_image_big","icons")

        self.shipFittingInfo = shipFittingInfo
        self.shipName, self.fitName, self.timestamp = shipFittingInfo

        self.copyBmp = bitmapLoader.getBitmap("fit_add_small", "icons")
        self.renameBmp = bitmapLoader.getBitmap("fit_rename_small", "icons")
        self.deleteBmp = bitmapLoader.getBitmap("fit_delete_small","icons")
        self.acceptBmp = bitmapLoader.getBitmap("faccept_small", "icons")

        self.shipEffBk = bitmapLoader.getBitmap("fshipbk_big","icons")

        img = wx.ImageFromBitmap(self.shipEffBk)
        img = img.Mirror(False)
        self.shipEffBkMirrored = wx.BitmapFromImage(img)

        self.dragTLFBmp = None

        self.bkBitmap = None

        self.padding = 4
        self.editWidth = 150

        self.dragging = False
        self.dragged = False
        self.dragMotionTrail = 5
        self.dragMotionTrigger = self.dragMotionTrail
        self.dragWindow = None

        self.fontBig = wx.FontFromPixelSize((0,15),wx.SWISS, wx.NORMAL, wx.BOLD, False)
        self.fontNormal = wx.FontFromPixelSize((0,14),wx.SWISS, wx.NORMAL, wx.NORMAL, False)
        self.fontSmall = wx.FontFromPixelSize((0,12),wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.SetDraggable()

        self.toolbar.AddButton(self.copyBmp,"Copy", self.copyBtnCB)
        self.renameBtn = self.toolbar.AddButton(self.renameBmp,"Rename", self.renameBtnCB)
        self.toolbar.AddButton(self.deleteBmp, "Delete", self.deleteBtnCB)

        self.tcFitName = wx.TextCtrl(self, wx.ID_ANY, "%s" % self.fitName, wx.DefaultPosition, (self.editWidth,-1), wx.TE_PROCESS_ENTER)

        if self.shipBrowser.fitIDMustEditName != self.fitID:
            self.tcFitName.Show(False)
        else:
            self.tcFitName.SetFocus()
            self.tcFitName.SelectAll()
            self.shipBrowser.fitIDMustEditName = -1
            self.renameBtn.SetBitmap(self.acceptBmp)

        self.tcFitName.Bind(wx.EVT_TEXT_ENTER, self.renameFit)
        self.tcFitName.Bind(wx.EVT_KILL_FOCUS, self.editLostFocus)
        self.tcFitName.Bind(wx.EVT_KEY_DOWN, self.editCheckEsc)

        self.animTimerId = wx.NewId()
        self.animTimer = wx.Timer(self, self.animTimerId)
        self.animStep = 0
        self.animPeriod = 10
        self.animDuration = 100

        self.maxDelta = 48

        self.Bind(wx.EVT_TIMER, self.OnTimer)

        #=======================================================================
        # DISABLED - it will be added as an option in PREFERENCES

        # if self.shipBrowser.GetActiveStage() != 4 and self.shipBrowser.GetLastStage() !=3:
        #    self.animTimer.Start(self.animPeriod)
        # else:
        #    self.animCount = 0
        #=======================================================================

        self.selTimerID = wx.NewId()

        self.selTimer = wx.Timer(self,self.selTimerID)
        self.selTimer.Start(100)

    def GetType(self):
        return 3


    def OnTimer(self, event):

        if self.selTimerID == event.GetId():
            ctimestamp = time.time()
            interval = 5
            if ctimestamp < self.timestamp + interval:
                delta = (ctimestamp - self.timestamp) / interval
                self.selectedDelta = self.CalculateDelta(0x0,self.maxDelta,delta)
                self.Refresh()
            else:
                self.selectedDelta = self.maxDelta
                self.selTimer.Stop()

        if self.animTimerId == event.GetId():
            step = self.OUT_QUAD(self.animStep, 0, 10, self.animDuration)
            self.animCount = 10 - step
            self.animStep += self.animPeriod
            if self.animStep > self.animDuration or self.animCount < 0 :
                self.animCount = 0
                self.animTimer.Stop()
            self.Refresh()

    def CalculateDelta(self, start, end, delta):
        return start + (end-start)*delta

    def OUT_QUAD (self, t, b, c, d):
        t=float(t)
        b=float(b)
        c=float(c)
        d=float(d)

        t/=d

        return -c *(t)*(t-2) + b

    def editLostFocus(self, event):
        self.RestoreEditButton()
        self.Refresh()

    def editCheckEsc(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.RestoreEditButton()
        else:
            event.Skip()

    def copyBtnCB(self):
        if self.tcFitName.IsShown():
            self.RestoreEditButton()
            return

        self.copyFit()

    def copyFit(self, event=None):
        sFit = service.Fit.getInstance()
        fitID = sFit.copyFit(self.fitID)
        self.shipBrowser.fitIDMustEditName = fitID
        wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID, back=True))
        wx.PostEvent(self.mainFrame, FitSelected(fitID=fitID))

    def renameBtnCB(self):
        if self.tcFitName.IsShown():
            self.RestoreEditButton()
            self.renameFit()
        else:
            self.tcFitName.SetValue(self.fitName)
            self.tcFitName.Show()
            self.renameBtn.SetBitmap(self.acceptBmp)
            self.tcFitName.SetFocus()
            self.tcFitName.SelectAll()

            self.Refresh()

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

    def deleteBtnCB(self):
        if self.tcFitName.IsShown():
            self.RestoreEditButton()
            return

        self.deleteFit()

    def deleteFit(self, event=None):
        if self.deleted:
            return
        else:
            self.deleted = True

        sFit = service.Fit.getInstance()

        sFit.deleteFit(self.fitID)

        if self.shipBrowser.GetActiveStage() == 4:
            wx.PostEvent(self.shipBrowser,SearchSelected(text=self.shipBrowser.hpane.lastSearch,back=True))
        else:
            wx.PostEvent(self.shipBrowser,Stage3Selected(shipID=self.shipID, back=True))

        wx.PostEvent(self.mainFrame, FitRemoved(fitID=self.fitID))

    def MouseLeftUp(self, event):

        if self.dragging and self.dragged:
            self.dragging = False
            self.dragged = False
            if self.HasCapture():
                self.ReleaseMouse()
            self.dragWindow.Show(False)
            self.dragWindow = None

            targetWnd = wx.FindWindowAtPointer()

            if not targetWnd:
                return

            wnd = targetWnd
            while wnd is not None:
                handler = getattr(wnd, "handleDrag", None)
                if handler:
                    handler("fit", self.fitID)
                    break
                else:
                    wnd = wnd.Parent
            event.Skip()
            return

        if self.dragging:
            self.dragging = False

        if self.tcFitName.IsShown():
            self.RestoreEditButton()
        else:
            activeFitID = self.mainFrame.getActiveFit()
            if activeFitID != self.fitID:
                self.selectFit()

    def MouseLeftDown(self, event):
        self.dragging = True

    def MouseMove(self, event):
        pos = self.ClientToScreen(event.GetPosition())
        if self.dragging:
            if not self.dragged:
                if self.dragMotionTrigger < 0:
                    self.CaptureMouse()
                    self.dragWindow = PFBitmapFrame(self, pos, self.dragTLFBmp)
                    self.dragWindow.Show()
                    self.dragged = True
                    self.dragMotionTrigger = self.dragMotionTrail
                else:
                    self.dragMotionTrigger -= 1
            if self.dragWindow:
                pos.x += 3
                pos.y += 3
                self.dragWindow.SetPosition(pos)
            return

    def selectFit(self, event=None):
        wx.PostEvent(self.mainFrame, FitSelected(fitID=self.fitID))
        self.Parent.RefreshList(True)

    def RestoreEditButton(self):
            self.tcFitName.Show(False)
            self.renameBtn.SetBitmap(self.renameBmp)
            self.Refresh()

    def UpdateElementsPos(self, mdc):
        rect = self.GetRect()

        self.toolbarx = rect.width - self.toolbar.GetWidth() - self.padding
        self.toolbary = (rect.height - self.toolbar.GetHeight()) / 2

        self.toolbarx = self.toolbarx + self.animCount

        self.shipEffx = self.padding + (rect.height - self.shipEffBk.GetWidth())/2
        self.shipEffy = (rect.height - self.shipEffBk.GetHeight())/2

        self.shipEffx = self.shipEffx - self.animCount

        self.shipBmpx = self.padding + (rect.height - self.shipBmp.GetWidth()) / 2
        self.shipBmpy = (rect.height - self.shipBmp.GetHeight()) / 2

        self.shipBmpx= self.shipBmpx - self.animCount

        self.textStartx = self.shipEffx + self.shipEffBk.GetWidth() + self.padding

        self.fitNamey = (rect.height - self.shipBmp.GetHeight()) / 2

        mdc.SetFont(self.fontBig)
        wtext, htext = mdc.GetTextExtent(self.fitName)

        self.timestampy = self.fitNamey + htext

        mdc.SetFont(self.fontSmall)

        wlabel,hlabel = mdc.GetTextExtent(self.toolbar.hoverLabel)

        self.thoverx = self.toolbarx - self.padding - wlabel
        self.thovery = (rect.height - hlabel)/2
        self.thoverw = wlabel

    def DrawItem(self, mdc):
        rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        textColor = colorUtils.GetSuitableColor(windowColor, 1)

        mdc.SetTextForeground(textColor)

        self.UpdateElementsPos(mdc)

        self.toolbar.SetPosition((self.toolbarx, self.toolbary))

        if self.GetState() & SFItem.SB_ITEM_HIGHLIGHTED:
            shipEffBk = self.shipEffBkMirrored
        else:
            shipEffBk = self.shipEffBk

        mdc.DrawBitmap(shipEffBk, self.shipEffx, self.shipEffy, 0)

        mdc.DrawBitmap(self.shipBmp, self.shipBmpx, self.shipBmpy, 0)

        shipName, fittings, timestamp = self.shipFittingInfo

        mdc.SetFont(self.fontNormal)

        fitDate = time.localtime(self.timestamp)
        fitLocalDate = "%d/%02d/%02d %02d:%02d" % ( fitDate[0], fitDate[1], fitDate[2], fitDate[3], fitDate[4])
        pfdate = drawUtils.GetPartialText(mdc, fitLocalDate, self.toolbarx - self.textStartx - self.padding * 2 - self.thoverw)

        mdc.DrawText(pfdate, self.textStartx, self.timestampy)

        mdc.SetFont(self.fontSmall)
        mdc.DrawText(self.toolbar.hoverLabel, self.thoverx, self.thovery)

        mdc.SetFont(self.fontBig)

        psname = drawUtils.GetPartialText(mdc, self.fitName, self.toolbarx - self.textStartx - self.padding * 2 - self.thoverw)

        mdc.DrawText(psname, self.textStartx, self.fitNamey)

        if self.tcFitName.IsShown():
            self.AdjustControlSizePos(self.tcFitName, self.textStartx, self.toolbarx - self.editWidth - self.padding)

        tdc = wx.MemoryDC()
        self.dragTLFBmp = wx.EmptyBitmap((self.toolbarx if self.toolbarx < 200 else 200), rect.height)
        tdc.SelectObject(self.dragTLFBmp)
        tdc.Blit(0, 0, (self.toolbarx if self.toolbarx < 200 else 200), rect.height, mdc, 0, 0, wx.COPY)
        tdc.SelectObject(wx.NullBitmap)

    def AdjustControlSizePos(self, editCtl, start, end):
        fnEditSize = editCtl.GetSize()
        wSize = self.GetSize()
        fnEditPosX = end
        fnEditPosY = (wSize.height - fnEditSize.height)/2
        if fnEditPosX < start:
            editCtl.SetSize((self.editWidth + fnEditPosX - start,-1))
            editCtl.SetPosition((start,fnEditPosY))
        else:
            editCtl.SetSize((self.editWidth,-1))
            editCtl.SetPosition((fnEditPosX,fnEditPosY))

    def GetState(self):
        activeFitID = self.mainFrame.getActiveFit()

        if self.highlighted and not activeFitID == self.fitID:
            state = SFItem.SB_ITEM_HIGHLIGHTED

        else:
            if activeFitID == self.fitID:
                if self.highlighted:
                    state = SFItem.SB_ITEM_SELECTED  | SFItem.SB_ITEM_HIGHLIGHTED
                else:
                    state = SFItem.SB_ITEM_SELECTED
            else:
                state = SFItem.SB_ITEM_NORMAL
        return state

    def RenderBackground(self):
        rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)

        activeFitID = self.mainFrame.getActiveFit()

        state = self.GetState()

        sFactor = 0.2
        mFactor = None
        eFactor = 0

        if state == SFItem.SB_ITEM_HIGHLIGHTED:
            mFactor = 0.45
            eFactor = 0.30

        elif state == SFItem.SB_ITEM_SELECTED  | SFItem.SB_ITEM_HIGHLIGHTED:
            eFactor = 0.3
            mFactor = 0.4

        elif state == SFItem.SB_ITEM_SELECTED:
            eFactor = (self.maxDelta - self.selectedDelta)/100 + 0.25
        else:
            sFactor = 0

        if self.bkBitmap:
            if self.bkBitmap.eFactor == eFactor and self.bkBitmap.sFactor == sFactor and self.bkBitmap.mFactor == mFactor \
             and rect.width == self.bkBitmap.GetWidth() and rect.height == self.bkBitmap.GetHeight() :
                return
            else:
                del self.bkBitmap

        self.bkBitmap = drawUtils.RenderGradientBar(windowColor, rect.width, rect.height, sFactor, eFactor, mFactor)
        self.bkBitmap.state = state
        self.bkBitmap.sFactor = sFactor
        self.bkBitmap.eFactor = eFactor
        self.bkBitmap.mFactor = mFactor

