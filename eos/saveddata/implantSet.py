# ===============================================================================
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
# ===============================================================================

from copy import deepcopy

from eos.effectHandlerHelpers import HandledImplantBoosterList


class ImplantSet(object):
    def __init__(self, name=None):
        self.name = name
        self.__implants = HandledImplantBoosterList()

    @property
    def implants(self):
        return self.__implants

    @classmethod
    def exportSets(cls, *sets):
        out = "# Exported from pyfa\n#\n" \
              "# Values are in following format:\n" \
              "# [Implant Set name]\n" \
              "# [Implant name]\n" \
              "# [Implant name]\n" \
              "# ...\n\n"

        for set in sets:
            out += "[{}]\n".format(set.name)
            for implant in set.implants:
                out += "{}\n".format(implant.item.name)
            out += "\n"

        return out.strip()

    def __deepcopy__(self, memo):
        copy = ImplantSet(self.name)
        copy.name = "%s copy" % self.name

        orig = getattr(self, 'implants')
        c = getattr(copy, 'implants')
        for i in orig:
            c.append(deepcopy(i))

        return copy
