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


from enum import IntEnum, unique

from service.price import Price as sPrc


@unique
class Options(IntEnum):
    IMPLANTS = 1
    CARGO = 2
    LOADED_CHARGES = 3
    OPTIMIZE_PRICES = 4


MULTIBUY_OPTIONS = (
    (Options.LOADED_CHARGES.value, 'Loaded Charges', 'Export charges loaded into modules', True),
    (Options.IMPLANTS.value, 'Implants && Boosters', 'Export implants and boosters', False),
    (Options.CARGO.value, 'Cargo', 'Export cargo contents', True),
    (Options.OPTIMIZE_PRICES.value, 'Optimize Prices', 'Replace items by cheaper alternatives', False),
)


def exportMultiBuy(fit, options, callback):
    itemAmounts = {}

    for module in fit.modules:
        if module.item:
            # Mutated items are of no use for multibuy
            if module.isMutated:
                continue
            _addItem(itemAmounts, module.item)
        if module.charge and options[Options.LOADED_CHARGES.value]:
            _addItem(itemAmounts, module.charge, module.numCharges)

    for drone in fit.drones:
        _addItem(itemAmounts, drone.item, drone.amount)

    for fighter in fit.fighters:
        _addItem(itemAmounts, fighter.item, fighter.amountActive)

    if options[Options.CARGO.value]:
        for cargo in fit.cargo:
            _addItem(itemAmounts, cargo.item, cargo.amount)

    if options[Options.IMPLANTS.value]:
        for implant in fit.implants:
            _addItem(itemAmounts, implant.item)

        for booster in fit.boosters:
            _addItem(itemAmounts, booster.item)

    if options[Options.OPTIMIZE_PRICES.value]:

        def processCheaperMapCb(replacementsCheaper):
            updatedAmounts = {}
            for item, itemAmount in itemAmounts.items():
                _addItem(updatedAmounts, replacementsCheaper.get(item, item), itemAmount)
            string = _prepareString(fit.ship.item, updatedAmounts)
            callback(string)

        priceSvc = sPrc.getInstance()
        priceSvc.findCheaperReplacements(itemAmounts, processCheaperMapCb)
    else:
        string = _prepareString(fit.ship.item, itemAmounts)
        if callback:
            callback(string)
        else:
            return string


def _addItem(container, item, quantity=1):
    if item not in container:
        container[item] = 0
    container[item] += quantity


def _prepareString(shipItem, itemAmounts):
    exportLines = []
    exportLines.append(shipItem.name)
    for item in sorted(itemAmounts, key=lambda i: (i.group.category.name, i.group.name, i.name)):
        count = itemAmounts[item]
        if count == 1:
            exportLines.append(item.name)
        else:
            exportLines.append('{} x{}'.format(item.name, count))

    return "\n".join(exportLines)
