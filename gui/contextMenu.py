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

# noinspection PyPackageRequirements
import wx
from logbook import Logger

pyfalog = Logger(__name__)


class ContextMenu(object):
    menus = []
    _ids = []  # [wx.NewId() for x in xrange(200)]  # init with decent amount
    _idxid = -1

    @classmethod
    def register(cls):
        ContextMenu.menus.append(cls)

    @classmethod
    def getMenu(cls, selection, *fullContexts):
        """
        getMenu returns a menu that is used with wx.PopupMenu.

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
        cls._idxid = -1
        debug_start = len(cls._ids)

        rootMenu = wx.Menu()
        rootMenu.info = {}
        rootMenu.selection = (selection,) if not hasattr(selection, "__iter__") else selection
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
                if m.display(srcContext, selection):
                    display_amount += 1
                    texts = m.getText(itemContext, selection)

                    if isinstance(texts, str):
                        texts = (texts,)

                    bitmap = m.getBitmap(srcContext, selection)
                    multiple = not isinstance(bitmap, wx.Bitmap)
                    for it, text in enumerate(texts):
                        id = cls.nextID()
                        rootItem = wx.MenuItem(rootMenu, id, text)
                        rootMenu.info[id] = (m, fullContext, it)

                        sub = m.getSubMenu(srcContext, selection, rootMenu, it, rootItem)

                        if sub is None:
                            # if there is no sub menu, bind the handler to the rootItem
                            rootMenu.Bind(wx.EVT_MENU, cls.handler, rootItem)
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

                    empty = False

            if display_amount > 0 and i != len(fullContexts) - 1:
                rootMenu.AppendSeparator()

        debug_end = len(cls._ids)
        if debug_end - debug_start:
            pyfalog.debug("{0} new IDs created for this menu", (debug_end - debug_start))

        return rootMenu if empty is False else None

    @classmethod
    def handler(cls, event):
        menu = event.EventObject
        stuff = menu.info.get(event.Id)
        if stuff is not None:
            menuHandler, context, i = stuff
            selection = menu.selection
            if not hasattr(selection, "__iter__"):
                selection = (selection,)

            menuHandler.activate(context, selection, i)
        else:
            event.Skip()

    def display(self, context, selection):
        raise NotImplementedError()

    def activate(self, fullContext, selection, i):
        return None

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        return None

    @classmethod
    def nextID(cls):
        """
        Fetches an ID from the pool of IDs allocated to Context Menu.
        If we don't have enough ID's to fulfill request, create new
        ID and add it to the pool.

        See GH Issue #589
        """
        cls._idxid += 1

        if cls._idxid >= len(cls._ids):  # We don't ahve an ID for this index, create one
            cls._ids.append(wx.NewId())

        return cls._ids[cls._idxid]

    def getText(self, context, selection):
        """
        getText should be implemented in child classes, and should return either
        a string that will make up a menu item label or a list of strings which
        will make numerous menu items.

        These menu items will be added to the root menu
        """
        raise NotImplementedError()

    def getBitmap(self, context, selection):
        return None


# noinspection PyUnresolvedReferences
from gui.builtinContextMenus import (  # noqa: E402,F401
    openFit,
    moduleGlobalAmmoPicker,
    moduleAmmoPicker,
    itemStats,
    damagePattern,
    marketJump,
    droneSplit,
    itemRemove,
    droneRemoveStack,
    ammoPattern,
    project,
    factorReload,
    whProjector,
    cargo,
    shipJump,
    changeAffectingSkills,
    tacticalMode,
    targetResists,
    priceClear,
    priceOptions,
    amount,
    cargoAmmo,
    droneStack,
    metaSwap,
    implantSets,
    fighterAbilities,
    boosterSideEffects,
    commandFits,
    tabbedFits,
    mutaplasmids,
)
