from collections import OrderedDict
from itertools import chain

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from gui.utils.sorter import smartSort
from service.fit import Fit
from service.targetProfile import TargetProfile as svc_TargetProfile

# noinspection PyPackageRequirements

_t = wx.GetTranslation


class TargetProfileSwitcher(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if srcContext != 'firepowerViewFull':
            return False
        if self.mainFrame.getActiveFit() is None:
            return False
        # We always show "No Profile" anyway
        return True

    def getText(self, callingWindow, itmContext):
        # We take into consideration just target resists, so call menu item accordingly
        return _t('Target Resists')

    def handleResistSwitch(self, event):
        profile = self.profileEventMap.get(event.Id, False)
        if profile is False:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.setTargetProfile(fitID, profile)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))

    def _addProfile(self, parentMenu, profile, name):
        id = ContextMenuUnconditional.nextID()
        self.profileEventMap[id] = profile
        menuItem = wx.MenuItem(parentMenu, id, name, kind=wx.ITEM_CHECK)
        parentMenu.Bind(wx.EVT_MENU, self.handleResistSwitch, menuItem)

        # determine active profile
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        checked = sFit.getFit(fitID).targetProfile is profile
        return menuItem, checked

    def _addCategory(self, parentMenu, name):
        id = ContextMenuUnconditional.nextID()
        menuItem = wx.MenuItem(parentMenu, id, name)
        parentMenu.Bind(wx.EVT_MENU, self.handleResistSwitch, menuItem)
        return menuItem

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        sTR = svc_TargetProfile.getInstance()
        profiles = list(chain(sTR.getBuiltinTargetProfileList(), sTR.getUserTargetProfileList()))
        profiles.sort(key=lambda p: smartSort(p.fullName))

        self.profileEventMap = {}
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
                mitem, checked = self._addProfile(rootMenu if msw else parentMenu, None, _t('No Profile'))
                menu.Append(mitem)
                mitem.Check(checked)
                if len(container[0]) > 0 or len(container[1]) > 0:
                    menu.AppendSeparator()
            for name, pattern in container[0].items():
                menuItem, checked = self._addProfile(rootMenu if msw else parentMenu, pattern, name)
                menu.Append(menuItem)
                menuItem.Check(checked)
            for name, subcontainer in container[1].items():
                menuItem = self._addCategory(rootMenu if msw else parentMenu, name)
                subMenu = makeMenu(subcontainer, menu)
                menuItem.SetSubMenu(subMenu)
                menu.Append(menuItem)
            menu.Bind(wx.EVT_MENU, self.handleResistSwitch)
            return menu

        subMenu = makeMenu(items, rootMenu, first=True)
        return subMenu


TargetProfileSwitcher.register()
