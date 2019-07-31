from collections import OrderedDict
from itertools import chain

# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from eos.saveddata.targetProfile import TargetProfile
from gui.contextMenu import ContextMenuUnconditional
from service.targetProfile import TargetProfile as svc_TargetProfile


class TargetProfileAdder(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if srcContext != 'graphTgtList':
            return False

        sTR = svc_TargetProfile.getInstance()
        self.callingWindow = callingWindow
        self.profiles = sTR.getTargetProfileList()
        self.profiles.sort(key=lambda p: (p.name in ['None'], p.name))

        return len(self.profiles) > 0

    def getText(self, callingWindow, itmContext):
        return 'Add Target Profile'

    def handleProfileAdd(self, event):
        profile = self.profileIds.get(event.Id, False)
        if profile is False:
            event.Skip()
            return
        self.callingWindow.addProfile(profile)

    def addProfile(self, rootMenu, profile):
        id = ContextMenuUnconditional.nextID()
        name = getattr(profile, '_name', profile.name)

        self.profileIds[id] = profile
        item = wx.MenuItem(rootMenu, id, name)
        rootMenu.Bind(wx.EVT_MENU, self.handleProfileAdd, item)

        return item

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        self.profileIds = {}
        self.subMenus = OrderedDict()
        self.singles = []

        sub = wx.Menu()
        for profile in chain([TargetProfile.getIdeal()], self.profiles):
            start, end = profile.name.find('['), profile.name.find(']')
            if start is not -1 and end is not -1:
                currBase = profile.name[start + 1:end]
                # set helper attr
                setattr(profile, '_name', profile.name[end + 1:].strip())
                if currBase not in self.subMenus:
                    self.subMenus[currBase] = []
                self.subMenus[currBase].append(profile)
            else:
                self.singles.append(profile)

        # Single items, no parent
        msw = 'wxMSW' in wx.PlatformInfo
        for profile in self.singles:
            sub.Append(self.addProfile(rootMenu if msw else sub, profile))

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
                grandSub.Append(self.addProfile(rootMenu if msw else grandSub, profile))
            sub.Append(item)  # finally, append parent item to root menu

        return sub


TargetProfileAdder.register()
