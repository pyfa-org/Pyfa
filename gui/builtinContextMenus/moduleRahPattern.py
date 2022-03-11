from collections import OrderedDict

# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.builtinContextMenus.shared.patterns import DamagePatternMixin
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit

_t = wx.GetTranslation


class ChangeRahPattern(ContextMenuSingle, DamagePatternMixin):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext != 'fittingModule':
            return False

        if self.mainFrame.getActiveFit() is None:
            return False

        if (mainItem is None or getattr(mainItem, "isEmpty", False)) and srcContext != "fittingShip":
            return False

        if mainItem.item.group.name != 'Armor Resistance Shift Hardener':
            return False

        self.module = mainItem
        self.patternEventMap = {}
        self.patterns = self._getPatterns()
        self.items = self._getItems(self.patterns)
        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return _t('RAH Damage Pattern')

    def _addPattern(self, parentMenu, pattern, name):
        id = ContextMenuSingle.nextID()
        self.patternEventMap[id] = pattern
        menuItem = wx.MenuItem(parentMenu, id, name, kind=wx.ITEM_CHECK)
        parentMenu.Bind(wx.EVT_MENU, self.handlePatternSwitch, menuItem)

        checked = self.module.rahPatternOverride is pattern
        return menuItem, checked

    def _addCategory(self, parentMenu, name):
        id = ContextMenuSingle.nextID()
        menuItem = wx.MenuItem(parentMenu, id, name)
        parentMenu.Bind(wx.EVT_MENU, self.handlePatternSwitch, menuItem)
        return menuItem

    def getSubMenu(self, callingWindow, context, mainItem, rootMenu, i, pitem):
        # Category as menu item - expands further
        msw = "wxMSW" in wx.PlatformInfo

        def makeMenu(container, parentMenu, root=False):
            menu = wx.Menu()
            if root:
                menuItem, checked = self._addPattern(rootMenu if msw else parentMenu, None, 'Fit Pattern')
                menu.Append(menuItem)
                menuItem.Check(checked)
                menuItem, checked = self._addPattern(rootMenu if msw else parentMenu, 'disable', 'Do Not Adapt')
                menu.Append(menuItem)
                menuItem.Check(checked)
                menu.AppendSeparator()
            for name, subcontainer in container[1].items():
                menuItem = self._addCategory(rootMenu if msw else parentMenu, name)
                subMenu = makeMenu(subcontainer, menu)
                menuItem.SetSubMenu(subMenu)
                menu.Append(menuItem)
            for name, pattern in container[0].items():
                menuItem, checked = self._addPattern(rootMenu if msw else parentMenu, pattern, name)
                menu.Append(menuItem)
                menuItem.Check(checked)
            menu.Bind(wx.EVT_MENU, self.handlePatternSwitch)
            return menu

        subMenu = makeMenu(self.items, rootMenu, root=True)
        return subMenu

    def handlePatternSwitch(self, event):
        pattern = self.patternEventMap.get(event.Id, False)
        if pattern is False:
            event.Skip()
            return
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.setRahPattern(fitID, self.module, pattern)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))


ChangeRahPattern.register()
