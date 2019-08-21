import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cargo.add import CalcAddCargoCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory


class GuiImportCargosCommand(wx.Command):

    def __init__(self, fitID, cargos):
        wx.Command.__init__(self, True, 'Import Cargos')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.cargos = {}
        for itemID, amount in cargos:
            if itemID not in self.cargos:
                self.cargos[itemID] = 0
            self.cargos[itemID] += amount

    def Do(self):
        if not self.cargos:
            return False
        commands = []
        for itemID, amount in self.cargos.items():
            commands.append(CalcAddCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=itemID, amount=amount)))
        success = self.internalHistory.submitBatch(*commands)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
