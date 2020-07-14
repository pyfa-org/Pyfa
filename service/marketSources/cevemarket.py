# =============================================================================
# Copyright (C) 2020 Copy Liu
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



class CEveMarketBase:

    @staticmethod
    def fetchPrices(priceMap, fetchTimeout, system=None, serenity=False):
        params = {'typeid': {typeID for typeID in priceMap}}
        if system is not None:
            params['usesystem'] = system
        baseurl = 'https://www.ceve-market.org/api/marketstat' if serenity else 'https://www.ceve-market.org/tqapi/marketstat'
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
            if percprice == 0 and system is not None:
                continue
            priceMap[typeID].update(PriceStatus.fetchSuccess, percprice)
            del priceMap[typeID]


class CEveMarketTq(CEveMarketBase):

    name = 'ceve-market.org (Tranquility)'
    group = 'tranquility'

    def __init__(self, priceMap, system, fetchTimeout):
        # Try selected system first
        self.fetchPrices(priceMap, max(2 * fetchTimeout / 3, 2), system, serenity=False)
        # If price was not available - try globally
        if priceMap:
            self.fetchPrices(priceMap, max(fetchTimeout / 3, 2), serenity=False)


class CEveMarketCn(CEveMarketBase):

    name = 'ceve-market.org (Serenity)'
    group = 'serenity'

    def __init__(self, priceMap, system, fetchTimeout):
        # Try selected system first
        self.fetchPrices(priceMap, max(2 * fetchTimeout / 3, 2), system, serenity=True)
        # If price was not available - try globally
        if priceMap:
            self.fetchPrices(priceMap, max(fetchTimeout / 3, 2), serenity=True)


Price.register(CEveMarketCn)
Price.register(CEveMarketTq)
