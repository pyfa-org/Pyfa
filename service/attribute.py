# =============================================================================
# Copyright (C) 2010 Diego Duclos
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

from eos.gamedata import getAttributeInfo


class Attribute():
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Attribute()

        return cls.instance

    def getAttributeInfo(self, identity):
        if isinstance(identity, (int, basestring)):
            return getAttributeInfo(identity, eager=("icon", "unit"))
        elif isinstance(identity, (int, float)):
            return getAttributeInfo(int(identity), eager=("icon", "unit"))
        else:
            info = None
        return info
