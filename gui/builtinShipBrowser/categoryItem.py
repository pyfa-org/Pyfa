# coding: utf-8

import wx
from logbook import Logger

from gui.builtinShipBrowser.sfBrowserItem import SFBrowserItem
import gui.utils.colorUtils as colorUtils
import gui.utils.drawUtils as drawUtils
import gui.utils.fonts as fonts
from gui.bitmapLoader import BitmapLoader
import events

pyfalog = Logger(__name__)


class CategoryItem(SFBrowserItem):
    def __init__(self, parent, categoryID, fittingInfo, size=(0, 16)):
        SFBrowserItem.__init__(self, parent, size=size)

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

    def OnKeyUp(self, event):
        if event.GetKeyCode() in (32, 13):  # space and enter
            self.selectCategory(event)
        event.Skip()

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

    def selectCategory(self, event):
        categoryID = self.categoryID
        wx.PostEvent(self.shipBrowser, events.Stage2Selected(categoryID=categoryID, back=False))

    def MouseLeftUp(self, event):
        self.selectCategory(event)

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
