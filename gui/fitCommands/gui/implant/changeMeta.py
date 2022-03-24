import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.implant.add import CalcAddImplantCommand
from gui.fitCommands.helpers import ImplantInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeImplantMetaCommand(wx.Command):

    def __init__(self, fitID, position, newItemID):
        wx.Command.__init__(self, True, 'Change Implant Meta')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.newItemID = newItemID
        self.newPosition = None

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        implant = fit.implants[self.position]
        if implant.itemID == self.newItemID:
            return False
        info = ImplantInfo.fromImplant(implant)
        info.itemID = self.newItemID
        cmd = CalcAddImplantCommand(fitID=self.fitID, implantInfo=info)
        success = self.internalHistory.submit(cmd)
        eos.db.flush()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        self.newPosition = cmd.newPosition
        newImplant = fit.implants[self.newPosition]
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        wx.PostEvent(mainFrame, GE.FitChanged(fitIDs=(self.fitID,)))
        wx.PostEvent(mainFrame, GE.ItemChangedInplace(old=implant, new=newImplant))
        return success

    def Undo(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        oldImplant = fit.implants[self.newPosition]
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        newImplant = fit.implants[self.position]
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        wx.PostEvent(mainFrame, GE.FitChanged(fitIDs=(self.fitID,)))
        wx.PostEvent(mainFrame, GE.ItemChangedInplace(old=oldImplant, new=newImplant))
        return success
