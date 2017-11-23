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

    name = "eve-central.com"

    def __init__(self, types, system, priceMap):
        data = []
        baseurl = "https://eve-central.com/api/marketstat"
        data.append(("usesystem", system))  # Use Jita for market

        for typeID in types:  # Add all typeID arguments
            data.append(("typeid", typeID))

        # Attempt to send request and process it
        try:
            network = Network.getInstance()
            data = network.request(baseurl, network.PRICES, data)
            xml = minidom.parse(data)
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

        # If getting or processing data returned any errors
        except TimeoutError:
            # Timeout error deserves special treatment
            pyfalog.warning("Price fetch timout")
            for typeID in priceMap.keys():
                priceobj = priceMap[typeID]
                priceobj.time = time.time() + TIMEOUT
                priceobj.failed = True

                del priceMap[typeID]
        except:
            # all other errors will pass and continue onward to the REREQUEST delay
            pyfalog.warning("Caught exception in fetchPrices")
            pass
        pass


Price.register(EveCentral)
