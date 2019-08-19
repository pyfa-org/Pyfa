from collections import OrderedDict

# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.damagePattern import DamagePattern as import_DamagePattern
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
        sDP = import_DamagePattern.getInstance()
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        self.fit = sFit.getFit(fitID)

        self.patterns = sDP.getDamagePatternList()
        self.patterns.sort(key=lambda p: (p.name not in ["Uniform", "Selected Ammo"], p.name))

        self.patternIds = {}
        self.subMenus = OrderedDict()
        self.singles = []

        # iterate and separate damage patterns based on "[Parent] Child"
        for pattern in self.patterns:
            start, end = pattern.name.find('['), pattern.name.find(']')
            if start is not -1 and end is not -1:
                currBase = pattern.name[start + 1:end]
                name = pattern.name[end + 1:].strip()
                if not name:
                    self.singles.append(pattern)
                    continue
                # set helper attr
                setattr(pattern, "_name", name)
                if currBase not in self.subMenus:
                    self.subMenus[currBase] = []
                self.subMenus[currBase].append(pattern)
            else:
                self.singles.append(pattern)

        # return list of names, with singles first followed by submenu names
        self.m = [p.name for p in self.singles] + list(self.subMenus.keys())
        return self.m

    def addPattern(self, rootMenu, pattern):
        id = ContextMenuUnconditional.nextID()
        name = getattr(pattern, "_name", pattern.name) if pattern is not None else "No Profile"

        self.patternIds[id] = pattern
        menuItem = wx.MenuItem(rootMenu, id, name, kind=wx.ITEM_CHECK)
        rootMenu.Bind(wx.EVT_MENU, self.handlePatternSwitch, menuItem)

        # set pattern attr to menu item
        menuItem.pattern = pattern

        # determine active pattern
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)
        if fit:
            dp = fit.damagePattern
            checked = dp is pattern
        else:
            checked = False
        return menuItem, checked

    def isChecked(self, i):
        try:
            single = self.singles[i]
        except IndexError:
            return super().isChecked(i)
        if self.fit and single is self.fit.damagePattern:
            return True
        return False

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        # Attempt to remove attribute which carries info if non-sub-items should
        # be checked or not
        self.checked = None

        if self.m[i] not in self.subMenus:
            # if we're trying to get submenu to something that shouldn't have one,
            # redirect event of the item to handlePatternSwitch and put pattern in
            # our patternIds mapping, then return None for no submenu
            id = pitem.GetId()
            self.patternIds[id] = self.singles[i]
            rootMenu.Bind(wx.EVT_MENU, self.handlePatternSwitch, pitem)
            return False

        sub = wx.Menu()

        # Items that have a parent
        msw = "wxMSW" in wx.PlatformInfo
        for pattern in self.subMenus[self.m[i]]:
            mitem, checked = self.addPattern(rootMenu if msw else sub, pattern)
            sub.Append(mitem)
            mitem.Check(checked)

        return sub

    def handlePatternSwitch(self, event):
        pattern = self.patternIds.get(event.Id, False)
        if pattern is False:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.setDamagePattern(fitID, pattern)
        setattr(self.mainFrame, "_activeDmgPattern", pattern)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))


ChangeDamagePattern.register()
