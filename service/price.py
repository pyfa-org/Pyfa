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
from xml.dom import minidom

from eos import db
from service.network import Network, TimeoutError
from service.fit import Fit
from logbook import Logger
from service.settings import NetworkSettings

pyfalog = Logger(__name__)


VALIDITY = 24 * 60 * 60  # Price validity period, 24 hours
REREQUEST = 4 * 60 * 60  # Re-request delay for failed fetches, 4 hours
TIMEOUT = 15 * 60  # Network timeout delay for connection issues, 15 minutes


class Price(object):
    systemsList = {
        "Jita": 30000142,
        "Amarr": 30002187,
        "Dodixie": 30002659,
        "Rens": 30002510,
        "Hek": 30002053
    }

    @classmethod
    def invalidPrices(cls, prices):
        for price in prices:
            price.time = 0

    @classmethod
    def fetchPrices(cls, prices):
        """Fetch all prices passed to this method"""

        # Dictionary for our price objects
        priceMap = {}
        # Check all provided price objects, and add invalid ones to dictionary
        for price in prices:
            if not price.isValid:
                priceMap[price.typeID] = price

        if len(priceMap) == 0:
            return

        # Set of items which are still to be requested from this service
        toRequest = set()

        # Compose list of items we're going to request
        for typeID in priceMap:
            # Get item object
            item = db.getItem(typeID)
            # We're not going to request items only with market group, as eve-central
            # doesn't provide any data for items not on the market
            if item is not None and item.marketGroupID:
                toRequest.add(typeID)

        # Do not waste our time if all items are not on the market
        if len(toRequest) == 0:
            return

        # This will store POST data for eve-central
        data = []

        sFit = Fit.getInstance()
        # Base request URL
        baseurl = "https://eve-central.com/api/marketstat"
        data.append(("usesystem", cls.systemsList[sFit.serviceFittingOptions["priceSystem"]]))  # Use Jita for market

        for typeID in toRequest:  # Add all typeID arguments
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

        # if we get to this point, then we've got an error. Set to REREQUEST delay
        for typeID in priceMap.keys():
            priceobj = priceMap[typeID]
            priceobj.time = time.time() + REREQUEST
            priceobj.failed = True

    @classmethod
    def fetchItemPrice(cls, item):
        """Fetch all prices passed to this method"""

        # Check if price is valid (within the time frame) or failed.
        if item.price.isValid and item.price.failed is not True:
            return item.price.price

        # We're not going to request items only with market group, as eve-central
        # doesn't provide any data for items not on the market
        if item is None or not item.marketGroupID:
            return 0

        network = Network.getInstance()
        settings = NetworkSettings.getInstance()

        if not settings.isEnabled(network.PRICES):
            # Network settings for fetching prices is disabled. Try and return the cache or return nothing.
            if item.price.price:
                return item.price.price
            else:
                return 0

        # This will store POST data for eve-central
        data = []

        sFit = Fit.getInstance()
        # Base request URL
        baseurl = "https://eve-central.com/api/marketstat"
        data.append(("usesystem", cls.systemsList[sFit.serviceFittingOptions["priceSystem"]]))  # Use Jita for market
        data.append(("typeid", item.ID))

        # Attempt to send request and process it
        try:
            data = network.request(baseurl, network.PRICES, data)
            xml = minidom.parse(data)
            types = xml.getElementsByTagName("marketstat").item(0).getElementsByTagName("type")
            # Cycle through all types we've got from request
            for type_ in types:
                # Get data out of each typeID details tree
                typeID = int(type_.getAttribute("id"))
                sell = type_.getElementsByTagName("sell").item(0)

                if item.ID != typeID:
                    pyfalog.warning("Type mismatch between passed in value ({0}) and returned value ({1}).", item.ID, typeID)
                    percprice = 0
                else:
                    # If price data wasn't there, set price to zero
                    try:
                        percprice = float(sell.getElementsByTagName("percentile").item(0).firstChild.data)
                    except (TypeError, ValueError):
                        pyfalog.warning("Failed to get price for: {0}", type_)
                        percprice = 0

                # Fill price data
                priceobj = item.price
                priceobj.price = percprice
                priceobj.time = time.time() + VALIDITY
                priceobj.failed = None

            return item.price.price

        # If getting or processing data returned any errors
        except TimeoutError:
            # Timeout error deserves special treatment
            pyfalog.warning("Price fetch timout")
            priceobj = item.price
            priceobj.time = time.time() + TIMEOUT
            priceobj.failed = True
            return 0
        except:
            # all other errors will pass and continue onward to the REREQUEST delay
            pyfalog.warning("Caught exception in fetchPrices")

        # if we get to this point, then we've got an error. Set to REREQUEST delay
        priceobj = item.price
        priceobj.time = time.time() + REREQUEST
        priceobj.failed = True
        return 0
