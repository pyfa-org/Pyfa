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

systemAliases = {
    None: 'universe',
    30000142: 'jita',
    30002187: 'amarr',
    30002659: 'dodixie',
    30002510: 'rens',
    30002053: 'hek'}


class EvePraisal:

    name = 'evepraisal'
    group = 'tranquility'

    def __init__(self, priceMap, system, fetchTimeout):
        # Try selected system first
        self.fetchPrices(priceMap, max(2 * fetchTimeout / 3, 2), system)
        # If price was not available - try globally
        if priceMap:
            self.fetchPrices(priceMap, max(fetchTimeout / 3, 2))

    @staticmethod
    def fetchPrices(priceMap, fetchTimeout, system=None):
        if system not in systemAliases:
            return
        jsonData = {
            'market_name': systemAliases[system],
            'items': [{'type_id': typeID} for typeID in priceMap]}
        baseurl = 'https://evepraisal.com/appraisal/structured.json'
        network = Network.getInstance()
        resp = network.post(baseurl, network.PRICES, jsonData=jsonData, timeout=fetchTimeout)
        data = resp.json()
        try:
            itemsData = data['appraisal']['items']
        except (KeyError, TypeError):
            return
        # Cycle through all types we've got from request
        for itemData in itemsData:
            try:
                typeID = int(itemData['typeID'])
                price = itemData['prices']['sell']['min']
                orderCount = itemData['prices']['sell']['order_count']
            except (KeyError, TypeError):
                continue
            # evepraisal returns 0 if price data doesn't even exist for the item
            if price == 0:
                continue
            # evepraisal seems to provide price for some items despite having no orders up
            if orderCount < 1:
                continue
            priceMap[typeID].update(PriceStatus.fetchSuccess, price)
            del priceMap[typeID]


Price.register(EvePraisal)
