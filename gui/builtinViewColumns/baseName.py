# coding: utf-8
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
from eos.saveddata.cargo import Cargo
from eos.saveddata.implant import Implant
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.module import Module, Slot, Rack
from eos.saveddata.fit import Fit
from service.fit import Fit as FitSvc
from service.market import Market
from gui.viewColumn import ViewColumn
from gui.builtinContextMenus.whProjector import WhProjector
import gui.mainFrame

pyfalog = Logger(__name__)


class BaseName(ViewColumn):
    name = "Base Name"

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.columnText = "Name"
        self.shipImage = fittingView.imageList.GetImageIndex("ship_small", "gui")
        self.mask = wx.LIST_MASK_TEXT
        self.projectedView = isinstance(fittingView, gui.builtinAdditionPanes.projectedView.ProjectedView)

    def getText(self, stuff):
        if isinstance(stuff, Drone):
            return "%dx %s" % (stuff.amount, stuff.item.name)
        elif isinstance(stuff, Fighter):
            return "%d/%d %s" % \
                   (stuff.amountActive, stuff.getModifiedItemAttr("fighterSquadronMaxSize"), stuff.item.name)
        elif isinstance(stuff, Cargo):
            return "%dx %s" % (stuff.amount, stuff.item.name)
        elif isinstance(stuff, Fit):
            if self.projectedView:
                # we need a little more information for the projected view
                fitID = self.mainFrame.getActiveFit()
                info = stuff.getProjectionInfo(fitID)

                if info:
                    return "%dx %s (%s)" % (stuff.getProjectionInfo(fitID).amount, stuff.name, stuff.ship.item.name)

                pyfalog.warning("Projected View trying to display things that aren't there. stuff: {}, info: {}", repr(stuff),
                                info)
                return "<unknown>"
            else:
                return "%s (%s)" % (stuff.name, stuff.ship.item.name)
        elif isinstance(stuff, Rack):
            if FitSvc.getInstance().serviceFittingOptions["rackLabels"]:
                if stuff.slot == Slot.MODE:
                    return '─ Tactical Mode ─'
                else:
                    return '─ {} {} Slot{}─'.format(stuff.num, Slot.getName(stuff.slot).capitalize(), '' if stuff.num == 1 else 's')
            else:
                return ""
        elif isinstance(stuff, Module):
            if self.projectedView:
                # check for projected abyssal name
                name_check = stuff.item.name[0:-2]
                type = WhProjector.abyssal_mapping.get(name_check, None)
                if type:
                    sMkt = Market.getInstance()
                    type = sMkt.getItem(type)
                    return "{} {}".format(type.name, stuff.item.name[-1:])

            if stuff.isEmpty:
                return "%s Slot" % Slot.getName(stuff.slot).capitalize()
            else:
                return stuff.item.name
        elif isinstance(stuff, Implant):
            return stuff.item.name
        else:
            item = getattr(stuff, "item", stuff)

            if FitSvc.getInstance().serviceFittingOptions["showMarketShortcuts"]:
                marketShortcut = getattr(item, "marketShortcut", None)

                if marketShortcut:
                    # use unicode subscript to display shortcut value
                    shortcut = chr(marketShortcut + 8320) + " "
                    del item.marketShortcut
                    return shortcut + item.name

            return item.name


BaseName.register()
