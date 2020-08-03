# noinspection PyPackageRequirements

import wx

import gui.mainFrame
from gui.builtinViews.emptyView import BlankPage
from gui.contextMenu import ContextMenuUnconditional
from service.fit import Fit

_t = wx.GetTranslation


class AddCurrentlyOpenFit(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):

        if srcContext not in ('projected', 'commandView', 'graphFitList', 'graphTgtList'):
            return False

        if srcContext in ('projected', 'commandView') and self.mainFrame.getActiveFit() is None:
            return False

        return True

    def getText(self, callingWindow, itmContext):
        return _t('Add Currently Open Fit')

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        self.fitLookup = {}
        self.context = context
        self.callingWindow = callingWindow
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
            id = ContextMenuUnconditional.nextID()
            mitem = wx.MenuItem(rootMenu, id, "{}: {}".format(fit.ship.item.name, fit.name))
            bindmenu.Bind(wx.EVT_MENU, self.handleSelection, mitem)
            self.fitLookup[id] = fit
            m.Append(mitem)

        return m

    def handleSelection(self, event):
        fit = self.fitLookup[event.Id]
        self.callingWindow.addFit(fit)


AddCurrentlyOpenFit.register()
