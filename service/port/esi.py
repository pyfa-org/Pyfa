# =============================================================================
# Copyright (C) 2014 Ryan Holmes
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


import json
from collections import defaultdict

from logbook import Logger

from eos.const import FittingModuleState, FittingSlot
from eos.saveddata.cargo import Cargo
from eos.saveddata.citadel import Citadel
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.fit import Fit
from eos.saveddata.module import Module
from eos.saveddata.ship import Ship
from gui.fitCommands.helpers import activeStateLimit
from service.fit import Fit as svcFit
from service.market import Market


class ESIExportException(Exception):
    pass


pyfalog = Logger(__name__)

INV_FLAGS = {
    FittingSlot.LOW: 11,
    FittingSlot.MED: 19,
    FittingSlot.HIGH: 27,
    FittingSlot.RIG: 92,
    FittingSlot.SUBSYSTEM: 125,
    FittingSlot.SERVICE: 164
}

INV_FLAG_CARGOBAY = 5
INV_FLAG_DRONEBAY = 87
INV_FLAG_FIGHTER = 158


def exportESI(ofit, exportCharges, callback):
    # A few notes:
    # max fit name length is 50 characters
    # Most keys are created simply because they are required, but bogus data is okay

    nested_dict = lambda: defaultdict(nested_dict)
    fit = nested_dict()
    sFit = svcFit.getInstance()

    # max length is 50 characters
    name = ofit.name[:47] + '...' if len(ofit.name) > 50 else ofit.name
    fit['name'] = name
    fit['ship_type_id'] = ofit.ship.item.ID

    # 2017/03/29 NOTE: "<" or "&lt;" is Ignored
    # fit['description'] = "<pyfa:%d />" % ofit.ID
    fit['description'] = "" if ofit.notes is None else ofit.notes[:397] + '...' if len(ofit.notes) > 400 else ofit.notes
    fit['items'] = []

    slotNum = {}
    charges = {}
    for module in ofit.modules:
        if module.isEmpty:
            continue

        item = nested_dict()
        slot = module.slot

        if slot == FittingSlot.SUBSYSTEM:
            # Order of subsystem matters based on this attr. See GH issue #130
            slot = int(module.getModifiedItemAttr("subSystemSlot"))
            item['flag'] = slot
        else:
            if slot not in slotNum:
                slotNum[slot] = INV_FLAGS[slot]

            item['flag'] = slotNum[slot]
            slotNum[slot] += 1

        item['quantity'] = 1
        item['type_id'] = module.item.ID
        fit['items'].append(item)

        if module.charge and exportCharges:
            if module.chargeID not in charges:
                charges[module.chargeID] = 0
            # `or 1` because some charges (ie scripts) are without qty
            charges[module.chargeID] += module.numCharges or 1

    for cargo in ofit.cargo:
        item = nested_dict()
        item['flag'] = INV_FLAG_CARGOBAY
        item['quantity'] = cargo.amount
        item['type_id'] = cargo.item.ID
        fit['items'].append(item)

    for chargeID, amount in list(charges.items()):
        item = nested_dict()
        item['flag'] = INV_FLAG_CARGOBAY
        item['quantity'] = amount
        item['type_id'] = chargeID
        fit['items'].append(item)

    for drone in ofit.drones:
        item = nested_dict()
        item['flag'] = INV_FLAG_DRONEBAY
        item['quantity'] = drone.amount
        item['type_id'] = drone.item.ID
        fit['items'].append(item)

    for fighter in ofit.fighters:
        item = nested_dict()
        item['flag'] = INV_FLAG_FIGHTER
        item['quantity'] = fighter.amount
        item['type_id'] = fighter.item.ID
        fit['items'].append(item)

    if len(fit['items']) == 0:
        raise ESIExportException("Cannot export fitting: module list cannot be empty.")

    text = json.dumps(fit)

    if callback:
        callback(text)
    else:
        return text


def importESI(string):

    sMkt = Market.getInstance()
    fitobj = Fit()
    refobj = json.loads(string)
    items = refobj['items']
    # "<" and ">" is replace to "&lt;", "&gt;" by EVE client
    fitobj.name = refobj['name']
    # 2017/03/29: read description
    fitobj.notes = refobj['description']

    try:
        ship = refobj['ship_type_id']
        try:
            fitobj.ship = Ship(sMkt.getItem(ship))
        except ValueError:
            fitobj.ship = Citadel(sMkt.getItem(ship))
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        pyfalog.warning("Caught exception in importESI")
        return None

    items.sort(key=lambda k: k['flag'])

    moduleList = []
    for module in items:
        try:
            item = sMkt.getItem(module['type_id'], eager="group.category")
            if not item.published:
                continue
            if module['flag'] == INV_FLAG_DRONEBAY:
                d = Drone(item)
                d.amount = module['quantity']
                fitobj.drones.append(d)
            elif module['flag'] == INV_FLAG_CARGOBAY:
                c = Cargo(item)
                c.amount = module['quantity']
                fitobj.cargo.append(c)
            elif module['flag'] == INV_FLAG_FIGHTER:
                fighter = Fighter(item)
                fitobj.fighters.append(fighter)
            else:
                try:
                    m = Module(item)
                # When item can't be added to any slot (unknown item or just charge), ignore it
                except ValueError:
                    pyfalog.debug("Item can't be added to any slot (unknown item or just charge)")
                    continue
                # Add subsystems before modules to make sure T3 cruisers have subsystems installed
                if item.category.name == "Subsystem":
                    if m.fits(fitobj):
                        fitobj.modules.append(m)
                else:
                    if m.isValidState(FittingModuleState.ACTIVE):
                        m.state = activeStateLimit(m.item)

                    moduleList.append(m)

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pyfalog.warning("Could not process module.")
            continue

    # Recalc to get slot numbers correct for T3 cruisers
    sFit = svcFit.getInstance()
    sFit.recalc(fitobj)
    sFit.fill(fitobj)

    for module in moduleList:
        if module.fits(fitobj):
            fitobj.modules.append(module)

    return fitobj
