# coding: utf-8

import wx
from logbook import Logger

import gui.builtinShipBrowser.sfBrowserItem as SFItem
import gui.mainFrame
import gui.utils.colorUtils as colorUtils
import gui.utils.drawUtils as drawUtils
import gui.utils.fonts as fonts
import events
from gui.bitmapLoader import BitmapLoader
from service.fit import Fit

pyfalog = Logger(__name__)


class NavigationPanel(SFItem.SFBrowserItem):
    def __init__(self, parent, size=(-1, 24)):
        SFItem.SFBrowserItem.__init__(self, parent, size=size)

        self.rewBmpH = BitmapLoader.getBitmap("frewind_small", "gui")
        self.forwBmp = BitmapLoader.getBitmap("fforward_small", "gui")
        self.searchBmpH = BitmapLoader.getBitmap("fsearch_small", "gui")
        self.newBmpH = BitmapLoader.getBitmap("fit_add_small", "gui")
        self.resetBmpH = BitmapLoader.getBitmap("freset_small", "gui")
        self.switchBmpH = BitmapLoader.getBitmap("fit_switch_view_mode_small", "gui")
        self.recentBmpH = BitmapLoader.getBitmap("frecent_small", "gui")

        switchImg = BitmapLoader.getImage("fit_switch_view_mode_small", "gui")
        switchImg = switchImg.AdjustChannels(1, 1, 1, 0.4)
        self.switchBmpD = wx.BitmapFromImage(switchImg)

        recentImg = BitmapLoader.getImage("frecent_small", "gui")
        recentImg = recentImg.AdjustChannels(1, 1, 1, 0.4)
        self.recentBmpD = wx.BitmapFromImage(recentImg)

        self.resetBmp = self.AdjustChannels(self.resetBmpH)
        self.rewBmp = self.AdjustChannels(self.rewBmpH)
        self.searchBmp = self.AdjustChannels(self.searchBmpH)
        self.switchBmp = self.AdjustChannels(self.switchBmpH)
        self.recentBmp = self.AdjustChannels(self.recentBmpH)
        self.newBmp = self.AdjustChannels(self.newBmpH)

        self.toolbar.AddButton(self.resetBmp, "Ship groups", clickCallback=self.OnHistoryReset,
                               hoverBitmap=self.resetBmpH)
        self.toolbar.AddButton(self.rewBmp, "Back", clickCallback=self.OnHistoryBack, hoverBitmap=self.rewBmpH)
        self.btnNew = self.toolbar.AddButton(self.newBmp, "New fitting", clickCallback=self.OnNewFitting,
                                             hoverBitmap=self.newBmpH, show=False)
        self.btnSwitch = self.toolbar.AddButton(self.switchBmpD, "Hide empty ship groups",
                                                clickCallback=self.ToggleEmptyGroupsView, hoverBitmap=self.switchBmpH,
                                                show=False)
        self.btnRecent = self.toolbar.AddButton(self.recentBmpD, "Recent Fits",
                                                clickCallback=self.ToggleRecentShips, hoverBitmap=self.recentBmpH,
                                                show=True)

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
                                             (wx.BORDER_NONE if 'wxGTK' in wx.PlatformInfo else 0))
        self.BrowserSearchBox.Show(False)

        # self.BrowserSearchBox.Bind(wx.EVT_TEXT_ENTER, self.OnBrowserSearchBoxEnter)
        # self.BrowserSearchBox.Bind(wx.EVT_KILL_FOCUS, self.OnBrowserSearchBoxLostFocus)
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
            wx.PostEvent(self.shipBrowser, events.SearchSelected(text=search, back=False))

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

    def ToggleRecentShips(self, bool=None, emitEvent=True):
        # this is so janky. Need to revaluate pretty much entire ship browser. >.<
        toggle = bool if bool is not None else not self.shipBrowser.recentFits

        if not toggle:
            self.shipBrowser.recentFits = False
            self.btnRecent.label = "Recent Fits"
            self.btnRecent.normalBmp = self.recentBmpD

            if emitEvent:
                wx.PostEvent(self.shipBrowser, events.Stage1Selected())
        else:
            self.shipBrowser.recentFits = True
            self.btnRecent.label = "Hide Recent Fits"
            self.btnRecent.normalBmp = self.recentBmp

            if emitEvent:
                sFit = Fit.getInstance()
                fits = sFit.getRecentFits()
                wx.PostEvent(self.shipBrowser, events.ImportSelected(fits=fits, back=True, recent=True))

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
            wx.PostEvent(self.shipBrowser, events.Stage1Selected())
        elif stage == 2:
            categoryID = self.shipBrowser.GetStageData(stage)
            wx.PostEvent(self.shipBrowser, events.Stage2Selected(categoryID=categoryID, back=True))

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
            wx.PostEvent(self.Parent, events.Stage3Selected(shipID=shipID))
            wx.PostEvent(self.mainFrame, events.FitSelected(fitID=fitID))

    def OnHistoryReset(self):
        self.ToggleRecentShips(False, False)
        if self.shipBrowser.browseHist:
            self.shipBrowser.browseHist = []
        self.gotoStage(1, 0)

    def OnHistoryBack(self):
        self.ToggleRecentShips(False, False)
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
        self.shipBrowser.recentFits = False
        if stage == 1:
            wx.PostEvent(self.Parent, events.Stage1Selected())
        elif stage == 2:
            wx.PostEvent(self.Parent, events.Stage2Selected(categoryID=data, back=True))
        elif stage == 3:
            wx.PostEvent(self.Parent, events.Stage3Selected(shipID=data))
        elif stage == 4:
            self.shipBrowser._activeStage = 4
            wx.PostEvent(self.Parent, events.SearchSelected(text=data, back=True))
        elif stage == 5:
            wx.PostEvent(self.Parent, events.ImportSelected(fits=data))
        else:
            wx.PostEvent(self.Parent, events.Stage1Selected())
