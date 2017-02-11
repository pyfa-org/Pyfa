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
from service.market import Market
from service.attribute import Attribute
from gui.display import Display
import gui.PFSearchBox as SBox
from gui.cachingImageList import CachingImageList
from gui.contextMenu import ContextMenu
from gui.bitmapLoader import BitmapLoader

ItemSelected, ITEM_SELECTED = wx.lib.newevent.NewEvent()

RECENTLY_USED_MODULES = -2
MAX_RECENTLY_USED_MODULES = 20


class MetaButton(wx.ToggleButton):
    def __init__(self, *args, **kwargs):
        super(MetaButton, self).__init__(*args, **kwargs)
        self.setUserSelection(True)

    def setUserSelection(self, isSelected):
        self.userSelected = isSelected
        self.SetValue(isSelected)

    def setMetaAvailable(self, isAvailable):
        self.Enable(isAvailable)
        # need to also SetValue(False) for windows because Enabled=False AND SetValue(True) looks enabled.
        if not isAvailable:
            self.SetValue(False)

    def reset(self):
        self.Enable(True)
        self.SetValue(self.userSelected)


class MarketBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        # Add a search box on top
        self.search = SearchBox(self)
        vbox.Add(self.search, 0, wx.EXPAND)

        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        vbox.Add(self.splitter, 1, wx.EXPAND)

        # Grab market service instance and create child objects
        self.sMkt = Market.getInstance()
        self.searchMode = False
        self.marketView = MarketTree(self.splitter, self)
        self.itemView = ItemView(self.splitter, self)

        self.splitter.SplitHorizontally(self.marketView, self.itemView)
        self.splitter.SetMinimumPaneSize(250)

        # Setup our buttons for metaGroup selection
        # Same fix as for search box on macs,
        # need some pixels of extra space or everything clips and is ugly
        p = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)
        p.SetSizer(box)
        vbox.Add(p, 0, wx.EXPAND)
        self.metaButtons = []
        btn = None
        for name in self.sMkt.META_MAP.keys():
            btn = MetaButton(p, wx.ID_ANY, name.capitalize(), style=wx.BU_EXACTFIT)
            setattr(self, name, btn)
            box.Add(btn, 1, wx.ALIGN_CENTER)
            btn.Bind(wx.EVT_TOGGLEBUTTON, self.toggleMetaButton)
            btn.metaName = name
            self.metaButtons.append(btn)
        # Make itemview to set toggles according to list contents
        self.itemView.setToggles()

        p.SetMinSize((wx.SIZE_AUTO_WIDTH, btn.GetSize()[1] + 5))

    def toggleMetaButton(self, event):
        """Process clicks on toggle buttons"""
        appendMeta = wx.GetMouseState().CmdDown()
        clickedBtn = event.EventObject

        if appendMeta:
            activeBtns = [btn for btn in self.metaButtons if btn.GetValue()]
            if activeBtns:
                clickedBtn.setUserSelection(clickedBtn.GetValue())
                self.itemView.filterItemStore()
            else:
                # Do 'nothing' if we're trying to turn last active button off
                # Keep button in the same state
                clickedBtn.setUserSelection(True)
        else:
            for btn in self.metaButtons:
                btn.setUserSelection(btn == clickedBtn)

            self.itemView.filterItemStore()

    def jump(self, item):
        self.marketView.jump(item)


class SearchBox(SBox.PFSearchBox):
    def __init__(self, parent, **kwargs):
        SBox.PFSearchBox.__init__(self, parent, **kwargs)
        cancelBitmap = BitmapLoader.getBitmap("fit_delete_small", "gui")
        searchBitmap = BitmapLoader.getBitmap("fsearch_small", "gui")
        self.SetSearchBitmap(searchBitmap)
        self.SetCancelBitmap(cancelBitmap)
        self.ShowSearchButton()
        self.ShowCancelButton()


class MarketTree(wx.TreeCtrl):
    def __init__(self, parent, marketBrowser):
        wx.TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        self.root = self.AddRoot("root")

        self.imageList = CachingImageList(16, 16)
        self.SetImageList(self.imageList)

        self.sMkt = marketBrowser.sMkt
        self.marketBrowser = marketBrowser

        # Form market tree root
        sMkt = self.sMkt
        for mktGrp in sMkt.getMarketRoot():
            iconId = self.addImage(sMkt.getIconByMarketGroup(mktGrp))
            childId = self.AppendItem(self.root, mktGrp.name, iconId, data=wx.TreeItemData(mktGrp.ID))
            # All market groups which were never expanded are dummies, here we assume
            # that all root market groups are expandable
            self.AppendItem(childId, "dummy")
        self.SortChildren(self.root)

        # Add recently used modules node
        rumIconId = self.addImage("market_small", "gui")
        self.AppendItem(self.root, "Recently Used Modules", rumIconId, data=wx.TreeItemData(RECENTLY_USED_MODULES))

        # Bind our lookup method to when the tree gets expanded
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)

    def addImage(self, iconFile, location="icons"):
        if iconFile is None:
            return -1
        return self.imageList.GetImageIndex(iconFile, location)

    def expandLookup(self, event):
        """Process market tree expands"""
        root = event.Item
        child = self.GetFirstChild(root)[0]
        # If child of given market group is a dummy
        if self.GetItemText(child) == "dummy":
            # Delete it
            self.Delete(child)
            # And add real market group contents
            sMkt = self.sMkt
            currentMktGrp = sMkt.getMarketGroup(self.GetPyData(root), eager="children")
            for childMktGrp in sMkt.getMarketGroupChildren(currentMktGrp):
                # If market should have items but it doesn't, do not show it
                if sMkt.marketGroupValidityCheck(childMktGrp) is False:
                    continue
                iconId = self.addImage(sMkt.getIconByMarketGroup(childMktGrp))
                try:
                    childId = self.AppendItem(root, childMktGrp.name, iconId, data=wx.TreeItemData(childMktGrp.ID))
                except:
                    continue
                if sMkt.marketGroupHasTypesCheck(childMktGrp) is False:
                    self.AppendItem(childId, "dummy")

            self.SortChildren(root)

    def jump(self, item):
        """Open market group and meta tab of given item"""
        self.marketBrowser.searchMode = False
        sMkt = self.sMkt
        mg = sMkt.getMarketGroupByItem(item)

        jumpList = []
        while mg is not None:
            jumpList.append(mg.ID)
            mg = mg.parent

        for id in sMkt.ROOT_MARKET_GROUPS:
            if id in jumpList:
                jumpList = jumpList[:jumpList.index(id) + 1]

        item = self.root
        for i in range(len(jumpList) - 1, -1, -1):
            target = jumpList[i]
            child, cookie = self.GetFirstChild(item)
            while self.GetItemPyData(child) != target:
                child, cookie = self.GetNextChild(item, cookie)

            item = child
            self.Expand(item)

        self.SelectItem(item)
        self.marketBrowser.itemView.selectionMade()


class ItemView(Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name",
                    "attr:power,,,True",
                    "attr:cpu,,,True"]

    def __init__(self, parent, marketBrowser):
        Display.__init__(self, parent)
        marketBrowser.Bind(wx.EVT_TREE_SEL_CHANGED, self.selectionMade)

        self.unfilteredStore = set()
        self.filteredStore = set()
        self.recentlyUsedModules = set()
        self.sMkt = marketBrowser.sMkt
        self.searchMode = marketBrowser.searchMode

        self.marketBrowser = marketBrowser
        self.marketView = marketBrowser.marketView

        # Make sure our search actually does interesting stuff
        self.marketBrowser.search.Bind(SBox.EVT_TEXT_ENTER, self.scheduleSearch)
        self.marketBrowser.search.Bind(SBox.EVT_SEARCH_BTN, self.scheduleSearch)
        self.marketBrowser.search.Bind(SBox.EVT_CANCEL_BTN, self.clearSearch)
        self.marketBrowser.search.Bind(SBox.EVT_TEXT, self.scheduleSearch)

        # Make sure WE do interesting stuff too
        self.Bind(wx.EVT_CONTEXT_MENU, self.contextMenu)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.itemActivated)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)

        # Make reverse map, used by sorter
        self.metaMap = self.makeReverseMetaMap()

        # Fill up recently used modules set
        for itemID in self.sMkt.serviceMarketRecentlyUsedModules["pyfaMarketRecentlyUsedModules"]:
            self.recentlyUsedModules.add(self.sMkt.getItem(itemID))

    def startDrag(self, event):
        row = self.GetFirstSelected()

        if row != -1:
            data = wx.PyTextDataObject()
            data.SetText("market:" + str(self.active[row].ID))

            dropSource = wx.DropSource(self)
            dropSource.SetData(data)
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
            seldata = self.marketView.GetPyData(sel)
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
        search = self.marketBrowser.search.GetLineText(0)
        # Make sure we do not count wildcard as search symbol
        realsearch = search.replace("*", "")
        # Re-select market group if search query has zero length
        if len(realsearch) == 0:
            self.selectionMade()
            return
        # Show nothing if query is too short
        elif len(realsearch) < 3:
            self.clearSearch()
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
            mktgrpid = None
            print("unable to find market group for", item.name)
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
        for mgids in self.sMkt.META_MAP.itervalues():
            for mgid in mgids:
                revmap[mgid] = i
            i += 1
        return revmap
