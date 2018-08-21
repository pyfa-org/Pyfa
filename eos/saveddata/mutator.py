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

    A note on the different attributes on this object:
    * attribute: points to the definition of the attribute from dgmattribs.
    * baseAttribute: points to the attribute defined for the base item (contains the base value with with to mutate)
    * dynamicAttribute: points to the Mutaplasmid definition of the attribute, including min/max

    This could probably be cleaned up with smarter relationships, but whatever
    """

    def __init__(self, module, attr, value):
        # this needs to be above module assignment, as assigning the module will add it to the list and it via
        # relationship and needs this set 4correctly
        self.attrID = attr.ID

        self.module = module
        self.moduleID = module.ID

        self.__attr = attr
        self.build()
        self.value = value  # must run after the build(), because the validator requires build() to run first

    @reconstructor
    def init(self):
        self.__attr = None

        if self.attrID:
            self.__attr = eos.db.getAttributeInfo(self.attrID)
            if self.__attr is None:
                pyfalog.error("Attribute (id: {0}) does not exist", self.attrID)
                return

        self.build()
        self.value = self.value  # run the validator (to ensure we catch any changed min/max values might CCP release)

    def build(self):
        # try...except here to catch orphaned mutators. Pretty rare, only happens so far if hacking the database
        # But put it here to remove the module link if it happens, until a better solution can be developed
        try:
            # dynamic attribute links to the Mutaplasmids attribute definition for this mutated definition
            self.dynamicAttribute = next(a for a in self.module.mutaplasmid.attributes if a.attributeID == self.attrID)
            # base attribute links to the base ite's attribute for this mutated definition (contains original, base value)
            self.baseAttribute = self.module.item.attributes[self.dynamicAttribute.name]
        except:
            self.module = None

    @validates("value")
    def validator(self, key, val):
        """ Validates values as properly falling within the range of the modules' Mutaplasmid """
        mod = val / self.baseValue

        if self.minMod <= mod <= self.maxMod:
            # sweet, all good
            returnVal = val
        else:
            # need to fudge the numbers a bit. Go with the value closest to base
            if val >= 0:
                returnVal = min(self.maxValue, max(self.minValue, val))
            else:
                returnVal = max(self.maxValue, min(self.minValue, val))

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
    def highIsGood(self):
        return self.attribute.highIsGood

    @property
    def minMod(self):
        return round(self.dynamicAttribute.min, 3)

    @property
    def maxMod(self):
        return round(self.dynamicAttribute.max, 3)

    @property
    def baseValue(self):
        return self.baseAttribute.value

    @property
    def minValue(self):
        return self.minMod * self.baseAttribute.value

    @property
    def maxValue(self):
        return self.maxMod * self.baseAttribute.value

    @property
    def attribute(self):
        return self.__attr
