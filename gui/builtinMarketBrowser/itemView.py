import wx

import config
import gui.builtinMarketBrowser.pfSearchBox as SBox
from gui.contextMenu import ContextMenu
from gui.display import Display
from service.attribute import Attribute
from service.fit import Fit
from gui.utils.staticHelpers import DragDropHelper

from logbook import Logger

from gui.builtinMarketBrowser.events import RECENTLY_USED_MODULES, MAX_RECENTLY_USED_MODULES, ItemSelected

pyfalog = Logger(__name__)


class ItemView(Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name",
                    "attr:power,,,True",
                    "attr:cpu,,,True"]

    def __init__(self, parent, marketBrowser):
        Display.__init__(self, parent)
        pyfalog.debug("Initialize ItemView")
        marketBrowser.Bind(wx.EVT_TREE_SEL_CHANGED, self.selectionMade)

        self.unfilteredStore = set()
        self.filteredStore = set()
        self.recentlyUsedModules = set()
        self.sMkt = marketBrowser.sMkt
        self.searchMode = marketBrowser.searchMode

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

        # Make reverse map, used by sorter
        self.metaMap = self.makeReverseMetaMap()

        # Fill up recently used modules set
        pyfalog.debug("Fill up recently used modules set")
        for itemID in self.sMkt.serviceMarketRecentlyUsedModules["pyfaMarketRecentlyUsedModules"]:
            self.recentlyUsedModules.add(self.sMkt.getItem(itemID))

    def delaySearch(self, evt):
        sFit = Fit.getInstance()
        self.searchTimer.Stop()
        self.searchTimer.Start(sFit.serviceFittingOptions["marketSearchDelay"], True)  # 150ms

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

            self.storeRecentlyUsedMarketItem(self.active[sel].ID)
            self.recentlyUsedModules = set()
            for itemID in self.sMkt.serviceMarketRecentlyUsedModules["pyfaMarketRecentlyUsedModules"]:
                self.recentlyUsedModules.add(self.sMkt.getItem(itemID))

            wx.PostEvent(self.mainFrame, ItemSelected(itemID=self.active[sel].ID))

    def storeRecentlyUsedMarketItem(self, itemID):
        if len(self.sMkt.serviceMarketRecentlyUsedModules["pyfaMarketRecentlyUsedModules"]) > MAX_RECENTLY_USED_MODULES:
            self.sMkt.serviceMarketRecentlyUsedModules["pyfaMarketRecentlyUsedModules"].pop(0)

        self.sMkt.serviceMarketRecentlyUsedModules["pyfaMarketRecentlyUsedModules"].append(itemID)

    def selectionMade(self, event=None):
        self.marketBrowser.searchMode = False
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
                    items = self.recentlyUsedModules
                else:
                    items = set()

            # Fill store
            self.updateItemStore(items)

            # Set toggle buttons / use search mode flag if recently used modules category is selected (in order to have all modules listed and not filtered)
            if seldata is not RECENTLY_USED_MODULES:
                self.setToggles()
            else:
                self.marketBrowser.searchMode = True
                self.setToggles()

            # Update filtered items
            self.filterItemStore()

    def updateItemStore(self, items):
        self.unfilteredStore = items

    def filterItemStore(self):
        sMkt = self.sMkt
        selectedMetas = set()
        for btn in self.marketBrowser.metaButtons:
            if btn.GetValue():
                selectedMetas.update(sMkt.META_MAP[btn.metaName])
        self.filteredStore = sMkt.filterItemsByMeta(self.unfilteredStore, selectedMetas)
        self.update(list(self.filteredStore))

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
        # Make sure we do not count wildcard as search symbol
        realsearch = search.replace("*", "")
        # Re-select market group if search query has zero length
        if len(realsearch) == 0:
            self.selectionMade()
            return

        self.marketBrowser.searchMode = True
        self.sMkt.searchItems(search, self.populateSearch)

    def clearSearch(self, event=None):
        # Wipe item store and update everything to accomodate with it
        # If clearSearch was generated by SearchCtrl's Cancel button, clear the content also

        if event:
            self.marketBrowser.search.Clear()

        self.marketBrowser.searchMode = False
        self.updateItemStore(set())
        self.setToggles()
        self.filterItemStore()

    def populateSearch(self, items):
        # If we're no longer searching, dump the results
        if self.marketBrowser.searchMode is False:
            return
        self.updateItemStore(items)
        self.setToggles()
        self.filterItemStore()

    def itemSort(self, item):
        sMkt = self.sMkt
        catname = sMkt.getCategoryByItem(item).name
        try:
            mktgrpid = sMkt.getMarketGroupByItem(item).ID
        except AttributeError:
            mktgrpid = -1
            print(("unable to find market group for", item.name))
        parentname = sMkt.getParentItemByItem(item).name
        # Get position of market group
        metagrpid = sMkt.getMetaGroupIdByItem(item)
        metatab = self.metaMap.get(metagrpid)
        metalvl = self.metalvls.get(item.ID, 0)

        return catname, mktgrpid, parentname, metatab, metalvl, item.name

    def contextMenu(self, event):
        # Check if something is selected, if so, spawn the menu for it
        sel = self.GetFirstSelected()
        if sel == -1:
            return

        item = self.active[sel]

        sMkt = self.sMkt
        sourceContext = "marketItemGroup" if self.marketBrowser.searchMode is False else "marketItemMisc"
        itemContext = sMkt.getCategoryByItem(item).name

        menu = ContextMenu.getMenu((item,), (sourceContext, itemContext))
        self.PopupMenu(menu)

    def populate(self, items):
        if len(items) > 0:
            # Get dictionary with meta level attribute
            sAttr = Attribute.getInstance()
            attrs = sAttr.getAttributeInfo("metaLevel")
            sMkt = self.sMkt
            self.metalvls = sMkt.directAttrRequest(items, attrs)
            # Clear selection
            self.deselectItems()
            # Perform sorting, using item's meta levels besides other stuff
            items.sort(key=self.itemSort)
        # Mark current item list as active
        self.active = items
        # Show them
        Display.populate(self, items)

    def refresh(self, items):
        if len(items) > 1:
            # Get dictionary with meta level attribute
            sAttr = Attribute.getInstance()
            attrs = sAttr.getAttributeInfo("metaLevel")
            sMkt = self.sMkt
            self.metalvls = sMkt.directAttrRequest(items, attrs)
            # Re-sort stuff
            items.sort(key=self.itemSort)

        for i, item in enumerate(items[:9]):
            # set shortcut info for first 9 modules
            item.marketShortcut = i + 1

        Display.refresh(self, items)

    def makeReverseMetaMap(self):
        """
        Form map which tells in which tab items of given metagroup are located
        """
        revmap = {}
        i = 0
        for mgids in self.sMkt.META_MAP.values():
            for mgid in mgids:
                revmap[mgid] = i
            i += 1
        return revmap
