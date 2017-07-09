# noinspection PyPackageRequirements
import wx
# noinspection PyPackageRequirements
from wx.lib.buttons import GenBitmapButton

import gui.builtinMarketBrowser.pfSearchBox as SBox
import gui.display as d
from gui.bitmapLoader import BitmapLoader
from gui.marketBrowser import SearchBox
from service.market import Market


class BaseImplantEditorView(wx.Panel):
    def addMarketViewImage(self, iconFile):
        if iconFile is None:
            return -1
        bitmap = BitmapLoader.getBitmap(iconFile, "icons")
        if bitmap is None:
            return -1
        else:
            return self.availableImplantsImageList.Add(bitmap)

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))

        pmainSizer = wx.BoxSizer(wx.HORIZONTAL)

        availableSizer = wx.BoxSizer(wx.VERTICAL)

        self.searchBox = SearchBox(self)
        self.itemView = ItemView(self)

        self.itemView.Hide()

        availableSizer.Add(self.searchBox, 0, wx.EXPAND)
        availableSizer.Add(self.itemView, 1, wx.EXPAND)

        '''
        self.availableImplantsSearch = wx.SearchCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.availableImplantsSearch.ShowCancelButton(True)

        availableSizer.Add(self.availableImplantsSearch, 0, wx.BOTTOM | wx.EXPAND, 2)
        '''

        self.availableImplantsTree = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        root = self.availableRoot = self.availableImplantsTree.AddRoot("Available")
        self.availableImplantsImageList = wx.ImageList(16, 16)
        self.availableImplantsTree.SetImageList(self.availableImplantsImageList)

        availableSizer.Add(self.availableImplantsTree, 1, wx.EXPAND)

        pmainSizer.Add(availableSizer, 1, wx.ALL | wx.EXPAND, 5)

        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer.AddSpacer((0, 0), 1)

        self.btnAdd = GenBitmapButton(self, wx.ID_ADD, BitmapLoader.getBitmap("fit_add_small", "gui"),
                                      style=wx.BORDER_NONE)
        buttonSizer.Add(self.btnAdd, 0)

        self.btnRemove = GenBitmapButton(self, wx.ID_REMOVE, BitmapLoader.getBitmap("fit_delete_small", "gui"),
                                         style=wx.BORDER_NONE)
        buttonSizer.Add(self.btnRemove, 0)

        buttonSizer.AddSpacer((0, 0), 1)
        pmainSizer.Add(buttonSizer, 0, wx.EXPAND, 0)

        characterImplantSizer = wx.BoxSizer(wx.VERTICAL)
        self.pluggedImplantsTree = AvailableImplantsView(self)
        characterImplantSizer.Add(self.pluggedImplantsTree, 1, wx.ALL | wx.EXPAND, 5)
        pmainSizer.Add(characterImplantSizer, 1, wx.EXPAND, 5)

        self.SetSizer(pmainSizer)

        # Populate the market tree

        sMkt = Market.getInstance()
        for mktGrp in sMkt.getImplantTree():
            iconId = self.addMarketViewImage(sMkt.getIconByMarketGroup(mktGrp))
            childId = self.availableImplantsTree.AppendItem(root, mktGrp.name, iconId, data=wx.TreeItemData(mktGrp.ID))
            if sMkt.marketGroupHasTypesCheck(mktGrp) is False:
                self.availableImplantsTree.AppendItem(childId, "dummy")

        self.availableImplantsTree.SortChildren(self.availableRoot)

        # Bind the event to replace dummies by real data
        self.availableImplantsTree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)
        self.availableImplantsTree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.itemSelected)

        self.itemView.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.itemSelected)

        # Bind add & remove buttons
        self.btnAdd.Bind(wx.EVT_BUTTON, self.itemSelected)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.removeItem)

        # We update with an empty list first to set the initial size for Layout(), then update later with actual
        # implants for character. This helps with sizing issues.
        self.pluggedImplantsTree.update([])
        self.bindContext()
        self.Layout()

        self.update()

    def bindContext(self):
        # Binds self.contextChanged to whatever changes the context
        raise NotImplementedError()

    def getImplantsFromContext(self):
        """ Gets list of implants from current context """
        raise NotImplementedError()

    def addImplantToContext(self, item):
        """ Adds implant to the current context"""
        raise NotImplementedError()

    def removeImplantFromContext(self, implant):
        """ Removes implant from the current context"""
        raise NotImplementedError()

    def update(self):
        """Updates implant list based off the current context"""
        self.implants = self.getImplantsFromContext()
        self.implants.sort(key=lambda i: int(i.getModifiedItemAttr("implantness")))
        self.pluggedImplantsTree.update(self.implants)

    def contextChanged(self, event):
        self.update()
        event.Skip()

    def expandLookup(self, event):
        tree = self.availableImplantsTree
        sMkt = Market.getInstance()
        parent = event.Item
        child, _ = tree.GetFirstChild(parent)
        text = tree.GetItemText(child)

        if text == "dummy" or text == "itemdummy":
            tree.Delete(child)

        # if the dummy item is a market group, replace with actual market groups
        if text == "dummy":
            # Add 'real stoof!' instead
            currentMktGrp = sMkt.getMarketGroup(tree.GetPyData(parent), eager="children")
            for childMktGrp in sMkt.getMarketGroupChildren(currentMktGrp):
                iconId = self.addMarketViewImage(sMkt.getIconByMarketGroup(childMktGrp))
                childId = tree.AppendItem(parent, childMktGrp.name, iconId, data=wx.TreeItemData(childMktGrp.ID))
                if sMkt.marketGroupHasTypesCheck(childMktGrp) is False:
                    tree.AppendItem(childId, "dummy")
                else:
                    tree.AppendItem(childId, "itemdummy")

        # replace dummy with actual items
        if text == "itemdummy":
            currentMktGrp = sMkt.getMarketGroup(tree.GetPyData(parent))
            items = sMkt.getItemsByMarketGroup(currentMktGrp)
            for item in items:
                iconId = self.addMarketViewImage(item.icon.iconFile)
                tree.AppendItem(parent, item.name, iconId, data=wx.TreeItemData(item))

        tree.SortChildren(parent)

    def itemSelected(self, event):
        if event.EventObject is self.btnAdd:
            # janky fix that sets EventObject so that we don't have similar code elsewhere.
            if self.itemView.IsShown():
                event.EventObject = self.itemView
            else:
                event.EventObject = self.availableImplantsTree

        if event.EventObject is self.itemView:
            curr = event.EventObject.GetFirstSelected()

            while curr != -1:
                item = self.itemView.items[curr]
                self.addImplantToContext(item)

                curr = event.EventObject.GetNextSelected(curr)
        else:
            root = self.availableImplantsTree.GetSelection()

            if not root.IsOk():
                return

            nchilds = self.availableImplantsTree.GetChildrenCount(root)
            if nchilds == 0:
                item = self.availableImplantsTree.GetPyData(root)
                self.addImplantToContext(item)
            else:
                event.Skip()
                return

        self.update()

    def removeItem(self, event):
        pos = self.pluggedImplantsTree.GetFirstSelected()
        if pos != -1:
            self.removeImplantFromContext(self.implants[pos])
            self.update()


class AvailableImplantsView(d.Display):
    DEFAULT_COLS = ["attr:implantness",
                    "Base Icon",
                    "Base Name"]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.LC_SINGLE_SEL)
        self.Bind(wx.EVT_LEFT_DCLICK, parent.removeItem)


class ItemView(d.Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name",
                    "attr:power,,,True",
                    "attr:cpu,,,True"]

    def __init__(self, parent):
        d.Display.__init__(self, parent)
        self.parent = parent
        self.searchBox = parent.searchBox

        self.items = []

        # Bind search actions
        self.searchBox.Bind(SBox.EVT_TEXT_ENTER, self.scheduleSearch)
        self.searchBox.Bind(SBox.EVT_SEARCH_BTN, self.scheduleSearch)
        self.searchBox.Bind(SBox.EVT_CANCEL_BTN, self.clearSearch)
        self.searchBox.Bind(SBox.EVT_TEXT, self.scheduleSearch)

    def clearSearch(self, event=None):
        if self.IsShown():
            self.parent.availableImplantsTree.Show()
            self.Hide()
            self.parent.Layout()

        if event:
            self.searchBox.Clear()

        self.items = []
        self.update(self.items)

    def scheduleSearch(self, event=None):
        sMkt = Market.getInstance()

        search = self.searchBox.GetLineText(0)
        # Make sure we do not count wildcard as search symbol
        realsearch = search.replace("*", "")
        # Show nothing if query is too short
        if len(realsearch) < 3:
            self.clearSearch()
            return

        sMkt.searchItems(search, self.populateSearch, ["Implant"])

    def populateSearch(self, items):
        if not self.IsShown():
            self.parent.availableImplantsTree.Hide()
            self.Show()
            self.parent.Layout()

        self.items = sorted(list(items), key=lambda i: i.name)

        self.update(self.items)
