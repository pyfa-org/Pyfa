from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.fittingView
import wx
from gui import bitmapLoader

class DamagePattern(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        return context in ("resistancesViewFull",) and self.mainFrame.getActiveFit() is not None

    def getText(self, context, selection):
        sDP = service.DamagePattern.getInstance()
        self.patterns = sDP.getDamagePatternList()
        self.patterns.sort( key=lambda p: (p.name in ["Selected Ammo", 
                            "Uniform"], p.name) )
        m = map(lambda p: p.name, self.patterns)
        return m

    def activate(self, context, selection, i):
        sDP = service.DamagePattern.getInstance()
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.setDamagePattern(fitID, self.patterns[i])
        setattr(self.mainFrame,"_activeDmgPattern",self.patterns[i])
        wx.PostEvent(self.mainFrame, gui.fittingView.FitChanged(fitID=fitID))

    def getBitmap(self, context, selection):
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        f = sFit.getFit(fitID)
        dp = f.damagePattern
        if dp is None:
            return None

        index = self.patterns.index(dp)
        bitmap = bitmapLoader.getBitmap("state_active_small", "icons")
        l = [None] * len(self.patterns)
        l[index] = bitmap

        return l


DamagePattern.register()
