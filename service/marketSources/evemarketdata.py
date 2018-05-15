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

import time
from logbook import Logger
from xml.dom import minidom

from service.network import Network
from service.price import Price, VALIDITY, TIMEOUT, TimeoutError


pyfalog = Logger(__name__)


class EveMarketData(object):

    name = "eve-marketdata.com"

    def __init__(self, types, system, priceMap):
        data = {}
        baseurl = "https://eve-marketdata.com/api/item_prices.xml"
        data["system_id"] = system # Use Jita for market
        data["type_ids"] = ','.join(str(x) for x in types)

        network = Network.getInstance()
        data = network.request(baseurl, network.PRICES, params=data)
        xml = minidom.parseString(data.text)
        types = xml.getElementsByTagName("eve").item(0).getElementsByTagName("price")

        # Cycle through all types we've got from request
        for type_ in types:
            # Get data out of each typeID details tree
            typeID = int(type_.getAttribute("id"))

            try:
                price = float(type_.firstChild.data)
            except (TypeError, ValueError):
                pyfalog.warning("Failed to get price for: {0}", type_)

            # Fill price data
            priceobj = priceMap[typeID]

            # eve-marketdata returns 0 if price data doesn't even exist for the item. In this case, don't reset the
            # cached price, and set the price timeout to TIMEOUT (every 15 minutes currently). Se GH issue #1334
            if price != 0:
                priceobj.price = price
                priceobj.time = time.time() + VALIDITY
            else:
                priceobj.time = time.time() + TIMEOUT

            priceobj.failed = None

            # delete price from working dict
            del priceMap[typeID]


Price.register(EveMarketData)
