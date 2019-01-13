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


def exportMultiBuy(fit):
    itemCounts = {}

    def addItem(item, quantity=1):
        if item not in itemCounts:
            itemCounts[item] = 0
        itemCounts[item] += quantity

    exportCharges = svcFit.getInstance().serviceFittingOptions["exportCharges"]
    for module in fit.modules:
        if module.item:
            addItem(module.item)
        if exportCharges and module.charge:
            addItem(module.charge, module.numCharges)

    for drone in fit.drones:
        addItem(drone.item, drone.amount)

    for fighter in fit.fighters:
        addItem(fighter.item, fighter.amountActive)

    for cargo in fit.cargo:
        addItem(cargo.item, cargo.amount)

    for implant in fit.implants:
        addItem(implant.item)

    for booster in fit.boosters:
        addItem(booster.item)

    exportLines = []
    exportLines.append(fit.ship.item.name)
    for item in sorted(itemCounts, key=lambda i: (i.group.category.name, i.group.name, i.name)):
        count = itemCounts[item]
        if count == 1:
            exportLines.append(item.name)
        else:
            exportLines.append('{} x{}'.format(item.name, count))

    return "\n".join(exportLines)
