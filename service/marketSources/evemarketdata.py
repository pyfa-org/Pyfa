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


class EveMarketData:

    name = 'eve-marketdata.com'
    group = 'tranquility'

    def __init__(self, priceMap, system, fetchTimeout):
        # Try selected system first
        self.fetchPrices(priceMap, max(2 * fetchTimeout / 3, 2), system)
        # If price was not available - try globally
        if priceMap:
            self.fetchPrices(priceMap, max(fetchTimeout / 3, 2))

    @staticmethod
    def fetchPrices(priceMap, fetchTimeout, system=None):
        params = {'type_ids': ','.join(str(typeID) for typeID in priceMap)}
        if system is not None:
            params['system_id'] = system
        baseurl = 'https://eve-marketdata.com/api/item_prices.xml'
        network = Network.getInstance()
        data = network.get(url=baseurl, type=network.PRICES, params=params, timeout=fetchTimeout)
        xml = minidom.parseString(data.text)
        types = xml.getElementsByTagName('eve').item(0).getElementsByTagName('price')

        # Cycle through all types we've got from request
        for type_ in types:
            # Get data out of each typeID details tree
            typeID = int(type_.getAttribute('id'))

            try:
                price = float(type_.firstChild.data)
            except (TypeError, ValueError):
                pyfalog.warning('Failed to get price for: {0}', type_)
                continue

            # eve-marketdata returns 0 if price data doesn't even exist for the item
            if price == 0:
                continue
            priceMap[typeID].update(PriceStatus.fetchSuccess, price)
            del priceMap[typeID]


# Price.register(EveMarketData)
