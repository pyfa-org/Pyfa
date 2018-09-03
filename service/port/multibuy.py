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


from service.fit import Fit as svcFit
from service.port.eft import SLOT_ORDER as EFT_SLOT_ORDER


def exportMultiBuy(fit):
    export = "%s\n" % fit.ship.item.name
    stuff = {}
    sFit = svcFit.getInstance()
    for module in fit.modules:
        slot = module.slot
        if slot not in stuff:
            stuff[slot] = []
        curr = "%s\n" % module.item.name if module.item else ""
        if module.charge and sFit.serviceFittingOptions["exportCharges"]:
            curr += "%s x%s\n" % (module.charge.name, module.numCharges)
        stuff[slot].append(curr)

    for slotType in EFT_SLOT_ORDER:
        data = stuff.get(slotType)
        if data is not None:
            # export += "\n"
            for curr in data:
                export += curr

    if len(fit.drones) > 0:
        for drone in fit.drones:
            export += "%s x%s\n" % (drone.item.name, drone.amount)

    if len(fit.cargo) > 0:
        for cargo in fit.cargo:
            export += "%s x%s\n" % (cargo.item.name, cargo.amount)

    if len(fit.implants) > 0:
        for implant in fit.implants:
            export += "%s\n" % implant.item.name

    if len(fit.boosters) > 0:
        for booster in fit.boosters:
            export += "%s\n" % booster.item.name

    if len(fit.fighters) > 0:
        for fighter in fit.fighters:
            export += "%s x%s\n" % (fighter.item.name, fighter.amountActive)

    if export[-1] == "\n":
        export = export[:-1]

    return export
