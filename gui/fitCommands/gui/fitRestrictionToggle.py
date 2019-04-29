import wx
from service.fit import Fit

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import InternalCommandHistory
from gui.fitCommands.calc.module.localRemove import CalcRemoveLocalModulesCommand


class GuiToggleFittingRestrictionsCommand(wx.Command):

    def __init__(self, fitID):
        wx.Command.__init__(self, True, 'Toggle Fitting Restrictions')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID

    def Do(self):
        fit = Fit.getInstance().getFit(self.fitID)
        fit.ignoreRestrictions = not fit.ignoreRestrictions

        success = True
        if not fit.ignoreRestrictions:
            results = []
            for position, mod in sorted(enumerate(fit.modules), key=lambda i: i[0], reverse=True):
                if not mod.isEmpty and not mod.fits(fit, hardpointLimit=False):
                    cmd = CalcRemoveLocalModulesCommand(fitID=self.fitID, positions=[position], commit=False)
                    results.append(self.internalHistory.submit(cmd))
            if len(results) > 0:
                success = any(results)

        eos.db.commit()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        fit.ignoreRestrictions = not fit.ignoreRestrictions
        success = self.internalHistory.undoAll()
        eos.db.commit()
        sFit.recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
