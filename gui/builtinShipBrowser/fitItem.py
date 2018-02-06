# coding: utf-8

import re
import time

import wx
from logbook import Logger

import gui.builtinShipBrowser.sfBrowserItem as SFItem
import gui.globalEvents as GE
import gui.mainFrame
import gui.utils.colorUtils as colorUtils
import gui.utils.drawUtils as drawUtils
import gui.utils.fonts as fonts
import events
from gui.bitmapLoader import BitmapLoader
from gui.builtinShipBrowser.pfBitmapFrame import PFBitmapFrame
from service.fit import Fit

pyfalog = Logger(__name__)


class FitItem(SFItem.SFBrowserItem):
    def __init__(self, parent, fitID=None, shipFittingInfo=("Test", "TestTrait", "cnc's avatar", 0, 0, None), shipID=None,
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
        self.shipName, self.shipTrait, self.fitName, self.fitBooster, self.timestamp, self.notes = shipFittingInfo

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

        self.__setToolTip()

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

        """
        # Remove this bit as the time stuff is non-functional (works... but not exactly sure what it's meant to do)
        self.selTimerID = wx.NewId()

        self.selTimer = wx.Timer(self, self.selTimerID)
        self.selTimer.Start(100)
        """

        self.Bind(wx.EVT_RIGHT_UP, self.OnContextMenu)
        self.Bind(wx.EVT_MIDDLE_UP, self.OpenNewTab)

    def __setToolTip(self):
        sFit = Fit.getInstance()
        # show no tooltip if no trait available or setting is disabled
        if self.shipTrait and sFit.serviceFittingOptions["showShipBrowserTooltip"]:
            notes = ""
            if self.notes:
                notes = u'─' * 20 + u"\nNotes: {}\n".format(self.notes[:197] + '...' if len(self.notes) > 200 else self.notes)
            self.SetToolTip(wx.ToolTip(u'{}\n{}{}\n{}'.format(self.shipName, notes, u'─' * 20, self.shipTrait)))

    def OnKeyUp(self, event):
        if event.GetKeyCode() in (32, 13):  # space and enter
            self.selectFit(event)
        event.Skip()

    def OpenNewTab(self, evt):
        self.selectFit(newTab=True)

    def OnToggleBooster(self, event):
        sFit = Fit.getInstance()
        sFit.toggleBoostFit(self.fitID)
        self.fitBooster = not self.fitBooster
        self.boosterBtn.Show(self.fitBooster)
        self.Refresh()
        wx.PostEvent(self.mainFrame, events.BoosterListUpdated())
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
            newTabItem = menu.Append(wx.ID_ANY, "Open in new tab")
            self.Bind(wx.EVT_MENU, self.OpenNewTab, newTabItem)

            projectedItem = menu.Append(wx.ID_ANY, "Project onto Active Fit")
            self.Bind(wx.EVT_MENU, self.OnProjectToFit, projectedItem)

            commandItem = menu.Append(wx.ID_ANY, "Add Command Booster")
            self.Bind(wx.EVT_MENU, self.OnAddCommandFit, commandItem)

        self.PopupMenu(menu, pos)

        event.Skip()

    def GetType(self):
        return 3

    def OnTimer(self, event):

        # @todo: figure out what exactly this is supposed to accomplish
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
        wx.PostEvent(self.shipBrowser, events.Stage3Selected(shipID=self.shipID))
        wx.PostEvent(self.mainFrame, events.FitSelected(fitID=fitID))

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
            wx.PostEvent(self.mainFrame, events.FitRenamed(fitID=self.fitID))
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
        pyfalog.debug("Deleting ship fit.")
        if self.deleted:
            return
        else:
            self.deleted = True

        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)

        # need to delete from import cache before actually deleting fit
        if self.shipBrowser.GetActiveStage() == 5:
            for x in self.shipBrowser.lastdata:  # remove fit from import cache
                if x[0] == self.fitID:
                    self.shipBrowser.lastdata.remove(x)
                    break

        sFit.deleteFit(self.fitID)

        # Notify other areas that a fit has been deleted
        wx.PostEvent(self.mainFrame, events.FitRemoved(fitID=self.fitID))

        # todo: would a simple RefreshList() work here instead of posting that a stage has been selected?
        if self.shipBrowser.GetActiveStage() == 5:
            wx.PostEvent(self.shipBrowser, events.ImportSelected(fits=self.shipBrowser.lastdata, recent=self.shipBrowser.recentFits))
        elif self.shipBrowser.GetActiveStage() == 4:
            wx.PostEvent(self.shipBrowser, events.SearchSelected(text=self.shipBrowser.navpanel.lastSearch, back=True))
        else:
            wx.PostEvent(self.shipBrowser, events.Stage3Selected(shipID=self.shipID))

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

    def selectFit(self, event=None, newTab=False):
        if newTab:
            wx.PostEvent(self.mainFrame, events.FitSelected(fitID=self.fitID, startup=2))
        else:
            wx.PostEvent(self.mainFrame, events.FitSelected(fitID=self.fitID))

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

        fitDate = self.timestamp.strftime("%m/%d/%Y %H:%M")
        fitLocalDate = fitDate  # "%d/%02d/%02d %02d:%02d" % (fitDate[0], fitDate[1], fitDate[2], fitDate[3], fitDate[4])
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

    def Refresh(self):
        activeFit = self.mainFrame.getActiveFit()
        if activeFit == self.fitID and not self.deleted:
            sFit = Fit.getInstance()
            fit = sFit.getFit(activeFit)
            if fit is not None:  # sometimes happens when deleting fits, dunno why.
                self.timestamp = fit.modifiedCoalesce
                self.notes = fit.notes
                self.__setToolTip()

        SFItem.SFBrowserItem.Refresh(self)

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
