from collections import OrderedDict

# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.damagePattern import DamagePattern as DmgPatternSvc
from service.fit import Fit


class ChangeDamagePattern(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        return srcContext == "resistancesViewFull"

    @property
    def enabled(self):
        return self.mainFrame.getActiveFit() is not None

    def getText(self, callingWindow, itmContext):
        sDP = DmgPatternSvc.getInstance()
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        self.fit = sFit.getFit(fitID)

        self.patterns = sDP.getDamagePatternList()
        self.patterns.sort(key=lambda p: (p.name not in ["Uniform", "Selected Ammo"], p.name))

        self.patternEventMap = {}
        self.items = ([], OrderedDict())

        for pattern in self.patterns:
            remainingName = pattern.name.strip()
            container = self.items
            while True:
                start, end = remainingName.find('['), remainingName.find(']')
                if start == -1 or end == -1:
                    container[0].append((remainingName, pattern))
                    break
                container = container[1].setdefault(remainingName[start + 1:end], ([], OrderedDict()))
                remainingName = remainingName[end + 1:].strip()

        return [i[0] for i in self.items[0]] + list(self.items[1].keys())

    def _addPattern(self, parentMenu, pattern, name):
        id = ContextMenuUnconditional.nextID()
        self.patternEventMap[id] = pattern
        menuItem = wx.MenuItem(parentMenu, id, name, kind=wx.ITEM_CHECK)
        parentMenu.Bind(wx.EVT_MENU, self.handlePatternSwitch, menuItem)

        # determine active pattern
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)
        checked = fit.damagePattern is pattern if fit else False
        return menuItem, checked

    def _addCategory(self, parentMenu, name):
        id = ContextMenuUnconditional.nextID()
        menuItem = wx.MenuItem(parentMenu, id, name)
        parentMenu.Bind(wx.EVT_MENU, self.handlePatternSwitch, menuItem)
        return menuItem

    def isChecked(self, i):
        try:
            single = self.items[0][i][1]
        except IndexError:
            return super().isChecked(i)
        if self.fit and single is self.fit.damagePattern:
            return True
        return False

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):

        # Pattern as menu item
        if i < len(self.items[0]):
            id = pitem.GetId()
            self.patternEventMap[id] = self.items[0][i][1]
            rootMenu.Bind(wx.EVT_MENU, self.handlePatternSwitch, pitem)
            return False

        # Category as menu item - expands further
        msw = "wxMSW" in wx.PlatformInfo

        def makeMenu(container, parentMenu):
            menu = wx.Menu()
            for name, subcontainer in container[1].items():
                menuItem = self._addCategory(rootMenu if msw else parentMenu, name)
                subMenu = makeMenu(subcontainer, menu)
                menuItem.SetSubMenu(subMenu)
                menu.Append(menuItem)
            for name, pattern in container[0]:
                menuItem, checked = self._addPattern(rootMenu if msw else parentMenu, pattern, name)
                menu.Append(menuItem)
                menuItem.Check(checked)
            menu.Bind(wx.EVT_MENU, self.handlePatternSwitch)
            return menu

        container = list(self.items[1].values())[i - len(self.items[0])]
        subMenu = makeMenu(container, rootMenu)
        return subMenu

    def handlePatternSwitch(self, event):
        pattern = self.patternEventMap.get(event.Id, False)
        if pattern is False:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.setDamagePattern(fitID, pattern)
        setattr(self.mainFrame, "_activeDmgPattern", pattern)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))


ChangeDamagePattern.register()
