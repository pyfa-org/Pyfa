import wx
import service
import bitmapLoader
import gui.mainFrame
import  wx.lib.newevent

FitCreated, EVT_FIT_CREATED = wx.lib.newevent.NewEvent()
FitRenamed, EVT_FIT_RENAMED = wx.lib.newevent.NewEvent()
FitRemoved, EVT_FIT_REMOVED = wx.lib.newevent.NewEvent()
FitSelected, EVT_FIT_SELECTED = wx.lib.newevent.NewEvent()

class ShipBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.built = False
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
        self.fitIconId = self.shipImageList.Add(bitmapLoader.getBitmap("fit_small", "icons"))
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
            tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.triggerFitSelect)

        #Bind buttons
        self.shipMenu.new.Bind(wx.EVT_BUTTON, self.newFit)
        self.shipMenu.rename.Bind(wx.EVT_BUTTON, self.renameFit)
        self.shipMenu.delete.Bind(wx.EVT_BUTTON, self.deleteFit)
        self.shipMenu.copy.Bind(wx.EVT_BUTTON, self.copyFit)

        #Bind search
        self.shipMenu.search.Bind(wx.EVT_TEXT_ENTER, self.scheduleSearch)
        self.shipMenu.search.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.scheduleSearch)
        self.shipMenu.search.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.clearSearch)
        self.shipMenu.search.Bind(wx.EVT_TEXT, self.scheduleSearch)
        self.Bind(wx.EVT_TIMER, self.startSearch)

        self.searchTimer = wx.Timer(self)

        self.timer = None

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def build(self):
        if not self.built:
            self.built = True
            cMarket = service.Market.getInstance()
            shipRoot = cMarket.getShipRoot()
            iconId = self.shipImageList.Add(bitmapLoader.getBitmap("ship_small", "icons"))
            for id, name in shipRoot:
                childId = self.shipView.AppendItem(self.shipRoot, name, iconId, data=wx.TreeItemData(("group", id)))
                self.shipView.AppendItem(childId, "dummy")

        self.shipView.SortChildren(self.shipRoot)

    def getActiveTree(self):
        if self.searchView:
            if self.searchView.IsShown():
                return self.searchView
            else:
                return self.shipView

    def triggerFitSelect(self, event):
        selection = event.Item
        if selection.IsOk():
            tree = self.getActiveTree()
            data = tree.GetPyData(selection)
            if data is not None:
                type, fitID = data
                if type == "fit":
                    if self.mainFrame.getActiveFit() != fitID:
                        wx.PostEvent(self.mainFrame, FitSelected(fitID=fitID))

        event.Skip()

    def toggleButtons(self, event):
        tree = self.getActiveTree()
        if tree is None:
            return
        root = tree.GetSelection()
        btns = (self.shipMenu.new, self.shipMenu.rename, self.shipMenu.delete, self.shipMenu.copy)
        if not root.IsOk():
            for btn in btns:
                btn.Enable(False)
        else:
            data = tree.GetPyData(root)
            if data is None:
                return

            type, fitID = data
            if type == "fit":
                for btn in btns:
                    btn.Enable()

            elif type == "ship":
                for btn in btns:
                    btn.Enable(btn == self.shipMenu.new)

            else:
                for btn in btns:
                    btn.Enable(False)

        event.Skip()

    def expandLookup(self, event):
        tree = self.getActiveTree()
        root = event.Item
        child, cookie = tree.GetFirstChild(root)
        self.idRaceMap.clear()
        if tree.GetItemText(child) == "dummy":
            tree.Delete(child)

            cMarket = service.Market.getInstance()
            cFit = service.Fit.getInstance()

            type, groupID = tree.GetPyData(root)
            if type == "group":
                for id, name, race in cMarket.getShipList(groupID):
                    iconId = self.raceImageIds[race] if race in self.raceImageIds else -1
                    self.idRaceMap[id] = race
                    childId = tree.AppendItem(root, name, iconId, data=wx.TreeItemData(("ship", id)))
                    for fitID, fitName in cFit.getFitsWithShip(id):
                        tree.AppendItem(childId, fitName, self.fitIconId, data=wx.TreeItemData(("fit", fitID)))

            tree.SortChildren(root)

        event.Skip()

    def newFit(self, event):
        tree = self.getActiveTree()
        root = tree.GetSelection()
        type, shipID = tree.GetPyData(root)
        cFit = service.Fit.getInstance()
        noChildren = False
        if type == "fit":
            fit = cFit.getFit(shipID)
            type, shipID = "ship", fit.ship.item.ID
            name = "%s fit" % fit.ship.item.name
            if tree == self.searchView:
                root = self.searchRoot
                noChildren = True
        else:
            name = "%s fit" % tree.GetItemText(root)

        fitID = cFit.newFit(shipID, name)
        childId = tree.AppendItem(root, name, self.fitIconId, data=wx.TreeItemData(("fit", fitID)))
        tree.SetItemText(childId, name)
        if not noChildren:
            tree.SortChildren(root)
            tree.Expand(root)

        tree.SelectItem(childId)
        tree.EditLabel(childId)

        wx.PostEvent(self.mainFrame, FitCreated(fitID=fitID))

    def renameFit(self, event):
        tree = self.getActiveTree()
        root = tree.GetSelection()
        type, _ = tree.GetPyData(root)
        if type == "fit":
            tree.EditLabel(root)

        event.Skip()

    def changeFitName(self, event):
        self.triggerFitSelect(event)
        if event.IsEditCancelled():
            return

        tree = self.getActiveTree()
        item = event.Item
        newName = event.Label
        type, fitID = tree.GetPyData(item)
        cFit = service.Fit.getInstance()
        cFit.renameFit(fitID, newName)

        if tree == self.searchView:
            def checkRename(item):
                type, id = tree.GetPyData(item)
                if type == "fit" and id == fitID:
                    if tree.GetItemParent(item) == self.searchRoot:
                        tree.SetItemText(item, "%s (%s)" % (newName, cFit.getFit(fitID).ship.item.name))
                    else:
                        tree.SetItemText(item, newName)

            self.checkSearchView(checkRename)

        wx.CallAfter(tree.SortChildren, tree.GetItemParent(item))

        wx.PostEvent(self.mainFrame, FitRenamed(fitID=fitID))

    def deleteFit(self, event):
        tree = self.getActiveTree()
        root = tree.GetSelection()
        type, fitID = tree.GetPyData(root)
        if type == "fit":
            cFit = service.Fit.getInstance()
            cFit.deleteFit(fitID)
            tree.Delete(root)

        if tree == self.searchView:
            def checkRemoval(item):
                type, id = tree.GetPyData(item)
                if type == "fit" and id == fitID:
                    tree.Delete(item)

            self.checkSearchView(checkRemoval)
        wx.PostEvent(self.mainFrame, FitRemoved(fitID=fitID))

    def checkSearchView(self, callback):
        tree = self.searchView
        item, cookie = tree.GetFirstChild(self.searchRoot)
        while item.IsOk():
            type, id = tree.GetPyData(item)
            if type == "ship":
                child, childCookie = tree.GetFirstChild(item)
                while child.IsOk():
                    callback(child)
                    child, childCookie = tree.GetNextChild(child, childCookie)

            callback(item)
            item, cookie = tree.GetNextChild(item, cookie)

    def copyFit(self, event):
        tree = self.getActiveTree()
        root = tree.GetSelection()
        type, fitID = tree.GetPyData(root)
        if type == "fit":
            cFit = service.Fit.getInstance()
            newID = cFit.copyFit(fitID)
            parent = tree.GetItemParent(root)
            newFit= cFit.getFit(newID)
            name = newFit.name
            iconID = tree.GetItemImage(root)
            childId = tree.AppendItem(parent, name, iconID, data=wx.TreeItemData(("fit", newID)))
            tree.SetItemText(childId, name)
            tree.SelectItem(childId)
            tree.EditLabel(childId)

        wx.PostEvent(self.mainFrame, FitCreated(fitID=newID))

    def scheduleSearch(self, event):
        self.searchTimer.Stop()
        self.searchTimer.Start(50, wx.TIMER_ONE_SHOT)
        event.Skip()

    def clearSearch(self, event, clearText=True):
        if self.getActiveTree() == self.searchView:
            if clearText:
                self.shipMenu.search.Clear()

            self.viewSizer.Replace(self.searchView, self.shipView)

            self.shipView.Show()
            self.searchView.Hide()

            self.viewSizer.Layout()

        event.Skip()

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
        cMarket = service.Market.getInstance()
        cFit = service.Fit.getInstance()

        for id, name, race in cMarket.searchShips(search):
            iconId = self.raceImageIds[race] if race in self.raceImageIds else -1
            self.idRaceMap[id] = race
            childId = self.searchView.AppendItem(self.searchRoot, name, iconId, data=wx.TreeItemData(("ship", id)))
            for fitID, fitName in cFit.getFitsWithShip(id):
                self.searchView.AppendItem(childId, fitName, self.fitIconId, data=wx.TreeItemData(("fit", fitID)))

        foundFits = cMarket.searchFits(search)
        if foundFits:
            for id, name, shipName in foundFits:
                rowText = "{0} ({1})".format(name, shipName)
                self.searchView.AppendItem(self.searchRoot, rowText, self.fitIconId, data=wx.TreeItemData(("fit", id)))

        self.searchView.SortChildren(self.searchRoot)

        #To make sure that the shipView stays in sync, we'll clear its fits data
        root = self.shipRoot
        child, cookie = self.shipView.GetFirstChild(root)
        while child.IsOk():
            self.shipView.DeleteChildren(child)
            self.shipView.AppendItem(child, "dummy")
            self.shipView.Collapse(child)
            child, cookie = self.shipView.GetNextChild(root, cookie)

        if event is not None:
            event.Skip()

    def getSelectedFitID(self):
        tree = self.getActiveTree()
        selection = tree.GetSelection()
        if selection.IsOk():
            data = tree.GetPyData(selection)
            if data is not None:
                type, fitID = data
                if type == "fit":
                    return fitID


class ShipView(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.TR_EDIT_LABELS)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.vetoEdit)
        self.rename = False

    def OnCompareItems(self, treeId1, treeId2):
        child, cookie = self.GetFirstChild(treeId1)
        type1, id1 = self.GetPyData(treeId1)
        type2, id2 = self.GetPyData(treeId2)
        if type1 != type2:
            order = ["group", "ship", "fit"]
            return cmp(order.index(type1), order.index(type2))

        if type1 in ("fit", "group"):
            return cmp(self.GetItemText(treeId1), self.GetItemText(treeId2))
        else:
            c = cmp(self.races.index(self.idRaceMap.get(id1) or "None"), self.races.index(self.idRaceMap.get(id2) or "None"))
            if c != 0:
                return c
            else:
                return cmp(self.GetItemText(treeId1), self.GetItemText(treeId2))

    def OnEraseBackGround(self, event):
        #Prevent flicker by not letting the parent's method get called.
        pass

    def EditLabel(self, childId):
        self.rename = True
        wx.TreeCtrl.EditLabel(self, childId)

    def vetoEdit(self, event):
        if not self.rename:
            event.Veto()

        self.rename = False

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
            btn.SetToolTipString("%s fit" % name.capitalize())
            sizer.Add(btn, 0, wx.EXPAND)

        p = wx.Panel(self)
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        p.SetSizer(psizer)

        self.search = wx.SearchCtrl(p, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        psizer.Add(self.search, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
#        p.SetMinSize((wx.SIZE_AUTO_WIDTH, 27))
        sizer.Add(p, 1, wx.EXPAND)

