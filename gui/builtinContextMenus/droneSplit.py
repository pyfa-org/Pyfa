from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import gui.mainFrame
import gui.fittingView
import service
import wx

class DroneSplit(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        return context in ("drone") and selection[0].amount > 1

    def getText(self, context, selection):
        return "Split stack"

    def activate(self, context, selection, i):
        dlg = DroneSpinner(self.mainFrame, selection[0])
        dlg.ShowModal()
        dlg.Destroy()

DroneSplit.register()


class DroneSpinner(wx.Dialog):

    def __init__(self, parent, drone):
        wx.Dialog.__init__(self, parent, title="Select Amount", size=wx.Size(220, 60))
        self.drone = drone

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.spinner = wx.SpinCtrl(self)
        self.spinner.SetRange(1, drone.amount)
        self.spinner.SetValue(1)

        bSizer1.Add(self.spinner, 0, wx.ALL, 5)

        self.button = wx.Button(self, wx.ID_OK, u"Split")
        bSizer1.Add(self.button, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.button.Bind(wx.EVT_BUTTON, self.split)

    def split(self, event):
        sFit = service.Fit.getInstance()
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        fitID = mainFrame.getActiveFit()
        sFit.splitDroneStack(fitID, self.drone, self.spinner.GetValue())
        wx.PostEvent(mainFrame, gui.fittingView.FitChanged(fitID=fitID))
        event.Skip()
