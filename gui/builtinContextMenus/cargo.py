from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import eos.types
import gui.mainFrame
import service
import gui.globalEvents as GE
import wx

class Cargo(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        # Make sure context menu registers in the correct view
        if srcContext not in ("marketItemGroup", "marketItemMisc") or self.mainFrame.getActiveFit() is None:
            return False
        return True

    def getText(self, itmContext, selection):
        return "Add {0} to Cargo".format(itmContext)

    def activate(self, fullContext, selection, i):
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()

        typeID = int(selection[0].ID)
        sFit.addCargo(fitID, typeID)
        self.mainFrame.additionsPane.select("Cargo")
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

Cargo.register()

class CargoAmount(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        return srcContext in ("cargoItem",) and selection[0].amount >= 0

    def getText(self, itmContext, selection):
        return "Change {0} Quantity".format(itmContext)

    def activate(self, fullContext, selection, i):
        srcContext = fullContext[0]
        dlg = CargoChanger(self.mainFrame, selection[0], srcContext)
        dlg.ShowModal()
        dlg.Destroy()

CargoAmount.register()

class CargoChanger(wx.Dialog):

    def __init__(self, parent, cargo, context):
        wx.Dialog.__init__(self, parent, title="Select Amount", size=wx.Size(220, 60))
        self.cargo = cargo
        self.context = context

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.input = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)

        bSizer1.Add(self.input, 1, wx.ALL, 5)
        self.input.Bind(wx.EVT_CHAR, self.onChar)
        self.input.Bind(wx.EVT_TEXT_ENTER, self.change)
        self.button = wx.Button(self, wx.ID_OK, u"Done")
        bSizer1.Add(self.button, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        self.button.Bind(wx.EVT_BUTTON, self.change)

    def change(self, event):
        sFit = service.Fit.getInstance()
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        fitID = mainFrame.getActiveFit()

        sFit.addCargo(fitID, self.cargo, int(self.input.GetLineText(0)))

        wx.PostEvent(mainFrame, GE.FitChanged(fitID=fitID))

        event.Skip()
        self.Destroy()
    ## checks to make sure it's valid number
    def onChar(self, event):
        key = event.GetKeyCode()

        acceptable_characters = "1234567890"
        acceptable_keycode    = [3, 22, 13, 8, 127] # modifiers like delete, copy, paste
        if key in acceptable_keycode or key >= 255 or (key < 255 and chr(key) in acceptable_characters):
            event.Skip()
            return
        else:
            return False

