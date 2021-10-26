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

import gui.mainFrame
from eos.const import FittingSlot
from eos.saveddata.cargo import Cargo
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.fit import Fit, FitLite
from eos.saveddata.implant import Implant
from eos.saveddata.module import Module, Rack
from eos.saveddata.targetProfile import TargetProfile
from graphs.wrapper import BaseWrapper
from gui.builtinContextMenus.envEffectAdd import AddEnvironmentEffect
from gui.utils.numberFormatter import formatAmount
from gui.viewColumn import ViewColumn
from service.fit import Fit as FitSvc
from service.market import Market


pyfalog = Logger(__name__)
_t = wx.GetTranslation


class BaseName(ViewColumn):

    name = "Base Name"
    proportionWidth = 7

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.columnText = _t("Name")
        self.mask = wx.LIST_MASK_TEXT
        self.projectedView = isinstance(fittingView, gui.builtinAdditionPanes.projectedView.ProjectedView)
        self.rackTranslations = {
            FittingSlot.HIGH: _t('High'),
            FittingSlot.MED: _t('Med'),
            FittingSlot.LOW: _t('Low'),
            FittingSlot.SUBSYSTEM: _t('Subsystem'),
            FittingSlot.RIG: _t('Rig'),
            FittingSlot.SERVICE: _t('Service')
        }


    def getText(self, stuff):
        if isinstance(stuff, BaseWrapper):
            stuff = stuff.item

        if isinstance(stuff, Drone):
            if FitSvc.getInstance().serviceFittingOptions["expandedMutantNames"]:
                return "%dx %s" % (stuff.amount, stuff.fullName)
            else:
                return "%dx %s" % (stuff.amount, stuff.item.name)
        elif isinstance(stuff, Fighter):
            return "%d/%d %s" % \
                   (stuff.amount, stuff.getModifiedItemAttr("fighterSquadronMaxSize"), stuff.item.name)
        elif isinstance(stuff, Cargo):
            if stuff.item.group.name in ("Cargo Container", "Secure Cargo Container", "Audit Log Secure Container", "Freight Container"):
                capacity = stuff.item.getAttribute('capacity')
                if capacity:
                    return "{:d}x {} ({} m\u00B3)".format(stuff.amount, stuff.item.name, formatAmount(capacity, 3, 0, 6))
            return "{:d}x {}".format(stuff.amount, stuff.item.name)
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
        elif isinstance(stuff, FitLite):
            return "{} ({})".format(stuff.name, stuff.shipName)
        elif isinstance(stuff, Rack):
            if FitSvc.getInstance().serviceFittingOptions["rackLabels"]:
                if stuff.slot == FittingSlot.MODE:
                    return '─ {} ─'.format(_t('Tactical Mode'))
                else:
                    return '─ {} ─'.format(_t('{} {} Slot', '{} {} Slots', stuff.num).format(stuff.num, self.rackTranslations.get(stuff.slot, FittingSlot(stuff.slot).name.capitalize())))
            else:
                return ""
        elif isinstance(stuff, Module):
            if self.projectedView:
                # check for projected abyssal name
                name_check = stuff.item.customName[0:-2]
                type = AddEnvironmentEffect.abyssal_mapping.get(name_check, None)
                if type:
                    sMkt = Market.getInstance()
                    type = sMkt.getItem(type)
                    return "{} {}".format(type.name, stuff.item.customName[-1:])

            if stuff.isEmpty:
                return "%s Slot" % FittingSlot(stuff.slot).name.capitalize()
            else:
                if FitSvc.getInstance().serviceFittingOptions["expandedMutantNames"]:
                    return stuff.fullName
                else:
                    return stuff.item.customName
        elif isinstance(stuff, Implant):
            return stuff.item.name
        elif isinstance(stuff, TargetProfile):
            return stuff.shortName
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
