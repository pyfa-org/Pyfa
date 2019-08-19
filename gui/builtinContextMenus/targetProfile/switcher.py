from collections import OrderedDict

# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.fit import Fit
from service.targetProfile import TargetProfile as svc_TargetProfile


class TargetProfileSwitcher(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if self.mainFrame.getActiveFit() is None or srcContext != 'firepowerViewFull':
            return False

        sTR = svc_TargetProfile.getInstance()
        self.profiles = sTR.getTargetProfileList()
        self.profiles.sort(key=lambda p: (p.name in ['None'], p.name))

        return len(self.profiles) > 0

    def getText(self, callingWindow, itmContext):
        # We take into consideration just target resists, so call menu item accordingly
        return 'Target Resists'

    def handleResistSwitch(self, event):
        profile = self.profileIds.get(event.Id, False)
        if profile is False:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.setTargetProfile(fitID, profile)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))

    def addProfile(self, rootMenu, profile):
        id = ContextMenuUnconditional.nextID()
        name = getattr(profile, '_name', profile.name) if profile is not None else 'No Profile'

        self.profileIds[id] = profile
        item = wx.MenuItem(rootMenu, id, name, kind=wx.ITEM_CHECK)
        rootMenu.Bind(wx.EVT_MENU, self.handleResistSwitch, item)

        # determine active profile
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        f = sFit.getFit(fitID)
        tr = f.targetProfile

        checked = tr == profile

        return item, checked

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        self.profileIds = {}
        self.subMenus = OrderedDict()
        self.singles = []

        sub = wx.Menu()
        for profile in self.profiles:
            start, end = profile.name.find('['), profile.name.find(']')
            if start is not -1 and end is not -1:
                currBase = profile.name[start + 1:end]
                name = profile.name[end + 1:].strip()
                if not name:
                    self.singles.append(profile)
                    continue
                # set helper attr
                setattr(profile, '_name', name)
                if currBase not in self.subMenus:
                    self.subMenus[currBase] = []
                self.subMenus[currBase].append(profile)
            else:
                self.singles.append(profile)
        # Add reset
        msw = 'wxMSW' in wx.PlatformInfo
        mitem, checked = self.addProfile(rootMenu if msw else sub, None)
        sub.Append(mitem)
        mitem.Check(checked)
        sub.AppendSeparator()

        # Single items, no parent
        for profile in self.singles:
            mitem, checked = self.addProfile(rootMenu if msw else sub, profile)
            sub.Append(mitem)
            mitem.Check(checked)

        # Items that have a parent
        for menuName, profiles in list(self.subMenus.items()):
            # Create parent item for root menu that is simply name of parent
            item = wx.MenuItem(rootMenu, ContextMenuUnconditional.nextID(), menuName)

            # Create menu for child items
            grandSub = wx.Menu()

            # Apply child menu to parent item
            item.SetSubMenu(grandSub)

            # Append child items to child menu
            for profile in profiles:
                mitem, checked = self.addProfile(rootMenu if msw else grandSub, profile)
                grandSub.Append(mitem)
                mitem.Check(checked)
            sub.Append(item)  # finally, append parent item to root menu

        return sub


TargetProfileSwitcher.register()
