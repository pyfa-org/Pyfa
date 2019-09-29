import re

# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.mainFrame
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.fit import Fit as es_Fit
from eos.saveddata.module import Module
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit


class ChangeItemProjectionRange(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in ('projectedFit', 'projectedModule', 'projectedDrone', 'projectedFighter'):
            return False
        if mainItem is None:
            return False
        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return 'Change {} Range'.format(itmContext)

    def activate(self, callingWindow, fullContext, mainItem, i):
        fitID = self.mainFrame.getActiveFit()
        srcContext = fullContext[0]
        if isinstance(mainItem, es_Fit):
            try:
                value = mainItem.getProjectionInfo(fitID).projectionRange
            except AttributeError:
                return
        else:
            value = mainItem.projectionRange
        if value is not None:
            value /= 1000
        with RangeChanger(self.mainFrame, value) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                sFit = Fit.getInstance()
                fit = sFit.getFit(fitID)
                cleanInput = re.sub(r'[^0-9.]', '', dlg.input.GetLineText(0).strip())
                if cleanInput:
                    try:
                        cleanInputFloat = float(cleanInput)
                    except ValueError:
                        return
                    newRange = cleanInputFloat * 1000
                else:
                    newRange = None

                if isinstance(mainItem, es_Fit):
                    self.mainFrame.command.Submit(cmd.GuiChangeProjectedFitRangeCommand(
                        fitID=fitID, projectedFitID=mainItem.ID, projectionRange=newRange))
                elif isinstance(mainItem, Module):
                    if mainItem in fit.projectedModules:
                        position = fit.projectedModules.index(mainItem)
                        pass
                elif isinstance(mainItem, Drone):
                    pass
                elif isinstance(mainItem, Fighter):
                    if mainItem in fit.projectedFighters:
                        position = fit.projectedFighters.index(mainItem)
                        pass


ChangeItemProjectionRange.register()


class RangeChanger(wx.Dialog):

    def __init__(self, parent, value):
        super().__init__(parent, title='Change Projection Range', style=wx.DEFAULT_DIALOG_STYLE)
        self.SetMinSize((346, 156))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, wx.ID_ANY, 'New Range, km:')
        bSizer2.Add(text, 0)

        bSizer1.Add(bSizer2, 0, wx.ALL, 10)

        self.input = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        if value is None:
            value = ''
        else:
            if value == int(value):
                value = int(value)
            value = str(value)
        self.input.SetValue(value)
        self.input.SelectAll()

        bSizer1.Add(self.input, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 15)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        bSizer3.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.BOTTOM | wx.EXPAND, 15)

        bSizer3.Add(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL), 0, wx.EXPAND)
        bSizer1.Add(bSizer3, 0, wx.ALL | wx.EXPAND, 10)

        self.input.SetFocus()
        self.input.Bind(wx.EVT_CHAR, self.onChar)
        self.input.Bind(wx.EVT_TEXT_ENTER, self.processEnter)
        self.SetSizer(bSizer1)
        self.CenterOnParent()
        self.Fit()

    def processEnter(self, evt):
        self.EndModal(wx.ID_OK)

    # checks to make sure it's valid number
    @staticmethod
    def onChar(event):
        key = event.GetKeyCode()

        acceptable_characters = '1234567890.'
        acceptable_keycode = [3, 22, 13, 8, 127]  # modifiers like delete, copy, paste
        if key in acceptable_keycode or key >= 255 or (key < 255 and chr(key) in acceptable_characters):
            event.Skip()
            return
        else:
            return False
