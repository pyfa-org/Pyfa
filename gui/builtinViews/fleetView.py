import wx.gizmos
import gui.fleetBrowser
import service

#Tab spawning handler
class FleetSpawner(gui.multiSwitch.TabSpawner):
    def __init__(self, multiSwitch):
        self.multiSwitch = multiSwitch
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        mainFrame.Bind(gui.fleetBrowser.EVT_FLEET_SELECTED, self.fleetSelected)

    def fleetSelected(self, event):
        view = FleetView(self.multiSwitch)
        self.multiSwitch.ReplaceActivePage(view)
        view.populate(event.fleetID)
        view.Show()

FleetSpawner.register()

class FleetView(wx.gizmos.TreeListCtrl):
    def __init__(self, parent):
        wx.gizmos.TreeListCtrl.__init__(self, parent)

        self.tabManager = parent
        self.imageList = wx.ImageList(16, 16)
        self.SetImageList(self.imageList)

        for col in ("Fit", "Shiptype", "Character", "Bonusses"):
            self.AddColumn(col)

        self.SetMainColumn(0)

    def populate(self, fleetID):
        sFleet = service.Fleet.getInstance()
        f = sFleet.getFleet(fleetID)
        self.tabManager.SetPageTextIcon(self.tabManager.GetSelection(), f.name)
        self.fleet = f
        self.DeleteAllItems()
        root = self.AddRoot("")

        self.setEntry(root, f.leader)

    def setEntry(self, treeItemId, fit):
        if fit is None:
            self.SetItemText(treeItemId, "Empty", 0)
        else:
            fleet = self.fleet
            self.SetItemText(treeItemId, fit.name, 0)
            self.SetItemText(treeItemId, fit.ship.item.name, 1)
            self.SetItemText(treeItemId, fit.character.name, 2)
            boosts = fleet.store.getBoosts(fit)
            if boosts:
                bonusses = []
                for name, info in boosts.iteritems():
                    bonusses.append("%s: %.2g" % (name, info[0]))

                self.SetItemText(treeItemId, ", ".join(bonusses), 3)
