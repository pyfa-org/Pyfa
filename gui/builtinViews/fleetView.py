import wx.gizmos
import gui.fleetBrowser
import service
from gui import bitmapLoader

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
        self.imageList = wx.ImageList(16, 16)
        self.SetImageList(self.imageList)

        for col in ("", "Fit", "Shiptype", "Character", "Bonusses"):
            self.AddColumn(col)

        self.SetMainColumn(1)

        self.icons = {}
        for icon in ("fb", "fc", "sb", "sc", "wb", "wc"):
            self.icons[icon] = self.imageList.Add(bitmapLoader.getBitmap("fleet_%s_small" % icon, "icons"))

    def populate(self, fleetID):
        sFleet = service.Fleet.getInstance()
        f = sFleet.getFleet(fleetID)
        self.tabManager.SetPageTextIcon(self.tabManager.GetSelection(), f.name)
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

        self.SetColumnWidth(0, 16)
        for i in xrange(1, 5):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            headerWidth = self.GetColumnWidth(i)
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            baseWidth = self.GetColumnWidth(i)
            if baseWidth < headerWidth:
                self.SetColumnWidth(i, headerWidth)


    def setEntry(self, treeItemId, fit, layer, info):
        if fit is None:
            self.SetItemText(treeItemId, "Empty", 0)
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
