from collections import OrderedDict

import wx

import gui.mainFrame
from graphs.events import ResistModeChanged
from graphs.wrapper import TargetWrapper
from gui.contextMenu import ContextMenuCombined
from service.const import TargetResistMode
from service.settings import GraphSettings

# noinspection PyPackageRequirements

_t = wx.GetTranslation

optionMap = OrderedDict((
    ('Auto', TargetResistMode.auto),
    ('Shield', TargetResistMode.shield),
    ('Armor', TargetResistMode.armor),
    ('Hull', TargetResistMode.hull),
    ('Weighted Average', TargetResistMode.weightedAverage)))


class TargetWrapperResists(ContextMenuCombined):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem, selection):
        if srcContext != 'graphTgtList':
            return False
        if GraphSettings.getInstance().get('ignoreResists'):
            return False
        if not isinstance(mainItem, TargetWrapper) or not mainItem.isFit:
            return False
        self.callingWindow = callingWindow
        self.selection = selection
        return True

    def getText(self, callingWindow, itmContext, mainItem, selection):
        return _t('Resist Mode')

    def addOption(self, menu, optionLabel):
        id = ContextMenuCombined.nextID()
        self.optionIds[id] = optionLabel
        menuItem = wx.MenuItem(menu, id, optionLabel, kind=wx.ITEM_CHECK)
        menu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def getSubMenu(self, callingWindow, context, mainItem, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.optionIds = {}
        sub = wx.Menu()
        for optionLabel, optionValue in optionMap.items():
            menuItem = self.addOption(rootMenu if msw else sub, optionLabel)
            sub.Append(menuItem)
            menuItem.Check(mainItem.resistMode == optionValue)
        return sub

    def handleMode(self, event):
        optionLabel = self.optionIds[event.Id]
        optionValue = optionMap[optionLabel]
        changedFitIDs = set()
        for wrapper in self.selection:
            if wrapper.isFit and wrapper.resistMode != optionValue:
                wrapper.resistMode = optionValue
                changedFitIDs.add(wrapper.item.ID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), ResistModeChanged(fitIDs=changedFitIDs))


TargetWrapperResists.register()
