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

import eos.db


class Attribute(object):
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Attribute()

        return cls.instance

    @staticmethod
    def getAttributeInfo(identity):
        if isinstance(identity, (int, str)):
            info = eos.db.getAttributeInfo(identity, eager=("icon", "unit"))
        elif isinstance(identity, (int, float)):
            id_ = int(identity)
            info = eos.db.getAttributeInfo(id_, eager=("icon", "unit"))
        else:
            info = None
        return info
