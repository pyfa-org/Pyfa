# noinspection PyPackageRequirements
import wx

from service.fit import Fit
from service.market import Market
import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.settings import ContextMenuSettings

class CommandFits(ContextMenu):
    # Get list of items that define a command fit
    sMkt = Market.getInstance()
    grp = sMkt.getGroup(1770)  # Command burst group
    commandTypeIDs = [item.ID for item in grp.items]
    commandFits = []
    menu = None

    @classmethod
    def populateFits(cls, evt):
        if evt is None or (getattr(evt, 'action', None) in ("modadd", "moddel") and getattr(evt, 'typeID', None) in cls.commandTypeIDs):
            # we are adding or removing an item that defines a command fit. Need to refresh fit list
            sFit = Fit.getInstance()
            cls.commandFits = sFit.getFitsWithModules(cls.commandTypeIDs)
            print (cls.commandFits)
            #todo: create menu here.
            pass

    def __init__(self):
        print (self.__class__.commandTypeIDs)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        # todo: the whole thing
        return False

    def getText(self, itmContext, selection):
        return "Command Fits"

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        if self.__class__.menu is None:
            self.__class__.populateFits()
        return self.__class__.menu


CommandFits.register()
