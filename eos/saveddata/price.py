# ===============================================================================
# Copyright (C) 2010 Diego Duclos
# Copyright (C) 2011 Anton Vorobyov
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


from enum import IntEnum, unique
from time import time

from logbook import Logger


VALIDITY = 24 * 60 * 60  # Price validity period, 24 hours
REREQUEST = 4 * 60 * 60  # Re-request delay for failed fetches, 4 hours
TIMEOUT = 15 * 60  # Network timeout delay for connection issues, 15 minutes


pyfalog = Logger(__name__)


@unique
class PriceStatus(IntEnum):
    initialized = 0
    notSupported = 1
    fetchSuccess = 2
    fetchFail = 3
    fetchTimeout = 4


class Price:
    def __init__(self, typeID):
        self.typeID = typeID
        self.time = 0
        self.price = 0
        self.status = PriceStatus.initialized

    def isValid(self, validityOverride=None):
        # Always attempt to update prices which were just initialized, and prices
        # of unsupported items (maybe we start supporting them at some point)
        if self.status in (PriceStatus.initialized, PriceStatus.notSupported):
            return False
        elif self.status == PriceStatus.fetchSuccess:
            return time() <= self.time + (validityOverride if validityOverride is not None else VALIDITY)
        elif self.status == PriceStatus.fetchFail:
            return time() <= self.time + REREQUEST
        elif self.status == PriceStatus.fetchTimeout:
            return time() <= self.time + TIMEOUT
        else:
            return False

    def update(self, status, price=0):
        # Keep old price if we failed to fetch new one
        if status in (PriceStatus.fetchFail, PriceStatus.fetchTimeout):
            price = self.price
        elif status != PriceStatus.fetchSuccess:
            price = 0
        self.time = time()
        self.price = price
        self.status = status
