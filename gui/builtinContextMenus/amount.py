from gui.contextMenu import ContextMenu
from eos.saveddata.fit import Fit as es_Fit
import gui.mainFrame
import gui.globalEvents as GE
# noinspection PyPackageRequirements
import wx
import re
from service.fit import Fit
from eos.saveddata.cargo import Cargo as es_Cargo
from eos.saveddata.fighter import Fighter as es_Fighter
from service.settings import ContextMenuSettings


class ChangeAmount(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('amount'):
            return False

        return srcContext in ("cargoItem", "projectedFit", "fighterItem", "projectedFighter")

    def getText(self, itmContext, selection):
        return u"Change {0} Quantity".format(itmContext)

    def activate(self, fullContext, selection, i):
        srcContext = fullContext[0]
        dlg = AmountChanger(self.mainFrame, selection[0], srcContext)
        dlg.ShowModal()


ChangeAmount.register()


class AmountChanger(wx.Dialog):
    def __init__(self, parent, thing, context):
        wx.Dialog.__init__(self, parent, title="Select Amount", size=wx.Size(220, 60))
        self.thing = thing
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
        if self.input.GetLineText(0).strip() == '':
            event.Skip()
            self.Close()
            return

        sFit = Fit.getInstance()
        cleanInput = re.sub(r'[^0-9.]', '', self.input.GetLineText(0).strip())
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        fitID = mainFrame.getActiveFit()

        if isinstance(self.thing, es_Cargo):
            sFit.addCargo(fitID, self.thing.item.ID, int(float(cleanInput)), replace=True)
        elif isinstance(self.thing, es_Fit):
            sFit.changeAmount(fitID, self.thing, int(float(cleanInput)))
        elif isinstance(self.thing, es_Fighter):
            sFit.changeActiveFighters(fitID, self.thing, int(float(cleanInput)))

        wx.PostEvent(mainFrame, GE.FitChanged(fitID=fitID))

        event.Skip()
        self.Close()

    # checks to make sure it's valid number
    @staticmethod
    def onChar(event):
        key = event.GetKeyCode()

        acceptable_characters = "1234567890"
        acceptable_keycode = [3, 22, 13, 8, 127]  # modifiers like delete, copy, paste
        if key in acceptable_keycode or key >= 255 or (key < 255 and chr(key) in acceptable_characters):
            event.Skip()
            return
        else:
            return False
