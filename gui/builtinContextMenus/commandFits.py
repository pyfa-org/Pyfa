# noinspection PyPackageRequirements
import wx

from service.fit import Fit
from service.market import Market
import gui.mainFrame
import gui.globalEvents as GE
from gui.contextMenu import ContextMenu
from service.settings import ContextMenuSettings


class CommandFits(ContextMenu):
    # Get list of items that define a command fit
    sMkt = Market.getInstance()
    grp = sMkt.getGroup(1770)  # Command burst group
    commandTypeIDs = {item.ID for item in grp.items}
    commandFits = []
    menu = None

    @classmethod
    def fitChanged(cls, evt):
        # This fires on a FitChanged event and updates the command fits whenever a command burst module is added or
        # removed from a fit. evt.typeID can be either a int or a set (in the case of multiple module deletions)
        if evt is None or (getattr(evt, 'action', None) in ("modadd", "moddel") and getattr(evt, 'typeID', None)):
            if evt is not None:
                ids = getattr(evt, 'typeID')
                if not isinstance(ids, set):
                    ids = set([ids])

            if evt is None or not ids.isdisjoint(cls.commandTypeIDs):
                # we are adding or removing an item that defines a command fit. Need to refresh fit list
                cls.populateFits(evt)

    @classmethod
    def populateFits(cls, evt):
        sFit = Fit.getInstance()
        cls.commandFits = sFit.getFitsWithModules(cls.commandTypeIDs)

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if self.mainFrame.getActiveFit() is None or len(self.__class__.commandFits) == 0 or srcContext != "commandView":
            return False

        return True

    def getText(self, itmContext, selection):
        return "Command Fits"

    def addFit(self, menu, fit, includeShip=False):
        label = fit.name if not includeShip else u"({}) {}".format(fit.ship.item.name, fit.name)
        id = ContextMenu.nextID()
        self.fitMenuItemIds[id] = fit
        menuItem = wx.MenuItem(menu, id, label)
        menu.Bind(wx.EVT_MENU, self.handleSelection, menuItem)
        return menuItem

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.context = context
        self.fitMenuItemIds = {}

        sub = wx.Menu()

        if len(self.__class__.commandFits) < 15:
            for fit in sorted(self.__class__.commandFits, key=lambda x: x.name):
                menuItem = self.addFit(rootMenu if msw else sub, fit, True)
                sub.AppendItem(menuItem)
        else:
            typeDict = {}

            for fit in self.__class__.commandFits:
                shipName = fit.ship.item.name
                if shipName not in typeDict:
                    typeDict[shipName] = []
                typeDict[shipName].append(fit)

            for ship in sorted(typeDict.keys()):
                shipItem = wx.MenuItem(sub, ContextMenu.nextID(), ship)
                grandSub = wx.Menu()
                shipItem.SetSubMenu(grandSub)

                for fit in sorted(typeDict[ship], key=lambda x: x.name):
                    fitItem = self.addFit(rootMenu if msw else grandSub, fit, False)
                    grandSub.AppendItem(fitItem)

                sub.AppendItem(shipItem)

        return sub

    def handleSelection(self, event):
        fit = self.fitMenuItemIds[event.Id]
        if fit is False or fit not in self.__class__.commandFits:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()

        sFit.addCommandFit(fitID, fit)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


CommandFits.populateFits(None)
CommandFits.register()
