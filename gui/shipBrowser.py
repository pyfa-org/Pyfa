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
from gui.contextMenu import ContextMenu

import service

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
    def __init__ (self, parent, id = wx.ID_ANY, label = "", pos = wx.DefaultPosition, size = wx.DefaultSize, style = 0, layout = wx.VERTICAL, animate = False):
        wx.Window.__init__(self, parent, id, pos = pos, size = size, style = style)

        self.animTimerID = wx.NewId()
        self.animTimer = wx.Timer(self, self.animTimerID)
        self.animPeriod = 25
        self.animDuration = 250
        self.animStep = 0
        self.maxWidth = 24
        self.minWidth = 5 if animate else self.maxWidth
        self.maxHeight = 24
        self.minHeight = 10 if animate else self.maxHeight

        self.direction = 0 if animate else 1
        self.layout = layout
        self.animate = animate

        if layout == wx.VERTICAL:
            self.SetSize(wx.Size(self.minWidth, -1))
            self.SetMinSize(wx.Size(self.minWidth, -1))
        else:
            self.SetSize(wx.Size(-1, self.minHeight))
            self.SetMinSize(wx.Size(-1, self.minHeight))


        self.checkTimerID = wx.NewId()
        self.checkTimer = wx.Timer(self, self.checkTimerID)
        self.checkPeriod = 250
        self.checkMaximize = True
        self.shipBrowser = self.Parent
        self.raceBmps = []
        self.raceNames = []
        self.hoveredItem = None

        if layout == wx.VERTICAL:
            self.buttonsBarPos = (4,0)
        else:
            self.buttonsBarPos = (0,4)

        self.buttonsPadding = 4

        if layout == wx.VERTICAL:
            self.bmpArrow = bitmapLoader.getBitmap("down-arrow2","icons")
        else:
            self.bmpArrow = bitmapLoader.getBitmap("up-arrow2","icons")

        #    Make the bitmaps have the same color as window text

        sysTextColour = wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT )

        img = self.bmpArrow.ConvertToImage()
        if layout == wx.VERTICAL:
            img = img.Rotate90(False)
        img.Replace(0, 0, 0, sysTextColour[0], sysTextColour[1], sysTextColour[2])
        if layout == wx.VERTICAL:
            img = img.Scale(self.minWidth, 8, wx.IMAGE_QUALITY_HIGH)

        self.bmpArrow = wx.BitmapFromImage(img)

        self.RebuildRaces(self.shipBrowser.RACE_ORDER)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnWindowEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnBackgroundErase)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_SIZE, self.OnSizeUpdate)

        self.Layout()

    def OnMouseMove(self, event):
        mx,my = event.GetPosition()

        location = self.HitTest(mx,my)
        if location != self.hoveredItem:
            self.hoveredItem = location
            self.Refresh()
            if location is not None:
                self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            else:
                self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

    def OnSizeUpdate(self,event):
        self.CalcButtonsBarPos()

        self.Refresh()

        event.Skip()

    def CalcButtonsBarPos(self):

        if self.layout == wx.HORIZONTAL:
            rect = self.GetRect()
            width = 0
            height = 0
            for bmp in self.raceBmps:
                width += bmp.GetWidth() + self.buttonsPadding
                height = max(bmp.GetHeight(), height)

            posx = (rect.width - width) / 2
            posy = (rect.height - height) / 2

            self.buttonsBarPos = (posx, posy)

    def OnLeftUp(self, event):

        mx,my = event.GetPosition()

        toggle = self.HitTest(mx,my)

        if toggle is not None:
            self.Refresh()

            self.shipBrowser.ToggleRacesFilter(self.raceNames[toggle])

            stage = self.shipBrowser.GetActiveStage()

            if stage == 2:
                categoryID = self.shipBrowser.GetStageData(stage)
                wx.PostEvent(self.shipBrowser,Stage2Selected(categoryID=categoryID, back = True))
        event.Skip()

    def HitTest(self, mx,my):
        x,y = self.buttonsBarPos
        padding = self.buttonsPadding

        for bmp in self.raceBmps:
            if (mx > x and mx < x + bmp.GetWidth()) and (my > y and my < y + bmp.GetHeight()):
                return self.raceBmps.index(bmp)
            if self.layout == wx.VERTICAL:
                y += bmp.GetHeight() + padding
            else:
                x += bmp.GetWidth() + padding

        return None

    def RebuildRaces(self, races):
        self.raceBmps = []
        for race in races:
            if race:
                self.raceBmps.append(bitmapLoader.getBitmap("race_%s_small" % race, "icons"))
        self.raceNames = races
        self.CalcButtonsBarPos()
        self.Refresh()

    def OnBackgroundErase(self, event):
        pass

    def OnPaint(self, event):
        rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        bkColor = colorUtils.GetSuitableColor(windowColor, 0.1)
        sepColor = colorUtils.GetSuitableColor(windowColor, 0.2)

        mdc = wx.BufferedPaintDC(self)

        bkBitmap = drawUtils.RenderGradientBar(windowColor, rect.width, rect.height, 0.1, 0.1, 0.2, 2)
        mdc.DrawBitmap(bkBitmap,0,0,True)


        x ,y = self.buttonsBarPos

        if self.direction == 1:
            for raceBmp in self.raceBmps:
                dropShadow = drawUtils.CreateDropShadowBitmap(raceBmp, 0.2)

                if self.shipBrowser.GetRaceFilterState(self.raceNames[self.raceBmps.index(raceBmp)]):
                    bmp = raceBmp
                else:
                    img = wx.ImageFromBitmap(raceBmp)
                    if self.hoveredItem == self.raceBmps.index(raceBmp):
                        img = img.AdjustChannels(1, 1, 1, 0.7)
                    else:
                        img = img.AdjustChannels(1, 1, 1, 0.4)
                    bmp = wx.BitmapFromImage(img)

                if self.layout == wx.VERTICAL:
                    mdc.DrawBitmap(dropShadow, rect.width - self.buttonsPadding - bmp.GetWidth() + 1, y + 1)
                    mdc.DrawBitmap(bmp, rect.width - self.buttonsPadding - bmp.GetWidth(), y)
                    y+=raceBmp.GetHeight() + self.buttonsPadding
                    mdc.SetPen(wx.Pen(sepColor,1))
                    mdc.DrawLine(rect.width - 1, 0, rect.width -1, rect.height)
                else:
                    mdc.DrawBitmap(dropShadow, x + 1, self.buttonsPadding + 1)
                    mdc.DrawBitmap(bmp, x, self.buttonsPadding)
                    x+=raceBmp.GetWidth() + self.buttonsPadding
                    mdc.SetPen(wx.Pen(sepColor,1))
                    mdc.DrawLine(0, 0, rect.width, 0)

        if self.direction < 1:
            if self.layout == wx.VERTICAL:
                mdc.DrawBitmap(self.bmpArrow, -2, (rect.height - self.bmpArrow.GetHeight()) / 2)
            else:
                mdc.SetPen(wx.Pen(sepColor,1))
                mdc.DrawLine(0, 0, rect.width, 0)
                mdc.DrawBitmap(self.bmpArrow, (rect.width - self.bmpArrow.GetWidth()) / 2, -2)



    def OnTimer(self,event):
        if event.GetId() == self.animTimerID:
            start = 0
            if self.layout == wx.VERTICAL:
                end = self.maxWidth - self.minWidth
            else:
                end = self.maxHeight - self.minHeight

            step = animEffects.OUT_CIRC(self.animStep, start, end, self.animDuration)
            self.animStep += self.animPeriod * self.direction

            self.AdjustSize((self.minWidth if self.layout == wx.VERTICAL else self.minHeight) + step)

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

    def AdjustSize(self, delta):
        self.SetMinSize(wx.Size(delta,-1) if self.layout == wx.VERTICAL else wx.Size(-1, delta))
        self.Parent.Layout()
        self.Refresh()

    def OnWindowEnter(self, event):
        if not self.animate:
            return

        if not self.checkTimer.IsRunning():
            self.checkTimer.Start(self.checkPeriod, wx.TIMER_ONE_SHOT)
        self.checkMaximize = True

        event.Skip()

    def OnWindowLeave(self, event):
        if self.hoveredItem is not None:
            self.hoveredItem = None
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            self.Refresh()

        if not self.animate:
            return

        if not self.checkTimer.IsRunning():
            self.checkTimer.Start(self.checkPeriod, wx.TIMER_ONE_SHOT)
        self.checkMaximize = False

        event.Skip()

class NavigationPanel(SFItem.SFBrowserItem):
    def __init__(self,parent, size = (-1,24)):
        SFItem.SFBrowserItem.__init__(self,parent,size = size)

        self.rewBmpH = bitmapLoader.getBitmap("frewind_small","icons")
        self.forwBmp = bitmapLoader.getBitmap("fforward_small","icons")
        self.searchBmpH = bitmapLoader.getBitmap("fsearch_small","icons")
        self.newBmpH = bitmapLoader.getBitmap("fit_add_small","icons")
        self.resetBmpH = bitmapLoader.getBitmap("freset_small","icons")
        self.switchBmpH = bitmapLoader.getBitmap("fit_switch_view_mode_small","icons")

        self.resetBmp = self.AdjustChannels(self.resetBmpH)
        self.rewBmp = self.AdjustChannels(self.rewBmpH)
        self.searchBmp = self.AdjustChannels(self.searchBmpH)
        self.switchBmp = self.AdjustChannels(self.switchBmpH)
        self.newBmp = self.AdjustChannels(self.newBmpH)

        self.toolbar.AddButton(self.resetBmp, "Ship groups", clickCallback = self.OnHistoryReset, hoverBitmap = self.resetBmpH)
        self.toolbar.AddButton(self.rewBmp, "Back", clickCallback = self.OnHistoryBack, hoverBitmap = self.rewBmpH)
        self.btnNew = self.toolbar.AddButton(self.newBmp, "New fitting", clickCallback = self.OnNewFitting, hoverBitmap = self.newBmpH, show = False)
        self.btnSwitch = self.toolbar.AddButton(self.switchBmp, "Hide empty ship groups", clickCallback  = self.ToggleEmptyGroupsView, hoverBitmap = self.switchBmpH, show = False)
        self.toolbar.AddButton(self.searchBmp, "Search fittings", clickCallback = self.ToggleSearchBox, hoverBitmap = self.searchBmpH)

        self.padding = 4
        self.lastSearch = ""
        self.recentSearches = []
        self.inSearch = False

        self.fontSmall = wx.FontFromPixelSize((0,12),wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.BrowserSearchBox = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, (-1,-1), wx.TE_PROCESS_ENTER)
        self.BrowserSearchBox.Show(False)

        self.BrowserSearchBox.Bind(wx.EVT_TEXT_ENTER, self.OnBrowserSearchBoxEnter)
        self.BrowserSearchBox.Bind(wx.EVT_KILL_FOCUS, self.OnBrowserSearchBoxLostFocus)
        self.BrowserSearchBox.Bind(wx.EVT_KEY_DOWN, self.OnBrowserSearchBoxEsc)
        self.BrowserSearchBox.Bind(wx.EVT_TEXT, self.OnScheduleSearch)

        self.SetMinSize(size)
        self.shipBrowser = self.Parent
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.Bind(wx.EVT_SIZE, self.OnResize)


    def OnScheduleSearch(self, event):
        search = self.BrowserSearchBox.GetValue()
        if len(search) < 3 and len(search) >= 0:
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

    def ToggleSearchBox(self):
        if self.BrowserSearchBox.IsShown():
            self.BrowserSearchBox.Show(False)
        else:
            self.BrowserSearchBox.Show(True)
            self.BrowserSearchBox.ChangeValue("")
            self.BrowserSearchBox.SetFocus()

    def OnBrowserSearchBoxEnter(self, event):
        self.OnBrowserSearchBoxLostFocus(None)

    def OnBrowserSearchBoxLostFocus(self, event):
        self.lastSearch = self.BrowserSearchBox.GetValue()
        self.BrowserSearchBox.ChangeValue("")
        self.BrowserSearchBox.Show(False)

    def OnBrowserSearchBoxEsc(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.BrowserSearchBox.Show(False)
        else:
            event.Skip()


    def OnResize(self, event):
        self.Refresh()

    def ToggleEmptyGroupsView(self):
        if self.shipBrowser.filterShipsWithNoFits:
            self.shipBrowser.filterShipsWithNoFits = False
            self.btnSwitch.label = "Hide empty ship groups"
        else:
            self.shipBrowser.filterShipsWithNoFits = True
            self.btnSwitch.label = "Show empty ship groups"
        stage = self.shipBrowser.GetActiveStage()
        if stage == 2:
            categoryID = self.shipBrowser.GetStageData(stage)
            wx.PostEvent(self.shipBrowser,Stage2Selected(categoryID=categoryID, back = True))

    def ShowNewFitButton(self, show):
        self.btnNew.Show(show)
        self.Refresh()

    def ShowSwitchEmptyGroupsButton(self, show):
        self.btnSwitch.Show(show)
        self.Refresh()

    def OnNewFitting(self):
        stage = self.Parent.GetActiveStage()
        if stage == 3:
            shipID = self.Parent.GetStageData(stage)
            shipName = self.Parent.GetStage3ShipName()
            sFit = service.Fit.getInstance()
            fitID = sFit.newFit(shipID, "%s fit" %shipName)
            self.shipBrowser.fitIDMustEditName = fitID
            wx.PostEvent(self.Parent,Stage3Selected(shipID=shipID, back = True))
            wx.PostEvent(self.mainFrame, FitSelected(fitID=fitID))

    def OnHistoryReset(self):
        if self.shipBrowser.browseHist:
            self.shipBrowser.browseHist = []
            self.gotoStage(1,0)

    def OnHistoryBack(self):
        if len(self.shipBrowser.browseHist) > 0:
            stage,data = self.shipBrowser.browseHist.pop()
            self.gotoStage(stage,data)

    def AdjustChannels(self, bitmap):
        img = wx.ImageFromBitmap(bitmap)
        img = img.AdjustChannels(1.05,1.05,1.05,1)
        return wx.BitmapFromImage(img)

    def UpdateElementsPos(self, mdc):
        rect = self.GetRect()

        self.toolbarx = self.padding
        self.toolbary = (rect.height - self.toolbar.GetHeight()) / 2

        mdc.SetFont(self.fontSmall)

        wlabel,hlabel = mdc.GetTextExtent(self.toolbar.hoverLabel)

        self.thoverx = self.toolbar.GetWidth() + self.padding
        self.thovery = (rect.height - hlabel)/2
        self.thoverw = wlabel

        self.browserBoxX = self.thoverx
        bEditBoxWidth, bEditBoxHeight = self.BrowserSearchBox.GetSize()
        self.browserBoxY = (rect.height - bEditBoxHeight) / 2

        self.bEditBoxWidth = rect.width - self.browserBoxX - self.padding

    def DrawItem(self, mdc):
        rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        textColor = colorUtils.GetSuitableColor(windowColor, 1)
        sepColor = colorUtils.GetSuitableColor(windowColor, 0.2)

        mdc.SetTextForeground(textColor)

        self.UpdateElementsPos(mdc)
        self.BrowserSearchBox.SetPosition((self.browserBoxX, self.browserBoxY))
        self.BrowserSearchBox.SetSize(wx.Size(self.bEditBoxWidth, -1))

        self.toolbar.SetPosition((self.toolbarx, self.toolbary))
        mdc.SetFont(self.fontSmall)
        mdc.DrawText(self.toolbar.hoverLabel, self.thoverx, self.thovery)
        mdc.SetPen(wx.Pen(sepColor,1))
        mdc.DrawLine(0,rect.height - 1, rect.width, rect.height - 1)

    def RenderBackground(self):
        rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)

        sFactor = 0.1

        shipGroupsFilter = getattr(self.shipBrowser,"filterShipsWithNoFits", None)
        if shipGroupsFilter:
            sFactor = 0.15
            mFactor = 0.25
        else:
            mFactor = 0.2

        eFactor = 0.1

        if self.bkBitmap:
            if self.bkBitmap.eFactor == eFactor and self.bkBitmap.sFactor == sFactor and self.bkBitmap.mFactor == mFactor \
             and rect.width == self.bkBitmap.GetWidth() and rect.height == self.bkBitmap.GetHeight() :
                return
            else:
                del self.bkBitmap

        self.bkBitmap = drawUtils.RenderGradientBar(windowColor, rect.width, rect.height, sFactor, eFactor, mFactor, 2)

        self.bkBitmap.sFactor = sFactor
        self.bkBitmap.eFactor = eFactor
        self.bkBitmap.mFactor = mFactor


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

        self.racesFilter = {}

        self.showRacesFilterInStage2Only = True

        for race in self.RACE_ORDER:
            if race:
                self.racesFilter[race] = False

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.lpane = PFWidgetsContainer(self)
        layout = wx.VERTICAL

        self.navpanel = NavigationPanel(self)
        mainSizer.Add(self.navpanel, 0 , wx.EXPAND)
        self.raceselect = RaceSelector(self, layout = layout, animate = False)
        container = wx.BoxSizer(wx.VERTICAL if layout == wx.HORIZONTAL else wx.HORIZONTAL)

        if layout == wx.HORIZONTAL:
            container.Add(self.lpane,1,wx.EXPAND)
            container.Add(self.raceselect,0,wx.EXPAND)
        else:
            container.Add(self.raceselect,0,wx.EXPAND)
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
        self.navpanel.gotoStage(stage, stageData)

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

    def ToggleRacesFilter(self, race):
        if self.racesFilter[race]:
            self.racesFilter[race] = False
        else:
            self.racesFilter[race] = True

    def GetRaceFilterState(self, race):
        return self.racesFilter[race]

    def stage1(self, event):
        self._lastStage = self._activeStage
        self._activeStage = 1
        self.lastdata = 0

        self.navpanel.ShowNewFitButton(False)
        self.navpanel.ShowSwitchEmptyGroupsButton(False)

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
        self.raceselect.RebuildRaces(self.RACE_ORDER)
        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(False)
            self.Layout()

    RACE_ORDER = ["amarr", "caldari", "gallente", "minmatar", "ore", "serpentis", "angel", "blood", "sansha", "guristas", "jove", None]

    def raceNameKey(self, ship):
        return self.RACE_ORDER.index(ship.race), ship.name

    def stage2Callback(self, data):
        if self.GetActiveStage() != 2:
            return
        ships = list(data[1])
        sFit = service.Fit.getInstance()

        ships.sort(key=self.raceNameKey)
        racesList = []
        subRacesFilter = {}

        for ship in ships:
            if ship.race:
                if ship.race not in racesList:
                    racesList.append(ship.race)

        for race,state in self.racesFilter.iteritems():
            if race in racesList:
                subRacesFilter[race] = self.racesFilter[race]

        override = True
        for race, state in subRacesFilter.iteritems():
            if state:
                override = False
                break

        for ship in ships:
            fits = sFit.countFitsWithShip(ship.ID)
            filter = subRacesFilter[ship.race] if ship.race else True

            if override:
                filter = True

            if self.filterShipsWithNoFits:
                if fits>0:
                    if filter:
                        self.lpane.AddWidget(ShipItem(self.lpane, ship.ID, (ship.name, fits), ship.race))
            else:
                if filter:
                    self.lpane.AddWidget(ShipItem(self.lpane, ship.ID, (ship.name, fits), ship.race))

        self.raceselect.RebuildRaces(racesList)


        self.lpane.ShowLoading(False)

        self.lpane.RefreshList()

        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(True)
            self.Layout()

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

        self.navpanel.ShowNewFitButton(False)
        self.navpanel.ShowSwitchEmptyGroupsButton(True)

    def nameKey(self, info):
        return info[1]

    def stage3(self, event):

        self.lpane.ShowLoading(False)

        if event.back == 0:
            self.browseHist.append( (2,self._stage2Data) )
        elif event.back == -1:
            if len(self.navpanel.recentSearches)>0:
                self.browseHist.append((4, self.navpanel.lastSearch))

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
            self.navpanel.gotoStage(stage,data)
            return

        self.navpanel.ShowNewFitButton(True)
        self.navpanel.ShowSwitchEmptyGroupsButton(False)

        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(False)
            self.Layout()

        fitList.sort(key=self.nameKey)
        shipName = sMarket.getItem(shipID).name

        self._stage3ShipName = shipName
        self._stage3Data = shipID

        for ID, name, timestamp in fitList:
            self.lpane.AddWidget(FitItem(self.lpane, ID, (shipName, name, timestamp),shipID))

        self.lpane.RefreshList()
        self.lpane.Thaw()
        self.raceselect.RebuildRaces(self.RACE_ORDER)

    def searchStage(self, event):

        self.lpane.ShowLoading(False)

        self.navpanel.ShowNewFitButton(False)
        self.navpanel.ShowSwitchEmptyGroupsButton(False)

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

        self.raceselect.RebuildRaces(self.RACE_ORDER)

        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(False)
            self.Layout()


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

class CategoryItem(SFItem.SFBrowserItem):
    def __init__(self,parent, categoryID, fittingInfo, size = (0,16)):
        SFItem.SFBrowserItem.__init__(self,parent,size = size)

        if categoryID:
            self.shipBmp = bitmapLoader.getBitmap("ship_small","icons")
        else:
            self.shipBmp = wx.EmptyBitmap(16,16)

        self.dropShadowBitmap = drawUtils.CreateDropShadowBitmap(self.shipBmp, 0.2)

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
        mdc.DrawBitmap(self.dropShadowBitmap, self.shipBmpx + 1, self.shipBmpy + 1)
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

        self.raceDropShadowBmp = drawUtils.CreateDropShadowBitmap(self.raceBmp, 0.2)

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

        self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

        self.marketInstance = service.Market.getInstance()
        self.baseItem = self.marketInstance.getItem(self.shipID)

        #=======================================================================\
        # DISABLED - it will be added as an option in PREFERENCES

        self.animCount = 0

        # if self.shipBrowser.GetActiveStage() != 4 and self.shipBrowser.GetLastStage() !=2:
        #    self.Bind(wx.EVT_TIMER, self.OnTimer)
        #    self.animTimer.Start(self.animPeriod)
        # else:
        #    self.animCount = 0
        #=======================================================================


    def OnShowPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        contexts = []
        contexts.append(("baseShip", "Ship Basic"))
        menu = ContextMenu.getMenu(self.baseItem, *contexts)
        self.PopupMenu(menu, pos)

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

        mdc.DrawBitmap(self.raceDropShadowBmp, self.raceBmpx + 1, self.raceBmpy + 1)
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
            wx.PostEvent(self.shipBrowser,SearchSelected(text=self.shipBrowser.navpanel.lastSearch,back=True))
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

