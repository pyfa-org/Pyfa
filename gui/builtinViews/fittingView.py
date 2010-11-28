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
import wx.lib.newevent
import service
import gui.mainFrame
import gui.marketBrowser
import gui.display as d
from gui.contextMenu import ContextMenu
import gui.shipBrowser
import gui.multiSwitch
from eos.types import Slot
from gui.builtinViewColumns.state import State
from gui import bitmapLoader

import gui.globalEvents as GE

#Tab spawning handler
class FitSpawner(gui.multiSwitch.TabSpawner):
    def __init__(self, multiSwitch):
        self.multiSwitch = multiSwitch
        self.mainFrame = mainFrame = gui.mainFrame.MainFrame.getInstance()
        mainFrame.Bind(gui.shipBrowser.EVT_FIT_SELECTED, self.fitSelected)

    def fitSelected(self, event):
        count = -1
        if self.multiSwitch.GetPageCount() == 0:
            self.multiSwitch.AddPage()
        for index, page in enumerate(self.multiSwitch.pages):
            try:
                if page.activeFitID == event.fitID:
                    count +=1
                    self.multiSwitch.SetSelection(index)
                    wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=event.fitID))
                    break
            except:
                pass
        if count <0:
            view = FittingView(self.multiSwitch)
            self.multiSwitch.ReplaceActivePage(view)
            view.fitSelected(event)

    def handleDrag(self, type, fitID):
        if type == "fit":
            for page in self.multiSwitch.pages:
                if isinstance(page, FittingView) and page.activeFitID == fitID:
                    index = self.multiSwitch.GetPageIndex(page)
                    self.multiSwitch.SetSelection(index)
                    return
                elif isinstance(page, gui.multiSwitch.BlankPage):
                    view = FittingView(self.multiSwitch)
                    self.multiSwitch.ReplaceActivePage(view)
                    view.handleDrag(type, fitID)
                    return

            view = FittingView(self.multiSwitch)
            self.multiSwitch.AddPage(view)
            view.handleDrag(type, fitID)

FitSpawner.register()

#Drag'n'drop handler
class FittingViewDrop(wx.PyDropTarget):
        def __init__(self, dropFn):
            wx.PyDropTarget.__init__(self)
            self.dropFn = dropFn
            # this is really transferring an EvE itemID
            self.dropData = wx.PyTextDataObject()
            self.SetDataObject(self.dropData)

        def OnData(self, x, y, t):
            if self.GetData():
                self.dropFn(x, y, int(self.dropData.GetText()))
            return t


class FittingView(d.Display):
    DEFAULT_COLS = ["State",
                    "Ammo Icon",
                    "Base Icon",
                    "Base Name",
                    "attr:power",
                    "attr:cpu",
                    "Capacitor Usage",
                    "Max Range",
                    "Tracking",
                    "Price",
                    "Ammo",
                    ]

    def __init__(self, parent):
        d.Display.__init__(self, parent, size = (0,0))
        self.Show(False)
        self.parent = parent
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(gui.shipBrowser.EVT_FIT_RENAMED, self.fitRenamed)
        self.mainFrame.Bind(gui.shipBrowser.EVT_FIT_REMOVED, self.fitRemoved)
        self.mainFrame.Bind(gui.marketBrowser.ITEM_SELECTED, self.appendItem)

        self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)
        if "__WXGTK__" in  wx.PlatformInfo:
            self.Bind(wx.EVT_RIGHT_UP, self.scheduleMenu)
        else:
            self.Bind(wx.EVT_RIGHT_DOWN, self.scheduleMenu)

        self.SetDropTarget(FittingViewDrop(self.swapItems))
        self.activeFitID = None
        self.FVsnapshot = None
        self.itemCount = 0
        self.itemRect = 0

        self.Bind(wx.EVT_KEY_UP, self.kbEvent)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_RIGHT_DOWN, self.click)
        self.Bind(wx.EVT_SHOW, self.OnShow)
        self.parent.Bind(gui.chromeTabs.EVT_NOTEBOOK_PAGE_CHANGED, self.pageChanged)

    def handleDrag(self, type, fitID):
        if type == "fit":
            wx.PostEvent(self.mainFrame, gui.shipBrowser.FitSelected(fitID=fitID))

    def Destroy(self):
        self.parent.Unbind(gui.chromeTabs.EVT_NOTEBOOK_PAGE_CHANGED, handler=self.pageChanged)
        self.mainFrame.Unbind(GE.FIT_CHANGED, handler=self.fitChanged)
        self.mainFrame.Unbind(gui.shipBrowser.EVT_FIT_RENAMED, handler=self.fitRenamed)
        self.mainFrame.Unbind(gui.shipBrowser.EVT_FIT_REMOVED, handler=self.fitRemoved)
        self.mainFrame.Unbind(gui.marketBrowser.ITEM_SELECTED, handler=self.appendItem)

        d.Display.Destroy(self)

    def pageChanged(self, event):
        if self.parent.IsActive(self):
            fitID = self.getActiveFit()
            sFit = service.Fit.getInstance()
            sFit.switchFit(fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

        event.Skip()

    def getActiveFit(self):
        return self.activeFitID

    def startDrag(self, event):
        row = event.GetIndex()
        if row != -1:
            data = wx.PyTextDataObject()
            data.SetText(str(self.GetItemData(row)))

            dropSource = wx.DropSource(self)
            dropSource.SetData(data)
            res = dropSource.DoDragDrop()


    def getSelectedMods(self):
        sel = []
        row = self.GetFirstSelected()
        while row != -1:
            sel.append(self.mods[self.GetItemData(row)])
            row = self.GetNextSelected(row)

        return sel

    def kbEvent(self,event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE or keycode == wx.WXK_NUMPAD_DELETE:
            row = self.GetFirstSelected()
            firstSel = row
            while row != -1:
                cFit = service.Fit.getInstance()
                populate = cFit.removeModule(self.activeFitID, self.mods[self.GetItemData(row)].position)
                self.Select(row,0)
                row = self.GetNextSelected(row)
                if populate is not None:
                    self.Select(firstSel)
                    if populate: self.slotsChanged()
                    wx.PostEvent(self.mainFrame, FitChanged(fitID=self.activeFitID))

        event.Skip()

    def fitRemoved(self, event):
        fitID = event.fitID
        if fitID == self.getActiveFit():
            self.parent.DeletePage(self.parent.GetPageIndex(self))

        event.Skip()

    def fitRenamed(self, event):
        fitID = event.fitID
        if fitID == self.getActiveFit():
            self.updateTab()

        event.Skip()

    def fitSelected(self, event):
        if self.parent.IsActive(self):
            fitID = event.fitID
            self.activeFitID = fitID
            self.Show(fitID is not None)
            self.slotsChanged()
            sFit = service.Fit.getInstance()
            sFit.switchFit(fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
            self.updateTab()

        event.Skip()

    def updateTab(self):
        cFit = service.Fit.getInstance()
        fit = cFit.getFit(self.getActiveFit())
        bitmap = bitmapLoader.getImage("race_%s_small" % fit.ship.item.race, "icons")
        text = "%s: %s" % (fit.ship.item.name, fit.name)
        self.parent.SetPageTextIcon(self.parent.GetSelection(), text, bitmap)

    def appendItem(self, event):
        if self.parent.IsActive(self):
            itemID = event.itemID
            fitID = self.activeFitID
            if fitID != None:
                cFit = service.Fit.getInstance()
                if cFit.isAmmo(itemID):
                    modules = []
                    sel = self.GetFirstSelected()
                    while sel != -1:
                        modules.append(self.mods[self.GetItemData(sel)])
                        sel = self.GetNextSelected(sel)

                    cFit.setAmmo(fitID, itemID, modules)
                    wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
                else:
                    populate = cFit.appendModule(fitID, itemID)
                    if populate:
                        self.slotsChanged()
                    if populate is not None:
                        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

        event.Skip()

    def removeItem(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                cFit = service.Fit.getInstance()
                populate = cFit.removeModule(self.activeFitID, self.mods[self.GetItemData(row)].position)

                if populate is not None:
                    if populate: self.slotsChanged()
                    wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.activeFitID))

        event.Skip()

    def swapItems(self, x, y, itemID):
        srcRow = self.FindItemData(-1,itemID)
        dstRow, _ = self.HitTest((x, y))
        if srcRow != -1 and dstRow != -1:
            self._swap(srcRow, dstRow)

    def _swap(self, srcRow, dstRow):
        mod1 = self.mods[self.GetItemData(srcRow)]
        mod2 = self.mods[self.GetItemData(dstRow)]

        if mod1.slot != mod2.slot:
            if srcRow > dstRow:
                mod = 1
            else:
                mod = -1

            while mod1.slot != mod2.slot:
                dstRow += mod
                mod2 = self.mods[self.GetItemData(dstRow)]

        cFit = service.Fit.getInstance()
        cFit.swapModules(self.mainFrame.getActiveFit(),
                         mod1.position,
                         mod2.position)

        self.generateMods()
        self.refresh(self.mods)

    def generateMods(self):
        cFit = service.Fit.getInstance()
        fit = cFit.getFit(self.activeFitID)

        slotOrder = [Slot.SUBSYSTEM, Slot.HIGH, Slot.MED, Slot.LOW, Slot.RIG]

        if fit is not None:
            self.mods = fit.modules[:]
            self.mods.sort(key=lambda mod: (slotOrder.index(mod.slot), mod.position))
        else:
            self.mods = None

    def slotsChanged(self):
        self.generateMods()
        self.populate(self.mods)

    def fitChanged(self, event):
        try:
            if self.activeFitID is not None and self.activeFitID == event.fitID:
                self.generateMods()
                self.refresh(self.mods)

            self.Show(self.activeFitID is not None and self.activeFitID == event.fitID)
        except wx._core.PyDeadObjectError:
            pass
        finally:
            event.Skip()

    def scheduleMenu(self, event):
        event.Skip()
        if self.getColumn(event.Position) != self.getColIndex(State):
            wx.CallAfter(self.spawnMenu)

    def spawnMenu(self):
        if self.activeFitID is None:
            return
        cFit = service.Fit.getInstance()
        selection = []
        sel = self.GetFirstSelected()
        contexts = set()
        while sel != -1:
            mod = self.mods[self.GetItemData(sel)]
            if not mod.isEmpty:
                contexts.add("module")
                if mod.charge is not None and "ammo" not in contexts:
                    contexts.add("ammo")

                selection.append(mod)

            sel = self.GetNextSelected(sel)

        contexts.add("ship")

        menu = ContextMenu.getMenu(selection, *contexts)
        self.PopupMenu(menu)

    def click(self, event):
        row, _ = self.HitTest(event.Position)
        col = self.getColumn(event.Position)
        if row != -1 and col == self.getColIndex(State):
            sel = []
            curr = self.GetFirstSelected()
            while curr != -1:
                sel.append(curr)
                curr = self.GetNextSelected(curr)

            if row not in sel:
                mods = [self.mods[self.GetItemData(row)]]
            else:
                mods = self.getSelectedMods()

            sFit = service.Fit.getInstance()
            fitID = self.mainFrame.getActiveFit()
            sFit.toggleModulesState(fitID, self.mods[self.GetItemData(row)], mods, "right" if event.Button == 3 else "left")
            wx.PostEvent(self.mainFrame, FitChanged(fitID=self.mainFrame.getActiveFit()))
        else:
            event.Skip()

    def refresh(self, stuff):
        d.Display.refresh(self, stuff)
        sFit = service.Fit.getInstance()
        fit = sFit.getFit(self.activeFitID)
        slotMap = {}
        for slotType in Slot.getTypes():
            slot = Slot.getValue(slotType)
            slotMap[slot] = fit.getSlotsFree(slot) < 0
        bkcolor = self.GetBackgroundColour()
        for i, mod in enumerate(self.mods):
            if slotMap[mod.slot]:
                self.SetItemBackgroundColour(i, wx.Colour(204, 51, 51))
            else:
                icolor = self.GetItemBackgroundColour(i)
                if icolor != bkcolor:
                    self.SetItemBackgroundColour(i, bkcolor)
        self.itemCount = self.GetItemCount()
        self.itemRect = self.GetItemRect(0)

        if 'wxMac' in wx.PlatformInfo:
            self.MakeSnapshot()

    def OnShow(self, event):
        if not event.GetShow():
            self.MakeSnapshot()
        event.Skip()

    def Snapshot(self):
        return self.FVsnapshot

    def MakeSnapshot(self):
        if self.FVsnapshot:
            del self.FVsnapshot

        wantedWidth = 0
        for i in xrange(4):
            wantedWidth += self.GetColumnWidth(i)

        icount = self.itemCount
        irect = self.itemRect
        if irect:
            ih = irect.height
            it = irect.top
        else:
            ih = 0
            it = 0
        rect = self.GetRect()
        rect.height = min(ih * icount + it, rect.height - 16)
        rect.width = min(rect.width, wantedWidth)

        mdc = wx.MemoryDC()
        mbmp = wx.EmptyBitmap(rect.width, rect.height)
        mdc.SelectObject(mbmp)

        pageDC = wx.ClientDC(self)

        mdc.Blit(0, 0, rect.width, rect.height, pageDC, 0, 0)

        mdc.SelectObject(wx.NullBitmap)

        self.FVsnapshot = mbmp
