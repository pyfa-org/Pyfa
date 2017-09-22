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
        data = []
        baseurl = "https://eve-marketdata.com/api/item_prices.xml"
        data.append(("system_id", system))  # Use Jita for market
        data.append(("type_ids", ','.join(str(x) for x in types)))

        # Attempt to send request and process it
        try:
            network = Network.getInstance()
            data = network.request(baseurl, network.PRICES, data)
            xml = minidom.parse(data)
            print (xml.getElementsByTagName("eve").item(0))
            types = xml.getElementsByTagName("eve").item(0).getElementsByTagName("price")
            # Cycle through all types we've got from request
            for type_ in types:
                # Get data out of each typeID details tree
                typeID = int(type_.getAttribute("id"))
                price = 0

                try:
                    price = float(type_.firstChild.data)
                except (TypeError, ValueError):
                    pyfalog.warning("Failed to get price for: {0}", type_)

                # Fill price data
                priceobj = priceMap[typeID]
                priceobj.price = price
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


Price.register(EveMarketData)
