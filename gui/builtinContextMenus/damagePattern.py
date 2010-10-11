from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.fittingView
import wx

class DamagePattern(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        return context in ("resistancesViewFull",) and self.mainFrame.getActiveFit() is not None

    def getText(self, context, selection):
        sDP = service.DamagePattern.getInstance()
        self.patterns = sDP.getDamagePatternList()
        self.patterns.sort(key=lambda p: p.name)
        m = map(lambda p: p.name, self.patterns)
        m.append("Raw")
        return m

    def activate(self, context, selection, i):
        sDP = service.DamagePattern.getInstance()
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.setDamagePattern(fitID, self.patterns[i] if i < len(self.patterns) else None)
        wx.PostEvent(self.mainFrame, gui.fittingView.FitChanged(fitID=fitID))

DamagePattern.register()
