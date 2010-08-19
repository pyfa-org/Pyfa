import wx
import controller
import bitmapLoader

class ShipBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        self.shipView = ShipView(self)
        vbox.Add(self.shipView, 1, wx.EXPAND)

        self.shipImageList = wx.ImageList(16, 16)
        self.shipView.SetImageList(self.shipImageList)

        self.shipRoot = self.shipView.AddRoot("Ships")

        iconId = self.shipImageList.Add(bitmapLoader.getBitmap("ship_small", "icons"))

        cMarket = controller.Market.getInstance()
        shipRoot = cMarket.getShipRoot()
        for id, name in shipRoot:
            childId = self.shipView.AppendItem(self.shipRoot, name, iconId, data=wx.TreeItemData(id))
            self.shipView.AppendItem(childId, "dummy")

        self.shipView.SortChildren(self.shipRoot)

        self.raceImageIds = {}
        self.races = ["amarr", "caldari", "gallente", "minmatar", "ore", "serpentis", "angel", "blood", "sansha", "guristas"]
        for race in self.races:
            imageId = self.shipImageList.Add(bitmapLoader.getBitmap("race_%s_small" % race, "icons"))
            self.raceImageIds[race] = imageId

        self.races.append("None")
        #Bind our lookup method to when the tree gets expanded
        self.shipView.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)
        self.idRaceMap = {}
        self.shipView.races = self.races
        self.shipView.idRaceMap = self.idRaceMap

    def expandLookup(self, event):
        root = event.Item
        child, cookie = self.shipView.GetFirstChild(root)
        self.idRaceMap.clear()
        if self.shipView.GetItemText(child) == "dummy":
            self.shipView.Delete(child)

            cMarket = controller.Market.getInstance()

            for id, name, race in cMarket.getShipList(self.shipView.GetPyData(root)):
                iconId = self.raceImageIds[race] if race in self.raceImageIds else -1
                self.idRaceMap[id] = race
                self.shipView.AppendItem(root, name, iconId, data=wx.TreeItemData(id))

            self.shipView.SortChildren(root)

class ShipView(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent)
        treeStyle = self.GetWindowStyleFlag()
        treeStyle |= wx.TR_HIDE_ROOT
        self.SetWindowStyleFlag(treeStyle)

    def OnCompareItems(self, treeId1, treeId2):
        child, cookie = self.GetFirstChild(treeId1)
        if child.IsOk():
            return cmp(self.GetItemText(treeId1), self.GetItemText(treeId2))
        else:
            id1 = self.GetPyData(treeId1)
            id2 = self.GetPyData(treeId2)
            c = cmp(self.races.index(self.idRaceMap[id1] or "None"), self.races.index(self.idRaceMap[id2] or "None"))
            if c != 0:
                return c
            else:
                return cmp(self.GetItemText(treeId1), self.GetItemText(treeId2))
