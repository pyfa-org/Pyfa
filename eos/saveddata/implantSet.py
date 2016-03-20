#===============================================================================
# Copyright (C) 2016 Ryan Holmes
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

from eos.effectHandlerHelpers import HandledImplantBoosterList

class ImplantSet(object):
    DAMAGE_TYPES = ("em", "thermal", "kinetic", "explosive")

    def __init__(self, name=None):
        self.name = name
        self.__implants = HandledImplantBoosterList()

    @property
    def implants(self):
        return self.__implants


    EXPORT_FORMAT = "ImplantSet = %s,%d,%d,%d,%d\n"
    @classmethod
    def exportPatterns(cls, *patterns):
        out  = "# Exported from pyfa\n#\n"
        out += "# Values are in following format:\n"
        out += "# DamageProfile = [name],[EM amount],[Thermal amount],[Kinetic amount],[Explosive amount]\n\n"
        for dp in patterns:
            out += cls.EXPORT_FORMAT % (dp.name, dp.emAmount, dp.thermalAmount, dp.kineticAmount, dp.explosiveAmount)

        return out.strip()

    def __deepcopy__(self, memo):
        p = ImplantSet(self.name)
        p.name = "%s copy" % self.name
        return p
