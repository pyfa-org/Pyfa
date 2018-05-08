from gui.contextMenu import ContextMenu
import gui.mainFrame
import gui.globalEvents as GE
from service.fit import Fit
# noinspection PyPackageRequirements
import wx
from service.settings import ContextMenuSettings


class DroneSplit(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('droneSplit'):
            return False

        return srcContext in ("droneItem", "projectedDrone") and selection[0].amount > 1

    def getText(self, itmContext, selection):
        return "Split {0} Stack".format(itmContext)

    def activate(self, fullContext, selection, i):
        srcContext = fullContext[0]
        dlg = DroneSpinner(self.mainFrame, selection[0], srcContext)
        dlg.ShowModal()
        dlg.Destroy()


DroneSplit.register()


class DroneSpinner(wx.Dialog):
    def __init__(self, parent, drone, context):
        wx.Dialog.__init__(self, parent, title="Select Amount", size=wx.Size(220, 60))
        self.drone = drone
        self.context = context

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.spinner = wx.SpinCtrl(self)
        self.spinner.SetRange(1, drone.amount - 1)
        self.spinner.SetValue(1)

        bSizer1.Add(self.spinner, 1, wx.ALL, 5)

        self.button = wx.Button(self, wx.ID_OK, "Split")
        bSizer1.Add(self.button, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.button.Bind(wx.EVT_BUTTON, self.split)

    def split(self, event):
        sFit = Fit.getInstance()
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        fitID = mainFrame.getActiveFit()
        if self.context == "droneItem":
            sFit.splitDroneStack(fitID, self.drone, self.spinner.GetValue())
        else:
            sFit.splitProjectedDroneStack(fitID, self.drone, self.spinner.GetValue())
        wx.PostEvent(mainFrame, GE.FitChanged(fitID=fitID))
        event.Skip()
