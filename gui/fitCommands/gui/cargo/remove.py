import math

import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory
from service.market import Market


class GuiRemoveCargosCommand(wx.Command):

    def __init__(self, fitID, itemIDs):
        wx.Command.__init__(self, True, 'Remove Cargos')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemIDs = itemIDs

    def Do(self):
        sMkt = Market.getInstance()
        results = []
        for itemID in self.itemIDs:
            cmd = CalcRemoveCargoCommand(
                fitID=self.fitID,
                cargoInfo=CargoInfo(itemID=itemID, amount=math.inf))
            results.append(self.internalHistory.submit(cmd))
            sMkt.storeRecentlyUsed(itemID)
        success = any(results)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
