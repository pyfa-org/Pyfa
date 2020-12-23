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


from logbook import Logger

from eos.saveddata.price import PriceStatus
from service.network import Network
from service.price import Price

pyfalog = Logger(__name__)


locations = {
    None: {},  # Universe
    30000142: {'station': 60003760},  # Jita 4-4 CNAP
    30002187: {'station': 60008494},  # Amarr VIII
    30002659: {'station': 60011866},  # Dodixie
    30002510: {'station': 60004588},  # Rens
    30002053: {'station': 60005686}}  # Hek


class FuzzworkMarket:

    name = 'fuzzwork market'
    group = 'tranquility'

    def __init__(self, priceMap, system, fetchTimeout):
        # Try selected system first
        self.fetchPrices(priceMap, max(2 * fetchTimeout / 3, 2), system)
        # If price was not available - try globally
        if priceMap:
            self.fetchPrices(priceMap, max(fetchTimeout / 3, 2))

    @staticmethod
    def fetchPrices(priceMap, fetchTimeout, system=None):
        params = {'types': ','.join(str(typeID) for typeID in priceMap)}
        for k, v in locations.get(system, {}).items():
            params[k] = v
        baseurl = 'https://market.fuzzwork.co.uk/aggregates/'
        network = Network.getInstance()
        resp = network.get(url=baseurl, type=network.PRICES, params=params, timeout=fetchTimeout)
        data = resp.json()
        # Cycle through all types we've got from request
        for typeID, typeData in data.items():
            try:
                typeID = int(typeID)
                price = float(typeData['sell']['percentile'])
            except (KeyError, TypeError):
                continue
            # Fuzzworks returns 0 when there's no data for item
            if price == 0:
                continue
            if typeID not in priceMap:
                continue
            priceMap[typeID].update(PriceStatus.fetchSuccess, price)
            del priceMap[typeID]


Price.register(FuzzworkMarket)
