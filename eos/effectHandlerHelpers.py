# ===============================================================================
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
# ===============================================================================

from logbook import Logger

pyfalog = Logger(__name__)


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

    def remove(self, thing):
        # We must flag it as modified, otherwise it not be removed from the database
        # @todo: flag_modified isn't in os x skel. need to rebuild to include
        # flag_modified(thing, "itemID")
        if thing.isInvalid:  # see GH issue #324
            thing.itemID = 0
        list.remove(self, thing)


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
            if mod.isInvalid:
                self.remove(mod)
            return

        mod.position = len(self)
        HandledList.append(self, mod)
        if mod.isInvalid:
            self.remove(mod)
            return

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
            dummy = mod.buildEmpty(mod.slot)
            dummy.position = index
            self[index] = dummy

    def toModule(self, index, mod):
        mod.position = index
        self[index] = mod

    def freeSlot(self, slot):
        for i in range(len(self)):
            mod = self[i]
            if mod.getModifiedItemAttr("subSystemSlot") == slot:
                self.toDummy(i)
                break


class HandledDroneCargoList(HandledList):
    def find(self, item):
        for o in self:
            if o.item == item:
                yield o

    def findFirst(self, item):
        for o in self.find(item):
            return o

    def append(self, thing):
        HandledList.append(self, thing)

        if thing.isInvalid:
            self.remove(thing)


class HandledImplantBoosterList(HandledList):
    def append(self, thing):
        if thing.isInvalid:
            HandledList.append(self, thing)
            self.remove(thing)
            return

        # if needed, remove booster that was occupying slot
        oldObj = next((m for m in self if m.slot == thing.slot), None)
        if oldObj:
            pyfalog.info("Slot {0} occupied with {1}, replacing with {2}", thing.slot, oldObj.item.name, thing.item.name)
            oldObj.itemID = 0  # hack to remove from DB. See GH issue #324
            self.remove(oldObj)

        HandledList.append(self, thing)


class HandledProjectedModList(HandledList):
    def append(self, proj):
        if proj.isInvalid:
            # we must include it before we remove it. doing it this way ensures
            # rows and relationships in database are removed as well
            HandledList.append(self, proj)
            self.remove(proj)
            return

        proj.projected = True
        isSystemEffect = proj.item.group.name == "Effect Beacon"

        if isSystemEffect:
            # remove other system effects - only 1 per fit plz
            oldEffect = next((m for m in self if m.item.group.name == "Effect Beacon"), None)

            if oldEffect:
                pyfalog.info("System effect occupied with {0}, replacing with {1}", oldEffect.item.name, proj.item.name)
                self.remove(oldEffect)

        HandledList.append(self, proj)

        # Remove non-projectable modules
        if not proj.item.isType("projected") and not isSystemEffect:
            self.remove(proj)


class HandledProjectedDroneList(HandledDroneCargoList):
    def append(self, proj):
        proj.projected = True
        HandledList.append(self, proj)

        # Remove invalid or non-projectable drones
        if proj.isInvalid or not proj.item.isType("projected"):
            self.remove(proj)


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
