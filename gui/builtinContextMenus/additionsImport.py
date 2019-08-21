import gui.mainFrame
from gui import fitCommands as cmd
from gui.contextMenu import ContextMenuUnconditional
from gui.utils.clipboard import fromClipboard
from service.fit import Fit
from service.port.eft import parseAdditions
from service.settings import ContextMenuSettings


viewSpecMap = {
    'droneItemMisc': ('Drones', lambda i: i.isDrone, cmd.GuiImportLocalDronesCommand),
    'fighterItemMisc': ('Fighters', lambda i: i.isFighter, cmd.GuiImportLocalFightersCommand),
    'cargoItemMisc': ('Cargo Items', lambda i: not i.isAbyssal, cmd.GuiImportCargosCommand),
    'implantItemMisc': ('Implants', lambda i: i.isImplant, cmd.GuiImportImplantsCommand),
    'implantItemMiscChar': ('Implants', lambda i: i.isImplant, cmd.GuiImportImplantsCommand),
    'boosterItemMisc': ('Boosters', lambda i: i.isBooster, cmd.GuiImportBoostersCommand)}


class AdditionsImport(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if not ContextMenuSettings.getInstance().get('additionsCopyPaste'):
            return False
        if srcContext not in viewSpecMap:
            return False
        fit = Fit.getInstance().getFit(self.mainFrame.getActiveFit())
        if fit is None:
            return False
        if not fromClipboard():
            return False

        self.srcContext = srcContext
        return True

    def getText(self, callingWindow, itmContext):
        return 'Paste {}'.format(viewSpecMap[self.srcContext][0])

    def activate(self, callingWindow, fullContext, i):
        text = fromClipboard()
        items = parseAdditions(text)
        filterFunc = viewSpecMap[self.srcContext][1]
        items = [(i.ID, a) for i, a in items if filterFunc(i)]
        if not items:
            return
        command = viewSpecMap[self.srcContext][2]
        self.mainFrame.command.Submit(command(self.mainFrame.getActiveFit(), items))


AdditionsImport.register()
