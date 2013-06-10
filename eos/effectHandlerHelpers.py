#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import eos.db
import eos.types

class HandledList(list):
    def filteredItemPreAssign(self, filter, *args, **kwargs):
        for element in self:
            try:
                if filter(element):
                    element.preAssignItemAttr(*args, **kwargs)
            except AttributeError:
                pass

    def filteredItemIncrease(self, filter, *args, **kwargs):
        for element in self:
            try:
                if filter(element):
                    element.increaseItemAttr(*args, **kwargs)
            except AttributeError:
                pass

    def filteredItemMultiply(self, filter, *args, **kwargs):
        for element in self:
            try:
                if filter(element):
                    element.multiplyItemAttr(*args, **kwargs)
            except AttributeError:
                pass

    def filteredItemBoost(self, filter, *args, **kwargs):
        for element in self:
            try:
                if filter(element):
                    element.boostItemAttr(*args, **kwargs)
            except AttributeError:
                pass

    def filteredItemForce(self, filter, *args, **kwargs):
        for element in self:
            try:
                if filter(element):
                    element.forceItemAttr(*args, **kwargs)
            except AttributeError:
                pass

    def filteredChargePreAssign(self, filter, *args, **kwargs):
        for element in self:
            try:
                if filter(element):
                    element.preAssignChargeAttr(*args, **kwargs)
            except AttributeError:
                pass

    def filteredChargeIncrease(self, filter, *args, **kwargs):
        for element in self:
            try:
                if filter(element):
                    element.increaseChargeAttr(*args, **kwargs)
            except AttributeError:
                pass

    def filteredChargeMultiply(self, filter, *args, **kwargs):
        for element in self:
            try:
                if filter(element):
                    element.multiplyChargeAttr(*args, **kwargs)
            except AttributeError:
                pass

    def filteredChargeBoost(self, filter, *args, **kwargs):
        for element in self:
            try:
                if filter(element):
                    element.boostChargeAttr(*args, **kwargs)
            except AttributeError:
                pass

    def filteredChargeForce(self, filter, *args, **kwargs):
        for element in self:
            try:
                if filter(element):
                    element.forceChargeAttr(*args, **kwargs)
            except AttributeError:
                pass

class HandledModuleList(HandledList):
    def append(self, mod):
        emptyPosition = float("Inf")
        for i in xrange(len(self)):
            currMod = self[i]
            if currMod.isEmpty and not mod.isEmpty and currMod.slot == mod.slot:
                currPos = mod.position or i
                if currPos < emptyPosition:
                    emptyPosition = currPos

        if emptyPosition < len(self):
            del self[emptyPosition]
            mod.position = emptyPosition
            HandledList.insert(self, emptyPosition, mod)
            return

        mod.position = len(self)
        HandledList.append(self, mod)

    def insert(self, index, mod):
        mod.position = index
        i = index
        while i < len(self):
            self[i].position += 1
            i += 1
        HandledList.insert(self, index, mod)

    def remove(self, mod):
        HandledList.remove(self, mod)
        oldPos = mod.position

        mod.position = None
        for i in xrange(oldPos, len(self)):
            self[i].position -= 1

    def toDummy(self, index):
        mod = self[index]
        if not mod.isEmpty:
            dummy = eos.types.Module.buildEmpty(mod.slot)
            dummy.position = index
            self[index] = dummy

    def freeSlot(self, slot):
        for i in range(len(self) -1, -1, -1):
            mod = self[i]
            if mod.getModifiedItemAttr("subSystemSlot") == slot:
                del self[i]

class HandledDroneList(HandledList):
    def find(self, item):
        for d in self:
            if d.item == item:
                yield d

    def findFirst(self, item):
        for d in self.find(item):
            return d

    def append(self, drone):
        list.append(self, drone)

    def remove(self, drone):
        HandledList.remove(self, drone)

    def appendItem(self, item, amount = 1):
        if amount < 1: ValueError("Amount of drones to add should be >= 1")
        d = self.findFirst(item)

        if d is None:
            d = eos.types.Drone(item)
            self.append(d)

        d.amount += amount
        return d

    def removeItem(self, item, amount):
        if amount < 1: ValueError("Amount of drones to remove should be >= 1")
        d = self.findFirst(item)
        if d is None: return
        d.amount -= amount
        if d.amount <= 0:
            self.remove(d)
            return None

        return d


class HandledImplantBoosterList(HandledList):
    def __init__(self):
        self.__slotCache = {}

    def append(self, implant):
        if self.__slotCache.has_key(implant.slot):
            raise ValueError("Implant/Booster slot already in use, remove the old one first or set replace = True")
        self.__slotCache[implant.slot] = implant
        HandledList.append(self, implant)

    def remove(self, implant):
        HandledList.remove(self, implant)
        del self.__slotCache[implant.slot]
        # While we deleted this implant, in edge case seems like not all references
        # to it are removed and object still lives in session; forcibly remove it,
        # or otherwise when adding the same booster twice booster's table (typeID, fitID)
        # constraint will report database integrity error
        # TODO: make a proper fix, probably by adjusting fit-boosters sqlalchemy relationships
        eos.db.remove(implant)

    def freeSlot(self, slot):
        if hasattr(slot, "slot"):
            slot = slot.slot

        try:
            implant = self.__slotCache[slot]
        except KeyError:
            return False
        try:
            self.remove(implant)
        except ValueError:
            return False
        return True

class HandledProjectedModList(HandledList):
    def append(self, proj):
        proj.projected = True
        HandledList.append(self, proj)

class HandledProjectedDroneList(HandledDroneList):
    def append(self, proj):
        proj.projected = True
        list.append(self, proj)

class HandledProjectedFitList(HandledList):
    def append(self, proj):
        proj.projected = True
        list.append(self, proj)

class HandledItem(object):
    def preAssignItemAttr(self, *args, **kwargs):
        self.itemModifiedAttributes.preAssign(*args, **kwargs)

    def increaseItemAttr(self, *args, **kwargs):
        self.itemModifiedAttributes.increase(*args, **kwargs)

    def multiplyItemAttr(self, *args, **kwargs):
        self.itemModifiedAttributes.multiply(*args, **kwargs)

    def boostItemAttr(self, *args, **kwargs):
        self.itemModifiedAttributes.boost(*args, **kwargs)

    def forceItemAttr(self, *args, **kwargs):
        self.itemModifiedAttributes.force(*args, **kwargs)

class HandledCharge(object):
    def preAssignChargeAttr(self, *args, **kwargs):
        self.chargeModifiedAttributes.preAssign(*args, **kwargs)

    def increaseChargeAttr(self, *args, **kwargs):
        self.chargeModifiedAttributes.increase(*args, **kwargs)

    def multiplyChargeAttr(self, *args, **kwargs):
        self.chargeModifiedAttributes.multiply(*args, **kwargs)

    def boostChargeAttr(self, *args, **kwargs):
        self.chargeModifiedAttributes.boost(*args, **kwargs)

    def forceChargeAttr(self, *args, **kwargs):
        self.chargeModifiedAttributes.force(*args, **kwargs)
