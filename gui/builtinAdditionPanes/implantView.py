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

import gui.display as d
import gui.fitCommands as cmd
import gui.globalEvents as GE
import gui.mainFrame
from eos.const import ImplantLocation
from gui.builtinMarketBrowser.events import ITEM_SELECTED
from gui.builtinViewColumns.state import State
from gui.contextMenu import ContextMenu
from gui.utils.staticHelpers import DragDropHelper
from service.fit import Fit
from service.market import Market

_t = wx.GetTranslation


class ImplantViewDrop(wx.DropTarget):
    def __init__(self, dropFn, *args, **kwargs):
        super(ImplantViewDrop, self).__init__(*args, **kwargs)
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


class ImplantView(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.implantDisplay = ImplantDisplay(self)
        mainSizer.Add(self.implantDisplay, 1, wx.EXPAND, 0)

        radioSizer = wx.BoxSizer(wx.HORIZONTAL)
        radioSizer.AddStretchSpacer()
        self.rbFit = wx.RadioButton(self, id=wx.ID_ANY, label=_t("Use Fit-specific Implants"), style=wx.RB_GROUP)
        self.rbChar = wx.RadioButton(self, id=wx.ID_ANY, label=_t("Use Character Implants"))
        radioSizer.Add(self.rbFit, 0, wx.ALL, 5)
        radioSizer.Add(self.rbChar, 0, wx.ALL, 5)
        radioSizer.AddStretchSpacer()

        mainSizer.Add(radioSizer, 0, wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioSelect, self.rbFit)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioSelect, self.rbChar)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)

    def fitChanged(self, event):
        event.Skip()
        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID is not None and activeFitID not in event.fitIDs:
            return

        sFit = Fit.getInstance()
        fit = sFit.getFit(activeFitID)
        if fit:
            self.source = fit.implantSource
            if fit.implantSource == ImplantLocation.FIT:
                self.rbFit.SetValue(True)
            else:
                self.rbChar.SetValue(True)

        self.rbFit.Enable(fit is not None)
        self.rbChar.Enable(fit is not None)

    def OnRadioSelect(self, event):
        fitID = self.mainFrame.getActiveFit()
        if fitID is not None:
            self.mainFrame.command.Submit(cmd.GuiChangeImplantLocationCommand(
                fitID=fitID, source=ImplantLocation.FIT if self.rbFit.GetValue() else ImplantLocation.CHARACTER))

    def getTabExtraText(self):
        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return None
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        if fit is None:
            return None
        opt = sFit.serviceFittingOptions["additionsLabels"]
        # Amount of active implants
        if opt == 1:
            amount = len([i for i in fit.appliedImplants if i.active])
            return ' ({})'.format(amount) if amount else None
        # Total amount of implants
        elif opt == 2:
            amount = len(fit.appliedImplants)
            return ' ({})'.format(amount) if amount else None
        else:
            return None

class ImplantDisplay(d.Display):

    DEFAULT_COLS = [
        "State",
        "attr:implantness",
        "Base Icon",
        "Base Name",
        "Price",
    ]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.BORDER_NONE)

        self.lastFitId = None

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(ITEM_SELECTED, self.addItem)
        self.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDoubleClick)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)
        self.SetDropTarget(ImplantViewDrop(self.handleListDrag))

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)


    def handleListDrag(self, x, y, data):
        """
        Handles dragging of items from various pyfa displays which support it

        data is list with two indices:
            data[0] is hard-coded str of originating source
            data[1] is typeID or index of data we want to manipulate
        """

        if data[0] == "market":
            if self.mainFrame.command.Submit(cmd.GuiAddImplantCommand(
                    fitID=self.mainFrame.getActiveFit(), itemID=int(data[1]))):
                self.mainFrame.additionsPane.select("Implants")

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        modifiers = event.GetModifiers()
        if keycode == wx.WXK_ESCAPE and modifiers == wx.MOD_NONE:
            self.unselectAll()
        elif keycode == 65 and modifiers == wx.MOD_CONTROL:
            self.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and modifiers == wx.MOD_NONE:
            implants = self.getSelectedImplants()
            self.removeImplants(implants)
        event.Skip()

    def fitChanged(self, event):
        event.Skip()
        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID is not None and activeFitID not in event.fitIDs:
            return

        sFit = Fit.getInstance()
        fit = sFit.getFit(activeFitID)

        self.Parent.Parent.Parent.DisablePage(self.Parent, not fit or fit.isStructure)

        # Clear list and get out if current fitId is None
        if activeFitID is None and self.lastFitId is not None:
            self.DeleteAllItems()
            self.lastFitId = None
            return

        self.original = fit.appliedImplants if fit is not None else None
        self.implants = fit.appliedImplants[:] if fit is not None else None
        if self.implants is not None:
            self.implants.sort(key=lambda implant: implant.slot or 0)

        if activeFitID != self.lastFitId:
            self.lastFitId = activeFitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.unselectAll()

        self.update(self.implants)

    def addItem(self, event):
        item = Market.getInstance().getItem(event.itemID, eager='group.category')
        if item is None or not item.isImplant:
            event.Skip()
            return

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)

        if not fit or fit.isStructure:
            event.Skip()
            return

        self.mainFrame.command.Submit(cmd.GuiAddImplantCommand(
            fitID=fitID, itemID=event.itemID))
        # Select in any case - as we might've added implant which has been there already and command failed
        self.mainFrame.additionsPane.select('Implants')

        event.Skip()

    def onLeftDoubleClick(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                try:
                    implant = self.implants[row]
                except IndexError:
                    return
                self.removeImplants([implant])

    def removeImplants(self, implants):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if fit.implantLocation != ImplantLocation.FIT:
            return
        positions = []
        for implant in implants:
            if implant in self.original:
                positions.append(self.original.index(implant))
        self.mainFrame.command.Submit(cmd.GuiRemoveImplantsCommand(fitID=fitID, positions=positions))

    def click(self, event):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if fit.implantLocation == ImplantLocation.FIT:
            mainRow, _ = self.HitTest(event.Position)
            if mainRow != -1:
                col = self.getColumn(event.Position)
                if col == self.getColIndex(State):
                    fitID = self.mainFrame.getActiveFit()
                    try:
                        mainImplant = self.implants[mainRow]
                    except IndexError:
                        return
                    if mainImplant in self.original:
                        mainPosition = self.original.index(mainImplant)
                        positions = []
                        for row in self.getSelectedRows():
                            try:
                                implant = self.implants[row]
                            except IndexError:
                                continue
                            if implant in self.original:
                                positions.append(self.original.index(implant))
                        if mainPosition not in positions:
                            positions = [mainPosition]
                        self.mainFrame.command.Submit(cmd.GuiToggleImplantStatesCommand(
                            fitID=fitID,
                            mainPosition=mainPosition,
                            positions=positions))
                        return
        event.Skip()

    def spawnMenu(self, event):
        clickedPos = self.getRowByAbs(event.Position)
        self.ensureSelection(clickedPos)

        selection = self.getSelectedImplants()
        mainImplant = None
        if clickedPos != -1:
            try:
                implant = self.implants[clickedPos]
            except IndexError:
                pass
            else:
                if implant in self.original:
                    mainImplant = implant
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        sourceContext1 = "implantItem" if fit.implantSource == ImplantLocation.FIT else "implantItemChar"
        sourceContext2 = "implantItemMisc" if fit.implantSource == ImplantLocation.FIT else "implantItemMiscChar"
        itemContext = None if mainImplant is None else Market.getInstance().getCategoryByItem(mainImplant.item).displayName
        menu = ContextMenu.getMenu(self, mainImplant, selection,
                                   (sourceContext1, itemContext),
                                   (sourceContext2, itemContext)
                                   )
        if menu:
            self.PopupMenu(menu)

    def getSelectedImplants(self):
        implants = []
        for row in self.getSelectedRows():
            try:
                implant = self.implants[row]
            except IndexError:
                continue
            implants.append(implant)
        return implants

    def addImplants(self, implants):
        self.mainFrame.command.Submit(cmd.GuiAddImplantSetCommand(
            fitID=self.mainFrame.getActiveFit(),
            itemIDs=[i.itemID for i in implants]))
