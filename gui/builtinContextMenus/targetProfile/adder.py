from collections import OrderedDict
from itertools import chain

import wx

import gui.mainFrame
from eos.saveddata.targetProfile import TargetProfile
from gui.contextMenu import ContextMenuUnconditional
from gui.utils.sorter import smartSort
from service.targetProfile import TargetProfile as svc_TargetProfile

# noinspection PyPackageRequirements

_t = wx.GetTranslation


class TargetProfileAdder(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if srcContext != 'graphTgtList':
            return False
        # We always show "Ideal Profile" anyway
        return True

    def getText(self, callingWindow, itmContext):
        return _t('Add Target Profile')

    def handleProfileAdd(self, event):
        profile = self.eventProfileMap.get(event.Id, False)
        if profile is False:
            event.Skip()
            return
        self.callingWindow.addProfile(profile)

    def _addProfile(self, parentMenu, profile, name):
        id = ContextMenuUnconditional.nextID()
        self.eventProfileMap[id] = profile
        menuItem = wx.MenuItem(parentMenu, id, name)
        parentMenu.Bind(wx.EVT_MENU, self.handleProfileAdd, menuItem)
        return menuItem

    def _addCategory(self, parentMenu, name):
        id = ContextMenuUnconditional.nextID()
        menuItem = wx.MenuItem(parentMenu, id, name)
        parentMenu.Bind(wx.EVT_MENU, self.handleProfileAdd, menuItem)
        return menuItem

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        self.callingWindow = callingWindow
        sTR = svc_TargetProfile.getInstance()
        profiles = list(chain(sTR.getBuiltinTargetProfileList(), sTR.getUserTargetProfileList()))
        profiles.sort(key=lambda p: smartSort(p.fullName))

        self.eventProfileMap = {}
        items = (OrderedDict(), OrderedDict())
        for profile in profiles:
            container = items
            for categoryName in profile.hierarchy:
                categoryName = _t(categoryName) if profile.builtin else categoryName
                container = container[1].setdefault(categoryName, (OrderedDict(), OrderedDict()))
            shortName = _t(profile.shortName) if profile.builtin else profile.shortName
            container[0][shortName] = profile

        # Category as menu item - expands further
        msw = "wxMSW" in wx.PlatformInfo

        def makeMenu(container, parentMenu, first=False):
            menu = wx.Menu()
            if first:
                idealProfile = TargetProfile.getIdeal()
                mitem = self._addProfile(rootMenu if msw else parentMenu, idealProfile, idealProfile.fullName)
                menu.Append(mitem)
            for name, pattern in container[0].items():
                menuItem = self._addProfile(rootMenu if msw else parentMenu, pattern, name)
                menu.Append(menuItem)
            for name, subcontainer in container[1].items():
                menuItem = self._addCategory(rootMenu if msw else parentMenu, name)
                subMenu = makeMenu(subcontainer, menu)
                menuItem.SetSubMenu(subMenu)
                menu.Append(menuItem)
            menu.Bind(wx.EVT_MENU, self.handleProfileAdd)
            return menu

        subMenu = makeMenu(items, rootMenu, first=True)
        return subMenu


TargetProfileAdder.register()
