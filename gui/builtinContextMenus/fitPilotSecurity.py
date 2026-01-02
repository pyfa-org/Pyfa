import re

import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from gui.utils.colors import ThemedDialog, Colors
from service.fit import Fit

_t = wx.GetTranslation


class FitPilotSecurityMenu(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if srcContext != "fittingShip":
            return False

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)

        if fit.ship.name not in ('Pacifier', 'Enforcer', 'Marshal', 'Sidewinder', 'Cobra', 'Python'):
            return

        return True

    def getText(self, callingWindow, itmContext):
        return _t("Pilot Security Status")

    def addOption(self, menu, optionLabel, optionValue):
        id = ContextMenuUnconditional.nextID()
        self.optionIds[id] = optionValue
        menuItem = wx.MenuItem(menu, id, optionLabel, kind=wx.ITEM_CHECK)
        menu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def addOptionCustom(self, menu, optionLabel):
        id = ContextMenuUnconditional.nextID()
        menuItem = wx.MenuItem(menu, id, optionLabel, kind=wx.ITEM_CHECK)
        menu.Bind(wx.EVT_MENU, self.handleModeCustom, menuItem)
        return menuItem

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.optionIds = {}
        sub = wx.Menu()
        presets = (-10, -8, -6, -4, -2, 0, 1, 2, 3, 4, 5)
        # Inherit
        char_sec_status = round(fit.character.secStatus, 2)
        menuItem = self.addOption(rootMenu if msw else sub, _t('Character') + f' ({char_sec_status})', None)
        sub.Append(menuItem)
        menuItem.Check(fit.pilotSecurity is None)
        # Custom
        label = _t('Custom')
        is_checked = False
        if fit.pilotSecurity is not None and fit.pilotSecurity not in presets:
            sec_status = round(fit.getPilotSecurity(), 2)
            label += f' ({sec_status})'
            is_checked = True
        menuItem = self.addOptionCustom(rootMenu if msw else sub, label)
        sub.Append(menuItem)
        menuItem.Check(is_checked)
        sub.AppendSeparator()
        # Predefined options
        for sec_status in presets:
            menuItem = self.addOption(rootMenu if msw else sub, str(sec_status), sec_status)
            sub.Append(menuItem)
            menuItem.Check(fit.pilotSecurity == sec_status)
        return sub

    def handleMode(self, event):
        optionValue = self.optionIds[event.Id]
        self.mainFrame.command.Submit(cmd.GuiChangeFitPilotSecurityCommand(
                fitID=self.mainFrame.getActiveFit(),
                secStatus=optionValue))

    def handleModeCustom(self, event):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        sec_status = fit.getPilotSecurity()

        with SecStatusChanger(self.mainFrame, value=sec_status) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                cleanInput = re.sub(r'[^0-9.\-+]', '', dlg.input.GetLineText(0).strip())
                if cleanInput:
                    try:
                        cleanInputFloat = float(cleanInput)
                    except ValueError:
                        return
                else:
                    return
                self.mainFrame.command.Submit(cmd.GuiChangeFitPilotSecurityCommand(
                        fitID=fitID, secStatus=max(-10.0, min(5.0, cleanInputFloat))))


FitPilotSecurityMenu.register()


class SecStatusChanger(ThemedDialog):

    def __init__(self, parent, value):
        super().__init__(parent, title=_t('Change Security Status'), style=wx.DEFAULT_DIALOG_STYLE)
        self.SetMinSize((346, 156))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, wx.ID_ANY, _t('Security Status (min -10.0, max 5.0):'))
        bSizer2.Add(text, 0)

        bSizer1.Add(bSizer2, 0, wx.ALL, 10)

        self.input = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        Colors.styleInput(self.input)
        if value is None:
            value = '0.0'
        else:
            if value == int(value):
                value = int(value)
            value = str(value)
        self.input.SetValue(value)

        bSizer1.Add(self.input, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 15)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        bSizer3.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.BOTTOM | wx.EXPAND, 15)

        bSizer3.Add(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL), 0, wx.EXPAND)
        bSizer1.Add(bSizer3, 0, wx.ALL | wx.EXPAND, 10)

        self.input.Bind(wx.EVT_CHAR, self.onChar)
        self.input.Bind(wx.EVT_TEXT_ENTER, self.processEnter)
        self.SetSizer(bSizer1)
        self.Fit()
        self.CenterOnParent()
        self.input.SetFocus()
        self.input.SelectAll()

    def processEnter(self, evt):
        self.EndModal(wx.ID_OK)

    # checks to make sure it's valid number
    @staticmethod
    def onChar(event):
        key = event.GetKeyCode()

        acceptable_characters = '1234567890.-+'
        acceptable_keycode = [3, 22, 13, 8, 127]  # modifiers like delete, copy, paste
        if key in acceptable_keycode or key >= 255 or (key < 255 and chr(key) in acceptable_characters):
            event.Skip()
            return
        else:
            return False
