from gui.contextMenu import ContextMenu
import gui.mainFrame
import gui.globalEvents as GE
# noinspection PyPackageRequirements
import wx
from gui.bitmap_loader import BitmapLoader
from service.fit import Fit
from service.damagePattern import DamagePattern as import_DamagePattern
from service.settings import ContextMenuSettings

from collections import OrderedDict


class DamagePattern(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('damagePattern'):
            return False

        return srcContext == "resistancesViewFull" and self.mainFrame.getActiveFit() is not None

    def getText(self, itmContext, selection):
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
                # set helper attr
                setattr(pattern, "_name", pattern.name[end + 1:].strip())
                if currBase not in self.subMenus:
                    self.subMenus[currBase] = []
                self.subMenus[currBase].append(pattern)
            else:
                self.singles.append(pattern)

        # return list of names, with singles first followed by submenu names
        self.m = [p.name for p in self.singles] + list(self.subMenus.keys())
        return self.m

    def addPattern(self, rootMenu, pattern):
        id = ContextMenu.nextID()
        name = getattr(pattern, "_name", pattern.name) if pattern is not None else "No Profile"

        self.patternIds[id] = pattern
        menuItem = wx.MenuItem(rootMenu, id, name)
        rootMenu.Bind(wx.EVT_MENU, self.handlePatternSwitch, menuItem)

        # set pattern attr to menu item
        menuItem.pattern = pattern

        # determine active pattern
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        f = sFit.getFit(fitID)
        dp = f.damagePattern

        if dp == pattern:
            bitmap = BitmapLoader.getBitmap("state_active_small", "gui")
            menuItem.SetBitmap(bitmap)
        return menuItem

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False

        if self.m[i] not in self.subMenus:
            # if we're trying to get submenu to something that shouldn't have one,
            # redirect event of the item to handlePatternSwitch and put pattern in
            # our patternIds mapping, then return None for no submenu
            id = pitem.GetId()
            self.patternIds[id] = self.singles[i]
            rootMenu.Bind(wx.EVT_MENU, self.handlePatternSwitch, pitem)
            if self.patternIds[id] == self.fit.damagePattern:
                bitmap = BitmapLoader.getBitmap("state_active_small", "gui")
                pitem.SetBitmap(bitmap)
            return False

        sub = wx.Menu()

        # Items that have a parent
        for pattern in self.subMenus[self.m[i]]:
            sub.Append(self.addPattern(rootMenu if msw else sub, pattern))

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
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


DamagePattern.register()
