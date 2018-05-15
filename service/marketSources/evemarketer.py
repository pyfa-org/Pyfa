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


class EveCentral(object):

    name = "evemarketer"

    def __init__(self, types, system, priceMap):
        data = {}
        baseurl = "https://api.evemarketer.com/ec/marketstat"

        data["usesystem"] = system  # Use Jita for market
        data["typeid"] = set()
        for typeID in types:  # Add all typeID arguments
            data["typeid"].add(typeID)

        network = Network.getInstance()
        data = network.request(baseurl, network.PRICES, params=data)
        xml = minidom.parseString(data.text)
        types = xml.getElementsByTagName("marketstat").item(0).getElementsByTagName("type")
        # Cycle through all types we've got from request
        for type_ in types:
            # Get data out of each typeID details tree
            typeID = int(type_.getAttribute("id"))
            sell = type_.getElementsByTagName("sell").item(0)
            # If price data wasn't there, set price to zero
            try:
                percprice = float(sell.getElementsByTagName("percentile").item(0).firstChild.data)
            except (TypeError, ValueError):
                pyfalog.warning("Failed to get price for: {0}", type_)
                percprice = 0

            # Fill price data
            priceobj = priceMap[typeID]
            priceobj.price = percprice
            priceobj.time = time.time() + VALIDITY
            priceobj.failed = None

            # delete price from working dict
            del priceMap[typeID]


Price.register(EveCentral)
