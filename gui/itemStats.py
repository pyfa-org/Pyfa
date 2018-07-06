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

import config
from service.market import Market
import gui.mainFrame
from gui.bitmap_loader import BitmapLoader

from gui.builtinItemStatsViews.itemTraits import ItemTraits
from gui.builtinItemStatsViews.itemDescription import ItemDescription
from gui.builtinItemStatsViews.itemAttributes import ItemParams
from gui.builtinItemStatsViews.itemCompare import ItemCompare
from gui.builtinItemStatsViews.itemRequirements import ItemRequirements
from gui.builtinItemStatsViews.itemDependants import ItemDependents
from gui.builtinItemStatsViews.itemEffects import ItemEffects
from gui.builtinItemStatsViews.itemAffectedBy import ItemAffectedBy
from gui.builtinItemStatsViews.itemProperties import ItemProperties
from gui.builtinItemStatsViews.itemMutator import ItemMutator

from eos.saveddata.module import Module


class ItemStatsDialog(wx.Dialog):
    counter = 0

    def __init__(
            self,
            victim,
            fullContext=None,
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            maximized=False
    ):

        wx.Dialog.__init__(
                self,
                gui.mainFrame.MainFrame.getInstance(),
                wx.ID_ANY,
                title="Item stats",
                pos=pos,
                size=size,
                style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU
        )

        empty = getattr(victim, "isEmpty", False)

        if empty:
            self.Hide()
            self.Destroy()
            return

        srcContext = fullContext[0]
        try:
            itmContext = fullContext[1]
        except IndexError:
            itmContext = None
        item = getattr(victim, "item", None) if srcContext.lower() not in (
            "projectedcharge",
            "fittingcharge"
        ) else getattr(victim, "charge", None)
        if item is None:
            sMkt = Market.getInstance()
            item = sMkt.getItem(victim.ID)
            victim = None
        self.context = itmContext
        if item.iconID is not None:
            itemImg = BitmapLoader.getBitmap(item.iconID, "icons")
            if itemImg is not None:
                self.SetIcon(wx.Icon(itemImg))
        self.SetTitle("%s: %s%s" % ("%s Stats" % itmContext if itmContext is not None else "Stats", item.name,
                                    " (%d)" % item.ID if config.debug else ""))

        self.SetMinSize((300, 200))
        if "wxGTK" in wx.PlatformInfo:  # GTK has huge tab widgets, give it a bit more room
            self.SetSize((580, 500))
        else:
            self.SetSize((550, 500))
        # self.SetMaxSize((500, -1))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.container = ItemStatsContainer(self, victim, item, itmContext)
        self.mainSizer.Add(self.container, 1, wx.EXPAND)

        if "wxGTK" in wx.PlatformInfo:
            self.closeBtn = wx.Button(self, wx.ID_ANY, "Close", wx.DefaultPosition, wx.DefaultSize, 0)
            self.mainSizer.Add(self.closeBtn, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
            self.closeBtn.Bind(wx.EVT_BUTTON, self.closeEvent)

        self.SetSizer(self.mainSizer)

        self.parentWnd = gui.mainFrame.MainFrame.getInstance()

        dlgsize = self.GetSize()
        psize = self.parentWnd.GetSize()
        ppos = self.parentWnd.GetPosition()

        ItemStatsDialog.counter += 1
        self.dlgOrder = ItemStatsDialog.counter

        counter = ItemStatsDialog.counter
        dlgStep = 30
        if counter * dlgStep > ppos.x + psize.width - dlgsize.x or counter * dlgStep > ppos.y + psize.height - dlgsize.y:
            ItemStatsDialog.counter = 1

        dlgx = ppos.x + counter * dlgStep
        dlgy = ppos.y + counter * dlgStep
        if pos == wx.DefaultPosition:
            self.SetPosition((dlgx, dlgy))
        else:
            self.SetPosition(pos)
        if maximized:
            self.Maximize(True)
        else:
            if size != wx.DefaultSize:
                self.SetSize(size)
        self.parentWnd.RegisterStatsWindow(self)

        self.Show()

        self.Bind(wx.EVT_CLOSE, self.closeEvent)
        self.Bind(wx.EVT_ACTIVATE, self.OnActivate)

    def OnActivate(self, event):
        self.parentWnd.SetActiveStatsWindow(self)

    def closeEvent(self, event):

        if self.dlgOrder == ItemStatsDialog.counter:
            ItemStatsDialog.counter -= 1
        self.parentWnd.UnregisterStatsWindow(self)

        event.Skip()


class ItemStatsContainer(wx.Panel):
    def __init__(self, parent, stuff, item, context=None):
        wx.Panel.__init__(self, parent)
        sMkt = Market.getInstance()

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.nbContainer = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.nbContainer, 1, wx.EXPAND | wx.ALL, 2)

        if item.traits is not None:
            self.traits = ItemTraits(self.nbContainer, stuff, item)
            self.nbContainer.AddPage(self.traits, "Traits")

        if isinstance(stuff, Module) and stuff.isMutated:
            self.mutator = ItemMutator(self.nbContainer, stuff, item)
            self.nbContainer.AddPage(self.mutator, "Mutations")

        self.desc = ItemDescription(self.nbContainer, stuff, item)
        self.nbContainer.AddPage(self.desc, "Description")

        self.params = ItemParams(self.nbContainer, stuff, item, context)
        self.nbContainer.AddPage(self.params, "Attributes")

        items = sMkt.getVariationsByItems([item])
        if len(items) > 1:
            self.compare = ItemCompare(self.nbContainer, stuff, item, items, context)
            self.nbContainer.AddPage(self.compare, "Compare")

        self.reqs = ItemRequirements(self.nbContainer, stuff, item)
        self.nbContainer.AddPage(self.reqs, "Requirements")

        if context == "Skill":
            self.dependents = ItemDependents(self.nbContainer, stuff, item)
            self.nbContainer.AddPage(self.dependents, "Dependents")

        self.effects = ItemEffects(self.nbContainer, stuff, item)
        self.nbContainer.AddPage(self.effects, "Effects")

        if stuff is not None:
            self.affectedby = ItemAffectedBy(self.nbContainer, stuff, item)
            self.nbContainer.AddPage(self.affectedby, "Affected by")

        if config.debug:
            self.properties = ItemProperties(self.nbContainer, stuff, item, context)
            self.nbContainer.AddPage(self.properties, "Properties")

        self.nbContainer.Bind(wx.EVT_LEFT_DOWN, self.mouseHit)
        self.SetSizer(mainSizer)
        self.Layout()

    def __del__(self):
        pass

    def mouseHit(self, event):
        tab, _ = self.nbContainer.HitTest(event.Position)
        if tab != -1:
            self.nbContainer.SetSelection(tab)
