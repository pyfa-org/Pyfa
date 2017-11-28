import re

import wx
from logbook import Logger

import gui.builtinShipBrowser.sfBrowserItem as SFItem
import gui.mainFrame
import gui.utils.color as colorUtils
import gui.utils.draw as drawUtils
import gui.utils.fonts as fonts
from .events import Stage3Selected, Stage2Selected, Stage1Selected, FitSelected
from gui.bitmap_loader import BitmapLoader
from gui.contextMenu import ContextMenu
from service.fit import Fit
from service.market import Market

pyfalog = Logger(__name__)


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

        img = self.shipEffBk.ConvertToImage()
        img = img.Mirror(False)
        self.shipEffBkMirrored = wx.Bitmap(img)

        self.raceBmp = BitmapLoader.getBitmap("race_%s_small" % self.shipRace, "gui")

        if not self.raceBmp:
            self.raceBmp = BitmapLoader.getBitmap("fit_delete_small", "gui")

        self.raceDropShadowBmp = drawUtils.CreateDropShadowBitmap(self.raceBmp, 0.2)

        sFit = Fit.getInstance()
        if self.shipTrait and sFit.serviceFittingOptions["showShipBrowserTooltip"]:
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

    def OnKeyUp(self, event):
        if event.GetKeyCode() in (32, 13):  # space and enter
            self.selectShip(event)
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
        return 2

    def selectShip(self, event):
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

    def MouseLeftUp(self, event):
        self.selectShip(event)

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

        windowColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        textColor = colorUtils.GetSuitable(windowColor, 1)

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
