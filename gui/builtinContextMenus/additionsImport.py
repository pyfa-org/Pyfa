import wx

import gui.mainFrame
from gui import fitCommands as cmd
from gui.contextMenu import ContextMenuUnconditional
from gui.utils.clipboard import fromClipboard
from service.fit import Fit
from service.port.eft import parseAdditions, importGetMutationData, lineIter

_t = wx.GetTranslation


class AdditionsImport(ContextMenuUnconditional):
    visibilitySetting = 'additionsCopyPaste'

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.viewSpecMap = {
            'droneItemMisc': (_t('Drones'), lambda i: i.isDrone, cmd.GuiImportLocalDronesCommand),
            'fighterItemMisc': (_t('Fighters'), lambda i: i.isFighter, cmd.GuiImportLocalFightersCommand),
            'cargoItemMisc': (_t('Cargo Items'), lambda i: not i.isAbyssal, cmd.GuiImportCargosCommand),
            'implantItemMisc': (_t('Implants'), lambda i: i.isImplant, cmd.GuiImportImplantsCommand),
            'implantItemMiscChar': (_t('Implants'), lambda i: i.isImplant, cmd.GuiImportImplantsCommand),
            'boosterItemMisc': (_t('Boosters'), lambda i: i.isBooster, cmd.GuiImportBoostersCommand)
        }

    def display(self, callingWindow, srcContext):
        if srcContext not in self.viewSpecMap:
            return False
        fit = Fit.getInstance().getFit(self.mainFrame.getActiveFit())
        if fit is None:
            return False
        if not fromClipboard():
            return False

        self.srcContext = srcContext
        return True

    def getText(self, callingWindow, itmContext):
        return _t('Paste {}').format(self.viewSpecMap[self.srcContext][0])

    def activate(self, callingWindow, fullContext, i):
        text = fromClipboard()
        lines = list(lineIter(text))
        mutaData = importGetMutationData(lines)
        text = '\n'.join(lines)
        items = parseAdditions(text, mutaData=mutaData)
        filterFunc = self.viewSpecMap[self.srcContext][1]
        items = [(i.ID, a, m) for i, a, m in items if filterFunc(i)]
        if not items:
            return
        command = self.viewSpecMap[self.srcContext][2]
        self.mainFrame.command.Submit(command(self.mainFrame.getActiveFit(), items))


AdditionsImport.register()
