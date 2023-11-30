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


from xml.dom import minidom

from logbook import Logger

from eos.saveddata.price import PriceStatus
from service.network import Network
from service.price import Price

pyfalog = Logger(__name__)

locations = {
    30000142: (10000002, 60003760),  # Jita 4-4 CNAP
    30002187: (10000043, 60008494),  # Amarr VIII
    30002659: (10000032, 60011866),  # Dodixie
    30002510: (10000030, 60004588),  # Rens
    30002053: (10000042, 60005686)}  # Hek


class EveTycoon:

    name = 'evetycoon'
    group = 'tranquility'

    def __init__(self, priceMap, system, fetchTimeout):
        # Try selected system first
        self.fetchPrices(priceMap, max(2 * fetchTimeout / 3, 2), system)

    @staticmethod
    def fetchPrices(priceMap, fetchTimeout, system=None):
        # Default to jita when system is not found
        regionID, stationID = locations.get(system, locations[30000142])
        baseurl = 'https://evetycoon.com/api/v1/market/stats'
        network = Network.getInstance()
        # Cycle through all types we've got from request
        for typeID in tuple(priceMap):
            url = f'{baseurl}/{regionID}/{typeID}'
            resp = network.get(url=url, params={'locationId': stationID}, type=network.PRICES, timeout=fetchTimeout)
            if resp.status_code != 200:
                continue
            price = resp.json()['sellAvgFivePercent']
            # Price is 0 - no data
            if price == 0:
                continue
            priceMap[typeID].update(PriceStatus.fetchSuccess, price)
            del priceMap[typeID]


Price.register(EveTycoon)
