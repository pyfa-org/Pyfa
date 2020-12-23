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


class EveMarketer:

    name = 'evemarketer'
    group = 'tranquility'

    def __init__(self, priceMap, system, fetchTimeout):
        # Try selected system first
        self.fetchPrices(priceMap, max(2 * fetchTimeout / 3, 2), system)
        # If price was not available - try globally
        if priceMap:
            self.fetchPrices(priceMap, max(fetchTimeout / 3, 2))

    @staticmethod
    def fetchPrices(priceMap, fetchTimeout, system=None):
        params = {'typeid': {typeID for typeID in priceMap}}
        if system is not None:
            params['usesystem'] = system
        baseurl = 'https://api.evemarketer.com/ec/marketstat'
        network = Network.getInstance()
        data = network.get(url=baseurl, type=network.PRICES, params=params, timeout=fetchTimeout)
        xml = minidom.parseString(data.text)
        types = xml.getElementsByTagName('marketstat').item(0).getElementsByTagName('type')
        # Cycle through all types we've got from request
        for type_ in types:
            # Get data out of each typeID details tree
            typeID = int(type_.getAttribute('id'))
            sell = type_.getElementsByTagName('sell').item(0)
            # If price data wasn't there, skip the item
            try:
                percprice = float(sell.getElementsByTagName('percentile').item(0).firstChild.data)
            except (TypeError, ValueError):
                pyfalog.warning('Failed to get price for: {0}', type_)
                continue

            # Price is 0 if evemarketer has info on this item, but it is not available
            # for current scope limit. If we provided scope limit - make sure to skip
            # such items to check globally, and do not skip if requested globally
            if percprice == 0 and system is not None:
                continue
            priceMap[typeID].update(PriceStatus.fetchSuccess, percprice)
            del priceMap[typeID]


Price.register(EveMarketer)
