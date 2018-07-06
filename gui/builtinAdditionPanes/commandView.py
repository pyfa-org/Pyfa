# =============================================================================
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
# =============================================================================

# noinspection PyPackageRequirements
import wx

import gui.builtinAdditionPanes.droneView
import gui.display as d
import gui.globalEvents as GE
from gui.builtinShipBrowser.events import EVT_FIT_REMOVED
from eos.saveddata.drone import Drone as es_Drone
from gui.builtinContextMenus.commandFits import CommandFits
from gui.builtinViewColumns.state import State
from gui.contextMenu import ContextMenu
from gui.utils.staticHelpers import DragDropHelper
from service.fit import Fit


class DummyItem(object):
    def __init__(self, txt):
        self.name = txt
        self.iconID = None


class DummyEntry(object):
    def __init__(self, txt):
        self.item = DummyItem(txt)


class CommandViewDrop(wx.DropTarget):
    def __init__(self, dropFn, *args, **kwargs):
        super(CommandViewDrop, self).__init__(*args, **kwargs)
        self.dropFn = dropFn
        # this is really transferring an EVE itemID
        self.dropData = wx.TextDataObject()
        self.SetDataObject(self.dropData)

    def OnData(self, x, y, t):
        if self.GetData():
            dragged_data = DragDropHelper.data
            data = dragged_data.split(':')
            self.dropFn(x, y, data)
        return t


class CommandView(d.Display):
    DEFAULT_COLS = ["State", "Base Name"]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.LC_SINGLE_SEL | wx.BORDER_NONE)

        self.lastFitId = None

        self.mainFrame.Bind(GE.FIT_CHANGED, CommandFits.fitChanged)
        self.mainFrame.Bind(EVT_FIT_REMOVED, CommandFits.populateFits)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_RIGHT_DOWN, self.click)
        self.Bind(wx.EVT_LEFT_DCLICK, self.remove)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)

        self.droneView = gui.builtinAdditionPanes.droneView.DroneView

        if "__WXGTK__" in wx.PlatformInfo:
            self.Bind(wx.EVT_RIGHT_UP, self.scheduleMenu)
        else:
            self.Bind(wx.EVT_RIGHT_DOWN, self.scheduleMenu)

        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)
        self.SetDropTarget(CommandViewDrop(self.handleListDrag))

    @staticmethod
    def handleListDrag(x, y, data):
        """
        Handles dragging of items from various pyfa displays which support it

        data is list with two indices:
            data[0] is hard-coded str of originating source
            data[1] is typeID or index of data we want to manipulate
        """
        pass

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE or keycode == wx.WXK_NUMPAD_DELETE:
            fitID = self.mainFrame.getActiveFit()
            sFit = Fit.getInstance()
            row = self.GetFirstSelected()
            if row != -1:
                sFit.removeCommand(fitID, self.get(row))
                wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def handleDrag(self, type, fitID):
        # Those are drags coming from pyfa sources, NOT builtin wx drags
        if type == "fit":
            activeFit = self.mainFrame.getActiveFit()
            if activeFit:
                sFit = Fit.getInstance()
                draggedFit = sFit.getFit(fitID)
                sFit.addCommandFit(activeFit, draggedFit)
                wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=activeFit))

    def startDrag(self, event):
        row = event.GetIndex()
        if row != -1 and isinstance(self.get(row), es_Drone):
            data = wx.TextDataObject()
            dataStr = "command:" + str(self.GetItemData(row))
            data.SetText(dataStr)

            dropSource = wx.DropSource(self)
            dropSource.SetData(data)
            DragDropHelper.data = dataStr
            dropSource.DoDragDrop()

    @staticmethod
    def fitSort(fit):
        return fit.name

    def fitChanged(self, event):
        sFit = Fit.getInstance()
        fit = sFit.getFit(event.fitID)

        CommandFits.populateFits(event)

        self.Parent.Parent.DisablePage(self, not fit or fit.isStructure)

        # Clear list and get out if current fitId is None
        if event.fitID is None and self.lastFitId is not None:
            self.DeleteAllItems()
            self.lastFitId = None
            event.Skip()
            return

        stuff = []
        if fit is not None:
            self.fits = fit.commandFits[:]
            self.fits.sort(key=self.fitSort)
            stuff.extend(self.fits)

        if event.fitID != self.lastFitId:
            self.lastFitId = event.fitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.deselectItems()

        # todo: verify
        if not stuff:
            stuff = [DummyEntry("Drag a fit to this area")]

        self.update(stuff)

        event.Skip()

    def get(self, row):
        if row == -1:
            return None

        numFits = len(self.fits)

        if numFits == 0:
            return None

        return self.fits[row]

    def click(self, event):
        event.Skip()
        row, _ = self.HitTest(event.Position)
        if row != -1:
            item = self.get(row)
            col = self.getColumn(event.Position)
            if col == self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                sFit = Fit.getInstance()
                sFit.toggleCommandFit(fitID, item)
                wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def scheduleMenu(self, event):
        event.Skip()
        if self.getColumn(event.Position) != self.getColIndex(State):
            wx.CallAfter(self.spawnMenu)

    def spawnMenu(self):
        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return

        sel = self.GetFirstSelected()
        context = ()
        item = self.get(sel)

        if item is not None:
            fitSrcContext = "commandFit"
            fitItemContext = item.name
            context = ((fitSrcContext, fitItemContext),)

        context += (("commandView",),)
        menu = ContextMenu.getMenu((item,) if item is not None else [], *context)
        if menu is not None:
            self.PopupMenu(menu)

    def remove(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                sFit = Fit.getInstance()
                thing = self.get(row)
                if thing:  # thing doesn't exist if it's the dummy value
                    sFit.removeCommand(fitID, thing)
                    wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
