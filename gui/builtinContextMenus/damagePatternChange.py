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

    def addPattern(self, rootMenu, pattern, name):
        id = ContextMenuUnconditional.nextID()
        self.patternEventMap[id] = pattern
        menuItem = wx.MenuItem(rootMenu, id, name, kind=wx.ITEM_CHECK)
        rootMenu.Bind(wx.EVT_MENU, self.handlePatternSwitch, menuItem)

        # set pattern attr to menu item
        menuItem.pattern = pattern

        # determine active pattern
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)
        checked = fit.damagePattern is pattern if fit else False
        return menuItem, checked

    def isChecked(self, i):
        try:
            single = self.items[0][i]
        except IndexError:
            return super().isChecked(i)
        if self.fit and single is self.fit.damagePattern:
            return True
        return False

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):

        if i < len(self.items[0]):
            # if we're trying to get submenu to something that shouldn't have one,
            # redirect event of the item to handlePatternSwitch and put pattern in
            # our patternIds mapping, then return None for no submenu
            id = pitem.GetId()
            self.patternEventMap[id] = self.items[0][i][1]
            rootMenu.Bind(wx.EVT_MENU, self.handlePatternSwitch, pitem)
            return False

        msw = "wxMSW" in wx.PlatformInfo
        sub = wx.Menu()

        mitemName = list(self.items[1].keys())[i - len(self.items[0])]
        for name, pattern in self.items[1][mitemName][0]:
            mitem, checked = self.addPattern(rootMenu if msw else sub, pattern, name)
            sub.Append(mitem)
            mitem.Check(checked)

        return sub

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
