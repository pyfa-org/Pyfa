# noinspection PyPackageRequirements

import wx

from gui.contextMenu import ContextMenuUnconditional
from service.implantSet import ImplantSets as UserImplantSets
from service.precalcImplantSet import PrecalcedImplantSets

_t = wx.GetTranslation


class ImplantSetApply(ContextMenuUnconditional):

    def display(self, callingWindow, srcContext):

        self.userImplantSets = UserImplantSets.getInstance().getImplantSetList()
        self.structedImplantSets = PrecalcedImplantSets.getStructuredSets()

        if len(self.userImplantSets) == 0 and len(self.structedImplantSets) == 0:
            return False

        return srcContext in ("implantItemMisc", "implantEditor")

    def getText(self, callingWindow, context):
        return _t("Apply Implant Set")

    def _addSeparator(self, m, text):
        id_ = ContextMenuUnconditional.nextID()
        m.Append(id_, '─ %s ─' % text)
        m.Enable(id_, False)

    def _addSet(self, parentMenu, profile, name):
        id = ContextMenuUnconditional.nextID()
        self.eventSetMap[id] = profile
        menuItem = wx.MenuItem(parentMenu, id, name)
        parentMenu.Bind(wx.EVT_MENU, self.handleSelection, menuItem)
        return menuItem

    def _addCategory(self, parentMenu, name):
        id = ContextMenuUnconditional.nextID()
        menuItem = wx.MenuItem(parentMenu, id, name)
        parentMenu.Bind(wx.EVT_MENU, self.handleSelection, menuItem)
        return menuItem

    def _gradeSorter(self, item):
        order = ['low-grade', 'mid-grade', 'high-grade']
        try:
            pos = order.index(item.lower())
        except IndexError:
            pos = len(order)
        return pos, item

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        msw = "wxMSW" in wx.PlatformInfo
        menu_lvl1 = wx.Menu()

        self.context = context
        self.callingWindow = callingWindow

        self.eventSetMap = {}

        # Auto-generated sets
        for setName in sorted(self.structedImplantSets):
            setData = self.structedImplantSets[setName]
            if len(setData) == 1:
                for implantIDs in setData.values():
                    menuitem_lvl1 = self._addSet(rootMenu, implantIDs, setName)
                    menu_lvl1.Append(menuitem_lvl1)
            else:
                menuitem_lvl1 = self._addCategory(rootMenu, setName)
                menu_lvl2 = wx.Menu()
                for gradeName in sorted(setData, key=self._gradeSorter):
                    implantIDs = setData[gradeName]
                    menuitem_lvl2 = self._addSet(rootMenu if msw else menu_lvl1, implantIDs, gradeName)
                    menu_lvl2.Append(menuitem_lvl2)
                menu_lvl2.Bind(wx.EVT_MENU, self.handleSelection)
                menuitem_lvl1.SetSubMenu(menu_lvl2)
                menu_lvl1.Append(menuitem_lvl1)

        # Separator
        if self.userImplantSets and self.structedImplantSets:
            menu_lvl1.AppendSeparator()

        # Saved sets
        if self.userImplantSets:
            menuitem_lvl1 = self._addCategory(rootMenu, 'Saved Sets')
            menu_lvl2 = wx.Menu()
            for implantSet in sorted(self.userImplantSets, key=lambda i: i.name):
                menuitem_lvl2 = self._addSet(rootMenu if msw else menu_lvl1, implantSet, implantSet.name)
                menu_lvl2.Append(menuitem_lvl2)
            menu_lvl2.Bind(wx.EVT_MENU, self.handleSelection)
            menuitem_lvl1.SetSubMenu(menu_lvl2)
            menu_lvl1.Append(menuitem_lvl1)

        menu_lvl1.Bind(wx.EVT_MENU, self.handleSelection)
        return menu_lvl1

    def handleSelection(self, event):
        impSet = self.eventSetMap.get(event.Id, None)
        if impSet is None:
            event.Skip()
            return
        if isinstance(impSet, str):
            implants = PrecalcedImplantSets.stringToImplants(impSet)
        else:
            implants = impSet.implants
        self.callingWindow.addImplants(implants)


ImplantSetApply.register()
