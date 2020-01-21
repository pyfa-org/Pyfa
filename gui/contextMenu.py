# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

from abc import ABCMeta, abstractmethod

# noinspection PyPackageRequirements
import wx
from logbook import Logger

from service.settings import ContextMenuSettings


pyfalog = Logger(__name__)


class ContextMenu(metaclass=ABCMeta):

    menus = []
    _ids = []  # [wx.NewId() for x in xrange(200)]  # init with decent amount
    _idxid = -1
    visibilitySetting = None

    @classmethod
    def register(cls):
        pyfalog.debug('registering context menu class {}'.format(cls.__name__))
        ContextMenu.menus.append(cls)

    @classmethod
    def hasMenu(cls, callingWindow, mainItem, selection, *fullContexts):
        for i, fullContext in enumerate(fullContexts):
            srcContext = fullContext[0]
            for menuHandler in cls.menus:
                m = menuHandler()
                if m._baseDisplay(callingWindow, srcContext, mainItem, selection):
                    return True
            return False

    @classmethod
    def getMenu(cls, callingWindow, mainItem, selection, *fullContexts):
        """
        getMenu returns a menu that is used with wx.PopupMenu.

        callingWindow: window (in wx' sense) which requested menu
        mainItem: usually, provides item which was clicked. Useful for single-
            item actions when user has multiple items selected
        selection: provides a list of what was selected. If only 1 item was
            selected, it's is a 1-item list or tuple. Can also be None for
            contexts without selection, such as statsPane or projected view
        fullContexts: a number of tuples of the following tuple:
            srcContext - context were menu was spawned, eg: projectedFit,
                         cargoItem, etc
            itemContext - usually the name of the item's category

            eg:
                (('fittingModule', 'Module'), ('fittingShip', 'Ship'))
                (('marketItemGroup', 'Implant'),)
                (('fittingShip', 'Ship'),)
        """
        ContextMenu._idxid = -1
        debug_start = len(ContextMenu._ids)

        # Control being pressed forces all hidden menu items to be shown
        visibilitySettingOverride = wx.GetMouseState().GetModifiers() == wx.MOD_CONTROL
        cmSettings = ContextMenuSettings.getInstance()

        rootMenu = wx.Menu()
        rootMenu.info = {}
        rootMenu.selection = (selection,) if not hasattr(selection, "__iter__") else selection
        rootMenu.mainItem = mainItem
        empty = True
        for i, fullContext in enumerate(fullContexts):
            display_amount = 0
            srcContext = fullContext[0]
            try:
                itemContext = fullContext[1]
            except IndexError:
                itemContext = None
            for menuHandler in cls.menus:
                # loop through registered menus
                m = menuHandler()
                if m.visibilitySetting:
                    visible = visibilitySettingOverride or cmSettings.get(m.visibilitySetting)
                else:
                    visible = True
                if visible and m._baseDisplay(callingWindow, srcContext, mainItem, selection):
                    display_amount += 1
                    texts = m._baseGetText(callingWindow, itemContext, mainItem, selection)

                    if isinstance(texts, str):
                        texts = (texts,)

                    bitmap = m._baseGetBitmap(callingWindow, srcContext, mainItem, selection)
                    multiple = not isinstance(bitmap, wx.Bitmap)
                    for it, text in enumerate(texts):
                        id = ContextMenu.nextID()
                        check = m.isChecked(it)
                        rootItem = wx.MenuItem(rootMenu, id, text, kind=wx.ITEM_NORMAL if check is None else wx.ITEM_CHECK)
                        rootMenu.info[id] = (m, callingWindow, fullContext, it)

                        sub = m._baseGetSubMenu(callingWindow, srcContext, mainItem, selection, rootMenu, it, rootItem)

                        if sub is None:
                            # if there is no sub menu, bind the handler to the rootItem
                            rootMenu.Bind(wx.EVT_MENU, ContextMenu.handler, rootItem)
                        elif sub:
                            # If sub exists and is not False, set submenu.
                            # Sub might return False when we have a mix of
                            # single menu items and submenus (see: damage profile
                            # context menu)
                            #
                            # If there is a submenu, it is expected that the sub
                            # logic take care of it's own bindings, including for
                            # any single root items. No binding is done here
                            #
                            # It is important to remember that when binding sub
                            # menu items, the menu to bind to depends on platform.
                            # Windows should bind to rootMenu, and all other
                            # platforms should bind to sub menu. See existing
                            # implementations for examples.
                            rootItem.SetSubMenu(sub)

                        if bitmap is not None:
                            if multiple:
                                bp = bitmap[it]
                                if bp:
                                    rootItem.SetBitmap(bp)
                            else:
                                rootItem.SetBitmap(bitmap)

                        rootMenu.Append(rootItem)

                        if check is not None:
                            rootItem.Check(check)
                        rootItem.Enable(m.enabled)

                    empty = False

            if display_amount > 0 and i != len(fullContexts) - 1:
                rootMenu.AppendSeparator()

        debug_end = len(ContextMenu._ids)
        if debug_end - debug_start:
            pyfalog.debug("{} new IDs created for this menu".format(debug_end - debug_start))

        return rootMenu if empty is False else None

    @staticmethod
    def handler(event):
        menu = event.EventObject
        stuff = menu.info.get(event.Id)
        if stuff is not None:
            menuHandler, callingWindow, context, i = stuff
            selection = menu.selection
            mainItem = menu.mainItem
            if not hasattr(selection, "__iter__"):
                selection = (selection,)

            menuHandler._baseActivate(callingWindow, context, mainItem, selection, i)
        else:
            event.Skip()

    @staticmethod
    def nextID():
        """
        Fetches an ID from the pool of IDs allocated to Context Menu.
        If we don't have enough ID's to fulfill request, create new
        ID and add it to the pool.

        See GH Issue #589.
        Has to be static method to properly handle modifications of primitives from subclasses (_idxid).
        """
        ContextMenu._idxid += 1

        if ContextMenu._idxid >= len(ContextMenu._ids):  # We don't ahve an ID for this index, create one
            ContextMenu._ids.append(wx.NewId())

        return ContextMenu._ids[ContextMenu._idxid]

    def isChecked(self, i):
        """If menu item is toggleable, this should return bool value"""
        return None

    @property
    def enabled(self):
        """If menu item is enabled. Allows an item to display, but not be selected"""
        return True

    @abstractmethod
    def _baseDisplay(self, callingWindow, context, mainItem, selection):
        raise NotImplementedError

    @abstractmethod
    def _baseGetBitmap(self, callingWindow, context, mainItem, selection):
        raise NotImplementedError

    @abstractmethod
    def _baseGetText(self, callingWindow, context, mainItem, selection):
        """
        getText should be implemented in child classes, and should return either
        a string that will make up a menu item label or a list of strings which
        will make numerous menu items.

        These menu items will be added to the root menu
        """
        raise NotImplementedError

    @abstractmethod
    def _baseGetSubMenu(self, callingWindow, context, mainItem, selection, rootMenu, i, pitem):
        raise NotImplementedError

    @abstractmethod
    def _baseActivate(self, callingWindow, fullContext, mainItem, selection, i):
        raise NotImplementedError


class ContextMenuUnconditional(ContextMenu, metaclass=ABCMeta):
    """
    Should be used for context menus which do not depend on which item
    has been clicked and what current selection is.
    """

    @abstractmethod
    def display(self, callingWindow, context):
        raise NotImplementedError

    def getBitmap(self, callingWindow, context):
        return

    @abstractmethod
    def getText(self, callingWindow, context):
        raise NotImplementedError

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        return

    def activate(self, callingWindow, fullContext, i):
        return

    def _baseDisplay(self, callingWindow, context, mainItem, selection):
        return self.display(callingWindow, context)

    def _baseGetBitmap(self, callingWindow, context, mainItem, selection):
        return self.getBitmap(callingWindow, context)

    def _baseGetText(self, callingWindow, context, mainItem, selection):
        return self.getText(callingWindow, context)

    def _baseGetSubMenu(self, callingWindow, context, mainItem, selection, rootMenu, i, pitem):
        return self.getSubMenu(callingWindow, context, rootMenu, i, pitem)

    def _baseActivate(self, callingWindow, fullContext, mainItem, selection, i):
        return self.activate(callingWindow, fullContext, i)


class ContextMenuSingle(ContextMenu, metaclass=ABCMeta):
    """
    Should be used for context menus which depend on
    which item was clicked, but not on selection.
    """

    @abstractmethod
    def display(self, callingWindow, context, mainItem):
        raise NotImplementedError

    def getBitmap(self, callingWindow, context, mainItem):
        return

    @abstractmethod
    def getText(self, callingWindow, context, mainItem):
        raise NotImplementedError

    def getSubMenu(self, callingWindow, context, mainItem, rootMenu, i, pitem):
        return

    def activate(self, callingWindow, fullContext, mainItem, i):
        return

    def _baseDisplay(self, callingWindow, context, mainItem, selection):
        return self.display(callingWindow, context, mainItem)

    def _baseGetBitmap(self, callingWindow, context, mainItem, selection):
        return self.getBitmap(callingWindow, context, mainItem)

    def _baseGetText(self, callingWindow, context, mainItem, selection):
        return self.getText(callingWindow, context, mainItem)

    def _baseGetSubMenu(self, callingWindow, context, mainItem, selection, rootMenu, i, pitem):
        return self.getSubMenu(callingWindow, context, mainItem, rootMenu, i, pitem)

    def _baseActivate(self, callingWindow, fullContext, mainItem, selection, i):
        return self.activate(callingWindow, fullContext, mainItem, i)


class ContextMenuSelection(ContextMenu, metaclass=ABCMeta):
    """
    Should be used for context menus which depend on which items are
    selected. Item clicked is used as fallback if no selection provided.
    """

    @abstractmethod
    def display(self, callingWindow, context, selection):
        raise NotImplementedError

    def getBitmap(self, callingWindow, context, selection):
        return

    @abstractmethod
    def getText(self, callingWindow, context, selection):
        raise NotImplementedError

    def getSubMenu(self, callingWindow, context, selection, rootMenu, i, pitem):
        return

    def activate(self, callingWindow, fullContext, selection, i):
        return

    def _baseDisplay(self, callingWindow, context, mainItem, selection):
        selection = self.__getSelection(selection, mainItem)
        return self.display(callingWindow, context, selection)

    def _baseGetBitmap(self, callingWindow, context, mainItem, selection):
        selection = self.__getSelection(selection, mainItem)
        return self.getBitmap(callingWindow, context, selection)

    def _baseGetText(self, callingWindow, context, mainItem, selection):
        selection = self.__getSelection(selection, mainItem)
        return self.getText(callingWindow, context, selection)

    def _baseGetSubMenu(self, callingWindow, context, mainItem, selection, rootMenu, i, pitem):
        selection = self.__getSelection(selection, mainItem)
        return self.getSubMenu(callingWindow, context, selection, rootMenu, i, pitem)

    def _baseActivate(self, callingWindow, fullContext, mainItem, selection, i):
        selection = self.__getSelection(selection, mainItem)
        return self.activate(callingWindow, fullContext, selection, i)

    def __getSelection(self, selection, mainItem):
        if mainItem is not None and mainItem not in selection:
            selection.append(mainItem)
        return selection


class ContextMenuCombined(ContextMenu, metaclass=ABCMeta):
    """
    Should be used for context menus which depend on both which
    item has been clicked and which items are selected.
    """

    @abstractmethod
    def display(self, callingWindow, context, mainItem, selection):
        raise NotImplementedError

    def getBitmap(self, callingWindow, context, mainItem, selection):
        return

    @abstractmethod
    def getText(self, callingWindow, context, mainItem, selection):
        raise NotImplementedError

    def getSubMenu(self, callingWindow, context, mainItem, selection, rootMenu, i, pitem):
        return

    def activate(self, callingWindow, fullContext, mainItem, selection, i):
        return

    def _baseDisplay(self, callingWindow, context, mainItem, selection):
        selection = self.__getSelection(selection, mainItem)
        return self.display(callingWindow, context, mainItem, selection)

    def _baseGetBitmap(self, callingWindow, context, mainItem, selection):
        selection = self.__getSelection(selection, mainItem)
        return self.getBitmap(callingWindow, context, mainItem, selection)

    def _baseGetText(self, callingWindow, context, mainItem, selection):
        selection = self.__getSelection(selection, mainItem)
        return self.getText(callingWindow, context, mainItem, selection)

    def _baseGetSubMenu(self, callingWindow, context, mainItem, selection, rootMenu, i, pitem):
        selection = self.__getSelection(selection, mainItem)
        return self.getSubMenu(callingWindow, context, mainItem, selection, rootMenu, i, pitem)

    def _baseActivate(self, callingWindow, fullContext, mainItem, selection, i):
        selection = self.__getSelection(selection, mainItem)
        return self.activate(callingWindow, fullContext, mainItem, selection, i)

    def __getSelection(self, selection, mainItem):
        if mainItem is not None and mainItem not in selection:
            selection.append(mainItem)
        return selection


import gui.builtinContextMenus
