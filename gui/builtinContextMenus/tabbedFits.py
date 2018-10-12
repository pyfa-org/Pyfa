# coding: utf-8

# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.builtinViews.emptyView import BlankPage
from gui.contextMenu import ContextMenu
from service.fit import Fit


class TabbedFits(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):

        if self.mainFrame.getActiveFit() is None or srcContext not in ("projected", "commandView"):
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

        for page in self.mainFrame.fitMultiSwitch._pages:
            if isinstance(page, BlankPage):
                continue
            fit = sFit.getFit(page.activeFitID, basic=True)
            id = ContextMenu.nextID()
            mitem = wx.MenuItem(rootMenu, id, "{}: {}".format(fit.ship.item.name, fit.name))
            bindmenu.Bind(wx.EVT_MENU, self.handleSelection, mitem)
            self.fitLookup[id] = fit
            m.Append(mitem)

        return m

    def handleSelection(self, event):
        fitID = self.mainFrame.getActiveFit()

        fit = self.fitLookup[event.Id]

        if self.context == 'commandView':
            self.mainFrame.command.Submit(cmd.GuiAddCommandCommand(fitID, fit.ID))
        elif self.context == 'projected':
            self.mainFrame.command.Submit(cmd.GuiAddProjectedCommand(fitID, fit.ID, 'fit'))


TabbedFits.register()
