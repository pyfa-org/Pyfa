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

    name = "evemarketer"

    def __init__(self, priceMap, system, timeout):
        data = {}
        baseurl = "https://api.evemarketer.com/ec/marketstat"

        data["usesystem"] = system
        data["typeid"] = {typeID for typeID in priceMap}

        network = Network.getInstance()
        data = network.request(baseurl, network.PRICES, params=data, timeout=timeout)
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
                continue

            # Fill price data
            priceMap[typeID].update(PriceStatus.fetchSuccess, percprice)
            del priceMap[typeID]


Price.register(EveMarketer)
