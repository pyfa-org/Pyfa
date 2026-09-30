# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.mainFrame
from eos.saveddata.commandLink import (
    ALL_LINK_TYPE, CATEGORY_LABELS, CATEGORY_LINKS, CATEGORY_ORDER, COMMAND_LINK_DEFS, STRENGTHS)
from gui.contextMenu import ContextMenuUnconditional

_t = wx.GetTranslation


class AddCommandLink(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if self.mainFrame.getActiveFit() is None or srcContext != "commandView":
            return False
        return True

    def getText(self, callingWindow, itmContext):
        return _t("Generic Links")

    def _addLeaf(self, parentMenu, label, linkType, strength, mindlink):
        menuID = ContextMenuUnconditional.nextID()
        self.menuItemData[menuID] = (linkType, strength, mindlink)
        # On Windows menu items must be parented to the root menu for the binding to work
        parent = self.rootMenu if self.msw else parentMenu
        parentMenu.Append(wx.MenuItem(parent, menuID, label))

    def _addLinkSubmenu(self, parentMenu, linkType):
        """Build the strength x mindlink leaf submenu for a single link type."""
        leafMenu = wx.Menu()
        # Mindlink options on top, then a separator, then the non-mindlink ones
        for mindlink in (True, False):
            for strength in STRENGTHS:
                label = "{}%/lvl{}".format(strength, _t(" + Mindlink") if mindlink else "")
                self._addLeaf(leafMenu, label, linkType, strength, mindlink)
            if mindlink:
                leafMenu.AppendSeparator()
        # Bind once per leaf menu rather than once per item (binding is the slow part)
        if not self.msw:
            leafMenu.Bind(wx.EVT_MENU, self.handleSelection)
        item = wx.MenuItem(parentMenu, ContextMenuUnconditional.nextID(), _t(COMMAND_LINK_DEFS[linkType][0]))
        item.SetSubMenu(leafMenu)
        return item

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        self.context = context
        self.rootMenu = rootMenu
        self.msw = "wxMSW" in wx.PlatformInfo
        self.menuItemData = {}

        sub = wx.Menu()

        # One-click "Max Links": all links at maximum strength with mindlink
        self._addLeaf(sub, _t("Max Links"), ALL_LINK_TYPE, max(STRENGTHS), True)
        sub.AppendSeparator()

        # Top-level "All Links" (choose strength)
        sub.Append(self._addLinkSubmenu(sub, ALL_LINK_TYPE))
        sub.AppendSeparator()

        # Per-category submenus
        for category in CATEGORY_ORDER:
            catMenu = wx.Menu()
            for linkType in CATEGORY_LINKS[category]:
                catMenu.Append(self._addLinkSubmenu(catMenu, linkType))
            catItem = wx.MenuItem(sub, ContextMenuUnconditional.nextID(), _t(CATEGORY_LABELS[category]))
            catItem.SetSubMenu(catMenu)
            sub.Append(catItem)

        # Bind once for all command items rather than per item
        if self.msw:
            rootMenu.Bind(wx.EVT_MENU, self.handleSelection)
        else:
            sub.Bind(wx.EVT_MENU, self.handleSelection)

        return sub

    def handleSelection(self, event):
        data = self.menuItemData.get(event.Id)
        if data is None:
            event.Skip()
            return
        linkType, strength, mindlink = data
        fitID = self.mainFrame.getActiveFit()
        self.mainFrame.command.Submit(cmd.GuiAddCommandLinkCommand(
            fitID=fitID, linkType=linkType, strength=strength, mindlink=mindlink))


AddCommandLink.register()
