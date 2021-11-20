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


import eos.db

from logbook import Logger


pyfalog = Logger(__name__)


class MutaError(Exception):
    pass


class MutatedMixin:

    @property
    def isMutated(self):
        return bool(self.baseItemID and self.mutaplasmidID)

    @property
    def baseItem(self):
        return self.__baseItem

    @property
    def mutaplasmid(self):
        return self.__mutaplasmid

    @property
    def fullName(self):
        if self.isMutated:
            mutaShortName = self.mutaplasmid.shortName
            mutaFullName = self.mutaplasmid.item.customName
            # Short name can be unavailable for non-english language
            if mutaShortName != mutaFullName:
                return f'{self.mutaplasmid.shortName} {self.baseItem.customName}'
        return self.item.customName

    def _mutaInit(self, baseItem, mutaplasmid):
        self.baseItemID = baseItem.ID if baseItem is not None else None
        self.mutaplasmidID = mutaplasmid.ID if mutaplasmid is not None else None
        if baseItem is not None:
            # we're working with a mutated module, need to get abyssal module loaded with the base attributes
            # Note: there may be a better way of doing this, such as a metho on this classe to convert(mutaplamid). This
            # will require a bit more research though, considering there has never been a need to "swap" out the item of a Module
            # before, and there may be assumptions taken with regards to the item never changing (pre-calculated / cached results, for example)
            self._item = eos.db.getItemWithBaseItemAttribute(self._item.ID, self.baseItemID)
            self.__baseItem = baseItem
            self.__mutaplasmid = mutaplasmid
        else:
            self.__baseItem = None
            self.__mutaplasmid = None

    def _mutaReconstruct(self):
        self.__baseItem = None
        self.__mutaplasmid = None
        if self.baseItemID:
            self._item = eos.db.getItemWithBaseItemAttribute(self.itemID, self.baseItemID)
            self.__baseItem = eos.db.getItem(self.baseItemID)
            self.__mutaplasmid = eos.db.getMutaplasmid(self.mutaplasmidID)
            if self.__baseItem is None:
                pyfalog.error("Base Item (id: {0}) does not exist", self.itemID)
                raise MutaError

    def _mutaLoadMutators(self, mutatorClass):
        # Instantiate / remove mutators if this is a mutated module
        if self.__baseItem:
            for x in self.mutaplasmid.attributes:
                attr = self.item.attributes[x.name]
                id = attr.ID
                if id not in self.mutators:  # create the mutator
                    mutatorClass(self, attr, attr.value)
            # @todo: remove attributes that are no longer part of the mutaplasmid.

    @property
    def _mutaIsInvalid(self):
        if self.item.isAbyssal and not self.isMutated:
            return True
        if self.isMutated and not self.__mutaplasmid:
            return True
        return False

    def _mutaApplyMutators(self, mutatorClass, targetInstance=None):
        if targetInstance is None:
            targetInstance = self
        for x in self.mutators.values():
            mutatorClass(targetInstance, x.attribute, x.value)
