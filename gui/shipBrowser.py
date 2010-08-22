import wx
import controller
import bitmapLoader
import gui.mainFrame

class ShipBrowser(wx.Panel):
    def __init__(self, parent):
        self.built = False
        wx.Panel.__init__(self, parent)
        self.viewSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.viewSizer)

        self.shipMenu = ShipMenu(self)
        self.viewSizer.Add(self.shipMenu, 0, wx.EXPAND)

        self.searchView = ShipView(self)
        #self.viewSizer.Add(self.searchView, 1, wx.EXPAND)
        self.searchView.Hide()

        self.shipView = ShipView(self)
        self.viewSizer.Add(self.shipView, 1, wx.EXPAND)

        self.shipImageList = wx.ImageList(16, 16)
        self.shipView.SetImageList(self.shipImageList)
        self.searchView.SetImageList(self.shipImageList)

        self.shipRoot = self.shipView.AddRoot("Ships")
        self.searchRoot = self.searchView.AddRoot("Ships")

        self.raceImageIds = {}
        self.races = ["amarr", "caldari", "gallente", "minmatar", "ore", "serpentis", "angel", "blood", "sansha", "guristas"]
        for race in self.races:
            imageId = self.shipImageList.Add(bitmapLoader.getBitmap("race_%s_small" % race, "icons"))
            self.raceImageIds[race] = imageId

        self.races.append("None")
        self.idRaceMap = {}

        self.shipView.races = self.races
        self.shipView.idRaceMap = self.idRaceMap

        self.searchView.races = self.races
        self.searchView.idRaceMap = self.idRaceMap

        self.build()

        #Bind our lookup methods for our trees
        for tree in (self.shipView, self.searchView):
            tree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)
            tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.toggleButtons)
            tree.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.changeFitName)
            tree.Bind(wx.EVT_LEFT_DCLICK, self.renameOrExpand)

        #Bind buttons
        self.shipMenu.new.Bind(wx.EVT_BUTTON, self.newFit)
        self.shipMenu.rename.Bind(wx.EVT_BUTTON, self.renameFit)
        self.shipMenu.delete.Bind(wx.EVT_BUTTON, self.deleteFit)
        self.shipMenu.copy.Bind(wx.EVT_BUTTON, self.copyFit)

        #Bind search
        self.shipMenu.search.Bind(wx.EVT_TEXT_ENTER, self.startSearch)
        self.shipMenu.search.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.startSearch)
        self.shipMenu.search.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.clearSearch)
        self.shipMenu.search.Bind(wx.EVT_TEXT, self.startSearch)

        self.timer = None

    def build(self):
        if not self.built:
            self.built = True
            cMarket = controller.Market.getInstance()
            shipRoot = cMarket.getShipRoot()
            iconId = self.shipImageList.Add(bitmapLoader.getBitmap("ship_small", "icons"))
            for id, name in shipRoot:
                childId = self.shipView.AppendItem(self.shipRoot, name, iconId, data=wx.TreeItemData(("group", id)))
                self.shipView.AppendItem(childId, "dummy")

        self.shipView.SortChildren(self.shipRoot)

    def getActiveTree(self):
        if self.searchView.IsShown():
            return self.searchView
        else:
            return self.shipView

    def toggleButtons(self, event):
        tree = self.getActiveTree()
        root = tree.GetSelection()
        btns = (self.shipMenu.new, self.shipMenu.rename, self.shipMenu.delete, self.shipMenu.copy)
        if not root.IsOk():
            for btn in btns:
                btn.Enable(False)
        else:
            data = tree.GetPyData(root)
            if data is None:
                return

            type, groupID = data
            if type == "fit":
                for btn in btns:
                    btn.Enable()

            elif  type == "ship":
                for btn in btns:
                    btn.Enable(btn == self.shipMenu.new)

            else:
                for btn in btns:
                    btn.Enable(False)

    def expandLookup(self, event):
        tree = self.getActiveTree()
        root = event.Item
        child, cookie = tree.GetFirstChild(root)
        self.idRaceMap.clear()
        if tree.GetItemText(child) == "dummy":
            tree.Delete(child)

            cMarket = controller.Market.getInstance()
            cFit = controller.Fit.getInstance()

            type, groupID = tree.GetPyData(root)
            if type == "group":
                for id, name, race in cMarket.getShipList(groupID):
                    iconId = self.raceImageIds[race] if race in self.raceImageIds else -1
                    self.idRaceMap[id] = race
                    childId = tree.AppendItem(root, name, iconId, data=wx.TreeItemData(("ship", id)))
                    for fitID, fitName in cFit.getFitsWithShip(id):
                        tree.AppendItem(childId, fitName, -1, data=wx.TreeItemData(("fit", fitID)))

            tree.SortChildren(root)

    def newFit(self, event):
        tree = self.getActiveTree()
        root = tree.GetSelection()
        type, shipID = tree.GetPyData(root)
        if type == "fit":
            root = tree.GetItemParent(root)
            type, shipID = tree.GetPyData(root)

        name = "%s fit" % tree.GetItemText(root)
        cFit = controller.Fit.getInstance()
        fitID = cFit.newFit(shipID, name)
        childId = tree.AppendItem(root, name, -1, data=wx.TreeItemData(("fit", fitID)))
        tree.SetItemText(childId, name)
        tree.SortChildren(root)
        tree.Expand(root)
        tree.SelectItem(childId)
        tree.EditLabel(childId)

    def renameOrExpand(self, event):
        tree = self.getActiveTree()
        root = tree.GetSelection()
        type, _ = tree.GetPyData(root)
        if type == "fit":
            tree.EditLabel(root)

        event.Skip()


    def renameFit(self, event):
        tree = self.getActiveTree()
        root = tree.GetSelection()
        type, _ = tree.GetPyData(root)
        if type == "fit":
            tree.EditLabel(root)

    def changeFitName(self, event):
        tree = self.getActiveTree()
        item = event.Item
        newName = event.Label
        type, fitID = tree.GetPyData(item)
        cFit = controller.Fit.getInstance()
        cFit.renameFit(fitID, newName)
        wx.CallAfter(tree.SortChildren, tree.GetItemParent(item))

    def deleteFit(self, event):
        tree = self.getActiveTree()
        root = tree.GetSelection()
        type, fitID = tree.GetPyData(root)
        if type == "fit":
            cFit = controller.Fit.getInstance()
            cFit.deleteFit(fitID)
            tree.Delete(root)

    def copyFit(self, event):
        tree = self.getActiveTree()
        root = tree.GetSelection()
        type, fitID = tree.GetPyData(root)
        if type == "fit":
            cFit = controller.Fit.getInstance()
            newID = cFit.copyFit(fitID)
            parent = tree.GetItemParent(root)
            name = tree.GetItemText(root)
            childId = tree.AppendItem(parent, name, -1, data=wx.TreeItemData(("fit", newID)))
            tree.SetItemText(childId, name)
            tree.SelectItem(childId)
            tree.EditLabel(childId)

    def clearSearch(self, event, clearText=True):
        if self.getActiveTree() == self.searchView:
            if clearText:
                self.shipMenu.search.Clear()

            self.viewSizer.Replace(self.searchView, self.shipView)

            self.shipView.Show()
            self.searchView.Hide()

            self.viewSizer.Layout()

    def startSearch(self, event):
        search = self.shipMenu.search.GetLineText(0)
        if len(search) < 3:
            self.clearSearch(event, False)
            return

        self.viewSizer.Replace(self.shipView, self.searchView)

        self.shipView.Hide()
        self.searchView.Show()

        self.viewSizer.Layout()

        #GTFO OLD STOOF
        self.searchView.DeleteAllItems()
        self.searchRoot = self.searchView.AddRoot("Search")

        #Get NEW STOOF
        cMarket = controller.Market.getInstance()
        cFit = controller.Fit.getInstance()

        for id, name, race in cMarket.searchShips(search):
            iconId = self.raceImageIds[race] if race in self.raceImageIds else -1
            self.idRaceMap[id] = race
            childId = self.searchView.AppendItem(self.searchRoot, name, iconId, data=wx.TreeItemData(("ship", id)))
            for fitID, fitName in cFit.getFitsWithShip(id):
                self.searchView.AppendItem(childId, fitName, -1, data=wx.TreeItemData(("fit", fitID)))

        # Sort fits by fit name, then ship name
        foundFits = cMarket.searchFits(search)
        foundFits = sorted(foundFits, key=lambda tuple: tuple[2])
        foundFits = sorted(foundFits, key=lambda tuple: tuple[1])
        for id, name, shipName in foundFits:
            iconId = self.shipImageList.Add(bitmapLoader.getBitmap("ship_small", "icons"))
            rowText = name + " (" + shipName + ")"
            self.searchView.AppendItem(self.searchRoot, rowText, iconId, data=wx.TreeItemData(("fit", id)))

        #To make sure that the shipView stays in sync, we'll clear its fits data
        root = self.shipRoot
        child, cookie = self.shipView.GetFirstChild(root)
        while child.IsOk():
            self.shipView.DeleteChildren(child)
            self.shipView.AppendItem(child, "dummy")
            self.shipView.Collapse(child)
            child, cookie = self.shipView.GetNextChild(root, cookie)


class ShipView(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent)
        treeStyle = self.GetWindowStyleFlag()
        treeStyle |= wx.TR_HIDE_ROOT
        self.SetWindowStyleFlag(treeStyle)

    def OnCompareItems(self, treeId1, treeId2):
        child, cookie = self.GetFirstChild(treeId1)
        type1, id1 = self.GetPyData(treeId1)
        type2, id2 = self.GetPyData(treeId2)
        if type1 in ("fit", "group"):
            return cmp(self.GetItemText(treeId1), self.GetItemText(treeId2))
        else:
            c = cmp(self.races.index(self.idRaceMap[id1] or "None"), self.races.index(self.idRaceMap[id2] or "None"))
            if c != 0:
                return c
            else:
                return cmp(self.GetItemText(treeId1), self.GetItemText(treeId2))

class ShipMenu(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)

        size = None
        for name, art in (("new", wx.ART_NEW), ("rename", bitmapLoader.getBitmap("rename", "icons")), ("copy", wx.ART_COPY), ("delete", wx.ART_DELETE)):
            bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON) if name != "rename" else art
            btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)
            if size is None:
                size = btn.GetSize()

            btn.SetMinSize(size)
            btn.SetMaxSize(size)

            btn.Layout()
            setattr(self, name, btn)
            btn.Enable(False)
            btn.SetToolTipString("%s fit." % name.capitalize())
            sizer.Add(btn, 0, wx.EXPAND)

        p = wx.Panel(self)
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        p.SetSizer(psizer)

        self.search = wx.SearchCtrl(p, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        psizer.Add(self.search, 1, wx.EXPAND | wx.TOP, 2)
        p.SetMinSize((wx.SIZE_AUTO_WIDTH, 27))
        sizer.Add(p, 1, wx.EXPAND)

