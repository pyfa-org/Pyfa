# ===============================================================================
# Copyright (C) 2015 Ryan Holmes
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

from sqlalchemy.orm import validates, reconstructor

import eos.db
from eos.eqBase import EqBase

pyfalog = Logger(__name__)


class Mutator(EqBase):
    """ Mutators are the object that represent an attribute override on the module level, in conjunction with
    mutaplasmids. Each mutated module, when created, is instantiated with a list of these objects, dictated by the
    mutaplasmid that is used on the base module.
    """

    def __init__(self, module, attr, value):
        self.module = module
        self.moduleID = module.ID
        self.attrID = attr.ID
        self.__attr = attr
        self.value = value

    @reconstructor
    def init(self):
        self.__attr = None

        if self.attrID:
            self.__attr = eos.db.getAttributeInfo(self.attrID)
            if self.__attr is None:
                pyfalog.error("Attribute (id: {0}) does not exist", self.attrID)
                return

        self.value = self.value  # run the validator (to ensure we catch any changed min/max values CCP releases)
        self.build()

    def build(self):
        pass

    @validates("value")
    def validator(self, key, val):
        """ Validates values as properly falling within the range of the modules mutaplasmid """
        dynAttr = next(a for a in self.module.mutaplasmid.attributes if a.attributeID == self.attrID)
        baseAttr = self.module.item.attributes[dynAttr.name]

        minValue = dynAttr.min * baseAttr.value
        maxValue = dynAttr.max * baseAttr.value
        mod = val/baseAttr.value

        if dynAttr.min < mod < dynAttr.max:
            # sweet, all good
            returnVal = val
        else:
            # need to fudge the numbers a bit. Go with the value closest to base
            returnVal = min(maxValue, max(minValue, val))

        return returnVal

    @property
    def isInvalid(self):
        # @todo: need to test what happens:
        # 1) if an attribute is removed from the EVE database
        # 2) if a mutaplasmid does not have the attribute anymore
        # 3) if a mutaplasmid does not exist (in eve or on the module's item)
        # Can remove invalid ones in a SQLAlchemy collection class... eventually
        return self.__attr is None

    @property
    def attr(self):
        return self.__attr

    @property
    def item(self):
        return self.__item
