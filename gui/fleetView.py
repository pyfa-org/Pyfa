import wx.gizmos
import gui.fleetBrowser

#Tab spawning handler
class FleetSpawner(gui.multiSwitch.TabSpawner):
    def __init__(self, multiSwitch):
        self.multiSwitch = multiSwitch
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        mainFrame.Bind(gui.fleetBrowser.EVT_FLEET_SELECTED, self.fleetSelected)

    def fleetSelected(self, event):
        view = FleetView(self.multiSwitch)
        self.multiSwitch.ReplaceActivePage(view)

FleetSpawner.register()

class FleetView(wx.gizmos.TreeListCtrl):
    def __init__(self, parent):
        wx.gizmos.TreeListCtrl.__init__(self, parent)
        self.imageList = wx.ImageList(16, 16)
        self.SetImageList(self.imageList)

        for col in ("Fit", "Character", "Bonusses"):
            self.AddColumn(col)

        self.AddRoot("WC")

    def populate(self):
        pass
