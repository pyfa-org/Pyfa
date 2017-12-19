# coding: utf-8

# noinspection PyPackageRequirements
import wx

from service.fit import Fit
import gui.mainFrame
import gui.globalEvents as GE
from gui.contextMenu import ContextMenu
from gui.builtinViews.emptyView import BlankPage


class TabbedFits(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):

        if self.mainFrame.getActiveFit() is None or srcContext not in ("projected", "commandView", "graphAttacker", "graphTargetFitsResists", "graphTargetFits"):
            return False

        return True

    def getText(self, itmContext, selection):
        return "Currently Open Fits"

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        self.fitLookup = {}
        self.context = context
        sFit = Fit.getInstance()

        m = wx.Menu()

        # If on Windows we need to bind out events into the root menu, on other
        # platforms they need to go to our sub menu
        if "wxMSW" in wx.PlatformInfo:
            bindmenu = rootMenu
        else:
            bindmenu = m

        for page in self.mainFrame.fitMultiSwitch.pages:
            if isinstance(page, BlankPage):
                continue
            fit = sFit.getFit(page.activeFitID, basic=True)
            id = ContextMenu.nextID()
            mitem = wx.MenuItem(rootMenu, id, u"{}: {}".format(fit.ship.item.name, fit.name))
            bindmenu.Bind(wx.EVT_MENU, self.handleSelection, mitem)
            self.fitLookup[id] = (page.activeFitID, fit)
            m.AppendItem(mitem)

        return m

    def handleSelection(self, event):
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()

        selFitID, selFit = self.fitLookup[event.Id]

        if self.context == 'commandView':
            sFit.addCommandFit(fitID, selFit)
        elif self.context == 'projected':
            sFit.project(fitID, selFit)
        elif self.context == "graphAttacker":
            self.mainFrame.graphFrame.AppendFitToList(selFitID)
        elif self.context in ("graphTargetFitsResists", "graphTargetFits"):
            self.mainFrame.graphFrame.addTargetFit(selFitID)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


TabbedFits.register()
