from collections import OrderedDict

# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.bitmap_loader import BitmapLoader
from gui.contextMenu import ContextMenuUnconditional
from service.fit import Fit
from service.targetProfile import TargetProfile as svc_TargetProfile


class TargetProfile(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if self.mainFrame.getActiveFit() is None or srcContext != "firepowerViewFull":
            return False

        sTR = svc_TargetProfile.getInstance()
        self.patterns = sTR.getTargetProfileList()
        self.patterns.sort(key=lambda p: (p.name in ["None"], p.name))

        return len(self.patterns) > 0

    def getText(self, callingWindow, itmContext):
        # We take into consideration just target resists, so call menu item accordingly
        return "Target Resists"

    def handleResistSwitch(self, event):
        pattern = self.patternIds.get(event.Id, False)
        if pattern is False:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.setTargetProfile(fitID, pattern)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))

    def addPattern(self, rootMenu, pattern):
        id = ContextMenuUnconditional.nextID()
        name = getattr(pattern, "_name", pattern.name) if pattern is not None else "No Profile"

        self.patternIds[id] = pattern
        item = wx.MenuItem(rootMenu, id, name)
        rootMenu.Bind(wx.EVT_MENU, self.handleResistSwitch, item)

        # set pattern attr to menu item
        item.pattern = pattern

        # determine active pattern
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        f = sFit.getFit(fitID)
        tr = f.targetProfile

        if tr == pattern:
            bitmap = BitmapLoader.getBitmap("state_active_small", "gui")
            item.SetBitmap(bitmap)
        return item

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.patternIds = {}
        self.subMenus = OrderedDict()
        self.singles = []

        sub = wx.Menu()
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

        sub.Append(self.addPattern(rootMenu if msw else sub, None))  # Add reset
        sub.AppendSeparator()

        # Single items, no parent
        for pattern in self.singles:
            sub.Append(self.addPattern(rootMenu if msw else sub, pattern))

        # Items that have a parent
        for menuName, patterns in list(self.subMenus.items()):
            # Create parent item for root menu that is simply name of parent
            item = wx.MenuItem(rootMenu, ContextMenuUnconditional.nextID(), menuName)

            # Create menu for child items
            grandSub = wx.Menu()
            # sub.Bind(wx.EVT_MENU, self.handleResistSwitch)

            # Apply child menu to parent item
            item.SetSubMenu(grandSub)

            # Append child items to child menu
            for pattern in patterns:
                grandSub.Append(self.addPattern(rootMenu if msw else grandSub, pattern))
            sub.Append(item)  # finally, append parent item to root menu

        return sub


TargetProfile.register()
