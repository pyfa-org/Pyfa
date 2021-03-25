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
from sqlalchemy.orm.attributes import flag_dirty
from sqlalchemy.orm.collections import collection


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
        flag_dirty(thing)
        list.remove(self, thing)

    def sort(self, *args, **kwargs):
        # We need it here to prevent external users from accidentally sorting the list as alot of
        # external logic relies on keeping modules at their places
        raise NotImplementedError


class HandledModuleList(HandledList):

    def append(self, mod):
        emptyPosition = float("Inf")
        for i in range(len(self)):
            currMod = self[i]
            if currMod.isEmpty and not mod.isEmpty and currMod.slot == mod.slot:
                currPos = mod.position or i
                if currPos < emptyPosition:
                    emptyPosition = currPos

        if emptyPosition < len(self):
            mod.position = emptyPosition
            self.__toModule(emptyPosition, mod)
            if mod.isInvalid:
                self.__toDummy(mod.position)
        else:
            self.appendIgnoreEmpty(mod)

    @collection.appender
    def appendIgnoreEmpty(self, mod):
        mod.position = len(self)
        super().append(mod)
        if mod.isInvalid:
            self.remove(mod)

    def replace(self, idx, mod):
        try:
            oldMod = self[idx]
        except IndexError:
            return
        self.__toModule(idx, mod)
        if mod.isInvalid:
            self.__toModule(idx, oldMod)

    def replaceRackPosition(self, rackPosition, mod):
        listPositions = []
        for currPos in range(len(self)):
            currMod = self[currPos]
            if currMod.slot == mod.slot:
                listPositions.append(currPos)
        listPositions.sort()
        try:
            modListPosition = listPositions[rackPosition]
        except IndexError:
            self.appendIgnoreEmpty(mod)
        else:
            oldMod = self[modListPosition]
            if mod.isEmpty:
                self.__toDummy(modListPosition)
            else:
                self.__toModule(modListPosition, mod)
                # If new module cannot be appended, restore old state
                if mod.isInvalid:
                    if oldMod.isEmpty:
                        self.__toDummy(modListPosition)
                    else:
                        self.__toModule(modListPosition, oldMod)

    def insert(self, idx, mod):
        mod.position = idx
        i = idx
        while i < len(self):
            self[i].position += 1
            i += 1
        HandledList.insert(self, idx, mod)
        if mod.isInvalid:
            self.remove(mod)

    def remove(self, mod):
        HandledList.remove(self, mod)
        oldPos = mod.position
        mod.position = None
        for i in range(oldPos, len(self)):
            self[i].position -= 1

    def free(self, idx):
        self.__toDummy(idx)

    def __toDummy(self, index):
        mod = self[index]
        if not mod.isEmpty:
            dummy = mod.buildEmpty(mod.slot)
            dummy.position = index
            self[index] = dummy
            mod.position = None

    def __toModule(self, index, mod):
        oldMod = self[index]
        mod.position = index
        self[index] = mod
        oldMod.position = None


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

    def insert(self, idx, thing):
        HandledList.insert(self, idx, thing)
        if thing.isInvalid:
            self.remove(thing)


class HandledImplantList(HandledList):

    def append(self, implant):
        if implant.isInvalid:
            HandledList.append(self, implant)
            self.remove(implant)
            return
        if self.__slotCheck(implant):
            HandledList.append(self, implant)
            self.remove(implant)
            return
        HandledList.append(self, implant)

    def insert(self, idx, implant):
        if implant.isInvalid:
            HandledList.insert(self, idx, implant)
            self.remove(implant)
            return
        if self.__slotCheck(implant):
            HandledList.insert(self, idx, implant)
            self.remove(implant)
            return
        HandledList.insert(self, idx, implant)

    def makeRoom(self, implant):
        # if needed, remove booster that was occupying slot
        oldObj = next((i for i in self if i.slot == implant.slot), None)
        if oldObj is not None:
            pyfalog.info("Slot {0} occupied with {1}, replacing with {2}", implant.slot, oldObj.item.name, implant.item.name)
            position = self.index(oldObj)
            from gui.fitCommands.helpers import ImplantInfo
            implantInfo = ImplantInfo.fromImplant(oldObj)
            oldObj.itemID = 0  # hack to remove from DB. See GH issue #324
            self.remove(oldObj)
            return position, implantInfo
        return None, None

    def __slotCheck(self, implant):
        return any(i.slot == implant.slot for i in self)


class HandledBoosterList(HandledList):

    def append(self, booster):
        if booster.isInvalid:
            HandledList.append(self, booster)
            self.remove(booster)
            return
        if self.__slotCheck(booster):
            HandledList.append(self, booster)
            self.remove(booster)
            return
        HandledList.append(self, booster)

    def insert(self, idx, booster):
        if booster.isInvalid:
            HandledList.insert(self, idx, booster)
            self.remove(booster)
            return
        if self.__slotCheck(booster):
            HandledList.insert(self, idx, booster)
            self.remove(booster)
            return
        HandledList.insert(self, idx, booster)

    def makeRoom(self, booster):
        # if needed, remove booster that was occupying slot
        oldObj = next((b for b in self if b.slot == booster.slot), None)
        if oldObj is not None:
            pyfalog.info("Slot {0} occupied with {1}, replacing with {2}", booster.slot, oldObj.item.name, booster.item.name)
            position = self.index(oldObj)
            from gui.fitCommands.helpers import BoosterInfo
            boosterInfo = BoosterInfo.fromBooster(oldObj)
            oldObj.itemID = 0  # hack to remove from DB. See GH issue #324
            self.remove(oldObj)
            return position, boosterInfo
        return None, None

    def __slotCheck(self, booster):
        return any(b.slot == booster.slot for b in self)


class HandledSsoCharacterList(list):

    def append(self, character):
        old = next((x for x in self if x.client == character.client), None)
        if old is not None:
            pyfalog.warning("Removing SSO Character with same hash: {}".format(repr(old)))
            list.remove(self, old)

        list.append(self, character)


class HandledProjectedModList(HandledList):

    def append(self, proj):
        if proj.isInvalid:
            # we must include it before we remove it. doing it this way ensures
            # rows and relationships in database are removed as well
            HandledList.append(self, proj)
            self.remove(proj)
            return
        proj.projected = True
        HandledList.append(self, proj)
        # Remove non-projectable modules
        if not proj.item.isType("projected") and not proj.isExclusiveSystemEffect:
            self.remove(proj)

    def insert(self, idx, proj):
        if proj.isInvalid:
            # we must include it before we remove it. doing it this way ensures
            # rows and relationships in database are removed as well
            HandledList.insert(self, idx, proj)
            self.remove(proj)
            return
        proj.projected = True
        HandledList.insert(self, idx, proj)
        # Remove non-projectable modules
        if not proj.item.isType("projected") and not proj.isExclusiveSystemEffect:
            self.remove(proj)

    @property
    def currentSystemEffect(self):
        return next((m for m in self if m.isExclusiveSystemEffect), None)

    def makeRoom(self, proj):
        if proj.isExclusiveSystemEffect:
            # remove other system effects - only 1 per fit plz
            mod = self.currentSystemEffect

            if mod:
                pyfalog.info("System effect occupied with {0}, removing it to make space for {1}".format(mod.item.name, proj.item.name))
                position = self.index(mod)
                # We need to pack up this info, so whatever...
                from gui.fitCommands.helpers import ModuleInfo
                modInfo = ModuleInfo.fromModule(mod)
                self.remove(mod)
                return position, modInfo
        return None, None


class HandledProjectedDroneList(HandledDroneCargoList):

    def append(self, proj):
        proj.projected = True
        HandledList.append(self, proj)
        # Remove invalid or non-projectable drones
        if proj.isInvalid or not proj.item.isType("projected"):
            self.remove(proj)
            proj.projected = False

    def insert(self, idx, proj):
        proj.projected = True
        HandledList.insert(self, idx, proj)
        # Remove invalid or non-projectable drones
        if proj.isInvalid or not proj.item.isType("projected"):
            self.remove(proj)
            proj.projected = False


class HandledItem:
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


class HandledCharge:
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
