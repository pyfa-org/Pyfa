# coding: utf-8

import re
import time

# noinspection PyPackageRequirements
import wx
# noinspection PyPackageRequirements
from wx.lib.buttons import GenBitmapButton

from service.fit import Fit
from service.market import Market
import gui.mainFrame
import gui.utils.fonts as fonts
import gui.globalEvents as GE
import gui.sfBrowserItem as SFItem
import gui.utils.colorUtils as colorUtils
import gui.utils.drawUtils as drawUtils
import gui.utils.animUtils as animUtils
import gui.utils.animEffects as animEffects
from gui.PFListPane import PFListPane
from gui.contextMenu import ContextMenu
from gui.bitmapLoader import BitmapLoader

FitRenamed, EVT_FIT_RENAMED = wx.lib.newevent.NewEvent()
FitSelected, EVT_FIT_SELECTED = wx.lib.newevent.NewEvent()
FitRemoved, EVT_FIT_REMOVED = wx.lib.newevent.NewEvent()

BoosterListUpdated, BOOSTER_LIST_UPDATED = wx.lib.newevent.NewEvent()

Stage1Selected, EVT_SB_STAGE1_SEL = wx.lib.newevent.NewEvent()
Stage2Selected, EVT_SB_STAGE2_SEL = wx.lib.newevent.NewEvent()
Stage3Selected, EVT_SB_STAGE3_SEL = wx.lib.newevent.NewEvent()
SearchSelected, EVT_SB_SEARCH_SEL = wx.lib.newevent.NewEvent()
ImportSelected, EVT_SB_IMPORT_SEL = wx.lib.newevent.NewEvent()


class PFWidgetsContainer(PFListPane):
    def __init__(self, parent):
        PFListPane.__init__(self, parent)

        self.anim = animUtils.LoadAnimation(self, label="", size=(100, 12))
        self.anim.Stop()
        self.anim.Show(False)

    def ShowLoading(self, mode=True):
        if mode:
            aweight, aheight = self.anim.GetSize()
            cweight, cheight = self.GetSize()
            ax = (cweight - aweight) / 2
            ay = (cheight - aheight) / 2
            self.anim.SetPosition((ax, ay))
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
    def __init__(self, parent, id=wx.ID_ANY, label="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 layout=wx.VERTICAL, animate=False):
        wx.Window.__init__(self, parent, id, pos=pos, size=size, style=style)

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
            self.buttonsBarPos = (4, 0)
        else:
            self.buttonsBarPos = (0, 4)

        self.buttonsPadding = 4

        if layout == wx.VERTICAL:
            self.bmpArrow = BitmapLoader.getBitmap("down-arrow2", "gui")
        else:
            self.bmpArrow = BitmapLoader.getBitmap("up-arrow2", "gui")

        # Make the bitmaps have the same color as window text

        sysTextColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)

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
        mx, my = event.GetPosition()

        location = self.HitTest(mx, my)
        if location != self.hoveredItem:
            self.hoveredItem = location
            self.Refresh()
            if location is not None:
                self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            else:
                self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

    def OnSizeUpdate(self, event):
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

        mx, my = event.GetPosition()

        toggle = self.HitTest(mx, my)

        if toggle is not None:
            self.Refresh()

            self.shipBrowser.ToggleRacesFilter(self.raceNames[toggle])

            stage = self.shipBrowser.GetActiveStage()

            if stage == 2:
                categoryID = self.shipBrowser.GetStageData(stage)
                wx.PostEvent(self.shipBrowser, Stage2Selected(categoryID=categoryID, back=True))
        event.Skip()

    def HitTest(self, mx, my):
        x, y = self.buttonsBarPos
        padding = self.buttonsPadding

        for bmp in self.raceBmps:
            if (x < mx < x + bmp.GetWidth()) and (y < my < y + bmp.GetHeight()):
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
                self.raceBmps.append(BitmapLoader.getBitmap("race_%s_small" % race, "gui"))
        self.raceNames = races
        self.CalcButtonsBarPos()
        self.Refresh()

    def OnBackgroundErase(self, event):
        pass

    def OnPaint(self, event):
        rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        # bkColor = colorUtils.GetSuitableColor(windowColor, 0.1)
        sepColor = colorUtils.GetSuitableColor(windowColor, 0.2)

        mdc = wx.BufferedPaintDC(self)

        bkBitmap = drawUtils.RenderGradientBar(windowColor, rect.width, rect.height, 0.1, 0.1, 0.2, 2)
        mdc.DrawBitmap(bkBitmap, 0, 0, True)

        x, y = self.buttonsBarPos

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
                    y += raceBmp.GetHeight() + self.buttonsPadding
                    mdc.SetPen(wx.Pen(sepColor, 1))
                    mdc.DrawLine(rect.width - 1, 0, rect.width - 1, rect.height)
                else:
                    mdc.DrawBitmap(dropShadow, x + 1, self.buttonsPadding + 1)
                    mdc.DrawBitmap(bmp, x, self.buttonsPadding)
                    x += raceBmp.GetWidth() + self.buttonsPadding
                    mdc.SetPen(wx.Pen(sepColor, 1))
                    mdc.DrawLine(0, 0, rect.width, 0)

        if self.direction < 1:
            if self.layout == wx.VERTICAL:
                mdc.DrawBitmap(self.bmpArrow, -2, (rect.height - self.bmpArrow.GetHeight()) / 2)
            else:
                mdc.SetPen(wx.Pen(sepColor, 1))
                mdc.DrawLine(0, 0, rect.width, 0)
                mdc.DrawBitmap(self.bmpArrow, (rect.width - self.bmpArrow.GetWidth()) / 2, -2)

    def OnTimer(self, event):
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
        self.SetMinSize(wx.Size(delta, -1) if self.layout == wx.VERTICAL else wx.Size(-1, delta))
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
    def __init__(self, parent, size=(-1, 24)):
        SFItem.SFBrowserItem.__init__(self, parent, size=size)

        self.rewBmpH = BitmapLoader.getBitmap("frewind_small", "gui")
        self.forwBmp = BitmapLoader.getBitmap("fforward_small", "gui")
        self.searchBmpH = BitmapLoader.getBitmap("fsearch_small", "gui")
        self.newBmpH = BitmapLoader.getBitmap("fit_add_small", "gui")
        self.resetBmpH = BitmapLoader.getBitmap("freset_small", "gui")
        self.switchBmpH = BitmapLoader.getBitmap("fit_switch_view_mode_small", "gui")

        switchImg = BitmapLoader.getImage("fit_switch_view_mode_small", "gui")
        switchImg = switchImg.AdjustChannels(1, 1, 1, 0.4)
        self.switchBmpD = wx.BitmapFromImage(switchImg)

        self.resetBmp = self.AdjustChannels(self.resetBmpH)
        self.rewBmp = self.AdjustChannels(self.rewBmpH)
        self.searchBmp = self.AdjustChannels(self.searchBmpH)
        self.switchBmp = self.AdjustChannels(self.switchBmpH)
        self.newBmp = self.AdjustChannels(self.newBmpH)

        self.toolbar.AddButton(self.resetBmp, "Ship groups", clickCallback=self.OnHistoryReset,
                               hoverBitmap=self.resetBmpH)
        self.toolbar.AddButton(self.rewBmp, "Back", clickCallback=self.OnHistoryBack, hoverBitmap=self.rewBmpH)
        self.btnNew = self.toolbar.AddButton(self.newBmp, "New fitting", clickCallback=self.OnNewFitting,
                                             hoverBitmap=self.newBmpH, show=False)
        self.btnSwitch = self.toolbar.AddButton(self.switchBmpD, "Hide empty ship groups",
                                                clickCallback=self.ToggleEmptyGroupsView, hoverBitmap=self.switchBmpH,
                                                show=False)

        modifier = "CTRL" if 'wxMac' not in wx.PlatformInfo else "CMD"
        self.toolbar.AddButton(self.searchBmp, "Search fittings ({}+F)".format(modifier), clickCallback=self.ToggleSearchBox,
                               hoverBitmap=self.searchBmpH)

        self.padding = 4
        self.lastSearch = ""
        self.recentSearches = []  # not used?
        self.inSearch = False

        self.fontSmall = wx.Font(fonts.SMALL, wx.SWISS, wx.NORMAL, wx.NORMAL)
        w, h = size
        self.BrowserSearchBox = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition,
                                            (-1, h - 2 if 'wxGTK' in wx.PlatformInfo else -1),
                                            wx.TE_PROCESS_ENTER | (wx.BORDER_NONE if 'wxGTK' in wx.PlatformInfo else 0))
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
        # Make sure we do not count wildcard as search symbol
        realsearch = search.replace("*", "")
        if len(realsearch) >= 3:
            self.lastSearch = search
            wx.PostEvent(self.shipBrowser, SearchSelected(text=search, back=False))

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
            self.btnSwitch.normalBmp = self.switchBmpD
        else:
            self.shipBrowser.filterShipsWithNoFits = True
            self.btnSwitch.label = "Show empty ship groups"
            self.btnSwitch.normalBmp = self.switchBmp

        stage = self.shipBrowser.GetActiveStage()

        if stage == 1:
            wx.PostEvent(self.shipBrowser, Stage1Selected())
        elif stage == 2:
            categoryID = self.shipBrowser.GetStageData(stage)
            wx.PostEvent(self.shipBrowser, Stage2Selected(categoryID=categoryID, back=True))

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
            sFit = Fit.getInstance()
            fitID = sFit.newFit(shipID, "%s fit" % shipName)
            self.shipBrowser.fitIDMustEditName = fitID
            wx.PostEvent(self.Parent, Stage3Selected(shipID=shipID))
            wx.PostEvent(self.mainFrame, FitSelected(fitID=fitID))

    def OnHistoryReset(self):
        if self.shipBrowser.browseHist:
            self.shipBrowser.browseHist = []
        self.gotoStage(1, 0)

    def OnHistoryBack(self):
        if len(self.shipBrowser.browseHist) > 0:
            stage, data = self.shipBrowser.browseHist.pop()
            self.gotoStage(stage, data)

    @staticmethod
    def AdjustChannels(bitmap):
        img = wx.ImageFromBitmap(bitmap)
        img = img.AdjustChannels(1.05, 1.05, 1.05, 1)
        return wx.BitmapFromImage(img)

    def UpdateElementsPos(self, mdc):
        rect = self.GetRect()

        self.toolbarx = self.padding
        self.toolbary = (rect.height - self.toolbar.GetHeight()) / 2

        mdc.SetFont(self.fontSmall)

        wlabel, hlabel = mdc.GetTextExtent(self.toolbar.hoverLabel)

        self.thoverx = self.toolbar.GetWidth() + self.padding
        self.thovery = (rect.height - hlabel) / 2
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
        mdc.SetPen(wx.Pen(sepColor, 1))
        mdc.DrawLine(0, rect.height - 1, rect.width, rect.height - 1)

    def RenderBackground(self):
        rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)

        sFactor = 0.1

        shipGroupsFilter = getattr(self.shipBrowser, "filterShipsWithNoFits", None)
        if shipGroupsFilter:
            sFactor = 0.15
            mFactor = 0.25
        else:
            mFactor = 0.2

        eFactor = 0.1

        if self.bkBitmap:
            if self.bkBitmap.eFactor == eFactor and self.bkBitmap.sFactor == sFactor and self.bkBitmap.mFactor == mFactor \
                    and rect.width == self.bkBitmap.GetWidth() and rect.height == self.bkBitmap.GetHeight():
                return
            else:
                del self.bkBitmap

        self.bkBitmap = drawUtils.RenderGradientBar(windowColor, rect.width, rect.height, sFactor, eFactor, mFactor, 2)

        self.bkBitmap.sFactor = sFactor
        self.bkBitmap.eFactor = eFactor
        self.bkBitmap.mFactor = mFactor

    def gotoStage(self, stage, data=None):
        if stage == 1:
            wx.PostEvent(self.Parent, Stage1Selected())
        elif stage == 2:
            wx.PostEvent(self.Parent, Stage2Selected(categoryID=data, back=True))
        elif stage == 3:
            wx.PostEvent(self.Parent, Stage3Selected(shipID=data))
        elif stage == 4:
            self.shipBrowser._activeStage = 4
            wx.PostEvent(self.Parent, SearchSelected(text=data, back=True))
        elif stage == 5:
            wx.PostEvent(self.Parent, ImportSelected(fits=data))
        else:
            wx.PostEvent(self.Parent, Stage1Selected())


class ShipBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=0)

        self._lastWidth = 0
        self._activeStage = 1
        self._lastStage = 0
        self.browseHist = []
        self.lastStage = (0, 0)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.categoryList = []
        self.categoryFitCache = {}

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
        layout = wx.HORIZONTAL

        self.navpanel = NavigationPanel(self)
        mainSizer.Add(self.navpanel, 0, wx.EXPAND)
        self.raceselect = RaceSelector(self, layout=layout, animate=False)
        container = wx.BoxSizer(wx.VERTICAL if layout == wx.HORIZONTAL else wx.HORIZONTAL)

        if layout == wx.HORIZONTAL:
            container.Add(self.lpane, 1, wx.EXPAND)
            container.Add(self.raceselect, 0, wx.EXPAND)
        else:
            container.Add(self.raceselect, 0, wx.EXPAND)
            container.Add(self.lpane, 1, wx.EXPAND)

        mainSizer.Add(container, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        self.Layout()
        self.Show()

        self.Bind(wx.EVT_SIZE, self.SizeRefreshList)
        self.Bind(EVT_SB_STAGE2_SEL, self.stage2)
        self.Bind(EVT_SB_STAGE1_SEL, self.stage1)
        self.Bind(EVT_SB_STAGE3_SEL, self.stage3)
        self.Bind(EVT_SB_SEARCH_SEL, self.searchStage)
        self.Bind(EVT_SB_IMPORT_SEL, self.importStage)

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
        if stage == 4:
            return self.navpanel.lastSearch
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
        self.browseHist = [(1, 0)]

        self.navpanel.ShowNewFitButton(False)
        self.navpanel.ShowSwitchEmptyGroupsButton(False)

        sMkt = Market.getInstance()
        sFit = Fit.getInstance()
        self.lpane.ShowLoading(False)

        self.lpane.Freeze()
        self.lpane.RemoveAllChildren()

        if len(self.categoryList) == 0:
            # set cache of category list
            self.categoryList = list(sMkt.getShipRoot())
            self.categoryList.sort(key=lambda _ship: _ship.name)

            # set map & cache of fittings per category
            for cat in self.categoryList:
                itemIDs = [x.ID for x in cat.items]
                num = sFit.countFitsWithShip(itemIDs)
                self.categoryFitCache[cat.ID] = num > 0

        for ship in self.categoryList:
            if self.filterShipsWithNoFits and not self.categoryFitCache[ship.ID]:
                continue
            else:
                self.lpane.AddWidget(CategoryItem(self.lpane, ship.ID, (ship.name, 0)))

        self.navpanel.ShowSwitchEmptyGroupsButton(True)

        self.lpane.RefreshList()
        self.lpane.Thaw()
        self.raceselect.RebuildRaces(self.RACE_ORDER)
        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(False)
            self.Layout()

    RACE_ORDER = [
        "amarr", "caldari", "gallente", "minmatar",
        "sisters", "ore",
        "serpentis", "angel", "blood", "sansha", "guristas", "mordu",
        "jove", "upwell", None
    ]

    def raceNameKey(self, ship):
        return self.RACE_ORDER.index(ship.race), ship.name

    def stage2Callback(self, data):
        if self.GetActiveStage() != 2:
            return

        categoryID = self._stage2Data
        ships = list(data[1])
        sFit = Fit.getInstance()

        ships.sort(key=self.raceNameKey)
        racesList = []
        subRacesFilter = {}
        t_fits = 0  # total number of fits in this category

        for ship in ships:
            if ship.race:
                if ship.race not in racesList:
                    racesList.append(ship.race)

        for race, state in self.racesFilter.iteritems():
            if race in racesList:
                subRacesFilter[race] = self.racesFilter[race]

        override = True
        for race, state in subRacesFilter.iteritems():
            if state:
                override = False
                break

        for ship in ships:
            fits = sFit.countFitsWithShip(ship.ID)
            t_fits += fits
            filter_ = subRacesFilter[ship.race] if ship.race else True
            if override:
                filter_ = True

            shipTrait = ship.traits.traitText if (ship.traits is not None) else ""  # empty string if no traits

            if self.filterShipsWithNoFits:
                if fits > 0:
                    if filter_:
                        self.lpane.AddWidget(ShipItem(self.lpane, ship.ID, (ship.name, shipTrait, fits), ship.race))
            else:
                if filter_:
                    self.lpane.AddWidget(ShipItem(self.lpane, ship.ID, (ship.name, shipTrait, fits), ship.race))

        self.raceselect.RebuildRaces(racesList)

        # refresh category cache
        if t_fits == 0:
            self.categoryFitCache[categoryID] = False
        else:
            self.categoryFitCache[categoryID] = True

        self.lpane.ShowLoading(False)

        self.lpane.RefreshList()

        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(True)
            self.Layout()

    def stage2(self, event):
        # back = event.back
        # if not back:
        #    self.browseHist.append( (1,0) )

        self._lastStage = self._activeStage
        self._activeStage = 2
        categoryID = event.categoryID
        self.lastdata = categoryID

        self.lpane.ShowLoading()

        self.lpane.RemoveAllChildren()

        sMkt = Market.getInstance()
        sMkt.getShipListDelayed(categoryID, self.stage2Callback)

        self._stage2Data = categoryID

        self.navpanel.ShowNewFitButton(False)
        self.navpanel.ShowSwitchEmptyGroupsButton(True)

    @staticmethod
    def nameKey(info):
        return info[1]

    def stage3(self, event):

        self.lpane.ShowLoading(False)

        # If back is False, do not append to history. This could be us calling
        # the stage from previous history, creating / copying fit, etc.
        # We also have to use conditional for search stage since it's last data
        # is kept elsewhere
        if getattr(event, "back", False):
            if self._activeStage == 4 and self.navpanel.lastSearch != "":
                self.browseHist.append((4, self.navpanel.lastSearch))
            else:
                self.browseHist.append((self._activeStage, self.lastdata))

        shipID = event.shipID
        self.lastdata = shipID
        self._lastStage = self._activeStage
        self._activeStage = 3

        sFit = Fit.getInstance()
        sMkt = Market.getInstance()

        ship = sMkt.getItem(shipID)
        categoryID = ship.group.ID

        self.lpane.Freeze()
        self.lpane.RemoveAllChildren()
        fitList = sFit.getFitsWithShip(shipID)

        if len(fitList) == 0:
            stage, data = self.browseHist.pop()
            self.lpane.Thaw()
            self.navpanel.gotoStage(stage, data)
            return

        self.categoryFitCache[categoryID] = True

        self.navpanel.ShowNewFitButton(True)
        self.navpanel.ShowSwitchEmptyGroupsButton(False)

        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(False)
            self.Layout()

        fitList.sort(key=self.nameKey)
        shipName = ship.name

        self._stage3ShipName = shipName
        self._stage3Data = shipID

        shipTrait = ship.traits.traitText if (ship.traits is not None) else ""  # empty string if no traits

        for ID, name, booster, timestamp in fitList:
            self.lpane.AddWidget(FitItem(self.lpane, ID, (shipName, shipTrait, name, booster, timestamp), shipID))

        self.lpane.RefreshList()
        self.lpane.Thaw()
        self.raceselect.RebuildRaces(self.RACE_ORDER)

    def searchStage(self, event):

        self.lpane.ShowLoading(False)

        self.navpanel.ShowNewFitButton(False)
        self.navpanel.ShowSwitchEmptyGroupsButton(False)

        if not event.back:
            if self._activeStage != 4:
                if len(self.browseHist) > 0:
                    self.browseHist.append((self._activeStage, self.lastdata))
                else:
                    self.browseHist.append((1, 0))
            self._lastStage = self._activeStage
            self._activeStage = 4

        sMkt = Market.getInstance()
        sFit = Fit.getInstance()
        query = event.text

        self.lpane.Freeze()

        self.lpane.RemoveAllChildren()
        if query:
            ships = sMkt.searchShips(query)
            fitList = sFit.searchFits(query)

            for ship in ships:
                shipTrait = ship.traits.traitText if (ship.traits is not None) else ""  # empty string if no traits

                self.lpane.AddWidget(
                    ShipItem(self.lpane, ship.ID, (ship.name, shipTrait, len(sFit.getFitsWithShip(ship.ID))),
                             ship.race))

            for ID, name, shipID, shipName, booster, timestamp in fitList:
                ship = sMkt.getItem(shipID)
                shipTrait = ship.traits.traitText if (ship.traits is not None) else ""  # empty string if no traits

                self.lpane.AddWidget(FitItem(self.lpane, ID, (shipName, shipTrait, name, booster, timestamp), shipID))
            if len(ships) == 0 and len(fitList) == 0:
                self.lpane.AddWidget(PFStaticText(self.lpane, label=u"No matching results."))
            self.lpane.RefreshList(doFocus=False)
        self.lpane.Thaw()

        self.raceselect.RebuildRaces(self.RACE_ORDER)

        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(False)
            self.Layout()

    def importStage(self, event):
        self.lpane.ShowLoading(False)

        self.navpanel.ShowNewFitButton(False)
        self.navpanel.ShowSwitchEmptyGroupsButton(False)

        if getattr(event, "back", False):
            self.browseHist.append((self._activeStage, self.lastdata))

        self._lastStage = self._activeStage
        self._activeStage = 5

        fits = event.fits

        # sort by ship name, then fit name
        fits.sort(key=lambda _fit: (_fit.ship.item.name, _fit.name))

        self.lastdata = fits
        self.lpane.Freeze()
        self.lpane.RemoveAllChildren()

        if fits:
            for fit in fits:
                shipTrait = fit.ship.item.traits.traitText if (fit.ship.item.traits is not None) else ""
                # empty string if no traits

                self.lpane.AddWidget(FitItem(
                    self.lpane,
                    fit.ID,
                    (
                        fit.ship.item.name,
                        shipTrait,
                        fit.name,
                        fit.booster,
                        fit.timestamp,
                    ),
                    fit.ship.item.ID,
                ))
            self.lpane.RefreshList(doFocus=False)
        self.lpane.Thaw()

        self.raceselect.RebuildRaces(self.RACE_ORDER)

        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(False)
            self.Layout()


class PFStaticText(wx.Panel):
    def __init__(self, parent, label=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=parent.GetSize())
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, wx.ID_ANY, label, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        text.Wrap(-1)
        mainSizer.Add(text, 1, wx.ALL, 10)
        self.SetSizer(mainSizer)
        self.Layout()

    @staticmethod
    def GetType():
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
    def __init__(self, parent, categoryID, fittingInfo, size=(0, 16)):
        SFItem.SFBrowserItem.__init__(self, parent, size=size)

        if categoryID:
            self.shipBmp = BitmapLoader.getBitmap("ship_small", "gui")
        else:
            self.shipBmp = wx.EmptyBitmap(16, 16)

        self.dropShadowBitmap = drawUtils.CreateDropShadowBitmap(self.shipBmp, 0.2)

        self.categoryID = categoryID
        self.fittingInfo = fittingInfo
        self.shipBrowser = self.Parent.Parent

        self.padding = 4

        self.fontBig = wx.Font(fonts.BIG, wx.SWISS, wx.NORMAL, wx.NORMAL)

        self.animTimerId = wx.NewId()

        self.animTimer = wx.Timer(self, self.animTimerId)
        self.animStep = 0
        self.animPeriod = 10
        self.animDuration = 100

        self.Bind(wx.EVT_TIMER, self.OnTimer)

        # =====================================================================
        # Disabled - it will be added as an option to Preferences
        self.animCount = 0
        # self.animTimer.Start(self.animPeriod)
        # =====================================================================

    def OnTimer(self, event):
        step = self.OUT_QUAD(self.animStep, 0, 10, self.animDuration)
        self.animCount = 10 - step
        self.animStep += self.animPeriod
        if self.animStep > self.animDuration or self.animCount < 0:
            self.animCount = 0
            self.animTimer.Stop()
        self.Refresh()

    @staticmethod
    def OUT_QUAD(t, b, c, d):
        t = float(t)
        b = float(b)
        c = float(c)
        d = float(d)

        t /= d

        return -c * t * (t - 2) + b

    def GetType(self):
        return 1

    def MouseLeftUp(self, event):

        categoryID = self.categoryID
        wx.PostEvent(self.shipBrowser, Stage2Selected(categoryID=categoryID, back=False))

    def UpdateElementsPos(self, mdc):
        rect = self.GetRect()
        self.shipBmpx = self.padding
        self.shipBmpy = (rect.height - self.shipBmp.GetWidth()) / 2

        self.shipBmpx -= self.animCount

        mdc.SetFont(self.fontBig)
        categoryName, fittings = self.fittingInfo
        wtext, htext = mdc.GetTextExtent(categoryName)

        self.catx = self.shipBmpx + self.shipBmp.GetWidth() + self.padding
        self.caty = (rect.height - htext) / 2

    def DrawItem(self, mdc):
        # rect = self.GetRect()
        self.UpdateElementsPos(mdc)

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        textColor = colorUtils.GetSuitableColor(windowColor, 1)

        mdc.SetTextForeground(textColor)
        mdc.DrawBitmap(self.dropShadowBitmap, self.shipBmpx + 1, self.shipBmpy + 1)
        mdc.DrawBitmap(self.shipBmp, self.shipBmpx, self.shipBmpy, 0)

        mdc.SetFont(self.fontBig)

        categoryName, fittings = self.fittingInfo

        mdc.DrawText(categoryName, self.catx, self.caty)


# =============================================================================
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
# =============================================================================


class ShipItem(SFItem.SFBrowserItem):
    def __init__(self, parent, shipID=None, shipFittingInfo=("Test", "TestTrait", 2), itemData=None,
                 id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=(0, 40), style=0):
        SFItem.SFBrowserItem.__init__(self, parent, size=size)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self._itemData = itemData

        self.shipRace = itemData

        self.shipID = shipID

        self.fontBig = wx.Font(fonts.BIG, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.fontNormal = wx.Font(fonts.NORMAL, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.fontSmall = wx.Font(fonts.SMALL, wx.SWISS, wx.NORMAL, wx.NORMAL)

        self.shipBmp = None
        if shipID:
            self.shipBmp = BitmapLoader.getBitmap(str(shipID), "renders")
        if not self.shipBmp:
            self.shipBmp = BitmapLoader.getBitmap("ship_no_image_big", "gui")

        self.shipFittingInfo = shipFittingInfo
        self.shipName, self.shipTrait, self.shipFits = shipFittingInfo
        self.shipTrait = re.sub("<.*?>", " ", self.shipTrait)

        self.newBmp = BitmapLoader.getBitmap("fit_add_small", "gui")
        self.acceptBmp = BitmapLoader.getBitmap("faccept_small", "gui")

        self.shipEffBk = BitmapLoader.getBitmap("fshipbk_big", "gui")

        img = wx.ImageFromBitmap(self.shipEffBk)
        img = img.Mirror(False)
        self.shipEffBkMirrored = wx.BitmapFromImage(img)

        self.raceBmp = BitmapLoader.getBitmap("race_%s_small" % self.shipRace, "gui")

        if not self.raceBmp:
            self.raceBmp = BitmapLoader.getBitmap("fit_delete_small", "gui")

        self.raceDropShadowBmp = drawUtils.CreateDropShadowBitmap(self.raceBmp, 0.2)

        self.SetToolTip(wx.ToolTip(self.shipTrait))

        self.shipBrowser = self.Parent.Parent

        self.editWidth = 150
        self.padding = 4

        self.tcFitName = wx.TextCtrl(self, wx.ID_ANY, "%s fit" % self.shipName, wx.DefaultPosition, (120, -1),
                                     wx.TE_PROCESS_ENTER)
        self.tcFitName.Show(False)

        self.newBtn = self.toolbar.AddButton(self.newBmp, "New", self.newBtnCB)

        self.tcFitName.Bind(wx.EVT_TEXT_ENTER, self.createNewFit)
        self.tcFitName.Bind(wx.EVT_KILL_FOCUS, self.editLostFocus)
        self.tcFitName.Bind(wx.EVT_KEY_DOWN, self.editCheckEsc)

        self.animTimerId = wx.NewId()

        self.animTimer = wx.Timer(self, self.animTimerId)
        self.animStep = 0
        self.animPeriod = 10
        self.animDuration = 100

        self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

        self.marketInstance = Market.getInstance()
        self.baseItem = self.marketInstance.getItem(self.shipID)

        # =====================================================================
        # DISABLED - it will be added as an option in PREFERENCES

        self.animCount = 0

        # if self.shipBrowser.GetActiveStage() != 4 and self.shipBrowser.GetLastStage() !=2:
        #    self.Bind(wx.EVT_TIMER, self.OnTimer)
        #    self.animTimer.Start(self.animPeriod)
        # else:
        #    self.animCount = 0
        # =====================================================================

    def OnShowPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        contexts = [("baseShip", "Ship Basic")]
        menu = ContextMenu.getMenu(self.baseItem, *contexts)
        self.PopupMenu(menu, pos)

    def OnTimer(self, event):
        step = self.OUT_QUAD(self.animStep, 0, 10, self.animDuration)
        self.animCount = 10 - step
        self.animStep += self.animPeriod
        if self.animStep > self.animDuration or self.animCount < 0:
            self.animCount = 0
            self.animTimer.Stop()
        self.Refresh()

    @staticmethod
    def OUT_QUAD(t, b, c, d):
        t = float(t)
        b = float(b)
        c = float(c)
        d = float(d)

        t /= d

        return -c * t * (t - 2) + b

    def GetType(self):
        return 2

    def MouseLeftUp(self, event):
        if self.tcFitName.IsShown():
            self.tcFitName.Show(False)
            self.newBtn.SetBitmap(self.newBmp)
            self.Refresh()
        else:
            shipName, shipTrait, fittings = self.shipFittingInfo
            if fittings > 0:
                wx.PostEvent(self.shipBrowser, Stage3Selected(shipID=self.shipID, back=True))
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

        sFit = Fit.getInstance()
        fitID = sFit.newFit(self.shipID, self.tcFitName.GetValue())

        wx.PostEvent(self.shipBrowser, Stage3Selected(shipID=self.shipID, back=False))
        wx.PostEvent(self.mainFrame, FitSelected(fitID=fitID))

    def UpdateElementsPos(self, mdc):
        rect = self.GetRect()

        self.toolbarx = rect.width - self.toolbar.GetWidth() - self.padding
        self.toolbary = (rect.height - self.toolbar.GetHeight()) / 2

        self.toolbarx += self.animCount

        self.shipEffx = self.padding + (rect.height - self.shipEffBk.GetWidth()) / 2
        self.shipEffy = (rect.height - self.shipEffBk.GetHeight()) / 2

        self.shipEffx -= self.animCount

        self.shipBmpx = self.padding + (rect.height - self.shipBmp.GetWidth()) / 2
        self.shipBmpy = (rect.height - self.shipBmp.GetHeight()) / 2

        self.shipBmpx -= self.animCount

        self.raceBmpx = self.shipEffx + self.shipEffBk.GetWidth() + self.padding
        self.raceBmpy = (rect.height - self.raceBmp.GetHeight()) / 2

        self.textStartx = self.raceBmpx + self.raceBmp.GetWidth() + self.padding

        self.shipNamey = (rect.height - self.shipBmp.GetHeight()) / 2

        shipName, shipTrait, fittings = self.shipFittingInfo

        mdc.SetFont(self.fontBig)
        wtext, htext = mdc.GetTextExtent(shipName)

        self.fittingsy = self.shipNamey + htext

        mdc.SetFont(self.fontSmall)

        wlabel, hlabel = mdc.GetTextExtent(self.toolbar.hoverLabel)

        self.thoverx = self.toolbarx - self.padding - wlabel
        self.thovery = (rect.height - hlabel) / 2
        self.thoverw = wlabel

    def DrawItem(self, mdc):
        # rect = self.GetRect()

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
        mdc.DrawBitmap(self.raceBmp, self.raceBmpx, self.raceBmpy)

        shipName, shipTrait, fittings = self.shipFittingInfo

        if fittings < 1:
            fformat = "No fits"
        elif fittings == 1:
            fformat = "%d fit"
        else:
            fformat = "%d fits"

        mdc.SetFont(self.fontNormal)
        mdc.DrawText(fformat % fittings if fittings > 0 else fformat, self.textStartx, self.fittingsy)

        mdc.SetFont(self.fontSmall)
        mdc.DrawText(self.toolbar.hoverLabel, self.thoverx, self.thovery)

        mdc.SetFont(self.fontBig)

        psname = drawUtils.GetPartialText(mdc, shipName,
                                          self.toolbarx - self.textStartx - self.padding * 2 - self.thoverw)

        mdc.DrawText(psname, self.textStartx, self.shipNamey)

        if self.tcFitName.IsShown():
            self.AdjustControlSizePos(self.tcFitName, self.textStartx, self.toolbarx - self.editWidth - self.padding)

    def AdjustControlSizePos(self, editCtl, start, end):
        fnEditSize = editCtl.GetSize()
        wSize = self.GetSize()
        fnEditPosX = end
        fnEditPosY = (wSize.height - fnEditSize.height) / 2
        if fnEditPosX < start:
            editCtl.SetSize((self.editWidth + fnEditPosX - start, -1))
            editCtl.SetPosition((start, fnEditPosY))
        else:
            editCtl.SetSize((self.editWidth, -1))
            editCtl.SetPosition((fnEditPosX, fnEditPosY))


class PFBitmapFrame(wx.Frame):
    def __init__(self, parent, pos, bitmap):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=pos, size=wx.DefaultSize,
                          style=wx.NO_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)
        img = bitmap.ConvertToImage()
        img = img.ConvertToGreyscale()
        bitmap = wx.BitmapFromImage(img)
        self.bitmap = bitmap
        self.SetSize((bitmap.GetWidth(), bitmap.GetHeight()))
        self.Bind(wx.EVT_PAINT, self.OnWindowPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnWindowEraseBk)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.timer = wx.Timer(self, wx.ID_ANY)
        self.direction = 1
        self.transp = 0
        self.SetSize((bitmap.GetWidth(), bitmap.GetHeight()))

        self.SetTransparent(0)
        self.Refresh()

    def OnTimer(self, event):
        self.transp += 20 * self.direction
        if self.transp > 200:
            self.transp = 200
            self.timer.Stop()
        if self.transp < 0:
            self.transp = 0
            self.timer.Stop()
            wx.Frame.Show(self, False)
            self.Destroy()
            return
        self.SetTransparent(self.transp)

    def Show(self, showWnd=True):
        if showWnd:
            wx.Frame.Show(self, showWnd)
            self.Parent.SetFocus()
            self.direction = 1
            self.timer.Start(5)
        else:
            self.direction = -1
            self.timer.Start(5)

    def OnWindowEraseBk(self, event):
        pass

    def OnWindowPaint(self, event):
        rect = self.GetRect()
        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        mdc.DrawBitmap(self.bitmap, 0, 0)
        mdc.SetPen(wx.Pen("#000000", width=1))
        mdc.SetBrush(wx.TRANSPARENT_BRUSH)
        mdc.DrawRectangle(0, 0, rect.width, rect.height)


class FitItem(SFItem.SFBrowserItem):
    def __init__(self, parent, fitID=None, shipFittingInfo=("Test", "TestTrait", "cnc's avatar", 0, 0), shipID=None,
                 itemData=None,
                 id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=(0, 40), style=0):

        # =====================================================================
        # animCount should be 10 if we enable animation in Preferences
        # =====================================================================

        self.animCount = 0
        self.selectedDelta = 0

        SFItem.SFBrowserItem.__init__(self, parent, size=size)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self._itemData = itemData

        self.fitID = fitID

        self.shipID = shipID

        self.shipBrowser = self.Parent.Parent

        self.shipBmp = None

        self.deleted = False

        if shipID:
            self.shipBmp = BitmapLoader.getBitmap(str(shipID), "renders")

        if not self.shipBmp:
            self.shipBmp = BitmapLoader.getBitmap("ship_no_image_big", "gui")

        self.shipFittingInfo = shipFittingInfo
        self.shipName, self.shipTrait, self.fitName, self.fitBooster, self.timestamp = shipFittingInfo
        self.shipTrait = re.sub("<.*?>", " ", self.shipTrait)
        # see GH issue #62

        # Disabling this due to change in gang boosts Nov 2016
        # if self.fitBooster is None: self.fitBooster = False
        self.fitBooster = False

        self.boosterBmp = BitmapLoader.getBitmap("fleet_fc_small", "gui")
        self.copyBmp = BitmapLoader.getBitmap("fit_add_small", "gui")
        self.renameBmp = BitmapLoader.getBitmap("fit_rename_small", "gui")
        self.deleteBmp = BitmapLoader.getBitmap("fit_delete_small", "gui")
        self.acceptBmp = BitmapLoader.getBitmap("faccept_small", "gui")
        self.shipEffBk = BitmapLoader.getBitmap("fshipbk_big", "gui")

        img = wx.ImageFromBitmap(self.shipEffBk)
        img = img.Mirror(False)
        self.shipEffBkMirrored = wx.BitmapFromImage(img)

        self.dragTLFBmp = None

        self.bkBitmap = None
        if self.shipTrait != "":  # show no tooltip if no trait available
            self.SetToolTip(wx.ToolTip(u'{}\n{}\n{}'.format(self.shipName, u'─' * 20, self.shipTrait)))
        self.padding = 4
        self.editWidth = 150

        self.dragging = False
        self.dragged = False
        self.dragMotionTrail = 5
        self.dragMotionTrigger = self.dragMotionTrail
        self.dragWindow = None

        self.fontBig = wx.Font(fonts.BIG, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.fontNormal = wx.Font(fonts.NORMAL, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.fontSmall = wx.Font(fonts.SMALL, wx.SWISS, wx.NORMAL, wx.NORMAL)

        self.SetDraggable()

        self.boosterBtn = self.toolbar.AddButton(self.boosterBmp, "Booster", show=self.fitBooster)
        self.toolbar.AddButton(self.copyBmp, "Copy", self.copyBtnCB)
        self.renameBtn = self.toolbar.AddButton(self.renameBmp, "Rename", self.renameBtnCB)
        self.toolbar.AddButton(self.deleteBmp, "Delete", self.deleteBtnCB)

        self.tcFitName = wx.TextCtrl(self, wx.ID_ANY, "%s" % self.fitName, wx.DefaultPosition, (self.editWidth, -1),
                                     wx.TE_PROCESS_ENTER)

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
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.OnMouseCaptureLost)

        self.animTimerId = wx.NewId()
        self.animTimer = wx.Timer(self, self.animTimerId)
        self.animStep = 0
        self.animPeriod = 10
        self.animDuration = 100

        self.maxDelta = 48

        self.Bind(wx.EVT_TIMER, self.OnTimer)

        # =====================================================================
        # DISABLED - it will be added as an option in PREFERENCES

        # if self.shipBrowser.GetActiveStage() != 4 and self.shipBrowser.GetLastStage() !=3:
        #    self.animTimer.Start(self.animPeriod)
        # else:
        #    self.animCount = 0
        # =====================================================================

        self.selTimerID = wx.NewId()

        self.selTimer = wx.Timer(self, self.selTimerID)
        self.selTimer.Start(100)

        self.Bind(wx.EVT_RIGHT_UP, self.OnContextMenu)

    def OnToggleBooster(self, event):
        sFit = Fit.getInstance()
        sFit.toggleBoostFit(self.fitID)
        self.fitBooster = not self.fitBooster
        self.boosterBtn.Show(self.fitBooster)
        self.Refresh()
        wx.PostEvent(self.mainFrame, BoosterListUpdated())
        event.Skip()

    def OnProjectToFit(self, event):
        activeFit = self.mainFrame.getActiveFit()
        if activeFit:
            sFit = Fit.getInstance()
            projectedFit = sFit.getFit(self.fitID)
            sFit.project(activeFit, projectedFit)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=activeFit))
            self.mainFrame.additionsPane.select("Projected")

    def OnAddCommandFit(self, event):
        activeFit = self.mainFrame.getActiveFit()
        if activeFit:
            sFit = Fit.getInstance()
            commandFit = sFit.getFit(self.fitID)
            sFit.addCommandFit(activeFit, commandFit)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=activeFit))
            self.mainFrame.additionsPane.select("Command")

    def OnMouseCaptureLost(self, event):
        """ Destroy drag information (GH issue #479)"""
        if self.dragging and self.dragged:
            self.dragging = False
            self.dragged = False
            if self.HasCapture():
                self.ReleaseMouse()
            self.dragWindow.Show(False)
            self.dragWindow = None

    def OnContextMenu(self, event):
        """ Handles context menu for fit. Dragging is handled by MouseLeftUp() """
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.mainFrame.getActiveFit())

        if not fit:
            return

        pos = wx.GetMousePosition()
        pos = self.ScreenToClient(pos)

        # Even though we may not select a booster, automatically set this so that the fleet pane knows which fit we're applying
        self.mainFrame.additionsPane.gangPage.draggedFitID = self.fitID

        menu = wx.Menu()
        # toggleItem = menu.Append(wx.ID_ANY, "Booster Fit", kind=wx.ITEM_CHECK)
        # menu.Check(toggleItem.GetId(), self.fitBooster)
        # self.Bind(wx.EVT_MENU, self.OnToggleBooster, toggleItem)

        # if fit and not fit.isStructure:
        #     # If there is an active fit, get menu for setting individual boosters
        #     menu.AppendSeparator()
        #     boosterMenu = self.mainFrame.additionsPane.gangPage.buildBoostermenu()
        #     menu.AppendSubMenu(boosterMenu, 'Set Booster')

        if fit:
            projectedItem = menu.Append(wx.ID_ANY, "Project onto Active Fit")
            self.Bind(wx.EVT_MENU, self.OnProjectToFit, projectedItem)

            commandItem = menu.Append(wx.ID_ANY, "Add Command Booster")
            self.Bind(wx.EVT_MENU, self.OnAddCommandFit, commandItem)

        self.PopupMenu(menu, pos)

        event.Skip()

    def GetType(self):
        return 3

    def OnTimer(self, event):

        if self.selTimerID == event.GetId():
            ctimestamp = time.time()
            interval = 5
            if ctimestamp < self.timestamp + interval:
                delta = (ctimestamp - self.timestamp) / interval
                self.selectedDelta = self.CalculateDelta(0x0, self.maxDelta, delta)
                self.Refresh()
            else:
                self.selectedDelta = self.maxDelta
                self.selTimer.Stop()

        if self.animTimerId == event.GetId():
            step = self.OUT_QUAD(self.animStep, 0, 10, self.animDuration)
            self.animCount = 10 - step
            self.animStep += self.animPeriod
            if self.animStep > self.animDuration or self.animCount < 0:
                self.animCount = 0
                self.animTimer.Stop()
            self.Refresh()

    @staticmethod
    def CalculateDelta(start, end, delta):
        return start + (end - start) * delta

    @staticmethod
    def OUT_QUAD(t, b, c, d):
        t = float(t)
        b = float(b)
        c = float(c)
        d = float(d)

        t /= d

        return -c * t * (t - 2) + b

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
        sFit = Fit.getInstance()
        fitID = sFit.copyFit(self.fitID)
        self.shipBrowser.fitIDMustEditName = fitID
        wx.PostEvent(self.shipBrowser, Stage3Selected(shipID=self.shipID))
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
        sFit = Fit.getInstance()
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

        # to prevent accidental deletion, give dialog confirmation unless shift is depressed
        if wx.GetMouseState().ShiftDown() or wx.GetMouseState().MiddleDown():
            self.deleteFit()
        else:
            dlg = wx.MessageDialog(
                self,
                "Do you really want to delete this fit?",
                "Confirm Delete",
                wx.YES | wx.NO | wx.ICON_QUESTION
            )

            if dlg.ShowModal() == wx.ID_YES:
                self.deleteFit()

    def deleteFit(self, event=None):
        if self.deleted:
            return
        else:
            self.deleted = True

        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)

        sFit.deleteFit(self.fitID)

        if self.shipBrowser.GetActiveStage() == 5:
            if fit in self.shipBrowser.lastdata:  # remove fit from import cache
                self.shipBrowser.lastdata.remove(fit)
            wx.PostEvent(self.shipBrowser, ImportSelected(fits=self.shipBrowser.lastdata))
        elif self.shipBrowser.GetActiveStage() == 4:
            wx.PostEvent(self.shipBrowser, SearchSelected(text=self.shipBrowser.navpanel.lastSearch, back=True))
        else:
            wx.PostEvent(self.shipBrowser, Stage3Selected(shipID=self.shipID))

        wx.PostEvent(self.mainFrame, FitRemoved(fitID=self.fitID))

    def MouseLeftUp(self, event):
        if self.dragging and self.dragged:
            self.OnMouseCaptureLost(event)

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
                    if not self.HasCapture():
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

        self.toolbarx += self.animCount

        self.shipEffx = self.padding + (rect.height - self.shipEffBk.GetWidth()) / 2
        self.shipEffy = (rect.height - self.shipEffBk.GetHeight()) / 2

        self.shipEffx -= self.animCount

        self.shipBmpx = self.padding + (rect.height - self.shipBmp.GetWidth()) / 2
        self.shipBmpy = (rect.height - self.shipBmp.GetHeight()) / 2

        self.shipBmpx -= self.animCount

        self.textStartx = self.shipEffx + self.shipEffBk.GetWidth() + self.padding

        self.fitNamey = (rect.height - self.shipBmp.GetHeight()) / 2

        mdc.SetFont(self.fontBig)
        wtext, htext = mdc.GetTextExtent(self.fitName)

        self.timestampy = self.fitNamey + htext

        mdc.SetFont(self.fontSmall)

        wlabel, hlabel = mdc.GetTextExtent(self.toolbar.hoverLabel)

        self.thoverx = self.toolbarx - self.padding - wlabel
        self.thovery = (rect.height - hlabel) / 2
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

        mdc.SetFont(self.fontNormal)

        fitDate = time.localtime(self.timestamp)
        fitLocalDate = "%d/%02d/%02d %02d:%02d" % (fitDate[0], fitDate[1], fitDate[2], fitDate[3], fitDate[4])
        pfdate = drawUtils.GetPartialText(mdc, fitLocalDate,
                                          self.toolbarx - self.textStartx - self.padding * 2 - self.thoverw)

        mdc.DrawText(pfdate, self.textStartx, self.timestampy)

        mdc.SetFont(self.fontSmall)
        mdc.DrawText(self.toolbar.hoverLabel, self.thoverx, self.thovery)

        mdc.SetFont(self.fontBig)

        psname = drawUtils.GetPartialText(mdc, self.fitName,
                                          self.toolbarx - self.textStartx - self.padding * 2 - self.thoverw)

        mdc.DrawText(psname, self.textStartx, self.fitNamey)

        if self.tcFitName.IsShown():
            self.AdjustControlSizePos(self.tcFitName, self.textStartx, self.toolbarx - self.editWidth - self.padding)

        tdc = wx.MemoryDC()
        self.dragTLFBmp = wx.EmptyBitmap((self.toolbarx if self.toolbarx < 200 else 200), rect.height, 24)
        tdc.SelectObject(self.dragTLFBmp)
        tdc.Blit(0, 0, (self.toolbarx if self.toolbarx < 200 else 200), rect.height, mdc, 0, 0, wx.COPY)
        tdc.SelectObject(wx.NullBitmap)

    def AdjustControlSizePos(self, editCtl, start, end):
        fnEditSize = editCtl.GetSize()
        wSize = self.GetSize()
        fnEditPosX = end
        fnEditPosY = (wSize.height - fnEditSize.height) / 2
        if fnEditPosX < start:
            editCtl.SetSize((self.editWidth + fnEditPosX - start, -1))
            editCtl.SetPosition((start, fnEditPosY))
        else:
            editCtl.SetSize((self.editWidth, -1))
            editCtl.SetPosition((fnEditPosX, fnEditPosY))

    def GetState(self):
        activeFitID = self.mainFrame.getActiveFit()

        if self.highlighted and not activeFitID == self.fitID:
            state = SFItem.SB_ITEM_HIGHLIGHTED

        else:
            if activeFitID == self.fitID:
                if self.highlighted:
                    state = SFItem.SB_ITEM_SELECTED | SFItem.SB_ITEM_HIGHLIGHTED
                else:
                    state = SFItem.SB_ITEM_SELECTED
            else:
                state = SFItem.SB_ITEM_NORMAL
        return state

    def RenderBackground(self):
        rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)

        # activeFitID = self.mainFrame.getActiveFit()
        state = self.GetState()

        sFactor = 0.2
        mFactor = None
        eFactor = 0

        if state == SFItem.SB_ITEM_HIGHLIGHTED:
            mFactor = 0.45
            eFactor = 0.30

        elif state == SFItem.SB_ITEM_SELECTED | SFItem.SB_ITEM_HIGHLIGHTED:
            eFactor = 0.3
            mFactor = 0.4

        elif state == SFItem.SB_ITEM_SELECTED:
            eFactor = (self.maxDelta - self.selectedDelta) / 100 + 0.25
        else:
            sFactor = 0

        if self.bkBitmap:
            if self.bkBitmap.eFactor == eFactor and self.bkBitmap.sFactor == sFactor and self.bkBitmap.mFactor == mFactor \
                    and rect.width == self.bkBitmap.GetWidth() and rect.height == self.bkBitmap.GetHeight():
                return
            else:
                del self.bkBitmap

        self.bkBitmap = drawUtils.RenderGradientBar(windowColor, rect.width, rect.height, sFactor, eFactor, mFactor)
        self.bkBitmap.state = state
        self.bkBitmap.sFactor = sFactor
        self.bkBitmap.eFactor = eFactor
        self.bkBitmap.mFactor = mFactor
