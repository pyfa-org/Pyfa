import wx.gizmos
import gui.fleetBrowser
from gui.bitmapLoader import BitmapLoader

#Tab spawning handler
class FleetSpawner(gui.multiSwitch.TabSpawner):
    def __init__(self, multiSwitch):
        self.multiSwitch = multiSwitch
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        mainFrame.Bind(gui.fleetBrowser.EVT_FLEET_SELECTED, self.fleetSelected)

    def fleetSelected(self, event):
        if self.multiSwitch.GetPageCount() == 0:
            self.multiSwitch.AddPage(wx.Panel(self.multiSwitch, size = (0,0)), "Empty Tab")

        view = FleetView(self.multiSwitch)
        self.multiSwitch.ReplaceActivePage(view)
        view.populate(event.fleetID)
        view.Show()

FleetSpawner.register()

class FleetView(wx.gizmos.TreeListCtrl):
    def __init__(self, parent, size = (0,0)):
        wx.gizmos.TreeListCtrl.__init__(self, parent, size = size)

        self.tabManager = parent

        self.fleetId = None
        self.fleetImg = BitmapLoader.getImage("53_16", "icons")

        self.imageList = wx.ImageList(16, 16)
        self.SetImageList(self.imageList)

        for col in ("", "Fit", "Shiptype", "Character", "Bonusses"):
            self.AddColumn(col)

        self.SetMainColumn(1)
        self.icons = {}
        self.addImage = self.imageList.Add(BitmapLoader.getBitmap("add_small", "gui"))
        for icon in ("fb", "fc", "sb", "sc", "wb", "wc"):
            self.icons[icon] = self.imageList.Add(BitmapLoader.getBitmap("fleet_%s_small" % icon, "gui"))

        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.checkNew)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.mainFrame.Bind(gui.fleetBrowser.EVT_FLEET_RENAMED, self.fleetRenamed)
        self.mainFrame.Bind(gui.fleetBrowser.EVT_FLEET_REMOVED, self.fleetRemoved)

    def Destroy(self):
        self.mainFrame.Unbind(gui.fleetBrowser.EVT_FLEET_REMOVED, handler = self.fleetRemoved)
        self.mainFrame.Unbind(gui.fleetBrowser.EVT_FLEET_RENAMED, handler = self.fleetRenamed)
        wx.gizmos.TreeListCtrl.Destroy(self)

    def fleetRenamed(self, event):
        if event.fleetID == self.fleetId:
            sFleet = service.Fleet.getInstance()
            f = sFleet.getFleetByID(event.fleetID)
            self.UpdateTab(f.name, self.fleetImg)

        event.Skip()

    def fleetRemoved(self, event):
        if event.fleetID == self.fleetId:
            self.tabManager.DeletePage(self.tabManager.GetPageIndex(self))

        event.Skip()

    def checkNew(self, event):
        data = self.GetPyData(event.Item)
        if data and isinstance(data, tuple) and data[0] == "add":
            layer = data[1]


    def UpdateTab(self, name, img):
        self.tabManager.SetPageTextIcon(self.tabManager.GetSelection(), name, img)

    def populate(self, fleetID):
        sFleet = service.Fleet.getInstance()
        f = sFleet.getFleetByID(fleetID)
        self.fleetId = fleetID

        self.UpdateTab( f.name, self.fleetImg)
        self.fleet = f
        self.DeleteAllItems()
        root = self.AddRoot("")

        self.setEntry(root, f.leader, "fleet", f)
        for wing in f.wings:
            wingId = self.AppendItem(root, "")
            self.setEntry(wingId, wing.leader, "wing", wing)
            for squad in wing.squads:
                for member in squad.members:
                    memberId = self.AppendItem(wingId, "")
                    self.setEntry(memberId, member, "squad", squad)

            self.addAdder(wingId, "squad")

        self.addAdder(root, "wing")

        self.ExpandAll(root)
        self.SetColumnWidth(0, 16)
        for i in xrange(1, 5):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            headerWidth = self.GetColumnWidth(i) + 5
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            baseWidth = self.GetColumnWidth(i)
            if baseWidth < headerWidth:
                self.SetColumnWidth(i, headerWidth)
            else:
                self.SetColumnWidth(i, baseWidth)


    def addAdder(self, treeItemId, layer):
        id = self.AppendItem(treeItemId, "Add new %s" % layer.capitalize())
        self.SetPyData(id, ("add", layer))
        self.SetItemImage(id, self.addImage, 1)

    def setEntry(self, treeItemId, fit, layer, info):
        self.SetPyData(treeItemId, info)
        if fit is None:
            self.SetItemText(treeItemId, "%s Commander" % layer.capitalize(), 1)
        else:
            fleet = self.fleet
            if fit == info.booster:
                self.SetItemImage(treeItemId, self.icons["%sb" % layer[0]], 0)
            elif fit == info.leader:
                self.SetItemImage(treeItemId, self.icons["%sc" % layer[0]], 1)

            self.SetItemText(treeItemId, fit.name, 1)
            self.SetItemText(treeItemId, fit.ship.item.name, 2)
            self.SetItemText(treeItemId, fit.character.name, 3)
            boosts = fleet.store.getBoosts(fit)
            if boosts:
                bonusses = []
                for name, info in boosts.iteritems():
                    bonusses.append("%s: %.2g" % (name, info[0]))

                self.SetItemText(treeItemId, ", ".join(bonusses), 3)
