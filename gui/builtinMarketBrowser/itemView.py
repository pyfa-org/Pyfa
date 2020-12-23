import wx
from logbook import Logger

import gui.builtinMarketBrowser.pfSearchBox as SBox
from config import slotColourMap
from eos.saveddata.module import Module
from gui.builtinMarketBrowser.events import ItemSelected, RECENTLY_USED_MODULES
from gui.contextMenu import ContextMenu
from gui.display import Display
from gui.utils.staticHelpers import DragDropHelper
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class ItemView(Display):

    DEFAULT_COLS = ["Base Icon",
                    "Base Name",
                    "attr:power,,,True",
                    "attr:cpu,,,True"]

    def __init__(self, parent, marketBrowser):
        Display.__init__(self, parent, style=wx.LC_SINGLE_SEL)
        pyfalog.debug("Initialize ItemView")
        marketBrowser.Bind(wx.EVT_TREE_SEL_CHANGED, self.treeSelectionChanged)

        self.unfilteredStore = set()
        self.filteredStore = set()
        self.sMkt = marketBrowser.sMkt
        self.sFit = Fit.getInstance()

        self.marketBrowser = marketBrowser
        self.marketView = marketBrowser.marketView

        # Set up timer for delaying search on every EVT_TEXT
        self.searchTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.scheduleSearch, self.searchTimer)

        # Make sure our search actually does interesting stuff
        self.marketBrowser.search.Bind(SBox.EVT_TEXT_ENTER, self.scheduleSearch)
        self.marketBrowser.search.Bind(SBox.EVT_SEARCH_BTN, self.scheduleSearch)
        self.marketBrowser.search.Bind(SBox.EVT_CANCEL_BTN, self.clearSearch)
        self.marketBrowser.search.Bind(SBox.EVT_TEXT, self.delaySearch)

        # Make sure WE do interesting stuff too
        self.Bind(wx.EVT_CONTEXT_MENU, self.contextMenu)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.itemActivated)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)

        self.active = []

    def delaySearch(self, evt):
        sFit = Fit.getInstance()
        self.searchTimer.Stop()
        self.searchTimer.Start(sFit.serviceFittingOptions["marketSearchDelay"], True)

    def startDrag(self, event):
        row = self.GetFirstSelected()

        if row != -1:
            data = wx.TextDataObject()
            dataStr = "market:" + str(self.active[row].ID)
            pyfalog.debug("Dragging from market: " + dataStr)

            data.SetText(dataStr)
            dropSource = wx.DropSource(self)
            dropSource.SetData(data)
            DragDropHelper.data = dataStr
            dropSource.DoDragDrop()

    def itemActivated(self, event=None):
        # Check if something is selected, if so, spawn the menu for it
        sel = self.GetFirstSelected()
        if sel == -1:
            return

        if self.mainFrame.getActiveFit():
            wx.PostEvent(self.mainFrame, ItemSelected(itemID=self.active[sel].ID))

    def treeSelectionChanged(self, event=None):
        self.selectionMade('tree')

    def selectionMade(self, context):
        self.marketBrowser.mode = 'normal'
        # Grab the threeview selection and check if it's fine
        sel = self.marketView.GetSelection()
        if sel.IsOk():
            # Get data field of the selected item (which is a marketGroup ID if anything was selected)
            seldata = self.marketView.GetItemData(sel)
            if seldata is not None and seldata != RECENTLY_USED_MODULES:
                # If market group treeview item doesn't have children (other market groups or dummies),
                # then it should have items in it and we want to request them
                if self.marketView.ItemHasChildren(sel) is False:
                    sMkt = self.sMkt
                    # Get current market group
                    mg = sMkt.getMarketGroup(seldata, eager=("items", "items.metaGroup"))
                    # Get all its items
                    items = sMkt.getItemsByMarketGroup(mg)
                else:
                    items = set()
            else:
                # If method was called but selection wasn't actually made or we have a hit on recently used modules
                if seldata == RECENTLY_USED_MODULES:
                    items = self.sMkt.getRecentlyUsed()
                else:
                    items = set()

            # Fill store
            self.updateItemStore(items)

            # Set toggle buttons / use search mode flag if recently used modules category is selected (in order to have all modules listed and not filtered)
            if seldata == RECENTLY_USED_MODULES:
                self.marketBrowser.mode = 'recent'

            self.setToggles()
            if context == 'tree' and self.marketBrowser.settings.get('marketMGMarketSelectMode') == 1:
                for btn in self.marketBrowser.metaButtons:
                    if not btn.GetValue():
                        btn.setUserSelection(True)
            self.filterItemStore()

    def updateItemStore(self, items):
        self.unfilteredStore = items

    def filterItemStore(self):
        filteredItems = self.filterItems()
        if len(filteredItems) == 0 and len(self.unfilteredStore) > 0:
            setting = self.marketBrowser.settings.get('marketMGEmptyMode')
            # Enable leftmost available
            if setting == 1:
                for btn in self.marketBrowser.metaButtons:
                    if btn.IsEnabled() and not btn.userSelected:
                        btn.setUserSelection(True)
                        break
                filteredItems = self.filterItems()
            # Enable all
            elif setting == 2:
                for btn in self.marketBrowser.metaButtons:
                    if btn.IsEnabled() and not btn.userSelected:
                        btn.setUserSelection(True)
                filteredItems = self.filterItems()
        self.filteredStore = filteredItems
        self.update(self.filteredStore)

    def filterItems(self):
        sMkt = self.sMkt
        selectedMetas = set()
        for btn in self.marketBrowser.metaButtons:
            if btn.userSelected:
                selectedMetas.update(sMkt.META_MAP[btn.metaName])
        filteredItems = sMkt.filterItemsByMeta(self.unfilteredStore, selectedMetas)
        return filteredItems

    def setToggles(self):
        metaIDs = set()
        sMkt = self.sMkt
        for item in self.unfilteredStore:
            metaIDs.add(sMkt.getMetaGroupIdByItem(item))

        for btn in self.marketBrowser.metaButtons:
            btn.reset()
            btnMetas = sMkt.META_MAP[btn.metaName]
            if len(metaIDs.intersection(btnMetas)) > 0:
                btn.setMetaAvailable(True)
            else:
                btn.setMetaAvailable(False)

    def scheduleSearch(self, event=None):
        self.searchTimer.Stop()  # Cancel any pending timers
        search = self.marketBrowser.search.GetLineText(0)
        # Make sure we do not count wildcards as search symbol
        realsearch = search.replace('*', '').replace('?', '')
        # Re-select market group if search query has zero length
        if len(realsearch) == 0:
            self.selectionMade('search')
            return

        self.marketBrowser.mode = 'search'
        self.sMkt.searchItems(search, self.populateSearch, 'market')

    def clearSearch(self, event=None):
        # Wipe item store and update everything to accomodate with it
        # If clearSearch was generated by SearchCtrl's Cancel button, clear the content also

        if event:
            self.marketBrowser.search.Clear()

        if self.marketBrowser.mode == 'search':
            self.marketBrowser.mode = 'normal'
            self.updateItemStore(set())
            self.setToggles()
            self.filterItemStore()

    def populateSearch(self, itemIDs):
        # If we're no longer searching, dump the results
        if self.marketBrowser.mode != 'search':
            return
        items = Market.getItems(itemIDs)
        self.updateItemStore(items)
        self.setToggles()
        self.filterItemStore()

    def contextMenu(self, event):
        clickedPos = self.getRowByAbs(event.Position)
        self.ensureSelection(clickedPos)

        # Check if something is selected, if so, spawn the menu for it
        if clickedPos == -1:
            return

        item = self.active[clickedPos]
        sMkt = self.sMkt
        sourceContext = "marketItemMisc" if self.marketBrowser.mode in ("search", "recent") else "marketItemGroup"
        itemContext = sMkt.getCategoryByItem(item).displayName

        menu = ContextMenu.getMenu(self, item, (item,), (sourceContext, itemContext))
        self.PopupMenu(menu)

    def populate(self, items):
        if len(items) > 0:
            # Clear selection
            self.unselectAll()
            # Perform sorting, using item's meta levels besides other stuff
            if self.marketBrowser.mode != 'recent':
                items.sort(key=self.sMkt.itemSort)
        # Mark current item list as active
        self.active = items
        # Show them
        Display.populate(self, items)

    def refresh(self, items):
        if len(items) > 1:
            # Re-sort stuff
            if self.marketBrowser.mode != 'recent':
                items.sort(key=self.sMkt.itemSort)
        for i, item in enumerate(items[:9]):
            # set shortcut info for first 9 modules
            item.marketShortcut = i + 1
        Display.refresh(self, items)

    def columnBackground(self, colItem, item):
        if self.sFit.serviceFittingOptions["colorFitBySlot"]:
            return slotColourMap.get(Module.calculateSlot(item)) or self.GetBackgroundColour()
        else:
            return self.GetBackgroundColour()
